from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

from docx import Document

try:
    from .config_paths import ROOT
    from .test_persona import validate as validate_persona
except ImportError:
    from config_paths import ROOT
    from test_persona import validate as validate_persona


VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
REQUIRED = (
    ".gitattributes",
    ".claude-plugin/marketplace.json",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    "AGENTS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "PRIVACY.md",
    "README.md",
    "SECURITY.md",
    "TERMS.md",
    "assets/icon.png",
    "assets/icon.svg",
    "assets/logo-dark.png",
    "assets/logo-dark.svg",
    "assets/logo.png",
    "assets/logo.svg",
    "assets/social-preview.png",
    "assets/social-preview.svg",
    "chief-of-staff.example.json",
    "docs/Codex Chief of Staff - Installation and SOP.docx",
    "hooks/chief-of-staff-hook.js",
    "hooks/hooks.json",
    "install.ps1",
    "install.sh",
    "persona/Technical Assistant Persona - source.pdf",
    "persona/persona-contract.json",
    "persona/technical-assistant-persona.txt",
    "scripts/build_release.py",
    "scripts/build_sop.py",
    "scripts/configure.py",
    "scripts/sync_project_agents.py",
    "scripts/test_persona.py",
    "scripts/validate_install.py",
    "scripts/validate_local_parity.py",
    "skills/chief-of-staff/SKILL.md",
    "skills/chief-of-staff/agents/openai.yaml",
    "tests/test_hooks.js",
    "tests/test_sync.py",
)
TEXT_SUFFIXES = {".json", ".md", ".ps1", ".py", ".sh", ".svg", ".txt", ".yaml", ".yml"}
PRIVATE_PATTERNS = {
    "Windows user path": re.compile(
        r"C:[\\/]+Users[\\/]+" + "Aa" + "ron", re.IGNORECASE
    ),
    "private Gmail identity": re.compile(
        "aaronz" + r"thomas@gmail\.com", re.IGNORECASE
    ),
    "private business identity": re.compile(
        "aaron@" + r"theingroup\.io", re.IGNORECASE
    ),
    "private client identity": re.compile(
        "aaron@" + r"drjonesdc\.com", re.IGNORECASE
    ),
    "private Slack user ID": re.compile(r"\bU08D9" + r"BUMQ95\b"),
    "private ClickUp workspace": re.compile(r"\b901414" + r"57186\b"),
    "private ClickUp user": re.compile(r"\b106" + r"489469\b"),
    "private project path": re.compile(
        "(" + "DEAN " + "DAYJOB|FAMILY " + "LAW|To Know " + "Oneself)",
        re.IGNORECASE,
    ),
}
PLACEHOLDER = re.compile(r"\b(TODO|TBD|REPLACE_WITH_[A-Z0-9_]+|YOUR_[A-Z0-9_]+)\b")


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))


def docx_text(path: Path) -> str:
    doc = Document(path)
    return "\n".join(
        [paragraph.text for paragraph in doc.paragraphs]
        + [
            cell.text
            for table in doc.tables
            for row in table.rows
            for cell in row.cells
        ]
    )


def public_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        return docx_text(path)
    return path.read_text(encoding="utf-8-sig")


def validate_versions() -> list[str]:
    errors: list[str] = []
    values = {
        ".codex-plugin/plugin.json": read_json(".codex-plugin/plugin.json").get(
            "version"
        ),
        ".claude-plugin/plugin.json": read_json(".claude-plugin/plugin.json").get(
            "version"
        ),
        "chief-of-staff.example.json": read_json(
            "chief-of-staff.example.json"
        ).get("release_version"),
    }
    hook = (ROOT / "hooks/chief-of-staff-hook.js").read_text(encoding="utf-8")
    hook_match = re.search(r'const VERSION = "([^"]+)";', hook)
    values["hooks/chief-of-staff-hook.js"] = (
        hook_match.group(1) if hook_match else None
    )
    for name, value in values.items():
        if value != VERSION:
            errors.append(f"{name} version is {value!r}; expected {VERSION!r}.")
    return errors


def validate_manifest_paths() -> list[str]:
    errors: list[str] = []
    manifest = read_json(".codex-plugin/plugin.json")
    for key, default in (("skills", None), ("hooks", "./hooks/hooks.json")):
        value = manifest.get(key, default)
        if not isinstance(value, str) or not (ROOT / value).exists():
            errors.append(f"Plugin manifest {key} path is missing: {value!r}.")
    interface = manifest.get("interface", {})
    for key in ("composerIcon", "logo", "logoDark"):
        value = interface.get(key)
        if not isinstance(value, str) or not (ROOT / value).is_file():
            errors.append(f"Plugin interface {key} path is missing: {value!r}.")
    marketplace = read_json(".claude-plugin/marketplace.json")
    plugins = marketplace.get("plugins", [])
    if not plugins or plugins[0].get("source") != "./":
        errors.append("Marketplace manifest must install the repository root.")
    return errors


def validate_public_text() -> list[str]:
    errors: list[str] = []
    skip_placeholders = {
        "chief-of-staff.example.json",
        "scripts/validate_install.py",
        "scripts/validate_repository.py",
        "scripts/test_persona.py",
    }
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith((".git/", "dist/", "qa/")):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.suffix.lower() != ".docx":
            continue
        text = public_text(path)
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{relative} contains {label}.")
        if relative not in skip_placeholders and PLACEHOLDER.search(text):
            errors.append(f"{relative} contains an unfinished placeholder.")
    return errors


def validate_archive(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with zipfile.ZipFile(path) as archive:
            names = [name.replace("\\", "/") for name in archive.namelist()]
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"Invalid release archive: {exc}"]
    prefix = f"codex-chief-of-staff-v{VERSION}/"
    if not names or any(not name.startswith(prefix) for name in names):
        errors.append(f"Every archive entry must be under {prefix}.")
    if any(name.endswith("/chief-of-staff.json") for name in names):
        errors.append("Release archive contains private chief-of-staff.json.")
    for required in REQUIRED:
        if f"{prefix}{required}" not in names:
            errors.append(f"Release archive is missing {required}.")
    return errors


def validate_repository(archive: Path | None = None) -> tuple[list[str], dict]:
    errors = [
        f"Missing required file: {name}" for name in REQUIRED if not (ROOT / name).is_file()
    ]
    errors.extend(validate_versions())
    errors.extend(validate_manifest_paths())
    errors.extend(validate_public_text())
    persona_errors, metrics = validate_persona()
    errors.extend(f"Persona validation: {error}" for error in persona_errors)
    if archive:
        errors.extend(validate_archive(archive))
    return errors, metrics


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the public Chief of Staff source and release archive."
    )
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    errors, metrics = validate_repository(args.archive)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(
        f"PASS: Chief of Staff v{VERSION} source is public-safe and version-consistent."
    )
    print(
        f"PASS: {metrics['persona_requirements']} persona requirements, "
        f"{metrics['integration_requirements']} integration rules, and "
        f"{metrics['live_acceptance_tests']} live scenarios preserved."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
