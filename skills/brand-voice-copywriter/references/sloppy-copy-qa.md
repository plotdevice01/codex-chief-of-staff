# AI Sloppy Copy QA

Use the installed AI Sloppy Copy skill and checker. The current Chief dependency requires plugin release `0.5.0` or later with Standard `2.2.0` or later. Verify the installed version when release behavior matters.

## Check sequence

1. Draft from approved facts and voice controls.
2. Protect only exact quotations, required legal text, code, paths, and approved named terminology.
3. Run the checker on the complete asset.
4. Rewrite every failed sentence from its concrete meaning.
5. Run the checker on the complete asset again.
6. Stop after two repair passes. If hard failures remain, return only their rule IDs and hold the asset.

Do not use a synonym swap as the repair. Do not inspect only the sentence named by the first report.

## Local command

Locate the active plugin copy first. Then run its checker:

```powershell
python <ai-sloppy-copy-root>\scripts\ai_sloppy_copy.py --json <asset-path>
```

For DOCX, pass the document path directly. For a workbook, extract assistant-authored prose from every sheet and check the assembled text. Preserve formulas and source data outside the authored-prose input.

## Glossary rule

Use a narrow glossary for approved client names, product names, required industry terms, or exact controlled wording. Store the approval source beside the glossary entry.

A glossary may suppress a language rule for the exact term. It cannot approve a claim or erase a disclosure. It cannot change a rights requirement.

## QA record

Record:

- Asset ID and checksum.
- Checker version and Standard version.
- Rules allowed by ID or glossary entry.
- Pass count and remaining rule IDs.
- Human reviewer and decision.

AI Sloppy Copy is a prose gate. It does not prove truth or legal compliance. It does not prove conversion performance or brand approval.
