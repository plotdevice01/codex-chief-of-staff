# Release pipeline

One job: turn approved Chief source into a verified release, then publish only
after a separate human approval.

| Stage | Job | Input | Output | Human check |
|---|---|---|---|---|
| `01_prepare` | Freeze release source | Source tree and version contract | Reviewable source diff | Approve exact scope and claims |
| `02_build` | Build candidate | Approved source | `dist/` archive and checksum | Inspect staged files |
| `03_validate` | Prove candidate | Candidate plus test contracts | Validation evidence | Confirm every required result |
| `04_publish` | Publish approved release | Verified candidate | Git tag and GitHub release | Approve exact commit and tag |

Stable rules live in `docs/release-process.md`, `docs/testing.md`, and the
release scripts. Candidate files live in ignored `dist/` and `qa/` paths.
Status is the highest numbered stage whose named outputs and human check exist.
