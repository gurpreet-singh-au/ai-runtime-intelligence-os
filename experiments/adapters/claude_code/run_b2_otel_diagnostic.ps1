param(
    [string]$RunId = "B2-ATTR-001-otel-diagnostic-r01"
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
$SchemaRequirementsPath = Join-Path $ScriptDir "otel-schema-requirements.txt"
$ReceiverScript = Join-Path $ScriptDir "otel_b2_diagnostic_receiver.py"
$RunRoot = Join-Path $RepoRoot "experiments/local-runs/$RunId"
$Workspace = Join-Path $RunRoot "workspace"
$Artifacts = Join-Path $RunRoot "artifacts"
$Venv = Join-Path $RunRoot ".venv"
$VenvPython = Join-Path $Venv "Scripts/python.exe"
$DiagnosticPath = Join-Path $Artifacts "OTLP_B2_DIAGNOSTIC.json"
$ReceiverStdout = Join-Path $Artifacts "receiver-stdout.log"
$ReceiverStderr = Join-Path $Artifacts "receiver-stderr.log"
$StreamPath = Join-Path $Artifacts "claude-stream.jsonl"
$StderrPath = Join-Path $Artifacts "claude-stderr.log"

if (Test-Path $RunRoot) {
    throw "Run directory already exists: $RunRoot. Use a new RunId or archive/remove the prior local run."
}

New-Item -ItemType Directory -Force -Path $Workspace | Out-Null
New-Item -ItemType Directory -Force -Path $Artifacts | Out-Null
Copy-Item -Path (Join-Path $FixtureSource "*") -Destination $Workspace -Recurse -Force
Copy-Item -Path $PromptPath -Destination (Join-Path $Artifacts "TASK_PROMPT.md")

& py -3.11 -m venv $Venv
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $VenvPython)) {
    throw "Failed to create benchmark virtual environment at $Venv"
}
& $VenvPython -m pip install --disable-pip-version-check -q -r $RequirementsPath
if ($LASTEXITCODE -ne 0) { throw "Failed to install benchmark requirements" }
& $VenvPython -m pip install --disable-pip-version-check -q -r $SchemaRequirementsPath
if ($LASTEXITCODE -ne 0) { throw "Failed to install OTel schema requirements" }

$EnvNames = @(
    "CLAUDE_CODE_ENABLE_TELEMETRY",
    "CLAUDE_CODE_ENHANCED_TELEMETRY_BETA",
    "OTEL_EXPORTER_OTLP_PROTOCOL",
    "OTEL_EXPORTER_OTLP_ENDPOINT",
    "OTEL_METRICS_EXPORTER",
    "OTEL_LOGS_EXPORTER",
    "OTEL_TRACES_EXPORTER",
    "OTEL_METRIC_EXPORT_INTERVAL",
    "OTEL_LOGS_EXPORT_INTERVAL",
    "OTEL_TRACES_EXPORT_INTERVAL",
    "OTEL_LOG_USER_PROMPTS",
    "OTEL_LOG_TOOL_DETAILS",
    "OTEL_LOG_TOOL_CONTENT",
    "OTEL_LOG_RAW_API_BODIES"
)
$OriginalEnv = @{}
foreach ($Name in $EnvNames) {
    $OriginalEnv[$Name] = [Environment]::GetEnvironmentVariable($Name, "Process")
}
$OriginalPath = $env:PATH
$Receiver = $null

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
        experiment_id = "B2-ATTR-001"
        stage = "B2-otel-diagnostic"
        benchmark_id = "B2-001"
        policy_variant = "baseline-semantics-with-diagnostic-otel"
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
        claude_permission_mode = "acceptEdits"
        observation_mode = "stream-json-plus-native-otlp-privacy-safe-diagnostic"
        benchmark_comparison_eligible = $false
        raw_otlp_bodies_persisted = $false
        raw_prompt_response_context_persisted = $false
        note = "Single Stage B2 diagnostic run. Same frozen B2 task semantics and deterministic evaluator as Baseline v1. Not eligible for savings comparison until instrumentation overhead/equivalence is assessed."
    }
    $Metadata | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "RUN_METADATA.json")

    $TestsBeforeExit = Run-PytestCapture $VenvPython (Join-Path $Artifacts "tests-before.txt")

    $Receiver = Start-Process -FilePath $VenvPython `
        -ArgumentList @($ReceiverScript, "--host", "127.0.0.1", "--port", "4318", "--output", $DiagnosticPath) `
        -RedirectStandardOutput $ReceiverStdout `
        -RedirectStandardError $ReceiverStderr `
        -PassThru `
        -WindowStyle Hidden
    Start-Sleep -Seconds 1
    if ($Receiver.HasExited) {
        throw "OTLP diagnostic receiver exited early. Inspect $ReceiverStderr"
    }

    $env:CLAUDE_CODE_ENABLE_TELEMETRY = "1"
    $env:CLAUDE_CODE_ENHANCED_TELEMETRY_BETA = "1"
    $env:OTEL_EXPORTER_OTLP_PROTOCOL = "http/protobuf"
    $env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://127.0.0.1:4318"
    $env:OTEL_METRICS_EXPORTER = "otlp"
    $env:OTEL_LOGS_EXPORTER = "otlp"
    $env:OTEL_TRACES_EXPORTER = "otlp"
    $env:OTEL_METRIC_EXPORT_INTERVAL = "1000"
    $env:OTEL_LOGS_EXPORT_INTERVAL = "1000"
    $env:OTEL_TRACES_EXPORT_INTERVAL = "1000"
    $env:OTEL_LOG_USER_PROMPTS = "0"
    $env:OTEL_LOG_TOOL_DETAILS = "0"
    $env:OTEL_LOG_TOOL_CONTENT = "0"
    $env:OTEL_LOG_RAW_API_BODIES = "0"

    $env:PATH = (Join-Path $Venv "Scripts") + ";" + $OriginalPath
    $Prompt = Get-Content -Raw $PromptPath
    & claude -p $Prompt --permission-mode acceptEdits --output-format stream-json --verbose 1> $StreamPath 2> $StderrPath
    $ClaudeExit = $LASTEXITCODE

    Start-Sleep -Seconds 4
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
    $FinalizerScript = Join-Path $ScriptDir "finalize_b2_outcome.py"
    & $VenvPython $FinalizerScript $Artifacts
    $OutcomeExit = $LASTEXITCODE
}
finally {
    Pop-Location
    $env:PATH = $OriginalPath
    if ($Receiver -and -not $Receiver.HasExited) {
        Stop-Process -Id $Receiver.Id -Force -ErrorAction SilentlyContinue
        try { Wait-Process -Id $Receiver.Id -Timeout 3 -ErrorAction SilentlyContinue } catch {}
    }
    foreach ($Name in $EnvNames) {
        $Value = $OriginalEnv[$Name]
        if ($null -eq $Value) {
            Remove-Item "Env:$Name" -ErrorAction SilentlyContinue
        } else {
            [Environment]::SetEnvironmentVariable($Name, $Value, "Process")
        }
    }
}

Write-Host ""
Write-Host "Stage B2 diagnostic complete: $RunId"
Write-Host "Deterministic B2 outcome exit: $OutcomeExit"
Write-Host "Diagnostic summary: $DiagnosticPath"
Write-Host "This run is diagnostic-only and not eligible for baseline savings comparison."
if (Test-Path $DiagnosticPath) {
    Write-Host ""
    Write-Host "Privacy-safe diagnostic summary:"
    Get-Content -Raw $DiagnosticPath | Write-Host
}
