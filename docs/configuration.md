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
- `owner.timezone` using an IANA timezone such as `America/Chicago`.

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
privacy, compliance and source rules remain separate from the shared managed
contract.

## Policy

Supported external-write values:

- `blocked`;
- `confirm_each`.

`automatic_authority_expansion` must remain `false`. A completed pilot or date
does not create standing permission. Repeated approval does not create it either.

## Validate

```bash
python validate_install.py
python Test-Persona.py
```

Use `--strict-dependencies` when full reference-install parity is required.
