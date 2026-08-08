from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from datetime import date
from pathlib import Path


REQUIRED_ROLES = {
    "voice_architecture",
    "terminology_register",
    "claim_register",
    "asset_register",
    "prohibited_language",
}
APPROVED_STATUSES = {"Approved", "Public ready"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if payload.get("schema_version") != 1:
        raise ValueError("Unsupported Brand Voice package schema version.")
    for field in ("package_id", "client_id", "client_name", "package_version", "status"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            raise ValueError(f"Manifest field is required: {field}")
    files = payload.get("files")
    if not isinstance(files, dict) or set(files) != REQUIRED_ROLES:
        raise ValueError("Manifest files must contain the five required roles.")
    for role, record in files.items():
        if not isinstance(record, dict) or not str(record.get("path", "")).strip():
            raise ValueError(f"Manifest path is required: {role}")
        relative = Path(str(record["path"]))
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Manifest path must stay inside the workspace: {role}")
    return payload


def workspace_root(manifest_path: Path) -> Path:
    resolved = manifest_path.resolve()
    expected = ("stages", "04_package", "output")
    if tuple(part.lower() for part in resolved.parent.parts[-3:]) != expected:
        raise ValueError("Package manifest must be in stages/04_package/output.")
    return resolved.parents[3]


def verify(manifest_path: Path, require_approved: bool = False) -> dict:
    payload = load_manifest(manifest_path)
    if require_approved and payload["status"] not in APPROVED_STATUSES:
        raise ValueError("Package status must be Approved or Public ready.")
    if payload["status"] in APPROVED_STATUSES:
        if payload.get("approved_by") in (None, "", "UNKNOWN"):
            raise ValueError("Approved packages require approved_by.")
        if payload.get("approved_on") in (None, "", "UNKNOWN"):
            raise ValueError("Approved packages require approved_on.")
    root = workspace_root(manifest_path)
    for role, record in payload["files"].items():
        source = (root / record["path"]).resolve()
        if root not in source.parents:
            raise ValueError(f"Manifest path escapes the workspace: {role}")
        if require_approved and not source.is_file():
            raise FileNotFoundError(f"Package file is missing: {role}: {source}")
        expected = record.get("sha256")
        if source.is_file() and expected not in (None, "", "UNKNOWN"):
            actual = sha256(source)
            if actual != expected:
                raise ValueError(f"Package file hash mismatch: {role}")
        elif require_approved:
            raise ValueError(f"Package file hash is required: {role}")
    return payload


def seal(manifest_path: Path, status: str, approved_by: str, approved_on: str) -> dict:
    if status not in APPROVED_STATUSES:
        raise ValueError("Status must be Approved or Public ready.")
    if not approved_by.strip():
        raise ValueError("approved_by is required.")
    payload = load_manifest(manifest_path)
    root = workspace_root(manifest_path)
    for role, record in payload["files"].items():
        source = (root / record["path"]).resolve()
        if root not in source.parents or not source.is_file():
            raise FileNotFoundError(f"Package file is missing: {role}: {source}")
        record["sha256"] = sha256(source)
    payload["status"] = status
    payload["approved_by"] = approved_by.strip()
    payload["approved_on"] = approved_on
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return verify(manifest_path, require_approved=True)


def self_test() -> None:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder) / "workspace"
        manifest_path = root / "stages" / "04_package" / "output" / "package-manifest.json"
        manifest_path.parent.mkdir(parents=True)
        files = {}
        for role in sorted(REQUIRED_ROLES):
            relative = Path("package") / f"{role}.txt"
            source = root / relative
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(role, encoding="utf-8")
            files[role] = {"path": relative.as_posix(), "sha256": "UNKNOWN"}
        manifest_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "package_id": "acme-brand-voice",
                    "client_id": "acme",
                    "client_name": "Acme",
                    "package_version": "0.2.1",
                    "status": "Draft",
                    "approved_by": "UNKNOWN",
                    "approved_on": "UNKNOWN",
                    "files": files,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        seal(manifest_path, "Approved", "Test Owner", date.today().isoformat())
        verify(manifest_path, require_approved=True)
        source.write_text("tampered", encoding="utf-8")
        try:
            verify(manifest_path, require_approved=True)
            raise AssertionError("tampered package passed verification")
        except ValueError as error:
            assert "hash mismatch" in str(error)
    print("self_test=PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description="Seal or verify a Brand Voice package manifest.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--manifest", type=Path, required=True)
    verify_parser.add_argument("--require-approved", action="store_true")
    seal_parser = subparsers.add_parser("seal")
    seal_parser.add_argument("--manifest", type=Path, required=True)
    seal_parser.add_argument("--status", choices=sorted(APPROVED_STATUSES), required=True)
    seal_parser.add_argument("--approved-by", required=True)
    seal_parser.add_argument("--approved-on", default=date.today().isoformat())
    subparsers.add_parser("self-test")
    args = parser.parse_args()
    if args.command == "self-test":
        self_test()
    elif args.command == "verify":
        verify(args.manifest, args.require_approved)
        print("manifest=PASS")
    else:
        seal(args.manifest, args.status, args.approved_by, args.approved_on)
        print("manifest=SEALED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
