# Architecture

Chief of Staff is an Agent Plugins 1.0 package with one discoverable skill,
shared
lifecycle hooks, local configuration, and default Interpretable Context
Methodology. It does not require an MCP server.

## Components

| Component | Responsibility |
|---|---|
| `plugin.json` | Portable Agent Plugins 1.0 manifest; its core discovers one immediate Chief skill |
| `.codex-plugin/plugin.json` | Shared ChatGPT Work and Codex manifest for identity, metadata, skills, hooks, and brand |
| `hooks/` | Load the generic contract once and the retained persona at session and subagent start |
| `CONTEXT.md` | Layer 1 repository routing and factory-product boundary |
| `skills/chief-of-staff/` | The only discoverable skill, universal router, internal contracts, scripts, and vendored workflows |
| `skills/chief-of-staff/internal/icm-architect/` | Internal pinned ICM build and restructure method, forms, references, and templates |
| `AGENTS.md` | Portable operating contract |
| `persona/` | Source PDF and retained text, plus the requirement contract and live scenarios |
| `chief-of-staff.json` | Private identities, scopes, paths, and approval rules |
| `scripts/` | Setup, validation, propagation, SOP, and release automation |
| `workflows/release/` | ICM release contracts and publication gate |

## Runtime flow

1. ChatGPT Work or Codex starts a task or subagent.
2. The trusted hook reads the retained persona from the installed plugin.
   Codex receives the complete contract only when its instruction chain does
   not already contain it. ChatGPT Work uses the bundled skill contract and
   supported plugin context; Codex-only hooks remain optional host extensions.
3. The hook locates a local configuration and reports its path without copying
   private values into the hook payload.
4. Generic response and execution behavior remains active everywhere.
5. Owner-specific role and recurring-work context load from local configuration.
6. Connector or registered-project work requires a valid local configuration.
7. A small fail-safe loader preserves each selected project's unique rules and
   points to the canonical contract if hook context is absent.
8. Chief classifies the request once and loads only the selected internal contracts.
9. Chief applies the compact ICM task contract and loads only its exact inputs.
10. A new project or workspace loads internal ICM Architect automatically. A recurring
   process does too. Full folders appear only when persistent work needs them.
11. The selected project's own instructions and sources are read before cloud
   systems or memory.
12. External writes follow the configured approval policy and use read-back
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
