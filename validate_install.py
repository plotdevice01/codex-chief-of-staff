from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "chief-of-staff.json"
REQUIRED_FILES = (
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "Test-Persona.py",
    "Sync-ProjectAgents.py",
    "chief-of-staff.example.json",
    "persona/Technical Assistant Persona - source.pdf",
    "persona/technical-assistant-persona.txt",
    "persona/persona-contract.json",
    "release-validation.json",
    "Codex Chief of Staff - Installation and SOP.docx",
)
PLACEHOLDER = re.compile(r"(YOUR_|REPLACE_WITH_|<[^>]+>)", re.IGNORECASE)
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SAFE_WRITE_POLICIES = {"blocked", "confirm_each"}


def find_placeholders(value, location: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            findings.extend(find_placeholders(child, f"{location}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_placeholders(child, f"{location}[{index}]"))
    elif isinstance(value, str) and PLACEHOLDER.search(value):
        findings.append(location)
    return findings


def get_nested(data: dict, dotted_path: str):
    current = data
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted_path)
        current = current[part]
    return current


def validate_behavior(config: dict) -> list[str]:
    errors: list[str] = []
    expected = {
        "communication.default_mode.name": "85_percent_compression",
        "communication.default_mode.compression_percent": 85,
        "communication.default_mode.always_on": True,
        "communication.default_mode.answer_first": True,
        "communication.caveman_mode.keyword": "caveman",
        "communication.caveman_mode.compression_percent": 100,
        "communication.caveman_mode.fragments_allowed": True,
        "communication.caveman_mode.preserve_exact_technical_content": True,
        "communication.direct_reply_personality.dry_sarcasm": "decent_amount",
        "communication.direct_reply_personality.cynical_humor": "decent_amount",
        "communication.direct_reply_personality.non_hostile": True,
        "communication.witty_advice.enabled": True,
        "communication.witty_advice.after_requested_work": True,
        "communication.external_tone": "professional",
        "communication.authored_copy_standard.name": "AI Sloppy Copy",
        "communication.authored_copy_standard.minimum_version": "2.1.0",
        "communication.authored_copy_standard.required": True,
    }
    for path, required in expected.items():
        try:
            actual = get_nested(config, path)
        except KeyError:
            errors.append(f"Missing behavior setting: {path}")
            continue
        if actual != required:
            errors.append(
                f"Behavior setting mismatch at {path}: "
                f"expected {required!r}, got {actual!r}"
            )
    return errors


def validate() -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (ROOT / name).is_file():
            errors.append(f"Missing required file: {name}")

    if not CONFIG.is_file():
        errors.append(
            "Missing chief-of-staff.json. Copy chief-of-staff.example.json and customize it."
        )
        return errors

    try:
        config = json.loads(CONFIG.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid chief-of-staff.json: {exc}")
        return errors

    placeholders = find_placeholders(config)
    if placeholders:
        errors.append("Template placeholders remain at: " + ", ".join(placeholders))

    version = config.get("release_version", "")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append("release_version must use semantic versioning, such as 0.3.0.")

    owner = config.get("owner")
    if not isinstance(owner, dict) or not owner.get("name") or not owner.get("timezone"):
        errors.append("owner.name and owner.timezone are required.")

    errors.extend(validate_behavior(config))

    connectors = config.get("connectors")
    if not isinstance(connectors, list):
        errors.append("connectors must be a list.")
        connectors = []

    connector_ids: list[str] = []
    for index, connector in enumerate(connectors):
        location = f"connectors[{index}]"
        if not isinstance(connector, dict):
            errors.append(f"{location} must be an object.")
            continue
        connector_id = connector.get("id")
        if not connector_id:
            errors.append(f"{location}.id is required.")
        else:
            connector_ids.append(str(connector_id))
        write_policy = connector.get("external_writes")
        if write_policy not in SAFE_WRITE_POLICIES:
            errors.append(f"{location}.external_writes must be blocked or confirm_each.")
        if connector.get("enabled"):
            if not connector.get("provider"):
                errors.append(f"{location}.provider is required when enabled.")
            identity = connector.get("expected_identity")
            if not isinstance(identity, dict) or not any(identity.values()):
                errors.append(f"{location}.expected_identity is required when enabled.")
            denied = connector.get("denied_identities", [])
            if not isinstance(denied, list):
                errors.append(f"{location}.denied_identities must be a list.")
            elif isinstance(identity, dict):
                approved_values = {str(value) for value in identity.values() if value}
                denied_values = {
                    str(value)
                    for item in denied
                    for value in (
                        item.values() if isinstance(item, dict) else (item,)
                    )
                    if value
                }
                if approved_values & denied_values:
                    errors.append(f"{location} approves an identity that is also denied.")

    if len(connector_ids) != len(set(connector_ids)):
        errors.append("Connector IDs must be unique.")

    policy = config.get("policy")
    if not isinstance(policy, dict):
        errors.append("policy must be an object.")
    else:
        if policy.get("default_external_writes") not in SAFE_WRITE_POLICIES:
            errors.append("policy.default_external_writes must be blocked or confirm_each.")
        if policy.get("automatic_authority_expansion") is not False:
            errors.append("policy.automatic_authority_expansion must be false.")

    projects = config.get("projects")
    if not isinstance(projects, list):
        errors.append("projects must be a list.")
        projects = []

    project_ids: list[str] = []
    for index, project in enumerate(projects):
        location = f"projects[{index}]"
        if not isinstance(project, dict):
            errors.append(f"{location} must be an object.")
            continue
        project_id = project.get("id")
        if not project_id:
            errors.append(f"{location}.id is required.")
        else:
            project_ids.append(str(project_id))
        if not project.get("enabled"):
            continue
        paths = project.get("paths")
        if not isinstance(paths, list) or not paths:
            errors.append(f"{location}.paths must contain at least one path.")
            continue
        for raw_path in paths:
            path = Path(str(raw_path)).expanduser()
            if not path.is_absolute():
                errors.append(f"{location} path must be absolute: {raw_path}")
            elif not path.exists():
                errors.append(f"{location} path does not exist: {raw_path}")
        instructions = project.get("instructions")
        if instructions:
            instruction_path = Path(str(instructions)).expanduser()
            if not instruction_path.is_absolute():
                errors.append(f"{location}.instructions must be an absolute path.")
            elif not instruction_path.is_file():
                errors.append(f"{location}.instructions does not exist: {instructions}")

    if len(project_ids) != len(set(project_ids)):
        errors.append("Project IDs must be unique.")

    gitignore = ROOT / ".gitignore"
    if gitignore.is_file() and "chief-of-staff.json" not in gitignore.read_text(
        encoding="utf-8"
    ):
        errors.append(".gitignore must exclude chief-of-staff.json.")

    persona_test = ROOT / "Test-Persona.py"
    if persona_test.is_file():
        result = subprocess.run(
            [sys.executable, str(persona_test)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            detail = " | ".join(
                line for line in (result.stdout + result.stderr).splitlines() if line
            )
            errors.append("Persona validation failed: " + detail)

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: Chief of Staff configuration, persona contract, and local paths validated.")
    print("Live connector identities and fresh-task persona responses were not checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
