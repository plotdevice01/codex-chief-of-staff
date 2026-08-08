# Chief content production

Use the OpenAI plugin root supplied as `PLUGIN_ROOT` for every bundled script
and resource. Legacy host-variable alternatives retained inside an exact
vendored upstream workflow are compatibility text, not an active Chief route.

Use this contract for assistant-authored business content. Chief owns routing. The user does not select Brand Voice Factory, Crafty Carousels, or AI Sloppy Copy.

## Classify once

Select one mode before drafting:

| Request | Required mode |
|---|---|
| Video ad, paid-video concept, performance-creative script, or motion-first paid placement | `paid_video` |
| Static ad, paid social copy, paid campaign copy, Meta, Google Ads, LinkedIn ad, or another paid placement | `paid_ad` |
| Instagram or LinkedIn carousel, slide copy, carousel visual production, or carousel release package | `carousel` |
| Brand voice creation, incomplete voice system, voice governance, or voice package update | `brand_voice` |
| Organic social post, short-form video script, reel script, caption, or campaign concept | `organic_social` |
| Email, report, reply, landing page, article, SOP, UI copy, or other authored prose | `general_copy` |

Mentions of ad spend, reporting, operations, or analysis do not activate `paid_ad` unless the requested deliverable is advertising copy or creative.

## Load voice and evidence

For a named client or speaker, load the approved voice package and the source records for the requested claims. If no approved package exists, use the Brand Voice workflow at `<SKILL_ROOT>/vendor/brand-voice-factory/workflow.md`. Do not invent voice traits while drafting.

Use only supplied or verified facts. Mark a material missing fact `UNKNOWN`. Stop when it could change the audience, offer, claim, legal position, or release decision.

## Query content intelligence

For `paid_video`, `paid_ad`, `carousel`, and `organic_social`, run one complete library query before drafting. Resolve `SKILL_ROOT` to this Chief skill folder.

```powershell
py -3 "<SKILL_ROOT>\scripts\content_intelligence.py" --content-class business --format video --query "audience problem offer proof" --cta-category sales --cta-text "exact requested action" --offer-type paid
```

Choose `business`, `ugc_creator`, or `influencer` from the campaign's authority. Do not infer it from industry. Choose `video` for spoken or motion-first work and `image_carousel` for static sequential work.

The receipt must report `hooks=751`, `scripts=7`, and `ctas=39` as searched. Pass the actual offer type; use `unknown` only when the offer genuinely is unresolved. Use the one `recommended` hook, script, and CTA from the result unless the evidence or offer-compatibility gate makes a record unusable. In that case, select another compatible record from the same result and report why. Do not inspect the raw libraries or rerun the query merely to browse more options. Do not recreate a hook, script framework, or CTA from memory. If the query cannot run or its complete libraries are unavailable, stop with `Hold: content library unavailable` instead of silently drafting generic copy.

The finished copy must preserve the semantic structure of every record reported as selected. Do not cite a hook ID after replacing it with a generic callout. If a returned pattern requires a pain, result, proof, urgency, or other claim that is not verified, select another returned record or hold. The ranking downweights these unsupported claim mechanisms, but the evidence gate still controls final selection.

## Produce by mode

### Paid video

Read `<SKILL_ROOT>/references/paid-video-creative.md`. Build complete concepts,
not isolated copy. Every concept needs a creator-native format, first-frame
action, spoken hook, visual progression, mechanism, sourced proof, offer,
compatible CTA, pacing, captions, and edit direction. Expand only approved
concepts into recording-ready variations. Cosmetic hook rewrites are not
distinct concepts.

### Paid ad

Read `<SKILL_ROOT>/vendor/ai-sloppy-copy/workflow.md` and activate its Paid ad mode. Every complete ad uses this order:

1. Hook or Callout.
2. Problem and Promise.
3. Mechanism and verified Proof.
4. Offer Snapshot and Risk.
5. One Direct CTA naming the action and immediate benefit.

Use one selected hook pattern and one selected script framework. Lock one CTA. Do not produce general copy and call it an ad.

### Carousel

Read `<SKILL_ROOT>/vendor/crafty-carousels/workflow.md`. Follow its copy-first and anchor-first gates. Use its bundled workspace scripts and assets under `<SKILL_ROOT>/vendor/crafty-carousels/`. Do not generate slides before exact copy and the anchor direction are approved.

### Brand voice

Read `<SKILL_ROOT>/vendor/brand-voice-factory/workflow.md`. Use its references, scripts, and workspace assets under `<SKILL_ROOT>/vendor/brand-voice-factory/`. Seal the approved package manifest before downstream use.

### Organic social

Use one selected hook pattern and one selected script framework. Use the selected CTA category that matches the requested action. Preserve evidence and approved voice. Do not claim a library pattern is current or high-performing without current evidence.

### General copy

Do not query the content library unless a hook, campaign structure, or CTA is part of the requested work. Apply the approved voice and the AI Sloppy Copy rules.

## Validate all authored prose

For prose that exists only in the current task, pass the complete assembled
text directly to the pinned checker. Do not create a temporary file merely to
run validation:

```powershell
py -3 "<SKILL_ROOT>\vendor\ai-sloppy-copy\scripts\ai_sloppy_copy.py" --rules "<SKILL_ROOT>\vendor\ai-sloppy-copy\scripts\AI-Sloppy-Copy-Rules.json" --text "<complete assembled prose>"
```

For an existing file deliverable, run the checker against that exact file:

```powershell
py -3 "<SKILL_ROOT>\vendor\ai-sloppy-copy\scripts\ai_sloppy_copy.py" --rules "<SKILL_ROOT>\vendor\ai-sloppy-copy\scripts\AI-Sloppy-Copy-Rules.json" "C:\path\to\deliverable"
```

Repair the full sentence, then check the complete deliverable again. Stop after two repair passes. Protected quotes, code, commands, paths, API fields, and required legal wording remain exact.

If the checker cannot run, the work may be returned only as `Draft`. It cannot be approved, public ready, or release ready.

## Return an execution receipt

Append a compact receipt outside client-facing copy:

```text
Mode: paid_ad
Voice package: loaded or not required
Content library: hooks 751, scripts 7, CTAs 39 searched
Selected records: hook ID, script ID, CTA ID
Hook -> Value -> CTA: applied or not applicable
AI Sloppy Copy: pass, hold, or unavailable
Offer compatibility: pass, hold, or not applicable
Status: Draft, Owner review, Approved, Public ready, or Hold
```

Never report a component as used merely because its workflow file was read. Report the query, selected record IDs, checker result, or produced specialist artifact.
