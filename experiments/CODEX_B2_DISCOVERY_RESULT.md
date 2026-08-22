# Codex B2 Discovery Result

Date: 2026-08-22
Lane: `CODEX-B2-C1`
Status: **Discovery executed; native-Windows bounded-write path blocked by upstream/runtime sandbox defect**

## Runs

### `B2-001-codex-discovery-r01`

Aborted before meaningful agent execution. The installed Codex client emitted the known shared `models_cache.json` compatibility diagnostic (`missing field base_instructions`), and the PowerShell harness initially promoted native stderr to a terminating `NativeCommandError`.

### `B2-001-codex-discovery-r02`

Aborted for the same PowerShell/native-stderr interaction after switching from the npm PowerShell shim to `codex.cmd`. This established that the wrapper choice alone did not solve the harness interaction.

### `B2-001-codex-discovery-r03`

The harness was changed to treat native stderr as captured process evidence while preserving the Codex exit code as authoritative.

The Codex process then executed successfully at the process level:

- Codex version: `codex-cli 0.144.3`
- command: Windows npm `codex.cmd`
- process exit code: `0`
- requested sandbox: `workspace-write`
- `danger-full-access`: **not used**
- models-cache compatibility warning: observed
- pre-tests: failed as expected (`exit 1`)
- post-tests: still failed (`exit 1`)
- deterministic outcome: failed
- tracked code diff: none
- benchmark comparison eligible: **false**

## Structured event evidence

The JSONL stream parsed cleanly with four events:

1. `thread.started`
2. `turn.started`
3. `item.completed`
4. `turn.completed`

The only completed item was:

- `agent_message`

No `command_execution` event was observed.
No `file_change` event was observed.
No tracked source-code change was observed.

## Codex usage evidence

`turn.completed` exposed native usage fields:

- input tokens: **9,010**
- cached input tokens: **0**
- output tokens: **46**
- reasoning output tokens: **0**

This is valuable telemetry evidence even though the run is not a valid benchmark sample.

Do not compare these numbers directly with Claude B2 statistics yet because the Codex task did not execute equivalently.

## Why the task failed

The completed agent message explicitly stated that the workspace was currently **read-only** and asked for the bug report/code change rather than inspecting and editing the benchmark.

This occurred despite the harness explicitly requesting:

`--sandbox workspace-write`

The apparent `workspace_modified: true` signal was caused only by untracked Python cache directories produced by the deterministic pre/post tests:

- `runtime_fixture/__pycache__/`
- `tests/__pycache__/`

There was no tracked benchmark-code modification.

## Upstream corroboration

OpenAI Codex issue `#34961`, titled **"Windows: codex exec --sandbox workspace-write remains read-only"**, describes the same observed pattern:

- native Windows;
- `codex exec`;
- explicit `--sandbox workspace-write`;
- process exits successfully;
- effective sandbox remains read-only;
- expected workspace file is not created;
- unrestricted filesystem access is rejected as an acceptable workaround.

This is close enough to the local observation that the current working diagnosis is:

> **The native-Windows Codex B2 discovery lane is blocked by a known/active workspace-write sandbox defect or limitation, rather than by B2 task semantics or the deterministic evaluator.**

This remains an evidence-based working diagnosis, not a claim about the entire Codex product or all platforms.

## Additional environment issue

OpenAI Codex issue `#39291` documents the `models_cache.json` backward-compatibility warning where a cache written by a newer client lacks the legacy `base_instructions` field expected by an older client. The issue states that the older client falls back to a remote model fetch.

The warning therefore remains recorded as an environment defect but is no longer the primary blocker for r03, because r03 reached and completed a model turn.

## Decision

**Do not weaken the experiment to `danger-full-access` merely to obtain a successful sample.**

That would change the security/runtime boundary and would conceal the bounded-write defect we are trying to measure.

**Do not count r01, r02 or r03 as Codex baseline runs.**

The Codex lane remains in discovery.

## Safe next paths

Preferred order:

1. Probe whether a WSL/Linux Codex execution environment is already available locally, without installing software or copying authentication material.
2. If a supported/authenticated WSL/Linux path exists, validate bounded `workspace-write` semantics with a minimal synthetic write probe before executing B2.
3. Independently watch the native-Windows Codex sandbox issue/current release status.
4. Only after a bounded-write runtime is validated should a fresh Codex B2 discovery execution be attempted and then considered for harness freeze.

Do not automatically upgrade Codex during an experiment. Runtime upgrades are experimental-factor changes and must be recorded and re-probed.

## Commercial/runtime-intelligence relevance

The failure itself is useful evidence for the project thesis:

- requested runtime policy and effective runtime policy can diverge;
- process exit `0` is insufficient evidence that intended execution occurred;
- workspace side-effect flags can be contaminated by evaluator/test artifacts;
- parent-task outcome validation is necessary;
- runtime-specific telemetry and policy propagation defects must be normalised rather than hidden.

This strengthens the need for independent outcome, policy and side-effect evidence in the canonical telemetry model.
