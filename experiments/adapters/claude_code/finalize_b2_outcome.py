#!/usr/bin/env python3
"""Finalize B2-001 outcome from deterministic benchmark evidence.

This script never trusts the model's own success claim. A successful B2 run requires:
- Claude process exit code == 0;
- pre-test exit code != 0 (fixture was actually broken before execution);
- post-test exit code == 0;
- a non-empty diff;
- the diff changes only runtime_fixture/pricing.py;
- the diff does not modify tests/;
- the intended shipping-after-discount implementation appears in the diff.

It updates normalized-run.json in place and emits B2_OUTCOME_EVALUATION.json.
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
            if len(parts) >= 3 and parts[2].startswith("b/"):
                paths.append(parts[2][2:])
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()

    metadata = load_json(run_dir / "RUN_METADATA.json")
    normalized = load_json(run_dir / "normalized-run.json")
    diff_text = read_text(run_dir / "git-diff.patch")
    tests_before = read_text(run_dir / "tests-before.txt")
    tests_after = read_text(run_dir / "tests-after.txt")

    paths = changed_paths(diff_text)
    checks = {
        "claude_exit_zero": metadata.get("claude_exit_code") == 0,
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
        "benchmark_id": metadata.get("benchmark_id"),
        "run_id": metadata.get("run_id"),
        "evaluator_id": "B2-001-deterministic-tests-and-diff-v1",
        "evaluator_version": "1",
        "success": success,
        "mandatory_compliance": success,
        "checks": checks,
        "changed_paths": paths,
        "evidence_refs": [
            "RUN_METADATA.json",
            "tests-before.txt",
            "tests-after.txt",
            "git-diff.patch",
        ],
    }

    outcome = normalized.setdefault("outcome", {})
    outcome.update(
        {
            "success": success,
            "mandatory_compliance": success,
            "evaluator_id": evaluation["evaluator_id"],
            "evaluator_version": evaluation["evaluator_version"],
            "notes": (
                "Deterministic B2 evaluation passed: broken fixture before run, all tests passed after run, "
                "and only the intended pricing implementation changed."
                if success
                else "Deterministic B2 evaluation failed; inspect B2_OUTCOME_EVALUATION.json checks."
            ),
        }
    )

    refs = normalized.setdefault("evidence_refs", [])
    if "B2_OUTCOME_EVALUATION.json" not in refs:
        refs.append("B2_OUTCOME_EVALUATION.json")

    (run_dir / "normalized-run.json").write_text(json.dumps(normalized, indent=2) + "\n", encoding="utf-8")
    (run_dir / "B2_OUTCOME_EVALUATION.json").write_text(json.dumps(evaluation, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": evaluation["run_id"], "success": success, "mandatory_compliance": success}, indent=2))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
