# Complete stack and dependencies

Exact reference-install behavior uses three public Codex plugins. Install them
in this order.

## 1. Ponytail 4.8.4 or later

- Repository: [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
- Latest release: [Ponytail releases](https://github.com/DietrichGebert/ponytail/releases/latest)
- Purpose: persistent implementation discipline, modes, lifecycle hooks, and
  review skills.

```powershell
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

## 2. AI Sloppy Copy plugin 2.2.3 or later

- Repository: [plotdevice01/ai-sloppy-copy](https://github.com/plotdevice01/ai-sloppy-copy)
- Latest release: [AI Sloppy Copy releases](https://github.com/plotdevice01/ai-sloppy-copy/releases/latest)
- Purpose: authored-copy rules, evidence and voice gates, lifecycle hooks, and
  deterministic local checking.
- Includes AI Sloppy Copy Standard 2.1.1 or later.

```powershell
codex plugin marketplace add plotdevice01/ai-sloppy-copy
codex plugin add ai-sloppy-copy@ai-sloppy-copy
```

## 3. Chief of Staff 0.5.0

- Repository: [plotdevice01/codex-chief-of-staff](https://github.com/plotdevice01/codex-chief-of-staff)
- Latest release: [Chief of Staff releases](https://github.com/plotdevice01/codex-chief-of-staff/releases/latest)
- Purpose: retained persona and response modes. It also supplies account gates
  and scope routing. Approval controls and project-rule preservation remain
  part of Chief of Staff.

```powershell
codex plugin marketplace add plotdevice01/codex-chief-of-staff
codex plugin add chief-of-staff@codex-chief-of-staff
```

Restart Codex after all six commands. Open `/hooks`, review and trust the hooks
from all three plugins, then start a new task.

Verify:

```powershell
codex plugin list --json
```

The list must show these active entries:

- `ponytail@ponytail`;
- `ai-sloppy-copy@ai-sloppy-copy`;
- `chief-of-staff@codex-chief-of-staff`.

From a Chief of Staff source checkout, run:

```powershell
python validate_install.py --strict-dependencies
```

Without `--strict-dependencies`, missing companion plugins are warnings. With
it, either missing companion fails validation. No other repository, runtime
service, MCP server, database, paid account, or connector is required.
