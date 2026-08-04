# 04_package

One job: compile the adopted voice into the full Brand Voice Package.

## Inputs

- Working: `../03_voice/output/voice-architecture.md`
- Working: `../03_voice/output/terminology-register.csv`
- Working: `../02_evidence/output/source-register.csv`
- Working: `../01_intake/output/owner-matrix.csv`
- Reference: `_shared/release-policy.md`

## Process

1. Build every component required by the skill package specification.
2. Label examples by status and use placeholders for unsupported facts.
3. Build the editable asset and release registers.
4. Run document checks and AI Sloppy Copy.

## Outputs

- `package/`
- `package-manifest.csv`
- `package-qa.json`

## Human check

The package owner adopts the exact package version. Asset-level public approval remains separate.
