# Research Source Register

Date started: 2026-08-21
Status: Living evidence register

This file records primary and research sources used to validate the AI Runtime Intelligence OS thesis. Claims should distinguish provider documentation, peer-reviewed research, preprints, and project hypotheses.

## Provider / primary sources

### Anthropic — Effective context engineering for AI agents
URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
Type: Provider engineering guidance
Published: 2025-09-29
Key evidence:
- Treats context as a finite resource with diminishing marginal returns.
- Defines context engineering as curating the full inference state, not only system prompts.
- Recommends the smallest high-signal context sufficient for the desired behaviour.
- Describes just-in-time retrieval, compaction, structured note-taking, and multi-agent techniques for long-horizon work.
Project relevance: Strong support for context utility, progressive disclosure, and long-running-session management.

### Anthropic — Manage tool context
URL: https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context
Type: Provider documentation
Observed: 2026-08-21
Key evidence:
- Tool definitions and accumulated tool results consume context.
- Recommends tool search for large toolsets, programmatic tool calling for tool chains, prompt caching for repeated definitions, and context editing for stale results.
- Explicitly frames old tool results as possible dead weight in long-running loops.
Project relevance: Strong support for dynamic tool exposure, deterministic/programmatic orchestration, and tool-result externalisation.

### Anthropic — Context editing
URL: https://platform.claude.com/docs/en/build-with-claude/context-editing
Type: Provider documentation
Observed: 2026-08-21
Key evidence:
- Server-side compaction is a primary strategy for long-running conversations.
- Fine-grained clearing can remove old tool results or prior thinking blocks.
- Clearing context can invalidate prompt-cache prefixes, exposing a real optimisation trade-off between context reduction and cache economics.
Project relevance: Important proof that runtime optimisation is multi-objective; reducing tokens can carry cache costs.

### Anthropic — Context windows
URL: https://platform.claude.com/docs/en/build-with-claude/context-windows
Type: Provider documentation
Observed: 2026-08-21
Key evidence:
- Cached prompt prefixes still occupy context even when their billing treatment changes.
- Multi-session agents should use state artifacts that allow rapid context recovery.
Project relevance: Supports the distinction between economic cache efficiency and semantic/context efficiency, plus externalised durable state.

### OpenAI — Model guidance
URL: https://developers.openai.com/api/docs/guides/latest-model
Type: Provider documentation
Observed: 2026-08-21
Key evidence:
- Exposes explicit reasoning-effort controls.
- Supports explicit and implicit prompt caching.
- Introduces programmatic tool calling for bounded tool-heavy workflows not requiring fresh model judgment at every step.
- Supports multi-agent orchestration for workstreams that divide cleanly.
- Recommends benchmarking task success, evidence completeness, total tokens, latency, and cost rather than assuming fewer calls are automatically better.
Project relevance: Strong support for model/reasoning allocation, programmatic substitution, quality-aware optimisation, and agent scheduling.

### OpenAI — GPT-5.6 Sol model
URL: https://developers.openai.com/api/docs/models/gpt-5.6-sol
Type: Provider documentation
Observed: 2026-08-21
Key evidence:
- 1.05M context window demonstrates that very large context capacity is becoming normal.
- Cached input is materially cheaper than uncached input.
- Prompts above a high-input threshold have different pricing, showing that context length remains economically relevant even with million-token windows.
Project relevance: Supports future-proofing around resource allocation rather than fixed context-window limits.

### Google — Gemini context caching
URL: https://ai.google.dev/gemini-api/docs/caching
Type: Provider documentation
Observed: 2026-08-21
Key evidence:
- Gemini provides implicit caching by default for newer model families.
- Reports cached-token usage telemetry.
- Large common prompt prefixes can benefit from reuse.
Project relevance: Supports provider-agnostic cache telemetry and cache-strategy adapters.

### Google — Gemini API optimisation and inference
URL: https://ai.google.dev/gemini-api/docs/optimization
Type: Provider documentation
Observed: 2026-08-21
Key evidence:
- Serving mode itself can be an economic decision: standard, flex, batch, caching.
- Different runtime criticality/latency requirements justify different inference economics.
Project relevance: Expands the resource model beyond tokens/models into serving mode, urgency, and workload criticality.

## Academic / research sources

### Liu et al. — Lost in the Middle: How Language Models Use Long Contexts
URL: https://aclanthology.org/2024.tacl-1.9/
Type: Peer-reviewed TACL paper
Key evidence:
- Long-context performance depends materially on where relevant information appears.
- More retrieved documents produced only marginal gains in evaluated multi-document QA settings.
Project relevance: Foundational evidence that context capacity does not imply uniform context utilisation and that distractors/relevance matter.

### Yang et al. — Understanding Agent Scaling in LLM-Based Multi-Agent Systems via Diversity
URL: https://arxiv.org/abs/2602.03794
Type: 2026 preprint
Key evidence:
- Reports strong diminishing returns for homogeneous agent scaling.
- Attributes gains to effective independent information channels rather than raw agent count.
- Reports that two diverse agents can match or exceed sixteen homogeneous agents in evaluated settings.
Project relevance: Supports marginal-agent utility, diversity-aware orchestration, and subagent budgeting.
Caution: Preprint; findings should be independently reproduced before product policy depends on them.

### Yu — AdaptOrch: Task-Adaptive Multi-Agent Orchestration
URL: https://arxiv.org/abs/2602.16873
Type: 2026 preprint
Key evidence:
- Treats orchestration topology as a first-class optimisation target.
- Evaluates task-adaptive routing among parallel, sequential, hierarchical, and hybrid patterns.
Project relevance: Supports topology selection rather than static agent architecture.
Caution: Preprint; validate independently.

### Chen et al. — Diversity Collapse in Multi-Agent LLM Systems
URL: https://arxiv.org/abs/2604.18005
Type: 2026 preprint
Key evidence:
- Reports diminishing returns from group-size scaling and risks of convergence under dense communication.
Project relevance: Supports preserving independent channels and avoiding agent swarms merely for scale.
Caution: Preprint and task-specific to open-ended ideation.

## Evidence-handling rules

1. Provider documentation is authoritative for current provider capabilities, not for universal performance claims.
2. Peer-reviewed papers outrank preprints for general scientific claims.
3. Preprints are hypothesis-generating evidence and must be marked as such.
4. Benchmark improvements are workload-specific until reproduced on our own task suite.
5. No architectural decision should depend on a single provider feature remaining available.
6. Every important optimisation claim should eventually be validated in our own experiment program.
