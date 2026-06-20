#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_world_araki_petz_quantum_information_geometry_v0_44 import (
    main as check_v044,
)
from scripts.run_kuuos_runtime_full_check_v0_43 import main as run_v043_full_check


def main() -> int:
    if check_v044() != 0:
        return 1
    return run_v043_full_check()


if __name__ == "__main__":
    raise SystemExit(main())
