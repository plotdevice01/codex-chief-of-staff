# Production system

## Core model

Use one sharp idea per carousel. Build copy first, approve the cover as the visual anchor, then produce one slide at a time.

The default eight-slide arc is:

| Slide | Job | Test |
|---|---|---|
| 1 | Hook | Stops the right reader and creates specific curiosity |
| 2 | Transition | States the gain, avoided loss, or credible reason to continue |
| 3-6 | Tease and value | Reveals one useful unit at a time with proof or examples |
| 7 | Climax or payoff | Delivers the clearest insight, reveal, or summary |
| 8 | Action | Makes one next step obvious |

Use fewer slides when the idea is smaller. Add slides only when each new slide contributes a distinct proof point, step, example, objection, or reveal. Do not pad a carousel to hit a preferred count.

## Copy rules

- Write all slide copy before image production.
- Draft at least three materially different hooks. Use five when the first batch is weak or the cover carries unusual commercial risk.
- Keep cover copy specific and legible at thumbnail size. Remove unsupported certainty.
- Make Slide 2 a second hook. It should clarify why the reader should continue.
- Give each slide one job and one primary message.
- Favor concrete language, examples, comparisons, and proof over abstract advice.
- Use open loops only when the next slide closes or advances them.
- Make the payoff worth the swipes. The final value slide should be the strongest insight, not a recap of the hook.
- Use one CTA. Match it to the campaign goal.
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
3. Request three genuinely different compositions, not color swaps.
4. Inspect at full size and thumbnail size.
5. Select one direction.
6. Refine that direction until copy accuracy, hierarchy, brand fit, and curiosity pass.
7. Record human approval and freeze the anchor rules.

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
