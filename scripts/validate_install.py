from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from .config_paths import ROOT, resolve_config_path
    from .sync_content_runtime import check as check_content_runtime
    from .test_persona import get_nested, validate as validate_persona
except ImportError:
    from config_paths import ROOT, resolve_config_path
    from sync_content_runtime import check as check_content_runtime
    from test_persona import get_nested, validate as validate_persona


PLACEHOLDER = re.compile(r"(YOUR_|REPLACE_WITH_|<[^>]+>)", re.IGNORECASE)
RELEASE_VERSION = re.compile(r"^\d+\.\d+\.\d+$")
SAFE_WRITE_POLICIES = {"blocked", "plan_scoped"}
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
REQUIRED_FILES = (
    ".codex-plugin/plugin.json",
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
    "scripts/live_acceptance_harness.py",
    "scripts/package_files.py",
    "scripts/stage_install.py",
    "scripts/verify_installed_cache.py",
    "skills/chief-of-staff/SKILL.md",
    "skills/chief-of-staff/references/universal-request-contract.md",
    "skills/chief-of-staff/references/capability-registry.json",
    "skills/chief-of-staff/references/content-production.md",
    "skills/chief-of-staff/references/live-acceptance.md",
    "skills/chief-of-staff/references/paid-video-creative.md",
    "skills/chief-of-staff/scripts/route_request.py",
    "skills/chief-of-staff/scripts/content_intelligence.py",
    "skills/chief-of-staff/scripts/validate_paid_video.py",
    "skills/chief-of-staff/vendor/manifest.json",
    "skills/chief-of-staff/internal/icm-architect/workflow.md",
    "skills/chief-of-staff/internal/icm-architect/LICENSE",
    "skills/chief-of-staff/internal/icm-architect/UPSTREAM.json",
    "tests/fixtures/paid-video/valid-professional-service.json",
    "tests/fixtures/paid-video/sanitized-failed-campaign.json",
    "tests/test_live_acceptance_harness.py",
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
        "communication.authored_copy_standard.minimum_version": "2.2.0",
        "communication.authored_copy_standard.required": True,
        "execution.default_tier": "standard",
        "execution.quick_tier_enabled": False,
        "execution.standard.model": "gpt-5.6-sol",
        "execution.standard.reasoning_effort": "medium",
        "execution.standard.workspace_scan": "relevant_sources",
        "execution.standard.validation": "focused_and_proportional",
        "execution.expert_high_risk.model": "gpt-5.6-sol",
        "execution.expert_high_risk.reasoning_effort": "high_or_xhigh",
        "execution.expert_high_risk.workspace_scan": "all_affected_boundaries",
        "execution.expert_high_risk.validation": "full_relevant_suite",
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


def skill_ids(root: Path) -> set[str]:
    names: set[str] = set()
    for path in root.glob("skills/*/SKILL.md"):
        match = re.search(r"(?m)^name:\s*([^\s]+)\s*$", path.read_text(encoding="utf-8-sig"))
        if match:
            names.add(match.group(1))
    return names


def duplicate_skill_warnings(roots: dict[str, Path]) -> list[str]:
    owners: dict[str, list[str]] = {}
    for plugin_name, root in roots.items():
        for skill_name in skill_ids(root):
            owners.setdefault(skill_name, []).append(plugin_name)
    return [
        f"Duplicate skill ID {skill_name} is provided by: {', '.join(sorted(providers))}."
        for skill_name, providers in sorted(owners.items())
        if len(providers) > 1
    ]


def dependency_warnings(config: dict) -> list[str]:
    del config
    discovered = skill_ids(ROOT)
    if discovered != {"chief-of-staff"}:
        return [
            "Chief must expose exactly one discoverable skill; found: "
            + ", ".join(sorted(discovered))
        ]
    expected = ROOT / "skills" / "chief-of-staff" / "SKILL.md"
    if sorted(ROOT.glob("skills/**/SKILL.md")) != [expected]:
        return ["Chief internal workflows must not expose nested SKILL.md entries."]
    return duplicate_skill_warnings({"chief-of-staff": ROOT})


def install_receipt(config_path: Path, config: dict) -> dict:
    del config
    vendor = json.loads(
        (ROOT / "skills" / "chief-of-staff" / "vendor" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    return {
        "schema_version": 1,
        "chief_of_staff_version": VERSION,
        "config": str(config_path),
        "discoverable_skills": sorted(skill_ids(ROOT)),
        "standalone_dependencies": [],
        "bundled_content_runtime": {
            name: {
                "version": item["version"],
                "commit": item["commit"],
                "files": len(item["files"]),
                "status": "found",
            }
            for name, item in vendor["packages"].items()
        },
    }


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

    if config.get("config_schema_version") != 2:
        errors.append("config_schema_version must be 2 for plan-scoped authorization.")

    version = config.get("release_version", "")
    if not isinstance(version, str) or not RELEASE_VERSION.fullmatch(version):
        errors.append("release_version must use a three-part semantic version.")
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
            errors.append(f"{location}.external_writes must be blocked or plan_scoped.")
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
                "policy.default_external_writes must be blocked or plan_scoped."
            )
        if policy.get("automatic_authority_expansion") is not False:
            errors.append("policy.automatic_authority_expansion must be false.")
        authorization = policy.get("plan_scoped_authorization")
        expected_authorization = {
            "full_access_instruction": "all_in_scope_actions_until_completion",
            "reconfirm_only_for": "material_scope_change_or_missing_material_decision",
            "safe_retries_do_not_reconfirm": True,
            "owner_can_steer_or_revoke": True,
        }
        if authorization != expected_authorization:
            errors.append(
                "policy.plan_scoped_authorization must define durable full-access, "
                "material-change-only reconfirmation, safe retries, and owner steering."
            )
        for key in ("delete", "public_post", "permission_change"):
            if policy.get(key) not in SAFE_WRITE_POLICIES:
                errors.append(f"policy.{key} must be blocked or plan_scoped.")
        if policy.get("financial_action") != "blocked":
            errors.append("policy.financial_action must remain blocked.")

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
    parser.add_argument("--doctor", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    errors = [
        f"Missing required file: {name}"
        for name in REQUIRED_FILES
        if not (ROOT / name).is_file()
    ]
    try:
        check_content_runtime()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        errors.append(f"Bundled content runtime failed validation: {exc}")
    config_path = (
        ROOT / "chief-of-staff.example.json"
        if args.example
        else resolve_config_path(args.config)
    )
    config_errors, warnings = validate_config(config_path)
    errors.extend(config_errors)
    persona_errors, _ = validate_persona(config_path)
    errors.extend(f"Persona validation: {error}" for error in persona_errors)

    if args.strict_dependencies or args.doctor:
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
    if args.doctor or args.receipt:
        config = json.loads(config_path.read_text(encoding="utf-8-sig"))
        receipt = install_receipt(config_path, config)
        if args.receipt:
            args.receipt.parent.mkdir(parents=True, exist_ok=True)
            args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
            print(f"PASS: install receipt written to {args.receipt}.")
        if args.doctor:
            print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
