# Claude Code deployment

Chief of Staff v2.0.1 supports Claude Code with the same portable operating
contract, retained persona, response modes, project-rule preservation, and
companion stack used by the Codex release. Only host-specific manifests, hook
environment variables, and installation commands differ.

Claude Code discovers the standard `hooks/hooks.json` path automatically. The
Claude manifest must not redeclare that path or the host will report a duplicate
hook error.

## ICM response enforcement

Architecture prompts for a project, task, workspace, plan, or system activate
the ICM enforcement hook. `UserPromptSubmit` stores the current prompt and adds
the required seven-line response contract. `Stop` checks the completed answer
before Claude Code returns it.

The answer must begin with labeled values for ICM, Mode, Repeating unit,
Canonical form, Factory, Product, and Human gate. Mode must be `Build` or
`Restructure`. The canonical form must be one of the five bundled forms.

An invalid answer is returned to the model for correction. A second invalid
answer gets one final correction. The third invalid answer stops the response
and tells the user how to recover. This stays below Claude Code's host limit of
eight consecutive blocking stop-hook decisions.

For recovery only, set `CHIEF_ICM_ENFORCEMENT=off` before starting a new
session. Set it to `on` after repairing or updating the plugin. The hook fails
open when its state is missing or unreadable, so a damaged state file cannot
trap the host.

`PreToolUse` blocks a tool request that contains known private project or
connector context when the current prompt did not provide it. The stop check
applies the same rule to the completed response. Both report a generic scope
failure without repeating the private value.

Claude Code documents prompt input, pre-tool denial, stop response input, and
blocking decisions in its [hook reference](https://code.claude.com/docs/en/hooks).

## Requirements

Install:

- [Claude Code](https://code.claude.com/docs/en/setup);
- [Git](https://git-scm.com/downloads);
- [Node.js 18 or later](https://nodejs.org/en/download);
- [Python 3.11 or later](https://www.python.org/downloads/).

## Install the complete stack

Repositories:
[DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail),
[plotdevice01/ai-sloppy-copy](https://github.com/plotdevice01/ai-sloppy-copy),
[plotdevice01/brand-voice-factory](https://github.com/plotdevice01/brand-voice-factory),
[plotdevice01/crafty-carousels-skill](https://github.com/plotdevice01/crafty-carousels-skill),
and
[plotdevice01/codex-chief-of-staff](https://github.com/plotdevice01/codex-chief-of-staff).

Run these commands in order:

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

Then:

1. Start Claude Code.
2. Run `/reload-plugins`.
3. Open `/hooks` and review the hooks from all five plugins.
4. Run `claude plugin list --json` in a terminal.
5. Confirm `ponytail@ponytail`, `ai-sloppy-copy@ai-sloppy-copy`,
   `brand-voice-factory@brand-voice-factory`,
   `crafty-carousels@crafty-carousels-skill`, and
   `chief-of-staff@codex-chief-of-staff` are installed and active.
6. Start a fresh Claude Code session so `SessionStart` loads the complete
   contract and persona.

## One-command installer

From a repository checkout:

```powershell
.\install-claude.ps1
```

On macOS or Linux:

```bash
chmod +x ./install-claude.sh
./install-claude.sh
```

The default installation scope is `user`. Use `-Scope project` in PowerShell
or `./install-claude.sh project` to share activation through a project's
settings. Use `local` for an uncommitted per-project installation.

## Team deployment

Copy [the project settings example](../examples/claude-project-settings.json)
to `.claude/settings.json` in the target repository. Commit that settings file
only when the entire team should receive the marketplaces and active plugins.
Claude Code prompts each user to approve third-party marketplaces before
installation.

Private identities, paths, scopes, and approval rules still belong in the local
ignored `chief-of-staff.json`. Do not put them in shared Claude settings.

## Configure

In a fresh Claude Code session, ask:

```text
Use the Chief of Staff skill to initialize my local configuration, then
validate the install. Report any missing plugin or hook.
```

From a checkout:

```powershell
python scripts/configure.py init --owner "Your Name" --timezone "Etc/UTC"
python validate_install.py
```

`validate_install.py --strict-dependencies` checks the Codex plugin cache. On
Claude Code, use `claude plugin list --json` for installed companion
verification and run the repository tests below for portable behavior.

## Validate the deployment assets

```powershell
claude plugin validate .
node tests/test_hooks.js
python Test-Persona.py
python scripts/validate_repository.py
```

The hook test runs both host protocols. It verifies lifecycle context injection
from the same contract and persona files. It also tests ICM prompt activation
and valid completion. Separate checks cover the correction ceiling and recovery
bypass. Privacy cases check tool requests and completed responses.

## Update

If AI Sloppy Copy `2.2.6` is installed, uninstall it once before moving to
`0.5.0`.

```powershell
claude plugin uninstall ai-sloppy-copy@ai-sloppy-copy
claude plugin marketplace update ponytail
claude plugin marketplace update ai-sloppy-copy
claude plugin marketplace update brand-voice-factory
claude plugin marketplace update crafty-carousels-skill
claude plugin marketplace update codex-chief-of-staff
claude plugin update ponytail@ponytail
claude plugin update ai-sloppy-copy@ai-sloppy-copy
claude plugin update brand-voice-factory@brand-voice-factory
claude plugin update crafty-carousels@crafty-carousels-skill
claude plugin update chief-of-staff@codex-chief-of-staff
```

Run `/reload-plugins` and review changed hooks. Then start a fresh session.

## Remove

```powershell
claude plugin uninstall chief-of-staff@codex-chief-of-staff
claude plugin marketplace remove codex-chief-of-staff
```

This retains the local `chief-of-staff.json`. Remove that file separately only
when discarding the configuration is deliberate.

## Official Claude Code references

- [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)
- [Plugin specification](https://code.claude.com/docs/en/plugins-reference)
- [Hooks](https://code.claude.com/docs/en/hooks)
