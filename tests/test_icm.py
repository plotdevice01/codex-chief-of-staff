from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_icm import estimate_tokens, validate_icm, validate_workspace


ENTRY = """# Example workspace

Read CONTEXT.md to route the current task.
"""
ROOT_CONTEXT = """# Example context

| Need | Read next |
|---|---|
| Start | stages/01_research/CONTEXT.md |
"""
CONTRACT = """# {name}

## Inputs
- Working: {working}
- Reference: references/rules.md

## Process
1. Read the named inputs.
2. Write the named output.

## Outputs
- result.md -> output/

## Human check
Read the result and confirm it matches the input.
"""


def build_fixture(root: Path) -> None:
    (root / "AGENTS.md").write_text(ENTRY, encoding="utf-8")
    (root / "CONTEXT.md").write_text(ROOT_CONTEXT, encoding="utf-8")
    for index, name in ((1, "research"), (2, "draft")):
        stage = root / "stages" / f"{index:02d}_{name}"
        (stage / "references").mkdir(parents=True)
        (stage / "output").mkdir()
        (stage / "references" / "rules.md").write_text("# Rules\n", encoding="utf-8")
        working = "source.md" if index == 1 else "../01_research/output/result.md"
        (stage / "CONTEXT.md").write_text(
            CONTRACT.format(name=name, working=working), encoding="utf-8"
        )


def main() -> int:
    errors, metrics = validate_icm()
    assert not errors, "\n".join(errors)
    assert metrics == {"forms": 5, "invariants": 10, "release_stages": 4}

    with TemporaryDirectory() as temporary:
        workspace = Path(temporary)
        build_fixture(workspace)
        assert not validate_workspace(workspace)

        contract = workspace / "stages" / "02_draft" / "CONTEXT.md"
        contract.write_text(CONTRACT.split("## Human check")[0], encoding="utf-8")
        failures = validate_workspace(workspace)
        assert any("## Human check" in failure for failure in failures)

    assert estimate_tokens(["word " * 1500]) == 2000
    assert 2000 <= estimate_tokens(["word " * 3000]) <= 8000
    print("PASS: ICM repository, cold-walk fixture, failure path, and token budget validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
