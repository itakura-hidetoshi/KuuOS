#!/usr/bin/env python3
from __future__ import annotations

from scripts.check_world_module_category_nimrep_tube_center_bridge_v0_41 import (
    main as check_v041,
)
from scripts.run_kuuos_runtime_full_check_v0_1 import main as run_existing_full_check


def main() -> int:
    if check_v041() != 0:
        return 1
    return run_existing_full_check()


if __name__ == "__main__":
    raise SystemExit(main())
