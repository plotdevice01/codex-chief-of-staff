from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    from .config_paths import ROOT
    from .sync_project_agents import (
        LOADER_MARKER,
        MANAGED_END,
        MANAGED_START,
        build_managed_block,
    )
    from .validate_install import validate_config
except ImportError:
    from config_paths import ROOT
    from sync_project_agents import (
        LOADER_MARKER,
        MANAGED_END,
        MANAGED_START,
        build_managed_block,
    )
    from validate_install import validate_config


START = "<!-- SHARED-BEHAVIOR-CONTRACT:START -->"
END = "<!-- SHARED-BEHAVIOR-CONTRACT:END -->"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def shared_block(path: Path) -> str:
    text = normalized_text(path)
    start = text.find(START)
    end = text.find(END)
    if start < 0 or end < start:
        raise ValueError(f"Managed behavior markers are missing in {path}.")
    return text[start : end + len(END)]


def managed_block(path: Path) -> str:
    text = normalized_text(path)
    start = text.find(MANAGED_START)
    end = text.find(MANAGED_END, start)
    if start < 0 or end < start:
        raise ValueError(f"Managed loader markers are missing in {path}.")
    return text[start : end + len(MANAGED_END)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(local_root: Path) -> list[str]:
    errors: list[str] = []
    required = (
        "AGENTS.md",
        "chief-of-staff.json",
        "persona/Technical Assistant Persona - source.pdf",
        "persona/persona-contract.json",
        "persona/technical-assistant-persona.txt",
    )
    for name in required:
        if not (local_root / name).is_file():
            errors.append(f"Local installation is missing {name}.")
    if errors:
        return errors

    config = local_root / "chief-of-staff.json"
    data = json.loads(config.read_text(encoding="utf-8-sig"))
    local_agents = local_root / "AGENTS.md"
    local_text = normalized_text(local_agents)
    try:
        if LOADER_MARKER in local_text:
            expected = build_managed_block(data, config.resolve())
            if managed_block(local_agents) != expected:
                errors.append("The local AGENTS.md fail-safe loader differs.")
        elif shared_block(local_agents) != shared_block(ROOT / "AGENTS.md"):
            errors.append("The shared AGENTS.md behavior contract differs.")
    except ValueError as exc:
        errors.append(str(exc))

    binary = "persona/Technical Assistant Persona - source.pdf"
    if sha256(local_root / binary) != sha256(ROOT / binary):
        errors.append("The retained persona PDF differs.")
    text = "persona/technical-assistant-persona.txt"
    if normalized_text(local_root / text) != normalized_text(ROOT / text):
        errors.append("The retained persona text differs.")
    contract = "persona/persona-contract.json"
    local_contract = json.loads((local_root / contract).read_text(encoding="utf-8-sig"))
    public_contract = json.loads((ROOT / contract).read_text(encoding="utf-8-sig"))
    if local_contract != public_contract:
        errors.append("The persona contract differs.")

    config_errors, _ = validate_config(config)
    errors.extend(f"Local configuration: {error}" for error in config_errors)
    if data.get("version") != VERSION:
        errors.append(f"Local version must be {VERSION}.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare a private local installation with the public behavior contract."
    )
    parser.add_argument("--local-root", type=Path, required=True)
    args = parser.parse_args()
    errors = validate(args.local_root.resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: local and portable Chief of Staff v{VERSION} behavior match.")
    print("Machine paths, private identities, secrets, and project data were allowed to differ.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
