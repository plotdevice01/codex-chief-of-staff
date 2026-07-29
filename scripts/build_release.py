from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from .build_sop import build as build_sop
    from .config_paths import ROOT
    from .test_persona import validate as validate_persona
    from .validate_install import validate_config
    from .validate_repository import validate_archive, validate_repository
except ImportError:
    from build_sop import build as build_sop
    from config_paths import ROOT
    from test_persona import validate as validate_persona
    from validate_install import validate_config
    from validate_repository import validate_archive, validate_repository


VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
RELEASE_NAME = f"codex-chief-of-staff-v{VERSION}"
FILES = (
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "PRIVACY.md",
    "README.md",
    "SECURITY.md",
    "Sync-ProjectAgents.py",
    "TERMS.md",
    "Test-Persona.py",
    "VERSION",
    "chief-of-staff.example.json",
    "install.ps1",
    "install.sh",
    "validate_install.py",
)
DIRECTORIES = (
    ".claude-plugin",
    ".codex-plugin",
    "assets",
    "docs",
    "examples",
    "hooks",
    "persona",
    "scripts",
    "skills",
    "tests",
)
SKIP_PARTS = {"__pycache__", ".DS_Store"}
TEXT_SUFFIXES = {".json", ".md", ".ps1", ".py", ".sh", ".svg", ".txt", ".yaml", ".yml"}
ZIP_TIME = (2026, 7, 29, 0, 0, 0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(path: Path) -> bytes:
    if path.suffix.lower() in TEXT_SUFFIXES or path.name in {
        ".gitattributes",
        ".gitignore",
        "LICENSE",
        "VERSION",
    }:
        text = path.read_text(encoding="utf-8-sig")
        return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return path.read_bytes()


def copied_files() -> list[Path]:
    paths = [ROOT / name for name in FILES]
    for directory in DIRECTORIES:
        paths.extend(path for path in (ROOT / directory).rglob("*") if path.is_file())
    return sorted(
        (
            path
            for path in paths
            if not any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts)
            and path.suffix.lower() not in {".pyc", ".pyo"}
        ),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def stage_release(stage: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for source in copied_files():
        relative = source.relative_to(ROOT)
        target = stage / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        content = canonical_bytes(source)
        target.write_bytes(content)
        source_hash = hashlib.sha256(content).hexdigest()
        if hashlib.sha256(target.read_bytes()).hexdigest() != source_hash:
            raise RuntimeError(f"Staged file mismatch: {relative}")
        hashes[relative.as_posix()] = source_hash
    sop = stage / "docs" / "Codex Chief of Staff - Installation and SOP.docx"
    shutil.copy2(sop, stage / sop.name)
    hashes[sop.name] = sha256(sop)
    return hashes


def run_hook_tests(node: str) -> None:
    result = subprocess.run(
        [node, str(ROOT / "tests" / "test_hooks.js")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    sync = subprocess.run(
        [sys.executable, str(ROOT / "tests" / "test_sync.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if sync.returncode:
        raise RuntimeError(sync.stderr or sync.stdout)


def write_zip(stage: Path, archive: Path) -> None:
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as output:
        for source in sorted(stage.rglob("*"), key=lambda path: path.relative_to(stage).as_posix()):
            if not source.is_file():
                continue
            relative = source.relative_to(stage).as_posix()
            info = zipfile.ZipInfo(f"{RELEASE_NAME}/{relative}", ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = (
                0o100755 if source.suffix == ".sh" else 0o100644
            ) << 16
            output.writestr(info, source.read_bytes())


def build(output: Path, node: str, *, build_document: bool = True) -> tuple[Path, Path]:
    output.mkdir(parents=True, exist_ok=True)
    if build_document:
        build_sop(ROOT / "docs" / "Codex Chief of Staff - Installation and SOP.docx")

    persona_errors, metrics = validate_persona()
    install_errors, install_warnings = validate_config(
        ROOT / "chief-of-staff.example.json"
    )
    repository_errors, _ = validate_repository()
    run_hook_tests(node)
    errors = persona_errors + install_errors + repository_errors
    if errors:
        raise RuntimeError("\n".join(errors))

    stage = output / RELEASE_NAME
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    hashes = stage_release(stage)
    validation = {
        "release_version": VERSION,
        "built_at": datetime(2026, 7, 29, tzinfo=timezone.utc).isoformat(),
        "status": "pass",
        "persona_requirements": metrics["persona_requirements"],
        "integration_requirements": metrics["integration_requirements"],
        "live_acceptance_tests": metrics["live_acceptance_tests"],
        "source_pdf_sha256": metrics["source_pdf_sha256"],
        "persona_text_sha256": metrics["persona_text_sha256"],
        "hook_tests": "pass",
        "project_sync_tests": "pass",
        "configuration_validation": "pass",
        "repository_privacy_scan": "pass",
        "dependency_warnings": install_warnings,
        "files": hashes,
    }
    validation_path = stage / "release-validation.json"
    validation_path.write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    archive = output / f"{RELEASE_NAME}.zip"
    if archive.exists():
        archive.unlink()
    write_zip(stage, archive)
    archive_errors = validate_archive(archive)
    if archive_errors:
        raise RuntimeError("\n".join(archive_errors))
    checksum = output / f"{archive.name}.sha256"
    checksum.write_text(f"{sha256(archive)}  {archive.name}\n", encoding="ascii")
    return archive, checksum


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a deterministic Chief of Staff release archive."
    )
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--node", default=shutil.which("node") or "node")
    parser.add_argument(
        "--skip-sop",
        action="store_true",
        help="Package the existing visually approved SOP instead of rebuilding it.",
    )
    args = parser.parse_args()
    archive, checksum = build(
        args.output.resolve(), args.node, build_document=not args.skip_sop
    )
    print(f"PASS: {archive}")
    print(f"PASS: {checksum}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
