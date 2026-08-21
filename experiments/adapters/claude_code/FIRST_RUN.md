# First Baseline Run — B2-001

Status: ready for local execution

## Goal

Capture `B2-001-baseline-r01` with passive observation only, then stop and audit telemetry completeness before any further repetitions.

## Preconditions

- repository cloned locally;
- Windows PowerShell available;
- `git` on PATH;
- `python` on PATH;
- `pytest` available to the selected Python environment;
- Claude Code CLI installed and already authenticated/configured for the operator's normal environment.

Do not place API keys or credentials in the repository.

## Run

From the repository root in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\experiments\adapters\claude_code\run_b2_baseline.ps1
```

The script creates an ignored local directory:

```text
experiments/local-runs/B2-001-baseline-r01/
```

It freezes a copy of the benchmark fixture in a local Git repository, captures the failing tests, executes Claude Code in non-interactive machine-readable mode, captures the resulting tests/diff/runtime metadata, and inventories the stream schema without assuming undocumented field semantics.

## Do not run r02-r05 yet

After r01, inspect:

- `artifacts/RUN_METADATA.json`
- `artifacts/claude-stream.jsonl`
- `artifacts/STREAM_INVENTORY.json`
- `artifacts/claude-stderr.log`
- `artifacts/git-diff.patch`
- `artifacts/tests-before.txt`
- `artifacts/tests-after.txt`

Then answer the telemetry-completeness questions in `README.md` for this adapter.

## Data handling

The first fixture is synthetic and contains no client/personal data. Keep later benchmark runs synthetic or appropriately sanitised until privacy/security governance for production telemetry has been validated.

## Failure handling

If `claude --output-format stream-json` or another observation-only flag is unsupported by the installed Claude Code version:

1. preserve the CLI version and error output;
2. do not silently switch to another execution policy;
3. record the incompatibility;
4. update this experimental adapter based on current official documentation;
5. re-run r01 under a new clearly documented adapter version.

If Claude completes the task but telemetry is insufficient, that is still a useful experimental result: the observability gap is evidence for the next instrumentation decision.
