from __future__ import annotations

import json

from runtime.kuuos_os_qi_closed_loop_scenarios_v0_24 import (
    run_os_qi_closed_loop_scenarios,
)


if __name__ == "__main__":
    print(json.dumps(run_os_qi_closed_loop_scenarios(), ensure_ascii=False, indent=2, sort_keys=True))
