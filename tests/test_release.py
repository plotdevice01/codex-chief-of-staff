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
)
from scripts.validate_install import duplicate_skill_warnings  # noqa: E402
from scripts.package_files import copied_files  # noqa: E402


def main() -> int:
    chief_skill = (ROOT / "skills" / "chief-of-staff" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    for required in (
        "## Run a chat-first client delivery cycle",
        "Ask one missing intake question at a time.",
        "Do not require a spreadsheet",
        "durable authorization for every included production and delivery action",
        "second confirmation gate for the record batch.",
        "Use one parent task",
        "for the delivery cycle.",
        "Create one subtask",
        "per included deliverable.",
        "Read every saved ClickUp record back.",
        "references/live-acceptance.md",
        "separate UI and runtime evidence",
        "Never create or delegate tasks",
        "put `Next steps` immediately before",
        "Never insert a closing summary before the trace",
    ):
        assert required in chief_skill, f"Missing chat-first delivery rule: {required}"
    for forbidden in (
        "Scope approval does not replace",
        "Wait for one immediate confirmation",
        "Release does not authorize publication",
        "Run `--apply` only after the workspace owner approves",
    ):
        assert forbidden not in chief_skill, f"Stale repeated-approval rule remains: {forbidden}"

    universal = (
        ROOT / "skills" / "chief-of-staff" / "references" / "universal-request-contract.md"
    ).read_text(encoding="utf-8")
    for required in (
        "## Plan-scoped authorization",
        "Do not request a new approval for each step of an approved plan.",
        "full access is",
        "idempotent retry does not require new",
        "Never insert a closing",
    ):
        assert required in universal, f"Missing plan-scoped authorization rule: {required}"

    content_production = (
        ROOT / "skills" / "chief-of-staff" / "references" / "content-production.md"
    ).read_text(encoding="utf-8")
    for required in (
        "quality record is not another permission prompt",
        "approved plan already includes downstream production",
    ):
        assert required in content_production, f"Missing bundled-workflow override: {required}"
    assert "Do not generate slides before exact copy and the anchor direction are approved." not in content_production

    live_acceptance = (
        ROOT / "skills" / "chief-of-staff" / "references" / "live-acceptance.md"
    ).read_text(encoding="utf-8")
    for required in (
        "self-report cannot prove",
        "ui_evidence=owner_verified",
        "runtime value of `codex` or `chatgpt-work` is valid",
        "cannot satisfy ChatGPT Work acceptance.",
        "**Ask for approval**",
        "**Ask for Approval**, **Approved",
        "codex --ask-for-approval never exec",
        "--plugin-root <installed-plugin-root>",
        "--runtime-version <observed-runtime-version>",
        "evidence_mode=embedded_preflight",
        "zero model tool calls",
        "ui_surface=codex-cli",
        "reason to ask for permission again",
        "Run all scenarios inline in the one fresh task.",
        "temporary files",
        "invalidates the entire run",
    ):
        assert required in live_acceptance, f"Missing read-only acceptance rule: {required}"

    assert not (ROOT / "skills" / "brand-voice-copywriter" / "SKILL.md").exists()
    assert not (ROOT / "tests" / "openai-directory-submission.json").exists()
    assert not (ROOT / "tests" / "receipts" / "chatgpt-work-v2.1.0.json").exists()
    packaged = {path.relative_to(ROOT).as_posix() for path in copied_files()}
    assert not any(
        name == ".git" or name.startswith((".git/", ".install/", "dist/", "qa/", "tmp/"))
        for name in packaged
    )
    windows_installer = (ROOT / "install.ps1").read_text(encoding="utf-8")
    posix_installer = (ROOT / "install.sh").read_text(encoding="utf-8")
    for installer in (windows_installer, posix_installer):
        assert "stage_install.py" in installer
        assert "codex-chief-of-staff" in installer
    validator = (ROOT / "scripts" / "validate_repository.py").read_text(encoding="utf-8")
    assert '".install/"' in validator
    assert 'marketplace", "add", $RepoRoot' not in windows_installer
    assert 'marketplace add "$REPO_ROOT"' not in posix_installer
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
    assert release_status == "pass"
    assert not validate_model_acceptance()
    assert not validate_model_acceptance(require_pass=True)

    pending = copy.deepcopy(evidence)
    pending["models"]["gpt-5.6-sol"]["status"] = "pending"
    assert model_acceptance_release_status(pending) == "candidate"

    failed = copy.deepcopy(evidence)
    failed["models"]["gpt-5.6-sol"]["status"] = "fail"
    failed["models"]["gpt-5.6-sol"]["evidence"] = "Observed failure fixture."
    assert model_acceptance_release_status(failed) == "candidate"

    print(
        "PASS: plan-scoped delivery rules and the Sol-only release gate are present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
