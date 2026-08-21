# Deep Research Tranche 02 — Resource Mechanics and Optimisation Surfaces

Date: 2026-08-21
Status: Research architecture

## Purpose

Go below the application-level symptom of "large context" and identify the physical/logical resources that modern AI runtimes consume, which controls providers expose, which trade-offs interact, and which abstractions remain durable as AI systems evolve.

## 1. The crucial shift: from token management to runtime resource management

Tokens are a billing/representation unit, not the whole system. A long-running agent consumes multiple coupled resources:

- prompt/context processing
- output/reasoning generation
- cache storage/reuse
- tool capability descriptions
- external tool execution
- intermediate-result ingestion
- agent/subagent inference trajectories
- durable state and retrieval
- verification
- wall-clock time
- serving/queueing infrastructure

A universal optimiser should reason over the full resource graph.

## 2. Prefill versus decode

At a simplified systems level, decoder-style inference has two distinct phases.

### Prefill
The model processes supplied input/context and builds internal state used for subsequent generation. Increasing input size primarily increases this phase's work and memory pressure.

### Decode
The model generates tokens sequentially using the existing context/state. Output length and reasoning effort primarily increase this phase.

### Why this matters

Two tasks with identical total token counts can have different runtime/economic profiles:

- huge prompt + tiny answer
- tiny prompt + long reasoning/output

The Runtime OS should therefore avoid a single "token count" metric. It needs at least:

- input/context load
- cached versus uncached input
- output load
- reasoning/test-time compute
- wall-clock latency
- tool/external compute

## 3. KV/prefix state and caching

Provider caching means repeated stable prefixes can be processed/reused more cheaply. But cached content may still occupy logical context and remain available to the model.

This creates a real optimisation tension:

- removing irrelevant context may improve focus and reduce context occupancy;
- modifying a stable prefix may destroy a cache hit and trigger a new cache write;
- keeping a stable but irrelevant prefix may be cheap financially but poor semantically.

### Required future metric

`Net Context Value = Semantic Utility + Cache Economic Value - Attention/Interference Cost - Context Occupancy Cost`

This cannot be estimated purely from token price.

## 4. Context position and retrieval quality

Long-context research shows that information use is not uniform across arbitrary positions and distractor-heavy inputs. Therefore retrieval should consider not only *what* to include but:

- ordering
- grouping
- authority
- task phase
- freshness
- redundancy
- evidence relationships

A future context compiler may need to assemble a deliberately structured working set rather than append ranked chunks blindly.

## 5. Instruction mechanics

Instructions are executable governance expressed through language. Their cost has at least four components:

1. token/context cost;
2. attention/interference cost;
3. contradiction-resolution cost;
4. maintenance/versioning cost.

### Canonical instruction object

An instruction should eventually have fields such as:

- `id`
- `canonical_rule`
- `authority`
- `scope`
- `priority`
- `mandatory`
- `activation_condition`
- `effective_from`
- `effective_to`
- `supersedes`
- `dependencies`
- `provenance`
- `risk_class`

This allows deterministic applicability/precedence where possible, with LLM assistance reserved for semantic classification or ambiguous scope.

## 6. Capability exposure mechanics

Large tool ecosystems should not imply large per-turn tool surfaces.

Provider movement toward tool search/deferred discovery indicates a general pattern:

`Capability universe -> discover -> permission-check -> task-match -> expose minimal relevant surface`

This should apply not only to tools but potentially to:

- skills
- agents
- data connectors
- model capabilities
- domain packs

A future Capability Graph could represent inputs, outputs, cost, permissions, latency, reliability, data sensitivity, and provider dependencies.

## 7. Intermediate-result mechanics

Agent workflows produce a large volume of transient information. The important distinction is between:

- **evidence that must remain retrievable**, and
- **representation that must remain in working context**.

Those should not be the same object.

### Proposed transformation pipeline

`raw result -> immutable artifact -> parser/extractor -> structured state/evidence -> compact working representation`

Keep a pointer from compact representation to raw artifact.

This can preserve auditability while shrinking active context.

## 8. Agent orchestration mechanics

An additional agent is another compute channel, not a free reasoning primitive.

Its expected value depends on:

- independence from existing channels
- specialist capability
- task decomposability
- shared-context duplication
- coordination/synthesis cost
- latency saved by parallelism
- model diversity
- tool diversity
- expected error correlation

Recent research supports the hypothesis that diversity/effective channels can matter more than homogeneous agent count. This should be experimentally validated rather than taken as universal.

### Candidate optimisation target

`Effective Information Gain per Agent-Dollar`

not raw agent count.

## 9. Reasoning allocation mechanics

Reasoning effort is now an explicit provider control in some platforms. This suggests a scheduler can potentially allocate more inference-time compute when complexity/risk justifies it.

Potential policy:

- low-risk deterministic transformation -> little/no extra reasoning
- ordinary synthesis -> moderate reasoning
- ambiguous high-impact decision -> high reasoning + verification
- exceptionally difficult task -> escalated reasoning/model + independent checks

The optimiser should learn the marginal quality curve for each task family rather than hard-code one global setting.

## 10. Programmatic versus model-mediated execution

Many agent loops currently spend model calls on operations that could be deterministic.

Examples:
- exact filtering
- schema validation
- counting
- file/path checks
- simple transformations
- deduplication by stable keys
- budget enforcement
- retry backoff

A core runtime principle should be:

**LLM judgment for uncertain semantic decisions; deterministic code for deterministic operations.**

This reduces cost and can improve reproducibility.

## 11. Durable state mechanics

For long-running work, the authoritative state should not be the transcript itself.

A checkpoint should contain sufficient structured information to reconstruct execution:

- objective and success criteria
- current plan
- completed work
- unresolved work
- accepted decisions
- constraints
- evidence pointers
- files/artifacts changed
- test/evaluation state
- budgets consumed/remain
- runtime lineage

This allows clean-session restart without replaying an entire trajectory.

## 12. Runtime-progress mechanics

Long duration is not automatically waste. We need a concept of meaningful progress.

Candidate signals:
- new validated artifact
- state transition
- resolved blocker
- test improvement
- unique evidence gained
- defect removed
- objective subtask completed

Candidate waste signals:
- identical file read repeatedly
- repeated search with no new evidence
- identical failing action
- repeated agent delegation without new information
- high token use with no state change
- oscillation between strategies

A runtime anomaly detector can combine these into a `Useful State Change Rate`.

## 13. Serving-mode economics

Provider APIs increasingly offer different economic/latency modes: standard interactive serving, discounted flex/opportunistic serving, batch processing, prompt caching, and different model tiers.

Therefore task scheduling itself is part of optimisation.

A non-urgent overnight evaluation suite should not necessarily use the same serving path as an interactive user request.

The canonical workload profile should include:
- deadline
- latency sensitivity
- interruptibility
- retry tolerance
- batchability
- confidentiality/data constraints

## 14. Cross-resource interactions

Resources cannot be optimised independently.

Examples:

### Context versus cache
Pruning changes prefixes and may reduce cache reuse.

### Context versus agents
Subagents may each duplicate large context, multiplying input load.

### Tools versus context
More tools increase schemas upfront and may generate more tool results later.

### Model strength versus agent count
A stronger single model may outperform several weaker/correlated agents or vice versa.

### Reasoning versus verification
Higher reasoning effort may reduce the need for a second evaluator on some tasks; on high-risk tasks independent verification may still be mandatory.

### Compaction versus provenance
Aggressive summarisation may save context but lose evidentiary detail unless raw artifacts remain retrievable.

Therefore the optimisation problem is a coupled resource-allocation problem.

## 15. Candidate runtime decision hierarchy

Before execution:
1. classify task/risk
2. determine mandatory instruction/policy set
3. determine required capabilities
4. select initial context/state
5. choose model/reasoning level
6. choose orchestration topology
7. choose verification policy
8. choose serving mode/budget

During execution:
1. observe context growth
2. observe cache economics
3. track unique information gain
4. track useful state change
5. adjust tools/context/agents
6. checkpoint milestones
7. stop/escalate on anomalies

After execution:
1. evaluate task success
2. calculate actual resource profile
3. attribute useful versus wasted compute
4. compare alternative policy if replayable
5. update learned policy only through governed evaluation

## 16. First prototype implication

The first technically meaningful product may not need to control Claude/Codex directly.

A lower-risk v0 could ingest/export telemetry and produce a **Runtime Efficiency Profile**:

- where tokens came from
- instruction load
- tool load
- cache hit/miss economics
- subagent multiplication
- repeated operations
- context growth
- no-progress periods
- model/reasoning allocation
- estimated optimisation opportunities
- quality-safe recommendations

This would let us validate diagnosis before intervention.

The progression could then be:

`Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise`

This staged path reduces risk and creates measurable evidence at every step.

## 17. Durable product thesis after this tranche

The enduring problem is not that one provider has a 150k-token session problem. It is that AI systems lack a universal resource scheduler analogous to what operating systems, databases, cloud FinOps, and compilers provide in their domains.

The opportunity is to create an independent runtime intelligence layer that understands **what the task needs**, **what resources are being consumed**, **what marginal value further computation provides**, and **when to retrieve, cache, compact, delegate, reason, verify, checkpoint, switch, or stop**.

That thesis remains a hypothesis until validated by controlled experiments.
