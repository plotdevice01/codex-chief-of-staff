[CmdletBinding()]
param(
    [ValidateSet("user", "project", "local")]
    [string]$Scope = "user"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    throw "Claude Code is not installed or is not on PATH. Install it, reopen PowerShell, and run this script again."
}

$stack = @(
    @{ Marketplace = "ponytail"; Repository = "DietrichGebert/ponytail"; Plugin = "ponytail@ponytail" },
    @{ Marketplace = "ai-sloppy-copy"; Repository = "plotdevice01/ai-sloppy-copy"; Plugin = "ai-sloppy-copy@ai-sloppy-copy"; ResetFrom = "2.2.6" },
    @{ Marketplace = "brand-voice-factory"; Repository = "plotdevice01/brand-voice-factory"; Plugin = "brand-voice-factory@brand-voice-factory" },
    @{ Marketplace = "crafty-carousels-skill"; Repository = "plotdevice01/crafty-carousels-skill"; Plugin = "crafty-carousels@crafty-carousels-skill" },
    @{ Marketplace = "codex-chief-of-staff"; Repository = "plotdevice01/codex-chief-of-staff"; Plugin = "chief-of-staff@codex-chief-of-staff" }
)

$marketplaces = (& claude plugin marketplace list --json 2>$null) -join "`n"
$installed = (& claude plugin list --json 2>$null) -join "`n"

foreach ($item in $stack) {
    $forceInstall = $false
    if (
        $item.ResetFrom -and
        $installed -match [regex]::Escape($item.Plugin) -and
        $installed -match ('"version"\s*:\s*"' + [regex]::Escape($item.ResetFrom) + '"')
    ) {
        & claude plugin uninstall $item.Plugin
        if ($LASTEXITCODE -ne 0) {
            throw "Claude Code could not remove $($item.Plugin) for its numbering reset."
        }
        $forceInstall = $true
    }

    if ($marketplaces -match [regex]::Escape('"' + $item.Marketplace + '"')) {
        & claude plugin marketplace update $item.Marketplace
    } else {
        & claude plugin marketplace add $item.Repository
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Code could not configure marketplace $($item.Marketplace)."
    }

    if (-not $forceInstall -and $installed -match [regex]::Escape($item.Plugin)) {
        & claude plugin update $item.Plugin
    } else {
        & claude plugin install $item.Plugin --scope $Scope
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Code could not install $($item.Plugin)."
    }
}

& claude plugin list --json
if ($LASTEXITCODE -ne 0) {
    throw "Claude Code installed the stack but could not read it back."
}

Write-Host "PASS: Chief of Staff stack installed for Claude Code at scope '$Scope'."
Write-Host "Next: start Claude Code, run /reload-plugins, review /hooks, then start a fresh session."
