# Contributing

Chief of Staff accepts focused fixes that preserve the behavior contract,
privacy boundary, and portable parity.

## Before changing code

1. Open an issue for material behavior, policy, packaging, or configuration
   changes.
2. Keep private identities, project paths, client names and secrets out of the
   repository.
3. Do not edit historical release tags or assets.
4. Preserve existing project-specific rules when changing propagation logic.

## Development

Requirements:

- Python 3.11 or later;
- Node.js 18 or later;
- `python-docx` only when rebuilding the DOCX SOP.

Run:

```bash
python Test-Persona.py
python validate_install.py --example
python scripts/validate_repository.py
node tests/test_hooks.js
python scripts/build_release.py --output dist
```

On Windows, `py -3` can replace `python`.

## Pull requests

- Explain the user-visible result and risk.
- Include the smallest test that proves non-trivial logic.
- Update `CHANGELOG.md` for behavior or packaging changes.
- Keep the plugin manifest, `VERSION`, hooks, configuration example, and
  release builder on the same semantic version.
- Do not weaken persona requirements or replace deterministic checks with
  prose assurances. Computers are already talented enough at pretending.
