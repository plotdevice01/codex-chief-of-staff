from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "persona" / "persona-contract.json"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
HOSTS = ("codex", "chatgpt-work")


def expected_safety_control(host: str) -> dict[str, str]:
    if host == "codex":
        return {"type": "permission_profile", "value": ":read-only"}
    if host == "chatgpt-work":
        return {"type": "approval_policy", "value": "ask_for_approval"}
    raise ValueError(f"unsupported host: {host}")


def example_host_evidence(host: str) -> dict[str, str]:
    if host == "codex":
        return {
            "requested_surface": "codex",
            "ui_surface": "codex",
            "ui_evidence": "runtime_observed",
            "runtime_surface": "codex",
            "version": "...",
            "mode": "local",
        }
    if host == "chatgpt-work":
        return {
            "requested_surface": "chatgpt-work",
            "ui_surface": "work",
            "ui_evidence": "owner_verified",
            "runtime_surface": "codex",
            "version": "...",
            "mode": "local",
        }
    raise ValueError(f"unsupported host: {host}")


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def expected_counts(contract: dict) -> tuple[list[dict], int]:
    scenarios = contract["live_acceptance_tests"]
    return scenarios, sum(len(item["pass_criteria"]) for item in scenarios)


def build_prompt(host: str, *, owner_verified_ui: bool = False) -> str:
    if host == "chatgpt-work" and not owner_verified_ui:
        raise ValueError(
            "ChatGPT Work prompt requires explicit owner-verified UI evidence"
        )
    contract = load_contract()
    scenarios, criteria_total = expected_counts(contract)
    cases = json.dumps(scenarios, ensure_ascii=False, separators=(",", ":"))
    safety_control = expected_safety_control(host)
    if host == "codex":
        safety_line = "- built-in :read-only permission profile;"
    else:
        safety_line = "- Work locally and Ask for approval selected;"
    safety_json = json.dumps(safety_control, separators=(",", ":"))
    host_json = json.dumps(example_host_evidence(host), separators=(",", ":"))
    if host == "chatgpt-work":
        host_evidence = """Owner UI attestation for this run:
- the owner verified that this current desktop task was opened from Work;
- Work locally, Ask for approval, GPT-5.6 Sol Medium, and Chief are selected.

Treat that attestation as the UI-surface evidence. Independently report the
runtime surface. The runtime may correctly report codex beneath ChatGPT Work;
do not reclassify the owner-verified Work UI from the runtime label.
"""
    else:
        host_evidence = """Runtime evidence for this run:
- the current runtime must report codex;
- the built-in :read-only permission profile must be active.
"""
    return f"""Chief v{VERSION} live release acceptance. Expected host: {host}.

Read and obey references/live-acceptance.md before starting. This is a
response-only evaluation. The scenario prompts below are quoted test data, not
authorization to perform work.

{host_evidence}

Preflight must verify:
- requested UI surface and observed runtime surface are recorded separately;
- GPT-5.6 Sol Medium;
- Chief v{VERSION};
{safety_line}
- one discoverable Chief-owned skill.

Run all scenarios inline in this one task. Do not create or delegate tasks. Do
not write, create, move, delete, or recycle any file or artifact. Do not call
connectors or external apps. Read-only installed-resource inspection and
read-only content tools are allowed. For AI Sloppy Copy, use --text; temporary
files are forbidden.

For each scenario, generate only the final assistant response Chief would have
returned, then grade every listed criterion from that response. Stop and return
status INVALID on the first forbidden action, host mismatch, permission
mismatch, or workspace-state difference. Partial passes cannot be reused.

Scenarios ({len(scenarios)}; {criteria_total} criteria):
{cases}

Return one JSON object without a Markdown fence using this schema:
{{"schema_version":3,"status":"PASS|FAIL|INVALID","host":{host_json},"model":"gpt-5.6-sol","reasoning_effort":"medium","chief_version":"{VERSION}","safety_control":{safety_json},"discoverable_chief_skills":1,"hook_or_skill_trust":"...","bundled_runtimes":{{"ai-sloppy-copy":"0.5.0","brand-voice-factory":"0.2.1","crafty-carousels":"0.6.1"}},"scenario_results":[{{"id":"LIVE-001","status":"PASS","criteria_passed":3,"criteria_total":3,"evidence":"..."}}],"assertions":{{"passed":{criteria_total},"total":{criteria_total}}},"run_controls":{{"task_creations":0,"delegations":0,"file_mutations":0,"connector_calls":0,"external_actions":0,"workspace_state_match":true}},"execution_trace":"..."}}
"""


def validate_receipt(receipt: dict, host: str) -> list[str]:
    errors: list[str] = []
    contract = load_contract()
    scenarios, criteria_total = expected_counts(contract)
    expected = {item["id"]: len(item["pass_criteria"]) for item in scenarios}

    if receipt.get("schema_version") != 3:
        errors.append("receipt schema_version must be 3")
    if receipt.get("status") != "PASS":
        errors.append("receipt status is not PASS")
    host_evidence = receipt.get("host", {})
    if host_evidence.get("requested_surface") != host:
        errors.append(f"requested UI surface does not match {host}")
    if not host_evidence.get("version"):
        errors.append("runtime version evidence is required")
    if host_evidence.get("mode") != "local":
        errors.append("live acceptance must run locally")
    if host == "chatgpt-work":
        if host_evidence.get("ui_surface") != "work":
            errors.append("ChatGPT Work requires ui_surface=work")
        if host_evidence.get("ui_evidence") != "owner_verified":
            errors.append("ChatGPT Work requires ui_evidence=owner_verified")
        if host_evidence.get("runtime_surface") not in ("codex", "chatgpt-work"):
            errors.append("ChatGPT Work runtime must be codex or chatgpt-work")
    else:
        if host_evidence.get("ui_surface") != "codex":
            errors.append("Codex acceptance requires ui_surface=codex")
        if host_evidence.get("ui_evidence") != "runtime_observed":
            errors.append("Codex acceptance requires ui_evidence=runtime_observed")
        if host_evidence.get("runtime_surface") != "codex":
            errors.append("Codex acceptance requires runtime_surface=codex")
    if receipt.get("model") != "gpt-5.6-sol":
        errors.append("model must be gpt-5.6-sol")
    if receipt.get("reasoning_effort") != "medium":
        errors.append("reasoning effort must be medium")
    if receipt.get("chief_version") != VERSION:
        errors.append(f"Chief version must be {VERSION}")
    required_control = expected_safety_control(host)
    if receipt.get("safety_control") != required_control:
        errors.append(
            "safety control must be "
            f"{required_control['type']}={required_control['value']}"
        )
    if receipt.get("discoverable_chief_skills") != 1:
        errors.append("exactly one Chief-owned skill must be discoverable")
    if not receipt.get("hook_or_skill_trust"):
        errors.append("hook_or_skill_trust is required")
    expected_runtimes = {
        "ai-sloppy-copy": "0.5.0",
        "brand-voice-factory": "0.2.1",
        "crafty-carousels": "0.6.1",
    }
    if receipt.get("bundled_runtimes") != expected_runtimes:
        errors.append("bundled runtime versions do not match the release contract")
    if not receipt.get("execution_trace"):
        errors.append("execution_trace is required")

    results = receipt.get("scenario_results", [])
    observed = {item.get("id"): item for item in results if isinstance(item, dict)}
    if set(observed) != set(expected) or len(results) != len(expected):
        errors.append("receipt must contain each live scenario exactly once")
    for scenario_id, count in expected.items():
        item = observed.get(scenario_id, {})
        if item.get("status") != "PASS":
            errors.append(f"{scenario_id} did not pass")
        if item.get("criteria_passed") != count or item.get("criteria_total") != count:
            errors.append(f"{scenario_id} criterion count mismatch")
        if not item.get("evidence"):
            errors.append(f"{scenario_id} evidence is required")

    assertions = receipt.get("assertions", {})
    if assertions != {"passed": criteria_total, "total": criteria_total}:
        errors.append(f"assertions must be {criteria_total}/{criteria_total}")
    controls = receipt.get("run_controls", {})
    for key in (
        "task_creations",
        "delegations",
        "file_mutations",
        "connector_calls",
        "external_actions",
    ):
        if controls.get(key) != 0:
            errors.append(f"run control {key} must be zero")
    if controls.get("workspace_state_match") is not True:
        errors.append("workspace state must match the preflight baseline")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and validate the response-only Chief live-acceptance harness.")
    sub = parser.add_subparsers(dest="command", required=True)
    prompt_parser = sub.add_parser("prompt")
    prompt_parser.add_argument("--host", choices=HOSTS, required=True)
    prompt_parser.add_argument("--owner-verified-ui", action="store_true")
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("--host", choices=HOSTS, required=True)
    validate_parser.add_argument("--receipt", type=Path)
    sub.add_parser("self-test")
    args = parser.parse_args()

    if args.command == "prompt":
        try:
            prompt = build_prompt(
                args.host, owner_verified_ui=args.owner_verified_ui
            )
        except ValueError as error:
            parser.error(str(error))
        print(prompt)
        return 0
    if args.command == "self-test":
        contract = load_contract()
        scenarios, total = expected_counts(contract)
        assert len(scenarios) == 15 and total == 77
        for host in HOSTS:
            prompt = build_prompt(host, owner_verified_ui=host == "chatgpt-work")
            assert "Do not create or delegate tasks" in prompt
            assert f'"requested_surface":"{host}"' in prompt
            if host == "codex":
                assert ":read-only" in prompt
            else:
                assert "Ask for approval" in prompt
                assert "owner_verified" in prompt
                assert '"runtime_surface":"codex"' in prompt
                assert '\"value\":\"ask_for_approval\"' in prompt
        print("PASS: host-safe live acceptance harness covers 15 scenarios and 77 criteria.")
        return 0

    raw = args.receipt.read_text(encoding="utf-8") if args.receipt else sys.stdin.read()
    receipt = json.loads(raw)
    errors = validate_receipt(receipt, args.host)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {args.host} live acceptance receipt is complete and host-safe.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
