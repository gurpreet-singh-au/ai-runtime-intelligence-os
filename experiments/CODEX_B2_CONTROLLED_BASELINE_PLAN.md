# Codex B2 Controlled Baseline Plan

Date: 2026-08-22
Lane: `CODEX-B2-C1`
Status: Designed; adapter not yet implemented
Purpose: cross-runtime/provider validation

## Objective

Establish a separate controlled Codex baseline for the same B2-001 task so the project can compare runtime resource behavior across materially different coding-agent runtimes without contaminating the frozen Claude baseline.

## Core rule

Claude B2 Baseline v1 and the Codex baseline are **separate empirical populations**.

Do not pool their raw statistics. Compare them only after each runtime has its own frozen, internally valid baseline distribution.

## Reuse from B2-001

Where technically compatible, Codex must reuse:

- the same defective fixture semantics;
- the same expected correct behavior;
- the same frozen task intent;
- the same pre-test/post-test evidence;
- the same bounded-diff rule;
- the same independent deterministic evaluator logic;
- the same mandatory-compliance standard.

Runtime-specific prompt wrappers may differ only where required by Codex execution mechanics; any difference must be recorded as an experimental factor.

## Adapter boundary

Create Codex-specific runtime integration under:

`experiments/adapters/codex/`

The adapter owns:

- invocation mechanics;
- permission/sandbox configuration;
- raw runtime capture;
- Codex-specific telemetry extraction;
- environment/version metadata;
- normalization mapping.

It must not own canonical benchmark semantics or redefine success.

## Discovery run

The first Codex execution is a **discovery run**, not automatically a valid baseline.

Suggested ID:

`B2-001-codex-discovery-r01`

Use it to validate:

- executable/CLI availability;
- authentication/credit path;
- workspace permissions;
- Python/pytest resolution;
- Codex sandbox behavior;
- code-edit persistence;
- output/log format;
- available usage/telemetry fields;
- deterministic evaluator compatibility.

If the discovery run exposes harness defects, fix the harness and preserve the run as invalid discovery evidence just as with Claude r01.

## Frozen Codex baseline configuration

After the harness is validated, freeze:

- Codex runtime/client version;
- selected model or default model policy;
- reasoning setting if configurable;
- sandbox/permission mode;
- working directory;
- benchmark Python/pytest environment;
- prompt wrapper;
- tool/access configuration;
- telemetry/normalization semantics.

Do not change these during the baseline series.

## Baseline repetitions

Target **five valid repetitions** where practical, revising only if observed variance justifies more.

Suggested IDs:

- `B2-001-codex-baseline-r01`
- `B2-001-codex-baseline-r02`
- `B2-001-codex-baseline-r03`
- `B2-001-codex-baseline-r04`
- `B2-001-codex-baseline-r05`

## Canonical comparison metrics

Capture when available:

- deterministic success;
- mandatory compliance;
- cost or credit/usage proxy;
- runtime duration;
- input/context processing;
- cached/reused context where exposed;
- output tokens;
- model/reasoning activity;
- tool calls and trajectory;
- agent/subagent activity;
- retries/no-progress loops;
- verification activity;
- telemetry completeness and evidence level.

Provider-specific fields remain provider-specific until mapped deliberately into the canonical telemetry model.

## Cross-runtime comparison rule

The purpose is not to declare a universal 'winner'.

Ask instead:

- does the same successful task induce materially different resource profiles?
- which resource classes are controllable in each runtime?
- which telemetry gaps are provider/runtime-specific?
- can one provider-neutral optimisation policy improve both runtimes, or are runtime-specific policies required behind a shared canonical interface?
- does an intervention transfer across runtimes without quality/compliance regression?

## Guardrails

- Do not use Codex results to retroactively reinterpret Claude measurements without evidence.
- Do not choose a permanent provider from B2 alone.
- Do not tune the Codex prompt to beat Claude; preserve task equivalence.
- Do not compare subscription credits directly with API dollar cost unless their economic semantics are normalized.
- Do not hide unavailable telemetry by converting it to zero.
- Do not run a cross-runtime optimiser before each runtime has a valid baseline.
