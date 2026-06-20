#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_indra_transport_request_scenarios_v1_6 import (
    run_indra_transport_request_scenarios,
)


def main() -> int:
    result = run_indra_transport_request_scenarios()
    assert result["status"] == "KUUOS_QI_WORLD_INDRA_TRANSPORT_REQUEST_V1_6_OK"
    assert result["source_patch_id"] != result["target_patch_id"]
    assert result["disposition"] == "EXTERNAL_ANALYTIC_TRANSPORT_RECEIPTS_REQUIRED"
    assert result["runtime_transport_realized"] is False
    assert all(value is False for value in result["request_non_authority"].values())
    print("PASS: Qi-WORLD Indra transport request v1.6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
