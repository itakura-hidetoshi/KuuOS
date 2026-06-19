from __future__ import annotations

import json

from runtime.kuuos_adaptive_agent_reference_scenarios_v1_0 import (
    run_reference_architecture,
)


def run_kernel() -> dict:
    return run_reference_architecture()


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
