# Deep Research Tranche 01 — Runtime Efficiency Foundations

Date: 2026-08-21
Status: Research baseline

## Executive finding

The opportunity is broader than token reduction. Current model providers and research communities are independently converging on the same underlying problem: long-running AI systems need active management of context, instructions, memory, tools, reasoning effort, agents, and durable state.

The durable opportunity is therefore best framed as **AI runtime resource allocation and governance** rather than context compression alone.

## 1. Context is an active computational resource

Modern agent context includes system instructions, user instructions, message history, tool schemas, tool results, retrieved data, code, memory, and intermediate state. Provider engineering guidance increasingly treats context curation as an iterative runtime activity rather than a one-time prompt-design exercise.

### Implication

The runtime should explicitly represent context components and their utility rather than concatenating everything into one append-only stream.

Candidate telemetry:
- total input tokens
- cached / uncached tokens
- instruction tokens
- tool-schema tokens
- retrieved evidence tokens
- raw tool-result tokens
- dialogue/history tokens
- current-task tokens
- estimated duplication
- estimated staleness
- estimated task relevance

## 2. Large context capacity does not eliminate context management

Research such as *Lost in the Middle* established that models can use information unevenly depending on its position in long contexts. Newer 2026 work continues to identify context explosion, semantic drift, distraction, and degraded long-horizon reasoning as practical problems.

### Implication

Our architecture must not assume that larger context windows solve the problem. It should optimise **useful context**, not simply fit within a limit.

## 3. Prompt caching is useful but solves only part of the problem

OpenAI, Anthropic, and Google all provide forms of prompt/context caching. Caching can lower the cost and latency of repeated prefixes. However, cached irrelevant information can still be cognitively unnecessary, may compete with relevant information, and may complicate instruction/tool selection.

### Principle

**Cache efficiency is not the same as context efficiency.**

The system should optimise both:
- economic reuse of stable prefixes; and
- semantic relevance of what is actually supplied.

## 4. Instructions are a first-class runtime resource

Current provider guidance explicitly recommends leaner prompts, avoiding repeated instructions, and exposing only relevant tools. OpenAI's current model guidance reports internal coding-agent evals where leaner system prompts improved scores while materially reducing tokens and cost; those figures are directional and workload-specific, but they are strong evidence that more instruction text can be both more expensive and less effective.

### Proposed subsystem: Instruction Intelligence Engine

Responsibilities:
- parse instructions into structured rules
- attach authority, scope, priority, provenance, effective dates, and conditions
- identify semantic duplicates
- detect conflicts
- resolve applicability to a task
- preserve mandatory rules
- compile a minimum-sufficient effective instruction set
- measure whether removing or consolidating instructions changes task success

This must be **semantic-preserving and governance-aware**, not simple summarisation.

## 5. Tool definitions and tool results create substantial context pressure

Anthropic has publicly described cases where tool definitions/results can consume tens of thousands of tokens before useful work begins. Both Anthropic and OpenAI have introduced tool-search/on-demand loading mechanisms so agents do not need every tool definition upfront.

### Implication

Tool exposure should become dynamic:

`Task -> capability requirements -> permission filter -> discover relevant tools -> expose minimal tool surface`

Raw tool results should also be separated from working state. A long terminal log should be stored as retrievable evidence while the active context contains a structured result plus a pointer to the original.

## 6. Long-running execution should externalise state

Anthropic's 2026 Managed Agents architecture explicitly separates durable session context from the model's immediate context window. This is a strong architectural signal: recoverable state should live outside transient inference context and be selectively interrogated/transformed when needed.

### Proposed memory/state tiers

- **Hot:** current objective, immediate evidence, active errors
- **Warm:** current plan, unresolved decisions, recent checkpoints
- **Cool:** project state, stable decisions, domain knowledge
- **Cold:** full historical traces, old tool outputs, superseded attempts
- **Evidence archive:** immutable/retrievable originals with provenance

## 7. Multi-agent scaling has diminishing returns

Recent 2026 research reports that homogeneous agent scaling can saturate rapidly and that diversity can matter more than raw agent count. One study reports that two diverse agents can match or exceed sixteen homogeneous agents on its evaluated settings. Other research finds non-monotonic scaling: larger teams do not always yield better long-term performance, particularly when memory and coordination are weak.

### Proposed subsystem: Agent/Subagent Scheduler

Before spawning another agent, estimate:
- task decomposability
- independence of workstream
- expected information gain
- correlation with existing agents
- coordination overhead
- model/tool diversity value
- latency benefit from parallelism
- marginal cost
- expected quality gain

The goal is not minimum agents; it is **optimal effective channels of computation**.

## 8. Reasoning effort is becoming an explicit allocation variable

Modern APIs expose reasoning effort / quality-latency trade-offs. This creates a runtime control surface that an independent layer can optimise.

### Proposed decision

Reasoning should be assigned according to:
- task complexity
- ambiguity
- risk
- verification needs
- observed marginal quality improvement

Simple deterministic operations should not automatically receive frontier reasoning budgets.

## 9. Programmatic orchestration can replace unnecessary inference turns

Provider platforms are beginning to support programmatic tool calling or code-based orchestration so loops, filtering, transformations, and bounded workflows do not require a fresh full model judgment between every mechanical operation.

### Architectural principle

**Use deterministic computation for deterministic work; reserve model inference for judgment.**

Candidate examples:
- filtering tool results
- checking file existence
- parsing structured output
- deduplicating exact records
- enforcing budgets
- validating schemas
- counting/reconciling state

## 10. Memory management is becoming a learned policy problem

2026 research such as Agentic Memory, Context as a Tool, MemoBrain, COMPASS, and related work treats memory/context maintenance as an active agent capability rather than a passive append-only store. Results generally support proactive pruning, summarisation, retrieval, and state organisation under bounded context budgets.

### Opportunity boundary

We should not attempt to win by inventing one more summariser. The higher-value layer is to coordinate:

`context + instructions + memory + tools + model + reasoning + agents + runtime + verification`

under a common outcome/economics policy.

## 11. Proposed optimisation objective

Do **not** minimise tokens in isolation.

A conceptual objective:

`max E[Utility] = OutcomeQuality + Reliability + Safety + Timeliness - ComputeCost - Latency - OperationalRisk`

subject to hard policy, permission, privacy, safety, and quality constraints.

Operational metrics should include:
- cost per successful outcome
- risk-adjusted cost per successful outcome
- useful state change per unit compute
- marginal quality gain per additional compute
- context utility density
- tool utility rate
- effective-agent contribution
- retry/loop waste
- cache economics

## 12. Emerging architecture thesis

The product should be a provider-agnostic **runtime control plane** with adapters to model/provider/framework capabilities.

Core policy remains independent; adapters translate policy into provider controls.

Candidate engines:
1. Task Intelligence
2. Context Intelligence
3. Instruction Intelligence
4. State/Memory Intelligence
5. Tool Capability Router
6. Model & Reasoning Router
7. Agent/Subagent Scheduler
8. Cache Strategy Engine
9. Runtime Anomaly/Loop Detector
10. Outcome & Economics Engine
11. Policy/Governance Engine
12. Evaluation & Learning Engine

## 13. What is likely to remain durable as providers evolve

Provider-specific controls will change quickly. The following abstractions appear more durable:
- desired outcome
- task characteristics
- required capabilities
- information relevance
- instruction applicability
- resource budgets
- execution state
- evidence/provenance
- quality evaluation
- economic outcome
- risk constraints

These should form the canonical core model.

## 14. Major unresolved questions

1. Can task relevance be estimated reliably enough to prune context without hidden regressions?
2. Can instruction applicability be compiled deterministically for a meaningful share of workloads?
3. Which provider/framework hooks allow external intervention during a live agent run?
4. Can we measure useful state change generically across coding, research, support, and enterprise workflows?
5. What is the minimum telemetry required to make good allocation decisions?
6. How much overhead does the control plane itself introduce?
7. Which runtime decisions should be predictive/learned versus deterministic?
8. Which first wedge exposes enough telemetry and cost pain to prove ROI quickly?
9. What parts are likely to be absorbed by model providers versus remain valuable cross-provider infrastructure?
10. Can the system prove quality preservation, not merely cost reduction?

## Provisional conclusion

There is strong evidence that runtime inefficiency is a real and growing systems problem. There is also clear provider movement toward native context, caching, tool-search, reasoning, and state-management controls. This does **not** eliminate the opportunity; it changes the opportunity from building low-level features to building the cross-provider intelligence that decides when and how those features should be used.

The next phase should be empirical: instrument representative agent tasks, establish baselines, and test isolated interventions before committing to a product implementation.
