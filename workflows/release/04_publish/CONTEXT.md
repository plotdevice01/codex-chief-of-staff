# 04_publish - publish authorized release

One job: publish the exact verified candidate when publication is included in
the current request or approved plan.

## Inputs

- Working: verified candidate and checksum from `../03_validate/CONTEXT.md`.
- Reference: `../../../docs/release-process.md`.

Do not publish outside the authorized scope. Do not ask again when push, tag,
release, permission changes, or publication are already listed in the current
request or approved plan.

## Process

1. Record the exact commit, tag, archive, checksum, and remaining risks.
2. Verify that publication is inside the current request or approved plan.
3. Push the authorized commit and tag, then verify CI and public artifacts.

## Outputs

- Authorized Git tag and GitHub release.
- Verified public asset, checksum, attestation, and Latest state.

## Human check

Confirm the exact published commit and tag, then verify public parity. This
check validates the result; it does not reopen permission already granted by
the approved plan.
