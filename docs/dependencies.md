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

## Repository distribution

Users install Chief from its GitHub repository. The project does not claim an
OpenAI review, approval, directory listing, or store distribution.

The three source products above are not separate user installs. Chief is the
single discoverable product.

Windows:

```powershell
git clone https://github.com/plotdevice01/codex-chief-of-staff.git
Set-Location .\codex-chief-of-staff
.\install.ps1
```

macOS or Linux:

```bash
git clone https://github.com/plotdevice01/codex-chief-of-staff.git
cd codex-chief-of-staff
./install.sh
```

Restart Codex after local installation. Start a fresh task so Codex discovers
the current package and its single Chief skill.

## Verify

```powershell
py -3 .\validate_install.py --doctor
py -3 .\validate_install.py --strict-dependencies --receipt install-receipt.json
py -3 .\tests\test_content_runtime.py
```

The receipt records the active Chief version, the single discoverable skill,
and each bundled content source version, commit, and file count.

AI Sloppy Copy has two version layers. Plugin `0.5.0` identifies the source
product release. Standard `2.2.0` identifies its writing-rules contract.
