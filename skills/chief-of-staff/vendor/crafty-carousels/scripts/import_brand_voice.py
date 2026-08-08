from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import shutil
import tempfile
from pathlib import Path


REQUIRED_ROLES = {
    "voice_architecture",
    "terminology_register",
    "claim_register",
    "asset_register",
    "prohibited_language",
}
APPROVED_STATUSES = {"Approved", "Public ready"}
CLAIM_FIELDS = (
    "claim_id",
    "approved_wording",
    "status",
    "source_path",
    "source_scope",
    "verified_by",
    "verified_on",
    "expiry_or_recheck",
    "notes",
)
ASSET_FIELDS = (
    "asset_id",
    "local_path",
    "asset_type",
    "person_or_owner",
    "source",
    "rights_holder",
    "organic_allowed",
    "paid_media_allowed",
    "ai_edit_allowed",
    "ai_generation_reference_allowed",
    "approved_platforms",
    "territory",
    "expiry_date",
    "approved_by",
    "approved_on",
    "required_credit",
    "exclusions",
    "status",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")


def load_package(manifest_path: Path) -> tuple[dict, Path, dict[str, Path]]:
    payload = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    if payload.get("schema_version") != 1:
        raise ValueError("Unsupported Brand Voice package schema version.")
    if payload.get("status") not in APPROVED_STATUSES:
        raise ValueError("Brand Voice package must be Approved or Public ready.")
    if payload.get("approved_by") in (None, "", "UNKNOWN") or payload.get("approved_on") in (None, "", "UNKNOWN"):
        raise ValueError("Brand Voice package approval is incomplete.")
    files = payload.get("files")
    if not isinstance(files, dict) or set(files) != REQUIRED_ROLES:
        raise ValueError("Brand Voice package files are incomplete.")
    root = manifest_path.resolve().parents[3]
    resolved: dict[str, Path] = {}
    for role, record in files.items():
        relative = Path(str(record.get("path", "")))
        source = (root / relative).resolve()
        if relative.is_absolute() or ".." in relative.parts or root not in source.parents:
            raise ValueError(f"Package path escapes the workspace: {role}")
        if not source.is_file():
            raise FileNotFoundError(f"Package file is missing: {role}: {source}")
        if sha256(source) != record.get("sha256"):
            raise ValueError(f"Package file hash mismatch: {role}")
        resolved[role] = source
    return payload, root, resolved


def read_csv(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8-sig"))))


def write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require_blank_workspace(workspace: Path) -> str:
    context = workspace / "CONTEXT.md"
    voice = workspace / "_shared" / "voice.md"
    if not context.is_file() or not voice.is_file():
        raise ValueError(f"Not a stamped Crafty workspace: {workspace}")
    if "- Profile version: UNKNOWN" not in voice.read_text(encoding="utf-8"):
        raise ValueError("Crafty voice controls are already configured.")
    for name in ("claim-register.csv", "asset-register.csv"):
        if read_csv(workspace / "_shared" / name):
            raise ValueError(f"Crafty register is not blank: {name}")
    return context.read_text(encoding="utf-8").splitlines()[0].removeprefix("# ").removesuffix(" carousel Pipeline")


def import_package(manifest_path: Path, workspace: Path) -> Path:
    manifest_path = manifest_path.resolve()
    workspace = workspace.resolve()
    payload, _, files = load_package(manifest_path)
    receipt_path = workspace / "_shared" / "brand-voice-import.json"
    manifest_hash = sha256(manifest_path)
    if receipt_path.is_file():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if receipt.get("manifest_sha256") == manifest_hash:
            return receipt_path
        raise ValueError("A different Brand Voice package is already imported.")
    workspace_client = require_blank_workspace(workspace)
    if slugify(workspace_client) != payload["client_id"]:
        raise ValueError("Brand Voice and Crafty client IDs do not match.")

    claims = []
    for row in read_csv(files["claim_register"]):
        claims.append(
            {
                "claim_id": row.get("Claim ID", ""),
                "approved_wording": row.get("Exact claim", ""),
                "status": row.get("Decision", ""),
                "source_path": row.get("Source IDs", ""),
                "source_scope": row.get("Claim class", ""),
                "verified_by": row.get("Owner route", ""),
                "verified_on": row.get("Review date", ""),
                "expiry_or_recheck": row.get("Review date", ""),
                "notes": "; ".join(
                    value
                    for value in (
                        row.get("Required qualification", ""),
                        row.get("Approval reference", ""),
                    )
                    if value
                ),
            }
        )
    assets = []
    for row in read_csv(files["asset_register"]):
        assets.append(
            {
                "asset_id": row.get("Asset ID", ""),
                "local_path": row.get("Template or file", ""),
                "asset_type": row.get("Format", ""),
                "person_or_owner": "",
                "source": row.get("Source packet", ""),
                "rights_holder": "",
                "organic_allowed": "UNKNOWN",
                "paid_media_allowed": "UNKNOWN",
                "ai_edit_allowed": "UNKNOWN",
                "ai_generation_reference_allowed": "UNKNOWN",
                "approved_platforms": row.get("Channel", ""),
                "territory": "UNKNOWN",
                "expiry_date": "UNKNOWN",
                "approved_by": row.get("Owner route", ""),
                "approved_on": "UNKNOWN",
                "required_credit": "UNKNOWN",
                "exclusions": "UNKNOWN",
                "status": row.get("Status", ""),
            }
        )

    shared = workspace / "_shared"
    package_dir = shared / "brand-voice-package"
    package_dir.mkdir()
    copied = {}
    for role, source in files.items():
        target = package_dir / f"{role}{source.suffix.lower()}"
        shutil.copy2(source, target)
        copied[role] = target.relative_to(workspace).as_posix()
    voice_text = files["voice_architecture"].read_text(encoding="utf-8-sig")
    (shared / "voice.md").write_text(
        "# Voice controls\n\n"
        f"- Profile version: {payload['package_version']}\n"
        f"- Approved by and date: {payload['approved_by']} on {payload['approved_on']}\n"
        f"- Brand Voice package: {payload['package_id']}\n"
        f"- Package status: {payload['status']}\n"
        "- Imported terminology: `_shared/brand-voice-package/terminology_register.csv`\n"
        "- Imported prohibited language: `_shared/brand-voice-package/prohibited_language.md`\n\n"
        "## Approved voice architecture\n\n"
        + voice_text.rstrip()
        + "\n",
        encoding="utf-8",
    )
    write_csv(shared / "claim-register.csv", CLAIM_FIELDS, claims)
    write_csv(shared / "asset-register.csv", ASSET_FIELDS, assets)
    receipt = {
        "schema_version": 1,
        "package_id": payload["package_id"],
        "package_version": payload["package_version"],
        "client_id": payload["client_id"],
        "status": payload["status"],
        "manifest_sha256": manifest_hash,
        "copied_files": copied,
        "claim_rows": len(claims),
        "asset_rows": len(assets),
        "unmapped_asset_controls": [
            "rights_holder",
            "organic_allowed",
            "paid_media_allowed",
            "ai_edit_allowed",
            "ai_generation_reference_allowed",
            "territory",
            "expiry_date",
            "approved_on",
            "required_credit",
            "exclusions",
        ],
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt_path


def self_test() -> None:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        source = root / "brand"
        output = source / "stages" / "04_package" / "output"
        output.mkdir(parents=True)
        files = {}
        samples = {
            "voice_architecture": ("voice.md", "# Voice\n\nDirect and clear.\n"),
            "terminology_register": ("terms.csv", "Term,Class\nExample,Preferred\n"),
            "claim_register": ("claims.csv", "Claim ID,Exact claim,Claim class,Source IDs,Required qualification,Owner route,Decision,Approval reference,Review date\nCLM-1,Example claim,Fact,SRC-1,,Owner,Approved,APR-1,2026-08-05\n"),
            "asset_register": ("assets.csv", "Asset ID,Format,Channel,Audience,Job,Template or file,Source packet,Owner route,Status,Release reference\nAST-1,PNG,Instagram,,Logo,logo.png,SRC-1,Owner,Approved,APR-1\n"),
            "prohibited_language": ("blocked.md", "# Prohibited language\n"),
        }
        for role, (name, content) in samples.items():
            path = source / name
            path.write_text(content, encoding="utf-8")
            files[role] = {"path": name, "sha256": sha256(path)}
        manifest = output / "package-manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "package_id": "acme-brand-voice",
                    "client_id": "acme",
                    "client_name": "Acme",
                    "package_version": "0.2.0",
                    "status": "Approved",
                    "approved_by": "Owner",
                    "approved_on": "2026-08-05",
                    "files": files,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        workspace = root / "crafty"
        shared = workspace / "_shared"
        shared.mkdir(parents=True)
        (workspace / "CONTEXT.md").write_text("# Acme carousel Pipeline\n", encoding="utf-8")
        (shared / "voice.md").write_text("# Voice controls\n\n- Profile version: UNKNOWN\n", encoding="utf-8")
        write_csv(shared / "claim-register.csv", CLAIM_FIELDS, [])
        write_csv(shared / "asset-register.csv", ASSET_FIELDS, [])
        receipt = import_package(manifest, workspace)
        assert receipt.is_file()
        assert import_package(manifest, workspace) == receipt
        assert len(read_csv(shared / "claim-register.csv")) == 1
        assert len(read_csv(shared / "asset-register.csv")) == 1
        mismatch = root / "mismatch"
        mismatch_shared = mismatch / "_shared"
        mismatch_shared.mkdir(parents=True)
        (mismatch / "CONTEXT.md").write_text("# Other Client carousel Pipeline\n", encoding="utf-8")
        (mismatch_shared / "voice.md").write_text("# Voice controls\n\n- Profile version: UNKNOWN\n", encoding="utf-8")
        write_csv(mismatch_shared / "claim-register.csv", CLAIM_FIELDS, [])
        write_csv(mismatch_shared / "asset-register.csv", ASSET_FIELDS, [])
        try:
            import_package(manifest, mismatch)
            raise AssertionError("mismatched client package was imported")
        except ValueError as error:
            assert "client IDs do not match" in str(error)
        (source / "voice.md").write_text("tampered", encoding="utf-8")
        try:
            load_package(manifest)
            raise AssertionError("tampered package passed verification")
        except ValueError as error:
            assert "hash mismatch" in str(error)
    print("self_test=PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import an approved Brand Voice package into a blank Crafty workspace.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    import_parser = subparsers.add_parser("import")
    import_parser.add_argument("--manifest", type=Path, required=True)
    import_parser.add_argument("--workspace", type=Path, required=True)
    subparsers.add_parser("self-test")
    args = parser.parse_args()
    if args.command == "self-test":
        self_test()
    else:
        print(import_package(args.manifest, args.workspace))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
