# B2-ATTR-001 Stage B1 Result

Date: 2026-08-22
Experiment: `B2-ATTR-001`
Stage: B1 — native OpenTelemetry capability discovery
Probe: `B2-ATTR-001-otel-capability-probe-r01`
Runtime: Claude Code 2.1.238 on Windows
Decision: **NO OTEL EMISSION OBSERVED VIA CONSOLE EXPORTERS; RUN ONE LOCAL OTLP TRANSPORT PROBE BEFORE ESCALATING**

## What was tested

The probe enabled Claude Code user-managed telemetry with console exporters for metrics, logs and traces while deliberately keeping raw API bodies, user prompt text, tool details and tool content disabled.

The Claude process completed successfully with exit code 0.

A split-channel analysis was then performed because the initial probe summary had combined normal Claude `stream-json` stdout with potential OpenTelemetry output.

## Split-channel result

### stdout

- four JSON objects were emitted;
- all four were ordinary Claude stream-json events:
  - `rate_limit_event`;
  - `system`;
  - `assistant`;
  - `result`;
- model/token/cache/cost/request keywords were present, but those fields are already part of ordinary Claude stream-json;
- no unambiguous OpenTelemetry structural payload was detected.

### stderr

- file existed;
- byte length: 0;
- no telemetry records or OpenTelemetry structural fields were observed.

Formal analyzer decision:

`NO_OTEL_EMISSION_OBSERVED`

## Interpretation

This result proves only that **the configured console-exporter probe did not produce a separately observable OpenTelemetry stream** in this environment.

It does not yet prove that Claude Code 2.1.238 cannot export user-managed OpenTelemetry through OTLP transport.

Relevant upstream evidence makes this distinction important:

- Anthropic's Claude Code repository has an open Windows issue describing cases where third-party OpenTelemetry never initializes and even console exporters emit nothing on managed/enterprise accounts (`anthropics/claude-code#46204`).
- A separate Windows regression report documented log/events exporters emitting nothing while metrics worked; that issue was later closed as completed (`anthropics/claude-code#64396`).

Therefore console-exporter silence should not be interpreted as definitive absence of all OTLP capability.

## Next smallest diagnostic

Before introducing an external collector, SDK wrapper or proxy, run one **local loopback OTLP transport probe**:

1. start a minimal local HTTP receiver on `127.0.0.1:4318`;
2. configure Claude Code to export OTLP over HTTP/protobuf to that receiver;
3. run a minimal no-tool prompt;
4. record only request path, content type and payload byte count — not request bodies;
5. determine whether Claude attempts `/v1/metrics`, `/v1/logs` or `/v1/traces` requests.

This directly answers whether the current runtime initializes and attempts OTLP export without requiring Docker, a cloud backend or raw-content inspection.

## Decision rule after loopback probe

- **OTLP requests observed** -> native telemetry transport works; inspect which signal classes are actually emitted and whether they improve attribution.
- **No OTLP requests observed** -> treat native OTel as unavailable/unreliable in this environment for the present experiment and move to the next-smallest observation mechanism under the telemetry-gap protocol.

## Privacy guardrails

The loopback receiver must not persist request bodies. It may record only:

- timestamp;
- HTTP method;
- request path;
- content type;
- content encoding;
- body byte length;
- response status.

No raw telemetry payload, prompt text, repository content or tool content should be committed to GitHub.
