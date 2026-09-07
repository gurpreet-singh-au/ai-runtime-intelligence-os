# Shared Observation — GPT-5.6 Sol Repeatability in Migration Legal Intelligence OS

Date: 2026-09-07

Source project: `gurpreet-singh-au/migration-legal-intelligence-os`

Data class: synthetic / de-identified evaluation fixture

Model: `gpt-5.6-sol`

Provider: OpenAI Responses API

Processing mode: Standard

Capability context: substantive legal matter analysis with evidence-grounding controls.

## Reusable observation

After a first seven-case synthetic benchmark in which GPT-5.6 Sol achieved 7/7 quality passes with zero deterministic hard failures, the project ran three targeted repeatability executions on `CASE-482-004`, the exact unsupported-business-growth fixture on which GPT-5.6 Terra had shown repeated `UNSUPPORTED_ESTABLISHED_FACT` failures.

Sol targeted repeatability result:

- 3/3 quality passes;
- 0/3 hard failures;
- 100% required issue/gap/escalation recall on every repeat;
- 0 prohibited-claim violations;
- weighted score 100/100 on every repeat;
- mean latency approximately 4.38 seconds;
- aggregate usage 2,607 input tokens and 729 output tokens.

Using the dated portfolio-observed Sol Standard pricing snapshot of US$4/1M input and US$20/1M output, the three-repeat estimate is approximately US$0.02501 total.

Combined with the first seven-case Sol benchmark, the currently observed record is 10/10 successful executions with zero hard failures across these specific synthetic records.

## Portfolio interpretation

This strengthens Sol's position as a provisional cost/performance candidate for substantive legal-analysis capabilities that require factual-grounding discipline. It is not a universal model recommendation and must not be transferred to another project without local capability-specific evaluation.

The evidence is still insufficient for confidential legal production use. Authoritative-source retrieval, larger evidence packs, broader stochastic repeatability, privacy/retention/data-residency controls and project-specific human-review gates remain unresolved.

Terra remains unsuitable for this same substantive evidence-grounding capability on current evidence because the source project observed three `UNSUPPORTED_ESTABLISHED_FACT` hard failures across four executions of the same targeted fixture.
