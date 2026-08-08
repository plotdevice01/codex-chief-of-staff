---
name: brand-voice-copywriter
description: Build or update evidence-backed corporate brand voice packages and write governed copy in that voice. Use for client intake, voice research, terminology controls, brand governance, ads, landing pages, press releases, scripts, email, SMS, social posts, event copy, executive messaging, or other business copy.
---

# Brand voice copywriter

Build a client-owned voice system, then use it to write conversion-oriented copy without inventing facts or weakening approval controls. Treat conversion as a testable target, not a promised outcome.

## Select the job

- New client or incomplete voice system: build the Brand Voice Package first.
- Existing approved package: load only the approved voice files and the current copy brief.
- Package update: preserve the adopted version, record the change, and route it through the named owner.
- Copy request: draft the requested asset. Then run the release gates and label its status.

## Start a client workspace

Use the bundled ICM Pipeline for new or recurring client work. Run:

```powershell
python scripts/new_brand_voice_project.py --client-name "Client name" --owner "Aaron Thomas" --output "C:\approved\client-path"
```

The script stamps a blank client workspace from `assets/client-workspace/`. Do not place one client's facts in the reusable skill or another client's workspace.

Read `references/intake-and-evidence.md` before collecting sources. Read `references/brand-voice-package-spec.md` before drafting the package.

## Run the pipeline

1. Intake: record the business, audience, offer, boundaries, and owner map. Mark gaps as unknown.
2. Evidence: inventory sources. Separate confirmed facts from inference and proposals. Record rights limits.
3. Voice: define the corporate voice and tone controls. Set the message order. Build terminology controls and prohibited language.
4. Package: build the governed documents and editable libraries in the required package specification.
5. Copy: write from an approved brief. Choose the closest format rule in `references/copy-production.md`.
6. Release: run claim, rights, privacy, channel, owner, and AI Sloppy Copy checks. Record the exact approved version.

Stop at a stage gate when a missing answer could change a material fact, claim, audience, offer, legal position, or public release decision. A placeholder may support internal rehearsal. It is not public copy.

Seal the adopted package manifest after its five referenced files are complete:

```powershell
python scripts/package_manifest.py seal --manifest "C:\client\stages\04_package\output\package-manifest.json" --status Approved --approved-by "Owner name"
```

The manifest is the handoff contract for downstream skills. It records the client, package version, approval, file paths, and SHA-256 hashes.

## Build the Brand Voice Package

Use these references:

- `references/brand-voice-package-spec.md` for required deliverables and acceptance tests.
- `references/governance-and-claims.md` for owner routes and hard release blocks.
- `references/sloppy-copy-qa.md` for AI Sloppy Copy execution.

Make the voice corporate. A founder, executive, clinician, or spokesperson may adapt delivery without becoming the source of the corporate voice.

## Write client copy

Load only:

- The current approved voice architecture.
- The terminology and prohibited-language controls.
- The current copy brief.
- Source records for the exact claims used.

Write one asset version at a time unless the brief requests variants. Use placeholders when approved facts are missing. Do not convert source silence into a claim.

For paid ads, retain `Hook -> Value -> CTA`. For every other format, use the channel rule in `references/copy-production.md`. For an unlisted format, identify the reader's decision and use the closest governed pattern.

## Apply hard boundaries

- Do not place protected health information or unnecessary personal data in prompts, connectors, source tools, or outputs.
- Do not create clinical, legal, financial, safety, performance, ranking, price, scarcity, or guarantee claims without current support and the required owner.
- Do not use testimonials, quotations, likeness, or third-party marks without recorded rights for the intended channel.
- Do not treat an assigned owner as approval. Record the decision and its source reference.
- Do not publish or send. Do not post or buy media. Do not change permissions or create external records unless the user authorizes that action.

Read `references/governance-and-claims.md` whenever the copy contains a material claim or regulated subject.

## Use AI Sloppy Copy

AI Sloppy Copy is mandatory for all authored prose. Its hard rules outrank voice samples. Client terminology may be protected through a narrow glossary entry, but a glossary cannot excuse a prohibited claim.

Run the full assembled asset through the checker. Repair the complete sentence, then check the full asset again. Use no more than two repair passes. See `references/sloppy-copy-qa.md` for the local command and report record.

## Record status

Use one status:

- Draft: the asset is still being written.
- Internal rehearsal: structure is usable, but facts or approvals are incomplete.
- Owner review: the exact version is awaiting a named decision.
- Approved: the exact version has a recorded decision for a defined use.
- Public ready: all sources, rights, channel rules, and release approvals are complete.
- Hold: one or more hard gates failed.

Never infer `Public ready` from package approval.

## Return the work

For a package, return the master guide and its editable libraries. Include a fixed-layout PDF and a checksum manifest when the user requests shipment.

For copy, return the finished asset first. Then state its status and source limits. Add required approvals and the recommended test. Keep internal notes outside the client copy.
