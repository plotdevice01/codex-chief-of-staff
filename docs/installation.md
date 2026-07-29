# Installation and upgrades

## Requirements

- Codex with plugin support;
- Git for GitHub-backed marketplace installation;
- Node.js 18 or later for lifecycle hooks;
- Python 3.11 or later for configuration and validation.

## Recommended installation

```bash
codex plugin marketplace add plotdevice01/codex-chief-of-staff
codex plugin add chief-of-staff@codex-chief-of-staff
```

Restart Codex. Open `/hooks`, review the `SessionStart` and `SubagentStart`
definitions, and trust them. Start a new task.

Verify:

```bash
codex plugin list --json
```

The installed entry should report:

- plugin: `chief-of-staff`;
- marketplace: `codex-chief-of-staff`;
- version: `0.4.4`;
- active state: `enabled: true`.

## Configure

Ask Codex:

```text
Use $chief-of-staff to initialize my local configuration.
```

Or run from a checkout:

```bash
python scripts/configure.py init --owner "Your Name" --timezone "Etc/UTC"
python validate_install.py
```

The initializer will not overwrite an existing file unless `--force` is
provided.

## Install from a checkout

```bash
git clone https://github.com/plotdevice01/codex-chief-of-staff.git
cd codex-chief-of-staff
```

PowerShell:

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

## Upgrade

```bash
codex plugin marketplace upgrade codex-chief-of-staff
codex plugin add chief-of-staff@codex-chief-of-staff
```

Restart Codex, review changed hooks, and start a new task. Existing local
configuration is not overwritten. If the configuration version changed, copy
your values into the new example structure and validate it.

Checkout installers also support:

```powershell
.\install.ps1 -Upgrade
```

```bash
./install.sh --upgrade
```

## Uninstall

```bash
codex plugin remove chief-of-staff@codex-chief-of-staff
codex plugin marketplace remove codex-chief-of-staff
```

The local configuration is intentionally retained. Delete it only when the
user explicitly wants their identities, paths and policies removed.

Checkout installers support `-Uninstall` or `--uninstall`.

## Optional release verification

GitHub publishes a SHA-256 digest for every release asset. A separate
`.sha256` file is also attached for offline or scripted verification.

PowerShell:

```powershell
(Get-FileHash .\codex-chief-of-staff-v0.4.4.zip -Algorithm SHA256).Hash
```

macOS or Linux:

```bash
sha256sum ./codex-chief-of-staff-v0.4.4.zip
```

Compare the result with `codex-chief-of-staff-v0.4.4.zip.sha256`.

## Recovery

1. Remove and reinstall the plugin.
2. Restart Codex and re-trust the current hooks.
3. Run `validate_install.py`.
4. Start a new task and run the eight persona scenarios.
5. Keep the prior release available until the new release passes.
