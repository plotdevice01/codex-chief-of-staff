---
name: crafty-carousels
description: Build governed, reference-first Instagram and LinkedIn carousels from approved client evidence, brand inputs, exact copy, and visual references. Use for carousel strategy, slide copy, GPT Image production, accessibility, QA, and release-ready delivery packages.
---

# Crafty Carousels Skill

Create high-retention carousel packages without promising virality. The repeating unit is one client carousel run inside the bundled ICM Pipeline.

## Route

1. Read `references/production-system.md` for structure, copy, reference selection, and image production.
2. Read `references/client-intake.md` when starting a client workspace or updating its brand, voice, people, or asset library.
3. Read `references/hook-library.md` when identifying the client content class or researching and selecting hook patterns.
4. Read `references/copy-library.md` when selecting an installed script framework or CTA.
5. Read `references/platform-delivery.md` for the chosen publishing route. Recheck current platform facts before release.
6. Read `references/governance-measurement.md` when claims, endorsements, regulated topics, client assets, or performance evaluation are involved.
7. Read `references/sources.md` only when provenance or source conflicts matter.

## Operating contract

- Use the bundled ICM Pipeline. Factory material includes the client brand and approved evidence. It also includes the platform route and production rules. Assigned reference roles plus release policy complete the factory. Product is one run's brief and claim decisions. It also includes approved copy, cover candidates and final slides. The caption, alt text and release record complete the product.
- Keep every client isolated. Never import another client's facts, voice, approvals, or assets.
- The bundled run records control scope and status. They also control approvals. Chief of Staff may coordinate them when installed, but the factory does not depend on Chief. Do not publish or schedule without explicit authorization. The same rule applies to media buying, external delivery and permission changes.
- AI Sloppy Copy is mandatory for carousel copy, caption, alt text, and client-facing notes. Preserve `Hook -> Value -> CTA`, then run the installed checker and repair up to two times. If AI Sloppy Copy is unavailable, drafting may continue, but final copy approval and release must stop with the dependency recorded as a blocker.
- Use the installed image generation skill for GPT Image 2 or the current approved image model. Follow its current instructions rather than embedding an API wrapper here.
- Treat `references/production-system.md` as a versioned contract. Every run records its SHA-256. Stop production when the recorded hash differs from the installed file; reread the current rules and repeat the affected human approvals.
- Treat supplied examples as references, not assets to redistribute. Record the visual job of each reference and confirm usage rights before client delivery.
- Virality is an outcome to test, not a claim to make. Design for attention and continuation. Aim for a useful payoff, saves and shares. Measure qualified action.

## Start a client workspace

Use the stamping script. It copies a blank workspace and leaves the skill source unchanged.

```powershell
python scripts/new_carousel_project.py init --client-name "Example Co" --owner "Content Lead" --output "C:\work\example-carousel"
```

Then create a run. Eight slides is the default, not a platform limit.

```powershell
python scripts/new_carousel_project.py new-run --workspace "C:\work\example-carousel" --slug "one-sharp-idea" --route instagram-native --slide-count 8
```

When Brand Voice Factory supplied the approved client voice, import its sealed package before creating a run:

```powershell
python scripts/import_brand_voice.py import --manifest "C:\client\stages\04_package\output\package-manifest.json" --workspace "C:\work\example-carousel"
```

The importer verifies the client ID, approval status, file paths, and hashes. It copies the approved package into the Crafty workspace. It maps claim and asset rows without pretending missing Crafty controls were approved.

Ask for one missing blocking decision at a time. Mark non-blocking gaps `UNKNOWN`. Never fill them from memory or another client.

Before the first run, complete `setup/client-intake.md`. Save stable visual rules in `_shared/brand.md`, stable writing rules in `_shared/voice.md`, and approved people plus likeness rules in `_shared/people-and-likeness.md`. Register every usable file in `_shared/asset-register.csv`. Keep actual client media in the private `_shared/media/` directory created by the stamping script. Record proof claims in `_shared/claim-register.csv`.

## Run the Pipeline

### 1. Intake and evidence

Run the guided client intake one unanswered blocking question at a time. Define one audience and one desired action. Ask whether this campaign is `business`, `ugc_creator`, or `influencer` content and record exactly one class. Ask whether hook research should use `image_carousel`, `video_adaptable`, or `both`; Crafty still delivers a carousel, so video-first hooks must be adapted and re-approved. Record one sharp idea plus the approved offer. Add the platform route and claim sources. Then record the brand files plus approved voice samples. Record the people who may appear and the rights-cleared visual references. Assign each reference a visual job.

Do not write proof claims from an inspiration image. A visual reference is not evidence.

### 2. Strategy and copy

Choose and record one copy mode before design: `exact-source` for visual-only comparisons or `approved-draft` for copy-and-design work. In `exact-source` mode, preserve the supplied copy without expansion or explainer text. Freeze approved `copy.md` with SHA-256 before image production. Select the narrative format that fits the insight. Supported formats include comparison and tutorial, plus a native personal lesson or story arc. Use a custom format only when explicitly approved.

For `approved-draft`, query only the recorded content class and hook-research format in the bundled 751-record source library. Show three to five patterns with stable IDs and format fit. Include source-supplied examples when available. Never invent an example when the source did not provide one. Adapt with approved client evidence and voice, then record the selected IDs. When useful, query the installed 7-script and 39-CTA library; do not recreate those records from memory. Never describe a library pattern as currently trending without current research evidence. For `exact-source`, preserve the supplied hook and do not substitute a library entry.

Write the full carousel before generating images. Default to the smallest slide count that carries the idea. Use eight when the idea benefits from the complete sequence:

1. Hook
2. Transition
3. Tease
4. Tease
5. Tease
6. Tease or proof
7. Climax or payoff
8. Action

Create at least three cover hooks. Slide 2 must reopen curiosity or state the promised gain. It may instead state the avoided loss or source of authority. Give each remaining slide one job. End with one obvious action.

Apply the screenshot test: each value slide should still help when seen alone. Reject repetition disguised as progress.

Stop for human approval of strategy and exact copy before generating a full carousel.

### 3. Anchor slide

Select two to four references and assign each one job. Generate exactly three distinct cover candidates with the exact approved copy. Do not substitute color swaps for different compositions. Compare all three at 320 pixels wide. Select one direction. Refine it until hierarchy and brand fit pass. Legibility and curiosity must pass too.

The approved cover is the visual anchor. Record all three files and their SHA-256 values. Record the selected candidate and the SHA-256 of `visual-brief.md`. Do not generate the remaining carousel until the human gate records anchor approval and validation passes.

### 4. Slide production

Generate or edit one slide at a time from the approved anchor. For each slide, pass:

- the anchor image;
- only the references needed for that slide;
- exact approved text;
- subject and composition instructions;
- fixed palette, typography behavior, spacing, numbering, and safe-zone rules.

After each result, inspect the image. Reject misspelled or missing text. Reject weak contrast and style drift. Reject unsafe cropping or repeated visuals. Reject false logos and unsupported depictions. Fix the current slide before moving on.

Use one locked type family unless the approved brand system requires another. It must be wide with a high x-height and heavy weight. Apply it to every text role. On 1080 by 1350 slides, headlines must render at 68 pixels or larger. Supporting copy must be at least 40 pixels, and CTAs must be at least 48 pixels. Use weight 800 or heavier and inspect at 320 pixels wide. Never place text on a glow or flare. Avoid colored haze and gradient hotspots. Keep text off people and primary objects. Keep CTAs above bottom crop and interface-safe zones. Do not add shapes or arrows. Do not add symbols or fake UI. Reject stray characters. Do not add explainer copy that is absent from the approved copy.

For a personal brand requiring strong identity fidelity, prefer an approved real-photo composite over a generated avatar. Use the image model for the background, environment, lighting plate, or non-identity elements, then preserve the approved person's real face and body asset. Record `approved-real-photo-composite`, `approved-ai-likeness`, or `not-applicable` in the run before production.

When the operator approves the deck except for named slides, edit only those slides. Do not regenerate approved slides.

Do not ask the image model for a contact sheet as the final output. Final slides must be separate files with identical dimensions.

### 5. Release package

Validate the run manifest:

```powershell
python scripts/new_carousel_project.py validate --run "C:\work\example-carousel\runs\20260804-one-sharp-idea"
```

The release package requires final slide files plus a caption. It also requires per-slide alt text and source decisions. Record rights decisions and any required disclosure language. Add the visual QA record plus human release approval. Record the live platform limit and verification date. Never infer `Release ready` from copy or anchor approval.

## Output contract

Return or save:

- `run.json` with state and approvals;
- `copy.md` with hooks and exact slide copy. It also holds the caption plus alt text;
- `visual-brief.md` with assigned reference roles and anchor rules;
- `prompts.md` with one prompt per generated asset;
- separate final slide files;
- `qa.md` with evidence, rights, accessibility, visual, and platform checks.
- the exact client profile versions used for brand, voice, people, assets, and claims.

State what is confirmed and what is an operator choice. Mark remaining gaps `UNKNOWN`.
