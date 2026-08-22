# Next Session — AI Runtime Intelligence OS

Last updated: 2026-08-22

## Read first

1. `PROJECT_STANDARD_ADOPTION.md`
2. `PROJECT_SPECIFIC_NON_NEGOTIABLES.md`
3. `PROJECT_STATE.md`
4. `DECISIONS.md`
5. `ROADMAP.md`
6. `architecture/AI_RUNTIME_RESOURCE_MODEL.md`
7. `architecture/TELEMETRY_MODEL.md`
8. `research/BENCHMARK_AND_BASELINE_SPEC.md`
9. `benchmarks/README.md`
10. `benchmarks/prompts/B2-001-baseline.md`
11. `experiments/B2_BASELINE_V1_RESULT.md`
12. `experiments/B2_CONTEXT_INSTRUCTION_ATTRIBUTION_SPEC.md`
13. `experiments/TELEMETRY_GAP_DECISION_PROTOCOL.md`
14. `experiments/RUN_SCHEMA.json`
15. `experiments/analyze_b2_baselines.py`
16. `experiments/adapters/claude_code/run_b2_baseline.ps1`
17. `experiments/adapters/claude_code/normalize_claude_run.py`
18. `experiments/adapters/claude_code/finalize_b2_outcome.py`
19. `research/MARKET_LANDSCAPE.md`
20. `research/COMPETITOR_MATRIX.md`
21. `research/SOURCE_REGISTER.md`

Also consult the pinned central framework `gurpreet-singh-au/ai-project-framework` v1.0.0 at commit `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2` when material governance questions arise.

## Current phase

Phase 0B — competitive boundary + experimental proof preparation. Do not start production implementation.

## Empirical status

B2 Baseline v1 is frozen at **five valid repetitions**:

- `B2-001-baseline-r02`
- `B2-001-baseline-r03`
- `B2-001-baseline-r04`
- `B2-001-baseline-r05`
- `B2-001-baseline-r06`

`B2-001-baseline-r01` remains an invalid harness/environment discovery run and is excluded from statistics.

All five included runs passed the deterministic B2 evaluator with 100% tested mandatory compliance.

Frozen distribution:

- mean cost: USD 0.19160122; CV 7.52%;
- mean Claude duration: 21,774.4 ms; CV 9.83%;
- mean fresh input: 1,087 tokens; CV 0.18%;
- mean cached input: 297,513.4 tokens; CV 11.84%;
- mean cache creation: 13,708.2 tokens; CV 2.97%;
- mean output: 1,273.8 tokens; CV 9.39%;
- mean tool calls: 9; CV 11.11%.

No r07 is required before the next phase unless later intervention variance shows n=5 was insufficient.

Formal baseline record: `experiments/B2_BASELINE_V1_RESULT.md`.

## Naturalistic observation

`NAT-001` used a fresh Claude Cowork session with a GitHub clone of this repository. It independently recommended context/instruction composition attribution as the highest-value experiment after the B2 baseline. Treat NAT-001 as naturalistic analytical evidence, not controlled proof.

## Next highest-value action

Execute **Stage A** of `experiments/B2_CONTEXT_INSTRUCTION_ATTRIBUTION_SPEC.md`.

The question is:

> What observable components are responsible for the approximately 298k mean provider-reported cached-input processing on B2, and which of those components are controllable without reducing task success or mandatory compliance?

Before adding any new telemetry layer, exhaust evidence already present in:

- `claude-stream.jsonl`;
- `STREAM_INVENTORY.json`;
- `normalized-run.json`;
- `RUN_METADATA.json`;
- assistant tool-use/tool-result events;
- model usage summaries;
- the frozen prompt, fixture and runner.

Produce an attribution-gap table for:

1. provider/system instructions;
2. project/repository instructions;
3. task prompt;
4. exposed tool schemas;
5. repository/file content;
6. conversation/tool-result history;
7. agent/subagent/internal utility activity;
8. residual provider/runtime overhead.

Classify each field as OBSERVED, DERIVED/ESTIMATED where justified, or UNKNOWN. Never turn missing evidence into zero.

## Instrumentation decision after Stage A

Only if existing evidence is insufficient, use the telemetry-gap protocol to choose the smallest additional observation layer. Consider richer native output first, then native telemetry such as OpenTelemetry, then a thin SDK/wrapper, gateway/proxy instrumentation, or an alternate measurement runtime if necessary.

For any added layer, measure and document its own overhead and whether it changes execution semantics.

## Intervention rule

After attribution, choose **one** isolated intervention according to the measured dominant controllable source. Possible mappings include context selection, instruction applicability compilation, tool-surface reduction, tool-result externalisation, or agent/model routing.

Do not combine interventions yet.

For a later B2 intervention comparison:

- retain the frozen fixture and task semantics;
- retain deterministic evaluator v1.1;
- target five valid intervention repetitions where practical;
- compare distributions, not one-off best runs;
- require non-inferior deterministic task quality and 100% tested mandatory compliance;
- do not claim savings if cost has merely moved into an unmeasured resource.

## First empirical gate

Do not claim the project thesis is validated until at least two representative workloads demonstrate material compute/cost or latency improvement with non-inferior parent-task quality and 100% tested mandatory-rule compliance.

## Do not do yet

- Do not run r07 by default.
- Do not choose a permanent model provider or agent framework.
- Do not make OpenRouter, Portkey, Langfuse, LangSmith or Braintrust foundational.
- Do not build another generic tracing dashboard or model gateway.
- Do not build an autonomous optimiser.
- Do not add OpenTelemetry merely to increase telemetry completeness.
- Do not optimise away mandatory safety/governance instructions.
- Do not infer causality from trace correlation alone.
- Do not interpret cached-input tokens as unique semantic context size.
