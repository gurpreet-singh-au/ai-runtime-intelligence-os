#!/usr/bin/env python3
"""Privacy-safe OTLP collector for B2-ATTR-001 Stage B2.

This receiver is diagnostic-only. It parses OTLP protobuf payloads in memory and
persists only allowlisted numeric/runtime fields plus structural summaries.
It never persists raw OTLP bodies, prompt/response text, tool content, repository
content, account identifiers, email addresses, or arbitrary attribute values.

`llm_request.context` is summarized structurally when possible. The raw value is
never written to disk.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from typing import Any, Iterable

from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import ExportLogsServiceRequest
from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import ExportMetricsServiceRequest
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceRequest

SAFE_ROLE_VALUES = {"system", "developer", "user", "assistant", "tool"}
SAFE_CONTENT_TYPES = {
    "text",
    "tool_use",
    "tool_result",
    "image",
    "document",
    "thinking",
    "redacted_thinking",
}
SAFE_MODELS_PREFIXES = ("claude-", "anthropic.")
NUMERIC_ATTRS = {
    "input_tokens",
    "output_tokens",
    "cache_read_tokens",
    "cache_creation_tokens",
    "duration_ms",
    "interaction.duration_ms",
    "ttft_ms",
    "cost_usd",
    "cost_usd_micros",
    "prompt_length",
    "response_length",
    "user_prompt_length",
    "attempt",
    "interaction.sequence",
    "event.sequence",
}
SAFE_STRING_ATTRS = {
    "model",
    "gen_ai.request.model",
    "gen_ai.system",
    "stop_reason",
    "speed",
    "status",
    "span.type",
    "transport_type",
    "query_source",
    "effort",
}


def h(value: bytes | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, bytes):
        raw = value
    else:
        raw = str(value).encode("utf-8", errors="replace")
    if not raw:
        return None
    return hashlib.sha256(raw).hexdigest()[:16]


def any_value_to_python(any_value) -> Any:
    """Convert OTLP AnyValue in memory only. Caller must persist only safe summaries."""
    kind = any_value.WhichOneof("value")
    if kind == "string_value":
        return str(any_value.string_value)
    if kind == "bool_value":
        return bool(any_value.bool_value)
    if kind == "int_value":
        return int(any_value.int_value)
    if kind == "double_value":
        return float(any_value.double_value)
    if kind == "bytes_value":
        return bytes(any_value.bytes_value)
    if kind == "array_value":
        return [any_value_to_python(v) for v in any_value.array_value.values]
    if kind == "kvlist_value":
        return {kv.key: any_value_to_python(kv.value) for kv in any_value.kvlist_value.values}
    return None


def attr_map(items: Iterable) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for item in items:
        if getattr(item, "key", None):
            out[str(item.key)] = any_value_to_python(item.value)
    return out


def safe_scalar(value: Any) -> int | float | bool | str | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value
    return None


def safe_string(attr: str, value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    if attr in {"model", "gen_ai.request.model"}:
        return value if value.startswith(SAFE_MODELS_PREFIXES) else "<redacted-model>"
    if attr in SAFE_STRING_ATTRS:
        return value[:160]
    return None


def summarize_json_structure(obj: Any) -> dict[str, Any]:
    """Return counts/allowlisted labels only; never arbitrary text or keys."""
    counts = Counter()
    role_counts = Counter()
    content_type_counts = Counter()
    list_lengths: list[int] = []
    max_depth = 0

    def walk(v: Any, depth: int = 0) -> None:
        nonlocal max_depth
        max_depth = max(max_depth, depth)
        if isinstance(v, dict):
            counts["dicts"] += 1
            role = v.get("role")
            if isinstance(role, str):
                role_counts[role if role in SAFE_ROLE_VALUES else "other"] += 1
            typ = v.get("type")
            if isinstance(typ, str):
                content_type_counts[typ if typ in SAFE_CONTENT_TYPES else "other"] += 1
            for child in v.values():
                walk(child, depth + 1)
        elif isinstance(v, list):
            counts["lists"] += 1
            list_lengths.append(len(v))
            for child in v:
                walk(child, depth + 1)
        elif isinstance(v, str):
            counts["strings"] += 1
            counts["string_chars"] += len(v)
        elif isinstance(v, bool):
            counts["bools"] += 1
        elif isinstance(v, (int, float)):
            counts["numbers"] += 1
        elif v is None:
            counts["nulls"] += 1
        else:
            counts["other"] += 1

    walk(obj)
    return {
        "root_type": type(obj).__name__,
        "max_depth": max_depth,
        "dict_count": counts["dicts"],
        "list_count": counts["lists"],
        "string_count": counts["strings"],
        "total_string_chars": counts["string_chars"],
        "number_count": counts["numbers"],
        "bool_count": counts["bools"],
        "null_count": counts["nulls"],
        "max_list_length": max(list_lengths) if list_lengths else 0,
        "role_counts": dict(sorted(role_counts.items())),
        "content_type_counts": dict(sorted(content_type_counts.items())),
    }


def summarize_context(value: Any) -> dict[str, Any]:
    if value is None:
        return {"present": False}

    out: dict[str, Any] = {"present": True, "otel_value_type": type(value).__name__}

    if isinstance(value, str):
        out["serialized_char_length"] = len(value)
        try:
            parsed = json.loads(value)
        except Exception:
            out["json_parseable"] = False
            return out
        out["json_parseable"] = True
        out["structure"] = summarize_json_structure(parsed)
        return out

    if isinstance(value, bytes):
        out["byte_length"] = len(value)
        return out

    if isinstance(value, (dict, list)):
        out["json_parseable"] = True
        out["structure"] = summarize_json_structure(value)
        try:
            out["serialized_char_length"] = len(json.dumps(value, ensure_ascii=False, separators=(",", ":")))
        except Exception:
            pass
        return out

    scalar = safe_scalar(value)
    if scalar is not None:
        out["scalar_type_only"] = type(value).__name__
    return out


class DiagnosticState:
    def __init__(self, output: Path):
        self.output = output
        self.lock = Lock()
        self.request_count = 0
        self.request_paths: Counter[str] = Counter()
        self.parse_errors: Counter[str] = Counter()
        self.metric_names: set[str] = set()
        self.llm_requests: list[dict[str, Any]] = []
        self.interactions: list[dict[str, Any]] = []
        self.log_events: list[dict[str, Any]] = []
        self.trace_parent_linkage_present = False
        self.log_trace_linkage_present = False

    def summary(self) -> dict[str, Any]:
        return {
            "experiment_id": "B2-ATTR-001",
            "stage": "B2-privacy-safe-otel-diagnostic",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "privacy": {
                "raw_otlp_bodies_persisted": False,
                "raw_prompt_response_context_persisted": False,
                "arbitrary_attribute_values_persisted": False,
                "account_or_email_values_persisted": False,
                "identifiers_hashed": True,
            },
            "transport": {
                "request_count": self.request_count,
                "request_paths": dict(self.request_paths),
                "parse_errors_by_path": dict(self.parse_errors),
            },
            "metric_names": sorted(self.metric_names),
            "trace_parent_linkage_present": self.trace_parent_linkage_present,
            "log_trace_linkage_present": self.log_trace_linkage_present,
            "llm_request_count": len(self.llm_requests),
            "interaction_count": len(self.interactions),
            "log_event_count": len(self.log_events),
            "llm_requests": self.llm_requests,
            "interactions": self.interactions,
            "log_events": self.log_events,
        }

    def persist(self) -> None:
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.output.write_text(json.dumps(self.summary(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def record_metrics(self, body: bytes) -> None:
        req = ExportMetricsServiceRequest()
        req.ParseFromString(body)
        for rm in req.resource_metrics:
            for sm in rm.scope_metrics:
                for metric in sm.metrics:
                    if metric.name:
                        self.metric_names.add(str(metric.name))

    def _safe_attrs(self, attrs: dict[str, Any]) -> dict[str, Any]:
        safe: dict[str, Any] = {}
        for key in sorted(NUMERIC_ATTRS):
            if key in attrs:
                value = safe_scalar(attrs[key])
                if value is not None:
                    safe[key] = value
        for key in sorted(SAFE_STRING_ATTRS):
            if key in attrs:
                value = safe_string(key, attrs[key])
                if value is not None:
                    safe[key] = value
        return safe

    def record_logs(self, body: bytes) -> None:
        req = ExportLogsServiceRequest()
        req.ParseFromString(body)
        for rl in req.resource_logs:
            for sl in rl.scope_logs:
                for rec in sl.log_records:
                    attrs = attr_map(rec.attributes)
                    if rec.trace_id or rec.span_id:
                        self.log_trace_linkage_present = True
                    event_name = attrs.get("event.name")
                    row: dict[str, Any] = {
                        "trace_id_hash": h(bytes(rec.trace_id)),
                        "span_id_hash": h(bytes(rec.span_id)),
                        "event_name_class": (
                            str(event_name) if isinstance(event_name, str) and str(event_name).startswith("claude_code.") else "<redacted-or-unknown>"
                        ),
                        "safe_attributes": self._safe_attrs(attrs),
                    }
                    # Record sensitive-field presence and lengths only.
                    for key in ("prompt", "response"):
                        if key in attrs and isinstance(attrs[key], str):
                            row[f"{key}_present"] = True
                            row[f"{key}_char_length"] = len(attrs[key])
                    if "request_id" in attrs:
                        row["request_id_hash"] = h(str(attrs["request_id"]))
                    if "client_request_id" in attrs:
                        row["client_request_id_hash"] = h(str(attrs["client_request_id"]))
                    self.log_events.append(row)

    def record_traces(self, body: bytes) -> None:
        req = ExportTraceServiceRequest()
        req.ParseFromString(body)
        for rs in req.resource_spans:
            for ss in rs.scope_spans:
                for span in ss.spans:
                    attrs = attr_map(span.attributes)
                    if span.parent_span_id:
                        self.trace_parent_linkage_present = True
                    row: dict[str, Any] = {
                        "trace_id_hash": h(bytes(span.trace_id)),
                        "span_id_hash": h(bytes(span.span_id)),
                        "parent_span_id_hash": h(bytes(span.parent_span_id)),
                        "safe_attributes": self._safe_attrs(attrs),
                    }
                    if "request_id" in attrs:
                        row["request_id_hash"] = h(str(attrs["request_id"]))
                    if "client_request_id" in attrs:
                        row["client_request_id_hash"] = h(str(attrs["client_request_id"]))
                    if "user_prompt" in attrs and isinstance(attrs["user_prompt"], str):
                        row["user_prompt_present"] = True
                        row["user_prompt_char_length"] = len(attrs["user_prompt"])
                    if "llm_request.context" in attrs:
                        row["context_summary"] = summarize_context(attrs["llm_request.context"])

                    if span.name == "claude_code.llm_request":
                        row["span_name"] = "claude_code.llm_request"
                        self.llm_requests.append(row)
                    elif span.name == "claude_code.interaction":
                        row["span_name"] = "claude_code.interaction"
                        self.interactions.append(row)

    def ingest(self, path: str, body: bytes) -> None:
        with self.lock:
            self.request_count += 1
            self.request_paths[path] += 1
            try:
                if path.endswith("/v1/metrics"):
                    self.record_metrics(body)
                elif path.endswith("/v1/logs"):
                    self.record_logs(body)
                elif path.endswith("/v1/traces"):
                    self.record_traces(body)
                else:
                    self.parse_errors[path] += 1
            except Exception:
                self.parse_errors[path] += 1
            self.persist()


class Handler(BaseHTTPRequestHandler):
    state: DiagnosticState

    def _handle(self) -> None:
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length else b""
        encoding = (self.headers.get("Content-Encoding") or "").lower()
        if encoding == "gzip":
            try:
                body = gzip.decompress(raw)
            except Exception:
                body = b""
        else:
            body = raw

        self.state.ingest(self.path, body)
        del raw
        del body

        self.send_response(200)
        self.send_header("Content-Type", "application/x-protobuf")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        self._handle()

    def do_PUT(self) -> None:  # noqa: N802
        self._handle()

    def log_message(self, format: str, *args) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4318)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    state = DiagnosticState(args.output)
    Handler.state = state
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Privacy-safe B2 OTel diagnostic receiver listening on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
