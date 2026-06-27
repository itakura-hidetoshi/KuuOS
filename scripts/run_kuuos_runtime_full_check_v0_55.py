#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_modular_evolution_mesh_v0_1 import (
    main as check_modular_evolution_mesh_v0_1,
)
from scripts.check_world_kuu_vacuum_information_geometry_v0_55 import (
    main as check_v055,
)
from scripts.run_kuuos_runtime_full_check_v0_54 import main as run_v054_full_check


def main() -> int:
    if check_modular_evolution_mesh_v0_1() != 0:
        return 1
    if check_v055() != 0:
        return 1
    return run_v054_full_check()


if __name__ == "__main__":
    raise SystemExit(main())
