# Complete stack and dependencies

The reference installation uses five plugins. Each product has one job and one canonical skill owner.

## Install order

1. Ponytail `4.8.4` or later supplies implementation discipline.
2. AI Sloppy Copy `0.5.0` or later supplies authored-copy rules and the local checker.
3. Brand Voice Factory `0.2.0` or later owns `brand-voice-copywriter` and sealed voice packages.
4. Crafty Carousels `0.6.0` or later imports approved voice packages and produces carousel runs.
5. Chief of Staff coordinates scope, approvals, routing, status, and confirmed external handoffs.

## Codex

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

Repositories:

- [Ponytail](https://github.com/DietrichGebert/ponytail)
- [AI Sloppy Copy](https://github.com/plotdevice01/ai-sloppy-copy)
- [Brand Voice Factory](https://github.com/plotdevice01/brand-voice-factory)
- [Crafty Carousels](https://github.com/plotdevice01/crafty-carousels-skill)
- [Chief of Staff](https://github.com/plotdevice01/codex-chief-of-staff)

Restart Codex after installation. Start a fresh task so lifecycle context and skill discovery use the current versions.

## Claude Code

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

Run `/reload-plugins`, review `/hooks`, and start a fresh session.

## Verify

```powershell
python validate_install.py --doctor
python validate_install.py --strict-dependencies --receipt install-receipt.json
```

The doctor checks minimum versions and companion behavior. It also checks duplicate skill IDs across the selected plugin versions. The receipt records the active paths, versions, manifest hashes, and discovered skill IDs.

AI Sloppy Copy carries a separate Standard version for its writing-rules contract. The plugin version is the number users install. The Standard version changes when the writing contract changes.
