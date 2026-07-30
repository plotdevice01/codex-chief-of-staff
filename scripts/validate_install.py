from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from .config_paths import ROOT, resolve_config_path
    from .test_persona import get_nested, validate as validate_persona
except ImportError:
    from config_paths import ROOT, resolve_config_path
    from test_persona import get_nested, validate as validate_persona


PLACEHOLDER = re.compile(r"(YOUR_|REPLACE_WITH_|<[^>]+>)", re.IGNORECASE)
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
SAFE_WRITE_POLICIES = {"blocked", "confirm_each"}
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
REQUIRED_FILES = (
    ".codex-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "Test-Persona.py",
    "Sync-ProjectAgents.py",
    "chief-of-staff.example.json",
    "hooks/hooks.json",
    "hooks/chief-of-staff-hook.js",
    "persona/Technical Assistant Persona - source.pdf",
    "persona/technical-assistant-persona.txt",
    "persona/persona-contract.json",
    "skills/chief-of-staff/SKILL.md",
)


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
        "communication.authored_copy_standard.minimum_version": "2.1.1",
        "communication.authored_copy_standard.required": True,
        "dependencies.ponytail.required_for_full_parity": True,
        "dependencies.ai_sloppy_copy.required_for_full_parity": True,
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


def parse_version(value: str) -> tuple[int, int, int] | None:
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)", value)
    return tuple(map(int, match.groups())) if match else None


def installed_plugin_records() -> dict[str, tuple[str, Path]]:
    found: dict[str, tuple[str, Path]] = {}
    cache = Path.home() / ".codex" / "plugins" / "cache"
    if not cache.is_dir():
        return found
    for manifest_path in cache.glob("*/*/*/.codex-plugin/plugin.json"):
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        name = manifest.get("name")
        version = manifest.get("version")
        if isinstance(name, str) and isinstance(version, str):
            current = found.get(name)
            if current is None or (parse_version(version) or (0, 0, 0)) > (
                parse_version(current[0]) or (0, 0, 0)
            ):
                found[name] = (version, manifest_path.parent.parent)
    return found


def validate_ponytail(root: Path) -> list[str]:
    warnings: list[str] = []
    skill_names = (
        "ponytail",
        "ponytail-review",
        "ponytail-audit",
        "ponytail-debt",
        "ponytail-gain",
        "ponytail-help",
    )
    for name in skill_names:
        if not (root / "skills" / name / "SKILL.md").is_file():
            warnings.append(f"Ponytail capability is missing: {name}.")
    hooks_path = root / "hooks" / "claude-codex-hooks.json"
    try:
        hooks = json.loads(hooks_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        warnings.append("Ponytail Codex hooks could not be read.")
    else:
        events = hooks.get("hooks", {})
        for event in ("SessionStart", "SubagentStart"):
            if event not in events:
                warnings.append(f"Ponytail hook is missing: {event}.")
    skill_path = root / "skills" / "ponytail" / "SKILL.md"
    try:
        skill = skill_path.read_text(encoding="utf-8-sig")
    except OSError:
        return warnings
    for required in (
        "User insists on the full version",
        "Hardware is never the ideal on paper",
        "Lazy code without its check is unfinished",
    ):
        if required not in skill:
            warnings.append(f"Ponytail full-mode rule is missing: {required}.")
    return warnings


def validate_sloppy_copy(root: Path) -> list[str]:
    warnings: list[str] = []
    hooks_path = root / "hooks" / "hooks.json"
    rules_path = root / "scripts" / "AI-Sloppy-Copy-Rules.json"
    skill_path = root / "skills" / "ai-sloppy-copy" / "SKILL.md"
    try:
        hooks = json.loads(hooks_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        warnings.append("AI Sloppy Copy hooks could not be read.")
    else:
        events = hooks.get("hooks", {})
        for event in ("UserPromptSubmit", "Stop"):
            if event not in events:
                warnings.append(f"AI Sloppy Copy hook is missing: {event}.")
    try:
        rules = json.loads(rules_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        warnings.append("AI Sloppy Copy rules could not be read.")
    else:
        counts = {
            "term": len(rules.get("banned_terms", [])),
            "expression": len(rules.get("prohibited_patterns", [])),
            "style": len(rules.get("style_rules", [])),
        }
        expected = {"term": 288, "expression": 21, "style": 34}
        if counts != expected:
            warnings.append(
                f"AI Sloppy Copy rule counts changed: expected {expected}, found {counts}."
            )
        if rules.get("standard", {}).get("version") != "2.1.1":
            warnings.append("AI Sloppy Copy standard 2.1.1 is required.")
    try:
        skill = skill_path.read_text(encoding="utf-8-sig")
    except OSError:
        warnings.append("AI Sloppy Copy skill could not be read.")
    else:
        for required in ("Evidence and voice gate", "Stop after two repair passes"):
            if required not in skill:
                warnings.append(f"AI Sloppy Copy behavior is missing: {required}.")
    return warnings


def dependency_warnings(config: dict) -> list[str]:
    warnings: list[str] = []
    installed = installed_plugin_records()
    dependencies = config.get("dependencies", {})
    mapping = {
        "ponytail": "ponytail",
        "ai_sloppy_copy": "ai-sloppy-copy",
    }
    for config_name, plugin_name in mapping.items():
        requirement = dependencies.get(config_name, {})
        if not requirement.get("required_for_full_parity"):
            continue
        minimum = str(requirement.get("minimum_version", "0.0.0"))
        record = installed.get(plugin_name)
        if not record:
            warnings.append(
                f"Full parity requires {plugin_name} {minimum} or later; "
                "it was not found in the local Codex plugin cache."
            )
            continue
        actual, root = record
        if (parse_version(actual) or (0, 0, 0)) < (
            parse_version(minimum) or (0, 0, 0)
        ):
            warnings.append(
                f"Full parity requires {plugin_name} {minimum} or later; "
                f"found {actual}."
            )
            continue
        if plugin_name == "ponytail":
            warnings.extend(validate_ponytail(root))
        elif plugin_name == "ai-sloppy-copy":
            warnings.extend(validate_sloppy_copy(root))
    return warnings


def validate_config(config_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Invalid configuration: {exc}"], warnings

    placeholders = find_placeholders(config)
    if placeholders:
        errors.append("Template placeholders remain at: " + ", ".join(placeholders))

    version = config.get("release_version", "")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append("release_version must use semantic versioning.")
    elif version != VERSION:
        errors.append(
            f"Configuration release_version is {version}; installed version is {VERSION}."
        )

    owner = config.get("owner")
    if not isinstance(owner, dict):
        errors.append("owner must be an object.")
    else:
        for key in ("name", "timezone", "role", "operating_profile"):
            if not isinstance(owner.get(key), str) or not owner[key].strip():
                errors.append(f"owner.{key} is required.")
        if not isinstance(owner.get("recurring_work"), list):
            errors.append("owner.recurring_work must be a list.")

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
        if connector.get("external_writes") not in SAFE_WRITE_POLICIES:
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
                approved = {str(value) for value in identity.values() if value}
                denied_values = {
                    str(value)
                    for item in denied
                    for value in (
                        item.values() if isinstance(item, dict) else (item,)
                    )
                    if value
                }
                if approved & denied_values:
                    errors.append(
                        f"{location} approves an identity that is also denied."
                    )
    if len(connector_ids) != len(set(connector_ids)):
        errors.append("Connector IDs must be unique.")

    policy = config.get("policy")
    if not isinstance(policy, dict):
        errors.append("policy must be an object.")
    else:
        if policy.get("default_external_writes") not in SAFE_WRITE_POLICIES:
            errors.append(
                "policy.default_external_writes must be blocked or confirm_each."
            )
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
        if project.get("enabled", True) is False:
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
                errors.append(
                    f"{location}.instructions does not exist: {instructions}"
                )
    if len(project_ids) != len(set(project_ids)):
        errors.append("Project IDs must be unique.")

    warnings.extend(dependency_warnings(config))
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Chief of Staff runtime files and local configuration."
    )
    parser.add_argument("--config")
    parser.add_argument(
        "--example",
        action="store_true",
        help="Validate the safe example instead of a local configuration.",
    )
    parser.add_argument("--strict-dependencies", action="store_true")
    args = parser.parse_args()

    errors = [
        f"Missing required file: {name}"
        for name in REQUIRED_FILES
        if not (ROOT / name).is_file()
    ]
    config_path = (
        ROOT / "chief-of-staff.example.json"
        if args.example
        else resolve_config_path(args.config)
    )
    config_errors, warnings = validate_config(config_path)
    errors.extend(config_errors)
    persona_errors, _ = validate_persona(config_path)
    errors.extend(f"Persona validation: {error}" for error in persona_errors)

    if args.strict_dependencies:
        errors.extend(warnings)
        warnings = []
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: Chief of Staff v{VERSION} validated with {config_path}.")
    print("Live connector identities and fresh-task responses were not checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
