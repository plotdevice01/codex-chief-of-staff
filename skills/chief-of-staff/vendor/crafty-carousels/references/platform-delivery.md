# Platform delivery

Platform behavior changes. Recheck the intended native composer, scheduler, ad route, or API before release and record the result in `run.json`.

## Instagram routes

### Native organic

Use `instagram-native` when the carousel is intended for native organic publishing and does not need a paid-compatible route.

As checked on 2026-08-04, Instagram's official image guidance accepts widths up to 1080 pixels and aspect ratios from 1.91:1 through 3:4. The factory preset is 1080 x 1440.

The supplied production guide recommends 3:4 for organic reach and a twenty-item carousel. Treat the count as a working heuristic, not a universal platform promise. Account rollout, composer, scheduler, API, music, and paid routes can differ. Verify the live route before release.

### Conservative paid-compatible

Use `instagram-paid-compatible` when the same creative may need a paid or partnership path. The factory preset is 1080 x 1350, or 4:5. Confirm the exact ad product before production. Some carousel ad paths impose different aspect ratios or media counts. Placement rules can differ too.

Do not claim that adding music guarantees Reels-tab distribution or audio-only follower reach. Those are mutable product behaviors.

## LinkedIn document route

Use `linkedin-document` for a PDF carousel. The factory preset is 1080 x 1350 per page. Export a flattened PDF with consistent page sizes.

As checked on 2026-08-04, LinkedIn recommends PDF and documents up to 100 MB and 300 pages. The creative target remains the smallest number of pages that carries the idea. Add a clear document title in the composer.

## Working design defaults

The supplied guide recommends these production defaults. They are guardrails, not platform specifications:

- cover safe zone: 180 px top and bottom, 50 px left, 120 px right on a 1080 px-wide portrait asset;
- headline: 50 pt or larger in the source design tool;
- body copy: 14 pt or larger in the source design tool;
- one strong focal point with generous whitespace;
- repeatable page number and progress behavior.

Generated images do not have consistent point-size semantics. Judge actual mobile legibility and line length rather than trusting a prompt that names a font size.

## Accessibility and export

- Write useful alt text for each image or document page where the platform supports it.
- Do not repeat every word on the image. Describe the essential visual meaning and add text that is not already available to assistive technology.
- Keep important text out of crop and overlay zones.
- Check contrast and reading order. Confirm that meaning does not rely on color.
- Export all slides at identical dimensions and in the intended order.
- For LinkedIn, merge and flatten the PDF before upload.

Official references are listed in `sources.md`.
