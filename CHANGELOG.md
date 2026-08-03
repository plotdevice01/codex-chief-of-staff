# Changelog

All notable changes are recorded here. Public releases use one-decimal pre-1.0
milestones. Host manifests use strict three-part semantic versions.

## Unreleased

### Changed

- Updated the complete-stack dependency to AI Sloppy Copy release `0.4`, host
  manifest `0.4.0`, and Standard `2.2.0` or later.
- Updated strict validation, installation guidance, release evidence, and the
  generated SOP to require the same dependency line.

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
