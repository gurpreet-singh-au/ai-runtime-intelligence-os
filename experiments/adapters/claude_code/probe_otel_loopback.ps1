param(
    [string]$ProbeId = "B2-ATTR-001-otel-loopback-r01"
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
$ReceiverScript = Join-Path $ScriptDir "otel_loopback_receiver.py"
$RequestsPath = Join-Path $Artifacts "OTLP_REQUESTS.json"
$ReceiverStdout = Join-Path $Artifacts "receiver-stdout.log"
$ReceiverStderr = Join-Path $Artifacts "receiver-stderr.log"
$ClaudeStdout = Join-Path $Artifacts "claude-stdout.log"
$ClaudeStderr = Join-Path $Artifacts "claude-stderr.log"

if (Test-Path $ProbeRoot) {
    throw "Probe directory already exists: $ProbeRoot. Use a new ProbeId or remove/archive the previous local probe."
}

New-Item -ItemType Directory -Force -Path $Workspace | Out-Null
New-Item -ItemType Directory -Force -Path $Artifacts | Out-Null

$ClaudeVersion = (& claude --version 2>&1 | Out-String).Trim()
$StartedAt = [DateTimeOffset]::Now

$Metadata = [ordered]@{
    schema_version = "0.1"
    probe_id = $ProbeId
    experiment_id = "B2-ATTR-001"
    stage = "B1-otlp-transport-probe"
    started_at = $StartedAt.ToString("o")
    source_repository_commit = (git -C $RepoRoot rev-parse HEAD)
    runtime = "Claude Code"
    runtime_version = $ClaudeVersion
    observation_mode = "native-otel-http-loopback"
    benchmark_comparison_eligible = $false
    raw_api_bodies_enabled = $false
    request_bodies_persisted = $false
    endpoint = "http://127.0.0.1:4318"
    note = "Transport capability discovery only. Local receiver records method/path/content-type/encoding/body byte length and discards all request bodies."
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
    $Receiver = Start-Process -FilePath "py" `
        -ArgumentList @("-3.11", $ReceiverScript, "--host", "127.0.0.1", "--port", "4318", "--output", $RequestsPath) `
        -RedirectStandardOutput $ReceiverStdout `
        -RedirectStandardError $ReceiverStderr `
        -PassThru `
        -WindowStyle Hidden

    Start-Sleep -Seconds 1
    if ($Receiver.HasExited) {
        throw "Local OTLP receiver exited early. Inspect $ReceiverStderr"
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

    $Prompt = "Reply exactly: OTLP_LOOPBACK_OK. Do not use tools."
    & claude -p $Prompt --output-format stream-json --verbose 1> $ClaudeStdout 2> $ClaudeStderr
    $ClaudeExit = $LASTEXITCODE

    # Give periodic exporters a brief chance to flush before terminating receiver.
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

$Requests = @()
if (Test-Path $RequestsPath) {
    try {
        $Loaded = Get-Content -Raw $RequestsPath | ConvertFrom-Json
        if ($Loaded -is [System.Array]) { $Requests = @($Loaded) }
        elseif ($null -ne $Loaded) { $Requests = @($Loaded) }
    } catch {}
}

$PathCounts = @{}
foreach ($Request in $Requests) {
    $Path = [string]$Request.path
    if (-not $PathCounts.ContainsKey($Path)) { $PathCounts[$Path] = 0 }
    $PathCounts[$Path]++
}

$Summary = [ordered]@{
    probe_id = $ProbeId
    claude_version = $ClaudeVersion
    claude_exit_code = $ClaudeExit
    request_count = $Requests.Count
    request_paths = $PathCounts
    otlp_transport_observed = ($Requests.Count -gt 0)
    raw_bodies_persisted = $false
    decision = $(if ($Requests.Count -gt 0) { "OTLP_REQUESTS_OBSERVED" } else { "NO_OTLP_REQUESTS_OBSERVED" })
}
$Summary | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "OTLP_TRANSPORT_SUMMARY.json")
$Summary | ConvertTo-Json -Depth 8 | Write-Host

Write-Host ""
Write-Host "Stage B1 OTLP loopback probe complete."
Write-Host "Send OTLP_TRANSPORT_SUMMARY.json output only first."
