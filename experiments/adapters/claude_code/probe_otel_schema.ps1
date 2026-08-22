param(
    [string]$ProbeId = "B2-ATTR-001-otel-schema-r01"
)

$ErrorActionPreference = "Stop"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

Require-Command "claude"
Require-Command "git"
Require-Command "py"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "../../..")).Path
$ProbeRoot = Join-Path $RepoRoot "experiments/local-runs/$ProbeId"
$Workspace = Join-Path $ProbeRoot "workspace"
$Artifacts = Join-Path $ProbeRoot "artifacts"
$Venv = Join-Path $ProbeRoot ".venv"
$VenvPython = Join-Path $Venv "Scripts/python.exe"
$Requirements = Join-Path $ScriptDir "otel-schema-requirements.txt"
$ReceiverScript = Join-Path $ScriptDir "otel_schema_receiver.py"
$SchemaPath = Join-Path $Artifacts "OTLP_SCHEMA_SUMMARY.json"
$ReceiverStdout = Join-Path $Artifacts "receiver-stdout.log"
$ReceiverStderr = Join-Path $Artifacts "receiver-stderr.log"
$ClaudeStdout = Join-Path $Artifacts "claude-stdout.log"
$ClaudeStderr = Join-Path $Artifacts "claude-stderr.log"

if (Test-Path $ProbeRoot) {
    throw "Probe directory already exists: $ProbeRoot. Use a new ProbeId or remove/archive the previous local probe."
}

New-Item -ItemType Directory -Force -Path $Workspace | Out-Null
New-Item -ItemType Directory -Force -Path $Artifacts | Out-Null

& py -3.11 -m venv $Venv
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $VenvPython)) {
    throw "Failed to create probe virtual environment at $Venv"
}
& $VenvPython -m pip install --disable-pip-version-check -q -r $Requirements
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install OTLP schema probe dependencies."
}

$ClaudeVersion = (& claude --version 2>&1 | Out-String).Trim()
$StartedAt = [DateTimeOffset]::Now

$Metadata = [ordered]@{
    schema_version = "0.1"
    probe_id = $ProbeId
    experiment_id = "B2-ATTR-001"
    stage = "B1-privacy-safe-otlp-schema-discovery"
    started_at = $StartedAt.ToString("o")
    source_repository_commit = (git -C $RepoRoot rev-parse HEAD)
    runtime = "Claude Code"
    runtime_version = $ClaudeVersion
    observation_mode = "native-otel-http-protobuf-schema-only"
    benchmark_comparison_eligible = $false
    raw_api_bodies_enabled = $false
    raw_otlp_bodies_persisted = $false
    arbitrary_attribute_values_persisted = $false
    prompt_logging_enabled = $false
    tool_detail_logging_enabled = $false
    tool_content_logging_enabled = $false
    endpoint = "http://127.0.0.1:4318"
    note = "Schema discovery only. Receiver parses OTLP protobuf in memory and persists structural names/attribute keys only; raw bodies and arbitrary values are discarded."
}
$Metadata | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "PROBE_METADATA.json")

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
$Original = @{}
foreach ($Name in $EnvNames) {
    $Original[$Name] = [Environment]::GetEnvironmentVariable($Name, "Process")
}

$Receiver = $null
Push-Location $Workspace
try {
    $Receiver = Start-Process -FilePath $VenvPython `
        -ArgumentList @($ReceiverScript, "--host", "127.0.0.1", "--port", "4318", "--output", $SchemaPath) `
        -RedirectStandardOutput $ReceiverStdout `
        -RedirectStandardError $ReceiverStderr `
        -PassThru `
        -WindowStyle Hidden

    Start-Sleep -Seconds 1
    if ($Receiver.HasExited) {
        throw "Privacy-safe OTLP schema receiver exited early. Inspect $ReceiverStderr"
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

    # Keep all content-bearing optional telemetry disabled. The receiver also discards
    # arbitrary values even if the runtime emits them through ordinary structural events.
    $env:OTEL_LOG_USER_PROMPTS = "0"
    $env:OTEL_LOG_TOOL_DETAILS = "0"
    $env:OTEL_LOG_TOOL_CONTENT = "0"
    $env:OTEL_LOG_RAW_API_BODIES = "0"

    $Prompt = "Reply exactly: OTEL_SCHEMA_OK. Do not use tools."
    & claude -p $Prompt --output-format stream-json --verbose 1> $ClaudeStdout 2> $ClaudeStderr
    $ClaudeExit = $LASTEXITCODE

    Start-Sleep -Seconds 4
}
finally {
    Pop-Location
    if ($Receiver -and -not $Receiver.HasExited) {
        Stop-Process -Id $Receiver.Id -Force -ErrorAction SilentlyContinue
        try { Wait-Process -Id $Receiver.Id -Timeout 3 -ErrorAction SilentlyContinue } catch {}
    }
    foreach ($Name in $EnvNames) {
        $Value = $Original[$Name]
        if ($null -eq $Value) {
            Remove-Item "Env:$Name" -ErrorAction SilentlyContinue
        } else {
            [Environment]::SetEnvironmentVariable($Name, $Value, "Process")
        }
    }
}

$EndedAt = [DateTimeOffset]::Now
$Metadata.ended_at = $EndedAt.ToString("o")
$Metadata.duration_ms = [int64](($EndedAt - $StartedAt).TotalMilliseconds)
$Metadata.claude_exit_code = $ClaudeExit
$Metadata | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "PROBE_METADATA.json")

if (-not (Test-Path $SchemaPath)) {
    throw "No OTLP schema summary was produced. Inspect receiver stderr at $ReceiverStderr"
}

$Schema = Get-Content -Raw $SchemaPath | ConvertFrom-Json
$Summary = [ordered]@{
    probe_id = $ProbeId
    claude_version = $ClaudeVersion
    claude_exit_code = $ClaudeExit
    request_count = $Schema.transport.request_count
    request_paths = $Schema.transport.request_paths
    parse_errors_by_path = $Schema.transport.parse_errors_by_path
    metric_names = $Schema.metrics.metric_names
    metric_datapoint_attribute_keys = $Schema.metrics.datapoint_attribute_keys
    log_event_names = $Schema.logs.safe_event_names
    log_attribute_keys = $Schema.logs.log_attribute_keys
    log_trace_linkage_present = $Schema.logs.trace_linkage_present
    span_names = $Schema.traces.safe_span_names
    span_attribute_keys = $Schema.traces.span_attribute_keys
    trace_parent_linkage_present = $Schema.traces.parent_linkage_present
    raw_bodies_persisted = $false
    arbitrary_attribute_values_persisted = $false
}

$Summary | ConvertTo-Json -Depth 12 | Out-File -Encoding utf8 (Join-Path $Artifacts "OTLP_SCHEMA_CONSOLE_SUMMARY.json")
$Summary | ConvertTo-Json -Depth 12 | Write-Host

Write-Host ""
Write-Host "Stage B1 privacy-safe OTLP schema discovery complete."
Write-Host "Send OTLP_SCHEMA_CONSOLE_SUMMARY.json output only."
