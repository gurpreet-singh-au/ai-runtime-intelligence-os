# B2-ATTR-001 Stage B1 Result

Date: 2026-08-22
Experiment: `B2-ATTR-001`
Stage: B1 — native OpenTelemetry capability discovery
Runtime: Claude Code 2.1.238 on Windows
Decision: **NATIVE OTLP TRANSPORT OBSERVED; CONTINUE WITH PRIVACY-SAFE SIGNAL-SCHEMA DISCOVERY**

## What was tested

Stage B1 used two increasingly specific probes.

### Probe 1 — console exporters

`B2-ATTR-001-otel-capability-probe-r01`

Claude Code user-managed telemetry was enabled with console exporters for metrics, logs and traces while deliberately keeping raw API bodies, user prompt text, tool details and tool content disabled.

The Claude process completed successfully with exit code 0, but split-channel analysis found no separately observable OpenTelemetry stream:

- stdout contained only ordinary Claude `stream-json` events;
- stderr was empty;
- analyzer decision: `NO_OTEL_EMISSION_OBSERVED`.

That result was intentionally treated as inconclusive for OTLP transport because console-exporter behavior can differ from OTLP export behavior.

### Probe 2 — local loopback OTLP transport

`B2-ATTR-001-otel-loopback-r01`

A minimal receiver listened only on `127.0.0.1:4318`. Claude Code was configured for OTLP/HTTP export. The receiver persisted no telemetry bodies and recorded only transport metadata.

Observed result:

- Claude exit code: `0`;
- total OTLP requests: **7**;
- `/v1/metrics`: **3** requests;
- `/v1/logs`: **2** requests;
- `/v1/traces`: **2** requests;
- `otlp_transport_observed`: **true**;
- raw bodies persisted: **false**;
- decision: `OTLP_REQUESTS_OBSERVED`.

## Interpretation

This resolves the transport question.

**Claude Code 2.1.238 is capable of initializing and exporting native OTLP telemetry in this environment.**

The earlier console-exporter silence must therefore not be interpreted as absence of native telemetry support.

The loopback result also confirms that all three signal classes were attempted in this diagnostic configuration:

1. metrics;
2. logs;
3. traces.

This is stronger than the earlier console probe and is sufficient to justify one further native-telemetry discovery step before considering a custom SDK wrapper, proxy or gateway.

## What remains unresolved

Transport success does **not** yet establish that the emitted payload exposes the attribution fields required by `B2-ATTR-001`.

We still need to know, without retaining sensitive values, which schema elements are actually present, including where available:

- metric names;
- event/log names;
- span names;
- resource attribute keys;
- log attribute keys;
- span attribute keys;
- model/request/tool/session/parent-child identifiers;
- token/cache/cost fields;
- context/compaction fields;
- any prompt/system/tool-schema composition metadata.

## Next smallest diagnostic

Run a **privacy-safe OTLP schema discovery probe**.

The receiver should parse OTLP protobuf bodies in memory, extract only structural names/keys, immediately discard values and raw bodies, and persist only a schema summary.

It must not persist:

- prompt text;
- repository/file content;
- tool arguments/results;
- model response text;
- raw telemetry bodies;
- attribute values that could contain user/repository content.

The purpose is to answer:

> Which native Claude Code OTel fields are actually observable in this installed runtime, and do they materially improve B2 context/instruction attribution?

## Decision rule after schema discovery

- **Useful attribution fields observed** -> design one B2 telemetry-enabled diagnostic capture under Stage B2.
- **Only generic usage/operations fields observed** -> native OTel is useful for runtime tracing but insufficient for composition attribution; escalate to the next-smallest observation mechanism under the telemetry-gap protocol.
- **Sensitive values required to answer composition** -> do not enable broad persistent logging; evaluate a tightly controlled local-only diagnostic or a thin wrapper instead.

## Privacy guardrails

- All raw OTLP payloads remain memory-only.
- Persist structural names and attribute keys only.
- Keep all diagnostic summaries under `experiments/local-runs/` unless explicitly redacted and promoted into a repository result document.
- No benchmark savings claim is allowed from these diagnostic probes.
