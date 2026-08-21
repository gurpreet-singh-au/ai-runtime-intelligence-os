# Next Session — AI Runtime Intelligence OS

Last updated: 2026-08-21

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
11. `research/EXPERIMENT_PROGRAM.md`
12. `research/OPENROUTER_AND_MODEL_ROUTING.md`
13. `experiments/README.md`
14. `experiments/RUN_SCHEMA.json`
15. `research/SOURCE_REGISTER.md`

Also consult the pinned central framework `gurpreet-singh-au/ai-project-framework` v1.0.0 at commit `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2` when material governance questions arise.

## Current phase

Phase 0B — competitive boundary + experimental proof design. Do not start production implementation.

## Work completed in current tranche

- primary-source market landscape started;
- competitor/adjacent capability matrix created;
- canonical provider-neutral telemetry model defined;
- first benchmark and baseline specification defined;
- first experiment harness directory and machine-readable run schema created;
- project state advanced from general research into falsifiable experimental preparation.

## Next highest-value actions

1. Turn B2/B3/B5/B7 into concrete benchmark cases with fixed snapshots, acceptance criteria and deterministic evaluators where possible.
2. Choose the **first passive-observation runtime adapter** based on telemetry access and reproducibility, not vendor preference.
3. Build only the minimum instrumentation required to populate `experiments/RUN_SCHEMA.json`; prefer OTel/native/vendor telemetry before custom collection.
4. Run untouched baseline repetitions before testing any intervention.
5. Calculate variance and refine repetition/sample-size requirements.
6. Then run isolated interventions in this order where practical:
   - context selection;
   - instruction compilation;
   - tool-result externalisation;
   - agent-count optimisation;
   - subagent model routing;
   - deterministic substitution;
   - loop/no-progress advisory;
   - model/reasoning routing;
   - verification allocation.
7. Continue competitor deep dives, especially Portkey and any product claiming adaptive runtime optimisation.
8. Update `PROJECT_STATE.md`, `DECISIONS.md`, `OPEN_QUESTIONS.md`, `CHANGELOG.md`, evaluation/model/open-source registers and source register after each material tranche.

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

## Immediate research/engineering question

What is the smallest passive instrumentation layer that can reconstruct a representative agent run as a provider-neutral resource graph with enough outcome evidence to test whether a proposed runtime intervention actually helped?
