from __future__ import annotations

import json

from runtime.kuuos_qi_world_concrete_third_licensed_cycle_materialization_public_scenarios_v2_2 import run_concrete_third_licensed_cycle_materialization_scenarios


def main() -> None:
    result = run_concrete_third_licensed_cycle_materialization_scenarios()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
