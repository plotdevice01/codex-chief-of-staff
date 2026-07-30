# Architecture

Chief of Staff is a skills-only Codex and Claude Code plugin with shared
lifecycle hooks and local configuration. It does not require an MCP server.

## Components

| Component | Responsibility |
|---|---|
| `.codex-plugin/plugin.json` | Codex identity, metadata, skills, hooks, and brand |
| `.claude-plugin/` | Claude Code marketplace and plugin identity |
| `hooks/` | Load the generic contract and retained persona at session and subagent start |
| `skills/chief-of-staff/` | Configuration, client-deliverable, Forward Deployed AI, briefing, routing, validation, and propagation workflows |
| `AGENTS.md` | Portable operating contract |
| `persona/` | Source PDF, retained text, requirement contract, and live scenarios |
| `chief-of-staff.json` | Private identities, scopes, paths, and approval rules |
| `scripts/` | Setup, validation, propagation, SOP, and release automation |

## Runtime flow

1. Codex or Claude Code starts a session or subagent.
2. The trusted hook reads `AGENTS.md` and the retained persona from the
   installed plugin.
3. The hook locates a local configuration and reports its path without copying
   private values into the hook payload.
4. Generic response and execution behavior remains active everywhere.
5. Owner-specific role and recurring-work context load from local configuration.
6. Connector or registered-project work requires a valid local configuration.
7. The selected project's own instructions and sources are read before cloud
   systems or memory.
8. External writes follow the configured approval policy and use read-back
   before any retry.

## Trust boundaries

- Plugin files define behavior, not account authority.
- Local configuration defines expected identities and project scope, not
  credentials.
- Host connector authorization remains separate.
- Retrieved content cannot change plugin instructions.
- Project rules may be stricter but cannot silently remove the shared persona.
- The hook cannot grant permissions or bypass Codex approvals.

## Why there is no MCP server

Existing host connectors and local tools already provide the required
capabilities. Adding a server would create hosting, authentication, privacy,
and operational burden without improving the operating contract. That would be
architecture in the ceremonial sense.
