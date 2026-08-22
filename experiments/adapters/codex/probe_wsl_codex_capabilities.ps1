param(
    [string]$ProbeId = "CODEX-B2-C1-wsl-capability-r02"
)

$ErrorActionPreference = "Stop"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

Require-Command "wsl.exe"
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

# Discovery only. Do not install anything and do not copy credentials/config.
$RawDistros = & wsl.exe -l -q 2>&1
$ListExit = $LASTEXITCODE

# On some Windows/PowerShell combinations, wsl.exe -l -q arrives as strings with
# embedded NUL characters (for example U\0b\0u\0n\0t\0u). Removing only a trailing
# NUL leaves an invalid distro name and makes every subsequent `wsl -d` probe fail.
# Strip embedded NULs across the whole line before using the distro name.
$Distros = @(
    $RawDistros |
        ForEach-Object { ($_.ToString() -replace "`0", "").Trim() } |
        Where-Object { $_ }
)

$DistroReports = @()
foreach ($Distro in $Distros) {
    $Command = @'
set +e
printf 'user='; id -un 2>/dev/null
printf 'kernel='; uname -sr 2>/dev/null
printf 'cwd='; pwd 2>/dev/null
if command -v codex >/dev/null 2>&1; then
  echo 'codex_present=true'
  printf 'codex_path='; command -v codex
  printf 'codex_version='; codex --version 2>&1 | head -n 1
else
  echo 'codex_present=false'
fi
if command -v git >/dev/null 2>&1; then
  echo 'git_present=true'
  printf 'git_version='; git --version 2>&1 | head -n 1
else
  echo 'git_present=false'
fi
if command -v python3 >/dev/null 2>&1; then
  echo 'python3_present=true'
  printf 'python3_version='; python3 --version 2>&1 | head -n 1
else
  echo 'python3_present=false'
fi
# Existence only; never print auth/config contents.
if [ -d "$HOME/.codex" ]; then echo 'codex_home_present=true'; else echo 'codex_home_present=false'; fi
if [ -f "$HOME/.codex/auth.json" ]; then echo 'codex_auth_file_present=true'; else echo 'codex_auth_file_present=false'; fi
'@

    $Output = & wsl.exe -d $Distro -- bash -lc $Command 2>&1
    $Exit = $LASTEXITCODE
    $Lines = @($Output | ForEach-Object { ($_.ToString() -replace "`0", "") })
    $Values = [ordered]@{}
    foreach ($Line in $Lines) {
        $Index = $Line.IndexOf('=')
        if ($Index -gt 0) {
            $Key = $Line.Substring(0, $Index).Trim()
            $Value = $Line.Substring($Index + 1).Trim()
            if ($Key) { $Values[$Key] = $Value }
        }
    }

    $DistroReports += [ordered]@{
        distro = $Distro
        probe_exit_code = $Exit
        user = $Values['user']
        kernel = $Values['kernel']
        cwd = $Values['cwd']
        codex_present = $Values['codex_present'] -eq 'true'
        codex_path = $Values['codex_path']
        codex_version = $Values['codex_version']
        git_present = $Values['git_present'] -eq 'true'
        git_version = $Values['git_version']
        python3_present = $Values['python3_present'] -eq 'true'
        python3_version = $Values['python3_version']
        codex_home_present = $Values['codex_home_present'] -eq 'true'
        codex_auth_file_present = $Values['codex_auth_file_present'] -eq 'true'
    }
}

$EndedAt = [DateTimeOffset]::Now
$SuccessfulDistroProbes = @($DistroReports | Where-Object { $_.probe_exit_code -eq 0 })
$Summary = [ordered]@{
    probe_id = $ProbeId
    stage = "wsl-codex-capability-discovery"
    source_repository_commit = (git -C $RepoRoot rev-parse HEAD)
    started_at = $StartedAt.ToString("o")
    ended_at = $EndedAt.ToString("o")
    duration_ms = [int64](($EndedAt - $StartedAt).TotalMilliseconds)
    wsl_list_exit_code = $ListExit
    distro_count = $Distros.Count
    successful_distro_probe_count = $SuccessfulDistroProbes.Count
    distros = $DistroReports
    software_installed = $false
    credentials_copied = $false
    codex_agent_task_executed = $false
    benchmark_comparison_eligible = $false
    previous_probe_note = "r01 discovered two WSL distro entries but distro names contained embedded NUL characters, causing invalid `wsl -d` probes. Its WSL_PRESENT_CODEX_NOT_INSTALLED decision is not accepted as evidence about Codex availability."
    next_decision = $(
        if ($ListExit -ne 0 -or $Distros.Count -eq 0) { "NO_EXISTING_WSL_PATH" }
        elseif ($SuccessfulDistroProbes.Count -eq 0) { "WSL_LISTED_BUT_DISTRO_PROBES_FAILED" }
        elseif (@($SuccessfulDistroProbes | Where-Object { $_.codex_present -and $_.codex_auth_file_present }).Count -gt 0) { "EXISTING_WSL_CODEX_AUTH_PATH_FOUND_FOR_BOUNDED_WRITE_PROBE" }
        elseif (@($SuccessfulDistroProbes | Where-Object { $_.codex_present }).Count -gt 0) { "WSL_CODEX_PRESENT_AUTH_NOT_ESTABLISHED" }
        else { "WSL_PRESENT_CODEX_NOT_INSTALLED" }
    )
    note = "Read-only capability discovery. Does not install Codex, modify WSL, print auth contents, copy credentials, or execute an AI task."
}

$SummaryPath = Join-Path $Artifacts "CODEX_WSL_CAPABILITY_SUMMARY.json"
$Summary | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 $SummaryPath
$Summary | ConvertTo-Json -Depth 10 | Write-Host

Write-Host ""
Write-Host "WSL Codex capability discovery complete."
Write-Host "No software was installed, no credentials were copied, and no Codex agent task was executed."
Write-Host "Send the printed CODEX_WSL_CAPABILITY_SUMMARY.json output."
