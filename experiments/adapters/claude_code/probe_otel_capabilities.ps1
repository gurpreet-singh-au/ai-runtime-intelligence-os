param(
    [string]$ProbeId = "B2-ATTR-001-otel-capability-probe-r01"
)

$ErrorActionPreference = "Stop"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

Require-Command "claude"
Require-Command "git"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "../../..")).Path
$ProbeRoot = Join-Path $RepoRoot "experiments/local-runs/$ProbeId"
$Workspace = Join-Path $ProbeRoot "workspace"
$Artifacts = Join-Path $ProbeRoot "artifacts"

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
    stage = "B1-capability-discovery"
    started_at = $StartedAt.ToString("o")
    source_repository_commit = (git -C $RepoRoot rev-parse HEAD)
    runtime = "Claude Code"
    runtime_version = $ClaudeVersion
    observation_mode = "native-otel-console-capability-probe"
    benchmark_comparison_eligible = $false
    raw_api_bodies_enabled = $false
    user_prompt_logging_enabled = $false
    tool_detail_logging_enabled = $false
    tool_content_logging_enabled = $false
    note = "Capability discovery only. Runs in an empty local workspace with a minimal no-tool prompt. Not part of B2 Baseline v1 and not eligible for savings comparison."
}
$Metadata | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 (Join-Path $Artifacts "PROBE_METADATA.json")

# Preserve any pre-existing values so this probe does not alter the user's shell after completion.
$Names = @(
    "CLAUDE_CODE_ENABLE_TELEMETRY",
    "CLAUDE_CODE_ENHANCED_TELEMETRY_BETA",
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
foreach ($Name in $Names) {
    $Original[$Name] = [Environment]::GetEnvironmentVariable($Name, "Process")
}

$StdoutPath = Join-Path $Artifacts "probe-stdout.log"
$StderrPath = Join-Path $Artifacts "probe-stderr.log"
$SummaryPath = Join-Path $Artifacts "CAPABILITY_SUMMARY.txt"

Push-Location $Workspace
try {
    $env:CLAUDE_CODE_ENABLE_TELEMETRY = "1"
    $env:CLAUDE_CODE_ENHANCED_TELEMETRY_BETA = "1"
    $env:OTEL_METRICS_EXPORTER = "console"
    $env:OTEL_LOGS_EXPORTER = "console"
    $env:OTEL_TRACES_EXPORTER = "console"
    $env:OTEL_METRIC_EXPORT_INTERVAL = "1000"
    $env:OTEL_LOGS_EXPORT_INTERVAL = "1000"
    $env:OTEL_TRACES_EXPORT_INTERVAL = "1000"

    # Privacy-first probe: do not emit prompt text, tool parameters/content, or raw API bodies.
    $env:OTEL_LOG_USER_PROMPTS = "0"
    $env:OTEL_LOG_TOOL_DETAILS = "0"
    $env:OTEL_LOG_TOOL_CONTENT = "0"
    $env:OTEL_LOG_RAW_API_BODIES = "0"

    $Prompt = "Reply exactly: OTEL_PROBE_OK. Do not use tools."
    & claude -p $Prompt --output-format stream-json --verbose 1> $StdoutPath 2> $StderrPath
    $ClaudeExit = $LASTEXITCODE
}
finally {
    Pop-Location
    foreach ($Name in $Names) {
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

# Produce a compact, privacy-conscious capability summary from both console streams.
$Patterns = @(
    "api_request",
    "api_error",
    "tool_result",
    "user_prompt",
    "session.id",
    "model",
    "input_token",
    "output_token",
    "cache",
    "cost",
    "duration",
    "latency",
    "trace",
    "span",
    "compaction",
    "context",
    "parent",
    "request"
)

$AllText = ""
if (Test-Path $StdoutPath) { $AllText += (Get-Content -Raw $StdoutPath) + "`n" }
if (Test-Path $StderrPath) { $AllText += (Get-Content -Raw $StderrPath) + "`n" }

$Summary = New-Object System.Collections.Generic.List[string]
$Summary.Add("Probe: $ProbeId")
$Summary.Add("Claude version: $ClaudeVersion")
$Summary.Add("Claude exit code: $ClaudeExit")
$Summary.Add("Raw API bodies: disabled")
$Summary.Add("Prompt/tool content logging: disabled")
$Summary.Add("")
$Summary.Add("Observed keyword counts (presence only; semantics not assumed):")
foreach ($Pattern in $Patterns) {
    $Count = ([regex]::Matches($AllText, [regex]::Escape($Pattern), [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)).Count
    $Summary.Add(("{0} = {1}" -f $Pattern, $Count))
}
$Summary.Add("")
$Summary.Add("Artifacts remain local under:")
$Summary.Add($Artifacts)
$Summary.Add("Do not commit probe stdout/stderr; review/redact before sharing raw telemetry.")

$Summary | Out-File -Encoding utf8 $SummaryPath
$Summary | ForEach-Object { Write-Host $_ }

Write-Host ""
Write-Host "Stage B1 OTel capability probe complete."
Write-Host "Send CAPABILITY_SUMMARY.txt first; inspect raw logs only if needed."
