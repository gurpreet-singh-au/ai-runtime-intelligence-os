#!/usr/bin/env python3
"""Stage A attribution audit for B2-ATTR-001.

This script exhausts evidence already present in local Claude Code artifacts before
any new instrumentation is introduced. It is deliberately conservative:

- directly visible facts are OBSERVED;
- arithmetic over observed values is DERIVED;
- plausible interpretation without direct composition evidence is INFERRED;
- unavailable composition remains UNKNOWN, never zero.

The audit does not claim that provider-reported cache-read tokens equal unique
semantic context, and it does not claim causal attribution from event correlation.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_RUNS = [
    "B2-001-baseline-r02",
    "B2-001-baseline-r03",
    "B2-001-baseline-r04",
    "B2-001-baseline-r05",
    "B2-001-baseline-r06",
]


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
    return raw.decode("utf-8", errors="replace")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        obj = json.loads(read_text_portable(path).lstrip("\ufeff"))
        return obj if isinstance(obj, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    for raw_line in read_text_portable(path).splitlines():
        line = raw_line.strip().lstrip("\ufeff")
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            out.append(obj)
    return out


def walk(obj: Any, prefix: str = ""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            yield path, value
            yield from walk(value, path)
    elif isinstance(obj, list):
        for value in obj:
            path = f"{prefix}[]"
            yield path, value
            yield from walk(value, path)


def text_size(value: Any) -> int:
    if isinstance(value, str):
        return len(value)
    if isinstance(value, (dict, list)):
        try:
            return len(json.dumps(value, ensure_ascii=False))
        except TypeError:
            return 0
    return 0


def message_blocks(event: dict[str, Any]) -> list[dict[str, Any]]:
    message = event.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, list):
        return []
    return [b for b in content if isinstance(b, dict)]


def extract_usage_snapshots(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collect usage-bearing objects without summing them.

    These may overlap/cumulate; they are evidence of per-step visibility only, not
    additive totals. The final modelUsage remains the authoritative run aggregate.
    """
    snapshots: list[dict[str, Any]] = []
    for i, event in enumerate(events, start=1):
        for path, value in walk(event):
            low = path.lower()
            if path.endswith("modelUsage"):
                continue
            if isinstance(value, dict) and (
                path.endswith("usage") or "usage" in low
            ) and any(
                k in value
                for k in (
                    "input_tokens",
                    "output_tokens",
                    "cache_read_input_tokens",
                    "cache_creation_input_tokens",
                    "inputTokens",
                    "outputTokens",
                    "cacheReadInputTokens",
                    "cacheCreationInputTokens",
                )
            ):
                snapshots.append({"event_index": i, "path": path, "value": value})
    return snapshots


def audit_run(run_id: str, artifacts: Path) -> dict[str, Any]:
    events = load_jsonl(artifacts / "claude-stream.jsonl")
    normalized = load_json(artifacts / "normalized-run.json")
    outcome = load_json(artifacts / "B2_OUTCOME_EVALUATION.json")
    metadata = load_json(artifacts / "RUN_METADATA.json")
    inventory = load_json(artifacts / "STREAM_INVENTORY.json")

    tool_sequence: list[str] = []
    tool_input_chars: Counter[str] = Counter()
    tool_result_chars = 0
    assistant_text_chars = 0
    user_text_chars = 0
    system_event_count = 0
    event_types: Counter[str] = Counter()
    agent_like_paths: Counter[str] = Counter()
    instruction_like_paths: Counter[str] = Counter()
    context_like_paths: Counter[str] = Counter()

    for event in events:
        event_type = str(event.get("type", "<unknown>"))
        event_types[event_type] += 1
        if event_type == "system":
            system_event_count += 1

        for path, value in walk(event):
            low = path.lower()
            if any(k in low for k in ("agent", "subagent", "delegate")):
                agent_like_paths[path] += 1
            if any(k in low for k in ("instruction", "system_prompt", "systemprompt")):
                instruction_like_paths[path] += 1
            if any(k in low for k in ("context", "prompt", "message")):
                context_like_paths[path] += 1

        for block in message_blocks(event):
            btype = block.get("type")
            if btype == "tool_use":
                name = str(block.get("name", "unknown"))
                tool_sequence.append(name)
                tool_input_chars[name] += text_size(block.get("input"))
            elif btype == "tool_result":
                tool_result_chars += text_size(block.get("content"))
            elif btype == "text":
                role = None
                msg = event.get("message")
                if isinstance(msg, dict):
                    role = msg.get("role")
                size = text_size(block.get("text"))
                if role == "assistant":
                    assistant_text_chars += size
                elif role == "user":
                    user_text_chars += size

    resources = normalized.get("resources") if isinstance(normalized.get("resources"), dict) else {}
    env = normalized.get("environment") if isinstance(normalized.get("environment"), dict) else {}
    cost = normalized.get("cost") if isinstance(normalized.get("cost"), dict) else {}
    snapshots = extract_usage_snapshots(events)

    return {
        "run_id": run_id,
        "valid_success": outcome.get("success") is True and outcome.get("mandatory_compliance") is True,
        "event_count": len(events),
        "event_types": dict(event_types),
        "system_event_count": system_event_count,
        "tool_sequence": tool_sequence,
        "tool_input_chars_by_tool": dict(tool_input_chars),
        "tool_result_chars_visible_in_message_blocks": tool_result_chars,
        "assistant_text_chars_visible_in_message_blocks": assistant_text_chars,
        "user_text_chars_visible_in_message_blocks": user_text_chars,
        "usage_snapshot_count_nonadditive": len(snapshots),
        "usage_snapshot_paths": sorted({s["path"] for s in snapshots}),
        "agent_like_paths": dict(agent_like_paths),
        "instruction_like_paths": dict(instruction_like_paths),
        "context_like_path_count": len(context_like_paths),
        "inventory_agent_like_paths": inventory.get("agent_like_paths", []),
        "observed_models": env.get("models_observed"),
        "per_model_usage": env.get("per_model_usage"),
        "resources": {
            "input_tokens": resources.get("input_tokens"),
            "cached_input_tokens": resources.get("cached_input_tokens"),
            "cache_creation_input_tokens": resources.get("cache_creation_input_tokens"),
            "output_tokens": resources.get("output_tokens"),
            "tool_calls": resources.get("tool_calls"),
            "duration_ms": resources.get("duration_ms"),
            "cost_usd": cost.get("total"),
        },
        "metadata_runtime": metadata.get("runtime"),
        "metadata_runtime_version": metadata.get("runtime_version") or metadata.get("claude_version"),
    }


def class_record(source_class: str, status: str, direct: list[str], derived: list[str], unresolved: list[str]) -> dict[str, Any]:
    return {
        "source_class": source_class,
        "status": status,
        "directly_observed": direct,
        "derived_or_inferred": derived,
        "unresolved": unresolved,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("experiments/local-runs"))
    parser.add_argument("--runs", nargs="*", default=DEFAULT_RUNS)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    runs: list[dict[str, Any]] = []
    missing: list[str] = []
    for run_id in args.runs:
        artifacts = args.root / run_id / "artifacts"
        if not artifacts.exists():
            missing.append(run_id)
            continue
        runs.append(audit_run(run_id, artifacts))

    all_agent_paths = sorted({p for run in runs for p in run.get("agent_like_paths", {})})
    all_instruction_paths = sorted({p for run in runs for p in run.get("instruction_like_paths", {})})
    all_usage_paths = sorted({p for run in runs for p in run.get("usage_snapshot_paths", [])})
    tool_names = sorted({name for run in runs for name in run.get("tool_sequence", [])})

    attribution_gap_table = [
        class_record(
            "provider/system instructions",
            "PARTIAL/UNKNOWN",
            ["system event presence/count is observable"] if any(r["system_event_count"] for r in runs) else [],
            [],
            ["system-instruction text/token contribution", "provider-hidden prompt/cache contribution"],
        ),
        class_record(
            "project/repository instructions and governance",
            "UNKNOWN",
            [f"instruction-like stream paths: {all_instruction_paths}"] if all_instruction_paths else [],
            ["repository files read may be visible via tool sequence/results, but visibility is not proof they were retained in model context"],
            ["tokens attributable specifically to repository governance/instruction material"],
        ),
        class_record(
            "task prompt",
            "PARTIAL",
            ["benchmark prompt is frozen outside the runtime stream; user/message blocks may expose some submitted text"],
            ["character length can be measured from artifact/repository prompt, but exact provider tokenization/caching class is not established"],
            ["exact task-prompt tokens inside each processed request", "cache-hit status of task-prompt segments"],
        ),
        class_record(
            "tool schemas/capability descriptions",
            "PARTIAL/UNKNOWN",
            [f"invoked tool names observable: {tool_names}"],
            ["tool input payload character sizes are measurable for invoked tools"],
            ["full exposed tool-schema text/tokens per request", "schemas for available-but-unused tools"],
        ),
        class_record(
            "repository/file content supplied to model",
            "PARTIAL",
            ["Read/Glob/Bash/Edit/PowerShell tool use and visible tool-result content can be enumerated"],
            ["visible tool-result character volume is measurable; it is not equivalent to provider-token contribution or retained context"],
            ["per-file token contribution to each model request", "retention/eviction/summarization behavior"],
        ),
        class_record(
            "conversation and prior tool-result history",
            "PARTIAL",
            ["message/tool-result blocks and their visible character volume can be enumerated", f"non-additive usage snapshot paths: {all_usage_paths}" if all_usage_paths else ""],
            ["event order provides trajectory evidence; usage snapshots may reveal context growth if semantics are cumulative, but that must be validated before arithmetic"],
            ["exact history tokens included in each request", "provider compaction/summarization boundaries"],
        ),
        class_record(
            "agent/subagent or internal utility activity",
            "PARTIAL/UNKNOWN",
            [f"agent-like stream paths: {all_agent_paths}"] if all_agent_paths else [],
            ["multiple models are directly reported in aggregate modelUsage; this alone does not identify a subagent"],
            ["agent lineage", "subagent count", "reason for secondary-model invocation", "per-call parent/child mapping"],
        ),
        class_record(
            "other provider/runtime overhead",
            "UNKNOWN",
            [],
            ["residual overhead exists by definition if observed aggregate usage cannot be assigned to visible classes"],
            ["magnitude and composition of hidden provider/runtime overhead"],
        ),
    ]

    # Remove empty placeholder strings while keeping the schema compact.
    for row in attribution_gap_table:
        row["directly_observed"] = [x for x in row["directly_observed"] if x]
        row["derived_or_inferred"] = [x for x in row["derived_or_inferred"] if x]

    report = {
        "experiment_id": "B2-ATTR-001",
        "stage": "A",
        "purpose": "Exhaust existing B2 baseline artifacts before adding instrumentation.",
        "runs_requested": args.runs,
        "runs_audited": [r["run_id"] for r in runs],
        "missing_runs": missing,
        "all_audited_runs_valid_success": bool(runs) and all(r["valid_success"] for r in runs),
        "runs": runs,
        "attribution_gap_table": attribution_gap_table,
        "stage_a_decision_rule": {
            "if_primary_composition_resolved": "Proceed to select one isolated intervention.",
            "if_primary_composition_unresolved": "Proceed to Stage B and select the smallest additional observation layer that exposes the unresolved composition fields.",
        },
        "interpretation_guardrails": [
            "Do not sum overlapping usage snapshots unless their semantics are proven non-overlapping.",
            "Do not treat visible character counts as token counts.",
            "Do not treat provider-reported cache-read tokens as unique semantic context size.",
            "Do not infer that a second observed model equals a subagent without lineage evidence.",
            "UNKNOWN is not zero.",
        ],
    }

    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote Stage A attribution audit: {args.output}")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
