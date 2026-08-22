#!/usr/bin/env python3
"""Deterministically evaluate a Codex B2-001 discovery run.

The model's own success claim is never trusted. This is discovery-only evidence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
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
    try:
        obj = json.loads(read_text(path).lstrip("\ufeff"))
        return obj if isinstance(obj, dict) else {}
    except json.JSONDecodeError:
        return {}


def changed_paths(diff_text: str) -> list[str]:
    paths: list[str] = []
    for line in diff_text.splitlines():
        if line.startswith("diff --git a/"):
            parts = line.split()
            if len(parts) >= 4 and parts[3].startswith("b/"):
                paths.append(parts[3][2:])
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifacts", type=Path)
    args = parser.parse_args()
    artifacts = args.artifacts.resolve()

    metadata = load_json(artifacts / "RUN_METADATA.json")
    diff_text = read_text(artifacts / "git-diff.patch")
    tests_before = read_text(artifacts / "tests-before.txt")
    tests_after = read_text(artifacts / "tests-after.txt")
    paths = changed_paths(diff_text)

    checks = {
        "codex_exit_zero": metadata.get("codex_exit_code") == 0,
        "fixture_failed_before": isinstance(metadata.get("tests_before_exit_code"), int) and metadata.get("tests_before_exit_code") != 0,
        "tests_passed_after": metadata.get("tests_after_exit_code") == 0,
        "pre_test_evidence_present": bool(tests_before.strip()),
        "post_test_evidence_present": bool(tests_after.strip()),
        "diff_present": bool(diff_text.strip()),
        "only_pricing_changed": paths == ["runtime_fixture/pricing.py"],
        "tests_untouched": all(not p.startswith("tests/") for p in paths),
        "intended_formula_present": "discounted_subtotal = subtotal *" in diff_text and "discounted_subtotal + shipping" in diff_text,
    }
    success = all(checks.values())
    evaluation = {
        "benchmark_id": "B2-001",
        "run_id": metadata.get("run_id"),
        "runtime": "Codex CLI",
        "evaluator_id": "B2-001-deterministic-tests-and-diff-v1",
        "evaluator_version": "1.1-codex-adapter",
        "success": success,
        "mandatory_compliance": success,
        "checks": checks,
        "changed_paths": paths,
        "benchmark_comparison_eligible": False,
        "note": "Discovery-run evaluator. Same deterministic task acceptance logic as Claude B2 evaluator; runtime exit field is Codex-specific.",
    }
    (artifacts / "B2_OUTCOME_EVALUATION.json").write_text(json.dumps(evaluation, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "run_id": evaluation["run_id"],
        "success": success,
        "mandatory_compliance": success,
        "changed_paths": paths,
    }, indent=2))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
