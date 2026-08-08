# Runtime and source dependencies

The reference installation uses one user-facing plugin: Chief of Staff.

## Runtime ownership

Chief bundles exact released runtime files from:

- [AI Sloppy Copy](https://github.com/plotdevice01/ai-sloppy-copy) `0.5.0` with Standard `2.2.0`;
- [Brand Voice Factory](https://github.com/plotdevice01/brand-voice-factory) `0.2.1`;
- [Crafty Carousels](https://github.com/plotdevice01/crafty-carousels-skill) `0.6.1`.

The files remain authoritative in their source repositories. Chief's
`skills/chief-of-staff/vendor/manifest.json` records each source repository,
release commit, destination, SHA-256, and byte count. The release validator
rejects drift.

## Team distribution

After public-directory approval, teammates open ChatGPT Work or Codex in the
ChatGPT desktop app, open **Plugins**, search for **Chief of Staff**, select
**+**, and start a new chat. Workspace admins can set Chief to **Installed**
for the required roles so members skip the install step.

The three source products above are not separate team installs or public
directory targets. Chief is the single discoverable product.

The public listing is not available until the OpenAI submission is approved
and published. Before then, administrators and developers can use the
GitHub-backed marketplace:

```powershell
codex plugin marketplace add plotdevice01/codex-chief-of-staff
codex plugin add chief-of-staff@codex-chief-of-staff
```

Repository: [Chief of Staff](https://github.com/plotdevice01/codex-chief-of-staff)

Restart the ChatGPT desktop app after local installation. Start a fresh task so
ChatGPT Work or Codex discovers the current package and its single Chief skill.

## Verify

```powershell
python validate_install.py --doctor
python validate_install.py --strict-dependencies --receipt install-receipt.json
python tests/test_content_runtime.py
```

The receipt records the active Chief version, the single discoverable skill,
and each bundled content source version, commit, and file count.

AI Sloppy Copy has two version layers. Plugin `0.5.0` identifies the source
product release. Standard `2.2.0` identifies its writing-rules contract.
