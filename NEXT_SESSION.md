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
12. `experiments/BASELINE_TRANCHE_01.md`
13. `experiments/baseline_tranche_01_manifest.json`
14. `experiments/RUN_SCHEMA.json`
15. `experiments/evaluators/B3_001_RUBRIC.md`
16. `experiments/evaluators/B7_001_RUBRIC.md`
17. `research/SOURCE_REGISTER.md`

Also consult the pinned central framework `gurpreet-singh-au/ai-project-framework` v1.0.0 at commit `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2` when material governance questions arise.

## Current phase

Phase 0B — competitive boundary + experimental proof preparation. Do not start production implementation.

## Work completed in current tranche

- primary-source market landscape started;
- competitor/adjacent capability matrix created;
- canonical provider-neutral telemetry model defined;
- benchmark/baseline specification defined;
- B2-001/B3-001/B5-001/B7-001 converted into concrete reproducible cases;
- deterministic defect fixtures created for B2/B5;
- frozen semantic rubrics created for B3/B7;
- baseline manifest and passive-observation execution plan created;
- Claude Code / Claude coding-agent workflow selected provisionally as first observation runtime only, not as an architecture dependency;
- benchmark fixture logic checked to confirm B2/B5 fail their intended pre-fix conditions;
- no baseline model run has been claimed yet.

## Next highest-value action

Execute the first untouched baseline cycle in a runtime-capable environment:

1. B2-001 baseline r01
2. B3-001 baseline r01
3. B5-001 baseline r01
4. B7-001 baseline r01

For each run preserve:
- exact repository commit/snapshot;
- runtime/provider/model/version;
- raw transcript/trace where available;
- token/cache/cost usage where available;
- agent/subagent events;
- tool/search/file/test events;
- changed-file diff for coding tasks;
- test/evaluator result;
- normalized `RUN_SCHEMA.json` record.

Unknown telemetry fields stay null. Do not invent relevance, causal contribution or hidden model internals.

After r01 across all four cases, inspect telemetry completeness before spending on r02-r05. If the first runtime cannot expose sufficient evidence, revise the observation adapter rather than pretending the missing data exists.

## After stable baselines

Only then begin isolated interventions:
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
