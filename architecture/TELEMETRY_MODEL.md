# AI Runtime Telemetry Model

Date: 2026-08-21
Status: Architecture research v0.1

## Purpose

Define the minimum provider-neutral telemetry needed to attribute AI runtime resource consumption to task outcomes and to support future Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise capabilities.

The telemetry model must remain independent of any one provider, gateway, observability vendor or agent framework.

## Design principles

1. **Outcome-first:** telemetry exists to explain and improve successful outcomes, not merely to count tokens.
2. **Canonical:** provider-specific events are normalised into internal event types.
3. **Temporal:** preserve timestamps, versions and ordering.
4. **Hierarchical:** represent parent tasks, agents, model calls, tool calls and verification spans.
5. **Evidence-preserving:** raw vendor/tool payloads may remain external, but canonical records retain references and provenance.
6. **Privacy-minimising:** do not retain raw sensitive content unless required and authorised.
7. **Intervention-ready:** record enough state to replay or compare execution strategies later.

## Core hierarchy

```text
Workflow / Parent Outcome
    └── Task
        ├── Context assembly
        ├── Instruction assembly
        ├── Agent / subagent
        │   ├── Model inference
        │   ├── Tool execution
        │   └── State transition
        ├── Verification
        └── Outcome evaluation
```

## Canonical identifiers

Every material event should be linkable through stable IDs:

```text
run_id
workflow_id
task_id
parent_task_id
agent_id
parent_agent_id
span_id
parent_span_id
provider_request_id (optional external reference)
```

## Event envelope

All canonical events should support:

```yaml
event_id:
event_type:
timestamp_start:
timestamp_end:
run_id:
workflow_id:
task_id:
agent_id:
span_id:
parent_span_id:
source_system:
source_version:
telemetry_schema_version:
correlation_ids: {}
metadata: {}
```

## Event families

### 1. Task lifecycle

Event types:
- `task.created`
- `task.started`
- `task.phase_changed`
- `task.completed`
- `task.failed`
- `task.cancelled`

Fields:
- task class/fingerprint
- objective reference
- complexity estimate
- ambiguity estimate
- risk class
- quality threshold
- latency target
- budget ceiling
- required capabilities
- expected verification depth
- final completion state

### 2. Context assembly

Event types:
- `context.item_considered`
- `context.item_included`
- `context.item_excluded`
- `context.compacted`
- `context.retrieved`
- `context.externalised`

Canonical context item fields:

```yaml
context_item_id:
source_type: conversation|file|retrieval|tool_result|memory|evidence|generated_state|other
source_reference:
version:
content_hash:
physical_tokens:
estimated_relevance:
staleness_status:
duplicate_group_id:
authority_level:
provenance_reference:
inclusion_reason:
exclusion_reason:
retention_tier: hot|warm|cool|cold|evidence
```

Derived metrics:
- total context tokens
- relevant context estimate
- duplicate/stale context estimate
- context utility density
- context growth rate
- hot-state turnover

### 3. Instruction assembly

Event types:
- `instruction.discovered`
- `instruction.applicability_evaluated`
- `instruction.included`
- `instruction.excluded`
- `instruction.conflict_detected`
- `instruction.compiled`

Canonical fields:

```yaml
instruction_id:
source_authority:
scope:
priority:
mandatory:
effective_from:
effective_to:
supersedes:
semantic_group:
applicability_score:
applicability_reason:
physical_tokens:
compiled_variant_id:
```

Required invariant telemetry:
- mandatory instructions applicable
- mandatory instructions included
- mandatory instruction compliance result

Derived metrics:
- instruction tokens
- applicability ratio
- duplicate/overlap ratio
- conflict count
- mandatory-rule compliance

### 4. Model inference

Event types:
- `model.requested`
- `model.started`
- `model.completed`
- `model.failed`
- `model.retried`
- `model.fallback`

Fields:

```yaml
capability_requested:
provider:
model:
model_version:
route_policy_version:
reasoning_effort:
input_tokens:
cached_input_tokens:
output_tokens:
reasoning_tokens_or_units:
time_to_first_token_ms:
duration_ms:
provider_cost:
retry_count:
finish_reason:
structured_output_valid:
cache_hit:
```

Do not assume all providers expose all fields. Preserve `unknown` rather than fabricate estimates unless explicitly labelled estimated.

### 5. Model routing decision

Event type: `routing.model_decision`

Fields:
- candidate models/providers
- qualification results
- task-specific benchmark/eval scores
- privacy/data-policy eligibility
- context/capability fit
- predicted quality
- predicted cost
- predicted latency
- chosen route
- rejected routes/reasons
- fallback order
- decision policy version

This event belongs to the Runtime Intelligence layer, not a provider gateway.

### 6. Agent/subagent lifecycle

Event types:
- `agent.spawn_proposed`
- `agent.spawn_approved`
- `agent.spawn_rejected`
- `agent.started`
- `agent.checkpointed`
- `agent.completed`
- `agent.terminated`
- `agent.failed`

Fields:

```yaml
agent_role:
agent_version:
subtask:
spawn_reason:
decomposability_estimate:
expected_information_gain:
expected_cost:
assigned_model:
agent_budget:
permissions_profile:
tool_allowlist:
stop_conditions:
termination_reason:
unique_contribution_score:
overlap_score:
```

Derived metrics:
- subagents per successful outcome
- agent marginal utility
- overlap/correlation
- coordination overhead
- cost by agent role

### 7. Tool capability exposure

Event types:
- `tool.discovered`
- `tool.exposed`
- `tool.hidden`
- `tool.permission_denied`

Fields:
- tool/capability ID
- schema version
- schema token estimate
- reason exposed
- permission policy
- relevant capability match

Derived metrics:
- exposed tools vs used tools
- tool-schema token load
- unnecessary capability exposure

### 8. Tool execution

Event types:
- `tool.called`
- `tool.completed`
- `tool.failed`
- `tool.retried`
- `tool.result_externalised`

Fields:

```yaml
tool_id:
capability:
input_reference:
output_reference:
raw_output_bytes:
model_visible_output_tokens:
duration_ms:
external_cost:
cache_hit:
retry_count:
result_hash:
information_gain_estimate:
repeated_call_group_id:
```

Derived metrics:
- repeated tool-call ratio
- useful tool-call rate
- model-visible result inflation
- tool information gain per cost

### 9. State / memory

Event types:
- `state.read`
- `state.write`
- `state.checkpoint`
- `state.superseded`
- `state.retrieved`

Fields:
- state object ID/type/version
- retention tier
- provenance
- read/write cost/latency
- supersession relationship
- retrieval score

### 10. Useful state change

Event type: `progress.state_change`

This is a project-specific experimental event.

Candidate fields:
- before-state reference
- after-state reference
- change category
- semantic novelty estimate
- objective progress estimate
- evaluator confidence
- reversible/irreversible

Candidate categories:
- evidence acquired
- decision resolved
- artifact changed
- test status changed
- blocker removed
- requirement clarified
- duplicate/no-op

This event is essential for testing Useful State Change Rate and semantic-loop detection.

### 11. Runtime anomaly / loop

Event types:
- `runtime.loop_suspected`
- `runtime.no_progress`
- `runtime.budget_threshold`
- `runtime.strategy_change`
- `runtime.stop_recommended`

Fields:
- detection rule/model
- evidence window
- repeated operations
- token/cost growth
- state-change rate
- recommended intervention
- intervention accepted/rejected

### 12. Verification

Event types:
- `verification.requested`
- `verification.started`
- `verification.completed`
- `verification.failed`
- `verification.escalated`

Fields:
- verification type
- risk basis
- deterministic/AI/human
- verifier independence
- defect/error detected
- confidence delta
- cost
- latency

### 13. Outcome evaluation

Event type: `outcome.evaluated`

Fields:

```yaml
outcome_id:
success:
quality_score:
reliability_score:
safety_compliance:
mandatory_rule_compliance:
grounding_score:
human_correction_required:
business_or_task_value:
latency_acceptance:
residual_risk:
evaluator_id:
evaluator_version:
```

A completed agent run must not automatically equal a successful outcome.

### 14. Economics

Canonical cost fields should distinguish:
- model input
- model cached input
- model output/reasoning
- tools/APIs
- storage/retrieval
- gateway/observability fees where attributable
- infrastructure/self-hosted inference
- verification
- human review where measured

Derived metrics:
- cost per successful outcome
- risk-adjusted cost per successful outcome
- quality per dollar
- cost by resource class
- wasted/redundant cost estimate

## Marginal Compute Utility event

Experimental event: `allocation.marginal_utility_estimated`

```yaml
resource_increment:
resource_class:
expected_outcome_delta:
expected_quality_delta:
expected_risk_delta:
incremental_cost:
incremental_latency:
confidence:
decision: allocate|do_not_allocate|mandatory_override
policy_version:
```

Examples:
- another subagent
- another search
- 20k more context tokens
- stronger model
- higher reasoning effort
- additional verifier

## Minimum Viable Telemetry (MVT)

For the first experiment, do not attempt the entire schema. Capture at minimum:

1. run/task/agent/span IDs;
2. model/provider/version;
3. input/cached/output tokens;
4. context size and coarse composition;
5. instruction size and source classes;
6. agent/subagent count and assigned models;
7. tool calls, repeated calls and model-visible result size;
8. start/end/duration;
9. cost where available;
10. meaningful state-change checkpoints;
11. final outcome/evaluator score;
12. intervention/baseline policy version.

## Integration strategy

Prefer adapters from existing telemetry formats rather than custom instrumentation everywhere.

Candidate inputs:
- OpenTelemetry-compatible traces;
- Langfuse traces;
- LangSmith traces;
- Braintrust traces;
- gateway/provider usage metadata;
- native agent-runtime logs;
- custom lightweight SDK for missing context/instruction/resource events.

Canonical pipeline:

```text
Native runtime / OTel / vendor telemetry
            ↓
      Telemetry Adapter
            ↓
    Canonical Event Model
            ↓
  Attribution + Evaluation
            ↓
Runtime Intelligence / Replay
```

## Privacy model

Default to references, hashes, classifications and aggregate metrics instead of raw content.

Raw prompts, tool outputs, documents and evidence should be retained only when required for evaluation/reconstruction and allowed by project/customer policy.

## Open research questions

- How accurately can context relevance be measured without expensive second-pass inference?
- How should semantic state change be measured across heterogeneous tasks?
- Which providers expose reliable cache and reasoning telemetry?
- Can traces from competing observability platforms be normalised without losing critical semantics?
- What telemetry is required for causal/counterfactual claims rather than correlation?
- How much overhead does instrumentation itself create?

## Acceptance criterion for v0.1

The schema is sufficient when one representative agent run can be reconstructed as a resource graph and its cost, time, agent/tool/model activity and evaluated outcome can be attributed without depending on provider-specific canonical state.
