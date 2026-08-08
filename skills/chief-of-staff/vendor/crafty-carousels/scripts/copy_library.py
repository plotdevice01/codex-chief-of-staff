from __future__ import annotations

import argparse
import json
from pathlib import Path


LIBRARY = Path(__file__).resolve().parent.parent / "assets" / "copy-library" / "scripts-7-ctas-39.json"


def load_library() -> dict[str, object]:
    payload = json.loads(LIBRARY.read_text(encoding="utf-8"))
    if len(payload.get("scripts", [])) != 7 or len(payload.get("ctas", [])) != 39:
        raise ValueError("Copy library must contain 7 scripts and 39 CTAs")
    return payload


def search(kind: str, category: str, needle: str) -> list[dict[str, object]]:
    payload = load_library()
    records = payload["scripts" if kind == "script" else "ctas"]
    query = needle.casefold().strip()
    matches = []
    for record in records:
        if kind == "cta" and category and record.get("category") != category:
            continue
        searchable = json.dumps(record, ensure_ascii=False).casefold()
        if query and query not in searchable:
            continue
        matches.append(record)
    return matches


def main() -> int:
    parser = argparse.ArgumentParser(description="Query the offline Crafty Carousels script and CTA library.")
    parser.add_argument("--type", choices=("script", "cta"))
    parser.add_argument("--category", choices=("engagement", "follow", "sales"), default="")
    parser.add_argument("--search", default="")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        payload = load_library()
        assert all(script["fields"] for script in payload["scripts"])
        assert all(search("cta", category, "") for category in ("engagement", "follow", "sales"))
        print("self_test=PASS scripts=7 ctas=39")
        return 0
    if not args.type:
        parser.error("--type is required")
    if args.count < 1 or args.count > 39:
        parser.error("--count must be between 1 and 39")
    if args.type == "script" and args.category:
        parser.error("--category applies only to CTA queries")
    records = search(args.type, args.category, args.search)[: args.count]
    if args.json:
        print(json.dumps(records, indent=2, ensure_ascii=False))
        return 0
    for record in records:
        if args.type == "script":
            print(f"{record['id']} - {record['name']}")
            for field in record["fields"]:
                print(f"  {field['name']}: {field['instruction']}")
        else:
            print(f"{record['id']} [{record['category']}] {record['cta']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
