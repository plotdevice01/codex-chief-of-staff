from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

try:
    from .config_paths import ROOT
except ImportError:
    from config_paths import ROOT


PERSONA_DIR = ROOT / "persona"
SOURCE_PDF = PERSONA_DIR / "Technical Assistant Persona - source.pdf"
PERSONA_TEXT = PERSONA_DIR / "technical-assistant-persona.txt"
CONTRACT = PERSONA_DIR / "persona-contract.json"
AGENTS = ROOT / "AGENTS.md"
EXAMPLE_CONFIG = ROOT / "chief-of-staff.example.json"
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
HOOKS = ROOT / "hooks" / "hooks.json"
SKILL = ROOT / "skills" / "chief-of-staff" / "SKILL.md"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
MANIFEST_VERSION = VERSION


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def canonical_text_sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest().upper()


def get_nested(data: dict, dotted_path: str):
    current = data
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted_path)
        current = current[part]
    return current


def validate(config_path: Path | None = None) -> tuple[list[str], dict]:
    errors: list[str] = []
    config_file = config_path or EXAMPLE_CONFIG
    required_files = (
        SOURCE_PDF,
        PERSONA_TEXT,
        CONTRACT,
        AGENTS,
        config_file,
        MANIFEST,
        HOOKS,
        SKILL,
    )
    for path in required_files:
        if not path.is_file():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")
    if errors:
        return errors, {}

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    persona_text = PERSONA_TEXT.read_text(encoding="utf-8")
    agents_text = AGENTS.read_text(encoding="utf-8")
    config = json.loads(config_file.read_text(encoding="utf-8-sig"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    hooks = json.loads(HOOKS.read_text(encoding="utf-8"))

    actual_pdf_hash = sha256(SOURCE_PDF)
    if actual_pdf_hash != contract.get("source_pdf_sha256"):
        errors.append("Persona source PDF hash does not match the contract.")
    actual_text_hash = canonical_text_sha256(PERSONA_TEXT)
    if actual_text_hash != contract.get("verbatim_text_sha256"):
        errors.append("Verbatim persona text hash does not match the contract.")

    requirements = contract.get("requirements", [])
    requirement_ids = [
        item.get("id") for item in requirements if isinstance(item, dict)
    ]
    if len(requirement_ids) != len(set(requirement_ids)):
        errors.append("Persona requirement IDs must be unique.")
    for item in requirements:
        if not isinstance(item, dict) or not item.get("id") or not item.get("match"):
            errors.append("Every persona requirement needs an id and match value.")
        elif item["match"] not in persona_text:
            errors.append(f"{item['id']} is missing from the verbatim persona text.")

    integration = contract.get("integration_requirements", [])
    integration_ids = [
        item.get("id") for item in integration if isinstance(item, dict)
    ]
    if len(integration_ids) != len(set(integration_ids)):
        errors.append("Integration requirement IDs must be unique.")
    for item in integration:
        if not isinstance(item, dict) or not item.get("id") or not item.get("match"):
            errors.append("Every integration requirement needs an id and match value.")
        elif item["match"] not in agents_text:
            errors.append(f"{item['id']} is missing from AGENTS.md.")

    expected_config = {
        "release_version": VERSION,
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
        "dependencies.ponytail.required_for_full_parity": True,
        "dependencies.ai_sloppy_copy.minimum_version": "0.5.0",
        "dependencies.ai_sloppy_copy.required_for_full_parity": True,
        "dependencies.brand_voice_factory.minimum_version": "0.2.0",
        "dependencies.brand_voice_factory.required_for_full_parity": True,
        "dependencies.crafty_carousels.minimum_version": "0.6.0",
        "dependencies.crafty_carousels.required_for_full_parity": True,
    }
    for path, expected in expected_config.items():
        try:
            actual = get_nested(config, path)
        except KeyError:
            errors.append(f"Missing behavior configuration: {path}")
            continue
        if actual != expected:
            errors.append(
                f"Behavior configuration mismatch at {path}: "
                f"expected {expected!r}, got {actual!r}"
            )

    live_tests = contract.get("live_acceptance_tests", [])
    live_ids = [item.get("id") for item in live_tests if isinstance(item, dict)]
    if len(live_ids) != len(set(live_ids)):
        errors.append("Live acceptance test IDs must be unique.")
    if len(live_tests) != 12:
        errors.append("Exactly twelve live acceptance tests are required.")
    for item in live_tests:
        if (
            not isinstance(item, dict)
            or not item.get("id")
            or not item.get("prompt")
            or not item.get("pass_criteria")
        ):
            errors.append("Every live acceptance test needs an id, prompt, and criteria.")

    if manifest.get("name") != "chief-of-staff":
        errors.append("Plugin manifest name must be chief-of-staff.")
    if manifest.get("version") != MANIFEST_VERSION:
        errors.append("Plugin manifest version does not match the host version.")
    if "SessionStart" not in hooks.get("hooks", {}):
        errors.append("SessionStart hook is missing.")
    if "SubagentStart" not in hooks.get("hooks", {}):
        errors.append("SubagentStart hook is missing.")
    if "TODO" in SKILL.read_text(encoding="utf-8"):
        errors.append("Chief of Staff skill still contains TODO text.")

    forbidden_regressions = (
        '"compression": "concise"',
        '"sarcasm": "off"',
        '"witty_advice": false',
        "optional personality",
    )
    combined = agents_text + "\n" + json.dumps(config)
    for value in forbidden_regressions:
        if value in combined:
            errors.append(f"Behavior regression found: {value}")

    skill_text = SKILL.read_text(encoding="utf-8")
    required_skill_blocks = (
        "For client-facing outputs, make them meeting-ready and operator-level.",
        "Define the workflow, data sources, tool or API access",
        "Verify each connector before first use.",
        "Use `Sync-ProjectAgents.py` to apply the fail-safe Chief of Staff loader",
        "Use idempotency when available.",
        "## Apply ICM by default",
        "ICM is the default operating architecture.",
        "Invoke the bundled `icm-architect` skill automatically",
        "Do not import client names or project facts from private",
        "Before proposing files, name ICM and state the repeating unit.",
        "Do not replace the canonical form name with a new label.",
        "Do not propose files first. Mark missing inputs as unknown",
        "Run the twelve",
    )
    for value in required_skill_blocks:
        if value not in skill_text:
            errors.append(f"Contextual Chief workflow is missing: {value}")
    required_agents_rules = (
        "Apply `persona/technical-assistant-persona.txt` in full.",
        "For coding and technical build work, apply the installed Ponytail skill",
        "For client-facing work, use the Chief skill's client-deliverable workflow.",
        "Use only these two tiers. There is no quick tier.",
        "`Expert/high-risk` applies",
        "Use idempotency when available.",
        "Apply the compact ICM task contract to every non-trivial task",
        "ICM is the default operating architecture for non-trivial work.",
        "invoke the bundled ICM",
        "If the user has not named a registered project, keep the task generic",
        "Do not invent data sources or connector names.",
        "Before proposing files, name ICM and state the repeating",
        "Use one canonical form name from ICM Architect",
        "Do not propose files before those fields. Mark missing inputs as",
    )
    for value in required_agents_rules:
        if value not in agents_text:
            errors.append(f"Core Chief router is missing: {value}")
    if agents_text.count("Default communication mode is 85% compression.") != 1:
        errors.append("85% compression must have one canonical core definition.")
    for removed in (
        "## Ponytail efficiency ladder",
        "6. Execute once.",
        "Use 85% compression. Lead with the answer.",
    ):
        if removed in agents_text:
            errors.append(f"Retired duplicate instruction remains: {removed}")

    metrics = {
        "persona_requirements": len(requirements),
        "integration_requirements": len(integration),
        "live_acceptance_tests": len(live_tests),
        "source_pdf_sha256": actual_pdf_hash,
        "persona_text_sha256": actual_text_hash,
    }
    return errors, metrics


def main() -> int:
    errors, metrics = validate()
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(
        f"PASS: {metrics['persona_requirements']}/"
        f"{metrics['persona_requirements']} persona requirements preserved."
    )
    print(
        f"PASS: {metrics['integration_requirements']} Chief of Staff integration "
        "rules and behavior defaults validated."
    )
    print(
        f"PASS: {metrics['live_acceptance_tests']} live acceptance scenarios "
        "are defined."
    )
    print(f"PDF SHA-256: {metrics['source_pdf_sha256']}")
    print(f"Persona text SHA-256: {metrics['persona_text_sha256']}")
    print("Live model responses still require a fresh Codex task.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
