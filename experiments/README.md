# Experiments — AI Runtime Intelligence OS

Status: Phase 0 experimental harness design

## Purpose

This directory will contain reproducible runtime-efficiency experiments derived from:

- `architecture/TELEMETRY_MODEL.md`
- `research/BENCHMARK_AND_BASELINE_SPEC.md`
- `research/EXPERIMENT_PROGRAM.md`

The goal is to test whether runtime interventions reduce compute, cost or latency while preserving required parent-task quality, safety, reliability and mandatory-rule compliance.

## Rules

1. Baselines must represent normal/default runtime behaviour; do not intentionally weaken them.
2. Change one major variable at a time before testing combined policies.
3. Preserve provider/model/runtime versions and task snapshots.
4. Record unknown telemetry as unknown rather than fabricating estimates.
5. Do not accept raw token/cost savings as success without outcome evaluation.
6. Mandatory-rule compliance failures invalidate an intervention.
7. High-risk scenarios may correctly consume more compute/verification.
8. Report variance and uncertainty; one successful run is not proof.
9. Use deterministic evaluators before model judges where possible.
10. Production autonomous intervention remains out of scope for Phase 0.

## Proposed layout

```text
experiments/
  README.md
  RUN_SCHEMA.json
  cases/
    <benchmark-id>/
      README.md
      task.yaml
      expected/
  runs/
    <date>/<run-id>/
      run.json
      artifacts/
  analysis/
    <experiment-family>/
```

## First tranche

Start with four task families:

- B2 — small bug fix
- B3 — repository research
- B5 — debug/test loop
- B7 — multi-agent decomposable research

Initial comparison:

`normal baseline -> isolated intervention -> evaluated outcome`

Do not run the combined Runtime Intelligence policy until isolated interventions are understood.

## First success milestone

On at least two representative workloads, demonstrate material compute/cost or latency reduction with non-inferior parent-task quality and 100% tested mandatory-rule compliance.
