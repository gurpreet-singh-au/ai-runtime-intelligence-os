# Next Session — AI Runtime Intelligence OS

Last updated: 2026-08-21

## Read first

1. `PROJECT_STANDARD_ADOPTION.md`
2. `PROJECT_SPECIFIC_NON_NEGOTIABLES.md`
3. `PROJECT_STATE.md`
4. `DECISIONS.md`
5. `ROADMAP.md`
6. `architecture/AI_RUNTIME_RESOURCE_MODEL.md`
7. `research/DEEP_RESEARCH_TRANCHE_01.md`
8. `research/DEEP_RESEARCH_TRANCHE_02_RESOURCE_MECHANICS.md`
9. `research/OPENROUTER_AND_MODEL_ROUTING.md`
10. `research/SOURCE_REGISTER.md`

Also consult the pinned central framework `gurpreet-singh-au/ai-project-framework` v1.0.0 at commit `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2` when material governance questions arise.

## Current phase

Phase 0 — research/opportunity validation. Do not start production implementation.

## Next highest-value actions

1. Build a primary-source competitor/adjacent landscape covering observability, agent tracing, LLM gateways, model routers, context/memory platforms, agent orchestration, AI FinOps, and runtime optimisation.
2. Separate features into `observe`, `evaluate`, `route`, `control`, `optimise`, and `learn` to identify the true opportunity boundary.
3. Draft `architecture/TELEMETRY_MODEL.md` describing the minimum provider-neutral events/fields required for context, instruction, cache, tool, model, agent, runtime, verification, cost, and outcome attribution.
4. Define a first benchmark workload and baseline experiment, ideally using a coding-agent/long-running-agent workload where waste is already observable.
5. Start `OPEN_SOURCE_STACK.md` with credible candidates only after current licence/maturity verification.
6. Update `PROJECT_STATE.md`, `DECISIONS.md`, `OPEN_QUESTIONS.md`, `CHANGELOG.md`, and source register after substantive work.

## Do not do yet

- Do not choose a permanent model provider.
- Do not make OpenRouter foundational.
- Do not build an autonomous optimiser.
- Do not claim cost savings without measured baseline/outcome data.
- Do not optimise away mandatory safety/governance instructions.
- Do not assume more subagents improve quality.

## Immediate research question

Where exactly is the defensible boundary between existing AI observability/routing products and a cross-provider runtime resource governor that can determine the minimum sufficient computation for a successful outcome?
