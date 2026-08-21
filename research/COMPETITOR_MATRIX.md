# Competitor / Adjacent Capability Matrix

Date: 2026-08-21
Status: Phase 0 research v0.1
Evidence policy: primary vendor documentation where possible; unknowns remain explicitly unknown.

## Purpose

Identify where existing products already observe, evaluate, route, control, optimise, and learn across AI execution, so the project does not build a duplicate observability/gateway product or make unsupported uniqueness claims.

## Capability legend

- **Y** — clearly documented current capability
- **P** — partial / adjacent capability
- **U** — not established from reviewed primary sources
- **N/A** — not the product's apparent purpose

## Matrix

| Product | Trace / Observe | Evals | Cost / Token Analytics | Model / Provider Routing | Fallback / Reliability | Agent / Tool Trace | Access / Budget Governance | Context / Instruction Optimisation | Spawn / No-Spawn Agent Decision | Task-Level Multi-Resource Planning | Outcome-Conditioned Runtime Learning | Likely Role for Us |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Langfuse | Y | Y | Y | U | U | Y | U | U | U | U | P | telemetry/eval integration candidate |
| LangSmith | Y | Y | Y | U | U | Y | P | U | U | U | P | telemetry/eval integration + watch |
| Braintrust | Y | Y | Y | U | U | Y | P | P | U | U | P | evaluation/trace backend candidate + watch |
| Helicone | Y | P | Y | Y | Y | P | P | U | U | U | U | gateway/telemetry adapter candidate |
| OpenRouter | P | U | Y | Y | Y | P | P | P via caching/routing | U | U | U | model/provider gateway adapter candidate |
| Portkey | Y | P | Y | Y | Y | Y | Y | P | U | P | P | closest competitive watch; potential lower-layer integration |
| AgentOps | Y | P | Y | U | U | Y | P | U | U | U | U | agent observability candidate/watch |
| RouteLLM | U | benchmark-oriented | P | Y | P | U | U | U | U | P for model routing | P | open-source routing research candidate |

## Important caveat

`U` does **not** mean a product definitely lacks a capability. It means the capability was not established to an acceptable level from the current primary-source research pass. Before any commercial claim, each material `U` must be rechecked.

## Product notes

### Langfuse

Current primary-source documentation establishes:
- structured application traces;
- observations for model generations, tools, agents, retrievers and evaluators;
- prompt/response, token, latency and cost tracking;
- production monitoring, dashboards and alerts;
- offline and online evaluation;
- datasets and experiments;
- OpenTelemetry-based instrumentation and self-hosting.

Implication: do not rebuild generic tracing/evaluation. A Runtime Intelligence layer should be able to consume Langfuse/OTel telemetry.

### LangSmith

Current positioning remains strongly centred on tracing, monitoring, evaluation and agent debugging. It should be treated as both an integration candidate and a competitive watch because LangChain can move upward into automated optimisation.

Research gap: complete current feature audit of any automated remediation, prompt optimisation, model-routing or runtime-control capabilities.

### Braintrust

Current primary-source material establishes:
- production traces for LLM calls, tools and retrieval;
- token, cost, latency and cache visibility;
- online scoring, alerts and quality gates;
- trace-to-dataset conversion;
- model/prompt experiment comparison;
- automatic pattern discovery (`Topics`);
- `Loop` assistance for improving prompts, scorers and datasets.

Implication: Braintrust is moving beyond passive observability toward active improvement. Our differentiation cannot simply be “learn from traces.” It must be specifically about execution-resource allocation across context, instructions, agents, models, tools, time and verification.

### OpenRouter

Current primary documentation establishes:
- unified model/provider access;
- price-, latency- and throughput-based provider routing;
- provider ordering/allowlists/ignore lists;
- provider and model fallbacks;
- parameter/capability compatibility filtering;
- Zero Data Retention/data-collection routing constraints;
- prompt-caching-aware sticky routing;
- BYOK support.

Implication: provider-level economic routing is already mature. The proposed Runtime OS should normally decide **which qualified model/capability strategy** is appropriate, then delegate provider-level routing to a gateway such as OpenRouter when useful.

### Portkey

Portkey is the most material adjacent competitor found so far.

Current primary-source material establishes:
- multi-provider AI Gateway;
- retries, fallbacks, load balancing and timeouts;
- budgets and rate limits;
- guardrails;
- full traces of model/tool activity;
- MCP Gateway governance;
- Agent Gateway with per-agent endpoints, access control, budgets, registry, capabilities and agent/MCP traces.

Implication: “universal agent gateway” is not an adequate wedge. A defensible Runtime Intelligence OS must demonstrate intelligence that sits above or across gateway mechanisms.

## The boundary we must prove

The project should test whether the following capabilities remain materially unsolved:

1. **Task Resource Profiling** — predict required context, instructions, model capability, tools, agents, runtime and verification before execution.
2. **Instruction Applicability Compilation** — load only applicable rules while deterministically preserving mandatory constraints.
3. **Context Utility Allocation** — identify relevant/stale/duplicate context and hot/warm/cold placement.
4. **Agent Spawn Economics** — decide whether a separate subagent has positive expected marginal value before spawning it.
5. **Cross-Resource Marginal Compute Utility** — compare the expected value of another model call, stronger model, additional retrieval, agent, tool call or verifier.
6. **Useful State Change / Loop Intelligence** — distinguish meaningful progress from repeated semantic work.
7. **Execution Counterfactuals** — estimate which consumed resources materially contributed to the final successful outcome.
8. **Outcome-Conditioned Policy Learning** — learn task fingerprint -> successful execution strategy mappings across providers/runtimes.

## Build / reuse / integrate consequence

Under the central project framework:

- **Do not build** generic trace ingestion dashboards if OTel/Langfuse/Braintrust/LangSmith can provide it.
- **Do not build** commodity provider fallback/load balancing if OpenRouter/Portkey/direct provider mechanisms can provide it.
- **Do not build** another agent registry merely to compete with Portkey.
- **Do build or own** canonical task/resource profiles, policy abstractions, evaluation-normalised execution outcomes, intervention logic, and cross-provider learned resource-allocation intelligence if experiments validate them.

## Current competitive conclusion

The market already contains strong components for observability, evaluation, routing, governance and reliability. That reduces the amount of plumbing the project may need to build, but increases the proof burden for the claimed intelligence layer.

The commercial thesis remains viable only if experiments show that cross-resource runtime planning/intervention creates material additional value beyond current gateways and observability/evaluation platforms.

## Next checks

- Complete exact current LangSmith feature audit.
- Complete AgentOps feature audit.
- Inspect RouteLLM and successor/open-source routers technically and legally.
- Map memory/context products separately.
- Map AI FinOps products separately.
- Re-run this matrix before prototype architecture is approved.
