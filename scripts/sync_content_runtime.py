from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
VENDOR_ROOT = ROOT / "skills" / "chief-of-staff" / "vendor"
MANIFEST = VENDOR_ROOT / "manifest.json"

PACKAGES = {
    "ai-sloppy-copy": {
        "version": "0.5.0",
        "repository": "https://github.com/plotdevice01/ai-sloppy-copy",
        "paths": (
            "LICENSE",
            "THIRD-PARTY-NOTICES.md",
            "plugins/ai-sloppy-copy/skills/ai-sloppy-copy/SKILL.md",
            "plugins/ai-sloppy-copy/scripts/ai_sloppy_copy.py",
            "plugins/ai-sloppy-copy/scripts/AI-Sloppy-Copy-Rules.json",
        ),
        "skill_prefix": "plugins/ai-sloppy-copy/skills/ai-sloppy-copy/",
        "plugin_prefix": "plugins/ai-sloppy-copy/",
    },
    "brand-voice-factory": {
        "version": "0.2.1",
        "repository": "https://github.com/plotdevice01/brand-voice-factory",
        "include_prefixes": (
            "plugins/brand-voice-factory/skills/brand-voice-copywriter/SKILL.md",
            "plugins/brand-voice-factory/skills/brand-voice-copywriter/references/",
            "plugins/brand-voice-factory/skills/brand-voice-copywriter/scripts/",
            "plugins/brand-voice-factory/skills/brand-voice-copywriter/assets/client-workspace/",
        ),
        "skill_prefix": "plugins/brand-voice-factory/skills/brand-voice-copywriter/",
    },
    "crafty-carousels": {
        "version": "0.6.1",
        "repository": "https://github.com/plotdevice01/crafty-carousels-skill",
        "include_prefixes": (
            "LICENSE",
            "plugins/crafty-carousels/skills/crafty-carousels/SKILL.md",
            "plugins/crafty-carousels/skills/crafty-carousels/references/",
            "plugins/crafty-carousels/skills/crafty-carousels/scripts/",
            "plugins/crafty-carousels/skills/crafty-carousels/assets/",
        ),
        "skill_prefix": "plugins/crafty-carousels/skills/crafty-carousels/",
    },
}


def run_git(repo: Path, *args: str, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=not binary,
    )
    return result.stdout if not binary else result.stdout


def git_files(repo: Path, ref: str) -> list[str]:
    output = run_git(repo, "ls-tree", "-r", "--name-only", ref)
    assert isinstance(output, str)
    return [line for line in output.splitlines() if line]


def selected_paths(repo: Path, ref: str, config: dict[str, object]) -> list[str]:
    available = git_files(repo, ref)
    exact = set(config.get("paths", ()))
    prefixes = tuple(config.get("include_prefixes", ()))
    selected = [path for path in available if path in exact or path.startswith(prefixes)]
    missing = sorted(exact - set(selected))
    if missing:
        raise ValueError(f"Missing pinned source files: {missing}")
    return selected


def destination(package: str, source: str, config: dict[str, object]) -> Path:
    skill_prefix = str(config.get("skill_prefix", ""))
    plugin_prefix = str(config.get("plugin_prefix", ""))
    if source.endswith("/SKILL.md"):
        relative = PurePosixPath("workflow.md")
    elif skill_prefix and source.startswith(skill_prefix):
        relative = PurePosixPath(source.removeprefix(skill_prefix))
    elif plugin_prefix and source.startswith(plugin_prefix):
        relative = PurePosixPath(source.removeprefix(plugin_prefix))
    else:
        relative = PurePosixPath("notices") / PurePosixPath(source).name
    return VENDOR_ROOT / package / Path(*relative.parts)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sync(roots: dict[str, Path]) -> None:
    stage = VENDOR_ROOT.with_name("vendor.next")
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    records: dict[str, object] = {"schema_version": 1, "packages": {}}
    try:
        for package, config in PACKAGES.items():
            repo = roots[package].resolve()
            ref_text = run_git(repo, "rev-parse", "HEAD")
            assert isinstance(ref_text, str)
            ref = ref_text.strip()
            version_bytes = run_git(repo, "cat-file", "blob", f"{ref}:VERSION", binary=True)
            assert isinstance(version_bytes, bytes)
            version = version_bytes.decode("utf-8-sig").strip()
            if version != config["version"]:
                raise ValueError(f"{package} is {version}; expected {config['version']}")
            files = []
            for source in selected_paths(repo, ref, config):
                content = run_git(repo, "cat-file", "blob", f"{ref}:{source}", binary=True)
                assert isinstance(content, bytes)
                target = destination(package, source, config)
                relative = target.relative_to(VENDOR_ROOT)
                staged = stage / relative
                staged.parent.mkdir(parents=True, exist_ok=True)
                staged.write_bytes(content)
                files.append(
                    {
                        "source": source,
                        "destination": relative.as_posix(),
                        "sha256": sha256_bytes(content),
                        "bytes": len(content),
                    }
                )
            records["packages"][package] = {
                "version": version,
                "repository": config["repository"],
                "commit": ref,
                "files": files,
            }
        (stage / "manifest.json").write_text(
            json.dumps(records, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        if VENDOR_ROOT.exists():
            shutil.rmtree(VENDOR_ROOT)
        stage.replace(VENDOR_ROOT)
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def check() -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("Content runtime manifest schema must be 1")
    packages = payload.get("packages", {})
    if set(packages) != set(PACKAGES):
        raise ValueError("Content runtime package set differs from the pinned contract")
    expected: set[str] = {"manifest.json"}
    for package, config in PACKAGES.items():
        record = packages[package]
        if record.get("version") != config["version"]:
            raise ValueError(f"Wrong pinned version for {package}")
        if record.get("repository") != config["repository"]:
            raise ValueError(f"Wrong source repository for {package}")
        if not record.get("commit"):
            raise ValueError(f"Missing source commit for {package}")
        for item in record.get("files", []):
            relative = str(item["destination"])
            expected.add(relative)
            path = VENDOR_ROOT / relative
            if not path.is_file():
                raise ValueError(f"Missing vendored file: {relative}")
            content = path.read_bytes()
            if sha256_bytes(content) != item["sha256"] or len(content) != item["bytes"]:
                raise ValueError(f"Vendored file differs from its lock record: {relative}")
    actual = {
        path.relative_to(VENDOR_ROOT).as_posix()
        for path in VENDOR_ROOT.rglob("*")
        if path.is_file()
    }
    extra = sorted(actual - expected)
    missing = sorted(expected - actual)
    if extra or missing:
        raise ValueError(f"Vendored file inventory differs: extra={extra}, missing={missing}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Vendor or verify Chief content runtime files.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    sync_parser = subparsers.add_parser("sync")
    sync_parser.add_argument("--ai-sloppy-copy-root", type=Path, required=True)
    sync_parser.add_argument("--brand-voice-factory-root", type=Path, required=True)
    sync_parser.add_argument("--crafty-carousels-root", type=Path, required=True)
    subparsers.add_parser("check")
    args = parser.parse_args()
    if args.command == "sync":
        sync(
            {
                "ai-sloppy-copy": args.ai_sloppy_copy_root,
                "brand-voice-factory": args.brand_voice_factory_root,
                "crafty-carousels": args.crafty_carousels_root,
            }
        )
    check()
    print("PASS: Chief content runtime matches its pinned source manifest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
