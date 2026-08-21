# Agent Governance Register

Last updated: 2026-08-21
Status: Bootstrap skeleton

## Purpose

Track material agents/subagents as governed software actors rather than anonymous inference branches.

## Required record

For each material agent define:
- agent_id
- purpose
- owner
- capability requirements
- model eligibility
- permitted tools
- data access
- write permissions
- external communication authority
- spend/token/time budget
- recursion/delegation authority
- risk class
- autonomy level
- escalation path
- KPIs/evaluation status
- version/lifecycle state

## Runtime-specific policy

Before spawning a subagent evaluate:
1. whether any LLM call is required;
2. whether a distinct agent is required;
3. whether deterministic software can perform the subtask;
4. whether the task is independently decomposable;
5. expected unique information/quality gain;
6. overlap/correlation with existing agents;
7. cheapest qualified model/capability route;
8. time/cost/tool budget;
9. termination and escalation conditions.

## Current agents

No production agents have been approved or registered yet.

Research experiments may create temporary agent profiles, but their purpose, model, permissions, budget, and evaluation result should be recorded before findings are promoted into architecture decisions.
