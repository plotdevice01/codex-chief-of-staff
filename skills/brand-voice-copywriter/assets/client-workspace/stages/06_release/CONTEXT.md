# 06_release

One job: record QA results and the release decision for the exact asset.

## Inputs

- Working: `../05_copy/output/asset-draft.<format>`
- Working: `../05_copy/output/source-packet.md`
- Working: `../05_copy/output/copy-qa.json`
- Template: `_templates/approval-record.md`
- Reference: `_shared/release-policy.md`

## Process

1. Confirm the asset checksum and destination.
2. Route claim, rights, privacy, channel, and commercial decisions.
3. Record the release owner's decision.
4. Set `Public ready` only when every hard gate passes.

## Outputs

- `approval-record.md`
- `release-copy.<format>`
- `test-record.md`

## Human check

The release owner approves or holds the exact version for its named destination.
