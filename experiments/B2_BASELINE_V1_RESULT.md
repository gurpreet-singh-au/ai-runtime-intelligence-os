# B2-001 Baseline v1 Result

Date frozen: 2026-08-22
Benchmark: `B2-001` — small bug fix: order discount
Baseline series: `B2-001-baseline-r02` through `B2-001-baseline-r06`
Excluded discovery run: `B2-001-baseline-r01`

## Decision

Freeze the first B2 baseline series at **n=5 valid repetitions** for exploratory intervention comparison.

This is sufficient for the current Phase 0B purpose: establish a descriptive baseline distribution before one isolated runtime intervention. It is **not** sufficient for publication-grade statistical claims or broad thesis validation.

## Validity

All five included runs satisfied the deterministic B2 evaluator:

- Claude process exited successfully;
- the fixture failed before execution as expected;
- all tests passed after execution;
- a non-empty implementation diff was produced;
- only `runtime_fixture/pricing.py` changed;
- tests were not modified;
- the intended shipping-after-discount implementation was present;
- `success: true`;
- `mandatory_compliance: true`.

Success rate across included runs: **5/5 = 100%**.

`r01` remains preserved as harness/environment discovery evidence and is excluded from all baseline performance statistics.

## Descriptive distribution

| Metric | Mean | Median | Min | Max | Std dev | CV |
|---|---:|---:|---:|---:|---:|---:|
| Total cost USD | 0.19160122 | 0.19402950 | 0.17634690 | 0.20899400 | 0.01440126 | 7.52% |
| Duration ms | 21,774.4 | 21,977 | 19,175 | 24,032 | 2,139.66 | 9.83% |
| Fresh input tokens | 1,087.0 | 1,087 | 1,085 | 1,089 | 2.00 | 0.18% |
| Cached-input tokens | 297,513.4 | 299,675 | 261,376 | 335,910 | 35,235.14 | 11.84% |
| Cache-creation input tokens | 13,708.2 | 13,739 | 13,224 | 14,222 | 407.68 | 2.97% |
| Output tokens | 1,273.8 | 1,280 | 1,154 | 1,460 | 119.59 | 9.39% |
| Tool calls | 9.0 | 9 | 8 | 10 | 1.00 | 11.11% |

Observed models in every valid run:

- `claude-sonnet-5`
- `claude-haiku-4-5-20251001`

Native telemetry completeness under the current generic rubric remains 0.4667. Missing fields remain UNKNOWN, not zero.

## Interpretation

The fixed task's fresh-input footprint is extremely stable (CV 0.18%), while cached-input processing, tool calls, duration, output and total cost vary materially more across otherwise successful runs.

This is a useful runtime-variance signal, but it is **not causal evidence**. The current evidence does not establish whether variation is caused by model stochasticity, tool trajectory, provider/runtime internals, cache state, instruction/context composition, internal utility calls, or another factor.

Provider-reported cached-input tokens must not be interpreted as unique semantic context size. They represent provider-reported cache/processing usage.

## Baseline adequacy decision

No r07 is required before the first diagnostic/intervention phase unless later comparison variance proves n=5 inadequate.

Use this frozen series as B2 Baseline v1 for the first isolated comparison. Preserve prompt, fixture, deterministic evaluator and baseline artifacts unchanged.

## Next experimental question

The highest-information-gain question is now attribution rather than immediate optimisation:

> What resource components are responsible for the roughly 298k mean provider-reported cached-input processing observed on this small successful task, and which of those components are controllable without degrading outcome quality or mandatory compliance?

The corresponding experiment is specified in `experiments/B2_CONTEXT_INSTRUCTION_ATTRIBUTION_SPEC.md`.

## Guardrails

- Do not infer causality from descriptive correlations.
- Do not claim cost savings until an isolated intervention is compared against this frozen baseline with non-inferior deterministic outcomes.
- Do not optimise away mandatory safety/governance instructions.
- Do not add instrumentation solely to improve the generic telemetry-completeness percentage.
- Prefer the smallest observation layer that can resolve the specific attribution question.
- Maintain the project maturity sequence: Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise.
