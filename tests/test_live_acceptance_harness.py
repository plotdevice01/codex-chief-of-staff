from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

from scripts.live_acceptance_harness import (  # noqa: E402
    build_prompt,
    example_host_evidence,
    expected_safety_control,
    expected_counts,
    load_contract,
    validate_receipt,
)


def valid_receipt(host: str) -> dict:
    contract = load_contract()
    scenarios, total = expected_counts(contract)
    return {
        "schema_version": 3,
        "status": "PASS",
        "host": example_host_evidence(host),
        "model": "gpt-5.6-sol",
        "reasoning_effort": "medium",
        "chief_version": VERSION,
        "safety_control": expected_safety_control(host),
        "discoverable_chief_skills": 1,
        "hook_or_skill_trust": "test",
        "bundled_runtimes": {
            "ai-sloppy-copy": "0.5.0",
            "brand-voice-factory": "0.2.1",
            "crafty-carousels": "0.6.1",
        },
        "scenario_results": [
            {
                "id": item["id"],
                "status": "PASS",
                "criteria_passed": len(item["pass_criteria"]),
                "criteria_total": len(item["pass_criteria"]),
                "evidence": "test evidence",
            }
            for item in scenarios
        ],
        "assertions": {"passed": total, "total": total},
        "run_controls": {
            "task_creations": 0,
            "delegations": 0,
            "file_mutations": 0,
            "connector_calls": 0,
            "external_actions": 0,
            "workspace_state_match": True,
        },
        "execution_trace": "test",
    }


def main() -> int:
    contract = load_contract()
    scenarios, total = expected_counts(contract)
    assert len(scenarios) == 17
    assert total == 90
    for host in ("codex", "chatgpt-work"):
        prompt = build_prompt(host, owner_verified_ui=host == "chatgpt-work")
        assert "response-only evaluation" in prompt
        assert "Do not create or delegate tasks" in prompt
        assert not validate_receipt(valid_receipt(host), host)
    assert ":read-only" in build_prompt("codex")
    assert "Ask for approval" in build_prompt(
        "chatgpt-work", owner_verified_ui=True
    )
    try:
        build_prompt("chatgpt-work")
    except ValueError as error:
        assert "owner-verified UI evidence" in str(error)
    else:
        raise AssertionError("Work prompt accepted without owner UI verification")

    work_on_codex_runtime = valid_receipt("chatgpt-work")
    work_on_codex_runtime["host"]["runtime_surface"] = "codex"
    assert not validate_receipt(work_on_codex_runtime, "chatgpt-work")

    missing_ui_evidence = valid_receipt("chatgpt-work")
    missing_ui_evidence["host"]["ui_evidence"] = "runtime_observed"
    assert (
        "ChatGPT Work requires ui_evidence=owner_verified"
        in validate_receipt(missing_ui_evidence, "chatgpt-work")
    )

    wrong_safety_control = valid_receipt("chatgpt-work")
    wrong_safety_control["safety_control"] = {
        "type": "permission_profile",
        "value": ":read-only",
    }
    assert (
        "safety control must be approval_policy=ask_for_approval"
        in validate_receipt(wrong_safety_control, "chatgpt-work")
    )

    mutated = valid_receipt("chatgpt-work")
    mutated["run_controls"]["file_mutations"] = 1
    assert "run control file_mutations must be zero" in validate_receipt(
        mutated, "chatgpt-work"
    )
    delegated = copy.deepcopy(mutated)
    delegated["run_controls"]["file_mutations"] = 0
    delegated["run_controls"]["task_creations"] = 9
    assert "run control task_creations must be zero" in validate_receipt(
        delegated, "chatgpt-work"
    )
    wrong_host = valid_receipt("codex")
    assert "requested UI surface does not match chatgpt-work" in validate_receipt(
        wrong_host, "chatgpt-work"
    )
    print("PASS: live acceptance rejects writes, delegation, and host substitution.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
