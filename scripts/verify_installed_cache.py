from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

try:
    from .config_paths import ROOT, resolve_config_path
    from .package_files import canonical_bytes, copied_files
    from .sync_project_agents import MANAGED_START, collect_targets, load_config
except ImportError:
    from config_paths import ROOT, resolve_config_path
    from package_files import canonical_bytes, copied_files
    from sync_project_agents import MANAGED_START, collect_targets, load_config


VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def default_cache_root() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "plugins" / "cache" / "codex-chief-of-staff" / "chief-of-staff"


def resolve_codex_cli() -> Path | None:
    if os.name == "nt" and os.environ.get("LOCALAPPDATA"):
        base = Path(os.environ["LOCALAPPDATA"]) / "OpenAI" / "Codex" / "bin"
        candidates = sorted(
            base.glob("*/codex.exe"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        ) if base.is_dir() else []
        if candidates:
            return candidates[0]
    command = shutil.which("codex")
    return Path(command) if command else None


def plugin_state() -> dict:
    cli = resolve_codex_cli()
    if not cli:
        return {"verified": False, "error": "Codex CLI not found"}
    try:
        completed = subprocess.run(
            [str(cli), "plugin", "list", "--json"],
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(completed.stdout)
        matches = [
            item for item in payload.get("installed", [])
            if item.get("pluginId") == "chief-of-staff@codex-chief-of-staff"
        ]
        if len(matches) != 1:
            return {"verified": False, "error": f"Expected one installed Chief; found {len(matches)}"}
        item = matches[0]
        return {
            "verified": True,
            "plugin_id": item.get("pluginId"),
            "version": item.get("version"),
            "installed": item.get("installed"),
            "enabled": item.get("enabled"),
            "source": item.get("source", {}).get("path"),
            "marketplace_source": item.get("marketplaceSource", {}).get("source"),
            "cli": str(cli),
        }
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return {"verified": False, "error": str(exc), "cli": str(cli)}


def expected_files() -> dict[str, str]:
    files = {
        path.relative_to(ROOT).as_posix(): digest(canonical_bytes(path))
        for path in copied_files()
    }
    sop = ROOT / "docs" / "Codex Chief of Staff - Installation and SOP.docx"
    files[sop.name] = digest(sop.read_bytes())
    return files


def loader_status(config_path: Path) -> tuple[int, list[str]]:
    config = load_config(config_path)
    marker = f"{MANAGED_START} version={VERSION} mode=hook-loader -->"
    drift: list[str] = []
    targets = collect_targets(config, include_global=True)
    for target in targets:
        if not target.path.is_file() or marker not in target.path.read_text(encoding="utf-8"):
            drift.append(str(target.path))
    return len(targets), drift


def verify(cache_root: Path, config_path: Path) -> dict:
    current = cache_root / VERSION
    expected = expected_files()
    observed = {
        path.relative_to(current).as_posix(): digest(path.read_bytes())
        for path in current.rglob("*")
        if path.is_file()
    } if current.is_dir() else {}
    stale = sorted(
        path.name for path in cache_root.iterdir()
        if path.is_dir() and path.name != VERSION
    ) if cache_root.is_dir() else []
    loader_count, loader_drift = loader_status(config_path)
    state = plugin_state()
    contract = ROOT / "AGENTS.md"
    installed_contract = current / "AGENTS.md"
    return {
        "schema_version": 1,
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "source_version": VERSION,
        "source_root": str(ROOT),
        "cache_root": str(cache_root),
        "active_cache_path": str(current),
        "active_cache_exists": current.is_dir(),
        "stale_cache_versions": stale,
        "expected_files": len(expected),
        "observed_files": len(observed),
        "missing_files": sorted(set(expected) - set(observed)),
        "unexpected_files": sorted(set(observed) - set(expected)),
        "differing_files": sorted(
            name for name in set(expected) & set(observed)
            if expected[name] != observed[name]
        ),
        "project_loader_targets": loader_count,
        "project_loader_drift": loader_drift,
        "canonical_contract_sha256": digest(contract.read_bytes()),
        "installed_contract_sha256": digest(installed_contract.read_bytes()) if installed_contract.is_file() else None,
        "plugin_state": state,
    }


def write_visual(path: Path, result: dict) -> None:
    ok = result.get("status") == "pass"
    state = result.get("plugin_state", {})
    rows = [
        ("Source version", result["source_version"]),
        ("Codex plugin", f"{state.get('version', 'unverified')} | installed={state.get('installed')} | enabled={state.get('enabled')}"),
        ("Active cache", result["active_cache_path"]),
        ("Stale caches", str(len(result["stale_cache_versions"]))),
        ("Canonical parity", f"{result['expected_files']} files | missing {len(result['missing_files'])} | different {len(result['differing_files'])} | unexpected {len(result['unexpected_files'])}"),
        ("Contract SHA-256", str(result["canonical_contract_sha256"])),
        ("Project loaders", f"{result['project_loader_targets']} targets | drift {len(result['project_loader_drift'])}"),
        ("Plugin source", str(state.get("source", "unverified"))),
        ("Verified UTC", result["verified_at"]),
    ]
    width, height = 1500, 770
    accent = "#2A9D8F" if ok else "#C2413B"
    status = "PASS" if ok else "FAIL"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1500" height="770" rx="28" fill="#F8FAFC"/>',
        '<rect x="0" y="0" width="1500" height="132" rx="28" fill="#14213D"/>',
        '<rect x="0" y="104" width="1500" height="28" fill="#14213D"/>',
        '<text x="60" y="62" font-family="Segoe UI,Arial" font-size="34" font-weight="700" fill="#FFFFFF">Chief installed-cache proof</text>',
        f'<text x="60" y="105" font-family="Consolas,monospace" font-size="25" fill="#DCE7F3">v{html.escape(result["source_version"])} canonical rebuild</text>',
        f'<rect x="1240" y="36" width="190" height="62" rx="31" fill="{accent}"/>',
        f'<text x="1335" y="78" text-anchor="middle" font-family="Segoe UI,Arial" font-size="28" font-weight="700" fill="#FFFFFF">{status}</text>',
    ]
    y = 185
    for index, (label, value) in enumerate(rows):
        if index % 2 == 0:
            parts.append(f'<rect x="42" y="{y - 34}" width="1416" height="56" rx="8" fill="#E8F4F2"/>')
        parts.append(f'<text x="66" y="{y}" font-family="Segoe UI,Arial" font-size="21" font-weight="700" fill="#14213D">{html.escape(label)}</text>')
        display = html.escape(value)
        if len(value) > 105:
            display = html.escape(value[:102] + "...")
        parts.append(f'<text x="330" y="{y}" font-family="Consolas,monospace" font-size="18" fill="#263445">{display}</text>')
        y += 64
    parts.append('</svg>')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prove installed Chief cache and project loaders match canonical source."
    )
    parser.add_argument("--cache-root", type=Path, default=default_cache_root())
    parser.add_argument("--config")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--visual", type=Path)
    parser.add_argument("--require-only-current", action="store_true")
    parser.add_argument("--require-plugin-state", action="store_true")
    args = parser.parse_args()
    config_path = resolve_config_path(args.config)
    result = verify(args.cache_root.expanduser().resolve(), config_path)
    errors = []
    if not result["active_cache_exists"]:
        errors.append("active cache path is missing")
    for key in ("missing_files", "unexpected_files", "differing_files", "project_loader_drift"):
        if result[key]:
            errors.append(f"{key}={len(result[key])}")
    if args.require_only_current and result["stale_cache_versions"]:
        errors.append(f"stale_cache_versions={len(result['stale_cache_versions'])}")
    state = result["plugin_state"]
    if args.require_plugin_state and (
        not state.get("verified")
        or state.get("version") != VERSION
        or state.get("installed") is not True
        or state.get("enabled") is not True
    ):
        errors.append("plugin_state is not installed, enabled, and version-matched")
    if result["canonical_contract_sha256"] != result["installed_contract_sha256"]:
        errors.append("installed AGENTS.md hash differs from canonical source")
    result["status"] = "pass" if not errors else "fail"
    result["errors"] = errors
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.visual:
        write_visual(args.visual, result)
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
