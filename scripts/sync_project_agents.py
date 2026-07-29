from __future__ import annotations

import argparse
import difflib
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

try:
    from .config_paths import ROOT, resolve_config_path
except ImportError:
    from config_paths import ROOT, resolve_config_path


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
    "qa",
    "release",
    "repository",
    "tmp",
    "venv",
}


@dataclass(frozen=True)
class Target:
    path: Path
    project_id: str
    scope: str
    replace_legacy: bool = False


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


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
    for project in config.get("projects", []):
        if project.get("enabled", True) is False or project.get("id") == "chief-of-staff":
            continue
        project_id = str(project["id"])
        scope = str(project["scope"])
        explicit = project.get("instructions")
        if explicit:
            path = Path(explicit).expanduser().resolve()
            targets.setdefault(path, Target(path, project_id, scope))
        for raw_root in project.get("paths", []):
            root = Path(raw_root).expanduser().resolve()
            target = Target(root / "AGENTS.md", project_id, scope)
            targets.setdefault(target.path, target)
            for nested in find_nested_agents(root):
                nested = nested.resolve()
                targets.setdefault(nested, Target(nested, project_id, scope))
    if include_global:
        path = Path.home() / ".codex" / "AGENTS.md"
        targets[path] = Target(
            path, "account-default", "all-configured-scopes", replace_legacy=True
        )
    return sorted(targets.values(), key=lambda item: str(item.path).lower())


def build_managed_block(config: dict, config_path: Path) -> str:
    version = config["release_version"]
    source = SOURCE_AGENTS.read_text(encoding="utf-8").strip()
    persona = ROOT / "persona" / "technical-assistant-persona.txt"
    source = source.replace(
        "`persona/technical-assistant-persona.txt`", f"`{persona}`"
    )
    source = source.replace(
        "the resolved Chief of Staff configuration", f"`{config_path}`"
    )
    return f"{MANAGED_START} version={version} -->\n{source}\n{MANAGED_END}"


def default_project_rules(target: Target) -> str:
    return (
        "# Project-specific rules\n\n"
        f"- Project ID: `{target.project_id}`\n"
        f"- Scope: `{target.scope}`\n"
        "- Read project source files, handoff documents, scripts, generated "
        "outputs, and nested instructions before substantive work.\n"
        "- Do not invent missing requirements, evidence, access, approval, or "
        "authority."
    )


def extract_project_rules(current: str, target: Target) -> str:
    if target.replace_legacy:
        return (
            "# Account-specific rules\n\n"
            "Load the selected project's project-specific rules after this "
            "account-wide Chief of Staff contract."
        )
    if PROJECT_START in current and PROJECT_END in current:
        start = current.index(PROJECT_START) + len(PROJECT_START)
        end = current.index(PROJECT_END, start)
        return current[start:end].strip()
    if MANAGED_START in current and MANAGED_END in current:
        end = current.index(MANAGED_END) + len(MANAGED_END)
        return current[end:].strip() or default_project_rules(target)
    return current.strip() or default_project_rules(target)


def render_target(managed: str, current: str, target: Target) -> str:
    return (
        f"{managed}\n\n{PROJECT_START}\n"
        f"{extract_project_rules(current, target)}\n{PROJECT_END}\n"
    )


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Propagate the Chief contract without replacing project rules."
    )
    parser.add_argument("--config")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--include-global", action="store_true")
    parser.add_argument("--diff", action="store_true")
    args = parser.parse_args()

    config_path = resolve_config_path(args.config)
    config = load_config(config_path)
    managed = build_managed_block(config, config_path)
    targets = collect_targets(config, args.include_global)
    changes: list[tuple[Target, str, str]] = []

    for target in targets:
        current = (
            target.path.read_text(encoding="utf-8") if target.path.is_file() else ""
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
            write_atomic(target.path, desired)
            print(f"UPDATED: {target.path}")
        print(f"PASS: {len(changes)} file(s) updated; {len(targets)} target(s) managed.")
        return 0

    if changes:
        for target, _, _ in changes:
            print(f"DRIFT: {target.path}")
        print(f"FAIL: {len(changes)} of {len(targets)} target(s) need synchronization.")
        return 1

    print(
        f"PASS: {len(targets)} target(s) match Chief of Staff "
        f"v{config['release_version']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
