# Hook library

## Required intake decision

Before researching or drafting hooks, ask:

**Which content class best describes this client for this campaign: Business, UGC Creator, or Influencer?**

- `business`: the company, professional practice, offer, product, service, or named business expert is the authority.
- `ugc_creator`: the creator demonstrates or reviews an experience. Comparisons and relatable narration also fit when presented in a UGC style.
- `influencer`: the creator's personality, point of view, story, taste, or audience relationship is the central reason to watch.

Save exactly one value in `run.json`: `business`, `ugc_creator`, or `influencer`. A client may use a different class on another campaign. Do not infer the class from industry alone.

Then ask which research pool to use:

- `image_carousel`: carousel-first and cross-format hooks that work as large cover text;
- `video_adaptable`: video-first hooks that need a spoken, motion, timing, or visual-action adaptation before carousel use;
- `both`: compare both pools and record why the selected hook transfers to a static cover.

Crafty Carousels still produces image carousels. This field controls research, not the final deliverable.

## Database

The local source library contains 751 source records:

- `viral-hooks-300.json`: 300 paired hook and example records, 100 per original content class;
- the 351-record categorized hook dataset;
- the 100-record hook-starter dataset. Duplicate source records remain stored and carry `duplicate_of` pointers so the query does not repeat them.

Every record has:

- a stable ID;
- one reusable hook pattern;
- content-class and format-fit routing;
- source provenance;
- a filled example when the source supplied one.

Query only the selected class:

```powershell
python scripts/hook_library.py --content-class business --format image_carousel --count 5
python scripts/hook_library.py --content-class ugc_creator --format video --search "website" --count 10
python scripts/hook_library.py --content-class influencer --format image_carousel --count 5 --json
```

Always display the filled example beside a recommended pattern. The human should not have to guess how placeholders map to a usable sentence.

## Selection controls

The library is an idea source, not a claim that a pattern is currently trending or guaranteed to perform.

1. Filter by the approved content class.
2. Filter by format fit. A video-first hook is not automatically a readable carousel cover.
3. Filter for the campaign topic, tension, desired action, or audience problem.
4. Show three to five candidates with each candidate's record ID and format fit. Include the source-supplied example when available.
5. Adapt placeholders using approved client evidence and voice only.
6. Reject any pattern that requires an unsupported claim or false urgency. Reject fake quotations and invented results. Reject unapproved personal experience.
7. Run AI Sloppy Copy and preserve `Hook -> Value -> CTA`. Then obtain copy approval.
8. Record selected hook IDs in `run.json` before the three anchor-slide compositions are generated.

The 351-record source uses rule-based content-class and format-fit labels. A human must review them. They are routing aids, not performance labels.

For `exact-source` work, do not replace the supplied hook with a library pattern. The selected content class is still recorded, but the source copy remains untouched.
