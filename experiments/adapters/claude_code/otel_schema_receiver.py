#!/usr/bin/env python3
"""Privacy-safe OTLP/HTTP schema receiver for B2-ATTR-001 Stage B1.

The receiver parses OTLP protobuf payloads in memory and persists only structural
metadata. Raw bodies, prompt/model/tool text, and arbitrary attribute values are
never written to disk or printed.

Persisted evidence includes:
- signal/request counts;
- metric names;
- conservative safe event/span names only when they are clearly namespaced runtime
  identifiers (otherwise a redacted placeholder is recorded);
- resource/scope/datapoint/log/span attribute KEYS;
- presence of structural fields such as trace/span linkage.

This is diagnostic-only and not a benchmark collector.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from typing import Iterable

from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import ExportLogsServiceRequest
from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import ExportMetricsServiceRequest
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceRequest


SAFE_NAME = re.compile(r"^(?:claude_code|gen_ai|anthropic|otel|opentelemetry)[A-Za-z0-9_.:/-]{0,160}$", re.I)


def safe_name(value: str) -> str:
    """Return only clearly runtime-namespaced identifiers; redact everything else."""
    if value and SAFE_NAME.fullmatch(value):
        return value
    return "<redacted-non-namespaced-name>"


def kv_keys(items: Iterable) -> list[str]:
    keys = sorted({str(item.key) for item in items if getattr(item, "key", None)})
    return keys


def any_value_string(any_value) -> str | None:
    # We inspect a value only for a small set of structural event-name keys and never
    # persist arbitrary values. String values that are not safely namespaced are redacted.
    try:
        kind = any_value.WhichOneof("value")
    except Exception:
        return None
    if kind == "string_value":
        return str(any_value.string_value)
    return None


class SchemaState:
    def __init__(self, output: Path):
        self.output = output
        self.lock = Lock()
        self.request_count = 0
        self.request_paths: Counter[str] = Counter()
        self.body_bytes: Counter[str] = Counter()
        self.parse_errors: Counter[str] = Counter()

        self.metric_names: set[str] = set()
        self.metric_resource_keys: set[str] = set()
        self.metric_scope_attribute_keys: set[str] = set()
        self.metric_datapoint_attribute_keys: set[str] = set()

        self.log_event_names: set[str] = set()
        self.log_resource_keys: set[str] = set()
        self.log_scope_attribute_keys: set[str] = set()
        self.log_attribute_keys: set[str] = set()
        self.log_trace_linkage_present = False

        self.span_names: set[str] = set()
        self.trace_resource_keys: set[str] = set()
        self.trace_scope_attribute_keys: set[str] = set()
        self.span_attribute_keys: set[str] = set()
        self.trace_parent_linkage_present = False
        self.trace_status_present = False

    def summary(self) -> dict:
        return {
            "experiment_id": "B2-ATTR-001",
            "stage": "B1-privacy-safe-otlp-schema-discovery",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "privacy": {
                "raw_bodies_persisted": False,
                "arbitrary_attribute_values_persisted": False,
                "prompt_or_tool_content_persisted": False,
                "non_namespaced_event_or_span_names_redacted": True,
            },
            "transport": {
                "request_count": self.request_count,
                "request_paths": dict(self.request_paths),
                "body_bytes_by_path": dict(self.body_bytes),
                "parse_errors_by_path": dict(self.parse_errors),
            },
            "metrics": {
                "metric_names": sorted(self.metric_names),
                "resource_attribute_keys": sorted(self.metric_resource_keys),
                "scope_attribute_keys": sorted(self.metric_scope_attribute_keys),
                "datapoint_attribute_keys": sorted(self.metric_datapoint_attribute_keys),
            },
            "logs": {
                "safe_event_names": sorted(self.log_event_names),
                "resource_attribute_keys": sorted(self.log_resource_keys),
                "scope_attribute_keys": sorted(self.log_scope_attribute_keys),
                "log_attribute_keys": sorted(self.log_attribute_keys),
                "trace_linkage_present": self.log_trace_linkage_present,
            },
            "traces": {
                "safe_span_names": sorted(self.span_names),
                "resource_attribute_keys": sorted(self.trace_resource_keys),
                "scope_attribute_keys": sorted(self.trace_scope_attribute_keys),
                "span_attribute_keys": sorted(self.span_attribute_keys),
                "parent_linkage_present": self.trace_parent_linkage_present,
                "status_present": self.trace_status_present,
            },
        }

    def persist(self) -> None:
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.output.write_text(json.dumps(self.summary(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def record_transport(self, path: str, body_len: int) -> None:
        self.request_count += 1
        self.request_paths[path] += 1
        self.body_bytes[path] += body_len

    def record_metrics(self, body: bytes) -> None:
        req = ExportMetricsServiceRequest()
        req.ParseFromString(body)
        for rm in req.resource_metrics:
            self.metric_resource_keys.update(kv_keys(rm.resource.attributes))
            for sm in rm.scope_metrics:
                self.metric_scope_attribute_keys.update(kv_keys(sm.scope.attributes))
                for metric in sm.metrics:
                    if metric.name:
                        self.metric_names.add(str(metric.name))
                    kind = metric.WhichOneof("data")
                    data = getattr(metric, kind) if kind else None
                    if data is None:
                        continue
                    points = []
                    if hasattr(data, "data_points"):
                        points = data.data_points
                    for point in points:
                        if hasattr(point, "attributes"):
                            self.metric_datapoint_attribute_keys.update(kv_keys(point.attributes))

    def record_logs(self, body: bytes) -> None:
        req = ExportLogsServiceRequest()
        req.ParseFromString(body)
        for rl in req.resource_logs:
            self.log_resource_keys.update(kv_keys(rl.resource.attributes))
            for sl in rl.scope_logs:
                self.log_scope_attribute_keys.update(kv_keys(sl.scope.attributes))
                for rec in sl.log_records:
                    self.log_attribute_keys.update(kv_keys(rec.attributes))
                    if rec.trace_id or rec.span_id:
                        self.log_trace_linkage_present = True
                    for attr in rec.attributes:
                        if attr.key in {"event.name", "event_name", "name"}:
                            value = any_value_string(attr.value)
                            if value is not None:
                                self.log_event_names.add(safe_name(value))

    def record_traces(self, body: bytes) -> None:
        req = ExportTraceServiceRequest()
        req.ParseFromString(body)
        for rs in req.resource_spans:
            self.trace_resource_keys.update(kv_keys(rs.resource.attributes))
            for ss in rs.scope_spans:
                self.trace_scope_attribute_keys.update(kv_keys(ss.scope.attributes))
                for span in ss.spans:
                    if span.name:
                        self.span_names.add(safe_name(str(span.name)))
                    self.span_attribute_keys.update(kv_keys(span.attributes))
                    if span.parent_span_id:
                        self.trace_parent_linkage_present = True
                    try:
                        if span.status.code or span.status.message:
                            self.trace_status_present = True
                    except Exception:
                        pass

    def ingest(self, path: str, body: bytes) -> None:
        with self.lock:
            self.record_transport(path, len(body))
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
                # Intentionally persist no exception text because protobuf/debug output
                # could accidentally contain content. Count only the failure.
                self.parse_errors[path] += 1
            self.persist()


class Handler(BaseHTTPRequestHandler):
    state: SchemaState

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

        # Body exists only in local memory during this call and is never persisted.
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

    state = SchemaState(args.output)
    Handler.state = state
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Privacy-safe OTLP schema receiver listening on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
