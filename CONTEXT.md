# Chief of Staff repository context

Form: Umbrella. The repository contains one discoverable Chief skill, internal
workflows, a pinned content runtime, lifecycle hooks, configuration tooling, validation, and a release
pipeline.

## Route the task

| Need | Read next | Product or state |
|---|---|---|
| Change global behavior | `AGENTS.md` | Shared contract plus persona tests |
| Change Chief workflows | `skills/chief-of-staff/SKILL.md` | Scoped operating workflow |
| Change request routing | `skills/chief-of-staff/references/universal-request-contract.md` | One-pass route and execution receipt |
| Design or restructure work | `skills/chief-of-staff/internal/icm-architect/workflow.md` | Internal ICM workspace or migration plan |
| Create business content | `skills/chief-of-staff/references/content-production.md` | Governed copy, voice package, ad, or carousel run |
| Create paid-video work | `skills/chief-of-staff/references/paid-video-creative.md` | Complete concepts, scripts, QA, and results loop |
| Update pinned content resources | `scripts/sync_content_runtime.py` | Hash-locked Chief content runtime |
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
