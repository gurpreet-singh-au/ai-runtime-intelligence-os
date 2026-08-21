# Experiment Program — Proving Runtime Optimisation

Date: 2026-08-21
Status: Proposed research protocol

## Objective

Turn the project thesis into falsifiable experiments. The product should not advance on claims such as “smaller context is better” or “fewer agents are cheaper” without measuring quality, reliability, latency, and cost.

## Experimental unit

Each experiment should use a reproducible **task run** containing:

- task identifier and task class
- repository/data snapshot
- provider/model/version
- system/project/user instructions
- tool set and tool schemas
- starting state/checkpoint
- context composition
- reasoning configuration
- agent/subagent topology
- budget/stop policy
- output and artifacts
- evaluator results
- runtime telemetry

## Baseline protocol

For every representative task, first capture the unoptimised/native execution as the baseline. Repeat sufficiently to observe variance.

Baseline metrics:
- task success
- quality/evaluator score
- input/output/cached token usage
- context size over time
- model calls
- tool calls and tool-result volume
- agent/subagent calls
- wall-clock duration
- retries
- repeated reads/searches
- meaningful state transitions
- direct monetary cost where observable

## Intervention families

### E1 — Context selection
Compare full accumulated context against relevance-selected context while keeping model, tools, instructions, and agent topology fixed.

Primary question: how much context can be removed before outcome quality degrades?

### E2 — Instruction compilation
Compare full project/system instruction bundles against task-scoped compiled instruction sets with mandatory constraints preserved.

Primary question: can token load and interference be reduced without governance or quality regressions?

### E3 — Dynamic tool exposure
Compare exposing the full tool library against a task-selected subset plus on-demand tool discovery.

Primary question: does smaller tool surface reduce context/cost and tool-choice errors?

### E4 — Tool-result externalisation
Compare retaining raw logs/results in context versus structured summaries/state plus retrievable evidence pointers.

Primary question: can large tool outputs be made cold without losing recoverability or reasoning accuracy?

### E5 — Agent-count optimisation
Compare parent-only, homogeneous multi-agent, diverse multi-agent, and adaptive spawning policies.

Primary question: where does marginal benefit from another agent saturate?

### E6 — Model/reasoning routing
Compare static frontier-model execution against complexity/risk-based model and reasoning allocation.

Primary question: can easier tasks be routed downward while difficult tasks retain or increase compute?

### E7 — Checkpoint and clean-resume
Compare append-only long sessions against periodic structured checkpoints followed by clean runtime restart.

Primary question: does externalised state preserve continuity while reducing accumulated context and drift?

### E8 — Loop/anomaly stopping
Introduce detection for repeated operations and declining useful-state-change rate.

Primary question: can unproductive execution be terminated or replanned without prematurely stopping difficult but productive work?

### E9 — Deterministic substitution
Replace model-mediated mechanical operations with deterministic code where semantics allow it.

Primary question: which inference calls are unnecessary because the operation is inherently deterministic?

### E10 — Combined runtime policy
Apply the best independently validated interventions together.

Primary question: do savings compose, or do interactions create hidden quality regressions?

## Initial task families

The first benchmark should deliberately include different resource profiles:

1. trivial code edit
2. small bug fix
3. repository research/question answering
4. multi-file feature
5. test/debug loop
6. architecture analysis
7. documentation update
8. high-risk/security-sensitive change
9. long-running research task
10. large-repository task requiring selective retrieval

## Quality gates

An optimisation is not accepted because it lowers tokens or cost. It must meet a quality-preservation threshold defined per task class.

Candidate rule:

- no statistically meaningful reduction in success rate for ordinary tasks;
- stricter non-inferiority margin for high-risk tasks;
- mandatory-rule compliance must remain 100% for deterministic governance tests;
- savings should be reported together with uncertainty/variance.

## Core derived metrics

### Cost per successful outcome
`total execution cost / successful executions`

### Risk-adjusted cost per successful outcome
Cost weighted by task consequence and observed failure severity.

### Context utility density
Estimated task-relevant, non-duplicative context divided by total supplied context.

### Useful state change rate
Meaningful progress events divided by compute/time.

### Agent marginal utility
Incremental quality/success improvement attributable to an added agent divided by incremental cost.

### Tool utility rate
Useful tool calls divided by all tool calls, with separate measurement of duplicate/redundant calls.

### Instruction efficiency
Mandatory + task-applicable instruction representation divided by total instruction tokens supplied.

### Runtime waste ratio
Compute attributable to duplicate, stale, failed-without-information-gain, or loop behaviour divided by total compute.

## Instrumentation principle

Prefer passive observation first. Do not intervene until the baseline instrumentation is trustworthy. Runtime optimisation based on bad telemetry can create invisible regressions.

## Experiment governance

- pin provider/model versions where possible
- preserve raw traces and evaluator outputs
- record exact intervention policy version
- never overwrite prior experiment results
- separate hypothesis generation from evaluation
- retain failure cases
- require regression suites before changing default runtime policies
- learned policies may recommend changes but do not silently rewrite governance rules

## Phase progression

### Phase A — Observe
Build a neutral execution trace/resource model.

### Phase B — Explain
Attribute cost/latency/context growth to concrete runtime causes.

### Phase C — Recommend
Generate non-binding optimisation recommendations.

### Phase D — Controlled intervention
Apply bounded optimisations with explicit policy constraints.

### Phase E — Adaptive runtime
Learn allocation policies from evaluated outcomes with rollback and regression protection.

## First success criterion

Demonstrate on a representative workload that the system can reduce total compute/cost or latency materially while maintaining non-inferior outcome quality and mandatory-rule compliance.

Until that is demonstrated, the project remains a research hypothesis rather than a validated product claim.
