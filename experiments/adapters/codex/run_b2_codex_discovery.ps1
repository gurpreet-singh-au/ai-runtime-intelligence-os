param(
    [string]$RunId = "B2-001-codex-discovery-r01"
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
Require-Command "codex"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "../../..")).Path
$FixtureSource = Join-Path $RepoRoot "benchmarks/fixtures/python_runtime_fixture"
$PromptPath = Join-Path $RepoRoot "benchmarks/prompts/B2-001-baseline.md"
$RequirementsPath = Join-Path $RepoRoot "experiments/adapters/claude_code/benchmark-requirements.txt"
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

& py -3.11 -m venv $Venv
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $VenvPython)) {
    throw "Failed to create benchmark-local virtual environment."
}
& $VenvPython -m pip install --disable-pip-version-check -q -r $RequirementsPath
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install benchmark test dependencies."
}

Push-Location $Workspace
try {
    git init -q
    git config user.email "benchmark@local.invalid"
    git config user.name "AI Runtime Benchmark"
    git add .
    git commit -q -m "Freeze B2-001 Codex discovery fixture"

    $GitBefore = git rev-parse HEAD
    $GitBefore | Out-File -Encoding utf8 (Join-Path $Artifacts "git-before.txt")

    $CodexCommand = (Get-Command codex).Source
    $CodexVersion = (& codex --version 2>&1 | Out-String).Trim()
    $PythonVersion = (& $VenvPython --version 2>&1 | Out-String).Trim()
    $PytestVersion = (& $VenvPython -m pytest --version 2>&1 | Out-String).Trim()
    $StartedAt = [DateTimeOffset]::Now

    $Metadata = [ordered]@{
        schema_version = "0.1"
        run_id = $RunId
        benchmark_id = "B2-001"
        lane = "CODEX-B2-C1"
        run_class = "discovery"
        policy_variant = "baseline-task-semantics"
        started_at = $StartedAt.ToString("o")
        source_repository_commit = (git -C $RepoRoot rev-parse HEAD)
        workspace_baseline_commit = $GitBefore
        runtime = "Codex CLI"
        runtime_version = $CodexVersion
        codex_command = $CodexCommand
        python_version = $PythonVersion
        pytest_version = $PytestVersion
        python_environment = "benchmark-local-venv"
        requested_sandbox = "workspace-write"
        network_requested = "disabled-via-config"
        session_persistence = "ephemeral"
        user_config_loaded = $false
        user_rules_loaded = $false
        json_event_capture = $true
        benchmark_comparison_eligible = $false
        note = "Discovery-only. Validates installed Codex 0.144.x execution, Windows workspace-write semantics, edit persistence, JSON event schema and deterministic evaluator compatibility. No dangerous-full-access fallback is permitted."
    }
    $Metadata | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "RUN_METADATA.json")

    $TestsBeforeExit = Run-PytestCapture $VenvPython (Join-Path $Artifacts "tests-before.txt")

    $Prompt = Get-Content -Raw $PromptPath
    $StreamPath = Join-Path $Artifacts "codex-stream.jsonl"
    $StderrPath = Join-Path $Artifacts "codex-stderr.log"
    $FinalMessagePath = Join-Path $Artifacts "codex-final-message.txt"

    # Give Codex the same controlled Python/pytest environment seen by the evaluator.
    $OriginalPath = $env:PATH
    $env:PATH = (Join-Path $Venv "Scripts") + ";" + $OriginalPath
    try {
        # Important discovery controls:
        # - workspace-write requested explicitly;
        # - no automatic fallback to danger-full-access;
        # - session is ephemeral;
        # - user config/rules are ignored to reduce uncontrolled runtime policy;
        # - network and plugin activity are disabled through explicit config overrides;
        # - JSONL events are captured for schema discovery.
        & codex exec `
            --json `
            --color never `
            --sandbox workspace-write `
            --ephemeral `
            --ignore-user-config `
            --ignore-rules `
            --skip-git-repo-check `
            -C $Workspace `
            -c 'sandbox_workspace_write.network_access=false' `
            -c 'web_search="disabled"' `
            -c 'features.plugins=false' `
            --output-last-message $FinalMessagePath `
            $Prompt `
            1> $StreamPath 2> $StderrPath
        $CodexExit = $LASTEXITCODE
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
    $Metadata.codex_exit_code = $CodexExit
    $Metadata.tests_before_exit_code = $TestsBeforeExit
    $Metadata.tests_after_exit_code = $TestsAfterExit
    $Metadata.workspace_modified = -not [string]::IsNullOrWhiteSpace((git status --short | Out-String))
    $Metadata | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "RUN_METADATA.json")

    $InventoryScript = Join-Path $ScriptDir "inventory_codex_stream.py"
    & $VenvPython $InventoryScript $StreamPath (Join-Path $Artifacts "CODEX_STREAM_INVENTORY.json")
    $InventoryExit = $LASTEXITCODE

    $FinalizerScript = Join-Path $ScriptDir "finalize_b2_codex_outcome.py"
    & $VenvPython $FinalizerScript $Artifacts
    $OutcomeExit = $LASTEXITCODE

    $Summary = [ordered]@{
        run_id = $RunId
        codex_version = $CodexVersion
        codex_exit_code = $CodexExit
        tests_before_exit_code = $TestsBeforeExit
        tests_after_exit_code = $TestsAfterExit
        workspace_modified = $Metadata.workspace_modified
        stream_inventory_exit_code = $InventoryExit
        deterministic_outcome_exit_code = $OutcomeExit
        requested_sandbox = "workspace-write"
        dangerous_full_access_used = $false
        benchmark_comparison_eligible = $false
        next_decision = $(if ($CodexExit -ne 0) { "DISCOVERY_RUNTIME_FAILURE" } elseif (-not $Metadata.workspace_modified) { "DISCOVERY_WRITE_PATH_UNCONFIRMED_OR_BLOCKED" } elseif ($OutcomeExit -ne 0) { "DISCOVERY_EXECUTED_BUT_TASK_INVALID" } else { "DISCOVERY_VALID_FOR_HARNESS_FREEZE_REVIEW" })
    }
    $Summary | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "CODEX_DISCOVERY_SUMMARY.json")

    Write-Host ""
    Write-Host "Codex B2 discovery complete: $RunId"
    Write-Host "Artifacts: $Artifacts"
    Write-Host "This run is discovery-only and is NOT a Codex baseline sample."
    Write-Host "No danger-full-access fallback was used."
    Write-Host ""
    Write-Host "CODEX_DISCOVERY_SUMMARY.json:"
    $Summary | ConvertTo-Json -Depth 8 | Write-Host
    Write-Host ""
    Write-Host "Send CODEX_DISCOVERY_SUMMARY.json and the printed stream inventory summary."
}
finally {
    Pop-Location
}
