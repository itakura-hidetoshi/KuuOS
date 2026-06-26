#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
from collections.abc import Callable

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_world_four_great_phase_transition_declaration_v0_60 import (
    main as check_v060,
)
from scripts.check_world_four_great_phase_dynamics_v0_59 import main as check_v059
from scripts.check_world_kuu_vacuum_araki_hessian_physical_realization_v0_56 import (
    main as check_v056,
)
from scripts.run_kuuos_runtime_full_check_v0_55 import main as run_v055_full_check


def run_check(check: Callable[[], int], name: str) -> int:
    try:
        result = check()
    except Exception as exc:
        print(f"[FAIL] {name}: {exc}", file=sys.stderr)
        return 1
    if result != 0:
        print(f"[FAIL] {name}: exit code {result}", file=sys.stderr)
        return 1
    print(f"[PASS] {name}")
    return 0


def main() -> int:
    checks: tuple[tuple[Callable[[], int], str], ...] = (
        (check_v060, "WORLD v0.60 phase-transition declaration"),
        (check_v059, "WORLD v0.59 four-great phase dynamics"),
        (check_v056, "WORLD v0.56 Araki Hessian physical realization"),
        (run_v055_full_check, "KuuOS cumulative runtime check through WORLD v0.55"),
    )
    for check, name in checks:
        if run_check(check, name) != 0:
            return 1
    print("KuuOS cumulative runtime full check through WORLD v0.60 passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
