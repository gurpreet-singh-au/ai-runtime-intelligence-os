# Market Landscape — AI Runtime Intelligence, Observability, Routing & Agent Operations

Date: 2026-08-21
Status: Phase 0 primary-source landscape v0.1

## Purpose

Map the adjacent market using primary vendor documentation and identify the boundary between existing observability/gateway/evaluation products and the proposed AI Runtime Intelligence OS.

This document is not a claim of uniqueness. It is a falsifiable market-positioning analysis that must be updated as products evolve.

## Market categories observed

### 1. AI observability / tracing

Representative products: Langfuse, LangSmith, Braintrust.

Common capabilities observed:
- end-to-end traces of model calls, tools, retrieval and agent steps;
- token, latency and cost recording;
- production monitoring;
- evaluation scores and feedback;
- datasets/experiments;
- dashboards and alerts;
- prompt/version comparison;
- framework/provider integrations.

Interpretation: this category is strong at answering **what happened, where it failed, and how quality/cost changed**.

Potential boundary for this project: move beyond trace inspection toward **resource attribution, counterfactual execution planning, and policy-constrained runtime allocation**.

### 2. AI gateways / model-provider routing

Representative products: Portkey, Helicone, OpenRouter.

Common capabilities observed:
- unified APIs across many models/providers;
- provider routing and failover;
- retries/load balancing/circuit-breaking;
- spend and usage controls;
- observability;
- model/provider selection configuration;
- privacy/data-routing controls in some products;
- semantic/prompt caching in some products.

Portkey has expanded further into Agent Gateway and MCP Gateway functions, including agent registry, access control, budgets, agent/MCP observability, guardrails and policy enforcement.

Interpretation: the gateway category is moving rapidly from transport abstraction into **runtime governance and agent infrastructure**. This is the strongest adjacent competitive pressure to the proposed thesis.

Potential boundary for this project: the proposed differentiator cannot simply be “one gateway for models and agents.” It would need to provide higher-order intelligence such as:
- deciding whether a model/subagent/tool call is needed at all;
- estimating task resource requirements before execution;
- compiling applicable instructions/context dynamically;
- estimating marginal value of additional computation;
- detecting redundant agents and low-value runtime trajectories;
- comparing execution strategies on successful parent outcomes;
- learning cross-provider resource-allocation policies from evaluated outcomes.

### 3. Evaluation-first AI engineering

Representative products: Braintrust, Langfuse, LangSmith.

Common capabilities observed:
- offline and online evals;
- production traces converted into datasets;
- prompt/model experiments;
- LLM-as-judge, code and human scoring;
- quality regression detection;
- alerts/CI gates.

Interpretation: evaluation infrastructure is mature enough that this project should likely **integrate with it rather than rebuild it**. Our runtime optimiser would need an evaluator interface and should be able to consume external scores/traces.

### 4. Agent observability / governance

The market is converging on agent-specific traces, tool/MCP visibility, agent registries, budget/permission controls, and failure analysis.

Portkey's 2026 Agent Gateway is particularly important because it introduces:
- per-agent endpoints;
- access/budget controls;
- agent registry and capabilities;
- traces including MCP activity;
- routing/reliability/guardrails.

LangSmith, Langfuse and Braintrust also trace nested agent/tool execution.

Interpretation: **“agent observability” alone is not an open wedge**. The remaining hypothesis is **agent resource economics and runtime scheduling**: when to spawn, which model to assign, whether parallelism adds unique information, when to checkpoint/terminate, and how much marginal quality is gained.

## Preliminary company notes

### Langfuse

Primary positioning observed:
- open-source LLM/AI observability;
- structured traces across model calls, tools and retrieval;
- token and cost tracking;
- quality scoring;
- dashboards/alerts;
- datasets and experiments;
- OpenTelemetry-based SDKs;
- self-hosting support.

Strength relevant to us:
- rich trace/evaluation data could be an upstream telemetry source.

Current apparent boundary from reviewed materials:
- primarily observation/evaluation/analysis rather than a general autonomous cross-provider resource scheduler.

Research status: **ADJACENT / POSSIBLE INTEGRATION**.

### LangSmith

Primary positioning observed:
- framework/provider-compatible tracing and observability;
- monitoring dashboards and alerts;
- feedback/annotations;
- online evaluations and automations;
- trace analysis, including AI-assisted diagnosis;
- cloud/hybrid/self-hosted options.

Strength relevant to us:
- deep agent trace semantics and evaluation workflows.

Current apparent boundary from reviewed materials:
- focuses on tracing, evaluation, monitoring and failure analysis. Need deeper investigation of any autonomous runtime optimisation features before claiming a gap.

Research status: **ADJACENT / POSSIBLE INTEGRATION / COMPETITIVE WATCH**.

### Braintrust

Primary positioning observed:
- AI observability + evals tightly coupled;
- nested traces for LLM/tool/retrieval/agent steps;
- tokens, latency and cost per trace/span;
- live scoring and alerts;
- production traces -> eval datasets;
- experiment comparison and CI regression testing;
- framework/provider agnosticism.

Strength relevant to us:
- potentially excellent evaluation backend for proving resource-intervention quality.

Current apparent boundary from reviewed materials:
- strongest on testing, tracing, quality discovery and improvement loops; not yet established from reviewed materials as a general runtime resource-allocation scheduler.

Research status: **ADJACENT / POSSIBLE INTEGRATION / COMPETITIVE WATCH**.

### Helicone

Primary positioning observed:
- OpenAI-compatible AI Gateway;
- access to 100+ providers/models;
- intelligent routing and automatic fallbacks;
- unified observability for usage, cost and performance;
- integrations with LangChain, LangGraph, LlamaIndex, Vercel AI SDK and Codex.

Strength relevant to us:
- gateway adapter and telemetry source.

Current apparent boundary from reviewed materials:
- routing/reliability/observability rather than the full task/resource intelligence thesis.

Research status: **ADJACENT / POSSIBLE ADAPTER**.

### OpenRouter

Primary positioning observed:
- unified multi-model/provider access;
- provider selection/routing;
- fallbacks;
- capability/parameter compatibility checks;
- routing controls including data-collection and zero-data-retention constraints.

Strength relevant to us:
- broad model access makes it attractive for early model-routing experiments.

Current apparent boundary:
- execution/routing substrate rather than canonical task intelligence, outcome learning, instruction/context allocation or agent spawn governance.

Research status: **POSSIBLE ADAPTER / BENCHMARK**.

### Portkey

Primary positioning observed:
- AI Gateway with multi-provider routing, reliability, budgets, observability and guardrails;
- dynamic per-request routing based on metadata, budgets, performance and policy;
- Agent Gateway with agent registry, access control, budgets, traces and reliability;
- MCP Gateway with tool/server governance, policy enforcement and end-to-end tracing;
- enterprise controls around Claude Code and other workloads.

Why this matters:
Portkey is the closest reviewed adjacent platform to a runtime control plane. It means our thesis must be narrower and technically stronger than “central governance/routing/observability for agents.”

Key remaining differentiation hypotheses to validate:
1. resource planning before execution rather than rule-based request routing only;
2. dynamic context and instruction compilation;
3. subagent spawn/no-spawn economics and model assignment;
4. useful-state-change / semantic-loop detection;
5. marginal compute utility across context, reasoning, tools, agents and verification;
6. outcome-conditioned learning of execution strategies;
7. replay/counterfactual analysis showing which resources were unnecessary;
8. provider/framework/gateway independence above existing gateways.

Research status: **CLOSEST COMPETITIVE WATCH / POTENTIAL INTEGRATION AND COMPETITOR**.

## Emerging market structure

A useful current model is:

```text
APPLICATION / AGENT
       |
       v
ORCHESTRATION / AGENT FRAMEWORK
       |
       v
GATEWAY / ROUTING / POLICY
       |
       v
MODEL / TOOL PROVIDERS

Cross-cutting today:
OBSERVABILITY + EVALS + COST + SECURITY
```

The proposed product would need to justify an additional intelligence layer:

```text
DESIRED OUTCOME
       |
       v
RUNTIME RESOURCE INTELLIGENCE
(task profile, context, instructions, tools, model, agents,
reasoning, budget, verification, stopping policy)
       |
       v
EXISTING GATEWAYS / RUNTIMES / PROVIDERS
       |
       v
TELEMETRY + EVALUATION
       |
       +----------------------+
                              |
                         LEARNING LOOP
```

## Provisional opportunity boundary

The most defensible current hypothesis is **not**:

- another trace dashboard;
- another model gateway;
- another agent registry;
- another eval platform;
- another memory summariser;
- another cost monitor.

The hypothesis is:

> A provider-independent intelligence layer can use telemetry + evaluations to determine the minimum sufficient, policy-compliant execution strategy for a task and continuously improve that allocation across context, instructions, models, tools, agents, runtime and verification.

This remains unproven.

## Market risk assessment

### High risk
- Gateways such as Portkey are expanding upward into agent governance and increasingly intelligent routing.
- Observability/eval companies can add recommendation/automation layers because they already possess trace data.
- Model providers can absorb context, memory, routing and agent optimisation features natively.

### Potential defence
A durable product would need to own or accumulate:
- cross-provider/task-specific outcome datasets;
- canonical resource and capability models;
- execution-strategy evaluations;
- model/tool/agent performance history;
- task fingerprint -> execution strategy mappings;
- policy/governance abstractions independent of vendors;
- intervention/replay algorithms validated across runtimes.

## Next research

1. Deep feature-by-feature Portkey comparison.
2. Investigate AgentOps and other dedicated agent-runtime products.
3. Investigate model routers such as RouteLLM and related open-source work.
4. Investigate context/memory platforms separately.
5. Investigate AI FinOps / cost optimisation products.
6. Search academic literature for adaptive inference/resource allocation and agent scaling.
7. Validate whether any competitor already performs task-level multi-resource optimisation rather than gateway routing.

## Source note

This v0.1 landscape is based primarily on current vendor documentation reviewed on 2026-08-21. Claims should be rechecked before architectural or commercial commitments because this market changes rapidly.
