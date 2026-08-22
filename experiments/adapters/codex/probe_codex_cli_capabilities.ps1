param(
    [string]$ProbeId = "CODEX-B2-C1-cli-capability-r01"
)

$ErrorActionPreference = "Stop"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

function Capture-Command([string]$FilePath, [string[]]$Arguments, [string]$OutputPath) {
    $Output = & $FilePath @Arguments 2>&1
    $ExitCode = $LASTEXITCODE
    @($Output) | Out-File -Encoding utf8 $OutputPath
    return [ordered]@{
        args = $Arguments
        exit_code = $ExitCode
        output_path = $OutputPath
    }
}

Require-Command "codex"
Require-Command "git"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "../../..")).Path
$ProbeRoot = Join-Path $RepoRoot "experiments/local-runs/$ProbeId"
$Artifacts = Join-Path $ProbeRoot "artifacts"

if (Test-Path $ProbeRoot) {
    throw "Probe directory already exists: $ProbeRoot. Use a new ProbeId or archive/remove the previous local probe."
}

New-Item -ItemType Directory -Force -Path $Artifacts | Out-Null

$StartedAt = [DateTimeOffset]::Now
$CodexCommand = (Get-Command codex).Source
$VersionPath = Join-Path $Artifacts "codex-version.txt"
$HelpPath = Join-Path $Artifacts "codex-help.txt"
$ExecHelpPath = Join-Path $Artifacts "codex-exec-help.txt"
$AppServerHelpPath = Join-Path $Artifacts "codex-app-server-help.txt"

$Version = Capture-Command $CodexCommand @("--version") $VersionPath
$TopHelp = Capture-Command $CodexCommand @("--help") $HelpPath

# Probe help surfaces only. No agent task is executed.
$ExecHelp = Capture-Command $CodexCommand @("exec", "--help") $ExecHelpPath
$AppServerHelp = Capture-Command $CodexCommand @("app-server", "--help") $AppServerHelpPath

function Read-Portable([string]$Path) {
    if (-not (Test-Path $Path)) { return "" }
    return Get-Content -Raw $Path
}

$All = @{
    top = Read-Portable $HelpPath
    exec = Read-Portable $ExecHelpPath
    app_server = Read-Portable $AppServerHelpPath
}

$Patterns = [ordered]@{
    exec_command = "exec"
    json = "--json"
    jsonl = "jsonl"
    sandbox = "--sandbox"
    approval = "approval"
    full_auto = "--full-auto"
    model = "--model"
    config = "--config"
    reasoning = "reasoning"
    output = "--output"
    output_last_message = "output-last-message"
    cwd = "--cd"
    workspace_write = "workspace-write"
    read_only = "read-only"
    danger_full_access = "danger-full-access"
    app_server = "app-server"
    generate_json_schema = "generate-json-schema"
}

$Presence = [ordered]@{}
foreach ($Name in $Patterns.Keys) {
    $Needle = [string]$Patterns[$Name]
    $Presence[$Name] = [ordered]@{
        top_help = $All.top.IndexOf($Needle, [System.StringComparison]::OrdinalIgnoreCase) -ge 0
        exec_help = $All.exec.IndexOf($Needle, [System.StringComparison]::OrdinalIgnoreCase) -ge 0
        app_server_help = $All.app_server.IndexOf($Needle, [System.StringComparison]::OrdinalIgnoreCase) -ge 0
    }
}

$VersionText = (Read-Portable $VersionPath).Trim()
$EndedAt = [DateTimeOffset]::Now

$Summary = [ordered]@{
    probe_id = $ProbeId
    stage = "codex-cli-capability-discovery"
    source_repository_commit = (git -C $RepoRoot rev-parse HEAD)
    started_at = $StartedAt.ToString("o")
    ended_at = $EndedAt.ToString("o")
    duration_ms = [int64](($EndedAt - $StartedAt).TotalMilliseconds)
    codex_command = $CodexCommand
    codex_version = $VersionText
    command_exit_codes = [ordered]@{
        version = $Version.exit_code
        top_help = $TopHelp.exit_code
        exec_help = $ExecHelp.exit_code
        app_server_help = $AppServerHelp.exit_code
    }
    capability_presence = $Presence
    agent_task_executed = $false
    network_probe_executed = $false
    benchmark_comparison_eligible = $false
    note = "Help/version discovery only. Raw help text remains local. Capability presence means the installed help surface contains the term; it is not yet proof of runtime semantics."
}

$SummaryPath = Join-Path $Artifacts "CODEX_CLI_CAPABILITY_SUMMARY.json"
$Summary | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 $SummaryPath
$Summary | ConvertTo-Json -Depth 8 | Write-Host

Write-Host ""
Write-Host "Codex CLI capability discovery complete."
Write-Host "No Codex agent task was executed."
Write-Host "Send CODEX_CLI_CAPABILITY_SUMMARY.json output first."
