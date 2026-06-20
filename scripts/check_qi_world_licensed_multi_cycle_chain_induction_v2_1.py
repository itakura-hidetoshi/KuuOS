from __future__ import annotations

import json

from runtime.kuuos_qi_world_licensed_multi_cycle_chain_induction_scenarios_v2_1 import (
    run_licensed_multi_cycle_chain_induction_scenarios,
)


def main() -> None:
    print(
        json.dumps(
            run_licensed_multi_cycle_chain_induction_scenarios(),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
