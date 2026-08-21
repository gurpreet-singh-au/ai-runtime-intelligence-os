#!/usr/bin/env python3
"""Conservative Claude Code baseline normalizer.

Reads a run artifact directory produced by the tranche-01 runner and emits a
provider-neutral `normalized-run.json` plus a telemetry completeness report.

Design rule: never convert unavailable evidence into zero. Every extracted
field carries an evidence class: OBSERVED, DERIVED, INFERRED, or UNKNOWN.

Windows PowerShell 5.1 may write redirected native-process output as UTF-16 and
JSON files with a UTF-8 BOM, so artifact readers detect common encodings.

Usage extraction deliberately prefers the final result event's `modelUsage`
summary when present. That object is a per-model run summary and avoids the
recursive double counting that occurs when message-level usage, result-level
usage and iteration-level usage are all summed together.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EVIDENCE_LEVELS = {"OBSERVED", "DERIVED", "INFERRED", "UNKNOWN"}


def read_text_portable(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16")
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig")
    if raw and raw.count(b"\x00") > len(raw) // 10:
        try:
            return raw.decode("utf-16-le")
        except UnicodeDecodeError:
            pass
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(read_text_portable(path).lstrip("\ufeff"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in read_text_portable(path).splitlines():
        line = line.strip().lstrip("\ufeff")
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            events.append(obj)
    return events


def evidence(value: Any = None, level: str = "UNKNOWN", source: str | None = None) -> dict[str, Any]:
    if level not in EVIDENCE_LEVELS:
        raise ValueError(f"invalid evidence level: {level}")
    return {"value": value, "evidence": level, "source": source}


def find_result_event(events: list[dict[str, Any]]) -> dict[str, Any]:
    for event in reversed(events):
        if event.get("type") == "result":
            return event
        if event.get("type") == "system" and event.get("subtype") == "result":
            return event
    return {}


def _number(value: Any) -> int | None:
    if isinstance(value, (int, float)) and value >= 0:
        return int(value)
    return None


def extract_result_usage(result: dict[str, Any]) -> tuple[dict[str, int], dict[str, Any], str]:
    """Extract non-overlapping run usage from the final result event.

    Priority:
    1. `modelUsage`: sum each model's final aggregate exactly once. This captures
       helper/secondary model activity without counting the same message usage again.
    2. top-level `usage`: use the final aggregate once when modelUsage is absent.
    3. no aggregate: return empty and leave usage UNKNOWN rather than invent totals.
    """
    model_usage = result.get("modelUsage")
    if isinstance(model_usage, dict) and model_usage:
        totals = {
            "input_tokens": 0,
            "cache_read_input_tokens": 0,
            "cache_creation_input_tokens": 0,
            "output_tokens": 0,
        }
        models: dict[str, Any] = {}
        seen_any = False
        for model_name, raw in model_usage.items():
            if not isinstance(raw, dict):
                continue
            mapped = {
                "input_tokens": _number(raw.get("inputTokens")),
                "cache_read_input_tokens": _number(raw.get("cacheReadInputTokens")),
                "cache_creation_input_tokens": _number(raw.get("cacheCreationInputTokens")),
                "output_tokens": _number(raw.get("outputTokens")),
                "cost_usd": raw.get("costUSD") if isinstance(raw.get("costUSD"), (int, float)) else None,
                "context_window": _number(raw.get("contextWindow")),
                "max_output_tokens": _number(raw.get("maxOutputTokens")),
                "canonical_model": raw.get("canonicalModel"),
                "provider": raw.get("provider"),
            }
            models[str(model_name)] = mapped
            for key in totals:
                value = mapped.get(key)
                if value is not None:
                    totals[key] += int(value)
                    seen_any = True
        return (totals if seen_any else {}), models, "claude-stream.jsonl:result.modelUsage"

    usage = result.get("usage")
    if isinstance(usage, dict):
        mapped = {
            "input_tokens": _number(usage.get("input_tokens")),
            "cache_read_input_tokens": _number(usage.get("cache_read_input_tokens")),
            "cache_creation_input_tokens": _number(usage.get("cache_creation_input_tokens")),
            "output_tokens": _number(usage.get("output_tokens")),
        }
        totals = {key: value for key, value in mapped.items() if value is not None}
        if totals:
            return totals, {}, "claude-stream.jsonl:result.usage"

    return {}, {}, ""


def detect_tool_events(events: list[dict[str, Any]]) -> tuple[int | None, list[str]]:
    tool_names: list[str] = []
    for event in events:
        message = event.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        blocks = content if isinstance(content, list) else []
        for block in blocks:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                name = block.get("name")
                tool_names.append(str(name) if name is not None else "unknown")
    return (len(tool_names), tool_names) if tool_names else (None, [])


def parse_iso(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def normalize(run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    metadata = load_json(run_dir / "RUN_METADATA.json")
    events = load_jsonl(run_dir / "claude-stream.jsonl")
    result = find_result_event(events)
    usage, per_model_usage, usage_source = extract_result_usage(result)
    tool_count, tool_names = detect_tool_events(events)

    started = metadata.get("started_at") or metadata.get("startedAt")
    ended = metadata.get("ended_at") or metadata.get("endedAt")
    duration_ms: int | None = None
    duration_source: str | None = None
    duration_level = "UNKNOWN"

    if isinstance(result.get("duration_ms"), (int, float)):
        duration_ms = int(result["duration_ms"])
        duration_source = "claude-stream.jsonl:result.duration_ms"
        duration_level = "OBSERVED"
    else:
        start_dt, end_dt = parse_iso(started), parse_iso(ended)
        if start_dt and end_dt:
            duration_ms = max(0, int((end_dt - start_dt).total_seconds() * 1000))
            duration_source = "RUN_METADATA.json timestamps"
            duration_level = "DERIVED"
        elif isinstance(metadata.get("duration_ms"), (int, float)):
            duration_ms = int(metadata["duration_ms"])
            duration_source = "RUN_METADATA.json:duration_ms"
            duration_level = "OBSERVED"

    total_cost = result.get("total_cost_usd")
    cost_level = "OBSERVED" if isinstance(total_cost, (int, float)) else "UNKNOWN"

    run_id = metadata.get("run_id") or metadata.get("runId") or run_dir.parent.name or run_dir.name
    benchmark_id = metadata.get("benchmark_id") or metadata.get("benchmarkId") or "B2-001"
    model_names = list(per_model_usage.keys())

    normalized = {
        "schema_version": "0.1",
        "run_id": run_id,
        "benchmark_id": benchmark_id,
        "policy_variant": metadata.get("policy_variant") or "baseline",
        "started_at": started or datetime.now(timezone.utc).isoformat(),
        "ended_at": ended,
        "environment": {
            "runtime": metadata.get("runtime") or "claude-code",
            "runtime_version": metadata.get("runtime_version") or metadata.get("claude_version"),
            "task_snapshot": metadata.get("task_snapshot") or metadata.get("repository_commit") or "unknown",
            "repository_commit": metadata.get("repository_commit"),
            "provider": metadata.get("provider") or "Anthropic",
            "model": result.get("model") or (model_names[0] if len(model_names) == 1 else None),
            "models_observed": model_names,
            "per_model_usage": per_model_usage,
            "model_version": metadata.get("model_version"),
            "reasoning_effort": metadata.get("reasoning_effort"),
        },
        "resources": {
            "input_tokens": usage.get("input_tokens"),
            "cached_input_tokens": usage.get("cache_read_input_tokens"),
            "cache_creation_input_tokens": usage.get("cache_creation_input_tokens"),
            "output_tokens": usage.get("output_tokens"),
            "reasoning_tokens_or_units": None,
            "context_peak_tokens": None,
            "instruction_tokens": None,
            "model_calls": None,
            "agent_count": None,
            "subagent_count": None,
            "tool_calls": tool_count,
            "repeated_tool_calls": None,
            "verification_calls": None,
            "duration_ms": duration_ms,
        },
        "cost": {
            "currency": "USD",
            "model": total_cost if isinstance(total_cost, (int, float)) else None,
            "tools": None,
            "verification": None,
            "infrastructure": None,
            "human_review": None,
            "total": total_cost if isinstance(total_cost, (int, float)) else None,
        },
        "progress": {
            "useful_state_changes": None,
            "no_progress_intervals": None,
            "repeated_operation_groups": None,
        },
        "outcome": {
            "success": False,
            "quality_score": None,
            "reliability_score": None,
            "mandatory_compliance": False,
            "safety_compliance": None,
            "grounding_score": None,
            "human_correction_required": None,
            "residual_risk": None,
            "evaluator_id": "B2-001-deterministic-tests-v1",
            "evaluator_version": "1",
            "notes": "Outcome must be finalized from deterministic benchmark tests; model output is not treated as proof of success.",
        },
        "interventions": [],
        "evidence_refs": [name for name in ["RUN_METADATA.json", "claude-stream.jsonl", "tests-after.txt", "git-diff.patch"] if (run_dir / name).exists()],
    }

    field_evidence = {
        "resources.input_tokens": evidence(normalized["resources"]["input_tokens"], "OBSERVED" if "input_tokens" in usage else "UNKNOWN", usage_source or None),
        "resources.cached_input_tokens": evidence(normalized["resources"]["cached_input_tokens"], "OBSERVED" if "cache_read_input_tokens" in usage else "UNKNOWN", usage_source or None),
        "resources.cache_creation_input_tokens": evidence(normalized["resources"]["cache_creation_input_tokens"], "OBSERVED" if "cache_creation_input_tokens" in usage else "UNKNOWN", usage_source or None),
        "resources.output_tokens": evidence(normalized["resources"]["output_tokens"], "OBSERVED" if "output_tokens" in usage else "UNKNOWN", usage_source or None),
        "resources.tool_calls": evidence(tool_count, "OBSERVED" if tool_count is not None else "UNKNOWN", "assistant tool_use blocks" if tool_count is not None else None),
        "resources.duration_ms": evidence(duration_ms, duration_level, duration_source),
        "cost.total": evidence(normalized["cost"]["total"], cost_level, "claude-stream.jsonl:result.total_cost_usd" if cost_level == "OBSERVED" else None),
        "resources.context_peak_tokens": evidence(),
        "resources.instruction_tokens": evidence(),
        "resources.model_calls": evidence(),
        "resources.agent_count": evidence(),
        "resources.subagent_count": evidence(),
        "resources.repeated_tool_calls": evidence(),
        "progress.useful_state_changes": evidence(),
        "progress.no_progress_intervals": evidence(),
    }

    known = sum(1 for item in field_evidence.values() if item["evidence"] != "UNKNOWN")
    completeness = round(known / len(field_evidence), 4) if field_evidence else 0.0

    report = {
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "telemetry_completeness_ratio": completeness,
        "field_evidence": field_evidence,
        "observed_tool_names": tool_names,
        "models_observed": model_names,
        "per_model_usage": per_model_usage,
        "stream_event_count": len(events),
        "result_event_present": bool(result),
        "decision": "AUDIT_BEFORE_MORE_RUNS",
        "notes": [
            "UNKNOWN means unavailable, not zero.",
            "Token totals prefer result.modelUsage and do not recursively sum message/result/iteration usage.",
            "Deterministic outcome must be populated from benchmark tests.",
            "Do not run further repetitions until telemetry gaps and outcome capture are reviewed.",
        ],
    }
    return normalized, report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    normalized, report = normalize(run_dir)
    (run_dir / "normalized-run.json").write_text(json.dumps(normalized, indent=2) + "\n", encoding="utf-8")
    (run_dir / "TELEMETRY_COMPLETENESS.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": normalized["run_id"], "telemetry_completeness_ratio": report["telemetry_completeness_ratio"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
