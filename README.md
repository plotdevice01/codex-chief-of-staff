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

## Install the complete stack

Use this order. Each plugin remains separate so it can update independently,
but all three are required for exact reference-install behavior.

Before starting, install
[Git](https://git-scm.com/downloads),
[Node.js 18 or later](https://nodejs.org/en/download), and
[Python 3.11 or later](https://www.python.org/downloads/). You also need
[Codex](https://developers.openai.com/codex/) with plugin support.

### 1. Install Ponytail

Repository: [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)

```powershell
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

### 2. Install AI Sloppy Copy

Repository: [plotdevice01/ai-sloppy-copy](https://github.com/plotdevice01/ai-sloppy-copy)

```powershell
codex plugin marketplace add plotdevice01/ai-sloppy-copy
codex plugin add ai-sloppy-copy@ai-sloppy-copy
```

### 3. Install Chief of Staff

Repository: [plotdevice01/codex-chief-of-staff](https://github.com/plotdevice01/codex-chief-of-staff)

```powershell
codex plugin marketplace add plotdevice01/codex-chief-of-staff
codex plugin add chief-of-staff@codex-chief-of-staff
```

### 4. Restart, trust, and verify

1. Restart Codex.
2. Open `/hooks`.
3. Review and trust the hooks offered by Ponytail, AI Sloppy Copy, and Chief of
   Staff.
4. Start a new task.
5. Run `codex plugin list --json`.
6. Confirm these entries are installed and active:
   `ponytail@ponytail`, `ai-sloppy-copy@ai-sloppy-copy`, and
   `chief-of-staff@codex-chief-of-staff`.

### 5. Configure and validate

In the new task, ask:

```text
Use $chief-of-staff to initialize my local configuration, then validate the
install with strict dependency checks. Report any missing plugin or hook.
```

Installation activates no connector or project access. Those remain off until
the local configuration explicitly turns them on.

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
Lifecycle hooks load the generic operating contract and retained persona.
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
- hook output for sessions and subagents;
- deterministic release contents.

The eight prompts in `persona/persona-contract.json` still require a fresh
Codex task. Static tests cannot grade live model behavior without becoming
test theater.

## Why three plugins

Chief of Staff contains the complete retained persona and response modes. It
also carries account gates and project routing. The core Ponytail ladder
remains included.
[Ponytail](https://github.com/DietrichGebert/ponytail) adds persistent
efficiency modes and lifecycle hooks. It also adds review skills.
[AI Sloppy Copy](https://github.com/plotdevice01/ai-sloppy-copy) adds authored
copy hooks and the deterministic local checker.

See [dependencies](docs/dependencies.md). No other repository or plugin is
required for the complete reference stack.

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
The checksum remains available for users and environments that require it.

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
