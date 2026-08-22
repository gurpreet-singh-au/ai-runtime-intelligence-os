#!/usr/bin/env python3
"""Analyze the privacy-safe Stage B2 OTLP diagnostic summary.

Produces deterministic trajectory mechanics without reading or reconstructing raw
prompt/context/tool content. It checks the cache recurrence relation between
successive Sonnet requests and quantifies how much of final per-request context was
already present before the tool trajectory began.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("diagnostic", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    data = load_json(args.diagnostic)
    reqs = data.get("llm_requests", [])

    haiku = []
    sonnet = []
    for req in reqs:
        attrs = req.get("safe_attributes", {})
        model = attrs.get("model", "")
        if "haiku" in model:
            haiku.append(req)
        if "sonnet" in model:
            sonnet.append(req)

    sequence = []
    for idx, req in enumerate(sonnet, start=1):
        a = req.get("safe_attributes", {})
        sequence.append({
            "request_index": idx,
            "cache_read_tokens": a.get("cache_read_tokens"),
            "cache_creation_tokens": a.get("cache_creation_tokens"),
            "fresh_input_tokens": a.get("input_tokens"),
            "output_tokens": a.get("output_tokens"),
            "duration_ms": a.get("duration_ms"),
            "ttft_ms": a.get("ttft_ms"),
            "cost_usd": next((e.get("safe_attributes", {}).get("cost_usd") for e in data.get("log_events", []) if e.get("request_id_hash") == req.get("request_id_hash") and "cost_usd" in e.get("safe_attributes", {})), None),
            "stop_reason": a.get("stop_reason"),
            "context_summary": req.get("context_summary"),
        })

    recurrence = []
    all_exact = True
    for prev, curr in zip(sequence, sequence[1:]):
        pr = prev.get("cache_read_tokens")
        pc = prev.get("cache_creation_tokens")
        cr = curr.get("cache_read_tokens")
        expected = pr + pc if all(isinstance(x, (int, float)) for x in (pr, pc)) else None
        exact = expected == cr if expected is not None else False
        all_exact = all_exact and exact
        recurrence.append({
            "from_request": prev["request_index"],
            "to_request": curr["request_index"],
            "prior_cache_read_plus_creation": expected,
            "next_cache_read": cr,
            "exact_match": exact,
        })

    first = sequence[0] if sequence else {}
    last = sequence[-1] if sequence else {}
    first_processed = sum(x for x in [first.get("cache_read_tokens"), first.get("cache_creation_tokens"), first.get("fresh_input_tokens")] if isinstance(x, (int, float)))
    final_processed = sum(x for x in [last.get("cache_read_tokens"), last.get("cache_creation_tokens"), last.get("fresh_input_tokens")] if isinstance(x, (int, float)))
    post_first_growth = final_processed - first_processed if sequence else None

    sonnet_totals = {}
    for key in ("cache_read_tokens", "cache_creation_tokens", "fresh_input_tokens", "output_tokens", "duration_ms", "cost_usd"):
        vals = [row.get(key) for row in sequence if isinstance(row.get(key), (int, float))]
        sonnet_totals[key] = sum(vals) if vals else None

    haiku_query_sources = sorted({
        e.get("safe_attributes", {}).get("query_source")
        for e in data.get("log_events", [])
        if "haiku" in str(e.get("safe_attributes", {}).get("model", "")) and e.get("safe_attributes", {}).get("query_source")
    })

    report = {
        "experiment_id": data.get("experiment_id"),
        "stage": "B2-otel-diagnostic-trajectory-analysis",
        "sonnet_request_count": len(sequence),
        "haiku_request_count": len(haiku),
        "haiku_query_sources_observed": haiku_query_sources,
        "sonnet_request_sequence": sequence,
        "cache_recurrence": {
            "comparisons": recurrence,
            "exact_for_all_successive_sonnet_requests": all_exact if len(sequence) > 1 else None,
            "interpretation": "If exact, each next request's cache-read prefix equals the previous request's cache-read plus cache-creation tokens. This demonstrates stepwise prefix carry-forward, not source composition.",
        },
        "context_growth": {
            "first_sonnet_processed_input_tokens": first_processed,
            "final_sonnet_processed_input_tokens": final_processed,
            "post_first_request_growth_tokens": post_first_growth,
            "first_request_share_of_final_processed_input": (first_processed / final_processed) if final_processed else None,
            "post_first_growth_share_of_final_processed_input": (post_first_growth / final_processed) if final_processed else None,
            "guardrail": "Processed input is provider token accounting for that request. It is not a claim about unique semantic context or source composition.",
        },
        "sonnet_run_totals": sonnet_totals,
        "context_field": {
            "serialized_lengths": [row.get("context_summary", {}).get("serialized_char_length") for row in sequence],
            "json_parseable_values": [row.get("context_summary", {}).get("json_parseable") for row in sequence],
            "interpretation": "The observed llm_request.context field is a short non-JSON string in this run and does not expose request composition under the privacy-safe collector.",
        },
        "decision_support": {
            "native_otel_resolves_request_boundaries_and_cache_growth": True,
            "native_otel_resolves_initial_prefix_source_composition": False,
            "native_otel_resolves_tool_schema_vs_instruction_share": False,
            "native_otel_resolves_secondary_haiku_purpose": bool(haiku_query_sources),
        },
    }

    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote B2 OTel trajectory analysis: {args.output}")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
