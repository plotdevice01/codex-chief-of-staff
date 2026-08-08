# Configuration

Chief of Staff keeps behavior in the plugin and private authority in
`chief-of-staff.json`. Plan-scoped authorization requires
`config_schema_version: 2`.

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
  "allowed_actions": ["read", "draft", "send"],
  "external_writes": "plan_scoped"
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
- `plan_scoped`.

`automatic_authority_expansion` must remain `false`. Authority changes only
through an explicit owner-approved configuration update. A direct request,
approved plan, approved goal, or full-access instruction is durable
authorization for every plainly included action through completion. Reconfirm
only for a material scope expansion or missing material decision. The owner may
steer or revoke the authorization at any time.

The policy object must also contain:

```json
{
  "plan_scoped_authorization": {
    "full_access_instruction": "all_in_scope_actions_until_completion",
    "reconfirm_only_for": "material_scope_change_or_missing_material_decision",
    "safe_retries_do_not_reconfirm": true,
    "owner_can_steer_or_revoke": true
  }
}
```

## Validate

```bash
python validate_install.py
python Test-Persona.py
```

Use `--strict-dependencies` when full reference-install parity is required.
