#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_adaptive_trace_scenarios_v1_1 import (
    run_adaptive_trace_adapter_scenarios,
)


def main() -> int:
    result = run_adaptive_trace_adapter_scenarios()
    assert result["status"] == "KUUOS_QI_WORLD_ADAPTIVE_TRACE_ADAPTER_V1_1_OK"
    assert result["event_count"] == 10
    assert result["state_count"] == 11
    assert result["os_packet_count"] == 8
    assert all(value is False for value in result["adapter_non_authority"].values())
    print("PASS: Qi-WORLD adaptive trace adapter v1.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
