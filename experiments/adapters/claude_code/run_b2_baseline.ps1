param(
    [string]$RunId = "B2-001-baseline-r01"
)

$ErrorActionPreference = "Stop"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

Require-Command "git"
Require-Command "python"
Require-Command "claude"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "../../..")).Path
$FixtureSource = Join-Path $RepoRoot "benchmarks/fixtures/python_runtime_fixture"
$PromptPath = Join-Path $RepoRoot "benchmarks/prompts/B2-001-baseline.md"
$RunRoot = Join-Path $RepoRoot "experiments/local-runs/$RunId"
$Workspace = Join-Path $RunRoot "workspace"
$Artifacts = Join-Path $RunRoot "artifacts"

if (Test-Path $RunRoot) {
    throw "Run directory already exists: $RunRoot. Use a new RunId or archive/remove the prior local run."
}

New-Item -ItemType Directory -Force -Path $Workspace | Out-Null
New-Item -ItemType Directory -Force -Path $Artifacts | Out-Null

Copy-Item -Path (Join-Path $FixtureSource "*") -Destination $Workspace -Recurse -Force
Copy-Item -Path $PromptPath -Destination (Join-Path $Artifacts "TASK_PROMPT.md")

Push-Location $Workspace
try {
    git init -q
    git config user.email "benchmark@local.invalid"
    git config user.name "AI Runtime Benchmark"
    git add .
    git commit -q -m "Freeze B2-001 benchmark baseline"

    $GitBefore = git rev-parse HEAD
    $GitBefore | Out-File -Encoding utf8 (Join-Path $Artifacts "git-before.txt")

    $ClaudeVersion = (& claude --version 2>&1 | Out-String).Trim()
    $PythonVersion = (& python --version 2>&1 | Out-String).Trim()
    $StartedAt = [DateTimeOffset]::Now

    $Metadata = [ordered]@{
        schema_version = "0.1"
        run_id = $RunId
        benchmark_id = "B2-001"
        policy_variant = "baseline"
        started_at = $StartedAt.ToString("o")
        source_repository_commit = (git -C $RepoRoot rev-parse HEAD)
        repository_commit = (git -C $RepoRoot rev-parse HEAD)
        task_snapshot = $GitBefore
        workspace_baseline_commit = $GitBefore
        runtime = "Claude Code"
        runtime_version = $ClaudeVersion
        python_version = $PythonVersion
        observation_mode = "passive-cli-stream-json"
        note = "No Runtime Intelligence intervention. Unknown telemetry fields remain unknown rather than zero."
    }
    $Metadata | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "RUN_METADATA.json")

    try {
        python -m pytest tests/test_pricing.py -q *>&1 | Tee-Object -FilePath (Join-Path $Artifacts "tests-before.txt")
    } catch {
        # A failing pre-run test is expected for this benchmark. Preserve output and continue.
    }

    $Prompt = Get-Content -Raw $PromptPath
    $StreamPath = Join-Path $Artifacts "claude-stream.jsonl"
    $StderrPath = Join-Path $Artifacts "claude-stderr.log"

    # Keep the Claude execution policy at its normal baseline. The flags below only request
    # non-interactive, machine-readable observation output.
    & claude -p $Prompt --output-format stream-json --verbose 1> $StreamPath 2> $StderrPath
    $ClaudeExit = $LASTEXITCODE

    $EndedAt = [DateTimeOffset]::Now

    try {
        python -m pytest tests/test_pricing.py -q *>&1 | Tee-Object -FilePath (Join-Path $Artifacts "tests-after.txt")
        $TestsAfterExit = 0
    } catch {
        $TestsAfterExit = 1
    }

    git status --short | Out-File -Encoding utf8 (Join-Path $Artifacts "git-after.txt")
    git diff --binary | Out-File -Encoding utf8 (Join-Path $Artifacts "git-diff.patch")

    $Metadata.ended_at = $EndedAt.ToString("o")
    $Metadata.duration_ms = [int64](($EndedAt - $StartedAt).TotalMilliseconds)
    $Metadata.claude_exit_code = $ClaudeExit
    $Metadata.tests_after_exit_code = $TestsAfterExit
    $Metadata | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "RUN_METADATA.json")

    $InventoryScript = Join-Path $ScriptDir "inventory_stream.py"
    python $InventoryScript $StreamPath (Join-Path $Artifacts "STREAM_INVENTORY.json")

    $NormalizerScript = Join-Path $ScriptDir "normalize_claude_run.py"
    python $NormalizerScript $Artifacts

    Write-Host "Baseline capture complete: $RunId"
    Write-Host "Artifacts: $Artifacts"
    Write-Host "Normalization: normalized-run.json"
    Write-Host "Telemetry audit: TELEMETRY_COMPLETENESS.json"
    Write-Host "STOP HERE before r02-r05. Audit telemetry completeness first."
}
finally {
    Pop-Location
}
