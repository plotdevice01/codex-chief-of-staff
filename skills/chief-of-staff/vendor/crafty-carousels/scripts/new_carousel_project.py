from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_TEMPLATE = SKILL_ROOT / "assets" / "client-workspace"
RUN_TEMPLATE = WORKSPACE_TEMPLATE / "_templates" / "carousel-run"
PRODUCTION_SYSTEM = SKILL_ROOT / "references" / "production-system.md"
HOOK_LIBRARY_DIR = SKILL_ROOT / "assets" / "hook-library"
RULESET_VERSION = "2026-08-05.3"
MIN_TYPE = {
    "headline_min_px": 68,
    "supporting_min_px": 40,
    "cta_min_px": 48,
    "thumbnail_test_width_px": 320,
}
NARRATIVE_FORMATS = ("comparison", "tutorial", "native", "story-arc", "custom-approved")
CONTENT_CLASSES = ("business", "ugc_creator", "influencer")
HOOK_RESEARCH_FORMATS = ("image_carousel", "video_adaptable", "both")
SAFE_ZONE_MINIMUMS = {"top": 180, "bottom": 180, "left": 50, "right": 120}
ROUTES = {
    "instagram-native": (1080, 1440),
    "instagram-paid-compatible": (1080, 1350),
    "linkedin-document": (1080, 1350),
}
STATUSES = (
    "intake",
    "copy_draft",
    "anchor_review",
    "production",
    "release_review",
    "release_ready",
    "published",
)
TEXT_SUFFIXES = {".md", ".csv", ".json", ".txt"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_hook_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(HOOK_LIBRARY_DIR.glob("*.json")):
        records.extend(json.loads(path.read_text(encoding="utf-8"))["records"])
    return records


def run_file(run: Path, value: object) -> Path | None:
    if not isinstance(value, str) or value in ("", "UNKNOWN"):
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    resolved = (run / relative).resolve()
    return resolved if resolved.is_relative_to(run) else None


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError("Value must contain a letter or number.")
    return slug


def replace_tokens(root: Path, replacements: dict[str, str]) -> None:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            content = path.read_text(encoding="utf-8")
            for old, new in replacements.items():
                content = content.replace(old, new)
            path.write_text(content, encoding="utf-8", newline="\n")


def create_workspace(client_name: str, owner: str, output: Path) -> Path:
    client_name = client_name.strip()
    owner = owner.strip()
    if not client_name or not owner:
        raise ValueError("Client name and owner are required.")
    if not WORKSPACE_TEMPLATE.is_dir():
        raise FileNotFoundError(f"Workspace template not found: {WORKSPACE_TEMPLATE}")

    target = output.resolve()
    if target.exists():
        raise FileExistsError(f"Output already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(WORKSPACE_TEMPLATE, target)
    replace_tokens(
        target,
        {
            "{{CLIENT_NAME}}": client_name,
            "{{CLIENT_SLUG}}": slugify(client_name),
            "{{OWNER}}": owner,
            "{{CREATED_DATE}}": date.today().isoformat(),
        },
    )
    (target / "runs").mkdir()
    (target / "_shared" / "media").mkdir()
    return target


def slide_role(number: int, count: int) -> str:
    if count == 5:
        return ("hook", "value", "frame", "proof", "action")[number - 1]
    if count == 10:
        if number == 1:
            return "hook"
        if number == 2:
            return "tension"
        if number <= 6:
            return "structural-insight"
        if number <= 9:
            return "application"
        return "action"
    if number == 1:
        return "hook"
    if number == count:
        return "action"
    if number == count - 1:
        return "climax"
    if number == 2:
        return "transition"
    return "tease"


def create_run(workspace: Path, slug: str, route: str, slide_count: int) -> Path:
    workspace = workspace.resolve()
    if not (workspace / "CONTEXT.md").is_file() or not (workspace / "runs").is_dir():
        raise ValueError(f"Not a stamped carousel workspace: {workspace}")
    if route not in ROUTES:
        raise ValueError(f"Unsupported route: {route}")
    if slide_count < 2:
        raise ValueError("A carousel requires at least two slides.")

    run_id = f"{date.today():%Y%m%d}-{slugify(slug)}"
    target = workspace / "runs" / run_id
    if target.exists():
        raise FileExistsError(f"Run already exists: {target}")
    shutil.copytree(RUN_TEMPLATE, target)

    client_heading = workspace.joinpath("CONTEXT.md").read_text(encoding="utf-8").splitlines()[0]
    client_name = client_heading.removeprefix("# ").removesuffix(" carousel Pipeline")
    width, height = ROUTES[route]
    slides = [
        {
            "number": number,
            "role": slide_role(number, slide_count),
            "copy": "UNKNOWN",
            "alt_text": "UNKNOWN",
            "final_file": "UNKNOWN",
            "qa": {
                "exact_copy": False,
                "thumbnail_legible": False,
                "stable_contrast": False,
                "text_safe": False,
                "no_glow": False,
                "no_stray_symbols": False,
                "anchor_consistent": False,
                "headline_px": "UNKNOWN",
                "minimum_text_px": "UNKNOWN",
                "cta_px": "UNKNOWN",
            },
        }
        for number in range(1, slide_count + 1)
    ]
    replace_tokens(
        target,
        {
            "{{RUN_ID}}": run_id,
            "{{CLIENT_NAME}}": client_name,
            "{{CREATED_DATE}}": date.today().isoformat(),
            "{{PLATFORM_ROUTE}}": route,
            "{{WIDTH}}": str(width),
            "{{HEIGHT}}": str(height),
            "{{SLIDE_COUNT}}": str(slide_count),
            "{{SLIDES_JSON}}": json.dumps(slides, indent=4),
            "{{RULESET_VERSION}}": RULESET_VERSION,
            "{{RULESET_SHA256}}": sha256_file(PRODUCTION_SYSTEM),
        },
    )
    (target / "slides").mkdir()
    (target / "anchors").mkdir()
    return target


def validate_run(run: Path) -> list[str]:
    run = run.resolve()
    manifest_path = run / "run.json"
    if not manifest_path.is_file():
        return [f"Missing run manifest: {manifest_path}"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"Invalid run manifest: {exc}"]

    errors: list[str] = []
    if manifest.get("schema_version") != 2:
        errors.append("schema_version must be 2")

    ruleset = manifest.get("ruleset", {})
    if ruleset.get("version") != RULESET_VERSION:
        errors.append(f"Run ruleset version must be {RULESET_VERSION}")
    if ruleset.get("production_system_sha256") != sha256_file(PRODUCTION_SYSTEM):
        errors.append("Production rules changed; reread them and repeat affected approvals")

    route = manifest.get("platform", {}).get("route")
    if route not in ROUTES:
        errors.append(f"Unsupported platform route: {route}")
    else:
        expected = ROUTES[route]
        actual = (
            manifest["platform"].get("width"),
            manifest["platform"].get("height"),
        )
        if actual != expected:
            errors.append(f"Route {route} requires dimensions {expected}, found {actual}")

    status = manifest.get("status")
    if status not in STATUSES:
        errors.append(f"Unsupported status: {status}")

    slides = manifest.get("slides")
    count = manifest.get("slide_count")
    if not isinstance(slides, list) or not isinstance(count, int) or count != len(slides):
        errors.append("slide_count must equal the number of slide records")
    elif count < 2:
        errors.append("A carousel requires at least two slides")
    else:
        expected_roles = [slide_role(number, count) for number in range(1, count + 1)]
        actual_roles = [slide.get("role") for slide in slides]
        if actual_roles != expected_roles:
            errors.append(f"Slide roles must be {expected_roles}")

    approvals = manifest.get("approvals", {})
    for name in ("intake", "strategy_copy", "anchor", "release"):
        if not isinstance(approvals.get(name), bool):
            errors.append(f"Approval {name} must be true or false")

    if status in ("copy_draft", "anchor_review", "production", "release_review", "release_ready", "published"):
        if not approvals.get("intake"):
            errors.append("Copy and later states require intake approval")
        if manifest.get("content_class") not in CONTENT_CLASSES:
            errors.append(f"Copy and later states require content_class as one of {CONTENT_CLASSES}")
        if manifest.get("hook_research_format") not in HOOK_RESEARCH_FORMATS:
            errors.append(f"Copy and later states require hook_research_format as one of {HOOK_RESEARCH_FORMATS}")

        hook_selection = manifest.get("hook_library", {})
        selected_ids = hook_selection.get("selected_record_ids")
        if not isinstance(selected_ids, list):
            errors.append("hook_library.selected_record_ids must be a list")
        else:
            library_records = load_hook_records()
            selected_class = manifest.get("content_class")
            selected_format = manifest.get("hook_research_format")
            allowed_formats = {
                "image_carousel": {"image_carousel"},
                "video_adaptable": {"video"},
                "both": {"video", "image_carousel"},
            }.get(selected_format, set())
            valid_ids = {
                record["id"]
                for record in library_records
                if selected_class in record.get("content_classes", [record.get("content_class")])
                and allowed_formats.intersection(record.get("format_fit", []))
            }
            invalid_ids = [record_id for record_id in selected_ids if record_id not in valid_ids]
            if invalid_ids:
                errors.append(f"Hook IDs do not belong to the selected content class: {invalid_ids}")

    if status in ("production", "release_review", "release_ready", "published"):
        if not approvals.get("strategy_copy") or not approvals.get("anchor"):
            errors.append("Production and later states require strategy-copy and anchor approval")

        copy_policy = manifest.get("copy_policy", {})
        mode = copy_policy.get("mode")
        if mode not in ("exact-source", "approved-draft"):
            errors.append("Production requires copy_policy.mode as exact-source or approved-draft")
        if mode == "approved-draft" and manifest.get("hook_library", {}).get("selection_reason") in (None, "", "UNKNOWN"):
            errors.append("Approved-draft production requires a hook selection reason")
        copy_path = run / "copy.md"
        copy_hash = sha256_file(copy_path) if copy_path.is_file() else None
        if copy_policy.get("approved_copy_sha256") != copy_hash:
            errors.append("Approved copy hash does not match copy.md")
        if mode == "exact-source" and copy_policy.get("source_copy_sha256") != copy_hash:
            errors.append("Exact-source mode requires source and approved copy hashes to match copy.md")

        if manifest.get("narrative_format") not in NARRATIVE_FORMATS:
            errors.append(f"Production narrative_format must be one of {NARRATIVE_FORMATS}")

        typography = manifest.get("typography", {})
        if typography.get("family") in (None, "", "UNKNOWN"):
            errors.append("Production requires one approved typography family")
        if not isinstance(typography.get("weight"), int) or typography.get("weight") < 800:
            errors.append("Production typography weight must be at least 800")
        for field, minimum in MIN_TYPE.items():
            value = typography.get(field)
            if not isinstance(value, int) or value < minimum:
                errors.append(f"Typography {field} must be at least {minimum}")

        design_system = manifest.get("design_system", {})
        secondary_family = design_system.get("secondary_font_family")
        if secondary_family in (None, "", "UNKNOWN"):
            errors.append("Production requires secondary_font_family as NONE or one approved family")
        colors = [design_system.get(field) for field in ("background_color", "text_color", "accent_color")]
        if any(not isinstance(color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", color) for color in colors):
            errors.append("Production colors must be three recorded six-digit hex values")
        elif not 2 <= len(set(colors)) <= 3:
            errors.append("Production requires two or three unique colors maximum")
        if design_system.get("visual_thread") in (None, "", "UNKNOWN"):
            errors.append("Production requires one recorded visual thread")
        safe_zone = design_system.get("safe_zone_px", {})
        for edge, minimum in SAFE_ZONE_MINIMUMS.items():
            value = safe_zone.get(edge)
            if not isinstance(value, int) or value < minimum:
                errors.append(f"Safe zone {edge} must be at least {minimum} px")

        candidates = manifest.get("anchor_candidates")
        if not isinstance(candidates, list) or len(candidates) != 3:
            errors.append("Production requires exactly three anchor candidates")
        else:
            candidate_ids: list[str] = []
            for candidate in candidates:
                candidate_id = candidate.get("id")
                candidate_ids.append(candidate_id)
                candidate_path = run_file(run, candidate.get("file"))
                if candidate_path is None or not candidate_path.is_file():
                    errors.append(f"Anchor candidate {candidate_id} file is missing or unsafe")
                elif candidate.get("sha256") != sha256_file(candidate_path):
                    errors.append(f"Anchor candidate {candidate_id} hash does not match its file")
                if candidate.get("composition") in (None, "", "UNKNOWN"):
                    errors.append(f"Anchor candidate {candidate_id} needs a distinct composition record")
                if candidate.get("thumbnail_pass") is not True:
                    errors.append(f"Anchor candidate {candidate_id} must pass the 320 px check")
            if len(set(candidate_ids)) != 3:
                errors.append("Anchor candidate IDs must be distinct")
            if manifest.get("selected_anchor") not in candidate_ids:
                errors.append("selected_anchor must identify one of the three candidates")

        visual_hash = manifest.get("visual_policy", {}).get("approved_anchor_rules_sha256")
        visual_path = run / "visual-brief.md"
        if visual_hash != sha256_file(visual_path):
            errors.append("Approved anchor rules hash does not match visual-brief.md")
        likeness_method = manifest.get("visual_policy", {}).get("likeness_method")
        if likeness_method not in ("not-applicable", "approved-real-photo-composite", "approved-ai-likeness"):
            errors.append("Production requires an approved likeness_method")

    if isinstance(slides, list):
        typography = manifest.get("typography", {})
        for slide in slides:
            final_path = run_file(run, slide.get("final_file"))
            if slide.get("final_file") not in (None, "", "UNKNOWN") and (final_path is None or not final_path.is_file()):
                errors.append(f"Slide {slide.get('number')} final_file is missing or unsafe")
            if final_path is None or not final_path.is_file():
                continue
            qa = slide.get("qa", {})
            for gate in ("exact_copy", "thumbnail_legible", "stable_contrast", "text_safe", "no_glow", "no_stray_symbols", "anchor_consistent"):
                if qa.get(gate) is not True:
                    errors.append(f"Slide {slide.get('number')} requires QA gate: {gate}")
            headline_px = qa.get("headline_px")
            minimum_text_px = qa.get("minimum_text_px")
            if not isinstance(headline_px, int) or headline_px < typography.get("headline_min_px", MIN_TYPE["headline_min_px"]):
                errors.append(f"Slide {slide.get('number')} headline is below the locked minimum")
            if not isinstance(minimum_text_px, int) or minimum_text_px < typography.get("supporting_min_px", MIN_TYPE["supporting_min_px"]):
                errors.append(f"Slide {slide.get('number')} contains undersized text")
            if slide.get("role") == "action":
                cta_px = qa.get("cta_px")
                if not isinstance(cta_px, int) or cta_px < typography.get("cta_min_px", MIN_TYPE["cta_min_px"]):
                    errors.append(f"Slide {slide.get('number')} CTA is below the locked minimum")

    if status in ("release_ready", "published"):
        platform = manifest.get("platform", {})
        verified_max = platform.get("verified_max")
        if not isinstance(verified_max, int) or verified_max < count:
            errors.append("Release requires a live verified platform maximum at or above slide_count")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(platform.get("verified_on", ""))):
            errors.append("Release requires platform.verified_on as YYYY-MM-DD")
        if not approvals.get("release"):
            errors.append("Release-ready and published states require release approval")
        profiles = manifest.get("client_profile_versions", {})
        for name in ("brand", "voice", "people_likeness", "asset_register", "claim_register"):
            if profiles.get(name) in (None, "", "UNKNOWN"):
                errors.append(f"Release requires client profile version: {name}")
        if isinstance(slides, list):
            for slide in slides:
                number = slide.get("number")
                for field in ("copy", "alt_text", "final_file"):
                    if slide.get(field) in (None, "", "UNKNOWN"):
                        errors.append(f"Slide {number} requires {field} before release")

    for filename in ("copy.md", "visual-brief.md", "prompts.md", "qa.md"):
        if not (run / filename).is_file():
            errors.append(f"Missing run file: {filename}")
    return errors


def self_test() -> None:
    with tempfile.TemporaryDirectory() as folder:
        workspace = create_workspace("Example Co", "Test Owner", Path(folder) / "workspace")
        run = create_run(workspace, "one-sharp-idea", "instagram-native", 8)
        assert not validate_run(run)
        compact_run = create_run(workspace, "compact-idea", "instagram-native", 5)
        compact_manifest = json.loads((compact_run / "run.json").read_text(encoding="utf-8"))
        assert [slide["role"] for slide in compact_manifest["slides"]] == ["hook", "value", "frame", "proof", "action"]
        spine_run = create_run(workspace, "long-spine", "instagram-native", 10)
        spine_manifest = json.loads((spine_run / "run.json").read_text(encoding="utf-8"))
        assert [slide["role"] for slide in spine_manifest["slides"]] == [
            "hook", "tension", "structural-insight", "structural-insight", "structural-insight",
            "structural-insight", "application", "application", "application", "action",
        ]
        manifest_path = run / "run.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["status"] = "copy_draft"
        manifest["approvals"]["intake"] = True
        manifest["content_class"] = "business"
        manifest["hook_research_format"] = "image_carousel"
        manifest["hook_library"]["selected_record_ids"] = ["notion-351-001"]
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
        assert not validate_run(run)

        manifest["status"] = "production"
        manifest["content_class"] = "UNKNOWN"
        manifest["hook_research_format"] = "UNKNOWN"
        manifest["approvals"].update({"intake": True, "strategy_copy": True, "anchor": True})
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
        errors = validate_run(run)
        assert any("copy_policy.mode" in error for error in errors)
        assert any("content_class" in error for error in errors)
        assert any("hook_research_format" in error for error in errors)
        assert any("narrative_format" in error for error in errors)
        assert any("Anchor candidate A" in error for error in errors)
        assert any("typography family" in error for error in errors)
        assert any("six-digit hex" in error for error in errors)

        manifest["ruleset"]["production_system_sha256"] = "drifted"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
        assert any("Production rules changed" in error for error in validate_run(run))
    print("self_test=PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description="Stamp and validate a carousel ICM workspace.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--client-name", required=True)
    init_parser.add_argument("--owner", required=True)
    init_parser.add_argument("--output", type=Path, required=True)

    run_parser = subparsers.add_parser("new-run")
    run_parser.add_argument("--workspace", type=Path, required=True)
    run_parser.add_argument("--slug", required=True)
    run_parser.add_argument("--route", choices=sorted(ROUTES), required=True)
    run_parser.add_argument("--slide-count", type=int, default=8)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--run", type=Path, required=True)
    subparsers.add_parser("self-test")
    args = parser.parse_args()

    if args.command == "init":
        print(create_workspace(args.client_name, args.owner, args.output))
    elif args.command == "new-run":
        print(create_run(args.workspace, args.slug, args.route, args.slide_count))
    elif args.command == "validate":
        errors = validate_run(args.run)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("validation=PASS")
    else:
        self_test()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
