from __future__ import annotations

import json

from runtime.kuuos_qi_world_cross_cycle_reentry_scenarios_v1_4 import (
    run_cross_cycle_reentry_scenarios,
)


def run_kernel() -> dict:
    return run_cross_cycle_reentry_scenarios()


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
