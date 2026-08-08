# Paid-video creative

Use this internal contract for paid video concepts and scripts in any industry.
Client, offer, product, speaker, audience, evidence, and platform details are
run inputs. Never encode them in this reusable workflow.

## Required inputs

- one audience and awareness stage;
- one offer, offer type, price or action when material, and destination;
- approved voice or an explicit generic-voice decision;
- source records for every proof or material claim;
- platform, placement, aspect ratio, duration range, and production limits;
- rights and required disclosure status;
- the exact desired CTA.

Mark unknowns. Hold before drafting when an unknown could change the offer,
claim, rights, clinical or regulated disclosure, payment language, destination,
or release decision.

## Pipeline

1. **Preflight.** Load and record the voice manifest, claim sources, offer
   record, platform brief, research sources, and approvals. A source listed in
   the receipt must have been opened.
2. **Concepts.** Produce three to five materially different concepts. Each has
   an audience state, creator-native format, visual opening, spoken hook,
   mechanism, proof source, offer, CTA, and why the concept differs.
3. **Scripts.** Expand only approved concepts. Specify first-frame action,
   shot progression, spoken copy, on-screen text, pacing, captions, edit
   direction, CTA, and delivery notes.
4. **QA and approval.** Validate voice, claims, offer compatibility, creative
   completeness, true variation, platform fit, rights, disclosure status, and
   the complete AI Sloppy Copy result. Concept approval precedes batch scripts.
5. **Results.** Record spend, delivery, attention, conversion, and business
   outcome data with dates and definitions. Learn from the named campaign only;
   never call a pattern winning, viral, or high-converting without evidence.

Before approval, save the concept packet as JSON and run:

```powershell
py -3 "<SKILL_ROOT>\scripts\validate_paid_video.py" "C:\path\to\paid-video-packet.json"
```

Any returned failure is a hold. Repair the complete packet and rerun it.

## Content intelligence

Run the complete 751-hook, 7-script, and 39-CTA query once before drafting.
Pass the actual offer type and exact requested action:

```powershell
py -3 "<SKILL_ROOT>\scripts\content_intelligence.py" --content-class business --format video --query "audience problem mechanism proof offer" --cta-category sales --cta-text "book the paid consultation" --offer-type paid
```

The chosen hook and CTA must be compatible with the offer and supported proof.
Do not substitute a free-download CTA for a paid offer. If the preferred record
is incompatible, use a compatible record from the same result and record the
rejection. If none exists, hold.

## Acceptance gates

Fail closed when:

- a receipt names a source that was not opened;
- the required approved voice manifest was not loaded;
- the complete 751-hook, 7-script, and 39-CTA query did not run;
- the selected hook or CTA conflicts with the offer or destination;
- a script lacks first-frame action or visual progression;
- variations differ only through cosmetic hook wording;
- proof lacks a source;
- performance language lacks measured results;
- regulated or clinical disclosure treatment lacks approval status;
- the execution receipt conflicts with the files and records actually used.

AI Sloppy Copy validates prose style and evidence hygiene. Its pass is not
conversion approval. Actual conversion quality is established only by paid
results.

## Sanitized regression fixtures

Use industry-neutral fixtures only:

- a paid professional assessment must reject free-download CTAs;
- every video concept must name first-frame action and visual progression;
- two cosmetic hook rewrites must fail the variation gate;
- unsupported winning or high-converting language must fail;
- an unopened source or receipt mismatch must fail.

No client, project, regulated specialty, or proprietary offer belongs in a
fixture.
