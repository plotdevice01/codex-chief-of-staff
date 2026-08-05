# Testing

## Deterministic checks

```bash
python Test-Persona.py
python validate_install.py --example
python scripts/validate_repository.py
node tests/test_hooks.js
python tests/test_viral_carousel_skill.py
python tests/test_icm.py
python tests/test_release.py
python tests/test_sync.py
python scripts/build_release.py --output dist
```

These checks cover:

- persona source hashes and 97 requirements;
- nine integration rules and twelve live scenario definitions;
- shared behavior, ICM routing, and configuration defaults;
- five ICM forms and ten invariants, plus release contracts and cold-walk failures;
- Viral Carousel skill files and ICM stage contracts, plus human gates and stamping scripts;
- companion plugin discovery and duplicate skill detection, plus install receipts;
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
on GPT-5.6 Sol Medium. Repeat the scenarios with GPT-5.6 Terra XHigh and in a
fresh Claude Code session. Record:

- prompt and response;
- pass criteria met or missed;
- plugin version;
- host surface and version;
- hook trust status;
- Ponytail and AI Sloppy Copy versions.

The active Standard route is Sol Medium; there is no quick or lower-model
route. v2.0.0 changes model-facing inputs and plugin ownership. Evidence from
v0.6 cannot be carried forward. A failed scenario blocks publication. A
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
- the ICM conformance validator or cold-walk failure fixture fails;
- Ponytail loses a bundled skill or session/subagent hook;
- AI Sloppy Copy rule counts, global hooks, protected text, evidence and voice
  gates, or two-pass enforcement drift.
