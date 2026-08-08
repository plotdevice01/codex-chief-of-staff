from __future__ import annotations

import argparse
import json
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = SKILL_ROOT / "references" / "capability-registry.json"


def load_registry() -> dict[str, object]:
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if payload.get("discoverable_skill") != "chief-of-staff":
        raise ValueError("capability registry must expose only chief-of-staff")
    return payload


def route(request: str) -> dict[str, object]:
    payload = load_registry()
    normalized = " ".join(request.casefold().split())
    selected: dict[str, object] | None = None
    matched: list[str] = []
    for capability in payload["capabilities"]:
        triggers = [str(value) for value in capability.get("triggers", [])]
        hits = [trigger for trigger in triggers if trigger in normalized]
        if hits:
            selected = capability
            matched = hits
            break
    if selected is None:
        selected = next(
            capability
            for capability in payload["capabilities"]
            if capability["id"] == payload["fallback"]
        )
    contracts = ["references/universal-request-contract.md"]
    contracts.extend(str(path) for path in selected.get("contracts", []))
    return {
        "discoverable_skill": "chief-of-staff",
        "primary_capability": selected["id"],
        "matched_triggers": matched,
        "internal_contracts": contracts,
        "specialist_selection_required": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Route one request through Chief once.")
    parser.add_argument("request", nargs="?", default="")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        assert route("Write three paid video ad scripts")["primary_capability"] == "paid_video"
        assert route("Create a carousel")["primary_capability"] == "carousel"
        assert route("Help me think through this decision")["primary_capability"] == "generic"
        print("self_test=PASS discoverable_skill=chief-of-staff")
        return 0
    if not args.request.strip():
        parser.error("request is required")
    print(json.dumps(route(args.request), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
