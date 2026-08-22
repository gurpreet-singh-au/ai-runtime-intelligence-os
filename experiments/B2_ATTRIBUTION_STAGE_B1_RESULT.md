# B2-ATTR-001 Stage B1 Result

Date: 2026-08-22
Experiment: `B2-ATTR-001`
Stage: B1 — native OpenTelemetry capability discovery
Runtime: Claude Code 2.1.238 on Windows
Decision: **USEFUL ATTRIBUTION-RELEVANT NATIVE OTEL FIELDS OBSERVED; PROCEED TO ONE STAGE B2 B2-DIAGNOSTIC CAPTURE**

## What was tested

Stage B1 used three increasingly specific native-telemetry probes.

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

This resolved the transport question: Claude Code 2.1.238 can initialize and export native OTLP telemetry in this environment.

### Probe 3 — privacy-safe OTLP schema discovery

`B2-ATTR-001-otel-schema-r01`

The receiver parsed OTLP protobuf payloads in memory and persisted only structural names/keys. Raw bodies and arbitrary attribute values were discarded.

Observed transport:

- Claude exit code: `0`;
- total OTLP requests: **8**;
- `/v1/metrics`: **3**;
- `/v1/logs`: **3**;
- `/v1/traces`: **2**;
- parse errors: **0**.

Observed metric names:

- `claude_code.active_time.total`;
- `claude_code.cost.usage`;
- `claude_code.session.count`;
- `claude_code.token.usage`.

Observed metric datapoint attribute keys include:

- `model`;
- `session.id`;
- `type`;
- `effort`;
- `query_source`;
- runtime/account dimensions.

Observed log attribute keys include:

- `input_tokens`;
- `output_tokens`;
- `cache_read_tokens`;
- `cache_creation_tokens`;
- `cost_usd` / `cost_usd_micros`;
- `duration_ms`;
- `model`;
- `request_id` / `client_request_id`;
- `message.uuid`;
- `event.name` / `event.sequence` / `event.timestamp`;
- `prompt` / `prompt.id` / `prompt_length`;
- `response` / `response_length`;
- `session.id`;
- `status` / `speed` / `transport_type`.

Observed trace span names:

- `claude_code.interaction`;
- `claude_code.llm_request`.

Observed span attribute keys include:

- `input_tokens`;
- `output_tokens`;
- `cache_read_tokens`;
- `cache_creation_tokens`;
- `duration_ms`;
- `ttft_ms`;
- `model` / `gen_ai.request.model`;
- `request_id` / `client_request_id`;
- `interaction.sequence`;
- `interaction.duration_ms`;
- `llm_request.context`;
- `user_prompt` / `user_prompt_length`;
- `success` / `stop_reason`;
- `gen_ai.response.id` / `gen_ai.response.finish_reasons`;
- `session.id`.

The log records had trace linkage and the trace data had parent linkage.

## Interpretation

Stage B1 now establishes more than generic observability.

Native Claude Code OTel exposes a request/interaction evidence surface with:

1. model-request spans;
2. trace/parent linkage;
3. per-request token/cache usage fields;
4. request/session identifiers;
5. duration and TTFT fields;
6. prompt/user-prompt length fields;
7. an `llm_request.context` field whose schema/type/content semantics remain uninspected;
8. log-side prompt/response fields whose raw values are intentionally not persisted.

This is enough to justify **one tightly controlled B2 telemetry-enabled diagnostic capture** before escalating to an SDK wrapper or proxy.

The strongest unresolved opportunity is `llm_request.context`. If that field carries a structured or serialized request-context representation, a privacy-safe in-memory summarizer may be able to report only composition structure and lengths — for example message counts, roles, system/tool section presence and serialized character sizes — without retaining content.

## What is not yet established

Stage B1 does **not** establish:

- exact system-instruction token contribution;
- exact project-governance instruction contribution;
- tool-schema token contribution;
- per-file retained context contribution;
- exact conversation-history token contribution;
- the semantics of `llm_request.context`;
- whether telemetry changes B2 execution cost/latency materially.

Presence of `prompt`, `response`, `user_prompt` and `llm_request.context` keys is not permission to persist their raw values.

## Stage B2 decision

Proceed with exactly one diagnostic run:

`B2-ATTR-001-otel-diagnostic-r01`

Use the frozen B2-001 fixture and task semantics, deterministic evaluator v1.1 and the same controlled Python/pytest environment as Baseline v1.

The diagnostic collector may persist only:

- known numeric telemetry fields;
- safe structural identifiers;
- trace/request/session linkage identifiers where needed for joins;
- value types;
- content lengths;
- privacy-safe structural summaries of `llm_request.context` if parseable in memory.

It must not persist prompt text, response text, repository/file content, tool argument/result content or raw OTLP payloads.

The first diagnostic is not eligible for a savings claim against Baseline v1. Its purpose is attribution and instrumentation-overhead assessment.

## Decision rule after Stage B2 diagnostic

- **B-PROCEED** — context/request structure becomes sufficiently attributable to identify one plausible dominant controllable source; design exactly one isolated intervention.
- **B-ESCALATE** — OTel improves lineage/usage visibility but still cannot separate the dominant composition classes; evaluate the next-smallest observation mechanism under the telemetry-gap protocol.
- **B-REDIRECT** — the suspected context/instruction source is not practically observable/controllable in Claude Code; test another runtime resource class or another runtime surface.

## Privacy guardrails

- Raw OTLP payloads remain memory-only.
- Raw prompt/response/context/tool/repository text is never persisted.
- Structural summaries must contain counts, lengths, types and allowlisted schema labels only.
- Keep diagnostic output under `experiments/local-runs/` unless explicitly redacted and promoted into a repository result document.
- No benchmark savings claim is allowed from Stage B1 or the first Stage B2 diagnostic.
