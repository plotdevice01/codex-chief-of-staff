from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_TEMPLATE = SKILL_ROOT / "assets" / "client-workspace"
RUN_TEMPLATE = WORKSPACE_TEMPLATE / "_templates" / "carousel-run"
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
        },
    )
    (target / "slides").mkdir()
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

    if status in ("production", "release_review", "release_ready", "published"):
        if not approvals.get("strategy_copy") or not approvals.get("anchor"):
            errors.append("Production and later states require strategy-copy and anchor approval")

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
        manifest_path = run / "run.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["status"] = "release_ready"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
        assert validate_run(run), "Release gate should reject incomplete records."
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
