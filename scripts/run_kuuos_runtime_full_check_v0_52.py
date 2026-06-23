#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_world_vacuum_expectation_host_effect_intake_v0_52 import (
    main as check_world_v052,
)
from scripts.run_kuuos_runtime_full_check_v0_51 import main as run_v051_full_check


def main() -> int:
    if check_world_v052() != 0:
        return 1
    return run_v051_full_check()


if __name__ == "__main__":
    raise SystemExit(main())
