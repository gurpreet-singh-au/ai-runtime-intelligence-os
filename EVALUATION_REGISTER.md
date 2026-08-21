# Evaluation Register

Last updated: 2026-08-21
Status: Bootstrap skeleton

## Purpose

Track representative evaluations for runtime interventions so claims of efficiency are tied to outcome quality, not token reduction alone.

## Evaluation dimensions

Where relevant measure:
- parent-task success
- task-specific accuracy/quality
- grounding/evidence completeness
- structured-output validity
- tool-use correctness
- failure/retry rate
- latency
- input/output/cached tokens
- instruction/context/tool-schema load
- agent count and contribution
- external tool cost
- total cost
- quality regression
- successful business/user outcome

## Experiment classes

1. Baseline execution
2. Context selection
3. Instruction compilation
4. Dynamic tool exposure
5. Tool-result externalisation
6. Subagent-count/model routing
7. Reasoning-effort routing
8. Checkpoint/clean resume
9. Loop/no-progress stopping
10. Deterministic substitution
11. Combined runtime policy

## Acceptance principle

An efficiency intervention is not considered successful merely because it costs less. It must meet the predefined quality/reliability/risk threshold for the target workload.

## Current evaluations

None completed under a formal benchmark protocol yet.
