from __future__ import annotations

import argparse
import difflib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "chief-of-staff.json"
SOURCE_AGENTS = ROOT / "AGENTS.md"
MANAGED_START = "<!-- CHIEF-OF-STAFF-MANAGED:START"
MANAGED_END = "<!-- CHIEF-OF-STAFF-MANAGED:END -->"
PROJECT_START = "<!-- PROJECT-SPECIFIC-RULES:START -->"
PROJECT_END = "<!-- PROJECT-SPECIFIC-RULES:END -->"
IGNORED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "github-release",
    "node_modules",
    "release",
    "tmp",
    "venv",
}


@dataclass(frozen=True)
class Target:
    path: Path
    project_id: str
    scope: str
    replace_legacy: bool = False


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8-sig"))


def find_nested_agents(root: Path) -> list[Path]:
    found: list[Path] = []
    if not root.is_dir():
        return found
    for current, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in IGNORED_DIRS]
        if "AGENTS.md" in files:
            found.append(Path(current) / "AGENTS.md")
    return found


def collect_targets(config: dict, include_global: bool) -> list[Target]:
    targets: dict[Path, Target] = {}
    for project in config["projects"]:
        if project["id"] == "chief-of-staff":
            continue
        roots = [Path(value).resolve() for value in project.get("paths", [])]
        for root in roots:
            target = Target(root / "AGENTS.md", project["id"], project["scope"])
            targets.setdefault(target.path, target)
            for nested in find_nested_agents(root):
                targets.setdefault(
                    nested.resolve(),
                    Target(nested.resolve(), project["id"], project["scope"]),
                )
    if include_global:
        global_path = Path.home() / ".codex" / "AGENTS.md"
        targets[global_path] = Target(
            global_path,
            "account-default",
            "all-configured-scopes",
            replace_legacy=True,
        )
    return sorted(targets.values(), key=lambda item: str(item.path).lower())


def build_managed_block(config: dict) -> str:
    version = config.get("version") or config["release_version"]
    source = SOURCE_AGENTS.read_text(encoding="utf-8").strip()
    persona = ROOT / "persona" / "technical-assistant-persona.txt"
    source = source.replace(
        "`persona/technical-assistant-persona.txt`",
        f"`{persona}`",
    )
    source = source.replace(
        "`chief-of-staff.json`",
        f"`{CONFIG}`",
    )
    return (
        f"{MANAGED_START} version={version} -->\n"
        f"{source}\n"
        f"{MANAGED_END}"
    )


def extract_project_rules(current: str, target: Target) -> str:
    if target.replace_legacy:
        return (
            "# Account-specific rules\n\n"
            "Use the selected project's project-specific rules after loading this "
            "account-wide Chief of Staff contract."
        )
    if PROJECT_START in current and PROJECT_END in current:
        start = current.index(PROJECT_START) + len(PROJECT_START)
        end = current.index(PROJECT_END, start)
        return current[start:end].strip()
    if MANAGED_START in current and MANAGED_END in current:
        end = current.index(MANAGED_END) + len(MANAGED_END)
        remainder = current[end:].strip()
        return remainder or default_project_rules(target)
    return current.strip() or default_project_rules(target)


def default_project_rules(target: Target) -> str:
    return (
        "# Project-specific rules\n\n"
        f"- Project ID: `{target.project_id}`\n"
        f"- Scope: `{target.scope}`\n"
        "- Read the project source files, handoff documents, scripts, generated "
        "outputs, and nested instructions before substantive work.\n"
        "- Do not invent missing requirements, evidence, access, approval, or "
        "authority."
    )


def render_target(managed: str, current: str, target: Target) -> str:
    project_rules = extract_project_rules(current, target)
    return (
        f"{managed}\n\n"
        f"{PROJECT_START}\n"
        f"{project_rules}\n"
        f"{PROJECT_END}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Propagate the Chief of Staff contract without replacing project rules."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Report drift without writing.")
    mode.add_argument("--apply", action="store_true", help="Write all required updates.")
    parser.add_argument(
        "--include-global",
        action="store_true",
        help="Also update the current user's .codex/AGENTS.md.",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Print exact unified diffs for changed targets.",
    )
    args = parser.parse_args()

    config = load_config()
    managed = build_managed_block(config)
    targets = collect_targets(config, args.include_global)
    changes: list[tuple[Target, str, str]] = []

    for target in targets:
        current = (
            target.path.read_text(encoding="utf-8")
            if target.path.is_file()
            else ""
        )
        desired = render_target(managed, current, target)
        if current != desired:
            changes.append((target, current, desired))

    if args.diff:
        for target, current, desired in changes:
            sys.stdout.writelines(
                difflib.unified_diff(
                    current.splitlines(keepends=True),
                    desired.splitlines(keepends=True),
                    fromfile=str(target.path),
                    tofile=str(target.path),
                )
            )

    if args.apply:
        for target, _, desired in changes:
            target.path.parent.mkdir(parents=True, exist_ok=True)
            target.path.write_text(desired, encoding="utf-8", newline="\n")
            print(f"UPDATED: {target.path}")
        print(f"PASS: {len(changes)} file(s) updated; {len(targets)} target(s) managed.")
        return 0

    if changes:
        for target, _, _ in changes:
            print(f"DRIFT: {target.path}")
        print(f"FAIL: {len(changes)} of {len(targets)} target(s) need synchronization.")
        return 1

    version = config.get("version") or config["release_version"]
    print(f"PASS: {len(targets)} target(s) match Chief of Staff v{version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
