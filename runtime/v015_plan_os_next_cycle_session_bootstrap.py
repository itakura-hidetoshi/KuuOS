from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_next_cycle_session_scenarios_v0_15 import (
    run_session_bootstrap,
)


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v015-") as temporary:
        session = run_session_bootstrap(Path(temporary))
        bootstrap = session["plan_bootstrap_state"]
        return {
            "status": "PLAN_OS_NEXT_CYCLE_SESSION_BOOTSTRAP_V0_15_OK",
            "session_status": session["status"],
            "mission_cycle_index": session["mission_cycle_index"],
            "mission_cycle_phase": session["mission_cycle_phase"],
            "plan_phase": bootstrap["current_phase"],
            "event_index": bootstrap["event_index"],
            "step_count": len(bootstrap["steps"]),
            "lease_clock_count": len(session["lease_clocks"]),
            "lease_monitor_started_at_ms": session[
                "lease_monitor_started_at_ms"
            ],
            "lease_monitor_deadline_ms": session[
                "lease_monitor_deadline_ms"
            ],
            "activation_consumed": session["activation_consumed"],
            "session_single_use": session["session_single_use"],
            "execution_granted": session["execution_granted"],
            "host_license_granted": session["host_license_granted"],
            "memory_overwrite": session["memory_overwrite"],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
