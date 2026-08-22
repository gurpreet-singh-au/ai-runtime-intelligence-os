# B2-ATTR-001 Stage A Result

Date: 2026-08-22
Experiment: `B2-ATTR-001`
Stage: A — exhaust existing native Claude Code evidence
Baseline reference: frozen B2 Baseline v1 (`r02`–`r06`)
Decision: **INSUFFICIENT EVIDENCE FOR COMPOSITION ATTRIBUTION; PROCEED TO STAGE B**

## Purpose

Determine whether the existing Claude Code stream and benchmark artifacts can attribute the large provider-reported cached-input footprint to specific source classes without adding any new observation layer.

## Evidence audited

All five valid B2 baseline runs were audited from preserved local artifacts:

- `B2-001-baseline-r02`
- `B2-001-baseline-r03`
- `B2-001-baseline-r04`
- `B2-001-baseline-r05`
- `B2-001-baseline-r06`

The audit inspected:

- `claude-stream.jsonl`;
- `STREAM_INVENTORY.json`;
- `normalized-run.json`;
- `RUN_METADATA.json`;
- deterministic outcome evidence;
- tool-use and visible tool-result blocks;
- message-level usage objects;
- final `usage` and `modelUsage` objects;
- `usage.iterations`;
- `subagent_stats`;
- event order and tool trajectory.

Local analysis tools:

- `experiments/analyze_b2_attribution_stage_a.py`
- `experiments/analyze_b2_native_usage_detail.py`

## Stage A findings

### 1. Spawned subagents are OBSERVED absent

Every valid baseline run contains explicit final-result subagent telemetry with:

- `subagent_stats.spawned = 0`;
- all requested background/foreground/unset counts = 0;
- `completed = 0`;
- `failed = 0`;
- `max_depth = 0`;
- no refused or killed subagent activity.

Therefore **spawned subagents are not responsible for the B2 baseline footprint**.

The repeated presence of a secondary Haiku model in `modelUsage` must not be described as a spawned subagent. Its exact internal purpose remains UNKNOWN.

### 2. The secondary Haiku footprint is small and highly stable

Across all five runs, Haiku usage is approximately:

- 1,069 input tokens per run;
- 13–14 output tokens;
- zero reported cache-read tokens;
- zero reported cache-creation tokens;
- approximately USD 0.00113 per run.

Most observed cost and cache processing is therefore associated with Sonnet, not the secondary Haiku usage.

This does not establish why Haiku is invoked.

### 3. Message-level usage exposes context/cache growth across the execution trajectory

The native stream exposes repeated assistant-message usage snapshots. Across the runs, the first observed Sonnet cache-read footprint is about 22,115 tokens and later snapshots rise into roughly the 35k–36k range.

The accompanying cache-creation values are large early in the run and generally smaller later, consistent with a growing/reused prefix pattern.

This is useful trajectory evidence, but the snapshots must not be summed naively because duplicate assistant events and overlapping/cumulative accounting are present.

### 4. Final Sonnet cache-read totals remain much larger than any single snapshot

Final provider-reported Sonnet cache-read totals across the baseline are approximately 261k–336k tokens, while individual message-level snapshots are roughly 22k–36k.

This is consistent with repeated processing/reuse across multiple model turns. It is **not** evidence that a unique 261k–336k semantic context existed at one time.

### 5. `usage.iterations` is not sufficient for source attribution

Each audited run exposes one `usage.iterations` entry, but Stage A does not establish that this object provides a non-overlapping decomposition of the full run. It therefore remains evidence-only and is not added to other usage objects.

### 6. Tool trajectory is directly observable

The runs use 8–10 tool calls with variation in Bash/PowerShell/Glob operations around a stable core of Read, Edit and verification activity.

Visible tool input and result volumes can be measured, but native stream data does not reveal exactly how much of each tool result is retained in every subsequent model request or how provider compaction behaves.

## Attribution status by source class

| Source class | Stage A status | What is known | What remains unresolved |
|---|---|---|---|
| Provider/system instructions | PARTIAL/UNKNOWN | System-event presence is visible | Exact system prompt text/tokens and hidden provider contribution |
| Project/repository instructions | UNKNOWN | Reads/tool results may expose some repository content | Exact instruction/governance contribution per request |
| Task prompt | PARTIAL | Frozen prompt known externally | Exact provider-token/cache placement per request |
| Tool schemas | PARTIAL/UNKNOWN | Invoked tools known | Full available tool-schema payload/tokens per request |
| Repository/file content | PARTIAL | Reads/results visible | Per-file retained token contribution and compaction |
| Conversation/tool-result history | PARTIAL | Event order and visible content known | Exact history included in each model request |
| Spawned subagents | **OBSERVED: ZERO** | Explicit `subagent_stats.spawned = 0` across all five runs | None for spawned-agent count |
| Secondary/internal model activity | PARTIAL/UNKNOWN | Haiku aggregate usage is visible and small | Invocation purpose and lineage |
| Other provider/runtime overhead | UNKNOWN | Residual category exists | Magnitude and composition |

## Hypothesis impact

### H1 — controllable context/instruction mass exists

**Not yet resolved.** Native evidence shows repeated context/cache processing but cannot separate the major source classes.

### H2 — dominant controllable source can be isolated

**Not yet resolved.** The existing stream cannot identify a dominant controllable source with sufficient confidence.

### H3 — savings without outcome regression

**Not tested in Stage A.** No intervention has been run.

## Stage A decision

Stage A is now considered **exhausted for the primary composition question**.

It successfully resolved several secondary questions — especially subagent activity and trajectory-level cache growth — but it cannot attribute system instructions, project instructions, tool schemas, repository content and accumulated history with enough precision to justify selecting an optimisation intervention.

Proceed to Stage B under the telemetry-gap protocol.

## Stage B evidence boundary

Anthropic documentation confirms Claude Code can be monitored using OpenTelemetry. That establishes OpenTelemetry as a legitimate native observation candidate, but **does not by itself establish that the exposed telemetry contains full request composition or prompt/source-class token attribution**.

Therefore Stage B begins with a capability/overhead audit of native OpenTelemetry rather than assuming it can answer the attribution question. If native telemetry does not expose the required composition fields, escalate to the next-smallest observation mechanism under the project telemetry-gap protocol.

Do not add an SDK wrapper or gateway until the native telemetry capability has been tested and documented as insufficient.

## Guardrails

- Never sum overlapping message usage, final usage and iteration usage objects without proven semantics.
- Provider-reported cache-read totals are processed/cache usage, not unique semantic context size.
- A secondary model in `modelUsage` is not equivalent to a spawned subagent.
- Any diagnostic capture that could contain prompts, repository content or tool data must remain local and out of Git unless deliberately redacted.
- Do not add a gateway or SDK wrapper unless native Stage B telemetry proves insufficient.
- No optimisation intervention is selected yet.
