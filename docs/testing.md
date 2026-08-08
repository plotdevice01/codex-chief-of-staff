# Testing

## Deterministic checks

```bash
python Test-Persona.py
python validate_install.py --example
python scripts/validate_repository.py
node tests/test_hooks.js
python tests/test_content_runtime.py
python tests/test_live_acceptance_harness.py
python tests/test_icm.py
python tests/test_release.py
python tests/test_sync.py
python scripts/build_release.py --output dist
```

These checks cover:

- persona source hashes and 97 requirements;
- ten integration rules and fifteen live scenario definitions;
- shared behavior, ICM routing, and configuration defaults;
- five ICM forms and ten invariants, plus release contracts and cold-walk failures;
- the pinned content manifest and the complete hook, script, and CTA libraries;
- Brand Voice and Crafty stamping scripts plus the final prose checker;
- one discoverable Chief skill and bundled-runtime install receipts;
- manifest, skill, hook, and version consistency;
- session and subagent hook output;
- intent-specific prompt activation and required response labels;
- ICM seven-line architecture validation;
- bounded read-only restructure inventory and mutation denial;
- reference and duplicate-proof gates before deletion proposals;
- Chief and AI Sloppy Copy response-contract compatibility;
- two correction cycles and fail-closed stop;
- recovery bypass;
- private-context rejection before tool use and at final response;
- generic hook results that do not repeat the private marker;
- project-rule preservation during fail-safe loader updates;
- private-value scanning;
- release contents and archive integrity.

## Live behavior checks

Run every prompt in `persona/persona-contract.json` after candidate installation
on GPT-5.6 Sol Medium in fresh Codex and ChatGPT Work tasks. The accepted v2.1.0
host and Sol evidence may be carried forward only for a documented
non-model-facing patch. Terra XHigh remains pending unless the owner explicitly
approves a version-bound release waiver. Record:

- prompt and response;
- pass criteria met or missed;
- plugin version;
- host surface and version;
- hook trust status;
- the single Chief route and bundled content source versions.

Generate the Codex prompt with
`python scripts/live_acceptance_harness.py prompt --host codex`. Generate the
ChatGPT Work prompt only after the owner verifies the current desktop task was
opened from **Work**, using
`python scripts/live_acceptance_harness.py prompt --host chatgpt-work --owner-verified-ui`.
For Codex, use the built-in `:read-only` permission profile. For ChatGPT Work,
select **Work**, **Work locally**, and **Ask for approval**. Record that UI
selection as owner-verified evidence and record the agent runtime separately;
the runtime may validly report `codex` beneath the Work UI.
Run the scenarios inline. Task creation, delegation, any file or temporary-file
mutation, connector use, or host substitution invalidates the complete run.
Validate the returned JSON with
`python scripts/live_acceptance_harness.py validate --host <host>`.

The active Standard route is Sol Medium; there is no quick or lower-model
route. v2.1.0 changed model-facing inputs and content routing, so evidence from
v2.0.1 could not be carried forward. A failed scenario blocks publication. A
pending Sol or Terra check requires an explicit version-bound owner waiver.
Pending evidence remains pending.

Static files cannot prove live tone or judgment. A green JSON file
does not become sentient because we named it validation.

## Release gate

A release fails when:

- any persona source or requirement drifts;
- generic and local behavior defaults differ;
- a private identity or local machine path enters public files;
- hooks fail on Windows or POSIX command paths;
- ICM enforcement accepts a response that misses its required header;
- the enforcement state can loop beyond two corrections;
- a tool request or final response can leak a private marker;
- a restructure can mutate files before approval;
- an unverified duplicate can be proposed for deletion;
- generated archive files differ from the staged release;
- version values disagree;
- the DOCX SOP does not render cleanly;
- either required model profile misses a live scenario;
- a pending model check lacks an explicit version-bound owner waiver;
- either required host remains pending or misses a live scenario;
- a live run lacks the required UI evidence, uses an incompatible runtime or
  safety control, delegates tasks, or makes any file, connector, or external
  mutation;
- the ICM conformance validator or cold-walk failure fixture fails;
- Agent Plugins discovery exposes a skill other than Chief;
- a vendored content file differs from its pinned hash;
- AI Sloppy Copy rule counts, protected text, evidence and voice gates, or
  two-pass enforcement drift.
