#!/usr/bin/env python3
"""Aggregate valid B2-001 baseline runs from experiments/local-runs.

Reads each run's normalized-run.json and B2_OUTCOME_EVALUATION.json, excludes
invalid/failed runs, and prints descriptive statistics for the first baseline
series. This tool is intentionally local-artifact only: experiment run data
remains outside GitHub unless deliberately summarized later.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def number(value: Any) -> float | None:
    return float(value) if isinstance(value, (int, float)) else None


def stat(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"n": 0, "mean": None, "median": None, "min": None, "max": None, "stdev": None, "cv": None}
    mean = statistics.mean(values)
    stdev = statistics.stdev(values) if len(values) >= 2 else 0.0
    return {
        "n": len(values),
        "mean": mean,
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
        "stdev": stdev,
        "cv": (stdev / mean) if mean else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("experiments/local-runs"),
        help="Local run root (default: experiments/local-runs)",
    )
    parser.add_argument(
        "--runs",
        nargs="*",
        default=["B2-001-baseline-r02", "B2-001-baseline-r03", "B2-001-baseline-r04", "B2-001-baseline-r05"],
        help="Run IDs to inspect",
    )
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []

    for run_id in args.runs:
        artifacts = args.root / run_id / "artifacts"
        outcome = load_json(artifacts / "B2_OUTCOME_EVALUATION.json")
        normalized = load_json(artifacts / "normalized-run.json")
        if outcome.get("success") is not True or outcome.get("mandatory_compliance") is not True:
            excluded.append({"run_id": run_id, "reason": "deterministic outcome not PASS"})
            continue
        if not normalized:
            excluded.append({"run_id": run_id, "reason": "normalized-run.json missing/unreadable"})
            continue

        resources = normalized.get("resources") if isinstance(normalized.get("resources"), dict) else {}
        cost = normalized.get("cost") if isinstance(normalized.get("cost"), dict) else {}
        environment = normalized.get("environment") if isinstance(normalized.get("environment"), dict) else {}
        rows.append(
            {
                "run_id": run_id,
                "cost_usd": number(cost.get("total")),
                "duration_ms": number(resources.get("duration_ms")),
                "input_tokens": number(resources.get("input_tokens")),
                "cached_input_tokens": number(resources.get("cached_input_tokens")),
                "cache_creation_input_tokens": number(resources.get("cache_creation_input_tokens")),
                "output_tokens": number(resources.get("output_tokens")),
                "tool_calls": number(resources.get("tool_calls")),
                "models_observed": environment.get("models_observed"),
            }
        )

    metrics = [
        "cost_usd",
        "duration_ms",
        "input_tokens",
        "cached_input_tokens",
        "cache_creation_input_tokens",
        "output_tokens",
        "tool_calls",
    ]
    summary = {
        "benchmark_id": "B2-001",
        "requested_runs": args.runs,
        "valid_runs": [row["run_id"] for row in rows],
        "excluded_runs": excluded,
        "success_rate_within_requested_runs": (len(rows) / len(args.runs)) if args.runs else None,
        "runs": rows,
        "statistics": {
            metric: stat([row[metric] for row in rows if row[metric] is not None])
            for metric in metrics
        },
        "interpretation_guardrails": [
            "Descriptive baseline statistics only; do not infer causality from correlations.",
            "Do not claim intervention savings until a frozen intervention is compared against this baseline with non-inferior deterministic outcomes.",
            "Cached-input tokens are provider-reported processing/cache usage, not unique semantic context size.",
        ],
    }

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
