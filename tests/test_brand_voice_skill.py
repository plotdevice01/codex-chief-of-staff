from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "brand-voice-copywriter"
REQUIRED = (
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/new_brand_voice_project.py",
    "references/brand-voice-package-spec.md",
    "references/copy-production.md",
    "references/governance-and-claims.md",
    "references/intake-and-evidence.md",
    "references/qa-and-measurement.md",
    "references/sloppy-copy-qa.md",
    "assets/client-workspace/AGENTS.md",
    "assets/client-workspace/CONTEXT.md",
    "assets/client-workspace/STATUS.md",
)
STAGES = (
    "01_intake",
    "02_evidence",
    "03_voice",
    "04_package",
    "05_copy",
    "06_release",
)


def main() -> int:
    missing = [relative for relative in REQUIRED if not (SKILL / relative).is_file()]
    assert not missing, f"Missing Brand Voice skill files: {missing}"

    for stage in STAGES:
        contract = SKILL / "assets" / "client-workspace" / "stages" / stage / "CONTEXT.md"
        assert contract.is_file(), f"Missing stage contract: {stage}"
        text = contract.read_text(encoding="utf-8")
        for heading in ("## Inputs", "## Process", "## Outputs", "## Human check"):
            assert heading in text, f"{stage} lacks {heading}"

    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for required in (
        "Use the bundled ICM Pipeline",
        "AI Sloppy Copy is mandatory",
        "Never infer `Public ready` from package approval",
        "Hook -> Value -> CTA",
    ):
        assert required in skill_text, f"Missing Brand Voice control: {required}"

    result = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "new_brand_voice_project.py"), "--self-test"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "self_test=PASS" in result.stdout

    print("PASS: Brand Voice skill files, ICM contracts, controls, and project stamp validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
