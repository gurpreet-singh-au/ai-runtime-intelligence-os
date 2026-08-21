# Telemetry Gap Decision Protocol

Date: 2026-08-22
Status: Phase 0B — governs the decision after the first real baseline run

## Purpose

Prevent the project from collecting repeated low-quality baseline data or over-engineering instrumentation before seeing what the selected runtime actually exposes.

The first Claude Code run is both a benchmark run and an instrumentation-discovery experiment.

## Governing principle

Do not confuse unavailable telemetry with absence of resource usage.

Every material field is classified as:

- **OBSERVED** — directly present in raw runtime/provider/tool/test evidence;
- **DERIVED** — mechanically calculated from observed evidence;
- **INFERRED** — estimated/classified by a declared method;
- **UNKNOWN** — unavailable from the current evidence source.

`UNKNOWN != 0`.

## Critical telemetry groups

### G1 — Parent outcome

Minimum acceptable evidence:
- deterministic benchmark tests or frozen semantic evaluator;
- final success/failure;
- mandatory-rule compliance.

Required for every useful experiment.

### G2 — Runtime identity

Minimum acceptable evidence:
- runtime name/version;
- provider/model where exposed;
- benchmark snapshot/commit;
- task prompt/version;
- timestamps.

Required for reproducibility.

### G3 — Inference economics

Desired evidence:
- input tokens;
- cached input tokens or cache read/create metrics where exposed;
- output tokens;
- reasoning units where exposed;
- model/provider cost or enough usage data to derive cost with a versioned price table.

At least aggregate model usage/cost must be available before making efficiency claims.

### G4 — Tool execution

Desired evidence:
- tool name;
- invocation ordering;
- success/failure;
- repeated calls;
- file/search/test targets where safely observable;
- duration where available.

Strongly preferred for B2/B3/B5.

### G5 — Agent lineage

Desired evidence:
- parent agent;
- child/subagent creation;
- agent model where exposed;
- parent-child relationship;
- start/end;
- contribution/artifact references.

Required before testing Agent Spawn Economics or multi-agent efficiency claims.

### G6 — Context composition

Desired evidence:
- physical context/token load;
- retrieved files/chunks/results;
- cache effects;
- identifiable context additions/removals/compaction events.

Exact provider-hidden system context may remain unknown. The project must document the observability boundary rather than reconstruct private internals by guesswork.

### G7 — Instruction composition

Desired evidence:
- model-visible user/project/repository instructions where accessible;
- authority/scope/source of instructions;
- compiled/applicable set for future intervention experiments.

Provider-hidden system instructions are out of scope unless officially exposed.

### G8 — Progress / useful state change

Initially allowed as INFERRED only, using declared methods such as:
- successful code/test state transition;
- new relevant evidence captured;
- decision resolved;
- acceptance criterion newly satisfied;
- repeated operation without material state change.

No commercial claim should treat this as a precise observed metric until validated.

## Post-r01 decision tree

### Path A — Native CLI stream is sufficient

Use when:
- G1 and G2 are complete;
- aggregate G3 is present;
- G4 is sufficiently reconstructable for the benchmark;
- no immediate hypothesis requires missing G5-G7.

Action:
- run r02-r05;
- quantify variance;
- only then begin isolated interventions.

### Path B — Add native OpenTelemetry

Use when:
- CLI stream has task/tool evidence but usage/cost/session metrics are materially incomplete;
- official Claude Code OpenTelemetry can add the missing fields without changing execution policy materially.

Action:
- create a separately versioned `baseline+otel` observation configuration;
- validate that telemetry export overhead is negligible or measured;
- do not silently merge it with previous baseline configuration.

### Path C — Add gateway/proxy observation

Use when:
- request-level provider/model/usage/cost evidence is unavailable or inconsistent;
- a gateway can expose it without changing model selection/routing behaviour for the experiment.

Action:
- define an observation-only gateway policy;
- pin gateway/version/configuration;
- quantify any added latency/cost;
- treat it as a separate benchmark configuration.

### Path D — Use Agent SDK/runtime harness

Use when:
- agent lineage, tool lifecycle or orchestration events cannot be reconstructed from CLI evidence;
- those fields are essential to the next hypothesis.

Action:
- implement a thin adapter around the provider/runtime SDK;
- keep task/resource schema canonical and provider-neutral;
- compare the harness behaviour with native CLI to check for benchmark distortion.

### Path E — Switch first runtime

Use when:
- native + practical official telemetry still cannot expose enough evidence to test the intended hypothesis;
- instrumentation would dominate the experiment or fundamentally alter normal execution.

Action:
- select another runtime by evidence access/reproducibility, not preference;
- preserve Claude findings as an observability-gap result.

## Tranche continuation gate

Do not proceed from r01 to r02-r05 until all are true:

1. deterministic/semantic outcome can be evaluated;
2. runtime/model/snapshot identity is reproducible;
3. aggregate inference usage or cost is available or a clear approved collection method is selected;
4. the telemetry needed for the specific benchmark hypothesis is sufficiently observable;
5. parser/normalizer behaviour has been tested against the captured field shapes;
6. no unavailable field is being represented as zero;
7. raw artifacts are preserved independently from normalized data.

## Automation gate

No automated resource intervention is allowed merely because telemetry completeness is high.

After baseline evidence, the maturity path remains:

`Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise`

Each transition requires its own evidence and evaluation gate.
