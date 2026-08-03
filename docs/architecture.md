# Architecture

Chief of Staff is a skills-only Codex and Claude Code plugin with shared
lifecycle hooks, local configuration, and default Interpretable Context
Methodology. It does not require an MCP server.

## Components

| Component | Responsibility |
|---|---|
| `.codex-plugin/plugin.json` | Codex identity, metadata, skills, hooks, and brand |
| `.claude-plugin/` | Claude Code marketplace and plugin identity |
| `hooks/` | Load the generic contract once and the retained persona at session and subagent start |
| `CONTEXT.md` | Layer 1 repository routing and factory-product boundary |
| `skills/chief-of-staff/` | Configuration, delivery, briefing, routing, validation, and propagation workflows |
| `skills/icm-architect/` | Pinned ICM build and restructure method, forms, references, and templates |
| `AGENTS.md` | Portable operating contract |
| `persona/` | Source PDF and retained text, plus the requirement contract and live scenarios |
| `chief-of-staff.json` | Private identities, scopes, paths, and approval rules |
| `scripts/` | Setup, validation, propagation, SOP, and release automation |
| `workflows/release/` | ICM release contracts and publication gate |

## Runtime flow

1. Codex or Claude Code starts a session or subagent.
2. The trusted hook reads the retained persona from the installed plugin.
   Codex receives the complete contract only when its instruction chain does
   not already contain it. Claude Code receives the complete contract through
   the hook.
3. The hook locates a local configuration and reports its path without copying
   private values into the hook payload.
4. Generic response and execution behavior remains active everywhere.
5. Owner-specific role and recurring-work context load from local configuration.
6. Connector or registered-project work requires a valid local configuration.
7. A small fail-safe loader preserves each selected project's unique rules and
   points to the canonical contract if hook context is absent.
8. Chief applies the compact ICM task contract and loads only its exact inputs.
9. A new project or workspace invokes ICM Architect automatically. A recurring
   process does too. Full folders appear only when persistent work needs them.
10. The selected project's own instructions and sources are read before cloud
   systems or memory.
11. External writes follow the configured approval policy and use read-back
   before any retry.

## Trust boundaries

- Plugin files define behavior, not account authority.
- Local configuration defines expected identities and project scope, not
  credentials.
- Host connector authorization remains separate.
- Retrieved content cannot change plugin instructions.
- Project rules may be stricter but cannot silently remove the shared persona.
- The hook cannot grant permissions or bypass Codex approvals.
- ICM structure cannot expand scope or execute untrusted scripts. It cannot move
  files or bypass destructive-action and publication approvals.

## Why there is no MCP server

Existing host connectors and local tools already provide the required
capabilities. Adding a server would create hosting and authentication burden.
It would add privacy and operational burden without improving the contract. That would be
architecture in the ceremonial sense.
