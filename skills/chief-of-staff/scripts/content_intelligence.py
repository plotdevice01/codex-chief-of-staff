from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
CRAFTY = SKILL_ROOT / "vendor" / "crafty-carousels"
HOOKS = CRAFTY / "assets" / "hook-library"
COPY = CRAFTY / "assets" / "copy-library" / "scripts-7-ctas-39.json"
CONTENT_CLASSES = ("business", "ugc_creator", "influencer")
FORMATS = ("video", "image_carousel")
CTA_CATEGORIES = ("engagement", "follow", "sales")
OFFER_TYPES = ("paid", "free", "lead_magnet", "engagement", "follow", "unknown")
CLAIM_RISK_TERMS = {
    "double",
    "desired",
    "outcome",
    "pain",
    "problem",
    "wrong",
    "hack",
    "result",
    "secret",
    "mistake",
    "losing",
    "zero",
    "money",
    "scary",
    "issues",
    "grow",
    "guarantee",
    "promise",
    "proof",
    "easiest",
    "explode",
    "exploded",
    "shocking",
    "changer",
    "lucky",
    "blow",
    "important",
    "taught",
    "started",
    "absolutely",
    "change",
    "budget",
    "strategy",
    "number",
    "tricks",
    "time",
    "success",
    "viral",
}


def terms(value: str) -> set[str]:
    return {term for term in re.findall(r"[a-z0-9]+", value.casefold()) if len(term) > 2}


def score(record: dict[str, object], query_terms: set[str]) -> tuple[int, str]:
    if "hook" in record:
        hook = str(record.get("hook", "")).casefold()
        example = str(record.get("example", "")).casefold()
        overlap = 3 * len(terms(hook) & query_terms)
        overlap += len(terms(example) & query_terms)
        unsupported = (terms(f"{hook} {example}") & CLAIM_RISK_TERMS) - query_terms
        return overlap - (5 * len(unsupported)), str(record.get("id", ""))
    searchable = terms(json.dumps(record, ensure_ascii=False))
    # Deterministic lexical ranking keeps retrieval inspectable and inexpensive.
    return len(searchable & query_terms), str(record.get("id", ""))


def cta_compatibility(record: dict[str, object], offer_type: str) -> tuple[bool, str]:
    cta = str(record.get("cta", "")).casefold()
    if offer_type == "paid" and ("free" in cta or "download" in cta):
        return False, "free-download CTA conflicts with a paid offer"
    return True, "compatible"


def load_hooks() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(HOOKS.glob("*.json")):
        records.extend(json.loads(path.read_text(encoding="utf-8"))["records"])
    if len(records) != 751 or len({record["id"] for record in records}) != 751:
        raise ValueError("Chief requires the complete 751-record Crafty hook library")
    return records


def load_copy() -> dict[str, list[dict[str, object]]]:
    payload = json.loads(COPY.read_text(encoding="utf-8"))
    if len(payload.get("scripts", [])) != 7 or len(payload.get("ctas", [])) != 39:
        raise ValueError("Chief requires all 7 scripts and 39 CTAs")
    return payload


def recommend(
    content_class: str,
    content_format: str,
    query: str,
    cta_category: str,
    cta_text: str,
    offer_type: str,
    hook_count: int,
    script_count: int,
    cta_count: int,
) -> dict[str, object]:
    query_terms = terms(query)
    hooks = [
        record
        for record in load_hooks()
        if content_class in record.get("content_classes", [record.get("content_class")])
        and content_format in record.get("format_fit", [])
        and not record.get("duplicate_of")
    ]
    library = load_copy()
    scripts = library["scripts"]
    category_ctas = [record for record in library["ctas"] if record.get("category") == cta_category]
    rejected_ctas: list[dict[str, str]] = []
    ctas: list[dict[str, object]] = []
    for record in category_ctas:
        compatible, reason = cta_compatibility(record, offer_type)
        if compatible:
            ctas.append(record)
        else:
            rejected_ctas.append({"id": str(record.get("id", "")), "reason": reason})
    if not ctas:
        raise ValueError(f"no {cta_category} CTA is compatible with offer type {offer_type}")

    def ranked(
        records: list[dict[str, object]],
        count: int,
        ranking_terms: set[str],
        preferred_id: str = "",
    ) -> list[dict[str, object]]:
        if ranking_terms or preferred_id:
            records = sorted(
                records,
                key=lambda record: (
                    str(record.get("id", "")) != preferred_id,
                    -score(record, ranking_terms)[0],
                    score(record, ranking_terms)[1],
                ),
            )
        return records[:count]

    ranked_hooks = ranked(hooks, hook_count, query_terms)
    ranked_scripts = ranked(
        scripts,
        script_count,
        query_terms,
        "pbl-script-07" if cta_category == "sales" else "",
    )
    ranked_ctas = ranked(ctas, cta_count, query_terms | terms(cta_text))

    return {
        "query": query,
        "content_class": content_class,
        "format": content_format,
        "offer_type": offer_type,
        "requested_cta": cta_text,
        "searched": {"hooks": 751, "scripts": 7, "ctas": 39},
        "compatibility": {"rejected_ctas": rejected_ctas},
        "recommended": {
            "hook": ranked_hooks[0]["id"],
            "script": ranked_scripts[0]["id"],
            "cta": ranked_ctas[0]["id"],
        },
        "hooks": ranked_hooks,
        "scripts": ranked_scripts,
        "ctas": ranked_ctas,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Chief's complete pinned content library once.")
    parser.add_argument("--content-class", choices=CONTENT_CLASSES)
    parser.add_argument("--format", choices=FORMATS, default="video")
    parser.add_argument("--query", default="")
    parser.add_argument("--cta-category", choices=CTA_CATEGORIES, default="sales")
    parser.add_argument("--cta-text", default="")
    parser.add_argument("--offer-type", choices=OFFER_TYPES, default="unknown")
    parser.add_argument("--hooks", type=int, default=5)
    parser.add_argument("--scripts", type=int, default=3)
    parser.add_argument("--ctas", type=int, default=5)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = recommend(
            "business", "video", "problem proof action", "sales", "book a call", "paid", 5, 3, 5
        )
        assert result["searched"] == {"hooks": 751, "scripts": 7, "ctas": 39}
        assert len(result["hooks"]) == 5 and len(result["scripts"]) == 3 and len(result["ctas"]) == 5
        print("self_test=PASS hooks=751 scripts=7 ctas=39")
        return 0
    if not args.content_class:
        parser.error("--content-class is required")
    for name, value, maximum in (
        ("--hooks", args.hooks, 20),
        ("--scripts", args.scripts, 7),
        ("--ctas", args.ctas, 13),
    ):
        if value < 1 or value > maximum:
            parser.error(f"{name} must be between 1 and {maximum}")
    print(
        json.dumps(
            recommend(
                args.content_class,
                args.format,
                args.query,
                args.cta_category,
                args.cta_text,
                args.offer_type,
                args.hooks,
                args.scripts,
                args.ctas,
            ),
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
