# Installation

Install one user-facing plugin. Chief includes the pinned content runtime.

## Requirements

- Git for marketplace installation;
- Node.js 18 or later for lifecycle-hook validation;
- Python 3.11 or later for configuration, content libraries, copy validation,
  and release checks.

## Codex and local ChatGPT Work

```powershell
codex plugin marketplace add plotdevice01/codex-chief-of-staff
codex plugin add chief-of-staff@codex-chief-of-staff
```

For a local checkout:

```powershell
.\install.ps1
```

On macOS or Linux:

```bash
./install.sh
```

Restart the ChatGPT desktop app. Start a fresh task in ChatGPT Work or Codex
and confirm `chief-of-staff@codex-chief-of-staff` is active with only the
`chief-of-staff` skill discoverable.

## ChatGPT Work

1. In workspace plugin controls, make Chief of Staff available to the required roles.
2. Open the Plugin Directory and install Chief of Staff.
3. Grant only the approved apps, files, and permissions.
4. Run the fresh-task acceptance prompts in ChatGPT Work.
5. Tell the team to open ChatGPT Work and ask Chief normally; no specialist selection is required.

Do not install AI Sloppy Copy, Brand Voice Factory, or Crafty Carousels for
ordinary team use. Their pinned runtime files are already inside Chief.

## Canonical source products

Chief is the team-facing install. These repositories remain the upstream
source and release boundaries used to update its pinned runtime:

- [Chief of Staff](https://github.com/plotdevice01/codex-chief-of-staff)
- [AI Sloppy Copy](https://github.com/plotdevice01/ai-sloppy-copy)
- [Brand Voice Factory](https://github.com/plotdevice01/brand-voice-factory)
- [Crafty Carousels](https://github.com/plotdevice01/crafty-carousels-skill)

## Configure

```powershell
python scripts/configure.py init --owner "Your Name" --timezone "Etc/UTC"
```

The initializer creates a private `chief-of-staff.json`. Connector authority
remains disabled until that file explicitly enables it.

## Verify

```powershell
python validate_install.py --example --strict-dependencies
python tests/test_content_runtime.py
python scripts/validate_repository.py
```

Expected installed state:

| Component | Delivery | Required state |
|---|---|---|
| Chief of Staff | Installed plugin | Active |
| AI Sloppy Copy `0.5.0` | Bundled runtime | Hash match |
| Brand Voice Factory `0.2.1` | Bundled runtime | Hash match |
| Crafty Carousels `0.6.1` | Bundled runtime | Hash match |
| Chief discoverable skills | `chief-of-staff` only | Exact |

The content test verifies the complete 751-hook database. It also verifies all
seven script frameworks, 39 CTAs, the voice and carousel scripts, and the final
AI Sloppy Copy checker.

## Upgrade

```powershell
codex plugin marketplace upgrade codex-chief-of-staff
codex plugin add chief-of-staff@codex-chief-of-staff
```

Restart the ChatGPT desktop app, then repeat fresh-task acceptance. A source-product
release does not change Chief until `scripts/sync_content_runtime.py` imports
the selected release and validation approves its new hashes.

## Uninstall

```powershell
codex plugin remove chief-of-staff@codex-chief-of-staff
codex plugin marketplace remove codex-chief-of-staff
```

Uninstalling does not delete the private configuration.

## Troubleshooting

- Missing content runtime: reinstall Chief and run
  `python tests/test_content_runtime.py`.
- Hooks do not load in Codex: restart the ChatGPT desktop app and start a fresh task.
- Wrong account: stop and reconnect the configured identity before reading.
- ChatGPT cannot run a required bundled script: keep the output at `Draft` and
  route the deterministic content operation through one approved remote MCP
  action.
