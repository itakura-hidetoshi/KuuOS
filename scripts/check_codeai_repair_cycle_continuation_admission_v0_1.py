#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import seal
from runtime.kuuos_codeai_repair_cycle_continuation_admission_v0_1 import (
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_repair_cycle_continuation_admission,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_repair_cycle_continuation_admission_v0_1.json"


def main() -> None:
    payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    result = build_codeai_repair_cycle_continuation_admission(
        source_cycle_receipt=payload["source_cycle_receipt"],
        continuation_request=payload["continuation_request"],
        continuation_policy=payload["continuation_policy"],
        budget_ledger=payload["budget_ledger"],
    )
    assert result.status == STATUS_READY, result.issues
    assert result.issues == ()
    assert result.receipt is not None
    receipt = result.receipt
    assert receipt["current_cycle_index"] == 1
    assert receipt["admitted_cycle_index"] == 2
    assert receipt["exactly_one_next_cycle_admitted"] is True
    assert receipt["continuation_admission_authority_granted"] is True
    assert receipt["admission_reusable"] is False
    assert receipt["automatic_next_cycle_started"] is False
    assert receipt["cycle_execution_performed"] is False
    assert receipt["repository_mutation_performed"] is False
    assert receipt["git_ref_changed"] is False
    assert receipt["network_access_performed"] is False
    assert receipt["secret_access_performed"] is False
    assert receipt["remaining_candidate_before_reservation"] == 9
    assert receipt["remaining_candidate_after_reservation"] == 6

    skipped = deepcopy(payload["continuation_request"])
    skipped["requested_next_cycle_index"] = 3
    skipped = seal(skipped, REQUEST_DIGEST_FIELD)
    blocked = build_codeai_repair_cycle_continuation_admission(
        source_cycle_receipt=payload["source_cycle_receipt"],
        continuation_request=skipped,
        continuation_policy=payload["continuation_policy"],
        budget_ledger=payload["budget_ledger"],
    )
    assert blocked.status == STATUS_BLOCKED
    assert "continuation_next_cycle_not_exact_successor" in blocked.issues

    escalated = deepcopy(payload["continuation_policy"])
    escalated["automatic_execution_allowed"] = True
    escalated = seal(escalated, POLICY_DIGEST_FIELD)
    blocked = build_codeai_repair_cycle_continuation_admission(
        source_cycle_receipt=payload["source_cycle_receipt"],
        continuation_request=payload["continuation_request"],
        continuation_policy=escalated,
        budget_ledger=payload["budget_ledger"],
    )
    assert blocked.status == STATUS_BLOCKED
    assert any("automatic_execution_allowed" in issue for issue in blocked.issues)

    print("CodeAI Repair Cycle Continuation Admission v0.1: OK")


if __name__ == "__main__":
    main()
