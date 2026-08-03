# Release process

Use `workflows/release/CONTEXT.md` as the routing file. Publication is a
separate approval after the candidate passes every required gate.

## 01 Prepare

1. Update `VERSION`, manifests, configuration example, hook version, docs, SOP
   source, tests, and `CHANGELOG.md`.
2. Preserve unrelated work and inspect the complete source diff.
3. Keep unexecuted model or host checks marked `pending`. Record failed checks
   as `fail` with evidence.

## 02 Build

1. Run `python scripts/build_release.py --output dist` for a local candidate.
2. Inspect the staged folder and ZIP list.
3. Confirm the embedded validation status is `candidate` until fresh acceptance
   passes.

## 03 Validate

1. Run the complete suite in `docs/testing.md`.
2. Render the generated SOP to PNG and inspect every page.
3. Install the candidate locally and run all live scenarios in fresh Codex and
   Claude Code sessions.
4. Confirm a fresh Claude Code architecture prompt activates ICM enforcement
   and returns a conforming answer after no more than two correction cycles.
5. Update `tests/model-acceptance.json` only from observed evidence.
6. An owner may approve a version-bound release waiver for pending Sol or Terra
   checks. Failed checks, host acceptance, and installed-runtime smoke cannot be
   waived. Pending evidence stays pending.
7. Rebuild with `--require-model-acceptance`. The embedded status must be
   `pass` or `pass_with_waiver`.

## 04 Publish

1. Present the exact commit, proposed tag, archive, checksum, evidence, and
   remaining risks.
2. Wait for explicit publication approval.
3. Commit the canonical source.
4. Create and push the signed or annotated `v1.0.0` tag.
5. Verify CI plus attestation. Verify the release asset and checksum. Check the
   README links and GitHub Latest. Confirm installed caches and fresh-host
   behavior.

Historical tags and release assets are immutable. Fixes ship as a new version.
