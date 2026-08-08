from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "chief-of-staff"
VENDOR = SKILL / "vendor"


def run(script: Path, *args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def main() -> int:
    run(ROOT / "scripts" / "sync_content_runtime.py", "check")
    output = run(SKILL / "scripts" / "content_intelligence.py", "--self-test")
    assert "hooks=751 scripts=7 ctas=39" in output
    route_output = run(SKILL / "scripts" / "route_request.py", "--self-test")
    assert "discoverable_skill=chief-of-staff" in route_output
    sparse = json.loads(
        run(
            SKILL / "scripts" / "content_intelligence.py",
            "--content-class",
            "business",
            "--format",
            "video",
            "--query",
            "small-business owners bookkeeping consultation 20 minutes",
            "--cta-category",
            "sales",
            "--cta-text",
            "Book the 20-minute consultation",
            "--offer-type",
            "paid",
        )
    )
    assert sparse["recommended"] == {
        "hook": "business-089",
        "script": "pbl-script-07",
        "cta": "pbl-cta-sales-13",
    }
    paid_offer = json.loads(
        run(
            SKILL / "scripts" / "content_intelligence.py",
            "--content-class",
            "business",
            "--format",
            "video",
            "--query",
            "small-business owners paid professional assessment",
            "--cta-category",
            "sales",
            "--cta-text",
            "Book the paid assessment",
            "--offer-type",
            "paid",
        )
    )
    assert paid_offer["recommended"]["cta"] == "pbl-cta-sales-13"
    assert {item["id"] for item in paid_offer["compatibility"]["rejected_ctas"]} == {
        "pbl-cta-sales-08"
    }
    assert "free" not in paid_offer["ctas"][0]["cta"].casefold()

    paid_validator = SKILL / "scripts" / "validate_paid_video.py"
    valid_fixture = ROOT / "tests" / "fixtures" / "paid-video" / "valid-professional-service.json"
    invalid_fixture = ROOT / "tests" / "fixtures" / "paid-video" / "sanitized-failed-campaign.json"
    valid_result = subprocess.run(
        [sys.executable, str(paid_validator), str(valid_fixture)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert valid_result.returncode == 0
    assert json.loads(valid_result.stdout)["status"] == "PASS"
    invalid_result = subprocess.run(
        [sys.executable, str(paid_validator), str(invalid_fixture)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert invalid_result.returncode == 1
    failure_codes = {item["code"] for item in json.loads(invalid_result.stdout)["failures"]}
    assert {
        "PV-SOURCE-001",
        "PV-VOICE-001",
        "PV-LIBRARY-001",
        "PV-OFFER-001",
        "PV-VISUAL-001",
        "PV-VISUAL-002",
        "PV-VARIATION-001",
        "PV-PROOF-001",
        "PV-PERFORMANCE-001",
        "PV-DISCLOSURE-001",
        "PV-RECEIPT-001",
    } <= failure_codes

    sloppy = VENDOR / "ai-sloppy-copy"
    result = subprocess.run(
        [
            sys.executable,
            str(sloppy / "scripts" / "ai_sloppy_copy.py"),
            "--rules",
            str(sloppy / "scripts" / "AI-Sloppy-Copy-Rules.json"),
            "--text",
            "Unlock your potential.",
            "--json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert json.loads(result.stdout)

    contract = (SKILL / "references" / "content-production.md").read_text(encoding="utf-8")
    universal = (SKILL / "references" / "universal-request-contract.md").read_text(
        encoding="utf-8"
    )
    registry = (SKILL / "references" / "capability-registry.json").read_text(
        encoding="utf-8"
    )
    paid_video = (SKILL / "references" / "paid-video-creative.md").read_text(
        encoding="utf-8"
    )
    for trigger in ("video ad", "paid campaign", "carousel", "brand voice", "social post"):
        assert trigger in registry.casefold()
    for control in (
        "The user does not select Brand Voice Factory, Crafty Carousels, or AI Sloppy Copy.",
        "hooks=751",
        "scripts=7",
        "ctas=39",
        "Do not produce general copy and call it an ad.",
        "Do not cite a hook ID after replacing it with a generic callout.",
        "Use the one `recommended` hook, script, and CTA",
        "Return an execution receipt",
        "Offer compatibility",
        "--text",
        "Do not create a temporary file merely to",
    ):
        assert control in contract
    for control in (
        "Chief is the only discoverable skill.",
        "Never ask the user to choose a specialist.",
        "generic` fallback",
    ):
        assert control in universal
    for control in (
        "first-frame action",
        "visual progression",
        "751-hook, 7-script, and 39-CTA",
        "free-download CTA",
        "cosmetic hook rewrites",
        "execution receipt conflicts",
        "Sanitized",
    ):
        assert control in paid_video
    private_name = " ".join(("To", "Know", "Oneself"))
    assert private_name not in paid_video
    assert "../vendor/" not in contract
    assert "<SKILL_ROOT>/vendor/crafty-carousels/workflow.md" in contract
    assert not (ROOT / "skills" / "viral-carousel-factory").exists()
    discovered = sorted(ROOT.glob("skills/*/SKILL.md"))
    assert discovered == [SKILL / "SKILL.md"]
    assert sorted(ROOT.glob("skills/**/SKILL.md")) == [SKILL / "SKILL.md"]
    print("PASS: one Chief route, offer-safe paid video, complete libraries, and final checker validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
