from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.sync_project_agents import (  # noqa: E402
    MANAGED_END,
    MANAGED_START,
    PROJECT_END,
    PROJECT_START,
    Target,
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
        managed_v2 = f"{MANAGED_START} version=0.4.4 -->\nnew\n{MANAGED_END}"
        updated = render_target(managed_v2, current, target)
        assert managed_v2 in updated
        assert local_rules in updated
        assert "old" not in updated
        assert updated.count(PROJECT_START) == 1
        assert updated.count(PROJECT_END) == 1
    print("PASS: project sync replaces only the managed block.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
