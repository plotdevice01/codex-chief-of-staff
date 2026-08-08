from __future__ import annotations

import hashlib
from pathlib import Path

try:
    from .config_paths import ROOT
except ImportError:
    from config_paths import ROOT


FILES = (
    ".gitattributes", ".gitignore", "AGENTS.md", "CHANGELOG.md", "CONTEXT.md",
    "CONTRIBUTING.md", "LICENSE", "PRIVACY.md", "plugin.json", "README.md",
    "SECURITY.md", "Sync-ProjectAgents.py", "TERMS.md", "Test-Persona.py",
    "VERSION", "chief-of-staff.example.json", "install.ps1", "install.sh",
    "validate_install.py",
)
DIRECTORIES = (
    ".agents", ".codex-plugin", "assets", "docs", "examples", "hooks",
    "persona", "scripts", "skills", "tests", "workflows",
)
SKIP_PARTS = {"__pycache__", ".DS_Store"}
TEXT_SUFFIXES = {".json", ".md", ".ps1", ".py", ".sh", ".svg", ".txt", ".yaml", ".yml"}


def canonical_bytes(path: Path) -> bytes:
    if path.suffix.lower() in TEXT_SUFFIXES or path.name in {
        ".gitattributes", ".gitignore", "LICENSE", "VERSION",
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
            path for path in paths
            if not any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts)
            and path.suffix.lower() not in {".pyc", ".pyo"}
        ),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def stage_package(stage: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for source in copied_files():
        relative = source.relative_to(ROOT)
        target = stage / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        content = canonical_bytes(source)
        target.write_bytes(content)
        file_hash = hashlib.sha256(content).hexdigest()
        if hashlib.sha256(target.read_bytes()).hexdigest() != file_hash:
            raise RuntimeError(f"Staged file mismatch: {relative}")
        hashes[relative.as_posix()] = file_hash
    sop = stage / "docs" / "Codex Chief of Staff - Installation and SOP.docx"
    root_sop = stage / sop.name
    root_sop.write_bytes(sop.read_bytes())
    hashes[sop.name] = hashlib.sha256(root_sop.read_bytes()).hexdigest()
    return hashes
