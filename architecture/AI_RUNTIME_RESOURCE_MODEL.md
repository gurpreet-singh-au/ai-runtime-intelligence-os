# Canonical AI Runtime Resource Model

Date: 2026-08-21
Status: Research architecture v0.1

## Purpose

Define the provider-independent resources consumed during modern AI/agent execution so the project can observe, measure, allocate, and eventually optimise them without coupling the core model to Claude, OpenAI, Gemini, or any one framework.

## Runtime lifecycle

A modern execution can be modelled as:

`Objective -> instruction assembly -> context assembly -> tokenisation -> cache/prefix handling -> prefill -> reasoning/decode -> tool selection -> tool execution -> result ingestion -> additional inference -> delegation -> persistence/checkpoint -> verification -> outcome`

This pipeline may repeat many times in an agent loop.

## Resource classes

### R1 — Information
What the model is shown.

Subresources:
- current task/objective
- conversation history
- retrieved documents/code
- evidence
- examples
- prior model outputs
- tool results
- current working state

Metrics:
- physical input tokens
- estimated task-relevant tokens
- duplicated tokens
- stale/superseded tokens
- authority/provenance coverage
- context utility density

Controls:
- retrieve
- rank
- prune
- externalise
- summarise/compact
- re-fetch on demand

### R2 — Instructions
Rules governing behaviour.

Subresources:
- provider/system rules
- safety/security policies
- organisation policies
- user constraints/preferences
- project/repository instructions
- task instructions
- tool-use instructions
- examples/few-shot guidance

Metrics:
- instruction tokens
- duplicate/overlapping rules
- conflicts
- applicability rate
- mandatory-rule compliance

Controls:
- scope
- classify
- deduplicate
- resolve precedence
- conditionally activate
- compile into effective instruction set

Invariant: mandatory safety, security, privacy, authorisation, governance and explicit user constraints cannot be removed merely to save compute.

### R3 — Model inference
Compute supplied by the foundation model.

Subresources:
- model capability tier
- prefill processing
- decode/output generation
- reasoning effort/test-time compute
- sampling/generation attempts

Metrics:
- uncached input tokens
- cached input tokens
- output tokens
- reasoning usage where exposed
- time-to-first-token
- tokens/sec
- inference cost
- task success

Controls:
- model routing
- reasoning-effort routing
- output limits
- retry policy
- escalation/de-escalation

### R4 — Cache / reuse
Reuse of prior computation or content.

Subresources:
- exact prefix cache
- provider prompt cache
- application semantic cache
- reusable tool results
- compiled instruction bundles

Metrics:
- cache-hit rate
- cacheable-prefix stability
- cached-token ratio
- avoided cost/latency
- stale-cache risk

Controls:
- preserve stable prefixes
- cache placement/lifetime
- content versioning
- invalidation
- routing to compatible cached state

Principle: cache efficiency and cognitive efficiency are distinct. A cheaply cached irrelevant prefix can still be poor context engineering.

### R5 — Tool capability surface
Capabilities exposed to a model.

Subresources:
- tool schemas/descriptions
- MCP/server capabilities
- APIs
- code execution
- search/retrieval
- connector actions

Metrics:
- tool-schema tokens
- number of exposed tools
- tool selection accuracy
- unused exposed tools
- duplicate/overlapping capabilities
- permission risk

Controls:
- deferred discovery
- capability routing
- permission filtering
- minimal tool exposure
- deterministic dispatch

### R6 — Tool execution/results
Work performed outside the model.

Subresources:
- file reads
- searches
- shell commands
- tests
- API calls
- database operations
- external services

Metrics:
- calls
- latency
- external cost
- payload/result tokens
- repeated calls
- failure/retry rate
- information gain

Controls:
- deduplicate
- batch
- cache
- truncate/structure results
- archive raw output with pointers
- prefer deterministic computation where judgment is unnecessary

### R7 — Agency / orchestration
Parallel or delegated inference trajectories.

Subresources:
- parent agent
- subagents
- critics/evaluators
- parallel branches
- specialist agents

Metrics:
- agent count
- inference cost per agent
- overlap/correlation
- unique contribution
- coordination overhead
- wall-clock benefit
- marginal quality gain

Controls:
- spawn/no-spawn
- model tier per agent
- concurrency
- diversity
- budgets
- termination
- result aggregation

### R8 — Memory / durable state
Information preserved outside immediate inference context.

Subresources:
- structured project state
- decisions
- plans
- evidence pointers
- memory notes
- checkpoints
- historical traces

Metrics:
- retrieval precision/recall
- duplication
- staleness
- reconstructability
- state size
- read/write overhead

Controls:
- tier hot/warm/cool/cold
- checkpoint
- version
- retrieve selectively
- expire/supersede
- maintain provenance

### R9 — Time / runtime trajectory
Elapsed execution and iteration structure.

Subresources:
- session duration
- number of turns
- retries
- idle/wait time
- loop cycles
- checkpoint intervals

Metrics:
- wall-clock time
- compute-active time
- useful state changes/hour
- repeated-operation ratio
- no-progress intervals

Controls:
- time budgets
- stop conditions
- anomaly detection
- checkpoint/reset
- strategy escalation/change

### R10 — Verification / assurance
Additional work used to increase confidence.

Subresources:
- tests
- deterministic validators
- critic/evaluator models
- cross-model verification
- policy checks
- human escalation where required

Metrics:
- defect detection
- false positives
- added cost/latency
- marginal reliability gain
- residual risk

Controls:
- risk-based verification depth
- independent evaluator selection
- deterministic checks before LLM checks
- escalation thresholds

### R11 — Infrastructure / serving
Lower-level compute and systems resources where observable.

Subresources:
- GPU/accelerator time
- KV-cache memory
- prefill capacity
- decode capacity
- network transfer
- storage
- queueing

Metrics:
- memory footprint
- throughput
- utilisation
- queue latency
- energy/compute cost where available

Controls may be direct for self-hosted/open-weight deployments and indirect for managed APIs.

### R12 — Outcome / economics
The reason resources are consumed.

Subresources:
- task completion
- quality
- reliability
- safety
- business/user value
- latency requirement
- monetary cost

Primary derived metrics:
- cost per successful outcome
- risk-adjusted cost per successful outcome
- quality per dollar
- useful state change per compute unit
- marginal utility of additional compute

## Prefill and decode

For decoder-style LLM serving, two phases matter:

- **Prefill:** processing the supplied prompt/context and producing internal KV state. Long contexts can impose substantial time/memory/compute here.
- **Decode:** generating new tokens autoregressively while attending to relevant stored state.

2026 systems research continues to optimise these phases separately, including layer-asymmetric KV visibility and prefill/decode disaggregation. The Runtime OS should therefore record input/context cost separately from output/reasoning cost whenever provider telemetry permits.

## Context externalisation principle

Raw tool output, historical transcripts and durable evidence should not automatically remain hot.

Preferred pattern:

`raw evidence -> immutable/retrievable store -> structured extraction/state -> compact active representation -> re-fetch original only when required`

This avoids choosing between "lose provenance" and "carry everything forever".

## Resource allocation policy

The control plane should estimate a Task Resource Profile before and during execution:

- complexity
- ambiguity
- consequence/risk
- required capabilities
- expected relevant context
- instruction scopes
- model strength/reasoning requirement
- agent parallelism value
- verification depth
- latency target
- cost/budget ceiling

Then allocate resources subject to hard policy constraints.

## Optimisation objective

A conceptual objective is:

`max E[Utility] = Quality + Reliability + Safety + Timeliness + OutcomeValue - InferenceCost - ToolCost - Latency - OperationalRisk`

This is not intended as a final mathematical formula. The key principle is that cost is one variable, not the objective itself.

## Marginal compute utility

For each optional increment of compute, estimate:

`MCU = expected incremental outcome utility / incremental resource cost`

Examples:
- adding 20k context tokens
- increasing reasoning effort
- spawning another subagent
- performing another search
- adding an independent verifier

Stop adding optional compute when expected marginal utility falls below the policy threshold, unless a mandatory assurance rule requires it.

## Control-loop architecture

`Observe -> Classify -> Estimate -> Plan -> Execute -> Measure -> Learn`

- Observe runtime telemetry.
- Classify task and resource components.
- Estimate relevance, marginal value and risk.
- Plan a provider-neutral allocation.
- Execute through provider/framework adapters.
- Measure actual quality/cost/latency/state change.
- Learn improved policies through governed evaluation.

## Provider adapters

Provider-specific mechanisms should be adapters, not canonical architecture.

Examples may include:
- prompt/context caching
- server-side compaction
- context editing/tool-result clearing
- reasoning effort controls
- deferred tool discovery
- model routing
- memory APIs
- agent harness checkpoints

The canonical core should survive provider feature changes.

## Research implication

The first prototype should likely be a telemetry + advisory control plane rather than an autonomous mutating governor. It should prove that we can:

1. observe resource usage correctly;
2. attribute waste/usefulness;
3. recommend a better execution plan;
4. replay or A/B test interventions;
5. preserve or improve task success;
6. quantify economic benefit.

Only then should automatic intervention expand.
