#!/usr/bin/env python3
"""Analyze a Codex B2 discovery run for execution-vs-harness failure.

This is intentionally narrow and benchmark-specific. The B2 fixture contains only
synthetic code, so the report may include the completed Codex agent message to
explain why a discovery run performed no tool/file actions. It never prints auth
material or arbitrary environment variables.
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
        value = json.loads(read_text(path).lstrip("\ufeff"))
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("artifacts", type=Path)
    args = p.parse_args()
    root = args.artifacts.resolve()

    metadata = load_json(root / "RUN_METADATA.json")
    outcome = load_json(root / "B2_OUTCOME_EVALUATION.json")
    stream_text = read_text(root / "codex-stream.jsonl")
    stderr = read_text(root / "codex-stderr.log")
    git_after = read_text(root / "git-after.txt")
    diff = read_text(root / "git-diff.patch")

    event_types: list[str] = []
    item_types: list[str] = []
    messages: list[str] = []
    usage: dict[str, Any] | None = None
    parse_failures = 0

    for raw in stream_text.splitlines():
        line = raw.strip().lstrip("\ufeff")
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            parse_failures += 1
            continue
        if not isinstance(obj, dict):
            continue
        typ = obj.get("type")
        if isinstance(typ, str):
            event_types.append(typ)
        item = obj.get("item")
        if isinstance(item, dict):
            item_type = item.get("type")
            if isinstance(item_type, str):
                item_types.append(item_type)
            if item_type == "agent_message" and isinstance(item.get("text"), str):
                messages.append(item["text"][:4000])
            elif item_type == "error" and isinstance(item.get("message"), str):
                messages.append("ITEM_ERROR: " + item["message"][:4000])
        if typ == "turn.completed" and isinstance(obj.get("usage"), dict):
            usage = obj["usage"]

    tracked_diff_present = bool(diff.strip())
    status_lines = [line for line in git_after.splitlines() if line.strip()]
    only_untracked_status = bool(status_lines) and all(line.lstrip().startswith("??") for line in status_lines)

    report = {
        "run_id": metadata.get("run_id"),
        "codex_exit_code": metadata.get("codex_exit_code"),
        "tests_before_exit_code": metadata.get("tests_before_exit_code"),
        "tests_after_exit_code": metadata.get("tests_after_exit_code"),
        "event_types": event_types,
        "item_types": item_types,
        "turn_usage": usage,
        "agent_or_error_messages": messages,
        "json_parse_failures": parse_failures,
        "tracked_git_diff_present": tracked_diff_present,
        "git_status_lines": status_lines,
        "git_status_only_untracked": only_untracked_status,
        "models_cache_compatibility_warning_observed": (
            "failed to load models cache" in stderr and "base_instructions" in stderr
        ),
        "deterministic_outcome_success": outcome.get("success"),
        "interpretation": {
            "codex_reached_model_turn": "turn.completed" in event_types,
            "command_execution_observed": "command_execution" in item_types,
            "file_change_event_observed": "file_change" in item_types,
            "tracked_code_change_observed": tracked_diff_present,
            "workspace_modified_flag_may_be_test_artifact": bool(metadata.get("workspace_modified")) and not tracked_diff_present,
        },
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
