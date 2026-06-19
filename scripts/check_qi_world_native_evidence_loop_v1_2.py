#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_native_evidence_loop_scenarios_v1_2 import (
    run_native_evidence_loop_scenarios,
)


def main() -> int:
    result = run_native_evidence_loop_scenarios()
    assert result["status"] == "KUUOS_QI_WORLD_NATIVE_EVIDENCE_LOOP_V1_2_OK"
    assert result["native_state_count"] == 4
    assert result["interface_packet_count"] == 8
    assert all(value is False for value in result["native_non_authority"].values())
    print("PASS: Qi-WORLD native evidence loop v1.2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
