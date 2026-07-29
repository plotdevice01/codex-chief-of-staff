# Privacy

Chief of Staff is a local, skills-only plugin. It does not operate a server,
collect telemetry, or transmit configuration to the maintainer.

The plugin can instruct Codex to use connectors that the user has separately
installed and authorized. Connector providers, Codex and the user's workspace
policies govern that access.

Local `chief-of-staff.json` files may contain account identities, denied
identities, project paths and approval rules. They are excluded from Git and
release archives. Users are responsible for keeping them private.

The repository contains a generic persona source and no user-specific account
configuration.
