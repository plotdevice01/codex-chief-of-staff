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
- fail-safe `AGENTS.md` loaders without erasing local rules;
- default ICM task contracts and automatic project architecture;
- 85% compression and `caveman` mode;
- a retained, traceable technical-assistant persona;
- Ponytail execution discipline and AI Sloppy Copy integration.

## What changed in v2.0.1

- Brand Voice Factory is now a standalone required plugin. Chief no longer
  bundles a duplicate `brand-voice-copywriter` skill.
- The complete-stack installers now install and update Ponytail, AI Sloppy
  Copy, Brand Voice Factory, Crafty Carousels, and Chief of Staff in order.
- Install validation now detects duplicate skill IDs and emits an install
  receipt with active versions, paths, manifest hashes, and skill ownership.
- Chief coordinates the approved Brand Voice package through Crafty's verified
  importer, then routes authored copy through AI Sloppy Copy before release.
- Chief now reports an execution trace that proves whether requested skills and
  plugins were materially used instead of merely loaded and name-dropped.

### Preserved from v1.0.0

- Every non-trivial task uses a compact ICM contract for scope, exact inputs,
  one job, relevant references, output, observable status, and human review.
- Every new project, workspace, or recurring process automatically invokes the
  bundled ICM Architect skill. Full folders appear only when persistent work
  needs them.
- Claude Code now enforces response contracts for analysis, debugging,
  contained changes, and ICM architecture. It allows two correction cycles,
  then stops with a documented recovery bypass.
- A pre-tool privacy check blocks configured project or connector values when
  the current prompt did not supply them.
- Restructure mode limits inventory reads and blocks mutation until approval.
  It requires reference checks plus content proof before a deletion proposal.
- The bundled Architect is pinned to `RinDig/icm-architect` commit `8f9cdf9`.
  It includes five workspace forms, ten invariants, both operating modes,
  Codex `AGENTS.md` routing, the cold walk, and Chief safety controls.
- The repository now carries Layer 1 routing and an ICM release pipeline.
  It also includes a conformance matrix and deterministic validation. Failure fixtures cover rejected paths.
- AI Sloppy Copy 0.5.0 with Standard 2.2.0 or later is required for full
  reference behavior.
- The retained persona stays unchanged at 97 requirements. The current
  integration contract has ten rules and thirteen live acceptance scenarios.
- The GitHub release, tag, ZIP, and both host manifests use `2.0.1`.

## Version numbers

These numbers describe different products or contracts. They are not competing
versions of the same file.

| Number | What it contains | What users install or cite |
|---|---|---|
| Chief of Staff `2.0.1` | This plugin, including its skills, hooks, documentation, and host manifests | Install or cite `2.0.1` |
| AI Sloppy Copy `0.5.0` | The separate companion plugin used for authored prose checks | Install `0.5.0` or later |
| AI Sloppy Copy Standard `2.2.0` | The writing-rules contract bundled inside AI Sloppy Copy | Cite the Standard when discussing rule behavior |
| Brand Voice Factory `0.2.1` | The canonical evidence-backed voice-package producer | Install `0.2.0` or later |
| Crafty Carousels `0.6.1` | The governed carousel producer and Brand Voice package importer | Install `0.6.0` or later |

Chief and AI Sloppy Copy now use the same three-part product version on their
GitHub release, tag, ZIP, and manifests. A manifest is host metadata inside a
release. It is not another product.

## v2.0.1 release evidence

The deterministic source suite passes. Fresh Sol Medium, Terra XHigh, Codex,
Claude Code, and installed-runtime acceptance passed for v2.0.1. Both Codex
profiles and Claude Code passed all 13 scenarios and 60/60 live assertions.

| Capability | Codex | Claude Code |
|---|:---:|:---:|
| Marketplace installation | Yes | Yes |
| Lifecycle contract loading | Yes | Yes |
| Chief response-contract enforcement | Host contract | Prompt and stop hooks |
| Complete retained persona | Yes | Yes |
| Default ICM task and project architecture | Yes | Yes |
| Ponytail and AI Sloppy Copy stack | Yes | Yes |
| Local private configuration | Yes | Yes |
| Project-level team setup | `AGENTS.md` sync | `.claude/settings.json` |

## Install the complete stack

Use this order. Each plugin remains separate so it can update independently,
and all five are required for exact reference-install behavior.

Before starting, install [Git](https://git-scm.com/downloads),
[Node.js 18 or later](https://nodejs.org/en/download), and
[Python 3.11 or later](https://www.python.org/downloads/). Choose
[Codex](https://developers.openai.com/codex/) or
[Claude Code](https://code.claude.com/docs/en/setup).

### Codex

Run all ten commands in order:

```powershell
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
codex plugin marketplace add plotdevice01/ai-sloppy-copy
codex plugin add ai-sloppy-copy@ai-sloppy-copy
codex plugin marketplace add plotdevice01/brand-voice-factory
codex plugin add brand-voice-factory@brand-voice-factory
codex plugin marketplace add plotdevice01/crafty-carousels-skill
codex plugin add crafty-carousels@crafty-carousels-skill
codex plugin marketplace add plotdevice01/codex-chief-of-staff
codex plugin add chief-of-staff@codex-chief-of-staff
```

Then restart Codex, open `/hooks`, review all five plugins, and start a fresh
task. Run `codex plugin list --json` and confirm:
`ponytail@ponytail`, `ai-sloppy-copy@ai-sloppy-copy`,
`brand-voice-factory@brand-voice-factory`,
`crafty-carousels@crafty-carousels-skill`, and
`chief-of-staff@codex-chief-of-staff`.

### Claude Code

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

Then start Claude Code, run `/reload-plugins`, review `/hooks`, and start a
fresh session. Run `claude plugin list --json` and confirm the same five
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
| Context and state are improvised per task | ICM names inputs, output, state and review |
| External writes inherit vague approval | Every write follows an explicit policy |
| Long answers bury the decision | The result leads; risks and the next action follow |
| Persona claims are prose | 97 requirements and thirteen scenarios are traceable |

## How it works

<p align="center">
  <img src="assets/architecture.svg" width="880" alt="Chief of Staff architecture">
</p>

The plugin is skills-only. It does not run a server or add connector access.
Shared Codex and Claude Code lifecycle hooks load the generic operating
contract and retained persona once. Codex omits duplicate contract injection
when its instruction chain already contains the canonical block. Claude Code
also uses prompt and stop hooks to reject architecture responses that omit the
required ICM header. Project loaders retain local rules and provide an explicit
fallback if a hook is absent.
Private identities, scopes, paths, and approvals live in a local ignored
configuration.

The shared contract applies the compact ICM task kernel by default. The bundled
ICM Architect skill handles project and workspace design through five forms.
It loads only the form reference and files needed for the current job.

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
python tests/test_icm.py
python tests/test_release.py
python tests/test_sync.py
python scripts/build_release.py --output dist
```

Static tests verify:

- 97 persona requirements and source hashes;
- ten integration rules and thirteen live acceptance definitions;
- five ICM forms and ten invariants, plus cold-walk failure behavior and token budgets;
- communication and safety defaults;
- plugin, hook, skill, configuration, and release version parity;
- public-file privacy scanning;
- Codex and Claude Code lifecycle hook output;
- ICM prompt classification and correction limits;
- recovery plus pre-tool and final-response privacy checks;
- deterministic release contents;
- complete companion capabilities under strict dependency validation for Ponytail;
  AI Sloppy Copy; Brand Voice Factory; and Crafty Carousels.

The thirteen prompts in `persona/persona-contract.json` still require a fresh host
session. Static tests cannot grade live model behavior without becoming test
theater.

## Why five plugins

Chief of Staff contains the complete retained persona and response modes. It
also carries account gates and project routing. A compact fallback protects
minimum implementation discipline when Ponytail is unavailable.
[Ponytail](https://github.com/DietrichGebert/ponytail) adds persistent
efficiency modes and the complete implementation ladder. It also supplies
lifecycle hooks plus all six bundled skills.
[AI Sloppy Copy](https://github.com/plotdevice01/ai-sloppy-copy) adds authored
copy hooks and the deterministic local checker.
[Brand Voice Factory](https://github.com/plotdevice01/brand-voice-factory) owns governed client voice packages and their sealed handoff contract.
[Crafty Carousels](https://github.com/plotdevice01/crafty-carousels-skill) imports that package and produces governed carousel runs.

See [dependencies](docs/dependencies.md) for ownership and minimum versions.

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
- [ICM conformance](docs/icm-conformance.md)
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
