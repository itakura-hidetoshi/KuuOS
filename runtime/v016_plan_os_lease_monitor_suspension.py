from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_lease_monitor_scenarios_v0_16 import run_lease_monitor


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v016-") as temporary:
        state = run_lease_monitor(Path(temporary))
        tick = state["latest_tick"]
        return {
            "status": "PLAN_OS_LEASE_MONITOR_SUSPENSION_V0_16_OK",
            "session_status_after": tick["session_status_after"],
            "tick_index": tick["tick_index"],
            "recovery_route": tick["recovery_route"],
            "reason_count": len(tick["suspension_reasons"]),
            "plan_progress_allowed": tick["plan_progress_allowed"],
            "session_suspended": tick["session_suspended"],
            "suspension_terminal": tick["suspension_terminal"],
            "execution_granted": tick["execution_granted"],
            "host_license_granted": tick["host_license_granted"],
            "memory_overwrite": tick["memory_overwrite"],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
