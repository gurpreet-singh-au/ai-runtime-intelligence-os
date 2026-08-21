# Project Non-Negotiables — AI Runtime Intelligence OS

Date established: 2026-08-21
Status: Binding project constraints unless changed through an explicit recorded decision

## 1. GitHub is the project source of truth

- Important requirements, architecture, research findings, decisions, experiments, evidence, state, tests, risks, and handoff information must be recorded in the repository.
- Chat history and model memory are not authoritative project state.
- Repository state overrides conversational recollection where they differ.
- Claims of implementation, validation, testing, deployment, or research completion require evidence.

## 2. Research before production implementation

- This project begins with deep technical, economic, competitive, and experimental research.
- Do not begin production implementation merely because the opportunity appears compelling.
- Architecture, security, evaluation, operating model, risk boundaries, and build-readiness criteria must be explicit before production build approval.
- Prototype-first workflow applies. A prototype validates concepts/UX/telemetry; it is not production approval.

## 3. Model-, provider-, framework-, and gateway-agnostic architecture

- Core architecture must not depend on Claude, OpenAI, Gemini, OpenRouter, LangGraph, CrewAI, MCP, ACP, or any single provider/framework/gateway.
- Providers, frameworks, gateways, orchestration systems, and protocols must sit behind replaceable adapters/interfaces where practical.
- OpenRouter may be useful as a routing/gateway adapter, but must not own canonical routing intelligence or project state.
- Direct provider APIs and self-hosted/open-weight execution must remain architecturally possible.

## 4. Capability-driven, not vendor-driven

- Define required capabilities before selecting implementations.
- Model selection must be based on measured task capability, quality, reliability, risk, latency, privacy, availability, and economics—not brand or popularity.
- "Free" is a dynamic price state, not a capability class.
- Never route sensitive/high-consequence work to a model merely because it is cheaper or free.

## 5. Open-source / open-weight optimisation without lock-in

- Strong open-source/open-weight components should be actively evaluated where technically, commercially, legally, securely, and operationally suitable.
- Do not adopt an open component merely because it is open or popular.
- Every important dependency requires an exit/replacement strategy, portable data/interface assumptions, and awareness of deprecation/maintenance risk.
- Preferred pattern: **we own the interface; external implementations plug into it**.

## 6. Canonical-state ownership

- The Runtime OS must own its canonical runtime policy, task/resource profiles, evidence, evaluations, cost records, routing decisions, approvals, and audit history.
- External providers/gateways may execute work but should not become the sole authoritative store for these objects.
- GitHub is the canonical engineering/research record, not the live transactional/runtime datastore.

## 7. Deterministic authority where possible

- Deterministic software should enforce rules that must not depend on probabilistic model judgment, including where applicable:
  - permissions and least privilege
  - mandatory policy inclusion
  - budget ceilings
  - maximum recursion/agent counts
  - stop conditions
  - secret/privacy boundaries
  - provenance/versioning
  - schema validation
  - audit logging
  - approval/escalation requirements
- Use LLM inference for uncertain semantic judgment, not for mechanical work that deterministic computation can safely perform.

## 8. Self-improving, not uncontrolled self-mutating

- The system may learn from evaluated outcomes and propose or select better execution policies within approved bounds.
- It must not silently rewrite authoritative policies, safety controls, architecture, schemas, routing qualification standards, or governance boundaries.
- Material changes require governed evaluation and explicit approval according to risk.

## 9. Quality and safety outrank token minimisation

- The objective is **AI runtime efficiency**, not minimum tokens or minimum spend.
- Do not remove context, instructions, agents, verification, or model capability merely to reduce cost when outcome quality, safety, reliability, or compliance would materially degrade.
- Sometimes the efficient decision is to spend more compute.
- Optimisation should be assessed using cost per successful outcome / risk-adjusted cost per successful outcome rather than raw token savings alone.

## 10. Mandatory constraints may not be optimised away

- Safety, security, privacy, authorisation, governance, explicit user constraints, and legally/commercially mandatory rules must remain effective.
- Instruction Intelligence may classify, deduplicate, scope, and compile rules, but must preserve semantics, authority, provenance, and applicable mandatory constraints.
- Any instruction-pruning mechanism must be evaluated for hidden compliance regressions.

## 11. Evidence-first and provenance-preserving

- Research claims and architectural decisions should trace to evidence and source quality.
- Distinguish provider documentation, peer-reviewed literature, preprints, benchmarks, community observations, and our own experiments.
- Do not treat benchmark claims as universal truths without reproduction/validation on representative workloads.
- Preserve raw evidence outside hot context where possible, with retrievable pointers and provenance.

## 12. Temporal and versioned reasoning

- Models, prices, free tiers, provider policies, APIs, benchmarks, tool capabilities, and routing availability change rapidly.
- Runtime decisions and research findings must be date/version-aware where materially relevant.
- Preserve enough version/provenance information to reconstruct why a past routing or optimisation decision was made.

## 13. Privacy-by-design and least privilege

- Apply data minimisation, purpose limitation, least privilege, tenant isolation where applicable, encryption, retention/deletion controls, scoped credentials, and auditable access.
- Provider data handling, retention/training terms, geography, and confidentiality requirements are part of routing eligibility.
- Do not route data to a provider/model solely on cost grounds if privacy/security policy does not permit it.

## 14. Human accountability / explicit escalation for high-risk decisions

- High-risk, uncertain, conflicting, legally consequential, security-sensitive, privacy-sensitive, or materially irreversible actions require appropriate approval/escalation boundaries.
- The Runtime OS should reduce unnecessary human involvement in routine optimisation, but must not erase accountable control where consequences justify it.

## 15. Graceful degradation and resilience

- Provider/model/tool/gateway failures must not collapse the architecture.
- Define fallbacks, degraded modes, timeout behaviour, retry policy, circuit breaking, and replacement routes where relevant.
- Avoid uncontrolled retry/agent loops; runtime persistence is not a substitute for progress.

## 16. Agent/subagent efficiency is a first-class problem

- Do not assume more agents means better outcomes.
- Before spawning a subagent, consider whether:
  - a model call is required at all;
  - a separate agent is required;
  - the work is decomposable/independent;
  - a cheaper/smaller qualified model is sufficient;
  - deterministic software can perform the task;
  - another agent is likely to add unique information rather than correlated duplication.
- Measure marginal quality/information gain and coordination cost.

## 17. Context, instructions, tools, and memory are separate runtime resources

- Do not treat all available information as one undifferentiated prompt.
- Separate and optimise:
  - information/context
  - instructions/policies
  - tool/capability surface
  - tool results/evidence
  - durable memory/state
  - model reasoning/inference
  - agents/subagents
  - runtime/time
  - verification
- Cache efficiency is not the same as cognitive/context efficiency.

## 18. Canonical abstractions must survive AI evolution

The durable core should be based on concepts such as:
- desired outcome
- task characteristics
- capability requirements
- risk/quality thresholds
- information relevance
- instruction applicability
- resource budgets
- execution state
- evidence/provenance
- evaluation results
- cost/latency/outcome

Provider-specific controls are adapters and may change without redefining these canonical concepts.

## 19. Observability before autonomous intervention

Adopt a staged control progression:

`Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise`

- Initial versions should prove telemetry, attribution, recommendations, replay/A-B evaluation, and quality preservation before broad autonomous intervention.
- Automatic context deletion, agent termination, model switching, or policy compilation should expand only after evidence supports safety and reliability.

## 20. Formal evaluation and Build Readiness

Before production build or material autonomous control, explicitly address:
- routing qualification and benchmarking
- evaluator/reviewer independence where required
- open-weight/direct-provider fallback
- privacy/security/threat model
- sandboxing and permissions
- provenance/audit model
- failure and recovery semantics
- FinOps/budget controls
- quality regression testing
- acceptance criteria
- deployment/resilience/observability
- governance and approval boundaries

Unresolved material blockers must not be silently bypassed.

## 21. Agent/developer independence and continuity

- Project state must be sufficiently documented that ChatGPT, Claude, Codex, Kimi, or another capable agent/developer can continue without relying on hidden conversational memory.
- Prompts and workflows should be agent-agnostic where practical.
- Tests, architecture, decision records, and handoff state are part of portability.

## 22. Commercial thesis remains falsifiable

- Do not assume a commercial product exists merely because the technical problem is real.
- Continuously test whether the unsolved, defensible value remains after provider-native features, open-source developments, and competitors are considered.
- The project must be willing to narrow, pivot, defer, or stop if evidence does not support a durable opportunity.

## 23. Current project objective

Investigate and, if evidence supports it, build a universal AI Runtime Intelligence OS that can determine the smallest/safest/most reliable and economically efficient combination of context, instructions, memory, models, reasoning, agents, tools, runtime, and verification needed to achieve a defined outcome under quality, risk, privacy, and governance constraints.

These non-negotiables override convenience and implementation enthusiasm. Any proposed change to them should be explicit, justified, and recorded in `DECISIONS.md` or a future governed-change mechanism.
