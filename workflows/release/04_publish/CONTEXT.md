# 04_publish - publish approved release

One job: publish the exact verified candidate after separate approval.

## Inputs

- Working: verified candidate and checksum from `../03_validate/CONTEXT.md`.
- Reference: `../../../docs/release-process.md`.

Do NOT push, tag, publish, or change permissions without immediate approval.

## Process

1. Present the exact commit, tag, archive, checksum, and remaining risks.
2. Wait for publication approval.
3. Push the approved commit and tag, then verify CI and public artifacts.

## Outputs

- Approved Git tag and GitHub release.
- Verified public asset, checksum, attestation, and Latest state.

## Human check

Approve the exact commit and tag before publishing. Confirm public parity after.
