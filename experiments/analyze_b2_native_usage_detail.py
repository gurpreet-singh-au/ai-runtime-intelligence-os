#!/usr/bin/env python3
"""Deep native-evidence pass for B2-ATTR-001 Stage A.

This script inspects fields already present in Claude Code stream-json captures that
were surfaced by the first Stage A inventory. It does not add instrumentation.

Focus:
- exact final result subagent_stats values;
- exact agent catalogue values if present;
- result usage.iterations structure and values;
- message-level usage sequence by event index;
- final per-model aggregate usage;
- tool trajectory.

Usage objects are emitted as evidence and are NOT summed unless their semantics are
known to be non-overlapping. UNKNOWN remains UNKNOWN.
"""

from __future__ import annotations

import argparse
import json
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


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for raw in read_text_portable(path).splitlines():
        line = raw.strip().lstrip("\ufeff")
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            events.append(obj)
    return events


def find_result(events: list[dict[str, Any]]) -> dict[str, Any]:
    for event in reversed(events):
        if event.get("type") == "result":
            return event
        if event.get("type") == "system" and event.get("subtype") == "result":
            return event
    return {}


def compact_usage(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    keys = (
        "input_tokens", "output_tokens", "cache_read_input_tokens",
        "cache_creation_input_tokens", "inputTokens", "outputTokens",
        "cacheReadInputTokens", "cacheCreationInputTokens", "cost_usd",
        "costUSD", "model", "model_name", "modelName",
    )
    compact = {k: value[k] for k in keys if k in value}
    return compact if compact else value


def tool_sequence(events: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for event in events:
        message = event.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                names.append(str(block.get("name", "unknown")))
    return names


def message_usage_sequence(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx, event in enumerate(events, start=1):
        message = event.get("message")
        if not isinstance(message, dict):
            continue
        usage = message.get("usage")
        if isinstance(usage, dict):
            out.append({
                "event_index": idx,
                "event_type": event.get("type"),
                "role": message.get("role"),
                "usage": compact_usage(usage),
            })
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("experiments/local-runs"))
    parser.add_argument("--runs", nargs="*", default=DEFAULT_RUNS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    audited: list[dict[str, Any]] = []
    for run_id in args.runs:
        artifacts = args.root / run_id / "artifacts"
        events = load_jsonl(artifacts / "claude-stream.jsonl")
        result = find_result(events)
        if not events:
            audited.append({"run_id": run_id, "error": "stream missing/unreadable"})
            continue

        usage = result.get("usage") if isinstance(result.get("usage"), dict) else {}
        iterations = usage.get("iterations") if isinstance(usage.get("iterations"), list) else []
        subagent_stats = result.get("subagent_stats") if isinstance(result.get("subagent_stats"), dict) else None
        agents = result.get("agents") if isinstance(result.get("agents"), list) else None

        audited.append({
            "run_id": run_id,
            "event_count": len(events),
            "tool_sequence": tool_sequence(events),
            "final_result": {
                "agents": agents,
                "subagent_stats": subagent_stats,
                "usage_top_level_without_iterations": {
                    k: compact_usage(v)
                    for k, v in usage.items()
                    if k != "iterations"
                },
                "usage_iterations_count": len(iterations),
                "usage_iterations": [
                    {"iteration_index": i + 1, "value": compact_usage(v)}
                    for i, v in enumerate(iterations)
                ],
                "modelUsage": result.get("modelUsage") if isinstance(result.get("modelUsage"), dict) else None,
                "duration_ms": result.get("duration_ms"),
                "total_cost_usd": result.get("total_cost_usd"),
            },
            "message_usage_sequence": message_usage_sequence(events),
        })

    all_subagent_stats_present = all(
        isinstance(r.get("final_result", {}).get("subagent_stats"), dict)
        for r in audited if "error" not in r
    )
    spawned_values = [
        r["final_result"]["subagent_stats"].get("spawned")
        for r in audited
        if isinstance(r.get("final_result", {}).get("subagent_stats"), dict)
    ]
    observed_zero_spawn_all = bool(spawned_values) and all(v == 0 for v in spawned_values)

    report = {
        "experiment_id": "B2-ATTR-001",
        "stage": "A-native-detail",
        "runs": audited,
        "cross_run_findings": {
            "subagent_stats_present_all_readable_runs": all_subagent_stats_present,
            "subagent_spawned_values": spawned_values,
            "subagents_spawned_zero_all_runs": observed_zero_spawn_all,
            "interpretation": (
                "If subagent_stats.spawned is explicitly 0 in every run, spawned subagents are OBSERVED absent for this baseline series. "
                "A secondary model in modelUsage must therefore not be labelled a spawned subagent without contrary lineage evidence."
                if observed_zero_spawn_all else
                "Subagent activity is not uniformly resolved by the observed final-result field."
            ),
        },
        "guardrails": [
            "Do not sum message usage, result usage and iteration usage together; these may overlap.",
            "Do not assume usage.iterations are incremental rather than cumulative without runtime documentation or an internally consistent proof.",
            "Do not equate a listed agent catalogue with an actually spawned agent.",
            "Do not infer the purpose of a secondary model call merely from model identity.",
            "Provider-reported cache-read tokens are not unique semantic context size.",
        ],
    }

    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote native detail audit: {args.output}")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
