# 02_evidence

One job: classify sources and build the claim record.

## Inputs

- Working: `../01_intake/output/client-intake.md`
- Working: source files supplied for this client
- Reference: `_shared/evidence-policy.md`
- Template: `_templates/source-register.csv`
- Template: `_templates/claim-register.csv`

## Process

1. Inventory every source and record its allowed use.
2. Extract facts and aggregate voice patterns separately.
3. Record each material claim and its owner route.
4. Put conflicts or missing support in the gap list.

## Outputs

- `source-register.csv`
- `claim-register.csv`
- `voice-evidence.md`
- `gap-list.md`

## Human check

The package owner confirms which evidence may shape the corporate voice. Claim owners confirm only their assigned rows.
