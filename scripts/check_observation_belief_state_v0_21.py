from __future__ import annotations

import json

from runtime.kuuos_observation_belief_state_scenarios_v0_21 import (
    run_observation_belief_state_scenarios,
)


def main() -> None:
    result = run_observation_belief_state_scenarios()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
