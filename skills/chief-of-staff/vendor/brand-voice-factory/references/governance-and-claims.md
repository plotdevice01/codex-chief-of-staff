# Governance and claims

## Owner map

Assign roles by accountability, not title. One person may hold several roles.

| Role | Accountability |
|---|---|
| Package owner | Adopts voice decisions and approves package changes. |
| Release owner | Records the final decision for the exact asset and use. |
| Claim owner | Confirms the claim and required qualification. |
| Privacy owner | Approves personal-data handling and privacy language. |
| Commercial owner | Approves price, offer, contract, and payment language. |
| Operations owner | Confirms workflow, capacity, timing, and service boundaries. |
| Security owner | Confirms portal, data-flow, access, and security statements. |
| Media owner | Controls public positions and spokesperson use. |
| Rights owner | Confirms quotation, testimonial, likeness, and third-party rights. |
| Domain owner | Confirms destination, redirects, tracking, and public availability. |

An owner assignment is not approval. Store the decision, exact version, scope, date, and source reference.

## Claim classes

| Class | Example | Default route |
|---|---|---|
| Identity | Company name or location | Package owner |
| Offer | Service, price, eligibility, or availability | Commercial and operations owners |
| Performance | Speed, savings, conversion, rank, or result | Claim owner and release owner |
| Regulated | Clinical, legal, financial, privacy, or safety statement | Qualified subject owner plus compliance route |
| Comparative | Better, faster, leading, or unique | Claim owner with comparison method |
| Testimonial | Customer experience or quotation | Rights owner plus claim owner when needed |
| Security | Encryption, certification, access, or data flow | Security and privacy owners |

Use the client's adopted owner matrix. The table gives defaults only.

## Hard release blocks

Set status to `Hold` when any condition applies:

- A material fact has no current source.
- The offer differs from the approved commercial record.
- A required qualification is missing or unreadable.
- Rights for the intended channel are absent.
- The destination, date, price, or availability is unverified.
- A regulated claim lacks the required subject review.
- Personal data appears outside an approved workflow.
- The exact asset version lacks a release decision.

## Privacy

Collect the minimum business information needed for the work. Do not place protected health information in a brand-voice workspace, prompts, connectors, analytics tools, or generated examples. Use fictional records for demonstrations.

## Current-source rule

Browse or use an authoritative connector when a law or platform rule could have changed. Do the same for price and schedule. Verify the current executive identity and product specification. Check the current technical standard when the asset uses it. Prefer primary sources. Record the URL and review date.

## Release record

The record must contain:

- Asset ID and exact filename.
- Version or checksum.
- Intended channel and destination.
- Source packet references.
- Claim decisions.
- Rights and privacy decisions.
- Release owner decision and date.
- Expiration or next review condition.
