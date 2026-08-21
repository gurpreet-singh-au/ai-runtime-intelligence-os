# Claude Code Passive Observation Adapter — Tranche 01

Status: experimental only; not a foundational dependency
Date: 2026-08-22

## Purpose

Capture the first untouched Claude Code benchmark run with enough raw evidence to normalise into `experiments/RUN_SCHEMA.json` without changing Claude Code's normal task-solving policy.

## Why Claude Code first

Claude Code is a practical first observation target because the project was partly motivated by long-context, long-running and subagent-heavy coding-agent behaviour. This is an experimental choice only. The canonical runtime model remains provider- and framework-neutral.

## Official capabilities used

Current Anthropic documentation confirms that Claude Code supports:

- non-interactive print mode via `claude -p`;
- `--output-format json` and `--output-format stream-json` for programmatic capture;
- `--verbose` for turn-by-turn logging;
- model/session controls and maximum-turn controls;
- enterprise usage monitoring via OpenTelemetry;
- LLM gateway configurations capable of usage tracking, audit logging, budgets and routing.

Primary references reviewed 2026-08-22:

- https://docs.anthropic.com/en/docs/claude-code/cli-usage
- https://docs.anthropic.com/en/docs/claude-code/llm-gateway
- https://docs.anthropic.com/en/docs/claude-code/security

Do not assume undocumented telemetry fields exist. Raw capture is authoritative; parser-derived fields must identify their confidence/source.

## Observation layers

### Layer A — mandatory raw CLI capture

For each run preserve:

1. exact task prompt;
2. benchmark/fixture commit SHA;
3. Claude Code version;
4. start/end timestamps;
5. complete `stream-json` output where available;
6. stderr/verbose log where available;
7. final Git diff;
8. deterministic test output;
9. any runtime-reported usage/cost/session metadata.

### Layer B — OpenTelemetry, when already available/configured

If the execution environment exposes Claude Code OpenTelemetry usage metrics, preserve the raw export as an additional evidence source.

Do not make OpenTelemetry availability a prerequisite for the first run. The purpose of r01 is also to discover the observability gap.

### Layer C — optional gateway telemetry

A future experiment may route through a gateway for additional request-level usage/cost telemetry. That would be a new experimental configuration and must not be mixed into the untouched baseline silently.

## Baseline contamination rules

For baseline r01:

- do not add Runtime Intelligence recommendations;
- do not deliberately restrict context or tools beyond the benchmark sandbox;
- do not instruct Claude to use fewer tokens, agents, searches or tool calls;
- do not impose a custom model solely to improve cost;
- do not add external routing/gateway behaviour unless that is already the selected baseline environment;
- do not modify the benchmark prompt after execution begins.

Safety/sandbox restrictions are not considered optimisation contamination.

## Minimum evidence bundle

Use the following directory shape outside the benchmark working tree or under a run-artifact location that Claude is not asked to edit:

```text
runs/B2-001-baseline-r01/
  RUN_METADATA.json
  TASK_PROMPT.md
  claude-stream.jsonl
  claude-stderr.log
  git-before.txt
  git-after.txt
  git-diff.patch
  tests-before.txt
  tests-after.txt
  normalized-run.json
  NORMALIZATION_NOTES.md
```

Missing artifacts are allowed only if the environment cannot expose them. Record the gap rather than fabricating data.

## Normalisation principles

- `OBSERVED`: directly present in raw runtime/tool/test evidence.
- `DERIVED`: mechanically calculated from observed evidence.
- `INFERRED`: estimated/classified from transcript or heuristics.
- `UNKNOWN`: unavailable.

Do not turn `UNKNOWN` into zero.

Examples:
- runtime-reported input token count -> OBSERVED;
- duration from two timestamps -> DERIVED;
- repeated unchanged-file read -> DERIVED if file/tool events are visible;
- useful state change -> INFERRED until a validated task-specific method exists;
- instruction tokens when system/project instructions are hidden -> UNKNOWN, not 0.

## First-run stopping point

After B2-001 baseline r01, stop the tranche and audit telemetry completeness before running r02-r05.

Questions to answer:

1. Can model/token usage be reconstructed?
2. Can tool calls be reconstructed?
3. Can repeated reads/tests be reconstructed?
4. Can agent/subagent lineage be reconstructed?
5. Is context composition visible or only aggregate usage?
6. Are instructions separable from other input?
7. Can elapsed runtime be measured reliably?
8. Is cost directly reported or only calculable from usage/pricing?
9. What important fields in `RUN_SCHEMA.json` remain UNKNOWN?

The answer determines whether the next adapter should use native OpenTelemetry, a gateway/proxy, a Claude Agent SDK harness, or another runtime.
