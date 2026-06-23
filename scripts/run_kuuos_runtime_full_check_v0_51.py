#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_verifyos_vacuum_expectation_commit_verification_receipt_v0_3 import (
    main as check_verifyos_v03,
)
from scripts.check_observeos_vacuum_expectation_intake_commit_receipt_v0_3 import (
    main as check_observeos_v03,
)
from scripts.check_world_vacuum_expectation_observeos_evidence_intake_v0_51 import (
    main as check_v051,
)
from scripts.run_kuuos_runtime_full_check_v0_50 import main as run_v050_full_check


def main() -> int:
    if check_verifyos_v03() != 0:
        return 1
    if check_observeos_v03() != 0:
        return 1
    if check_v051() != 0:
        return 1
    return run_v050_full_check()


if __name__ == "__main__":
    raise SystemExit(main())
