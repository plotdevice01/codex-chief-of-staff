# 02_build - build candidate archive

One job: produce the deterministic candidate from approved source.

## Inputs

- Working: repository source approved in `../01_prepare/CONTEXT.md`.
- Reference: `../../../scripts/build_release.py`.

Do NOT load private local configuration or existing public release assets.

## Process

1. Build the SOP from its source generator.
2. Stage the complete public file set.
3. Write the ZIP, checksum, and embedded validation manifest.

## Outputs

- `../../../dist/codex-chief-of-staff-v{version}.zip`.
- `../../../dist/codex-chief-of-staff-v{version}.zip.sha256`.

## Human check

Inspect the staged file list and confirm no private or unrelated file shipped.
