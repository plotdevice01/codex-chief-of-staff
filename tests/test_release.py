from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_repository import (  # noqa: E402
    model_acceptance_release_status,
    validate_model_acceptance,
    validate_release_waiver,
)
from scripts.live_acceptance_harness import validate_receipt  # noqa: E402
from scripts.validate_install import duplicate_skill_warnings  # noqa: E402


def main() -> int:
    chief_skill = (ROOT / "skills" / "chief-of-staff" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    for required in (
        "## Run a chat-first client delivery cycle",
        "Ask one missing intake question at a time.",
        "Do not require a spreadsheet",
        "Scope approval does not replace a configured external-write",
        "Wait for one immediate confirmation for that delivery cycle.",
        "Use one parent task",
        "for the delivery cycle.",
        "Create one subtask",
        "per included deliverable.",
        "Read every saved ClickUp record back.",
        "references/live-acceptance.md",
        "separate UI and runtime evidence",
        "Never create or delegate tasks",
    ):
        assert required in chief_skill, f"Missing chat-first delivery rule: {required}"

    live_acceptance = (
        ROOT / "skills" / "chief-of-staff" / "references" / "live-acceptance.md"
    ).read_text(encoding="utf-8")
    for required in (
        "self-report cannot prove",
        "ui_evidence=owner_verified",
        "runtime value of `codex` or `chatgpt-work` is valid",
        "cannot satisfy ChatGPT Work acceptance.",
        "**Ask for approval**",
        "built-in `:read-only` permission profile",
        "Run all scenarios inline in the one fresh task.",
        "temporary files",
        "invalidates the entire run",
    ):
        assert required in live_acceptance, f"Missing read-only acceptance rule: {required}"

    assert not (ROOT / "skills" / "brand-voice-copywriter" / "SKILL.md").exists()
    with tempfile.TemporaryDirectory() as folder:
        temp = Path(folder)
        roots = {}
        for plugin in ("one", "two"):
            root = temp / plugin
            skill = root / "skills" / "duplicate" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: duplicate\n---\n", encoding="utf-8")
            roots[plugin] = root
        warnings = duplicate_skill_warnings(roots)
        assert len(warnings) == 1 and "Duplicate skill ID duplicate" in warnings[0]

    evidence = json.loads(
        (ROOT / "tests" / "model-acceptance.json").read_text(encoding="utf-8")
    )
    release_status = model_acceptance_release_status(evidence)
    assert release_status == "pass_with_waiver"
    assert not validate_model_acceptance(require_pass=True)
    receipt_version = evidence.get("carried_forward_from_release", evidence["release_version"])
    work_receipt = json.loads(
        (ROOT / "tests" / "receipts" / f"chatgpt-work-v{receipt_version}.json").read_text(
            encoding="utf-8"
        )
    )
    assert not validate_receipt(
        work_receipt, "chatgpt-work", expected_version=receipt_version
    )

    waived = copy.deepcopy(evidence)
    waived["models"]["gpt-5.6-sol"]["status"] = "pass"
    waived["models"]["gpt-5.6-terra"]["status"] = "pending"
    waived["hosts"]["codex"]["status"] = "pass"
    waived["hosts"]["chatgpt-work"]["status"] = "pass"
    waived["installed_runtime_smoke"]["status"] = "pass"
    waived["release_waiver"] = {
        "status": "approved",
        "release_version": evidence["release_version"],
        "approved_at": "2026-08-05T00:00:00-05:00",
        "approved_by": "repository_owner",
        "waived_checks": ["models.gpt-5.6-terra"],
        "reason": "Version-bound test fixture for pending Terra evidence.",
    }
    assert model_acceptance_release_status(waived) == "pass_with_waiver"
    assert not validate_release_waiver(waived)[1]

    failed = copy.deepcopy(waived)
    failed["models"]["gpt-5.6-terra"]["status"] = "fail"
    assert model_acceptance_release_status(failed) == "candidate"
    _, errors = validate_release_waiver(failed)
    assert errors

    print(
        "PASS: chat-first delivery rules and release waiver controls are present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
