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
$Dependencies = @(
    @{ Marketplace = "ponytail"; Repository = "DietrichGebert/ponytail"; Plugin = "ponytail@ponytail" },
    @{ Marketplace = "ai-sloppy-copy"; Repository = "plotdevice01/ai-sloppy-copy"; Plugin = "ai-sloppy-copy@ai-sloppy-copy" },
    @{ Marketplace = "brand-voice-factory"; Repository = "plotdevice01/brand-voice-factory"; Plugin = "brand-voice-factory@brand-voice-factory" },
    @{ Marketplace = "crafty-carousels-skill"; Repository = "plotdevice01/crafty-carousels-skill"; Plugin = "crafty-carousels@crafty-carousels-skill" }
)

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

if ($Upgrade) {
    foreach ($item in $Dependencies) {
        Invoke-ChiefCommand -Arguments @("plugin", "marketplace", "upgrade", $item.Marketplace)
        Invoke-ChiefCommand -Arguments @("plugin", "add", $item.Plugin)
    }
    Invoke-ChiefCommand -Arguments @("plugin", "marketplace", "upgrade", $Marketplace)
    Invoke-ChiefCommand -Arguments @("plugin", "add", $PluginId)
} else {
    foreach ($item in $Dependencies) {
        Invoke-ChiefCommand -Arguments @("plugin", "marketplace", "add", $item.Repository)
        Invoke-ChiefCommand -Arguments @("plugin", "add", $item.Plugin)
    }
    Invoke-ChiefCommand -Arguments @("plugin", "marketplace", "add", $RepoRoot)
    Invoke-ChiefCommand -Arguments @("plugin", "add", $PluginId)
}

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

Write-Host "Restart Codex, review and trust the Chief of Staff hooks, then start a new task."
