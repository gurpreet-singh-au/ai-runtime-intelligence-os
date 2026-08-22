#!/usr/bin/env python3
"""Minimal privacy-safe OTLP HTTP loopback receiver for Stage B1.

Records only transport metadata and discards request bodies immediately.
No telemetry payload content is persisted or printed.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock


class Recorder:
    def __init__(self, output: Path):
        self.output = output
        self.lock = Lock()
        self.records: list[dict] = []

    def add(self, record: dict) -> None:
        with self.lock:
            self.records.append(record)
            self.output.parent.mkdir(parents=True, exist_ok=True)
            self.output.write_text(json.dumps(self.records, indent=2) + "\n", encoding="utf-8")


class Handler(BaseHTTPRequestHandler):
    recorder: Recorder

    def _handle(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0") or 0)
        if content_length:
            _ = self.rfile.read(content_length)  # discard without persisting

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": self.command,
            "path": self.path,
            "content_type": self.headers.get("Content-Type"),
            "content_encoding": self.headers.get("Content-Encoding"),
            "body_bytes": content_length,
            "response_status": 200,
        }
        self.recorder.add(record)

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

    recorder = Recorder(args.output)
    Handler.recorder = recorder
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"OTLP loopback receiver listening on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
