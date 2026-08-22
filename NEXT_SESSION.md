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
13. `experiments/B2_ATTRIBUTION_STAGE_A_RESULT.md`
14. `experiments/B2_ATTRIBUTION_STAGE_B_PLAN.md`
15. `experiments/CODEX_B2_CONTROLLED_BASELINE_PLAN.md`
16. `experiments/TELEMETRY_GAP_DECISION_PROTOCOL.md`
17. `experiments/RUN_SCHEMA.json`
18. `experiments/analyze_b2_baselines.py`
19. `experiments/analyze_b2_attribution_stage_a.py`
20. `experiments/analyze_b2_native_usage_detail.py`
21. `experiments/adapters/claude_code/run_b2_baseline.ps1`
22. `experiments/adapters/claude_code/normalize_claude_run.py`
23. `experiments/adapters/claude_code/finalize_b2_outcome.py`
24. `research/MARKET_LANDSCAPE.md`
25. `research/COMPETITOR_MATRIX.md`
26. `research/SOURCE_REGISTER.md`

Consult the pinned central framework `gurpreet-singh-au/ai-project-framework` v1.0.0 at commit `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2` for material governance questions.

## Current phase

Phase 0B — competitive boundary + experimental proof preparation. Do not start production implementation.

## Frozen Claude baseline

B2 Baseline v1 contains five valid runs: r02-r06. r01 is invalid discovery evidence only.

All five valid runs passed the independent deterministic evaluator with 100% tested mandatory compliance.

Frozen means:

- no r07 by default;
- do not alter historical prompt/fixture/evaluator artifacts;
- do not pool future telemetry-enabled diagnostics into the baseline;
- compare future intervention distributions against this baseline only after measurement semantics are understood.

## Stage A attribution result

Stage A is complete and formally recorded in `experiments/B2_ATTRIBUTION_STAGE_A_RESULT.md`.

Key findings:

- explicit `subagent_stats.spawned = 0` across every valid B2 baseline run;
- zero requested/completed/failed subagents;
- secondary Haiku usage is therefore not a spawned-subagent signal;
- Haiku usage is small and stable; exact invocation purpose remains UNKNOWN;
- Sonnet dominates observed cost and cache processing;
- message-level cache-read snapshots grow from roughly 22k early to roughly 35k–36k later;
- final 261k–336k cache-read totals represent repeated processing/reuse across turns, not a unique context size;
- native stream evidence still cannot attribute system instructions, project instructions, tool schemas, file context, history and residual runtime overhead sufficiently.

Stage A decision: **INSUFFICIENT EVIDENCE FOR COMPOSITION ATTRIBUTION; PROCEED TO STAGE B.**

## Immediate next action — Claude Stage B1

Execute a **native OpenTelemetry capability audit** before changing the benchmark harness.

Anthropic documentation establishes OpenTelemetry as a supported Claude Code monitoring mechanism, but do not assume it exposes request composition. Verify what the installed runtime actually emits.

Determine whether native telemetry can expose any of:

- model-request boundaries;
- per-request model identity;
- input/cache/output usage;
- tool-use events;
- session identifiers;
- parent/child or internal-call lineage;
- prompt/system/tool-schema size or composition;
- context/compaction events;
- per-request latency;
- retry/error events.

Classify each field OBSERVED, DERIVED, UNAVAILABLE or UNKNOWN.

Do not enable a proxy/gateway or custom SDK wrapper until the native capability audit is complete.

If native telemetry is useful, the first telemetry-enabled B2 run must be diagnostic-only with an ID such as `B2-ATTR-001-otel-diagnostic-r01`. Do not count it as baseline or intervention evidence.

## Parallel Codex lane

A separate plan now exists at `experiments/CODEX_B2_CONTROLLED_BASELINE_PLAN.md`.

Prepare Codex under its own adapter boundary:

`experiments/adapters/codex/`

The first Codex execution is discovery-only. Validate CLI/runtime availability, authentication/credit path, workspace permissions, sandbox behavior, test environment, edit persistence, telemetry/log formats and deterministic evaluator compatibility before freezing a Codex baseline configuration.

Do not mix Codex observations with Claude B2 Baseline v1.

## Intervention rule

No context/instruction/tool optimisation intervention is selected yet.

Select exactly one isolated intervention only after Stage B identifies a plausible dominant controllable source, or after evidence redirects the project to another resource class.

## First empirical gate

Do not claim the project thesis is validated until at least two representative workloads demonstrate material compute/cost or latency improvement with non-inferior parent-task quality and 100% tested mandatory-rule compliance.

## Do not do yet

- Do not run Claude r07 by default.
- Do not add OpenTelemetry merely to increase completeness percentage.
- Do not assume OpenTelemetry exposes raw request composition until observed.
- Do not add a gateway/proxy before native telemetry is shown insufficient.
- Do not build an autonomous optimiser or production control plane.
- Do not choose a permanent provider/model/runtime from B2 alone.
- Do not equate cached-input totals with unique semantic context.
- Do not call the secondary Haiku model a subagent without contrary lineage evidence.
