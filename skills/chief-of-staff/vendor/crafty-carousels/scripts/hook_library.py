from __future__ import annotations

import argparse
import json
from pathlib import Path


LIBRARY_DIR = Path(__file__).resolve().parent.parent / "assets" / "hook-library"
CONTENT_CLASSES = ("business", "ugc_creator", "influencer")
FORMATS = ("video", "image_carousel")


def load_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(LIBRARY_DIR.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        source_records = payload.get("records", [])
        if not isinstance(source_records, list):
            raise ValueError(f"Hook records must be a list: {path.name}")
        records.extend(source_records)

    ids = [str(record.get("id", "")) for record in records]
    if len(records) != 751:
        raise ValueError(f"Hook library must contain 751 source records; found {len(records)}")
    if any(not record_id for record_id in ids) or len(set(ids)) != len(ids):
        raise ValueError("Hook library IDs must be present and unique")
    for record in records:
        if not record.get("hook"):
            raise ValueError(f"Hook text is required: {record.get('id')}")
        classes = record.get("content_classes", [record.get("content_class")])
        formats = record.get("format_fit", [])
        if not set(classes).issubset(CONTENT_CLASSES) or not classes:
            raise ValueError(f"Invalid content classes: {record.get('id')}")
        if not set(formats).issubset(FORMATS) or not formats:
            raise ValueError(f"Invalid format fit: {record.get('id')}")
    return records


def query(content_class: str, content_format: str, search: str, count: int) -> list[dict[str, object]]:
    needle = search.casefold().strip()
    records = [
        record
        for record in load_records()
        if content_class in record.get("content_classes", [record.get("content_class")])
        and content_format in record.get("format_fit", [])
        and not record.get("duplicate_of")
    ]
    if needle:
        records = [
            record
            for record in records
            if needle in str(record["hook"]).casefold()
            or needle in str(record.get("example") or "").casefold()
            or needle in str(record.get("source_category") or "").casefold()
            or needle in str(record.get("hook_mechanism") or "").casefold()
        ]
    return records[:count]


def main() -> int:
    parser = argparse.ArgumentParser(description="Query Crafty Carousels hooks by client class and format fit.")
    parser.add_argument("--content-class", choices=CONTENT_CLASSES)
    parser.add_argument("--format", choices=FORMATS, default="image_carousel")
    parser.add_argument("--search", default="")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        all_records = load_records()
        assert len(all_records) == 751
        assert all(query(name, content_format, "", 751) for name in CONTENT_CLASSES for content_format in FORMATS)
        assert all(record["hook"] for record in all_records)
        print("self_test=PASS records=751")
        return 0
    if not args.content_class:
        parser.error("--content-class is required")
    if args.count < 1 or args.count > 751:
        parser.error("--count must be between 1 and 751")
    records = query(args.content_class, args.format, args.search, args.count)
    if args.json:
        print(json.dumps(records, indent=2, ensure_ascii=False))
        return 0
    if not records:
        print("No matching hooks.")
        return 0
    for record in records:
        print(f"{record['id']} [{record.get('recommended_format', 'UNKNOWN')}]\nHOOK: {record['hook']}")
        if record.get("example"):
            print(f"EXAMPLE: {record['example']}")
        else:
            print("EXAMPLE: Not supplied by source; fill only with approved client facts.")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
