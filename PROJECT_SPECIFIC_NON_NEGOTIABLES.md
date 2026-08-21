# Project-Specific Non-Negotiables — AI Runtime Intelligence OS

Date established: 2026-08-21
Status: Project-specific governing constraints

These rules supplement, and do not replace, the universal framework in `gurpreet-singh-au/ai-project-framework` pinned in `PROJECT_STANDARD_ADOPTION.md`.

## 1. Optimise runtime efficiency, not raw token count

The system must optimise for successful outcomes under quality, reliability, safety, privacy, latency and economic constraints. Token reduction alone is not a success criterion.

## 2. Runtime resources are separate canonical concepts

The architecture must model separately, where material:

- information/context;
- instructions/policies;
- persistent memory/state;
- model inference and reasoning effort;
- prompt/context cache;
- tools/capability surface;
- tool execution/results;
- agents/subagents;
- runtime/time;
- verification/assurance;
- infrastructure/serving resources;
- outcome/economics.

Do not collapse these into one generic "prompt cost" metric.

## 3. Instruction Intelligence must preserve authority and semantics

Instruction optimisation may classify, scope, deduplicate, resolve conflicts, conditionally activate and compile instructions, but it must preserve:

- mandatory constraints;
- authority hierarchy;
- scope;
- provenance;
- effective version/date where relevant;
- explicit user constraints;
- safety/security/privacy requirements.

Instruction pruning is not permitted merely because a rule appears rarely used.

## 4. Subagent creation is an economic and governance decision

Do not assume more agents means better outcomes.

Before spawning a subagent, the runtime should eventually evaluate:

1. whether an LLM call is needed at all;
2. whether a separate agent is needed;
3. task decomposability and independence;
4. expected unique information/quality gain;
5. coordination overhead;
6. qualified cheaper/smaller model availability;
7. deterministic substitution;
8. budget, latency and risk constraints;
9. stop/termination conditions.

## 5. Model routing is capability- and evidence-driven

OpenRouter or similar gateways may be used as adapters, but routing policy belongs to this system.

"Free" is a dynamic price state, not a model class. Free/cheap models may only be used when task-specific evaluation, privacy/security policy and risk thresholds permit them.

## 6. Cache efficiency is not context efficiency

A cached prefix may be cheaper to process but may still be irrelevant, stale, contradictory, privacy-inappropriate, or cognitively distracting. The system must distinguish economic reuse from semantic usefulness.

## 7. Raw evidence should be externalised from hot context

Large tool outputs, historical transcripts, logs and evidence should be stored retrievably with provenance. Active context should carry the minimum sufficient structured representation and pointers needed to recover originals.

## 8. Useful state change is a first-class runtime signal

Long-running execution should be assessed by meaningful progress, not elapsed time or activity alone. Repeated tool calls, duplicate reads, no-progress intervals, recursive delegation and retry loops should be observable and eventually governable.

## 9. Marginal Compute Utility is a core research hypothesis

For optional additional context, reasoning, agents, tools, retries or verification, the system should investigate whether expected incremental outcome value justifies incremental resource cost/risk.

This is a research hypothesis to validate empirically, not yet a production formula.

## 10. Provider-native features are implementation mechanisms, not the moat

Prompt caching, context editing, compaction, tool search, reasoning controls, memory APIs, provider routing and similar native features should be used where valuable. The product opportunity is the cross-provider intelligence that decides when and how to use them.

## 11. First control mode is observational/advisory

The maturity path is:

`Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise`

Do not begin with broad autonomous deletion of context, termination of agents, model switching, or policy rewriting before comparative evidence demonstrates safety and quality preservation.

## 12. The first wedge may be coding agents, but the core must remain workload-agnostic

Coding agents are a strong laboratory because telemetry, long contexts, subagents, tools and measurable outcomes are available. However, do not bake coding-specific assumptions into the canonical runtime model unless they are clearly adapter/domain-specific.

## 13. Commercial thesis remains open

The technical problem may be real without supporting a durable standalone business. Research must continuously test:

- customer pain and spend;
- provider-native substitution risk;
- competitor coverage;
- integration feasibility;
- willingness to pay;
- defensibility;
- measurable ROI.

## 14. No material architecture decision without current evidence

Because model APIs, pricing, context limits, routing products, open-source projects and agent frameworks change rapidly, any material selection must be rechecked at decision time.

## 15. Project objective

Investigate and, if evidence supports it, build a universal runtime intelligence/control plane that determines the minimum sufficient and risk-appropriate combination of context, instructions, memory, models, reasoning, tools, agents, runtime and verification needed to achieve a defined outcome reliably and economically.
