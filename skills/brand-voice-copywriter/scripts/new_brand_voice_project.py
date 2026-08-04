from __future__ import annotations

import argparse
import re
import shutil
import tempfile
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_ROOT / "assets" / "client-workspace"
STAGES = (
    "01_intake",
    "02_evidence",
    "03_voice",
    "04_package",
    "05_copy",
    "06_release",
)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError("Client name must contain a letter or number.")
    return slug


def create_project(client_name: str, owner: str, output: Path) -> Path:
    client_name = client_name.strip()
    owner = owner.strip()
    if not client_name or not owner:
        raise ValueError("Client name and owner are required.")
    if not TEMPLATE.is_dir():
        raise FileNotFoundError(f"Template not found: {TEMPLATE}")

    target = output.resolve()
    if target.exists():
        raise FileExistsError(f"Output already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE, target)

    replacements = {
        "{{CLIENT_NAME}}": client_name,
        "{{CLIENT_SLUG}}": slugify(client_name),
        "{{OWNER}}": owner,
        "{{CREATED_DATE}}": date.today().isoformat(),
    }
    for path in target.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".csv", ".json", ".txt"}:
            text = path.read_text(encoding="utf-8")
            for old, new in replacements.items():
                text = text.replace(old, new)
            path.write_text(text, encoding="utf-8", newline="\n")

    for stage in STAGES:
        (target / "stages" / stage / "output").mkdir(parents=True, exist_ok=True)
    (target / "runs").mkdir()
    return target


def self_test() -> None:
    with tempfile.TemporaryDirectory() as folder:
        target = Path(folder) / "acme-health"
        created = create_project("Acme Health", "Test Owner", target)
        assert (created / "AGENTS.md").is_file()
        assert all((created / "stages" / stage / "output").is_dir() for stage in STAGES)
        assert "Acme Health" in (created / "CONTEXT.md").read_text(encoding="utf-8")
        assert "{{CLIENT_NAME}}" not in (created / "CONTEXT.md").read_text(encoding="utf-8")
    print("self_test=PASS")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stamp a blank brand-voice ICM workspace.")
    parser.add_argument("--client-name")
    parser.add_argument("--owner")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return
    if not args.client_name or not args.owner or not args.output:
        parser.error("--client-name, --owner, and --output are required")
    print(create_project(args.client_name, args.owner, args.output))


if __name__ == "__main__":
    main()
