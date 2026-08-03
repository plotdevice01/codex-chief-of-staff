# Chief of Staff repository context

Form: umbrella. The repository contains one operating contract, two bundled
skills, lifecycle hooks, configuration tooling, validation, and a release
pipeline.

## Route the task

| Need | Read next | Product or state |
|---|---|---|
| Change global behavior | `AGENTS.md` | Shared contract plus persona tests |
| Change Chief workflows | `skills/chief-of-staff/SKILL.md` | Scoped operating workflow |
| Design or restructure work | `skills/icm-architect/SKILL.md` | ICM workspace or migration plan |
| Change hooks | `hooks/chief-of-staff-hook.js` | Session and subagent payload |
| Change configuration | `docs/configuration.md`, then `scripts/configure.py` | Local ignored configuration |
| Validate source | `docs/testing.md` | Test evidence |
| Build or publish | `workflows/release/CONTEXT.md` | Candidate archive or public release |

## Factory and product

Stable factory material lives in `AGENTS.md`, `persona/`, `skills/`, `hooks/`,
`scripts/`, `docs/`, and manifests. Per-run product belongs in ignored `dist/`,
`qa/`, or a configured local workspace. Never place private configuration or
project data in the public source tree.

## Status

Use Git status for source state. Use test output for validation state. Use
`dist/codex-chief-of-staff-v{version}/release-validation.json` for candidate
state. A public release exists only after its branch, tag, asset, checksum,
attestation, CI result, and fresh-host behavior are verified.
