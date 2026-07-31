# Claude Code deployment

Chief of Staff v0.6 supports Claude Code with the same portable operating
contract, retained persona, response modes, project-rule preservation, and
companion stack used by the Codex release. Only host-specific manifests, hook
environment variables, and installation commands differ.

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
and
[plotdevice01/codex-chief-of-staff](https://github.com/plotdevice01/codex-chief-of-staff).

Run these commands in order:

```powershell
claude plugin marketplace add DietrichGebert/ponytail
claude plugin install ponytail@ponytail --scope user
claude plugin marketplace add plotdevice01/ai-sloppy-copy
claude plugin install ai-sloppy-copy@ai-sloppy-copy --scope user
claude plugin marketplace add plotdevice01/codex-chief-of-staff
claude plugin install chief-of-staff@codex-chief-of-staff --scope user
```

Then:

1. Start Claude Code.
2. Run `/reload-plugins`.
3. Open `/hooks` and review the hooks from all three plugins.
4. Run `claude plugin list --json` in a terminal.
5. Confirm `ponytail@ponytail`, `ai-sloppy-copy@ai-sloppy-copy`, and
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

The hook test runs both host protocols. It verifies Codex JSON output and
Claude Code `SessionStart` and `SubagentStart` context injection from the same
contract and persona files.

## Update

If AI Sloppy Copy `2.2.6` is installed, uninstall it once before moving to
release `0.3`. Its required host manifest version is `0.3.0`.

```powershell
claude plugin uninstall ai-sloppy-copy@ai-sloppy-copy
claude plugin marketplace update ponytail
claude plugin marketplace update ai-sloppy-copy
claude plugin marketplace update codex-chief-of-staff
claude plugin update ponytail@ponytail
claude plugin update ai-sloppy-copy@ai-sloppy-copy
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
