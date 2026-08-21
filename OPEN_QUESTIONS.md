# Open Questions — AI Runtime Intelligence OS

Last updated: 2026-08-21

## Problem / market

1. Which customer segment experiences runtime waste acutely enough to pay for an independent control layer?
2. Is the first wedge coding agents, enterprise agent platforms, AI application teams, AI FinOps, or another segment?
3. Which parts of the problem will providers absorb natively and which remain durable cross-provider value?
4. What incumbent-copy and zero-integration tests should the commercial thesis pass?
5. What are explicit kill/pivot criteria after Phase 0 research?

## Telemetry

6. What minimum provider-neutral telemetry is available across Claude, OpenAI/Codex, Gemini, major gateways, and agent frameworks?
7. Can instruction-token, tool-schema, cache, subagent, and tool-result attribution be observed reliably?
8. How should useful state change be measured generically?
9. What data can be collected without retaining unnecessary sensitive prompts/content?

## Context / instructions

10. Can task relevance be estimated safely enough for selective context loading?
11. How can mandatory instructions be represented so they can never be pruned accidentally?
12. How should semantic duplicates/conflicts/supersession be detected and resolved?
13. What is the right balance between structured instructions and natural-language instructions?
14. Can instruction bundles be compiled/cached by scope and task class?

## Agents

15. When does an additional subagent materially improve the parent-task outcome?
16. How should overlap/correlation between agents be estimated?
17. Can simple subagents be safely routed to cheap/free models while preserving parent-task quality?
18. When does model diversity improve verification versus add noise?
19. What hard budget/recursion/timeout rules should apply?

## Models / routing

20. What task-specific evaluation data is required before a model becomes routing-eligible?
21. Should OpenRouter be used in the first prototype, direct APIs, or both?
22. How should free-tier volatility, provider privacy, rate limits, and deprecation be represented in routing policy?
23. How should reasoning effort be allocated dynamically?
24. Which tasks should never be routed automatically due to consequence/risk?

## Economics

25. Can Marginal Compute Utility be estimated in practice, and at what granularity?
26. What should be the primary economic metric: cost per successful outcome, risk-adjusted cost per successful outcome, or another measure?
27. How much overhead does the control plane itself add?
28. What minimum savings/quality improvement would create compelling ROI?

## Architecture / governance

29. Which runtime decisions should be deterministic versus learned/predictive?
30. What canonical schemas are needed for Task Resource Profile, Execution Plan, Runtime Event, Evaluation Result, and Routing Decision?
31. How should historical model/provider/policy versions be reconstructed?
32. What is the first safe autonomous intervention after advisory mode?
33. How should self-improvement propose routing/policy changes without crossing protected-governance boundaries?

## Experiments

34. What representative tasks provide realistic, repeatable, measurable agent workloads?
35. How should non-inferiority in quality be established when testing cost-saving interventions?
36. Which intervention should be tested first: instruction compilation, context selection, tool-surface reduction, model routing, or subagent control?
