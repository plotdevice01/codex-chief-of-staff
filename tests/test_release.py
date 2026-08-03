from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_repository import (  # noqa: E402
    model_acceptance_release_status,
    validate_model_acceptance,
    validate_release_waiver,
)


def main() -> int:
    evidence = json.loads(
        (ROOT / "tests" / "model-acceptance.json").read_text(encoding="utf-8")
    )
    assert not validate_model_acceptance(require_pass=True)
    assert model_acceptance_release_status(evidence) == "pass_with_waiver"

    without_waiver = copy.deepcopy(evidence)
    without_waiver.pop("release_waiver")
    assert model_acceptance_release_status(without_waiver) == "candidate"

    failed = copy.deepcopy(evidence)
    failed["models"]["gpt-5.6-terra"]["status"] = "fail"
    assert model_acceptance_release_status(failed) == "candidate"
    _, errors = validate_release_waiver(failed)
    assert errors

    print("PASS: release waiver is version-bound and covers only pending model checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
