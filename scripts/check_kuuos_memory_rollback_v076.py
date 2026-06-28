#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_authorized_memory_application_v0_75 import (
    apply_approved_memory_selection,
)
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_leibniz_candidate_validation_v0_71 import validate_leibniz_candidate
from runtime.kuuos_memory_application_request_v0_75 import build_memory_application_request
from runtime.kuuos_memory_family_evaluation_v0_73 import evaluate_memory_family
from runtime.kuuos_memory_policy_v0_73 import MemoryEvaluationPolicy
from runtime.kuuos_memory_review_identity_v0_74 import (
    EXTERNAL_REVIEWER,
    MemoryReviewerIdentity,
)
from runtime.kuuos_memory_review_receipt_v0_74 import APPROVE_MEMORY_SELECTION
from runtime.kuuos_memory_review_request_v0_74 import build_memory_review_request
from runtime.kuuos_memory_rollback_ledger_v0_76 import MemoryRollbackLedger
from runtime.kuuos_memory_rollback_receipt_v0_76 import (
    ROLLBACK_BLOCKED,
    ROLLBACK_COMMITTED,
)
from runtime.kuuos_memory_rollback_request_v0_76 import (
    build_memory_rollback_request,
    memory_rollback_request_digest,
)
from runtime.kuuos_memory_rollback_v0_76 import rollback_memory_commit
from runtime.kuuos_memory_selection_review_v0_74 import review_memory_selection
from runtime.kuuos_nonmarkov_memory_connection_v0_72 import NonMarkovMemoryConnection
from runtime.kuuos_nonmarkov_memory_kernel_v0_72 import (
    FiniteMemoryKernel,
    MemoryKernelTerm,
)
from runtime.kuuos_production_memory_state_v0_75 import ProductionMemoryState
from scripts.check_kuuos_memory_evaluation_v073 import build_family
from scripts.check_kuuos_noncommutative_leibniz_v071 import (
    fixture as leibniz_fixture,
    square_matrix,
)
from scripts.check_kuuos_nonmarkov_memory_v072 import history_fixture


def signed_request(request):
    unsigned = replace(request, request_digest="")
    return replace(unsigned, request_digest=memory_rollback_request_digest(unsigned))


def committed_fixture():
    leibniz_inputs = leibniz_fixture()
    calculus, module, _, _, gauge, algebra_samples, sections, _ = leibniz_inputs
    base_connection, base_receipt = validate_leibniz_candidate(*leibniz_inputs)
    assert base_receipt.status == "LEIBNIZ_CONNECTION_CANDIDATE_READY"

    capsule_digest = canonical_digest({"memory_capsule": "rollback-v076"})
    history = history_fixture(capsule_digest)
    source_kernel = FiniteMemoryKernel(
        module.digest,
        history.digest,
        calculus.direction_labels,
        module.module_rank,
        (
            MemoryKernelTerm(
                "dt",
                1,
                square_matrix(10, {(6, 6): 0.10, (7, 7): 0.20}),
            ),
        ),
    )
    family, _ = build_family(source_kernel)
    selected_connection, selection = evaluate_memory_family(
        family,
        module,
        calculus,
        base_connection,
        history,
        source_kernel,
        gauge,
        algebra_samples,
        sections,
        10,
        MemoryEvaluationPolicy(require_nonincrease=True),
    )
    review_request = build_memory_review_request(
        "rollback-review-v076",
        "kuuos-governance",
        selection,
        (EXTERNAL_REVIEWER,),
        100,
        200,
    )
    approved = review_memory_selection(
        review_request,
        selection,
        MemoryReviewerIdentity("reviewer-alpha", EXTERNAL_REVIEWER),
        APPROVE_MEMORY_SELECTION,
        150,
    )
    source_state = ProductionMemoryState(
        "production-memory-v076",
        0,
        history.digest,
        module.digest,
        source_kernel,
        NonMarkovMemoryConnection(base_connection, source_kernel),
    )
    application_request = build_memory_application_request(
        "rollback-source-commit-v076",
        source_state,
        approved,
        160,
    )
    committed_state, commit_receipt = apply_approved_memory_selection(
        source_state,
        application_request,
        approved,
        selected_connection,
    )
    return source_state, committed_state, commit_receipt


def main() -> int:
    source_state, committed_state, commit_receipt = committed_fixture()
    ledger = MemoryRollbackLedger("memory-rollback-ledger-v076", 0)
    request = build_memory_rollback_request(
        "memory-rollback-v076",
        committed_state,
        source_state,
        ledger,
        commit_receipt,
        170,
    )
    restored, updated_ledger, receipt = rollback_memory_commit(
        committed_state,
        source_state,
        ledger,
        request,
        commit_receipt,
    )
    assert receipt.status == ROLLBACK_COMMITTED
    assert receipt.atomic_commit
    assert receipt.state_write_performed
    assert receipt.live_application_performed
    assert receipt.permission_expansion_performed is False
    assert receipt.review_authority_reenabled is False
    assert restored.revision == committed_state.revision + 1
    assert restored.current_kernel.digest == source_state.current_kernel.digest
    assert restored.current_connection.digest == source_state.current_connection.digest
    assert restored.digest != source_state.digest
    assert restored.previous_state_digest == committed_state.digest
    assert restored.consumed_review_receipts == committed_state.consumed_review_receipts
    assert updated_ledger.revision == 1
    assert commit_receipt.receipt_digest in updated_ledger.rolled_back_commit_receipts
    assert updated_ledger.previous_ledger_digest == ledger.digest
    assert receipt.after_state_digest == restored.digest
    assert receipt.after_ledger_digest == updated_ledger.digest

    replay_state, replay_ledger, replay_receipt = rollback_memory_commit(
        restored,
        source_state,
        updated_ledger,
        request,
        commit_receipt,
    )
    assert replay_receipt.status == ROLLBACK_BLOCKED
    assert replay_state.digest == restored.digest
    assert replay_ledger.digest == updated_ledger.digest
    assert "memory_rollback_commit_already_rolled_back" in replay_receipt.issues

    stale_request = signed_request(replace(request, expected_ledger_revision=9))
    stale_state, stale_ledger, stale_receipt = rollback_memory_commit(
        committed_state,
        source_state,
        ledger,
        stale_request,
        commit_receipt,
    )
    assert stale_receipt.status == ROLLBACK_BLOCKED
    assert stale_state.digest == committed_state.digest
    assert stale_ledger.digest == ledger.digest
    assert "memory_rollback_ledger_revision_mismatch" in stale_receipt.issues

    snapshot_tamper = replace(source_state, revision=1)
    snapshot_state, _, snapshot_receipt = rollback_memory_commit(
        committed_state,
        snapshot_tamper,
        ledger,
        request,
        commit_receipt,
    )
    assert snapshot_receipt.status == ROLLBACK_BLOCKED
    assert snapshot_state.digest == committed_state.digest
    assert "memory_rollback_snapshot_digest_mismatch" in snapshot_receipt.issues

    receipt_tamper = replace(
        commit_receipt,
        selected_kernel_digest="tampered-selected-kernel",
    )
    tampered_state, _, tampered_receipt = rollback_memory_commit(
        committed_state,
        source_state,
        ledger,
        request,
        receipt_tamper,
    )
    assert tampered_receipt.status == ROLLBACK_BLOCKED
    assert tampered_state.digest == committed_state.digest
    assert "memory_rollback_commit_receipt_digest_mismatch" in tampered_receipt.issues

    early_request = build_memory_rollback_request(
        "early-memory-rollback-v076",
        committed_state,
        source_state,
        ledger,
        commit_receipt,
        159,
    )
    early_state, _, early_receipt = rollback_memory_commit(
        committed_state,
        source_state,
        ledger,
        early_request,
        commit_receipt,
    )
    assert early_receipt.status == ROLLBACK_BLOCKED
    assert early_state.digest == committed_state.digest
    assert "memory_rollback_precedes_commit" in early_receipt.issues

    print(json.dumps({
        "status": "KUUOS_MEMORY_ROLLBACK_V0_76_VALIDATED",
        "commit_receipt_digest": commit_receipt.receipt_digest,
        "restored_state_digest": restored.digest,
        "rollback_ledger_digest": updated_ledger.digest,
        "rollback_receipt_digest": receipt.receipt_digest,
        "checks": [
            "exact-precommit-snapshot-binding",
            "monotonic-revision-compensation",
            "rollback-ledger-consumption",
            "rollback-replay-rejected",
            "stale-ledger-rejected",
            "snapshot-tamper-rejected",
            "commit-receipt-tamper-rejected",
            "precommit-epoch-rejected",
            "review-authority-not-reenabled",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
