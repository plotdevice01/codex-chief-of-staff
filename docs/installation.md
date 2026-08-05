# Installation and upgrades

## Requirements

Install these first:

- [Codex](https://developers.openai.com/codex/) with plugin support or
  [Claude Code](https://code.claude.com/docs/en/setup);
- [Git](https://git-scm.com/downloads) for GitHub marketplace installation;
- [Node.js 18 or later](https://nodejs.org/en/download) for Ponytail and Chief
  of Staff lifecycle hooks;
- [Python 3.11 or later](https://www.python.org/downloads/) for AI Sloppy Copy,
  configuration, and validation.

After installing a requirement, close and reopen the terminal so its command is
available. Then install the plugins below in order.

## Codex installation

### 1. Install Ponytail

Open [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) if
you want to review the source.

```powershell
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

### 2. Install AI Sloppy Copy

Open [plotdevice01/ai-sloppy-copy](https://github.com/plotdevice01/ai-sloppy-copy)
if you want to review the source.

```powershell
codex plugin marketplace add plotdevice01/ai-sloppy-copy
codex plugin add ai-sloppy-copy@ai-sloppy-copy
```

### 3. Install Brand Voice Factory

```powershell
codex plugin marketplace add plotdevice01/brand-voice-factory
codex plugin add brand-voice-factory@brand-voice-factory
```

### 4. Install Crafty Carousels

```powershell
codex plugin marketplace add plotdevice01/crafty-carousels-skill
codex plugin add crafty-carousels@crafty-carousels-skill
```

### 5. Install Chief of Staff

Repository:
[plotdevice01/codex-chief-of-staff](https://github.com/plotdevice01/codex-chief-of-staff)

```powershell
codex plugin marketplace add plotdevice01/codex-chief-of-staff
codex plugin add chief-of-staff@codex-chief-of-staff
```

### 6. Restart and trust hooks

1. Restart the Codex desktop app, or start a new `codex` session.
2. Open `/hooks`.
3. Review and trust:
   - Ponytail: `SessionStart`, `SubagentStart`, and `UserPromptSubmit`;
   - AI Sloppy Copy: `UserPromptSubmit` and `Stop`;
   - Chief of Staff: `SessionStart` and `SubagentStart`.
4. Start a new Codex task. Existing tasks do not receive startup context
   retroactively.

### 7. Verify all five plugins

```powershell
codex plugin list --json
```

Confirm:

| Plugin | Marketplace | Minimum version | State |
|---|---|---:|---|
| `ponytail` | `ponytail` | `4.8.4` | active |
| `ai-sloppy-copy` | `ai-sloppy-copy` | `0.5.0` | active |
| `brand-voice-factory` | `brand-voice-factory` | `0.2.0` | active |
| `crafty-carousels` | `crafty-carousels-skill` | `0.6.0` | active |
| `chief-of-staff` | `codex-chief-of-staff` | `2.0.0` | active |

If any entry is absent, repeat only that plugin's two install commands, restart
Codex, and check again.

### 8. Configure and validate

In the new task, ask:

```text
Use $chief-of-staff to initialize my local configuration, then validate the
install with strict dependency checks. Report any missing plugin or hook.
```

The initializer does not overwrite an existing configuration without explicit
approval. Installation grants no connector access or external-write authority.
It does not authorize any project.

## Claude Code installation

The repositories are
[DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail),
[plotdevice01/ai-sloppy-copy](https://github.com/plotdevice01/ai-sloppy-copy),
[plotdevice01/brand-voice-factory](https://github.com/plotdevice01/brand-voice-factory),
[plotdevice01/crafty-carousels-skill](https://github.com/plotdevice01/crafty-carousels-skill),
and
[plotdevice01/codex-chief-of-staff](https://github.com/plotdevice01/codex-chief-of-staff).

Run all ten commands in order:

```powershell
claude plugin marketplace add DietrichGebert/ponytail
claude plugin install ponytail@ponytail --scope user
claude plugin marketplace add plotdevice01/ai-sloppy-copy
claude plugin install ai-sloppy-copy@ai-sloppy-copy --scope user
claude plugin marketplace add plotdevice01/brand-voice-factory
claude plugin install brand-voice-factory@brand-voice-factory --scope user
claude plugin marketplace add plotdevice01/crafty-carousels-skill
claude plugin install crafty-carousels@crafty-carousels-skill --scope user
claude plugin marketplace add plotdevice01/codex-chief-of-staff
claude plugin install chief-of-staff@codex-chief-of-staff --scope user
```

Start Claude Code, run `/reload-plugins`, review `/hooks`, and start a fresh
session. Confirm all five plugin IDs with:

```powershell
claude plugin list --json
```

The repository includes `install-claude.ps1`, `install-claude.sh`, and
`examples/claude-project-settings.json` for one-command and team deployment.
See the [complete Claude Code guide](claude-code.md).

## Install from a checkout

Use this route when you need to inspect the source or install offline. It also
exposes local validation scripts.

```powershell
git clone https://github.com/plotdevice01/codex-chief-of-staff.git
cd codex-chief-of-staff
```

Windows:

```powershell
.\install.ps1
```

macOS or Linux:

```bash
chmod +x ./install.sh
./install.sh
```

Preview without writing:

```powershell
.\install.ps1 -DryRun
```

```bash
./install.sh --dry-run
```

Configure and validate:

```powershell
python scripts/configure.py init --owner "Your Name" --timezone "Etc/UTC"
python validate_install.py --strict-dependencies
python Test-Persona.py
```

Windows users can use `py -3` instead of `python`.

## Upgrade the complete stack

If AI Sloppy Copy `2.2.6` is installed, remove it once before moving to
`0.5.0`. Semantic-version updaters sort `0.5.0` below `2.2.6`.

```powershell
codex plugin remove ai-sloppy-copy
codex plugin marketplace upgrade ponytail
codex plugin marketplace upgrade ai-sloppy-copy
codex plugin marketplace upgrade brand-voice-factory
codex plugin marketplace upgrade crafty-carousels-skill
codex plugin marketplace upgrade codex-chief-of-staff
codex plugin add ponytail@ponytail
codex plugin add ai-sloppy-copy@ai-sloppy-copy
codex plugin add brand-voice-factory@brand-voice-factory
codex plugin add crafty-carousels@crafty-carousels-skill
codex plugin add chief-of-staff@codex-chief-of-staff
```

Restart Codex and review changed hooks. Start a new task, then rerun strict
validation. Existing local configuration is not overwritten.

Checkout installers also support:

```powershell
.\install.ps1 -Upgrade
```

```bash
./install.sh --upgrade
```

## Uninstall

```powershell
codex plugin remove chief-of-staff
codex plugin marketplace remove codex-chief-of-staff
```

The local `chief-of-staff.json` is retained. Delete it only when you intend to
discard the entire configuration.

Checkout installers support `-Uninstall` or `--uninstall`.

## Optional release verification

GitHub publishes a SHA-256 digest for every release asset. A separate
`.sha256` file is also attached.

PowerShell:

```powershell
(Get-FileHash .\codex-chief-of-staff-v2.0.0.zip -Algorithm SHA256).Hash
```

macOS or Linux:

```bash
sha256sum ./codex-chief-of-staff-v2.0.0.zip
```

Compare the result with `codex-chief-of-staff-v2.0.0.zip.sha256`.

## Recovery

1. Repeat the ten install commands in the recommended order.
2. Restart Codex and re-trust the current hooks.
3. Run `codex plugin list --json`.
4. Run `validate_install.py --strict-dependencies` from a checkout, or ask the
   Chief of Staff skill to perform strict validation.
5. Start a new task and run the twelve persona scenarios.
6. Keep the prior release available until the new release passes.
