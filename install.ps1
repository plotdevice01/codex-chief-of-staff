[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$Upgrade,
    [switch]$Uninstall,
    [switch]$SkipConfig,
    [string]$Owner = "Your Name",
    [string]$Timezone = "Etc/UTC"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PluginId = "chief-of-staff@codex-chief-of-staff"
$Marketplace = "codex-chief-of-staff"

function Invoke-ChiefCommand {
    param([string[]]$Arguments)
    Write-Host ("codex " + ($Arguments -join " "))
    if ($DryRun) {
        return
    }
    & codex @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE."
    }
}

if ($Uninstall) {
    Invoke-ChiefCommand -Arguments @("plugin", "remove", $PluginId)
    Invoke-ChiefCommand -Arguments @("plugin", "marketplace", "remove", $Marketplace)
    Write-Host "Chief of Staff removed. Local configuration retained."
    exit 0
}

Invoke-ChiefCommand -Arguments @("plugin", "marketplace", "add", $RepoRoot)
Invoke-ChiefCommand -Arguments @("plugin", "add", $PluginId)

if (-not $SkipConfig) {
    $Python = Get-Command py -ErrorAction SilentlyContinue
    $PythonArgs = @("-3")
    if (-not $Python) {
        $Python = Get-Command python -ErrorAction SilentlyContinue
        $PythonArgs = @()
    }
    if ($Python) {
        $ConfigArgs = $PythonArgs + @(
            (Join-Path $RepoRoot "scripts\configure.py"),
            "init",
            "--owner",
            $Owner,
            "--timezone",
            $Timezone
        )
        Write-Host ($Python.Source + " " + ($ConfigArgs -join " "))
        if (-not $DryRun) {
            & $Python.Source @ConfigArgs
            if ($LASTEXITCODE -notin @(0, 2)) {
                throw "Configuration initialization failed with exit code $LASTEXITCODE."
            }
        }
    } else {
        Write-Warning "Python was not found. Plugin installed; configuration was not initialized."
    }
}

Write-Host "Restart Codex, review and trust the Chief of Staff hooks, then start a new task. All internal workflows are bundled."
