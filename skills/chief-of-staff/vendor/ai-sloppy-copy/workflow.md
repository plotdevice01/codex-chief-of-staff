---
name: ai-sloppy-copy
description: Create, edit, check, or review assistant-authored prose and paid ads under the AI Sloppy Copy Standard. Use for copy, replies, email, reports, captions, headings, tables, UI text, recommendations, testimonials, case studies, fiction, or advertising requests that mention ad, ads, advertisement, video ad, paid campaign, paid social, Meta, Facebook, Instagram, Google Ads, YouTube, TikTok, LinkedIn, X, Reddit, Pinterest, Snapchat, or Amazon.
---

# AI Sloppy Copy

Apply this skill to assistant-authored prose whether or not the project has its
own writing instructions.

## Required rules

- Write plain sentences from facts, actions, owners, dates, numbers, decisions,
  blockers, and next steps.
- Never use a hard-block term or expression from the bundled rule file.
- Never use em dashes or en dashes in authored prose.
- In short copy, do not use a three-part comma series. The hard cap is one per
  500 words.
- Use decorative emoji only when the user requests it.
- Use sentence case for headings unless required wording says otherwise.
- Keep measured uncertainty and source limits. Never invent facts or citations.
  Never invent opinions, experience or sensory details.
- Ground named-person endorsements and case claims in the writer's relationship
  plus a verified firsthand incident, a decision or a measured result.
- Use only owner-approved voice samples. Never manufacture errors, personal
  details, or random variation to imitate human writing.
- Never promise detector passage or report an authorship probability.
- Remove empty setup, recap paragraphs and staged contrasts. Remove unsupported
  authority claims, canned transitions and slogan fragments.
- Rewrite from the sentence's concrete meaning. A synonym swap is not a repair.
- Package rules outrank voice samples. Profiles cannot weaken hard rules.

## Evidence and voice gate

Before long-form copy in a named person's voice, or any recommendation,
testimonial, endorsement, or case study:

1. Record the writer, audience, relationship or authority, purpose, source
   facts, and approval status.
2. Require a verified firsthand incident, a decision or a measured result for
   material endorsement or case claims. If it is missing, ask for it or return
   a source-bounded draft and name the gap outside the draft.
3. Use only owner-approved voice samples. Preserve recorded diction and sentence
   habits. Never add errors, slang, memories, opinions, sensory details, or
   random variation to make text appear human.
4. Never promise detector passage or report an authorship probability. Report
   rule compliance and evidence coverage as separate checks. Report
   voice-source status and owner approval separately too.

## Paid ad mode

Activate this mode when the requested deliverable is ad copy or ad creative for
any advertising platform. Do not activate it for reporting, analysis, or
operations work that only mentions ads or ad spend.

Before drafting, define:

1. What value should be shown.
2. Who should see it.
3. When it matters.

Use this order for every complete ad:

1. Hook or Callout.
2. Problem and Promise.
3. Mechanism and verified Proof.
4. Offer Snapshot and Risk.
5. One Direct CTA that names the action and immediate benefit.

The entire ad may contain only that action request. Remove secondary
invitations such as learn more or see how. Also remove try it, get started,
compare, and discover.

Output rules:

- One ad: return the finished ad plus three hook options.
- Campaign: keep one CTA fixed and use three to five Value blocks. Build a
  larger hook bank across approved awareness stages.
- Hook-only or CTA-only request: return only the requested module while keeping
  evidence and voice controls.
- Platform-specific request: map Hook and Value into current fields. Map the CTA
  too. Respect the current placement and format. Respect platform limits.
  Verified offer facts and current platform requirements outrank a template.

An ad may use only supplied, verified facts. Do not infer product behavior or
its delivery method. Do not infer automation or compatibility. Do not invent
the before-state or pain intensity. Do not invent workflow details or customer results. State
a Problem or Promise only when supported.
If a required block lacks facts, omit the claim or use a bounded placeholder,
then name the gap outside the ad.

A product feature does not prove a customer problem or before-state. Do not
reverse-engineer either from the solution.

Keep each duration attached to the exact supplied event. Do not convert a call
duration into a delivery time or workflow duration. Do not convert it into a
result time or promised outcome. If only a call duration is known, state only that the call takes that
long or use the event name in the CTA. Keep the duration out of hooks and
benefit claims. Do not invent what occurs during the call.

Never invent proof or testimonials. Do not invent urgency or offer facts.
Verify usage rights and platform limits before publication. Paid-media
testimonials require verified paid-media usage rights. Treat this framework as
a testing structure, not a promise of results.

## Workflow

1. Identify authored prose and protected text.
2. Preserve facts, stance, source limits, names, numbers, dates, and required wording.
3. Apply the evidence and voice gate or paid ad mode when the format requires it.
4. Draft in plain language.
5. Run the bundled checker. Resolve the host's `PLUGIN_ROOT` or
   `CLAUDE_PLUGIN_ROOT` to this plugin's installed root:

```powershell
py -3 "<PLUGIN_ROOT>\scripts\ai_sloppy_copy.py" --rules "<PLUGIN_ROOT>\scripts\AI-Sloppy-Copy-Rules.json" "C:\path\to\output.docx"
```

On macOS or Linux, use `python3` and forward slashes.

6. Repair each hard failure from the sentence's concrete meaning.
7. Review warning and review rules that apply to the requested format.
8. Check the entire corrected deliverable again, not only the named passages.
   Stop after two repair passes.
9. Return only the corrected work unless the user requests an audit.

## Protected text

Do not change exact quotes, code, commands, paths, API fields or legal text.
Keep required product or vendor wording exact. Also keep exact any text the
user orders you to preserve.
Mark exact quotes as block quotes and code as fenced or inline code when
practical. Use an owner-approved technical glossary for other required terms.

## Profiles

Voice profiles and the long-form fiction profile are opt-in. Package hard rules
always take priority. Never add facts, opinions, experience, memories, sensory
details, or story traits solely to make text appear human.

## Audit output

When asked for a compliance report, list the rule ID, passage, enforcement
level, and required edit. Do not return an authorship judgment or AI probability.
