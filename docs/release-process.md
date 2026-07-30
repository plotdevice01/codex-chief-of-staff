# Release process

1. Update `VERSION`, plugin manifests, configuration example, hook version,
   documentation, and `CHANGELOG.md`.
2. Run the complete validation suite.
3. Build the release with `python scripts/build_release.py --output dist`.
4. Inspect the staged folder and ZIP file list.
5. Render and inspect the generated DOCX SOP.
6. Commit the canonical source.
7. Create and push a signed or annotated `vX.Y.Z` tag.
8. The release workflow rebuilds, validates, attests, and publishes the ZIP and
   checksum.
9. Run `claude plugin validate .`.
10. Verify the public release asset, digest, README links, and installation in
    fresh Codex and Claude Code sessions.

Historical tags and release assets are immutable. Fixes ship as a new version.
