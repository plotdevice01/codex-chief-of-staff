<p align="center">
  <img src="assets/logo.svg" width="680" alt="Codex Chief of Staff">
</p>

<p align="center">
  <strong>Turn Codex or Claude Code into a scoped operating partner, not an enthusiastic tab-completion machine.</strong>
</p>

<p align="center">
  <a href="https://github.com/plotdevice01/codex-chief-of-staff/releases"><img src="https://img.shields.io/github/v/release/plotdevice01/codex-chief-of-staff" alt="Release"></a>
  <a href="https://github.com/plotdevice01/codex-chief-of-staff/actions/workflows/validate.yml"><img src="https://github.com/plotdevice01/codex-chief-of-staff/actions/workflows/validate.yml/badge.svg" alt="Validation"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2A9D8F" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Codex-plugin-14213D" alt="Codex plugin">
  <img src="https://img.shields.io/badge/Claude_Code-plugin-D97757" alt="Claude Code plugin">
</p>

Chief of Staff adds durable operating judgment to Codex and Claude Code:

- explicit project scope and source order;
- account identity checks before connector access;
- approval gates for drafts and external writes;
- project-wide `AGENTS.md` propagation without erasing local rules;
- 85% compression and `caveman` mode;
- a retained, traceable technical-assistant persona;
- Ponytail execution discipline and AI Sloppy Copy integration.

## What changed in v0.5.1

- Claude Code is now a first-class host with a validated marketplace manifest,
  shared lifecycle hooks, team settings, and one-command installers.
- The v0.5 operating contract remains intact: duplicated prompt weight was
  removed, complete workflows moved into the existing Chief skill, and full
  Ponytail behavior replaced the old partial copy.
- The retained persona is unchanged: all 97 traceable requirements, 85%
  compression, caveman mode, direct-reply humor, tone boundaries, account
  gates, approval controls, and project-rule preservation remain present.
- AI Sloppy Copy 2.2.5 includes the matching Claude marketplace and cross-host
  hooks plus Python 3.10 and 3.11 input parsing. The checker and evidence gates
  remain local and unchanged. Protected text and repair rules remain unchanged
  too.

| Capability | Codex | Claude Code |
|---|:---:|:---:|
| Marketplace installation | Yes | Yes |
| Session and subagent contract loading | Yes | Yes |
| Complete retained persona | Yes | Yes |
| Ponytail and AI Sloppy Copy stack | Yes | Yes |
| Local private configuration | Yes | Yes |
| Project-level team setup | `AGENTS.md` sync | `.claude/settings.json` |

## Install the complete stack

Use this order. Each plugin remains separate so it can update independently,
but all three are required for exact reference-install behavior.

Before starting, install [Git](https://git-scm.com/downloads),
[Node.js 18 or later](https://nodejs.org/en/download), and
[Python 3.11 or later](https://www.python.org/downloads/). Choose
[Codex](https://developers.openai.com/codex/) or
[Claude Code](https://code.claude.com/docs/en/setup).

### Codex

Run all six commands in order:

```powershell
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
codex plugin marketplace add plotdevice01/ai-sloppy-copy
codex plugin add ai-sloppy-copy@ai-sloppy-copy
codex plugin marketplace add plotdevice01/codex-chief-of-staff
codex plugin add chief-of-staff@codex-chief-of-staff
```

Then restart Codex, open `/hooks`, review all three plugins, and start a fresh
task. Run `codex plugin list --json` and confirm:
`ponytail@ponytail`, `ai-sloppy-copy@ai-sloppy-copy`, and
`chief-of-staff@codex-chief-of-staff`.

### Claude Code

Run all six commands in order:

```powershell
claude plugin marketplace add DietrichGebert/ponytail
claude plugin install ponytail@ponytail --scope user
claude plugin marketplace add plotdevice01/ai-sloppy-copy
claude plugin install ai-sloppy-copy@ai-sloppy-copy --scope user
claude plugin marketplace add plotdevice01/codex-chief-of-staff
claude plugin install chief-of-staff@codex-chief-of-staff --scope user
```

Then start Claude Code, run `/reload-plugins`, review `/hooks`, and start a
fresh session. Run `claude plugin list --json` and confirm the same three
plugin IDs.

See the [Claude Code deployment guide](docs/claude-code.md) for the one-command
installer, project and team scopes, shared settings plus update and removal.

### Configure and validate

In the fresh task or session, ask:

```text
Use the Chief of Staff skill to initialize my local configuration, then
validate the install. Report any missing plugin or hook.
```

Installation activates no connector or project access. Those remain off until
the local configuration explicitly turns them on.

## Configure

Start a fresh task or session and ask:

```text
Use the Chief of Staff skill to initialize my local configuration.
```

The initializer creates a private `chief-of-staff.json` in the platform
configuration directory. Connectors remain disabled and projects remain empty
until the user adds them.

For a source checkout:

```bash
python scripts/configure.py init --owner "Your Name" --timezone "Etc/UTC"
python validate_install.py --strict-dependencies
```

Windows users can use `py -3` instead of `python`.

See [installation](docs/installation.md) and
[configuration](docs/configuration.md) for the complete paths, upgrade,
uninstall, and recovery procedures.

## What changes

| Without Chief of Staff | With Chief of Staff |
|---|---|
| Work starts before scope is named | One scope is selected first |
| A connected account is assumed correct | Live identity must match configuration |
| Project instructions can overwrite each other | Shared and project rules remain separate |
| External writes inherit vague approval | Every write follows an explicit policy |
| Long answers bury the decision | The result leads; risks and the next action follow |
| Persona claims are prose | 97 requirements and eight scenarios are traceable |

## How it works

<p align="center">
  <img src="assets/architecture.svg" width="880" alt="Chief of Staff architecture">
</p>

The plugin is skills-only. It does not run a server or add connector access.
Shared Codex and Claude Code lifecycle hooks load the generic operating
contract and retained persona.
Private identities, scopes, paths, and approvals live in a local ignored
configuration.

Read the [architecture](docs/architecture.md) for configuration resolution and
hook behavior. It also covers trust boundaries and project propagation.

## Behavior example

<p align="center">
  <img src="assets/behavior-demo.svg" width="880" alt="Example Chief of Staff response">
</p>

The sarcasm applies to direct replies when useful. It does not leak into
client-facing, legal, medical, executive, or external communication unless the
user explicitly asks.

## Validate

```bash
python Test-Persona.py
python validate_install.py --example
python scripts/validate_repository.py
node tests/test_hooks.js
python tests/test_sync.py
python scripts/build_release.py --output dist
```

Static tests verify:

- 97 persona requirements and source hashes;
- communication and safety defaults;
- plugin, hook, skill, configuration, and release version parity;
- public-file privacy scanning;
- Codex and Claude Code hook output for sessions and subagents;
- deterministic release contents;
- complete Ponytail and AI Sloppy Copy companion capabilities under strict
  dependency validation.

The eight prompts in `persona/persona-contract.json` still require a fresh host
session. Static tests cannot grade live model behavior without becoming test
theater.

## Why three plugins

Chief of Staff contains the complete retained persona and response modes. It
also carries account gates and project routing. A compact fallback protects
minimum implementation discipline when Ponytail is unavailable.
[Ponytail](https://github.com/DietrichGebert/ponytail) adds persistent
efficiency modes and the complete implementation ladder. It also supplies
lifecycle hooks plus all six bundled skills.
[AI Sloppy Copy](https://github.com/plotdevice01/ai-sloppy-copy) adds authored
copy hooks and the deterministic local checker.

See [dependencies](docs/dependencies.md). No other repository or plugin is
required for the complete reference stack.

## Manual and offline installation

Download the latest release ZIP or clone the repository. For Codex, run:

PowerShell:

```powershell
.\install.ps1
```

macOS or Linux:

```bash
./install.sh
```

For Claude Code, run:

```powershell
.\install-claude.ps1
```

```bash
./install-claude.sh
```

Checksum verification is optional and documented under
[release verification](docs/installation.md#optional-release-verification).
The checksum remains available for users and environments that require it.

## Documentation

- [Installation and upgrades](docs/installation.md)
- [Claude Code deployment](docs/claude-code.md)
- [Configuration](docs/configuration.md)
- [Architecture](docs/architecture.md)
- [Testing](docs/testing.md)
- [Release process](docs/release-process.md)
- [Examples](examples/example-interactions.md)
- [Changelog](CHANGELOG.md)

## Security and privacy

Never commit `chief-of-staff.json`. The repository excludes it, release
automation scans for private values, and the plugin does not send telemetry.

Read [SECURITY.md](SECURITY.md) and [PRIVACY.md](PRIVACY.md).

## License

[MIT](LICENSE)
