# Testing

## Deterministic checks

```bash
python Test-Persona.py
python validate_install.py --example
python scripts/validate_repository.py
node tests/test_hooks.js
python tests/test_sync.py
python scripts/build_release.py --output dist
```

These checks cover:

- persona source hashes and 97 requirements;
- shared behavior and configuration defaults;
- manifest, skill, hook, and version consistency;
- session and subagent hook output;
- project-rule preservation during shared-contract updates;
- private-value scanning;
- release contents and archive integrity.

## Live behavior checks

Run every prompt in `persona/persona-contract.json` in a fresh Codex task after
installation. Record:

- prompt and response;
- pass criteria met or missed;
- plugin version;
- Codex surface and version;
- hook trust status;
- Ponytail and AI Sloppy Copy versions.

Static files cannot prove tone, judgment, or host behavior. A green JSON file
does not become sentient because we named it validation.

## Release gate

A release fails when:

- any persona source or requirement drifts;
- generic and local behavior defaults differ;
- a private identity or local machine path enters public files;
- hooks fail on Windows or POSIX command paths;
- generated archive files differ from the staged release;
- version values disagree;
- the DOCX SOP does not render cleanly.
