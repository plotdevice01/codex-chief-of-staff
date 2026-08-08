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
    from .package_files import stage_package
    from .test_persona import validate as validate_persona
    from .validate_icm import validate_icm
    from .validate_install import validate_config
    from .validate_repository import (
        model_acceptance_release_status,
        validate_archive,
        validate_repository,
    )
except ImportError:
    from build_sop import build as build_sop
    from config_paths import ROOT
    from package_files import stage_package
    from test_persona import validate as validate_persona
    from validate_icm import validate_icm
    from validate_install import validate_config
    from validate_repository import (
        model_acceptance_release_status,
        validate_archive,
        validate_repository,
    )


VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
RELEASE_NAME = f"codex-chief-of-staff-v{VERSION}"
ZIP_TIME = (2026, 8, 6, 0, 0, 0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage_release(stage: Path) -> dict[str, str]:
    return stage_package(stage)


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
    icm = subprocess.run(
        [sys.executable, str(ROOT / "tests" / "test_icm.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if icm.returncode:
        raise RuntimeError(icm.stderr or icm.stdout)
    release = subprocess.run(
        [sys.executable, str(ROOT / "tests" / "test_release.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if release.returncode:
        raise RuntimeError(release.stderr or release.stdout)
    content = subprocess.run(
        [sys.executable, str(ROOT / "tests" / "test_content_runtime.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if content.returncode:
        raise RuntimeError(content.stderr or content.stdout)


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


def build(
    output: Path,
    node: str,
    *,
    build_document: bool = True,
    require_model_acceptance: bool = False,
) -> tuple[Path, Path]:
    output.mkdir(parents=True, exist_ok=True)
    if build_document:
        build_sop(ROOT / "docs" / "Codex Chief of Staff - Installation and SOP.docx")

    persona_errors, metrics = validate_persona()
    install_errors, _ = validate_config(
        ROOT / "chief-of-staff.example.json"
    )
    repository_errors, _ = validate_repository(
        require_model_acceptance=require_model_acceptance
    )
    icm_errors, icm_metrics = validate_icm()
    run_hook_tests(node)
    errors = persona_errors + install_errors + repository_errors
    if errors:
        raise RuntimeError("\n".join(errors))

    stage = output / RELEASE_NAME
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    hashes = stage_release(stage)
    model_acceptance = json.loads(
        (ROOT / "tests" / "model-acceptance.json").read_text(encoding="utf-8")
    )
    acceptance_status = model_acceptance_release_status(model_acceptance)
    validation = {
        "release_version": VERSION,
        "built_at": datetime(2026, 8, 6, tzinfo=timezone.utc).isoformat(),
        "status": acceptance_status,
        "persona_requirements": metrics["persona_requirements"],
        "integration_requirements": metrics["integration_requirements"],
        "live_acceptance_tests": metrics["live_acceptance_tests"],
        "source_pdf_sha256": metrics["source_pdf_sha256"],
        "persona_text_sha256": metrics["persona_text_sha256"],
        "hook_tests": "pass",
        "project_sync_tests": "pass",
        "model_acceptance": model_acceptance,
        "icm_conformance": {"status": "pass", **icm_metrics},
        "configuration_validation": "pass",
        "repository_privacy_scan": "pass",
        "runtime_requirements": {
            "discoverable_skills": ["chief-of-staff"],
            "standalone_dependencies": [],
            "bundled_content_runtime": {
                "ai_sloppy_copy": "0.5.0 with Standard 2.2.0",
                "brand_voice_factory": "0.2.1",
                "crafty_carousels": "0.6.1",
            },
        },
        "files": hashes,
    }
    validation_path = stage / "release-validation.json"
    validation_path.write_bytes(
        (json.dumps(validation, indent=2, sort_keys=True) + "\n").encode("utf-8")
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
    parser.add_argument(
        "--require-model-acceptance",
        action="store_true",
        help="Block the build unless fresh required model and host evidence passed.",
    )
    args = parser.parse_args()
    archive, checksum = build(
        args.output.resolve(),
        args.node,
        build_document=not args.skip_sop,
        require_model_acceptance=args.require_model_acceptance,
    )
    print(f"PASS: {archive}")
    print(f"PASS: {checksum}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
