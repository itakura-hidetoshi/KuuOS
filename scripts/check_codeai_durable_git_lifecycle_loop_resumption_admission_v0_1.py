#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_v0_1 import (
    DISPOSITION_ADMITTED,
    DISPOSITION_EVIDENCE_QUARANTINED,
    DISPOSITION_FAILED,
    DISPOSITION_UNAVAILABLE,
    STATUS_READY,
)
from tests.test_kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_v0_1 import (
    run_admission,
)


def main() -> None:
    admitted = run_admission()
    assert admitted.status == STATUS_READY, admitted.issues
    assert admitted.receipt is not None
    assert admitted.resume_input is not None
    assert admitted.receipt["codeai_disposition"] == DISPOSITION_ADMITTED
    assert admitted.receipt["checkpoint_read_verified"] is True
    assert admitted.receipt["resume_input_issued"] is True
    assert admitted.resume_input["future_only"] is True
    assert admitted.resume_input["active_now"] is False
    assert admitted.resume_input["loop_execution_authorized"] is False
    assert admitted.resume_input["git_effect_authorized"] is False
    assert admitted.resume_input["automatic_resumption_authorized"] is False
    assert admitted.receipt["general_git_authority_granted"] is False
    assert admitted.receipt["general_successor_stage_authority_granted"] is False

    unavailable = run_admission(adapter_mode="unavailable")
    assert unavailable.status == STATUS_READY, unavailable.issues
    assert unavailable.receipt is not None
    assert unavailable.receipt["codeai_disposition"] == DISPOSITION_UNAVAILABLE
    assert unavailable.resume_input is None
    assert unavailable.next_registry["resumption_attempt_count"] == 1
    assert unavailable.next_registry["successful_resumption_admission_count"] == 0

    failed = run_admission(adapter_mode="exception")
    assert failed.status == STATUS_READY, failed.issues
    assert failed.receipt is not None
    assert failed.receipt["codeai_disposition"] == DISPOSITION_FAILED
    assert failed.resume_input is None

    quarantined = run_admission(adapter_mode="effect")
    assert quarantined.status == STATUS_READY, quarantined.issues
    assert quarantined.receipt is not None
    assert quarantined.receipt["codeai_disposition"] == DISPOSITION_EVIDENCE_QUARANTINED
    assert quarantined.resume_input is None

    print("CodeAI durable Git lifecycle loop resumption admission v0.1: PASS")
    print("verified_checkpoint_read=true")
    print("resume_input_issued_once=true")
    print("automatic_resumption=false")
    print("general_successor_authority=false")


if __name__ == "__main__":
    main()
