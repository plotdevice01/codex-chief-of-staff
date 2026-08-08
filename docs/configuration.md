# Configuration

Chief of Staff keeps behavior in the plugin and private authority in
`chief-of-staff.json`.

## Resolution order

1. `CHIEF_OF_STAFF_CONFIG`.
2. `chief-of-staff.json` in the active workspace or manual install.
3. Codex `PLUGIN_DATA`.
4. Platform configuration:
   - Windows: `%APPDATA%\codex-chief-of-staff\chief-of-staff.json`
   - macOS and Linux:
     `~/.config/codex-chief-of-staff/chief-of-staff.json`
   - `XDG_CONFIG_HOME` replaces `~/.config` when set.

## Owner

Set:

- `owner.name`;
- `owner.timezone` using an IANA timezone such as `America/Chicago`;
- `owner.role`;
- `owner.operating_profile`;
- `owner.recurring_work` as a list.

The public template uses a generic operator-builder profile. Keep private
owner-specific work context in the ignored local configuration.

## Connectors

Connectors are disabled by omission. Add a connector only when the user wants
Chief of Staff to use it.

```json
{
  "id": "team_chat",
  "enabled": true,
  "provider": "Slack",
  "expected_identity": {
    "email": "operator@example.com",
    "workspace": "Example Workspace",
    "user_id": "U0123456789"
  },
  "denied_identities": [],
  "allowed_actions": ["read", "draft"],
  "external_writes": "confirm_each"
}
```

Never store passwords, API keys, OAuth tokens, or session cookies in this
file.

## Projects

```json
{
  "id": "operations",
  "name": "Operations",
  "scope": "operations",
  "enabled": true,
  "paths": ["C:\\Users\\Example\\Documents\\Operations"],
  "instructions": "C:\\Users\\Example\\Documents\\Operations\\AGENTS.md"
}
```

Use absolute paths. The `instructions` field is optional. Project-specific
privacy, compliance, source, hook and skill rules remain in each project's
marked section. Propagation replaces only the Chief-managed fail-safe loader;
it does not replace that project section.

The lifecycle hook supplies the complete canonical Chief contract and persona
once per session. The loader reads those same canonical sources only if the
hook header is absent. This removes repeated copies without creating two
different behavior contracts.

## Execution tiers

Only two tiers are supported:

- `standard`: GPT-5.6 Sol Medium, relevant workspace and source inspection,
  plus focused, proportional validators;
- `expert_high_risk`: GPT-5.6 Sol High or Extra High when available, inspection
  of all affected boundaries, the full relevant validator suite, failure-path
  checks, parity checks and read-back.

There is no quick tier. Keep `execution.quick_tier_enabled` set to `false`.
Expert/high-risk applies to explicit expert or deep requests and to release,
security, legal, medical, financial, production, permission, public-write,
destructive, cross-project and multi-system work.

## Policy

Supported external-write values:

- `blocked`;
- `confirm_each`.

`automatic_authority_expansion` must remain `false`. Authority changes only
through an explicit owner-approved configuration update. Repeated approval does
not create standing permission.

## Validate

```bash
python validate_install.py
python Test-Persona.py
```

Use `--strict-dependencies` when full reference-install parity is required.
