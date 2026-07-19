#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_v0_1 import (
    DISPOSITION_CONFLICT,
    DISPOSITION_EVIDENCE_QUARANTINED,
    DISPOSITION_FAILED,
    DISPOSITION_PERSISTED,
    STATUS_READY,
)
from tests.test_kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_v0_1 import (
    adapter_result,
    run_persistence,
)


def main() -> None:
    persisted = run_persistence()
    assert persisted.status == STATUS_READY, persisted.issues
    assert persisted.receipt is not None
    assert persisted.evidence is not None
    assert persisted.next_registry is not None
    assert persisted.next_store_state is not None
    assert persisted.receipt["codeai_disposition"] == DISPOSITION_PERSISTED
    assert persisted.receipt["checkpoint_persisted"] is True
    assert persisted.receipt["resume_input_issued"] is False
    assert persisted.receipt["automatic_resumption_performed"] is False
    assert persisted.receipt["general_git_authority_granted"] is False
    assert persisted.receipt["general_successor_stage_authority_granted"] is False
    assert persisted.next_registry["persistence_attempt_count"] == 1
    assert persisted.next_registry["successful_persistence_count"] == 1
    assert persisted.next_store_state["store_revision"] == 1

    conflict = run_persistence(
        adapter=lambda invocation: adapter_result(invocation, status="conflict")
    )
    assert conflict.status == STATUS_READY, conflict.issues
    assert conflict.receipt["codeai_disposition"] == DISPOSITION_CONFLICT
    assert conflict.next_store_state["store_revision"] == 0

    failed = run_persistence(
        adapter=lambda invocation: adapter_result(invocation, status="failed")
    )
    assert failed.status == STATUS_READY, failed.issues
    assert failed.receipt["codeai_disposition"] == DISPOSITION_FAILED

    quarantined = run_persistence(adapter=lambda _: "not-a-mapping")
    assert quarantined.status == STATUS_READY, quarantined.issues
    assert quarantined.receipt["codeai_disposition"] == DISPOSITION_EVIDENCE_QUARANTINED

    print("CodeAI durable Git lifecycle loop checkpoint persistence v0.1: PASS")
    print("checkpoint_persisted=true")
    print("compare_and_swap_conflict_separate=true")
    print("adapter_failure_separate=true")
    print("malformed_evidence_quarantined=true")
    print("resume_input_issued=false")
    print("automatic_resumption=false")


if __name__ == "__main__":
    main()
