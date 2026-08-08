from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
sys.path.insert(0, str(ROOT))

from scripts.sync_project_agents import (  # noqa: E402
    LOADER_MARKER,
    MANAGED_END,
    MANAGED_START,
    PROJECT_END,
    PROJECT_START,
    Target,
    build_managed_block,
    collect_targets,
    render_target,
)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="chief-of-staff-sync-") as folder:
        path = Path(folder) / "AGENTS.md"
        target = Target(path, "example", "operations")
        local_rules = "# Project rules\n\n- Keep the unique build hook."
        managed_v1 = f"{MANAGED_START} version=0.3.1 -->\nold\n{MANAGED_END}"
        current = (
            f"{managed_v1}\n\n{PROJECT_START}\n{local_rules}\n{PROJECT_END}\n"
        )
        config = Path(folder) / "chief-of-staff.json"
        config.write_text(f'{{"release_version":"{VERSION}"}}\n', encoding="utf-8")
        managed_v2 = build_managed_block({"release_version": VERSION}, config)
        updated = render_target(managed_v2, current, target)
        assert managed_v2 in updated
        assert LOADER_MARKER in updated
        assert f"CODEX CHIEF OF STAFF ACTIVE - v{VERSION}" in updated
        assert str(config.resolve()) in updated
        assert local_rules in updated
        assert "old" not in updated
        assert "<!-- SHARED-BEHAVIOR-CONTRACT:START -->" not in updated
        assert updated.count(PROJECT_START) == 1
        assert updated.count(PROJECT_END) == 1

        prefix = "# Local preface\n\n"
        bridge = "\n\n<!-- LOCAL-BRIDGE -->\n\n"
        suffix = "\n\n# Project-local output versioning\n\n- Keep every release.\n"
        current_with_extras = (
            f"{prefix}{managed_v1}{bridge}{PROJECT_START}\n{local_rules}\n"
            f"{PROJECT_END}{suffix}"
        )
        preserved = render_target(managed_v2, current_with_extras, target)
        assert preserved == (
            f"{prefix}{managed_v2}{bridge}{PROJECT_START}\n{local_rules}\n"
            f"{PROJECT_END}{suffix}"
        )

        chief_target = Target(path, "chief-of-staff", "personal")
        legacy = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        migrated = render_target(managed_v2, legacy, chief_target)
        assert migrated.count("<!-- SHARED-BEHAVIOR-CONTRACT:START -->") == 0
        assert "- Project ID: `chief-of-staff`" in migrated

        project_root = Path(folder) / "project"
        work_agents = project_root / "work" / "candidate" / "AGENTS.md"
        work_agents.parent.mkdir(parents=True)
        work_agents.write_text("# Candidate contract\n", encoding="utf-8")
        targets = collect_targets(
            {
                "projects": [
                    {
                        "id": "example",
                        "scope": "operations",
                        "paths": [str(project_root)],
                    }
                ]
            },
            include_global=False,
        )
        assert work_agents.resolve() not in {item.path for item in targets}

    powershell = (ROOT / "install.ps1").read_text(encoding="utf-8")
    shell = (ROOT / "install.sh").read_text(encoding="utf-8")
    for installer in (powershell, shell):
        assert "chief-of-staff@codex-chief-of-staff" in installer
        assert "marketplace\", \"upgrade" not in installer
        assert "marketplace upgrade" not in installer
        assert "ai-sloppy-copy@ai-sloppy-copy" not in installer
        assert "brand-voice-factory@brand-voice-factory" not in installer
        assert "crafty-carousels@crafty-carousels-skill" not in installer

    print(
        "PASS: project sync preserves rules and Codex installers use one Chief."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
