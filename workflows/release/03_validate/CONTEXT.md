# 03_validate - prove candidate behavior

One job: verify source, archive, rendered SOP, local parity, and fresh hosts.

## Inputs

- Working: candidate outputs from `../02_build/CONTEXT.md`.
- Reference: `../../../docs/testing.md`.
- Reference: `../../../tests/model-acceptance.json`.

Do NOT convert pending model evidence into a pass without a fresh run.

## Process

1. Run static, hook, sync, ICM, privacy, archive, and parity checks.
2. Render the SOP to images and inspect every page.
3. Run required fresh ChatGPT Work and Codex scenarios.

## Outputs

- `../../../dist/codex-chief-of-staff-v{version}/release-validation.json`.
- Recorded SOP visual review and fresh-host evidence.

## Human check

Confirm every required result is observed and every release claim is bounded.
