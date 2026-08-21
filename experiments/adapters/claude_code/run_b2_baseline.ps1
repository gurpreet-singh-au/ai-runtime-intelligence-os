param(
    [string]$RunId = "B2-001-baseline-r01"
)

$ErrorActionPreference = "Stop"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

function Run-PytestCapture([string]$PythonExe, [string]$OutputPath) {
    $Output = & $PythonExe -m pytest tests/test_pricing.py -q 2>&1
    $ExitCode = $LASTEXITCODE
    @($Output) | Out-File -Encoding utf8 $OutputPath
    return [int]$ExitCode
}

Require-Command "git"
Require-Command "py"
Require-Command "claude"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "../../..")).Path
$FixtureSource = Join-Path $RepoRoot "benchmarks/fixtures/python_runtime_fixture"
$PromptPath = Join-Path $RepoRoot "benchmarks/prompts/B2-001-baseline.md"
$RequirementsPath = Join-Path $ScriptDir "benchmark-requirements.txt"
$RunRoot = Join-Path $RepoRoot "experiments/local-runs/$RunId"
$Workspace = Join-Path $RunRoot "workspace"
$Artifacts = Join-Path $RunRoot "artifacts"
$Venv = Join-Path $RunRoot ".venv"
$VenvPython = Join-Path $Venv "Scripts/python.exe"

if (Test-Path $RunRoot) {
    throw "Run directory already exists: $RunRoot. Use a new RunId or archive/remove the prior local run."
}

New-Item -ItemType Directory -Force -Path $Workspace | Out-Null
New-Item -ItemType Directory -Force -Path $Artifacts | Out-Null

Copy-Item -Path (Join-Path $FixtureSource "*") -Destination $Workspace -Recurse -Force
Copy-Item -Path $PromptPath -Destination (Join-Path $Artifacts "TASK_PROMPT.md")

# Build a benchmark-local Python environment so unrelated agent/tool virtual environments
# on PATH (for example Hermes) cannot affect benchmark validity.
& py -3.11 -m venv $Venv
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $VenvPython)) {
    throw "Failed to create benchmark virtual environment at $Venv"
}
& $VenvPython -m pip install --disable-pip-version-check -q -r $RequirementsPath
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install benchmark test dependencies from $RequirementsPath"
}

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
    $PythonVersion = (& $VenvPython --version 2>&1 | Out-String).Trim()
    $PytestVersion = (& $VenvPython -m pytest --version 2>&1 | Out-String).Trim()
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
        pytest_version = $PytestVersion
        python_environment = "benchmark-local-venv"
        observation_mode = "passive-cli-stream-json"
        note = "No Runtime Intelligence intervention. Unknown telemetry fields remain unknown rather than zero."
    }
    $Metadata | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "RUN_METADATA.json")

    $TestsBeforeExit = Run-PytestCapture $VenvPython (Join-Path $Artifacts "tests-before.txt")

    $Prompt = Get-Content -Raw $PromptPath
    $StreamPath = Join-Path $Artifacts "claude-stream.jsonl"
    $StderrPath = Join-Path $Artifacts "claude-stderr.log"

    # Prepend the benchmark venv Scripts directory only for the Claude subprocess so that
    # when Claude invokes `python` or `pytest`, it sees the same controlled environment.
    $OriginalPath = $env:PATH
    $env:PATH = (Join-Path $Venv "Scripts") + ";" + $OriginalPath
    try {
        & claude -p $Prompt --output-format stream-json --verbose 1> $StreamPath 2> $StderrPath
        $ClaudeExit = $LASTEXITCODE
    }
    finally {
        $env:PATH = $OriginalPath
    }

    $EndedAt = [DateTimeOffset]::Now
    $TestsAfterExit = Run-PytestCapture $VenvPython (Join-Path $Artifacts "tests-after.txt")

    git status --short | Out-File -Encoding utf8 (Join-Path $Artifacts "git-after.txt")
    git diff --binary | Out-File -Encoding utf8 (Join-Path $Artifacts "git-diff.patch")

    $Metadata.ended_at = $EndedAt.ToString("o")
    $Metadata.duration_ms = [int64](($EndedAt - $StartedAt).TotalMilliseconds)
    $Metadata.claude_exit_code = $ClaudeExit
    $Metadata.tests_before_exit_code = $TestsBeforeExit
    $Metadata.tests_after_exit_code = $TestsAfterExit
    $Metadata | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "RUN_METADATA.json")

    $InventoryScript = Join-Path $ScriptDir "inventory_stream.py"
    & $VenvPython $InventoryScript $StreamPath (Join-Path $Artifacts "STREAM_INVENTORY.json")

    $NormalizerScript = Join-Path $ScriptDir "normalize_claude_run.py"
    & $VenvPython $NormalizerScript $Artifacts

    Write-Host "Baseline capture complete: $RunId"
    Write-Host "Artifacts: $Artifacts"
    Write-Host "Normalization: normalized-run.json"
    Write-Host "Telemetry audit: TELEMETRY_COMPLETENESS.json"
    Write-Host "STOP HERE before further repetitions. Audit telemetry completeness first."
}
finally {
    Pop-Location
}
