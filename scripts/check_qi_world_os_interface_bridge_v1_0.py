#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v1_0_qi_world_os_interface_bridge import run_kernel


def main() -> int:
    result = run_kernel()
    assert result["status"] == "KUUOS_QI_WORLD_OS_INTERFACE_BRIDGE_V1_0_OK"
    assert result["os_packet_count"] == 8
    assert result["cross_os_relation_count"] == 18
    assert result["same_process_lineage"] is True
    assert result["world_projection_read_only"] is True
    assert result["qi_process_is_temporal_substrate"] is True
    assert result["governance_is_cross_cutting"] is True
    assert result["governance_is_single_stage"] is False
    assert result["exact_world_updated"] is False
    assert all(value is False for value in result["non_authority"].values())
    print("PASS: Qi-WORLD OS interface bridge v1.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
