# Open Source / Open Weight Stack Register

Last updated: 2026-08-21
Status: Research-stage register; no production adoption implied

## Decision states

`WATCH | BENCHMARK | ADOPT | EXTEND | FORK | REJECT | REPLACE | RETIRE`

## Current candidates

| Capability | Candidate | Type | Status | Notes |
|---|---|---|---|---|
| Model gateway/router | OpenRouter | Managed gateway | BENCHMARK | Useful for broad model access and routing experiments; must remain replaceable. |
| Agent/runtime orchestration | LangGraph | Open source/framework | WATCH | Relevant to durable state/checkpointing; evaluate against simpler/native approaches. |
| Agent/runtime orchestration | AutoGen | Open source/framework | WATCH | Candidate multi-agent runtime; evaluate only if needed. |
| Agent/runtime orchestration | CrewAI | Open source/framework | WATCH | Candidate multi-agent runtime; evaluate only if materially useful. |
| Telemetry standard | OpenTelemetry | Open standard / OSS | WATCH | Strong candidate for provider-neutral tracing/export where fit is proven. |
| Local/open-weight inference | vLLM | Open source serving | WATCH | Relevant for self-hosted/open-weight execution; benchmark later. |
| Local/open-weight inference | llama.cpp | Open source inference | WATCH | Relevant for small/local workloads; benchmark later. |

## Required evaluation before ADOPT

For every material candidate verify:
- current licence and commercial-use rights
- maintenance/release activity
- security history
- architecture fit
- interoperability
- state/data portability
- observability
- operating cost/TCO
- replacement difficulty
- credible alternatives
- benchmark results on project workloads

No candidate in this file is production-approved merely by being listed.
