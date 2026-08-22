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
15. `experiments/CODEX_B2_CONTROLLED_BASELINE_PLAN.md`
16. `experiments/CODEX_B2_DISCOVERY_RESULT.md`
17. `experiments/TELEMETRY_GAP_DECISION_PROTOCOL.md`
18. `research/COMMERCIAL_DEFENSIBILITY_REAUDIT_2026-08-22.md`
19. `research/COMPETITOR_MATRIX.md`
20. `experiments/analyze_b2_otel_diagnostic.py`
21. `experiments/adapters/codex/analyze_codex_discovery.py`

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

## Codex discovery status — NATIVE WINDOWS BLOCKED

Formal record: `experiments/CODEX_B2_DISCOVERY_RESULT.md`.

Installed Codex: `codex-cli 0.144.3`.

Discovery r03 reached a real model turn and emitted valid JSONL telemetry, but the agent explicitly reported the workspace as read-only despite the harness requesting `--sandbox workspace-write`.

Observed r03 usage:

- input tokens: 9,010
- cached input tokens: 0
- output tokens: 46
- reasoning output tokens: 0

No command execution, no file-change event and no tracked code diff occurred. Post-tests remained failing, so the deterministic evaluator correctly rejected the run.

The only workspace changes were untracked Python `__pycache__` directories from test execution.

This closely matches active upstream OpenAI Codex issue `#34961`, which reports native Windows `codex exec --sandbox workspace-write` behaving read-only even while exiting successfully.

The separate `models_cache.json` / `base_instructions` warning matches upstream issue `#39291`, but it is no longer the primary blocker because r03 reached `turn.completed`.

### Codex next action

Do **not** use `danger-full-access` merely to force a successful benchmark run.

Next, check whether an already-available WSL/Linux environment exists locally and whether Codex is already installed/authenticated there. This is discovery only:

- do not install software;
- do not copy auth material;
- do not alter Windows Codex config;
- do not count a capability probe as a benchmark run.

If an existing WSL/Linux Codex path is available, first run a minimal synthetic bounded-write probe. Only if `workspace-write` works as intended should B2 be attempted there under a new discovery ID.

Any Codex version change is an experimental-factor change and requires fresh capability/sandbox probing before baseline freeze.

## Competitive/commercial status

The commercial boundary is narrower than initially assumed.

Material overlaps now include:

- Not Diamond Code: coding-agent session/cache-aware model and reasoning-effort routing.
- cascadeflow: MIT-licensed agent runtime intelligence/harness with model cascading and budget/compliance/KPI/tool controls.
- established observability/evaluation/gateway platforms.

Do not claim `agent runtime intelligence`, generic model routing, generic context optimisation, or agent governance as unique.

The remaining potentially differentiated thesis is **cross-resource marginal allocation under a common governed outcome objective** across context, instructions, models/reasoning, tools, agents, memory, verification and time.

Continue code-level teardown and empirical comparison rather than relying on product marketing.

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
- Do not weaken Codex to unrestricted filesystem access merely to obtain a valid sample.
- Do not automatically install/upgrade Codex or copy credentials into WSL as part of discovery.
- Do not build an autonomous optimiser or production control plane.
