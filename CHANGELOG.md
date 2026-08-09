# Changelog

All notable changes are recorded here. Public releases and host manifests use
the same three-part semantic product version.

## [2.2.0] - 2026-08-08

### Changed

- Replaced per-write `confirm_each` policy with durable `plan_scoped`
  authorization. A direct request, approved plan, approved goal, or full-access
  instruction now covers every plainly included local and external action
  through completion.
- Removed redundant confirmation gates from client-delivery batches, project
  propagation, repository publication, and release workflows.
- Removed the stale v2.1.0 host receipt from the active source and install
  package so its superseded approval behavior cannot be mistaken for policy.
- Changed operational closeout to numbered next steps followed by the execution
  trace. Available authorized steps must be completed before they are listed,
  and a closing summary may not be inserted before the trace.
- Limited reconfirmation to material scope expansion, a new target or
  recipient, an unplanned irreversible destructive action, or a missing
  decision that can change a material outcome.
- Preserved identity checks, blocked financial actions, evidence and rights
  gates, missing credentials, and host or system safeguards.

### Added

- Added explicit plan-scoped authorization context to the lifecycle hook.
- Added a live regression scenario proving that an approved repository publish
  plan proceeds through merge and release without another permission prompt.
- Added an installed-cache proof gate covering active version, exact path,
  stale-version removal, canonical parity, project-loader parity, and a visual
  receipt.

### Validation

- This release changes model-facing behavior. Prior host receipts are not
  carried forward; fresh Codex and ChatGPT Work acceptance is required before
  a public release is tagged.

## [2.1.2] - 2026-08-08

### Fixed

- Changed project synchronization to replace only Chief's managed loader block.
  Project-owned instructions before, between, or after the managed sections are
  now preserved exactly.
- Added regression coverage for project-local suffix and prefix preservation.
- Removed stale OpenAI directory-submission scaffolding that described steps
  the project did not take.
- Corrected both repository installers so upgrade mode re-registers the local
  checkout instead of calling a Git-only marketplace command.
- Aligned the repository release, registered project loaders, and installed
  cache on one immutable patch version.

### Distribution

- The GitHub repository and its bundled installer scripts remain the only
  documented installation path.
- Historical `v2.1.1` assets remain immutable; these corrections ship as
  `v2.1.2`.

## [2.1.1] - 2026-08-07

### Changed

- Made the GitHub repository and its bundled installer scripts the only
  documented installation path.
- Marked AI Sloppy Copy as a pinned upstream runtime source. Brand Voice
  Factory and Crafty Carousels have the same role. None is a separate
  team-facing plugin selection.
- Removed unperformed third-party submission, approval, directory, and
  workspace-rollout steps from public installation guidance.
- Replaced expired time-boxed authority language with the durable local policy
  model. Authority changes only through an owner-approved configuration update.

### Added

- Added an immutable-release rule: packaged SOP corrections require a patch
  release instead of replacing the v2.1.0 ZIP.

### Verification

- Runtime and model-facing behavior remain unchanged from v2.1.0. Its fresh
  Sol Medium ChatGPT Work and Codex evidence is carried forward with an explicit
  reason. A fresh v2.1.1 installed-runtime smoke validates package plumbing.
- Terra remains pending under the version-bound owner waiver.

## [2.1.0] - 2026-08-06

### Changed

- Made Chief the only discoverable skill and the universal route for business,
  creative, research, operational, document, technical, connected-app, and
  client-delivery work.
- Moved ICM Architect under Chief as an internal progressively loaded workflow.
- Replaced the stale bundled carousel skill with pinned runtime files from AI
  Sloppy Copy `0.5.0`, Brand Voice Factory `0.2.1`, and Crafty Carousels `0.6.1`.
- Removed the Ponytail dependency and standalone installation path.
- Added the Agent Plugins v1 root manifest.
- Limited the active build to ChatGPT Work and Codex. Removed the Claude Code
  manifest, marketplace, installers, templates, documentation, and acceptance gate.
- Replaced the legacy marketplace catalog with OpenAI's
  `.agents/plugins/marketplace.json` layout.
- Changed inline AI Sloppy Copy validation to use `--text` so chat drafts are
  not written to temporary files solely for checking.
- Corrected ChatGPT Work acceptance to use its visible **Work locally** and
  **Ask for approval** controls. Corrected Codex acceptance to use an
  ephemeral CLI run with an enforced read-only sandbox; the Desktop approval
  presets are no longer mislabeled as a `Read-only` UI option.
- Sealed live acceptance now embeds installed Chief sources, the complete
  LIVE-014 content query, and inline AI Sloppy Copy evidence before the model
  run. The model makes zero tool calls, avoiding native Windows sandbox process
  failures without weakening the read-only or never-approve controls.
- Separated owner-verified Work UI evidence from agent-observed runtime
  evidence. A `codex` runtime is valid beneath the Work UI and no longer causes
  a false host mismatch.

### Added

- Added a hash-locked content-runtime manifest and deterministic source sync.
- Added one complete content query across 751 hooks, seven script frameworks,
  and 39 CTAs.
- Added content-mode routing and a mandatory execution receipt.
- Added a universal one-pass request contract and capability registry.
- Added a generic paid-video workflow, offer-compatible CTA ranking, and
  sanitized regression fixtures for creative completeness and receipt truth.
- Added a host-verified, response-only live-acceptance harness that requires
  the host's own safety control and rejects task delegation, file mutations,
  connector calls, host substitution, and partial-pass reuse.

### Verification

- Fresh GPT-5.6 Sol Medium acceptance passed all 15 scenarios and 77 assertions
  in both ChatGPT Work and Codex. Both response-only runs reported zero
  forbidden actions. Terra XHigh remains pending under the recorded
  version-bound owner waiver.

## [2.0.1] - 2026-08-05

### Added

- Added a mandatory execution trace for non-trivial tasks and every task that
  names or automatically routes a skill or plugin.
- Distinguished loading a skill from materially using its workflow, inputs,
  handoffs, and validation.
- Added live acceptance coverage for partial or fake Crafty utilization.

## [2.0.0] - 2026-08-05

### Changed

- Made Brand Voice Factory the only owner of `brand-voice-copywriter` and
  removed Chief's duplicate bundled copy.
- Added complete-stack installation and update coverage for Ponytail, AI
  Sloppy Copy, Brand Voice Factory, Crafty Carousels, and Chief of Staff.
- Added strict duplicate-skill detection plus machine-readable install
  receipts with active paths, versions, manifests, hashes, and skill IDs.
- Added the governed Brand Voice to Crafty handoff and AI Sloppy Copy release
  check to Chief's content-production route.
- Raised full-parity minimums to Brand Voice Factory `0.2.0` and Crafty
  Carousels `0.6.0`.

### Verification

- Reset model and host evidence for fresh v2.0.0 acceptance. No v1.0.0 result
  is carried forward.

## [1.0.0] - 2026-08-03

### Added

- Added a default ICM task kernel to the shared Chief behavior contract.
- Bundled ICM Architect from `RinDig/icm-architect` commit `8f9cdf9` with its
  MIT license. It includes five forms and ten invariants. Both operating modes,
  Codex routing and the cold walk remain intact under Chief safety controls.
- Added repository and release `CONTEXT.md` contracts. Added a conformance
  matrix with deterministic ICM validation. Added a cold-walk failure fixture
  and four ICM live acceptance scenarios.
- Added Claude Code prompt and stop-hook enforcement for analysis, debugging,
  contained changes, and ICM architecture responses. It includes a
  two-correction ceiling and a recovery bypass.
- Added a pre-tool privacy decision so private configured context is blocked
  before a tool request can expose it.
- Added bounded read-only inventory for repository restructuring. Mutation is
  blocked until approval. Reference checks and content proof are required
  before any deletion proposal.

### Changed

- Each new project or workspace invokes ICM Architect automatically. Recurring
  processes do too. Contained tasks use the compact contract without ceremonial
  folders.
- Updated the complete-stack dependency to AI Sloppy Copy `0.5.0`. Standard
  `2.2.0` or later is required.
- Adopted one product version for the GitHub release, tag, ZIP, and both host
  manifests.
- Updated strict validation and installation guidance. Release evidence and the
  generated SOP now require the same dependency line.
- Local candidate builds preserve pending or failed model evidence when its
  status is accurate. A public build may use a version-bound owner waiver for a
  pending Sol or Terra check. Failed checks cannot be waived. Host acceptance
  and installed-runtime smoke must pass.
- Sol, Codex, Claude Code, and installed-runtime checks passed for v1.0.0. The
  Terra run remains pending under the recorded owner waiver.

### Fixed

- Removed an exact debug heading that conflicted with AI Sloppy Copy
  `TERM-078`. The replacement still requires the smallest root-cause fix.
- Constrained real-time and restructure responses so required Chief fields do
  not force excess list patterns. Repository inventory is collected once, then
  only evidence checks may use follow-up reads.

### Preserved

- All 97 retained persona requirements and account gates remain. Privacy
  boundaries and project-rule preservation remain. Action approvals and
  external-write controls remain too.

## [0.6] - 2026-07-30

### Changed

- Reset public release numbering from `0.5.2` to `0.6`. One-decimal
  milestones now state the project's pre-1.0 status without pretending every
  internal iteration deserves another dot.
- `0.6` is the successor to, and fully contains, `0.5.2`; the shorter number
  is a numbering reset, not a capability or behavior rollback.
- Codex and Claude Code manifests use `0.6.0` because their plugin formats
  require strict three-part semantic versions. The public release, Git tag,
  documentation, and ZIP use `0.6`.
- The complete stack now requires AI Sloppy Copy release `0.3`. Its host
  manifest reports `0.3.0` for the same compatibility reason.

### Preserved

- The complete persona source and all 97 traceable requirements.
- Sol Medium and expert/high-risk routing, 85% compression, caveman mode,
  direct-reply humor, project-rule preservation, account gates, approval
  controls, Ponytail behavior, and every AI Sloppy Copy rule.

## [0.5.2] - 2026-07-30

### Changed

- Standard work now defaults to GPT-5.6 Sol Medium. Expert/high-risk work uses
  Sol High or Extra High when available. No quick tier exists.
- Project propagation now installs a small fail-safe loader instead of copying
  the complete operating contract into every global and project `AGENTS.md`.
- The Codex session hook omits contract injection when Codex already loaded the
  canonical block. Claude Code still receives the complete contract and
  persona through the hook.
- The complete stack now requires AI Sloppy Copy 2.2.6 or later.

### Preserved

- The complete persona source and all 97 requirements.
- Every project-specific rule, verified before and after migration.
- Full Ponytail behavior, AI Sloppy Copy rules, account gates and approval
  controls.
- Evidence boundaries and local-portable parity.

## [0.5.1] - 2026-07-29

### Added

- First-class Claude Code marketplace, installation, update, removal, and team
  deployment guidance.
- Cross-platform Claude Code installers and a shareable project settings
  example for the complete three-plugin stack.
- Dual-host hook tests for Codex and Claude Code session and subagent startup.

### Changed

- Shared lifecycle hooks now resolve both `PLUGIN_ROOT` and
  `CLAUDE_PLUGIN_ROOT`.
- The public landing page now documents the v0.5 optimization, the preserved
  persona and controls, and the Codex/Claude Code capability matrix.
- The complete stack now requires AI Sloppy Copy 2.2.5 or later for matching
  Claude Code marketplace support and Python 3.10 or 3.11 input parsing.

No persona requirement, response mode, safety control or authority boundary was
removed. No Ponytail capability or AI Sloppy Copy rule was removed.

## [0.5.0] - 2026-07-29

### Changed

- Consolidated duplicated base instructions while preserving their meaning.
- Moved the complete client-deliverable and Forward Deployed AI workflows into
  the existing Chief skill.
- Moved daily-briefing and project-propagation workflows into the same skill.
- Replaced the partial Ponytail copy with a router to the complete installed
  Ponytail plugin while retaining a safety-first fallback.
- Replaced `Execute once` with idempotent external-write and read-back rules.
- Moved owner-specific role and recurring-work context into local
  configuration.

### Preserved

- The complete persona source and all 97 requirements.
- Full Ponytail v4.8.4 behavior, modes, skills, and lifecycle hooks.
- AI Sloppy Copy global enforcement and rule counts.
- Evidence and voice gates remain. Protected text and two-pass repair behavior
  remain too.
- Account, scope, privacy, sensitive-data, and external-write controls.
- Project-specific rules, hooks, commands, skills, and source references.

### Fixed

- Strict dependency validation now checks companion capabilities, not only
  version numbers.
- AI Sloppy Copy plugin 2.2.3 with Standard 2.1.1 masks HTML and XML tag
  structure while still detecting blocked terms in visible prose.
- Each previously under-specified acceptance prompt now supplies its test
  input. Caveman supplies commands. The vulnerable-user case supplies a plan.
  The code case supplies a bug.

## [0.4.5] - 2026-07-29

### Changed

- The recommended installation is now one numbered flow: Ponytail, AI Sloppy
  Copy, Chief of Staff, hook trust, verification, configuration, and
  full-parity validation.
- README and the installation guide now include direct repository links.
  The dependency guide and SOP include the same exact plugin commands.
- Repository validation now fails if ordered install steps or dependency links
  drift. It also checks commands and SOP hyperlinks.

No persona, safety, authority, privacy, or project-preservation rule changed.

## [0.4.4] - 2026-07-29

### Fixed

- Generated release evidence now uses explicit UTF-8 and LF bytes on every
  host, eliminating the final Windows/Linux archive difference.

No behavior, persona, safety or scope rule changed.

## [0.4.3] - 2026-07-29

### Fixed

- Release evidence now records companion requirements instead of
  machine-specific installation warnings.

No behavior, persona, safety or scope rule changed.

## [0.4.2] - 2026-07-29

### Fixed

- ZIP origin metadata is now explicit, removing the final Windows/Linux digest
  difference.

No behavior, persona, safety or scope rule changed.

## [0.4.1] - 2026-07-29

### Fixed

- Canonical DOCX and release ZIP entries now use deterministic storage across
  Windows and Linux.
- Local and GitHub release archives now produce the same SHA-256 digest.

No behavior, persona, safety or scope rule changed.

## [0.4.0] - 2026-07-29

### Added

- Native Codex plugin manifest and GitHub-backed marketplace installation.
- Session and subagent hooks that load the full behavior contract and retained
  persona.
- Safe, machine-independent configuration initialization and path resolution.
- PowerShell and POSIX installers. Both support dry runs, upgrades and
  uninstall.
- Canonical source layout and automated validation with tag-driven releases.
- MIT license, security policy, privacy policy, contribution guide, issue
  templates, examples, architecture documentation, and brand assets.
- Reproducible release ZIP generation with SHA-256 verification.

### Changed

- The primary install is now two Codex plugin commands.
- Checksum verification moved out of the quick-start path.
- Connectors and project routing remain disabled until a local configuration
  exists.

### Preserved

- The complete Technical Assistant Persona source and all 97 requirements.
- 85% compression and caveman mode, plus dry sarcasm, cynical humor and witty advice.
- Professional external-tone boundaries.
- Ponytail execution discipline and AI Sloppy Copy v2.1 requirements.
- Project rule preservation and account identity gates with approval controls.

## [0.3.1] - 2026-07-29

- First public portable release with persona validation and project
  propagation.

[0.6]: https://github.com/plotdevice01/codex-chief-of-staff/releases/tag/v0.6
[0.5.2]: https://github.com/plotdevice01/codex-chief-of-staff/releases/tag/v0.5.2
[0.5.1]: https://github.com/plotdevice01/codex-chief-of-staff/releases/tag/v0.5.1
[0.5.0]: https://github.com/plotdevice01/codex-chief-of-staff/releases/tag/v0.5.0
[0.4.5]: https://github.com/plotdevice01/codex-chief-of-staff/releases/tag/v0.4.5
[0.4.4]: https://github.com/plotdevice01/codex-chief-of-staff/releases/tag/v0.4.4
[0.4.3]: https://github.com/plotdevice01/codex-chief-of-staff/releases/tag/v0.4.3
[0.4.2]: https://github.com/plotdevice01/codex-chief-of-staff/releases/tag/v0.4.2
[0.4.1]: https://github.com/plotdevice01/codex-chief-of-staff/releases/tag/v0.4.1
[0.4.0]: https://github.com/plotdevice01/codex-chief-of-staff/releases/tag/v0.4.0
[0.3.1]: https://github.com/plotdevice01/codex-chief-of-staff/releases/tag/v0.3.1
