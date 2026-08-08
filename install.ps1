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
$CodexHomePath = if ($env:CODEX_HOME) {
    [System.IO.Path]::GetFullPath($env:CODEX_HOME)
} else {
    Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex'
}
$InstallSource = Join-Path $RepoRoot '.install\codex-chief-of-staff'
$CacheRoot = Join-Path $CodexHomePath 'plugins\cache\codex-chief-of-staff\chief-of-staff'

function Resolve-CodexCli {
    $localBin = Join-Path $env:LOCALAPPDATA 'OpenAI\Codex\bin'
    $localCli = Get-ChildItem -LiteralPath $localBin -Filter codex.exe -Recurse -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if ($localCli) {
        return $localCli.FullName
    }
    $command = Get-Command codex -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }
    throw 'Codex CLI was not found. Install or update the Codex desktop app.'
}

function Remove-ChiefPath {
    param([string]$Target, [string]$Expected)
    $resolvedTarget = [System.IO.Path]::GetFullPath($Target)
    $resolvedExpected = [System.IO.Path]::GetFullPath($Expected)
    if ($resolvedTarget -ne $resolvedExpected) {
        throw "Refusing to remove unexpected path: $resolvedTarget"
    }
    if (Test-Path -LiteralPath $resolvedTarget) {
        Write-Host "REMOVE $resolvedTarget"
        if (-not $DryRun) {
            Remove-Item -LiteralPath $resolvedTarget -Recurse -Force
        }
    }
}

$CodexCli = Resolve-CodexCli

function Invoke-ChiefCommand {
    param([string[]]$Arguments, [switch]$AllowFailure)
    Write-Host ($CodexCli + " " + ($Arguments -join " "))
    if ($DryRun) {
        return
    }
    & $CodexCli @Arguments
    if ($LASTEXITCODE -ne 0 -and -not $AllowFailure) {
        throw "Command failed with exit code $LASTEXITCODE."
    }
}

function Resolve-Python {
    $python = Get-Command py -ErrorAction SilentlyContinue
    if ($python) {
        return @($python.Source, '-3')
    }
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        return @($python.Source)
    }
    throw 'Python 3 is required to stage the repository-owned install package.'
}

if ($Uninstall) {
    Invoke-ChiefCommand -Arguments @("plugin", "remove", $PluginId) -AllowFailure
    Invoke-ChiefCommand -Arguments @("plugin", "marketplace", "remove", $Marketplace) -AllowFailure
    Remove-ChiefPath -Target $CacheRoot -Expected $CacheRoot
    Remove-ChiefPath -Target $InstallSource -Expected $InstallSource
    Write-Host "Chief of Staff and its cache removed. Local configuration retained."
    exit 0
}

$pythonCommand = Resolve-Python
Invoke-ChiefCommand -Arguments @("plugin", "remove", $PluginId) -AllowFailure
Invoke-ChiefCommand -Arguments @("plugin", "marketplace", "remove", $Marketplace) -AllowFailure
Remove-ChiefPath -Target $CacheRoot -Expected $CacheRoot
Remove-ChiefPath -Target $InstallSource -Expected $InstallSource

$stageArguments = @()
if ($pythonCommand.Count -gt 1) {
    $stageArguments += $pythonCommand[1]
}
$stageArguments += @((Join-Path $RepoRoot 'scripts\stage_install.py'), '--output', $InstallSource)
Write-Host ($pythonCommand[0] + " " + ($stageArguments -join " "))
if (-not $DryRun) {
    & $pythonCommand[0] @stageArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Clean install staging failed with exit code $LASTEXITCODE."
    }
}

Invoke-ChiefCommand -Arguments @("plugin", "marketplace", "add", $InstallSource)
Invoke-ChiefCommand -Arguments @("plugin", "add", $PluginId)

if (-not $SkipConfig) {
    $ConfigArgs = @()
    if ($pythonCommand.Count -gt 1) {
        $ConfigArgs += $pythonCommand[1]
    }
    $ConfigArgs += @(
            (Join-Path $RepoRoot "scripts\configure.py"),
            "init",
            "--owner",
            $Owner,
            "--timezone",
            $Timezone
        )
    Write-Host ($pythonCommand[0] + " " + ($ConfigArgs -join " "))
    if (-not $DryRun) {
        & $pythonCommand[0] @ConfigArgs
        if ($LASTEXITCODE -notin @(0, 2)) {
            throw "Configuration initialization failed with exit code $LASTEXITCODE."
        }
    }
}

Write-Host "Chief of Staff installed from a clean repository-owned staging package. Old Chief cache removed."
Write-Host "Restart Codex, review and trust the Chief of Staff hooks, then start a new task. All internal workflows are bundled."
