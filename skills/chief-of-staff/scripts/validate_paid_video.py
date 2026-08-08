from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from content_intelligence import cta_compatibility


REQUIRED_SEARCH = {"hooks": 751, "scripts": 7, "ctas": 39}
PERFORMANCE_TERMS = re.compile(r"\b(high[- ]converting|winning|viral)\b", re.IGNORECASE)


def validate(packet: dict[str, object]) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        failures.append({"code": code, "message": message})

    listed = {str(value) for value in packet.get("sources_listed", [])}
    opened = {str(value) for value in packet.get("sources_opened", [])}
    if listed - opened:
        fail("PV-SOURCE-001", "Every listed source must be opened.")
    if packet.get("voice_required") and not packet.get("voice_manifest_loaded"):
        fail("PV-VOICE-001", "The required approved voice manifest was not loaded.")
    if packet.get("content_query") != REQUIRED_SEARCH:
        fail("PV-LIBRARY-001", "The complete 751-hook, 7-script, and 39-CTA query did not run.")

    offer_type = str(packet.get("offer_type", "unknown"))
    selected_cta = str(packet.get("selected_cta", ""))
    compatible, reason = cta_compatibility({"cta": selected_cta}, offer_type)
    if not selected_cta or not compatible:
        fail("PV-OFFER-001", reason if selected_cta else "A selected CTA is required.")

    concepts = packet.get("concepts", [])
    if not isinstance(concepts, list) or not 3 <= len(concepts) <= 5:
        fail("PV-CONCEPT-001", "A concept batch must contain three to five concepts.")
        concepts = concepts if isinstance(concepts, list) else []

    signatures: dict[str, str] = {}
    performance_text: list[str] = []
    for index, concept in enumerate(concepts):
        if not isinstance(concept, dict):
            fail("PV-CONCEPT-002", f"Concept {index + 1} must be an object.")
            continue
        concept_id = str(concept.get("id", index + 1))
        if not str(concept.get("first_frame_action", "")).strip():
            fail("PV-VISUAL-001", f"Concept {concept_id} lacks first-frame action.")
        progression = concept.get("visual_progression", [])
        if not isinstance(progression, list) or len(progression) < 2:
            fail("PV-VISUAL-002", f"Concept {concept_id} lacks visual progression.")
        if not str(concept.get("proof_source", "")).strip():
            fail("PV-PROOF-001", f"Concept {concept_id} has proof without a source.")
        signature_fields = (
            "format",
            "mechanism",
            "proof_source",
            "offer",
            "cta",
            "first_frame_action",
            "visual_progression",
        )
        signature = json.dumps(
            {field: concept.get(field) for field in signature_fields},
            sort_keys=True,
            ensure_ascii=False,
        )
        if signature in signatures:
            fail(
                "PV-VARIATION-001",
                f"Concept {concept_id} differs from {signatures[signature]} only cosmetically.",
            )
        else:
            signatures[signature] = concept_id
        performance_text.append(json.dumps(concept, ensure_ascii=False))

    if PERFORMANCE_TERMS.search(" ".join(performance_text)) and not packet.get(
        "performance_evidence"
    ):
        fail("PV-PERFORMANCE-001", "Performance language requires measured evidence.")
    if packet.get("regulated") and packet.get("disclosure_status") not in {
        "approved",
        "not_required",
    }:
        fail("PV-DISCLOSURE-001", "Regulated disclosure treatment lacks approval status.")

    receipt = packet.get("receipt", {})
    receipt_files = receipt.get("files_used", []) if isinstance(receipt, dict) else []
    if sorted(str(value) for value in receipt_files) != sorted(
        str(value) for value in packet.get("files_used", [])
    ):
        fail("PV-RECEIPT-001", "The execution receipt conflicts with files actually used.")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one generic paid-video packet.")
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.packet.read_text(encoding="utf-8-sig"))
    failures = validate(payload)
    print(json.dumps({"status": "FAIL" if failures else "PASS", "failures": failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
