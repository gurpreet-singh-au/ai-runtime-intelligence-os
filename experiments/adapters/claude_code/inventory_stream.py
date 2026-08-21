#!/usr/bin/env python3
"""Inventory a Claude Code stream-json capture without assuming a fixed event schema.

This script intentionally does not normalise into RUN_SCHEMA.json yet. Its first job is
observability discovery: enumerate event types, keys, usage-like objects and parse failures
so the project can decide what is truly observable versus inferred or unknown.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def walk(obj: Any, prefix: str = ""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            yield path, value
            yield from walk(value, path)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            path = f"{prefix}[]"
            yield path, value
            yield from walk(value, path)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: inventory_stream.py <stream.jsonl> <inventory.json>", file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    target = Path(sys.argv[2])

    event_type_counts: Counter[str] = Counter()
    top_level_key_counts: Counter[str] = Counter()
    nested_key_counts: Counter[str] = Counter()
    usage_like_paths: Counter[str] = Counter()
    id_like_paths: Counter[str] = Counter()
    tool_like_paths: Counter[str] = Counter()
    agent_like_paths: Counter[str] = Counter()
    samples: dict[str, list[Any]] = defaultdict(list)
    parse_errors: list[dict[str, Any]] = []
    parsed_lines = 0

    if not source.exists():
        raise FileNotFoundError(source)

    with source.open("r", encoding="utf-8", errors="replace") as handle:
        for line_number, raw in enumerate(handle, start=1):
            text = raw.strip()
            if not text:
                continue
            try:
                record = json.loads(text)
            except json.JSONDecodeError as exc:
                parse_errors.append(
                    {
                        "line": line_number,
                        "error": str(exc),
                        "preview": text[:240],
                    }
                )
                continue

            parsed_lines += 1
            if isinstance(record, dict):
                for key in record:
                    top_level_key_counts[key] += 1

                event_type = None
                for candidate in ("type", "event", "event_type", "kind"):
                    value = record.get(candidate)
                    if isinstance(value, str):
                        event_type = f"{candidate}:{value}"
                        break
                event_type_counts[event_type or "<unclassified>"] += 1

            for path, value in walk(record):
                nested_key_counts[path] += 1
                low = path.lower()

                if any(token in low for token in ("usage", "token", "cost", "cache")):
                    usage_like_paths[path] += 1
                if any(token in low for token in ("session_id", "request_id", "message_id", "id")):
                    id_like_paths[path] += 1
                if any(token in low for token in ("tool", "command", "bash", "read", "write", "edit")):
                    tool_like_paths[path] += 1
                if any(token in low for token in ("agent", "subagent", "delegate")):
                    agent_like_paths[path] += 1

                if len(samples[path]) < 3 and isinstance(value, (str, int, float, bool, type(None))):
                    sample = value
                    if isinstance(sample, str) and len(sample) > 240:
                        sample = sample[:240] + "…"
                    samples[path].append(sample)

    def ranked(counter: Counter[str], limit: int = 200):
        return [{"path": key, "count": count, "samples": samples.get(key, [])} for key, count in counter.most_common(limit)]

    inventory = {
        "source": str(source),
        "parsed_json_lines": parsed_lines,
        "parse_error_count": len(parse_errors),
        "parse_errors": parse_errors[:50],
        "event_types": dict(event_type_counts.most_common()),
        "top_level_keys": dict(top_level_key_counts.most_common()),
        "usage_like_paths": ranked(usage_like_paths),
        "id_like_paths": ranked(id_like_paths),
        "tool_like_paths": ranked(tool_like_paths),
        "agent_like_paths": ranked(agent_like_paths),
        "all_nested_paths": ranked(nested_key_counts, 500),
        "interpretation_rule": "Presence is observed. Meaning is not assumed until mapped against runtime documentation/raw samples.",
    }

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote stream inventory: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
