#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_native_full_cycle_scenarios_v1_3 import (
    run_native_full_cycle_scenarios,
)


def main() -> int:
    result = run_native_full_cycle_scenarios()
    assert result["status"] == "KUUOS_QI_WORLD_NATIVE_FULL_CYCLE_V1_3_OK"
    assert result["artifact_count"] == 10
    assert result["interface_packet_count"] == 8
    assert all(value is False for value in result["full_cycle_non_authority"].values())
    print("PASS: Qi-WORLD native full OS cycle v1.3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
