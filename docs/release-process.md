# Release process

Use `workflows/release/CONTEXT.md` as the routing file. When the approved plan
includes publication, its authorization continues through push, tag, release,
and public verification after every required gate passes.

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
   ChatGPT Work tasks through `scripts/live_acceptance_harness.py`. Require the
   host-specific safety control (`:read-only` for Codex; **Work locally** plus
   **Ask for approval** for ChatGPT Work), separate UI and runtime evidence,
   inline response-only execution, and zero task, file, connector, or external
   mutations. ChatGPT Work requires owner-verified Work UI evidence; its agent
   runtime may report `codex`.
4. Confirm a fresh Codex architecture prompt activates ICM enforcement and
   returns a conforming answer after no more than two correction cycles. Confirm
   ChatGPT Work applies the same ICM contract through the Chief skill.
5. Update `tests/model-acceptance.json` only from observed evidence.
6. An owner may approve a version-bound release waiver for pending Sol or Terra
   checks. Failed checks, host acceptance, and installed-runtime smoke cannot be
   waived. Pending evidence stays pending.
7. A documentation-only patch may carry forward prior host and model evidence
   only when it names the prior release and records why runtime behavior is
   unchanged. Keep the prior receipt intact. Run a fresh installed-runtime
   smoke check. Any skill, contract, hook behavior, bundled runtime, routing,
   permission, or validator behavior change requires fresh host acceptance.
8. Rebuild with `--require-model-acceptance`. The embedded status must be
   `pass` or `pass_with_waiver`.

## 04 Publish

1. Record the exact commit, proposed tag, archive, checksum, evidence, and
   remaining risks.
2. Confirm that repository publication is included in the current request or
   approved plan. This is a scope check, not a new approval checkpoint.
3. Commit the canonical source.
4. Create and push the signed or annotated tag for the current `VERSION`.
5. Verify CI plus attestation. Verify the release asset and checksum. Check the
   README links and GitHub Latest. Confirm installed caches and fresh-host
   behavior.

Historical tags and release assets are immutable. Fixes ship as a new version.

Repository publication is the only documented distribution path. Release copy
must point users to the GitHub repository and its installer scripts. Do not
claim third-party review, approval, listing, or distribution without completed
evidence and an owner-authorized documentation change.
