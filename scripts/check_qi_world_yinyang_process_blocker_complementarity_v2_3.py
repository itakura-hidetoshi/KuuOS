#!/usr/bin/env python3
from __future__ import annotations

import json

from runtime.kuuos_qi_world_yinyang_process_blocker_complementarity_scenarios_v2_3 import (
    run_yinyang_process_blocker_scenarios,
)
from runtime.kuuos_qi_world_yinyang_process_blocker_complementarity_v2_3 import STATUS_OK


def main() -> int:
    result = run_yinyang_process_blocker_scenarios()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("status") == STATUS_OK else 1


if __name__ == "__main__":
    raise SystemExit(main())
