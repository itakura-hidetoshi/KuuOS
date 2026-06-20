from __future__ import annotations

import json

from runtime.kuuos_qi_world_successor_licensed_cycle_materialization_scenarios_v2_0 import (
    run_successor_licensed_cycle_materialization_scenarios,
)


def main() -> None:
    print(json.dumps(run_successor_licensed_cycle_materialization_scenarios(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
