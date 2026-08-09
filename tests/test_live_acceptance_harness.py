from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

from scripts.live_acceptance_harness import (  # noqa: E402
    build_embedded_sources,
    build_prompt,
    example_host_evidence,
    expected_safety_controls,
    expected_counts,
    load_contract,
    validate_receipt,
)


def valid_receipt(host: str) -> dict:
    contract = load_contract()
    scenarios, total = expected_counts(contract)
    return {
        "schema_version": 5,
        "status": "PASS",
        "host": example_host_evidence(host),
        "model": "gpt-5.6-sol",
        "reasoning_effort": "medium",
        "chief_version": VERSION,
        "evidence_mode": "embedded_preflight",
        "safety_controls": expected_safety_controls(host),
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
            "tool_calls": 0,
            "task_creations": 0,
            "delegations": 0,
            "write_attempts": 0,
            "approval_requests": 0,
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
    embedded_sources = build_embedded_sources(ROOT)
    for host in ("codex", "chatgpt-work"):
        prompt = build_prompt(
            host,
            owner_verified_ui=host == "chatgpt-work",
            embedded_sources=embedded_sources,
            runtime_version="test",
        )
        assert "response-only evaluation" in prompt
        assert "Do not create or delegate tasks" in prompt
        assert "Do not call any tool" in prompt
        assert '"hooks":751,"scripts":7,"ctas":39' in prompt
        assert '"business-077"' in prompt
        assert '"pbl-script-04"' in prompt
        assert '"pbl-cta-sales-13"' in prompt
        assert '"status":"pass","output":"PASS:' in prompt
        for item in scenarios:
            count = len(item["pass_criteria"])
            exact_result = (
                f'"id":"{item["id"]}","status":"PASS",'
                f'"criteria_passed":{count},"criteria_total":{count}'
            )
            assert exact_result in prompt
        assert not validate_receipt(valid_receipt(host), host)
    codex_prompt = build_prompt(
        "codex", embedded_sources=embedded_sources, runtime_version="test"
    ).replace("\n", " ")
    assert (
        "codex --ask-for-approval never exec --ephemeral --sandbox read-only"
        in codex_prompt
    )
    assert "Ask for approval" in build_prompt(
        "chatgpt-work",
        owner_verified_ui=True,
        embedded_sources=embedded_sources,
        runtime_version="test",
    )
    try:
        build_prompt(
            "chatgpt-work",
            embedded_sources=embedded_sources,
            runtime_version="test",
        )
    except ValueError as error:
        assert "owner-verified UI evidence" in str(error)
    else:
        raise AssertionError("Work prompt accepted without owner UI verification")

    try:
        build_prompt("codex", runtime_version="test")
    except ValueError as error:
        assert "embedded installed sources" in str(error)
    else:
        raise AssertionError("Codex prompt accepted without embedded evidence")

    try:
        build_prompt("codex", embedded_sources=embedded_sources)
    except ValueError as error:
        assert "observed runtime version" in str(error)
    else:
        raise AssertionError("Codex prompt accepted without runtime version")

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
    wrong_safety_control["safety_controls"] = {
        "sandbox_mode": "read-only",
        "approval_policy": "never",
        "session_persistence": "ephemeral",
    }
    assert any(
        "safety controls must be" in error
        for error in validate_receipt(wrong_safety_control, "chatgpt-work")
    )

    desktop_substitution = valid_receipt("codex")
    desktop_substitution["host"]["ui_surface"] = "codex"
    assert "Codex acceptance requires ui_surface=codex-cli" in validate_receipt(
        desktop_substitution, "codex"
    )

    write_attempt = valid_receipt("codex")
    write_attempt["run_controls"]["write_attempts"] = 1
    assert "run control write_attempts must be zero" in validate_receipt(
        write_attempt, "codex"
    )

    tool_call = valid_receipt("codex")
    tool_call["run_controls"]["tool_calls"] = 1
    assert "run control tool_calls must be zero" in validate_receipt(
        tool_call, "codex"
    )

    placeholder_evidence = valid_receipt("codex")
    placeholder_evidence["scenario_results"][0]["evidence"] = (
        "Generate scenario-specific evidence from the graded response."
    )
    assert "LIVE-001 evidence is required" in validate_receipt(
        placeholder_evidence, "codex"
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
