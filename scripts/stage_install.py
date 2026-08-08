from __future__ import annotations

import argparse
import shutil
from pathlib import Path

try:
    from .config_paths import ROOT
    from .package_files import stage_package
except ImportError:
    from config_paths import ROOT
    from package_files import stage_package


def validate_target(target: Path) -> Path:
    target = target.expanduser().resolve()
    expected = (ROOT / ".install" / "codex-chief-of-staff").resolve()
    if target != expected:
        raise ValueError(f"Install staging must use the repository-owned path {expected}.")
    if target.name != "codex-chief-of-staff":
        raise ValueError("Install staging directory must be named codex-chief-of-staff.")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage a clean Chief marketplace from canonical repository files."
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    target = validate_target(args.output)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    hashes = stage_package(target)
    print(f"PASS: staged {len(hashes)} canonical files at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
