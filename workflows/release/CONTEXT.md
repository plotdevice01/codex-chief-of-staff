# Release pipeline

One job: turn authorized Chief source into a verified release and publish it
when publication is included in the current request or approved plan.

| Stage | Job | Input | Output | Human check |
|---|---|---|---|---|
| `01_prepare` | Freeze release source | Source tree and version contract | Reviewable source diff | Approve exact scope and claims |
| `02_build` | Build candidate | Approved source | `dist/` archive and checksum | Inspect staged files |
| `03_validate` | Prove candidate | Candidate plus test contracts | Validation evidence | Confirm every required result |
| `04_publish` | Publish authorized release | Verified candidate plus plan-scoped publication authorization | Git tag and GitHub release | Verify exact commit, tag, and public parity |

Stable rules live in `docs/release-process.md`, `docs/testing.md`, and the
release scripts. Candidate files live in ignored `dist/` and `qa/` paths.
Status is the highest numbered stage whose named outputs and human check exist.
