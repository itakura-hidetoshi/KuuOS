from __future__ import annotations

import json

from runtime.kuuos_event_wakeup_control_resource_scenarios_v0_25 import (
    run_event_wakeup_control_resource_scenarios,
)


def main() -> None:
    print(
        json.dumps(
            run_event_wakeup_control_resource_scenarios(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
