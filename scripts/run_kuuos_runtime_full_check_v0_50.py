#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_memoryos_world_observe_intake_v0_39 import (
    main as check_memoryos_v039,
)
from scripts.check_world_vacuum_expectation_observation_candidate_v0_50 import (
    main as check_v050,
)
from scripts.run_kuuos_runtime_full_check_v0_49 import main as run_v049_full_check


def main() -> int:
    if check_memoryos_v039() != 0:
        return 1
    if check_v050() != 0:
        return 1
    return run_v049_full_check()


if __name__ == "__main__":
    raise SystemExit(main())
