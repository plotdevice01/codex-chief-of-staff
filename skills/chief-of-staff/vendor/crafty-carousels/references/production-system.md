# Production system

## Core model

Use one sharp idea per carousel. Build copy first, approve the cover as the visual anchor, then produce one slide at a time.

Treat this file as the canonical production contract. Every run must record its SHA-256. If the file changes, stop and reread it before continuing. Repeat strategy-copy or anchor approval when the changed rule affects that approval.

The default eight-slide arc is:

| Slide | Job | Test |
|---|---|---|
| 1 | Hook | Stops the right reader and creates specific curiosity |
| 2 | Transition | States the gain, avoided loss, or credible reason to continue |
| 3-6 | Tease and value | Reveals one useful unit at a time with proof or examples |
| 7 | Climax or payoff | Delivers the clearest insight, reveal, or summary |
| 8 | Action | Makes one next step obvious |

Use fewer slides when the idea is smaller. Add slides only when each new slide contributes a distinct proof point, step, example, objection, or reveal. Do not pad a carousel to hit a preferred count.

Use this compact five-slide arc when the idea can be delivered without additional steps:

| Slide | Job | Test |
|---|---|---|
| 1 | Hook | Stops the scroll |
| 2 | Value | Delivers an immediate useful gain |
| 3 | Frame | Makes the idea or market clear |
| 4 | Proof | Builds trust with approved evidence, reasoning, or example |
| 5 | Action | States one obvious next step |

The repeatable reference workflow is: complete visual brief, exact approved copy, exactly three Slide 1 compositions, one refined visual anchor, then one remaining slide at a time. Never ask the image model to generate the full carousel in one request. A full-deck generation request produces unreviewed visual drift and bypasses the anchor gate.

Use this 10-slide spine when the idea needs a longer conversion sequence:

| Slides | Job | Test |
|---|---|---|
| 1 | Pattern interrupt | Stop the right reader |
| 2 | Tension | Deepen curiosity without resolving it |
| 3-6 | Structural insight | One distinct idea per slide |
| 7-9 | Application | Make the insight usable and personally relevant |
| 10 | Action | One command and one action |

Every slide must earn the next swipe. Do not repeat an idea merely to extend the deck.

## Format menu

Pick the format that fits the insight before writing or arranging slides:

- `comparison`: before versus after, or old way versus new way;
- `tutorial`: step-by-step process or revealed method;
- `native`: personal story with an extracted lesson;
- `story-arc`: transformation narrative with an earned emotional payoff;
- `custom-approved`: another format explicitly approved for the run.

Do not force the insight into a preferred template.

## Design constraints

- Use no more than two font families. Create hierarchy through size, weight, spacing, and role rather than typeface variety.
- Use no more than three primary colors: background, text, and accent.
- Freeze one visual thread after anchor approval. Every slide must visibly belong to the same story through repeated typography, palette, spacing, image treatment, numbering, or another approved motif.
- Use 1080 by 1440, or 3:4, for the verified native-organic route when available. Use 1080 by 1350, or 4:5, for paid-compatible production. At equal width, 1:1 provides 25 percent less canvas area than 3:4; do not default to square when a supported portrait route is available.
- Keep critical content at least 180 pixels from the top and bottom, 50 pixels from the left, and 120 pixels from the right on a 1080-pixel portrait canvas.

## Slide templates

- Hook: stop the scroll. Slide 2 must confirm or deepen the promise through tension, not prematurely resolve it.
- Value: favor a strong visual plus minimal approved text and one insight per frame. In `exact-source` mode, preserve the approved text even when it is longer.
- CTA: use one command with no added explanation. For an approved personal-brand run, use the approved person's real photo when suitable and rights-cleared.

Repeat the approved template behavior consistently enough to build recognition without repeating content.

## Readability gate

Readability outranks decoration, image novelty, and fitting more copy onto a slide. Stop production when a slide cannot be understood at phone-thumbnail size.

- Use one dominant headline and no more than two short supporting sentences.
- Shorten copy before reducing type size. Treat the documented font sizes as minimum floors, not targets.
- Use wide, heavy, high-x-height sans-serif letterforms for primary mobile headlines. Do not use condensed display faces, thin serif faces, script fonts, or novelty fonts for the main message.
- Create visual style through scale, color, spacing, and composition. Stylized fonts may appear only in a short accent when the dominant headline remains immediately readable.
- Keep supporting copy in the same approved type family as the headline unless the brand system explicitly requires another family. Do not drop to a lighter, narrower, or more delicate face.
- On a 1080 by 1350 slide, start supporting copy at 40 pixels with a heavy weight. Reduce it only after shortening layout lines and confirming legibility at 320 pixels wide.
- Apply capitalization as a visual treatment without changing the stored source wording. Preserve exact source copy beneath the presentation layer.
- Reserve a dedicated text-safe area before placing the subject. Supporting copy may not overlap or crowd a face, head, body, hand, or primary object.
- Keep every text-safe area on a stable, high-contrast field. Never place a glow, flare, gradient hotspot, or colored haze behind production text.
- Keep the CTA above bottom crop and interface-safe zones, inside the primary reading path rather than at the extreme bottom edge.
- Keep anchor hooks to the fewest words that preserve the verified meaning. Prefer three short lines over one crowded line or five narrow lines.
- Review every anchor at approximately 320 pixels wide. Reject it when any headline word requires zooming, squinting, or rereading.
- Keep headlines concrete and useful. Remove labels, kickers, repeated titles, and footer copy that compete with the main message.
- Keep text away from faces, hands, and the primary visual subject.
- Use plain text by default. Do not add decorative bars, bullets, arrows, frames, symbols, fake interface elements, or stray characters.
- Add a shape or symbol only when the approved brand system requires it and it carries a clear function.
- Render final copy with a deterministic text layer. Do not rely on an image model to spell or typeset production copy.
- For personal brands requiring exact likeness, use an approved real-photo composite. Generate the scene or background separately and preserve the approved person's real face and body rather than asking the image model to recreate identity.
- Check every slide at full size and phone-thumbnail size. Reject weak contrast, crowded line breaks, or unclear reading order.

## Copy rules

- Declare `exact-source` or `approved-draft` before design. In `exact-source` mode, preserve every approved word and punctuation mark. Do not improvise hooks, explanations, labels, summaries, or CTA copy.
- Record one campaign content class: `business`, `ugc_creator`, or `influencer`. Record a hook-research pool: `image_carousel`, `video_adaptable`, or `both`. In `approved-draft` mode, query only that class and pool, display source-supplied examples when available, and record selected hook IDs. Video-first hooks require an explicit static-cover adaptation and renewed copy approval. In `exact-source` mode, do not replace supplied copy with a library pattern.
- Treat hook-library entries as reusable patterns, not proof of current trend status or guaranteed performance.
- Freeze approved `copy.md` with SHA-256. Stop production when the file hash changes after approval.
- Write all slide copy before image production.
- Draft at least three materially different hooks. Use five when the first batch is weak or the cover carries unusual commercial risk.
- Keep cover copy specific and legible at thumbnail size. Remove unsupported certainty.
- Make Slide 2 a second hook. It should clarify why the reader should continue.
- Give each slide one job and one primary message.
- Favor concrete language, examples, comparisons, and proof over abstract advice.
- Use open loops only when the next slide closes or advances them.
- Make the payoff worth the swipes. The final value slide should be the strongest insight, not a recap of the hook.
- Use one CTA. Match it to the campaign goal.
- For a comment-to-DM campaign, use one approved comment keyword as the dominant CTA. Never invent a keyword or reuse `IMAGE` unless that exact keyword is approved for the campaign.
- Apply the screenshot test to value slides.

Run AI Sloppy Copy on the complete package. Keep `Hook -> Value -> CTA`. Remove fake quotations and vague superlatives. Remove unsupported numbers plus repetitive conclusions. Repair choppy fragments. Rewrite instructions that masquerade as benefits.

## Reference-first visual brief

Choose two to four references. More references usually create ambiguity. Assign a job to each reference:

- composition and hierarchy;
- typography behavior;
- color and texture;
- character or object treatment;
- photographic treatment.

Do not say only "match this style." State which visual properties are binding and which are excluded. Do not copy a creator's logo, signature, protected character, or distinctive branded trade dress.

## Cover workflow

1. Supply the exact approved cover copy.
2. Supply the client brand assets and assigned visual references.
3. Request exactly three genuinely different compositions, not color swaps.
4. Save all three candidates and their SHA-256 values before selection.
5. Inspect all three at full size and 320 pixels wide.
6. Select one direction.
7. Refine that direction until copy accuracy, hierarchy, brand fit, and curiosity pass.
8. Record human approval and freeze `visual-brief.md` with SHA-256.

No remaining slide may be generated until all three candidate records exist, all three pass the thumbnail check, one is selected, and the anchor approval is recorded.

## Per-slide prompt contract

Each prompt must state:

- output dimensions and platform route;
- slide number and narrative role;
- exact text, including punctuation and line-break preference;
- the approved anchor image as the main style reference;
- the job of every additional reference;
- composition and subject;
- fixed colors, typography behavior, margins, numbering, and logo rules;
- elements that must not appear;
- approved person or likeness asset IDs plus their allowed use;
- a requirement to preserve exact text and generate one slide only.

Keep editable prompt text in `prompts.md`. Never rely on chat history as the only production record.

## Visual QA after every generation

Inspect before continuing:

- exact text and spelling;
- hierarchy and mobile legibility;
- correct dimensions and safe content placement;
- consistency with the approved anchor;
- distinct visual progression;
- no invented claims, logos, UI, people, or product details;
- no unapproved likeness edit or synthetic endorsement;
- no identity drift;
- no accidental watermark or creator signature;
- brand and legal fit;
- cultural fit.

If the slide fails, fix that slide. Do not continue and hope the final review catches it.

When review identifies only named failed slides, preserve every approved slide and regenerate or re-render only the named files.
