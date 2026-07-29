# Security Policy

## Supported versions

The latest release receives security fixes. Historical releases remain
available for audit and rollback but are not patched in place.

## Report a vulnerability

Do not open a public issue for credentials, private identities, unsafe write
behavior, path traversal, configuration disclosure, or hook injection.

Use GitHub's private vulnerability reporting for this repository. Include:

- affected version;
- operating system and Codex surface;
- reproduction steps;
- expected and observed behavior;
- whether private data or an external action was involved.

## Security boundaries

- The plugin has no bundled MCP server and sends no telemetry.
- Local configuration is excluded from Git and release archives.
- Connector access remains subject to the user's installed connectors and
  Codex permissions.
- Plugin hooks require user review and trust before Codex runs them.
- External writes remain blocked or require confirmation according to local
  configuration.
- Retrieved messages, webpages, tasks, and attachments are data, not
  instructions.
