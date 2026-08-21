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
11. `experiments/BASELINE_TRANCHE_01.md`
12. `experiments/RUN_SCHEMA.json`
13. `experiments/TELEMETRY_GAP_DECISION_PROTOCOL.md`
14. `experiments/adapters/claude_code/run_b2_baseline.ps1`
15. `experiments/adapters/claude_code/normalize_claude_run.py`
16. `experiments/adapters/claude_code/finalize_b2_outcome.py`
17. `research/MARKET_LANDSCAPE.md`
18. `research/COMPETITOR_MATRIX.md`
19. `research/SOURCE_REGISTER.md`

Also consult the pinned central framework `gurpreet-singh-au/ai-project-framework` v1.0.0 at commit `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2` when material governance questions arise.

## Current phase

Phase 0B — competitive boundary + experimental proof preparation. Do not start production implementation.

## Empirical status

- `B2-001-baseline-r01` is preserved as an invalid discovery run. It exposed two harness defects: Python PATH contamination from an unrelated Hermes venv, and Claude Code edit permission denial in non-interactive mode. Exclude r01 from baseline performance statistics.
- The harness now creates a benchmark-local Python 3.11 venv, installs pinned pytest 9.1.1, prepends that venv to Claude's subprocess PATH, and uses Claude Code `acceptEdits` rather than disabling permissions broadly.
- `B2-001-baseline-r02` is the first valid successful baseline candidate:
  - pre-test: 2 failed / 1 passed;
  - post-test: 3 passed;
  - Claude exit code: 0;
  - bounded implementation diff only in `runtime_fixture/pricing.py`;
  - reported total cost: USD 0.1763469;
  - Claude result duration: 20,054 ms;
  - aggregate input tokens: 1,085;
  - cache-read input tokens: 262,353;
  - cache-creation input tokens: 13,224;
  - output tokens: 1,154;
  - tool calls: 8;
  - observed models: Claude Sonnet 5 and Claude Haiku 4.5.
- Native CLI telemetry completeness is 0.4667 under the generic rubric. This percentage alone is not a reason to add instrumentation; B2 already exposes outcome, cost, latency, model usage, token/cache usage, tool count/sequence, code diff, and deterministic verification.
- Deterministic B2 finalization is now wired into the runner via `finalize_b2_outcome.py`, producing `B2_OUTCOME_EVALUATION.json` and updating `normalized-run.json` from deterministic evidence rather than model self-report.

## Next highest-value action

Collect additional identical valid B2 baseline repetitions to estimate natural variance before testing any Runtime Intelligence intervention.

Run **one repetition at a time**, beginning with r03:

```powershell
powershell -ExecutionPolicy Bypass -File .\experiments\adapters\claude_code\run_b2_baseline.ps1 -RunId "B2-001-baseline-r03"
```

After each run, verify at minimum:

- `B2_OUTCOME_EVALUATION.json` reports PASS;
- pre-test failed as expected;
- post-test passed;
- changed files remain bounded to the intended implementation;
- no permission denial or environment failure invalidated the run;
- normalized telemetry contains cost, duration, model usage and token/cache usage.

If r03 is valid, continue r04 and r05 under the exact same frozen configuration. Do not change prompt, fixture, model selection settings, permission mode, Python version, pytest version or runner semantics during this baseline series.

## Baseline analysis after enough valid repetitions

For valid B2 baseline runs only, calculate:

- success rate;
- total cost mean, median, min/max, standard deviation and coefficient of variation;
- runtime duration distribution;
- cache-read/cache-creation/input/output token distributions;
- tool-call count and sequence variation;
- model usage variation;
- correlations that are descriptive only, not causal.

Use variance to determine whether five valid repetitions are adequate or whether more are needed before intervention comparison.

## Telemetry decision

Do not add OpenTelemetry merely to increase generic completeness. Add a new observation layer only when a specific hypothesis cannot be tested with current evidence. Context composition, instruction composition and Useful State Change remain unavailable natively and may require richer instrumentation for later experiments, but they are not required to establish the initial B2 cost/latency baseline distribution.

## Once B2 baseline is stable

Begin isolated interventions one at a time, with no combined optimiser initially. Candidate sequence remains:

- context selection;
- instruction compilation;
- tool-result externalisation;
- agent-count optimisation;
- subagent model routing;
- deterministic substitution;
- loop/no-progress advisory;
- model/reasoning routing;
- verification allocation.

Choose the first intervention according to the B2 resource profile rather than the original list order if evidence shows another intervention is more relevant.

## First empirical gate

Do not claim the thesis is validated until at least two representative workloads show material compute/cost or latency improvement with non-inferior parent-task quality and 100% tested mandatory-rule compliance.

## Do not do yet

- Do not choose a permanent model provider or agent framework.
- Do not make OpenRouter, Portkey, Langfuse, LangSmith or Braintrust foundational.
- Do not build another generic tracing dashboard or model gateway.
- Do not build an autonomous optimiser.
- Do not claim cost savings from r02 alone.
- Do not optimise away mandatory safety/governance instructions.
- Do not assume more subagents improve quality.
- Do not infer causality from trace correlation alone.
- Do not include r01 in baseline statistics.
