from __future__ import annotations

import json

from runtime.kuuos_qi_window_trajectory_scenarios_v0_29 import run_qi_window_trajectory_scenarios


def main() -> None:
    result = run_qi_window_trajectory_scenarios()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
