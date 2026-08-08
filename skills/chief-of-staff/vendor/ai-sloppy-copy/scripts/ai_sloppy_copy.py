#!/usr/bin/env python3
"""Shared AI Sloppy Copy checker. Uses only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree


FAMILY_SUFFIXES = (
    "s|es|d|ed|ing|er|ers|est|ity|ities|ful|fully|less|lessly|ly|ness|"
    "nesses|ment|ments|tion|tions|al|ally|ive|ives|ively|able|ably|"
    "ability|abilities"
)
SEPARATOR = r"[\s\-\u2010-\u2015]+"
SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".html", ".htm", ".xml"}


def load_rules(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        try:
            data = archive.read("word/document.xml")
        except KeyError as exc:
            raise ValueError(f"DOCX has no word/document.xml: {path}") from exc
    root = ElementTree.fromstring(data)
    paragraphs = []
    for paragraph in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        paragraphs.append(
            "".join(
                node.text or ""
                for node in paragraph.iter(
                    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"
                )
            )
        )
    return "\n".join(paragraphs)


def read_input(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return read_docx(path)
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type '{suffix}': {path}")
    return path.read_text(encoding="utf-8")


def mask_protected_markdown(text: str) -> str:
    """Mask explicit protected spans while preserving offsets and line numbers."""
    patterns = (
        r"(?s)```.*?```",
        r"(?s)~~~.*?~~~",
        r"`[^`\r\n]+`",
        r"(?m)^\s*>[^\r\n]*(?:\r?\n|$)",
        r"https?://[^\s<>()]+",
        r"(?i)\b[A-Z]:\\(?:[^<>:\"/\\|?*\r\n]+\\)*[^<>:\"/\\|?*\r\n]*",
    )
    masked = list(text)
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            for index in range(match.start(), match.end()):
                if masked[index] not in "\r\n":
                    masked[index] = " "
    return "".join(masked)


def mask_markup_tags(text: str) -> str:
    """Mask HTML/XML structure while leaving visible prose available to scan."""
    patterns = (
        r"(?s)<!--.*?-->",
        r"(?s)<\?.*?\?>",
        r"(?s)</?[A-Za-z][^<>]*?>",
    )
    masked = list(text)
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            for index in range(match.start(), match.end()):
                if masked[index] not in "\r\n":
                    masked[index] = " "
    return "".join(masked)


def family_body(word: str) -> str:
    escaped = re.escape(word)
    forms = [escaped, rf"{escaped}(?:{FAMILY_SUFFIXES})"]
    if len(word) > 2 and word.lower().endswith("e"):
        stem = re.escape(word[:-1])
        forms.append(rf"{stem}(?:ing|ed|er|ers|est|ly|able|ably|ability|abilities|ive|ively)")
    if len(word) > 2 and word.lower().endswith("y"):
        stem = re.escape(word[:-1])
        forms.append(rf"{stem}(?:ies|ied|ying|ier|iest)")
    if re.search(r"(?i)[aeiou][bcdfghjklmnpqrstvwxyz]$", word):
        forms.append(rf"{escaped}{re.escape(word[-1])}(?:ed|ing|er|ers)")
    return "(?:" + "|".join(dict.fromkeys(forms)) + ")"


def term_regex(rule: dict[str, Any]) -> re.Pattern[str]:
    candidates = [rule.get("family_root"), *(rule.get("match_variants") or []), rule.get("value")]
    bodies = []
    for raw in dict.fromkeys(str(value).strip() for value in candidates if value):
        normalized = raw.replace("\u2018", "'").replace("\u2019", "'")
        parts = [part for part in re.split(r"[-\s\u2010-\u2015]+", normalized) if part]
        encoded = []
        for index, part in enumerate(parts):
            if rule.get("family_match") and index == len(parts) - 1:
                encoded.append(family_body(part))
            else:
                encoded.append(re.escape(part))
        bodies.append(SEPARATOR.join(encoded))
    body = "(?:" + "|".join(dict.fromkeys(bodies)) + ")"
    return re.compile(rf"(?i)(?<![\w]){body}(?![\w])")


def portable_pattern(pattern: str) -> str:
    return pattern.replace(
        r"[\uD83C-\uDBFF][\uDC00-\uDFFF]",
        r"[\U0001F000-\U0001FAFF]",
    )


def word_count(text: str) -> int:
    return len(re.findall(r"(?u)(?<![\w])[\w]+(?:['\-\u2010-\u2015][\w]+)*(?![\w])", text))


def line_column(text: str, index: int) -> tuple[int, int]:
    before = text[:index]
    line = before.count("\n") + 1
    last_break = before.rfind("\n")
    return line, index - last_break


def snippet(text: str, index: int, length: int) -> str:
    start = max(0, index - 45)
    end = min(len(text), index + length + 75)
    return re.sub(r"\s+", " ", text[start:end]).strip()


def load_glossary(path: Path | None) -> tuple[set[str], set[str]]:
    if path is None:
        return set(), set()
    with path.open("r", encoding="utf-8") as handle:
        glossary = json.load(handle)
    if glossary.get("owner_approved") is not True:
        raise ValueError(f"Glossary is not owner approved: {path}")
    return (
        {str(value).casefold() for value in glossary.get("allow_terms", [])},
        {str(value).casefold() for value in glossary.get("allow_rule_ids", [])},
    )


def scan_text(
    text: str,
    rules: dict[str, Any],
    source: str = "<text>",
    allow_terms: Iterable[str] = (),
    allow_rule_ids: Iterable[str] = (),
    protect_markdown: bool = True,
) -> list[dict[str, Any]]:
    original = text
    normalized = (
        text.replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )
    protected = mask_protected_markdown(normalized) if protect_markdown else normalized
    scan_value = mask_markup_tags(protected)
    allowed_terms = {value.casefold() for value in allow_terms}
    allowed_rules = {value.casefold() for value in allow_rule_ids}
    findings: list[dict[str, Any]] = []

    for rule in rules.get("banned_terms", []):
        names = [rule.get("value"), rule.get("family_root"), *(rule.get("match_variants") or [])]
        if str(rule.get("rule_id", "")).casefold() in allowed_rules:
            continue
        if any(str(name).casefold() in allowed_terms for name in names if name):
            continue
        for match in term_regex(rule).finditer(scan_value):
            line, column = line_column(original, match.start())
            findings.append(
                {
                    "source": source,
                    "line": line,
                    "column": column,
                    "rule_id": str(rule["rule_id"]),
                    "category": "term",
                    "enforcement": str(rule.get("enforcement", "hard")),
                    "match": original[match.start() : match.end()],
                    "action": "Rewrite the full sentence using concrete information.",
                    "snippet": snippet(original, match.start(), match.end() - match.start()),
                }
            )

    combined = [
        *rules.get("prohibited_patterns", []),
        *rules.get("style_rules", []),
    ]
    for rule in combined:
        rule_id = str(rule.get("rule_id", ""))
        if rule_id.casefold() in allowed_rules:
            continue
        matches: dict[tuple[int, int], re.Match[str]] = {}
        for expression in rule.get("detection_patterns") or []:
            for match in re.finditer(portable_pattern(str(expression)), scan_value):
                matches[(match.start(), match.end())] = match
        ordered = [matches[key] for key in sorted(matches)]
        allowed_count = 0
        limit = None
        rate = rule.get("rate_limit")
        if rate:
            words = word_count(scan_value)
            blocks = max(1, -(-words // int(rate["per_words"])))
            allowed_count = int(rate["max_occurrences"]) * blocks
            limit = f"{allowed_count} allowed in {words} words"
        for match in ordered[allowed_count:]:
            line, column = line_column(original, match.start())
            findings.append(
                {
                    "source": source,
                    "line": line,
                    "column": column,
                    "rule_id": rule_id,
                    "category": "style" if rule_id.startswith("STYLE-") else "expression",
                    "enforcement": str(rule.get("enforcement", "hard")),
                    "match": original[match.start() : match.end()],
                    "action": str(rule.get("instruction", "")),
                    "limit": limit,
                    "snippet": snippet(original, match.start(), match.end() - match.start()),
                }
            )

    unique: dict[tuple[Any, ...], dict[str, Any]] = {}
    for finding in findings:
        key = (
            finding["source"],
            finding["line"],
            finding["column"],
            finding["rule_id"],
            finding["match"],
        )
        unique[key] = finding
    return sorted(
        unique.values(),
        key=lambda item: (item["source"], item["line"], item["column"], item["rule_id"]),
    )


def default_rules_path() -> Path:
    bundled = Path(__file__).resolve().parent / "AI-Sloppy-Copy-Rules.json"
    if bundled.is_file():
        return bundled
    return Path(__file__).resolve().parent.parent / "dist" / "AI-Sloppy-Copy-Rules.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check authored prose against AI Sloppy Copy rules.")
    parser.add_argument("--text", help="Check one text value.")
    parser.add_argument("paths", nargs="*", help="TXT, MD, CSV, JSON, HTML, XML, or DOCX files.")
    parser.add_argument("--rules", type=Path, default=default_rules_path())
    parser.add_argument("--allow-term", action="append", default=[])
    parser.add_argument("--allow-rule-id", action="append", default=[])
    parser.add_argument("--glossary", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--no-exit", action="store_true")
    parser.add_argument("--hard-only", action="store_true")
    parser.add_argument("--no-protected-markdown", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if (args.text is None) == (not args.paths):
        raise SystemExit("Provide either --text or one or more paths.")
    rules = load_rules(args.rules)
    glossary_terms, glossary_rules = load_glossary(args.glossary)
    allow_terms = {*args.allow_term, *glossary_terms}
    allow_rule_ids = {*args.allow_rule_id, *glossary_rules}
    values = (
        [("<text>", args.text)]
        if args.text is not None
        else [(str(path.resolve()), read_input(path)) for path in map(Path, args.paths)]
    )
    findings = []
    for source, value in values:
        findings.extend(
            scan_text(
                value,
                rules,
                source,
                allow_terms,
                allow_rule_ids,
                not args.no_protected_markdown,
            )
        )
    hard_findings = [item for item in findings if item["enforcement"] == "hard"]
    displayed = hard_findings if args.hard_only else findings

    if args.as_json:
        print(json.dumps(displayed, ensure_ascii=False, indent=2))
    elif not args.quiet:
        if displayed:
            for item in displayed:
                print(
                    f'{item["source"]}:{item["line"]}:{item["column"]} '
                    f'{item["rule_id"]} [{item["enforcement"]}] {item["match"]!r}'
                )
            print(f"FAIL: {len(hard_findings)} hard violation(s); {len(findings) - len(hard_findings)} warning(s).")
        else:
            print("PASS: no AI Sloppy Copy findings.")
    if args.no_exit:
        return 0
    return 1 if hard_findings else 0


if __name__ == "__main__":
    sys.exit(main())
