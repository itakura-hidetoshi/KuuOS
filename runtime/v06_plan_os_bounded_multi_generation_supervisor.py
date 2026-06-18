from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_plan_os_multigeneration_scenarios_v0_6 import (
    run_primary_store_scenario,
    verify_decision_matrix,
)


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v06-") as temporary:
        state, store = run_primary_store_scenario(Path(temporary))
        decisions = verify_decision_matrix()
        result = {
            "status": "PLAN_OS_BOUNDED_MULTI_GENERATION_SUPERVISOR_V0_6_OK",
            "completed_generations": state["completed_generations"],
            "current_cycle_index": state["current_cycle_index"],
            "terminal_status": state["status"],
            "terminal_reason": state["terminal_reason"],
            "next_generation_authorized": state["next_generation_authorized"],
            "ledger_commits": store.ledger_commit_count(),
            "tested_decisions": decisions,
            "recovered_state_digest": state[
                "multi_generation_supervisor_state_digest"
            ],
        }
    from runtime.v07_plan_os_external_resume_handover_reentry import (
        run_kernel as run_next,
    )

    next_result = run_next()
    if next_result.get("status") != "PLAN_OS_EXTERNAL_RESUME_HANDOVER_REENTRY_V0_7_OK":
        raise AssertionError(next_result)
    return result


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
