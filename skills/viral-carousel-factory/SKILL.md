---
name: viral-carousel-factory
description: Build governed, reference-first Instagram and LinkedIn carousels from approved client evidence, brand inputs, exact copy, and visual references. Use for carousel strategy, slide copy, GPT Image production, accessibility, QA, and release-ready delivery packages.
---

# Viral Carousel Factory

Create high-retention carousel packages without promising virality. The repeating unit is one client carousel run inside the bundled ICM Pipeline.

## Route

1. Read `references/production-system.md` for structure, copy, reference selection, and image production.
2. Read `references/client-intake.md` when starting a client workspace or updating its brand, voice, people, or asset library.
3. Read `references/platform-delivery.md` for the chosen publishing route. Recheck current platform facts before release.
4. Read `references/governance-measurement.md` when claims, endorsements, regulated topics, client assets, or performance evaluation are involved.
5. Read `references/sources.md` only when provenance or source conflicts matter.

## Operating contract

- Use the bundled ICM Pipeline. Factory material includes the client brand and approved evidence. It also includes the platform route and production rules. Assigned reference roles plus release policy complete the factory. Product is one run's brief and claim decisions. It also includes approved copy, cover candidates and final slides. The caption, alt text and release record complete the product.
- Keep every client isolated. Never import another client's facts, voice, approvals, or assets.
- The bundled run records control scope and status. They also control approvals. Chief of Staff may coordinate them when installed, but the factory does not depend on Chief. Do not publish or schedule without explicit authorization. The same rule applies to media buying, external delivery and permission changes.
- AI Sloppy Copy is mandatory for carousel copy, caption, alt text, and client-facing notes. Preserve `Hook -> Value -> CTA`, then run the installed checker and repair up to two times. If AI Sloppy Copy is unavailable, drafting may continue, but final copy approval and release must stop with the dependency recorded as a blocker.
- Use the installed image generation skill for GPT Image 2 or the current approved image model. Follow its current instructions rather than embedding an API wrapper here.
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

Ask for one missing blocking decision at a time. Mark non-blocking gaps `UNKNOWN`. Never fill them from memory or another client.

Before the first run, complete `setup/client-intake.md`. Save stable visual rules in `_shared/brand.md`, stable writing rules in `_shared/voice.md`, and approved people plus likeness rules in `_shared/people-and-likeness.md`. Register every usable file in `_shared/asset-register.csv`. Keep actual client media in the private `_shared/media/` directory created by the stamping script. Record proof claims in `_shared/claim-register.csv`.

## Run the Pipeline

### 1. Intake and evidence

Run the guided client intake one unanswered blocking question at a time. Define one audience and one desired action. Record one sharp idea plus the approved offer. Add the platform route and claim sources. Then record the brand files plus approved voice samples. Record the people who may appear and the rights-cleared visual references. Assign each reference a visual job.

Do not write proof claims from an inspiration image. A visual reference is not evidence.

### 2. Strategy and copy

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

Select two to four references and assign each one job. Generate three distinct cover candidates with the exact approved copy. Compare them at thumbnail size. Select one direction. Refine it until hierarchy and brand fit pass. Legibility and curiosity must pass too.

The approved cover is the visual anchor. Do not generate the remaining carousel until the human gate records anchor approval.

### 4. Slide production

Generate or edit one slide at a time from the approved anchor. For each slide, pass:

- the anchor image;
- only the references needed for that slide;
- exact approved text;
- subject and composition instructions;
- fixed palette, typography behavior, spacing, numbering, and safe-zone rules.

After each result, inspect the image. Reject misspelled or missing text. Reject weak contrast and style drift. Reject unsafe cropping or repeated visuals. Reject false logos and unsupported depictions. Fix the current slide before moving on.

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
