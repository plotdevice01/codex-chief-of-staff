# Codex Chief of Staff

Public release `v0.3.1`, issued July 29, 2026.

This release combines the Chief of Staff operating system with the complete
retained Technical Assistant Persona. It includes the 85% default response
mode, `caveman` mode for 100% minimization, Ponytail execution rules, and an
AI Sloppy Copy v2.1 requirement.

The persona was not summarized into a weaker profile. The package retains the
source PDF, verbatim substantive text, 97 traceable requirements, deterministic
checks, and eight fresh-task acceptance scenarios.

## Requirements

- A local Codex installation that can open a folder as a workspace.
- Python 3 for installation and persona validation.
- AI Sloppy Copy v2.1 or later from its companion package.
- Account access for any connector the user activates.

## Install

1. Download `Codex-Chief-of-Staff-v0.3.1.zip` and its `.sha256` file from the
   repository's Releases page.
2. Confirm the ZIP hash matches the published checksum.
3. Extract the ZIP into a user-owned folder.
4. Install AI Sloppy Copy v2.1 or later from its companion package.
5. Create the local configuration.

PowerShell:

```powershell
Copy-Item .\chief-of-staff.example.json .\chief-of-staff.json
```

macOS or Linux:

```bash
cp ./chief-of-staff.example.json ./chief-of-staff.json
```

6. Replace every `YOUR_` and `REPLACE_WITH_` value in
   `chief-of-staff.json`.
7. Keep `chief-of-staff.json` local. The included `.gitignore` excludes it.
8. Run both validators.

PowerShell:

```powershell
py -3 .\validate_install.py
py -3 .\Test-Persona.py
```

macOS or Linux:

```bash
python3 ./validate_install.py
python3 ./Test-Persona.py
```

9. Open the extracted folder as a Codex workspace and start a new task.
10. Ask Codex:

```text
Read AGENTS.md, persona/technical-assistant-persona.txt in full, and
chief-of-staff.json. State my configured scopes, active connectors, account
gates, approval policy, response modes, persona boundary, Ponytail rule, and AI
Sloppy Copy requirement. Do not access a connector.
```

Do not use connectors until the reported identities and policies match the
local configuration.

## Apply the Chief rules to registered projects

Add each project and local path to `chief-of-staff.json`. Existing project
`AGENTS.md` content is preserved as project-specific rules.

PowerShell:

```powershell
py -3 .\Sync-ProjectAgents.py --check
py -3 .\Sync-ProjectAgents.py --apply
```

macOS or Linux:

```bash
python3 ./Sync-ProjectAgents.py --check
python3 ./Sync-ProjectAgents.py --apply
```

Use `--include-global` only when the user deliberately wants the current
account-level Codex instructions updated too.

## Validation boundary

`Test-Persona.py` proves the source files, 97 persona requirements, Chief of
Staff integration rules, and behavior defaults are present. The eight scenario
prompts in `persona/persona-contract.json` must be run in a fresh Codex task to
confirm host-level behavior. A static file check cannot observe a model
response. Pretending otherwise would be test theater, which this persona has
already expressed opinions about.

## Package contents

- `AGENTS.md`: persona loading, response behavior, scope, account gates, and
  action policy.
- `chief-of-staff.example.json`: safe local configuration template.
- `persona/`: retained PDF and verbatim text. It also contains the requirement
  contract and live tests.
- `Test-Persona.py`: deterministic persona and behavior-default validator.
- `validate_install.py`: configuration, path, policy, and persona validator.
- `Sync-ProjectAgents.py`: account-wide project instruction check and approved propagation tool.
- `release-validation.json`: build-time validation result.
- `Codex Chief of Staff - Installation and SOP.docx`: complete setup and
  operating guide. It covers testing and recovery.
- `.gitignore`: excludes customized local configuration.

Never publish a customized `chief-of-staff.json`.
