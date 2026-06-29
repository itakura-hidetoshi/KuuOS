#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_successor_cycle_materialization_public_scenarios_v2_0 import (
    run_successor_cycle_materialization_scenarios,
)


def main() -> int:
    result = run_successor_cycle_materialization_scenarios()
    expected = "KUUOS_QI_WORLD_SUCCESSOR_CYCLE_MATERIALIZATION_V2_0_OK"
    if result.get("status") != expected:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
