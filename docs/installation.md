# Installation

Install one user-facing plugin. Chief includes the pinned content runtime.

## Teammates: four steps

After OpenAI approves and publishes Chief in the universal Plugins Directory:

1. Open ChatGPT and switch to **Work**.
2. Open **Plugins** and search for **Chief of Staff**.
3. Select **+** to install it.
4. Start a new chat and ask for the finished work normally.

No terminal or Git is required. Teammates do not need Python, plugin names, or
specialist selection. Do not install AI Sloppy Copy separately. Brand Voice
Factory and Crafty Carousels are also already inside Chief.

## Workspace admins

After the public listing is available:

1. Open **Workspace settings** and select **Plugins**.
2. Select **Chief of Staff**.
3. Set the installation policy to **Installed** for the required roles.
4. Start one low-risk test chat with a member account.
5. Tell the team to open a new Work chat and ask Chief normally.

Chief is skills-only in this release. Installing it does not grant connector,
project, file, or external-write authority. Configure those separately only
when the team actually needs them.

## Current publication status

Chief `2.1.1` is available from its GitHub-backed marketplace. Its universal
OpenAI Plugins Directory listing is not public yet. The publisher must submit
it and wait for OpenAI approval. After approval, the publisher must select
**Publish**. Until that happens, do not tell teammates that Chief is publicly
searchable.

## Admin and Codex fallback

This fallback is for administrators. Developers may also use it for direct
testing or an offline installation. It requires Git. Node.js 18 or later is
needed for hooks. Python 3.11 or later is needed for configuration validation.

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
