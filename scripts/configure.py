from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path

try:
    from .config_paths import ROOT, default_write_path, resolve_config_path
except ImportError:
    from config_paths import ROOT, default_write_path, resolve_config_path


EXAMPLE = ROOT / "chief-of-staff.example.json"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def write_json_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, indent=2)
            stream.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def initialize(args: argparse.Namespace) -> int:
    output = (
        Path(args.output).expanduser().resolve()
        if args.output
        else default_write_path().resolve()
    )
    if output.exists() and not args.force:
        print(f"UNCHANGED: configuration already exists at {output}")
        print("Use --force only when replacing it is deliberate.")
        return 2

    config = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    config["release_version"] = VERSION
    config["updated"] = date.today().isoformat()
    config["owner"]["name"] = args.owner
    config["owner"]["timezone"] = args.timezone
    write_json_atomic(output, config)
    print(f"CREATED: {output}")
    print("Connectors remain disabled and projects remain empty until configured.")
    return 0


def show_path(args: argparse.Namespace) -> int:
    try:
        path = resolve_config_path(args.config)
        print(path)
        return 0
    except FileNotFoundError:
        print(default_write_path().resolve())
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize or locate the local Chief of Staff configuration."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init", help="Create a safe local configuration."
    )
    init_parser.add_argument("--owner", default="Your Name")
    init_parser.add_argument("--timezone", default="Etc/UTC")
    init_parser.add_argument("--output")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(handler=initialize)

    path_parser = subparsers.add_parser(
        "path", help="Print the resolved configuration path."
    )
    path_parser.add_argument("--config")
    path_parser.set_defaults(handler=show_path)

    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
