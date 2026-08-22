#!/usr/bin/env python3
"""Inventory Codex CLI --json/JSONL output without assuming a fixed event schema.

Discovery-only: records structural paths, event/type values where safely scalar,
and usage-like key paths. It does not sum potentially overlapping usage objects.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


USAGE_TERMS = ("token", "usage", "cost", "cache", "reasoning", "model", "duration", "latency", "turn", "tool", "command")


def read_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16"), "utf-16"
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig"), "utf-8-sig"
    if raw and raw.count(b"\x00") > len(raw) // 10:
        try:
            return raw.decode("utf-16-le"), "utf-16-le"
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", errors="replace"), "utf-8"


def walk(value: Any, path: str, paths: Counter[str], usage_paths: Counter[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            paths[child_path] += 1
            if any(term in str(key).lower() for term in USAGE_TERMS):
                usage_paths[child_path] += 1
            walk(child, child_path, paths, usage_paths)
    elif isinstance(value, list):
        for child in value:
            walk(child, f"{path}[]", paths, usage_paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stream", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    text, encoding = read_text(args.stream)
    event_types: Counter[str] = Counter()
    top_keys: Counter[str] = Counter()
    paths: Counter[str] = Counter()
    usage_paths: Counter[str] = Counter()
    parsed = 0
    failures = 0

    for raw_line in text.splitlines():
        line = raw_line.strip().lstrip("\ufeff")
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            failures += 1
            continue
        parsed += 1
        if isinstance(obj, dict):
            for key in obj:
                top_keys[str(key)] += 1
            for candidate in ("type", "event", "kind", "method"):
                val = obj.get(candidate)
                if isinstance(val, str) and len(val) <= 120:
                    event_types[f"{candidate}={val}"] += 1
                    break
        walk(obj, "", paths, usage_paths)

    report = {
        "schema_version": "0.1",
        "encoding": encoding,
        "line_count": len(text.splitlines()),
        "parsed_json_lines": parsed,
        "json_parse_failures": failures,
        "event_types": dict(event_types),
        "top_level_keys": dict(top_keys),
        "usage_like_paths": sorted(usage_paths),
        "all_structural_paths": sorted(paths),
        "guardrails": [
            "Path presence does not establish field semantics.",
            "Potentially overlapping usage objects are not summed.",
            "Missing fields remain UNKNOWN, not zero.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "parsed_json_lines": parsed,
        "json_parse_failures": failures,
        "event_types": dict(event_types),
        "usage_like_paths": sorted(usage_paths),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
