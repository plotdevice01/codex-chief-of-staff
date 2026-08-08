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

1. Present the exact commit, proposed tag, archive, checksum, evidence, and
   remaining risks.
2. Wait for explicit publication approval.
3. Commit the canonical source.
4. Create and push the signed or annotated tag for the current `VERSION`.
5. Verify CI plus attestation. Verify the release asset and checksum. Check the
   README links and GitHub Latest. Confirm installed caches and fresh-host
   behavior.

Historical tags and release assets are immutable. Fixes ship as a new version.

## Public OpenAI Plugins Directory

GitHub publication and public-directory publication are separate gates. A
GitHub or repo marketplace can distribute Chief to developers and a controlled
team, but it does not make Chief publicly searchable.

Chief is submitted as one skills-only plugin. AI Sloppy Copy, Brand Voice
Factory, and Crafty Carousels remain upstream source products and are not
separate team-facing submissions.

Before submission:

1. Confirm the publisher has **Apps Management: Write** in the OpenAI Platform.
2. Confirm the publisher's individual or business identity is verified.
3. Confirm the public website, support, privacy, and terms URLs match that identity.
4. Load the listing and starter prompts from
   `tests/openai-directory-submission.json`. Load its five positive tests and
   three negative tests too.
5. Upload the final Chief skill bundle and submit it through the OpenAI plugin
   submission portal.
6. Wait for OpenAI approval. Submission is not publication.
7. After approval, select **Publish** and verify that **Chief of Staff** is
   searchable in the universal Plugins Directory from both ChatGPT Work and Codex.
8. Test installation from a separate member account before workspace-wide rollout.

Do not use “available in the OpenAI Plugins Directory” in release copy until
step 7 is visibly confirmed. A directory listing is an external fact, not a
motivational poster.
