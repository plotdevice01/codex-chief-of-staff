from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_NAME = "chief-of-staff.json"


def platform_config_path() -> Path:
    if os.environ.get("XDG_CONFIG_HOME"):
        return (
            Path(os.environ["XDG_CONFIG_HOME"])
            / "codex-chief-of-staff"
            / CONFIG_NAME
        )
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return base / "codex-chief-of-staff" / CONFIG_NAME
    return Path.home() / ".config" / "codex-chief-of-staff" / CONFIG_NAME


def default_write_path() -> Path:
    plugin_data = os.environ.get("PLUGIN_DATA") or os.environ.get(
        "CLAUDE_PLUGIN_DATA"
    )
    return Path(plugin_data) / CONFIG_NAME if plugin_data else platform_config_path()


def candidate_paths(explicit: str | Path | None = None) -> list[Path]:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    if os.environ.get("CHIEF_OF_STAFF_CONFIG"):
        candidates.append(Path(os.environ["CHIEF_OF_STAFF_CONFIG"]).expanduser())
    candidates.extend((Path.cwd() / CONFIG_NAME, ROOT / CONFIG_NAME))
    plugin_data = os.environ.get("PLUGIN_DATA") or os.environ.get(
        "CLAUDE_PLUGIN_DATA"
    )
    if plugin_data:
        candidates.append(Path(plugin_data) / CONFIG_NAME)
    candidates.append(platform_config_path())

    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        key = os.path.normcase(str(resolved))
        if key not in seen:
            seen.add(key)
            unique.append(resolved)
    return unique


def resolve_config_path(
    explicit: str | Path | None = None, *, require_exists: bool = True
) -> Path:
    candidates = candidate_paths(explicit)
    if require_exists:
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        searched = "\n".join(f"- {path}" for path in candidates)
        raise FileNotFoundError(f"No {CONFIG_NAME} found. Searched:\n{searched}")
    return candidates[0] if explicit else default_write_path().resolve()
