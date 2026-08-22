#!/usr/bin/env python3
"""Analyze Claude Code Stage B1 OTel probe artifacts without exposing raw content.

The initial probe summary intentionally merged stdout and stderr for keyword presence.
That is insufficient to prove OpenTelemetry emission because Claude stream-json output
itself contains model/token/cache/cost fields. This analyzer separates the two channels
and reports only structural/keyword evidence.

It does not print prompt text, tool content, raw API bodies, or full telemetry records.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


KEYWORDS = [
    "api_request",
    "api_error",
    "tool_result",
    "user_prompt",
    "session.id",
    "model",
    "input_token",
    "output_token",
    "cache",
    "cost",
    "duration",
    "latency",
    "trace",
    "span",
    "compaction",
    "context",
    "parent",
    "request",
    "otel",
    "opentelemetry",
]

OTEL_STRUCTURAL_KEYS = {
    "resourceMetrics",
    "scopeMetrics",
    "metrics",
    "resourceLogs",
    "scopeLogs",
    "logRecords",
    "resourceSpans",
    "scopeSpans",
    "spans",
    "traceId",
    "spanId",
    "parentSpanId",
    "instrumentationScope",
    "resource",
    "attributes",
    "body",
    "name",
}


def read_text_portable(path: Path) -> tuple[str, str]:
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
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace"), "utf-8-replace"


def walk_keys(value: Any, out: Counter[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            out[str(key)] += 1
            walk_keys(child, out)
    elif isinstance(value, list):
        for child in value:
            walk_keys(child, out)


def analyze_channel(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False}

    text, encoding = read_text_portable(path)
    keyword_counts = {
        k: text.lower().count(k.lower())
        for k in KEYWORDS
    }

    json_line_count = 0
    parsed_json_objects = 0
    parse_failures = 0
    event_types: Counter[str] = Counter()
    all_keys: Counter[str] = Counter()
    otel_key_hits: Counter[str] = Counter()

    for raw in text.splitlines():
        line = raw.strip().lstrip("\ufeff")
        if not line:
            continue
        if not (line.startswith("{") or line.startswith("[")):
            continue
        json_line_count += 1
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            parse_failures += 1
            continue
        parsed_json_objects += 1
        if isinstance(obj, dict):
            typ = obj.get("type") or obj.get("event") or obj.get("kind")
            if isinstance(typ, str):
                event_types[typ] += 1
        walk_keys(obj, all_keys)

    for key in OTEL_STRUCTURAL_KEYS:
        if all_keys[key]:
            otel_key_hits[key] = all_keys[key]

    likely_otel = any(
        key in otel_key_hits
        for key in (
            "resourceMetrics",
            "scopeMetrics",
            "resourceLogs",
            "scopeLogs",
            "resourceSpans",
            "scopeSpans",
            "traceId",
            "spanId",
            "parentSpanId",
        )
    )

    return {
        "exists": True,
        "encoding": encoding,
        "bytes": path.stat().st_size,
        "line_count": len(text.splitlines()),
        "keyword_counts": keyword_counts,
        "json_candidate_lines": json_line_count,
        "parsed_json_objects": parsed_json_objects,
        "json_parse_failures": parse_failures,
        "event_types": dict(event_types),
        "otel_structural_key_hits": dict(otel_key_hits),
        "likely_otel_structured_payload_present": likely_otel,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_dir", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    artifact_dir = args.artifact_dir.resolve()
    stdout = analyze_channel(artifact_dir / "probe-stdout.log")
    stderr = analyze_channel(artifact_dir / "probe-stderr.log")

    decision = "INCONCLUSIVE"
    rationale: list[str] = []

    if stderr.get("likely_otel_structured_payload_present"):
        decision = "OTEL_EMISSION_OBSERVED"
        rationale.append("Structured OpenTelemetry-like keys were observed on stderr, separate from Claude stream-json stdout.")
    elif stderr.get("exists") and stderr.get("bytes", 0) > 0:
        decision = "STDERR_PRESENT_BUT_OTEL_NOT_CONFIRMED"
        rationale.append("stderr contains data, but no unambiguous OTel structural keys were detected by the conservative analyzer.")
    elif stderr.get("exists"):
        decision = "NO_OTEL_EMISSION_OBSERVED"
        rationale.append("stderr exists but is empty; stdout keyword counts alone cannot prove OTel because Claude stream-json carries overlapping model/token/cache fields.")
    else:
        rationale.append("probe-stderr.log is missing, so OTel console emission cannot be assessed separately from stream-json stdout.")

    report = {
        "experiment_id": "B2-ATTR-001",
        "stage": "B1-split-channel-analysis",
        "artifact_dir": str(artifact_dir),
        "stdout": stdout,
        "stderr": stderr,
        "decision": decision,
        "rationale": rationale,
        "interpretation_guardrails": [
            "Claude stream-json stdout contains model/token/cache/cost terms and therefore cannot by itself establish OTel emission.",
            "Keyword presence is not schema meaning.",
            "This analyzer reports structure only and does not print raw prompts, tool content, or telemetry bodies.",
            "If OTel emission is observed, field usefulness for composition attribution must still be evaluated separately.",
        ],
    }

    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote split-channel OTel analysis: {args.output}")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
