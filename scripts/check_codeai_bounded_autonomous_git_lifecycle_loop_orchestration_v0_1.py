#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    PHASE_CREATE_PR,
    PHASE_LOCAL_COMMIT,
    PHASE_MARK_PR_READY,
    PHASE_MERGE,
    PHASE_PUSH,
)
from runtime.kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1 import (
    DISPOSITION_COMPLETED,
    DISPOSITION_EFFECT_BUDGET_EXHAUSTED,
    DISPOSITION_EXECUTION_FAILED,
    STATUS_READY,
)
from tests.test_kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1 import (
    Simulation,
    run_loop,
)


def main() -> None:
    completed = run_loop()
    assert completed.status == STATUS_READY, completed.issues
    assert completed.receipt is not None
    assert completed.evidence is not None
    assert completed.receipt["codeai_disposition"] == DISPOSITION_COMPLETED
    assert completed.receipt["effect_count"] == 5
    assert completed.receipt["final_lifecycle_completed"] is True
    assert completed.receipt["final_execution_lease_issued"] is False
    assert [record["effect_phase"] for record in completed.evidence["iteration_records"]] == [
        PHASE_LOCAL_COMMIT,
        PHASE_PUSH,
        PHASE_CREATE_PR,
        PHASE_MARK_PR_READY,
        PHASE_MERGE,
    ]
    assert all(record["delegated_lifecycle_receipt_digest"] for record in completed.evidence["iteration_records"])
    assert completed.receipt["automatic_unbounded_continuation_performed"] is False
    assert completed.receipt["concurrent_effect_leases_executed"] is False
    assert completed.receipt["general_git_authority_granted"] is False
    assert completed.receipt["general_successor_stage_authority_granted"] is False

    bounded = run_loop(max_effects=2)
    assert bounded.status == STATUS_READY, bounded.issues
    assert bounded.receipt is not None
    assert bounded.final_lifecycle_receipt is not None
    assert bounded.receipt["codeai_disposition"] == DISPOSITION_EFFECT_BUDGET_EXHAUSTED
    assert bounded.receipt["effect_count"] == 2
    assert bounded.receipt["final_execution_lease_issued"] is True
    assert bounded.final_lifecycle_receipt["next_effect_phase"] == PHASE_CREATE_PR

    failed_simulation = Simulation()
    failed_simulation.execution_failure_phase = PHASE_PUSH
    failed = run_loop(simulation=failed_simulation)
    assert failed.status == STATUS_READY, failed.issues
    assert failed.receipt is not None
    assert failed.final_lifecycle_receipt is not None
    assert failed.receipt["codeai_disposition"] == DISPOSITION_EXECUTION_FAILED
    assert failed.receipt["effect_count"] == 2
    assert failed.final_lifecycle_receipt["next_effect_phase"] == PHASE_PUSH
    assert failed.receipt["automatic_unbounded_continuation_performed"] is False

    print("CodeAI bounded autonomous Git lifecycle loop orchestration v0.1: PASS")
    print("completed_effect_count=5")
    print("bounded_effect_count=2")
    print("failed_execution_reobserved=true")
    print("unbounded_continuation=false")


if __name__ == "__main__":
    main()
