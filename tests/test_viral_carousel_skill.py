from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "viral-carousel-factory"
REQUIRED = (
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/new_carousel_project.py",
    "references/production-system.md",
    "references/client-intake.md",
    "references/platform-delivery.md",
    "references/governance-measurement.md",
    "references/sources.md",
    "assets/client-workspace/AGENTS.md",
    "assets/client-workspace/CONTEXT.md",
    "assets/client-workspace/STATUS.md",
    "assets/client-workspace/setup/client-intake.md",
    "assets/client-workspace/_shared/voice.md",
    "assets/client-workspace/_shared/people-and-likeness.md",
    "assets/client-workspace/_shared/asset-register.csv",
    "assets/client-workspace/_shared/claim-register.csv",
)
STAGES = (
    "01_intake",
    "02_strategy_copy",
    "03_anchor",
    "04_production",
    "05_release",
)


def main() -> int:
    missing = [relative for relative in REQUIRED if not (SKILL / relative).is_file()]
    assert not missing, f"Missing Viral Carousel skill files: {missing}"

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
        "one unanswered blocking question at a time",
        "three distinct cover candidates",
        "one slide at a time",
        "Never infer `Release ready`",
    ):
        assert required in skill_text, f"Missing Viral Carousel control: {required}"

    script = SKILL / "scripts" / "new_carousel_project.py"
    result = subprocess.run(
        [sys.executable, str(script), "self-test"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "self_test=PASS" in result.stdout

    with tempfile.TemporaryDirectory() as folder:
        workspace = Path(folder) / "workspace"
        subprocess.run(
            [
                sys.executable,
                str(script),
                "init",
                "--client-name",
                "Example Co",
                "--owner",
                "Content Lead",
                "--output",
                str(workspace),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        result = subprocess.run(
            [
                sys.executable,
                str(script),
                "new-run",
                "--workspace",
                str(workspace),
                "--slug",
                "one-sharp-idea",
                "--route",
                "instagram-native",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        run = Path(result.stdout.strip())
        manifest = json.loads((run / "run.json").read_text(encoding="utf-8"))
        assert (workspace / "_shared" / "media").is_dir()
        assert (workspace / "setup" / "client-intake.md").is_file()
        assert set(manifest["client_profile_versions"]) == {
            "brand",
            "voice",
            "people_likeness",
            "asset_register",
            "claim_register",
        }
        assert manifest["approvals"]["intake"] is False
        assert manifest["slide_count"] == 8
        assert [slide["role"] for slide in manifest["slides"]] == [
            "hook",
            "transition",
            "tease",
            "tease",
            "tease",
            "tease",
            "climax",
            "action",
        ]
        subprocess.run(
            [sys.executable, str(script), "validate", "--run", str(run)],
            check=True,
            capture_output=True,
            text=True,
        )

    print("PASS: Viral Carousel files, Pipeline contracts, controls, and cold walk validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
