# Installation

Install Chief of Staff from the GitHub repository. This project does not claim
an OpenAI review, approval, directory listing, or store distribution.

Chief is the only user-facing plugin in this package. AI Sloppy Copy, Brand
Voice Factory, and Crafty Carousels are already bundled as pinned runtime
dependencies.

## Requirements

- Git
- Codex with plugin support
- Node.js 18 or later for lifecycle hooks
- Python 3.11 or later for clean install staging, configuration, and validation

## Windows

```powershell
git clone https://github.com/plotdevice01/codex-chief-of-staff.git
Set-Location .\codex-chief-of-staff
.\install.ps1
```

The PowerShell installer removes the prior Chief cache, stages only canonical
repository files under `.install/codex-chief-of-staff`, registers that clean
repository-owned staging folder as the local Codex marketplace, installs
`chief-of-staff@codex-chief-of-staff`, and runs the configuration initializer.
The macOS and Linux installer applies the same clean-cache process.

Useful installer options:

```powershell
.\install.ps1 -DryRun
.\install.ps1 -SkipConfig
.\install.ps1 -Owner "Your Name" -Timezone "Etc/UTC"
```

## macOS or Linux

```bash
git clone https://github.com/plotdevice01/codex-chief-of-staff.git
cd codex-chief-of-staff
./install.sh
```

Useful installer options:

```bash
./install.sh --dry-run
./install.sh --skip-config
./install.sh --owner "Your Name" --timezone "Etc/UTC"
```

## Restart and verify

Restart Codex after installation. Review and trust the Chief hooks, then start
a fresh task. Existing tasks do not retroactively load startup context.

From the repository root, run:

```powershell
py -3 .\validate_install.py --example --strict-dependencies
py -3 .\tests\test_content_runtime.py
py -3 .\scripts\validate_repository.py
py -3 .\scripts\verify_installed_cache.py --require-only-current --require-plugin-state --receipt qa\installed-cache-v2.2.0.json --visual qa\installed-cache-v2.2.0.svg
```

On macOS or Linux, use `python3` and forward-slash paths.

Expected installed state:

| Component | Delivery | Required state |
|---|---|---|
| Chief of Staff | Repository installer | Active |
| AI Sloppy Copy `0.5.0` | Bundled runtime | Hash match |
| Brand Voice Factory `0.2.1` | Bundled runtime | Hash match |
| Crafty Carousels `0.6.1` | Bundled runtime | Hash match |
| Chief discoverable skills | `chief-of-staff` only | Exact |

The content test verifies the complete 751-hook database. It also verifies all
seven script frameworks, 39 CTAs, the voice and carousel scripts, and the final
AI Sloppy Copy checker.

Installation grants no connector credentials or project scope. Those remain
disabled until the private configuration explicitly enables them. Once the
configuration permits `plan_scoped` writes, a direct request or approved plan
authorizes every included action without repeated confirmation.

## Upgrade

Update the local checkout, then rerun its installer:

```powershell
git pull --ff-only
.\install.ps1 -Upgrade
```

On macOS or Linux:

```bash
git pull --ff-only
./install.sh --upgrade
```

Upgrade mode removes the exact prior Chief cache and rebuilds it from the
updated repository staging package. Restart Codex and repeat the fresh-task
verification. A source-product release
does not change Chief until `scripts/sync_content_runtime.py` imports the
selected release and validation approves its new hashes.

## Uninstall

Run the repository installer in uninstall mode:

```powershell
.\install.ps1 -Uninstall
```

On macOS or Linux:

```bash
./install.sh --uninstall
```

Uninstalling does not delete the private `chief-of-staff.json` configuration.

## Troubleshooting

- Missing content runtime: update the checkout, rerun the repository installer,
  and run `py -3 .\tests\test_content_runtime.py`.
- Hooks do not load: restart Codex, review the hooks, and start a fresh task.
- Stale Chief cache: rerun the repository installer with upgrade mode, then run
  `scripts/verify_installed_cache.py --require-only-current --require-plugin-state` and inspect its
  version, path, stale-version, missing-file, differing-file, and loader fields.
- Wrong account: stop and reconnect the configured identity before reading.
- Python unavailable: rerun the installer with configuration enabled after
  Python 3.11 or later is installed.

## Canonical repositories

- [Chief of Staff](https://github.com/plotdevice01/codex-chief-of-staff)
- [AI Sloppy Copy](https://github.com/plotdevice01/ai-sloppy-copy)
- [Brand Voice Factory](https://github.com/plotdevice01/brand-voice-factory)
- [Crafty Carousels](https://github.com/plotdevice01/crafty-carousels-skill)
