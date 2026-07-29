<p align="center">
  <img src="assets/logo.svg" width="680" alt="Codex Chief of Staff">
</p>

<p align="center">
  <strong>Turn Codex into a scoped operating partner, not an enthusiastic tab-completion machine.</strong>
</p>

<p align="center">
  <a href="https://github.com/plotdevice01/codex-chief-of-staff/releases"><img src="https://img.shields.io/github/v/release/plotdevice01/codex-chief-of-staff" alt="Release"></a>
  <a href="https://github.com/plotdevice01/codex-chief-of-staff/actions/workflows/validate.yml"><img src="https://github.com/plotdevice01/codex-chief-of-staff/actions/workflows/validate.yml/badge.svg" alt="Validation"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2A9D8F" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Codex-plugin-14213D" alt="Codex plugin">
</p>

Chief of Staff adds durable operating judgment to Codex:

- explicit project scope and source order;
- account identity checks before connector access;
- approval gates for drafts and external writes;
- project-wide `AGENTS.md` propagation without erasing local rules;
- 85% compression and `caveman` mode;
- a retained, traceable technical-assistant persona;
- Ponytail execution discipline and AI Sloppy Copy integration.

## Install

```bash
codex plugin marketplace add plotdevice01/codex-chief-of-staff
codex plugin add chief-of-staff@codex-chief-of-staff
```

Restart Codex, open `/hooks`, review and trust the two Chief of Staff lifecycle
hooks, then start a new task. The hooks load the complete behavior contract at
session and subagent start.

Confirm installation:

```bash
codex plugin list --json
```

Installation activates no connector or project access.

## Configure

Start a task and ask:

```text
Use $chief-of-staff to initialize my local configuration.
```

The initializer creates a private `chief-of-staff.json` in the platform
configuration directory. Connectors remain disabled and projects remain empty
until the user adds them.

For a source checkout:

```bash
python scripts/configure.py init --owner "Your Name" --timezone "Etc/UTC"
python validate_install.py
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
| Long answers bury the decision | The result, risk, and next action lead |
| Persona claims are prose | 97 requirements and eight scenarios are traceable |

## How it works

<p align="center">
  <img src="assets/architecture.svg" width="880" alt="Chief of Staff architecture">
</p>

The plugin is skills-only. It does not run a server or add connector access.
Lifecycle hooks load the generic operating contract and retained persona.
Private identities, scopes, paths, and approvals live in a local ignored
configuration.

Read the [architecture](docs/architecture.md) for configuration resolution,
hook behavior, trust boundaries, and project propagation.

## Behavior example

<p align="center">
  <img src="assets/behavior-demo.svg" width="880" alt="Example Chief of Staff response">
</p>

The sarcasm applies to direct replies when useful. It does not leak into
client-facing, legal, medical, executive, or external communication unless the
user explicitly asks. Civilization survives another email.

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
- hook output for sessions and subagents;
- deterministic release contents.

The eight prompts in `persona/persona-contract.json` still require a fresh
Codex task. Static tests cannot grade live model behavior without becoming
test theater.

## Companion integrations

The plugin contains the full retained persona, 85% compression and caveman
rules. It also contains the core Ponytail ladder. Exact parity with the reference installation
also expects:

- Ponytail `4.8.4` or later;
- AI Sloppy Copy `2.1.0` or later.

See [dependencies](docs/dependencies.md). No other repository or plugin is
required.

## Manual and offline installation

Download the latest release ZIP or clone the repository, then run:

PowerShell:

```powershell
.\install.ps1
```

macOS or Linux:

```bash
./install.sh
```

Checksum verification is optional and documented under
[release verification](docs/installation.md#optional-release-verification).
The checksum stays available without making every user reenact a forensic lab.

## Documentation

- [Installation and upgrades](docs/installation.md)
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
