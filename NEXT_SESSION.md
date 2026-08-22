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
12. `experiments/B2_ATTRIBUTION_STAGE_A_RESULT.md`
13. `experiments/B2_ATTRIBUTION_STAGE_B1_RESULT.md`
14. `experiments/B2_ATTRIBUTION_STAGE_B2_RESULT.md`
15. `experiments/B2_ATTRIBUTION_STAGE_B_PLAN.md`
16. `experiments/CODEX_B2_CONTROLLED_BASELINE_PLAN.md`
17. `experiments/TELEMETRY_GAP_DECISION_PROTOCOL.md`
18. `experiments/analyze_b2_otel_diagnostic.py`
19. `experiments/adapters/claude_code/run_b2_baseline.ps1`
20. `experiments/adapters/claude_code/run_b2_otel_diagnostic.ps1`
21. `research/MARKET_LANDSCAPE.md`
22. `research/COMPETITOR_MATRIX.md`
23. `research/SOURCE_REGISTER.md`

Consult the pinned central framework `gurpreet-singh-au/ai-project-framework` v1.0.0 at commit `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2` for material governance questions.

## Current phase

Phase 0B — competitive boundary + experimental proof preparation. Do not start production implementation.

## Frozen Claude baseline

B2 Baseline v1 remains frozen at r02-r06. r01 is invalid discovery evidence only.

All five valid runs passed the independent deterministic evaluator with 100% tested mandatory compliance.

Do not run Claude r07 by default and do not pool telemetry diagnostics into Baseline v1.

## Claude attribution status

### Stage A

Complete. Native stream evidence established zero spawned subagents and repeated cache processing but could not resolve request source composition.

### Stage B1

Complete. Native Claude Code 2.1.238 OTLP transport, metrics, logs and traces were verified on Windows through privacy-safe local probes.

### Stage B2

Complete. `B2-ATTR-001-otel-diagnostic-r01` passed deterministic success/compliance and exposed 9 Sonnet requests plus one Haiku title-generation request.

Key mechanistic result:

`next cache_read = previous cache_read + previous cache_creation`

for all eight successive Sonnet transitions.

First Sonnet processed input = 31,594 tokens.
Final Sonnet processed input = 36,096 tokens.
Post-first growth = 4,502 tokens.
First-request share of final processed input = 87.53%.

Thus most of the final B2 request footprint existed before later tool-result/history growth.

Native `llm_request.context` was only an 11-character non-JSON string and did not expose semantic composition.

Stage B2 exit: **B-ESCALATE**.

## Highest-value Claude follow-up

Do not run further OTel probes merely to improve completeness.

Design the smallest controlled, local and reversible request-inspection mechanism that can observe **outbound request structure and size before model transmission** while persisting no raw prompt/code/tool/repository content.

Target source classes:

1. system/runtime instructions;
2. task/user prompt;
3. tool-schema payload;
4. conversation/message history;
5. tool-result blocks;
6. project/repository instructions;
7. residual request fields.

This is a measurement mechanism, not a product dependency.

## Immediate parallel action — Codex discovery

Start the separate `CODEX-B2-C1` lane now.

First perform **CLI capability discovery only**. Do not guess command flags from memory and do not immediately count the first execution as a baseline.

Record locally:

- `codex --version`;
- top-level help/command surface;
- non-interactive execution help if available;
- sandbox/approval options exposed by the installed build;
- structured/JSON output options;
- model/reasoning configuration options exposed by the installed build.

Then create the first discovery execution only after the installed CLI surface is understood.

Suggested first execution ID remains:

`B2-001-codex-discovery-r01`

Validate sandbox/write behavior, Python/pytest resolution, edit persistence, event/usage telemetry and deterministic evaluator compatibility.

## Intervention rule

No Claude context/instruction/tool optimisation intervention is selected yet.

Do not tune Codex to beat Claude. Preserve canonical B2 task semantics and keep the runtime populations analytically separate.

## First empirical gate

Do not claim the project thesis is validated until at least two representative workloads demonstrate material compute/cost or latency improvement with non-inferior parent-task quality and 100% tested mandatory-rule compliance.

## Do not do yet

- Do not run Claude r07 by default.
- Do not continue adding OTel probes without a new specific hypothesis.
- Do not persist raw outbound request content merely to improve attribution.
- Do not make a measurement proxy/wrapper a foundational architecture dependency.
- Do not pool Codex and Claude statistics.
- Do not tune runtime-specific prompts for comparative advantage.
- Do not build an autonomous optimiser or production control plane.
