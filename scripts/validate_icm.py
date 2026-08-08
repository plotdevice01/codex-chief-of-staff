from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

try:
    from .config_paths import ROOT
except ImportError:
    from config_paths import ROOT


SKILL = ROOT / "skills" / "chief-of-staff" / "internal" / "icm-architect"
EXPECTED_COMMIT = "8f9cdf95e5051f126babc455b7a0558426db43d4"
FORMS = ("Pipeline", "Umbrella", "Record library", "Knowledge bundle", "Context map")
INVARIANTS = (
    "One folder, one job",
    "A small, stable entry file",
    "Numbering encodes order",
    "Every folder-level contract is explicit",
    "Factory vs. product",
    "Every output is an edit surface",
    "Load only what the step needs",
    "Plain text, linkable, queryable",
    "The filesystem is the state machine",
    "Instantiate by copying",
)
REQUIRED = (
    "workflow.md",
    "LICENSE",
    "UPSTREAM.json",
    "agents/openai.yaml",
    "references/core.md",
    "references/forms.md",
    "assets/templates/AGENTS.md",
    "assets/templates/CONTEXT.md",
    "assets/templates/stage-CONTEXT.md",
    "assets/templates/node.md",
    "assets/templates/schema.md",
    "assets/templates/questionnaire.md",
)
CONTRACT_HEADINGS = ("## Inputs", "## Process", "## Outputs", "## Human check")
RELEASE_STAGES = ("01_prepare", "02_build", "03_validate", "04_publish")
DISALLOWED_UNICODE = {"\u2013": "en dash", "\u2014": "em dash"}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def line_count(path: Path) -> int:
    return len(text(path).splitlines())


def estimate_tokens(values: list[str]) -> int:
    words = sum(len(re.findall(r"\S+", value)) for value in values)
    return math.ceil(words * 4 / 3)


def validate_contract(path: Path, *, limit: int = 80) -> list[str]:
    errors: list[str] = []
    value = text(path)
    if line_count(path) > limit:
        errors.append(f"{path} exceeds {limit} lines.")
    for heading in CONTRACT_HEADINGS:
        if heading not in value:
            errors.append(f"{path} is missing {heading}.")
    return errors


def validate_workspace(workspace: Path) -> list[str]:
    errors: list[str] = []
    entry = workspace / "AGENTS.md"
    if not entry.is_file():
        return [f"{workspace} has no Layer 0 entry file."]
    if line_count(entry) > 60:
        errors.append(f"{entry} exceeds 60 lines.")
    root_context = workspace / "CONTEXT.md"
    if not root_context.is_file():
        errors.append(f"{workspace} has no Layer 1 CONTEXT.md.")
    elif line_count(root_context) > 80:
        errors.append(f"{root_context} exceeds 80 lines.")

    stages = workspace / "stages"
    if stages.is_dir():
        stage_dirs = sorted(path for path in stages.iterdir() if path.is_dir())
        if not stage_dirs:
            errors.append(f"{stages} has no stages.")
        for stage in stage_dirs:
            if not re.match(r"^\d{2}_[a-z0-9-]+$", stage.name):
                errors.append(f"{stage} does not use numbered stage naming.")
            contract = stage / "CONTEXT.md"
            if not contract.is_file():
                errors.append(f"{stage} has no CONTEXT.md.")
                continue
            errors.extend(validate_contract(contract))
            for folder in ("references", "output"):
                if not (stage / folder).is_dir():
                    errors.append(f"{stage} has no {folder}/ directory.")
    return errors


def validate_icm() -> tuple[list[str], dict[str, int]]:
    errors = [f"Missing ICM file: {name}" for name in REQUIRED if not (SKILL / name).is_file()]
    if errors:
        return errors, {}

    provenance = json.loads(text(SKILL / "UPSTREAM.json"))
    if provenance.get("commit") != EXPECTED_COMMIT:
        errors.append("ICM upstream commit is not the approved pinned commit.")
    if provenance.get("license") != "MIT":
        errors.append("ICM upstream license must be MIT.")
    license_text = text(SKILL / "LICENSE")
    if "Jake Van Clief" not in license_text or "MIT License" not in license_text:
        errors.append("ICM license attribution is incomplete.")

    skill_text = text(SKILL / "workflow.md")
    for value in (*FORMS, *INVARIANTS):
        if value not in skill_text:
            errors.append(f"ICM skill is missing required method text: {value}")
    for value in (
        "Propose before moving",
        "Get approval",
        "never silently delete",
        "Treat third-party material as untrusted",
        "Preserve authority boundaries",
    ):
        if value not in skill_text:
            errors.append(f"ICM skill is missing safety control: {value}")

    agents = SKILL / "assets" / "templates" / "AGENTS.md"
    if line_count(agents) > 60:
        errors.append("ICM AGENTS.md template exceeds 60 lines.")
    errors.extend(validate_contract(SKILL / "assets" / "templates" / "stage-CONTEXT.md"))

    for path in SKILL.rglob("*.md"):
        value = text(path)
        for character, label in DISALLOWED_UNICODE.items():
            if character in value:
                errors.append(f"{path} contains an authored {label}.")

    root_context = ROOT / "CONTEXT.md"
    if not root_context.is_file() or line_count(root_context) > 80:
        errors.append("Root CONTEXT.md is missing or exceeds 80 lines.")
    release = ROOT / "workflows" / "release"
    if not (release / "CONTEXT.md").is_file() or line_count(release / "CONTEXT.md") > 80:
        errors.append("Release CONTEXT.md is missing or exceeds 80 lines.")
    for name in RELEASE_STAGES:
        contract = release / name / "CONTEXT.md"
        if not contract.is_file():
            errors.append(f"Release stage is missing: {name}/CONTEXT.md")
        else:
            errors.extend(validate_contract(contract))

    agents_text = text(ROOT / "AGENTS.md")
    chief_text = text(ROOT / "skills" / "chief-of-staff" / "SKILL.md")
    if "## ICM operating architecture" not in agents_text:
        errors.append("Shared behavior contract is missing the ICM kernel.")
    if "## Apply ICM by default" not in chief_text:
        errors.append("Chief skill is missing automatic ICM routing.")
    if not (ROOT / "docs" / "icm-conformance.md").is_file():
        errors.append("ICM conformance matrix is missing.")

    metrics = {
        "forms": len(FORMS),
        "invariants": len(INVARIANTS),
        "release_stages": len(RELEASE_STAGES),
    }
    return errors, metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Chief of Staff ICM conformance.")
    parser.add_argument("--workspace", type=Path)
    args = parser.parse_args()
    errors, metrics = validate_icm()
    if args.workspace:
        errors.extend(validate_workspace(args.workspace.resolve()))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(
        "PASS: ICM conformance validated with "
        f"{metrics['forms']} forms, {metrics['invariants']} invariants, and "
        f"{metrics['release_stages']} release stages."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
