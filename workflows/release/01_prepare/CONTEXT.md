# 01_prepare - freeze release source

One job: make the intended version and capability contract reviewable.

## Inputs

- Working: current Git tree and approved release scope.
- Reference: `../../../docs/release-process.md`.
- Reference: `../../../docs/testing.md`.

Do NOT load private configuration values or unrelated project data.

## Process

1. Inventory the tree and preserve unrelated changes.
2. Match `VERSION` to the manifests and hook version. Update the changelog, docs and tests.
3. Record unverified claims as pending evidence.

## Outputs

- Reviewable source diff in the repository working tree.

## Human check

Approve the exact scope, version, claims, and publication boundary.
