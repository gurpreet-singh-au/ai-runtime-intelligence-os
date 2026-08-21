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
8. `research/MARKET_LANDSCAPE.md`
9. `research/COMPETITOR_MATRIX.md`
10. `research/BENCHMARK_AND_BASELINE_SPEC.md`
11. `benchmarks/README.md`
12. `benchmarks/prompts/B2-001-baseline.md`
13. `experiments/BASELINE_TRANCHE_01.md`
14. `experiments/baseline_tranche_01_manifest.json`
15. `experiments/RUN_SCHEMA.json`
16. `experiments/TELEMETRY_GAP_DECISION_PROTOCOL.md`
17. `experiments/adapters/claude_code/README.md`
18. `experiments/adapters/claude_code/FIRST_RUN.md`
19. `experiments/adapters/claude_code/normalize_claude_run.py`
20. `research/SOURCE_REGISTER.md`

Also consult the pinned central framework `gurpreet-singh-au/ai-project-framework` v1.0.0 at commit `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2` when material governance questions arise.

## Current phase

Phase 0B — competitive boundary + experimental proof preparation. Do not start production implementation.

## Work completed in current tranche

- primary-source market landscape and competitor matrix created;
- canonical provider-neutral telemetry model defined;
- B2-001/B3-001/B5-001/B7-001 converted into concrete reproducible cases;
- deterministic defect fixtures created for B2/B5;
- frozen semantic rubrics created for B3/B7;
- baseline manifest and passive-observation execution plan created;
- Claude Code chosen provisionally as the first observation runtime only, not as an architecture dependency;
- B2 baseline PowerShell runner prepared;
- stream inventory tooling prepared;
- conservative Claude-to-canonical normalizer prepared and wired into the runner;
- normalizer tests added to verify missing telemetry stays UNKNOWN/null and model self-claims do not become deterministic success;
- telemetry-gap decision protocol added so r01 determines whether native CLI, OpenTelemetry, gateway/proxy, SDK harness, or runtime switching is appropriate;
- no baseline model run has been claimed yet.

## Next highest-value action

Execute **only** `B2-001-baseline-r01` first in a runtime-capable Claude Code environment.

Runner:

```powershell
powershell -ExecutionPolicy Bypass -File .\experiments\adapters\claude_code\run_b2_baseline.ps1
```

The runner should produce raw evidence plus:

- `STREAM_INVENTORY.json`
- `normalized-run.json`
- `TELEMETRY_COMPLETENESS.json`

Then **stop before r02-r05**.

## Post-r01 decision

Apply `experiments/TELEMETRY_GAP_DECISION_PROTOCOL.md`.

Choose the smallest observation layer that makes the required hypothesis measurable:

1. native CLI stream if sufficient;
2. native OpenTelemetry if usage/session evidence is missing;
3. observation-only gateway/proxy if request/provider economics are missing;
4. thin Agent SDK/runtime harness if lineage/tool lifecycle is essential and unavailable;
5. another runtime if instrumentation would materially distort normal execution.

Do not add instrumentation merely because it is technically possible.

## Once telemetry is stable

Run baseline repetitions, quantify variance, and only then begin isolated interventions:
- context selection;
- instruction compilation;
- tool-result externalisation;
- agent-count optimisation;
- subagent model routing;
- deterministic substitution;
- loop/no-progress advisory;
- model/reasoning routing;
- verification allocation.

## First empirical gate

Do not claim the thesis is validated until at least two representative workloads show material compute/cost or latency improvement with non-inferior parent-task quality and 100% tested mandatory-rule compliance.

## Do not do yet

- Do not choose a permanent model provider or agent framework.
- Do not make OpenRouter, Portkey, Langfuse, LangSmith or Braintrust foundational.
- Do not build another generic tracing dashboard or model gateway.
- Do not build an autonomous optimiser.
- Do not claim cost savings without measured baseline/outcome data.
- Do not optimise away mandatory safety/governance instructions.
- Do not assume more subagents improve quality.
- Do not infer causality from trace correlation alone.
