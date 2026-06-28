#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_authorized_memory_application_v0_75 import (
    apply_approved_memory_selection,
)
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_leibniz_candidate_validation_v0_71 import validate_leibniz_candidate
from runtime.kuuos_memory_application_receipt_v0_75 import (
    APPLICATION_BLOCKED,
    APPLICATION_COMMITTED,
)
from runtime.kuuos_memory_application_request_v0_75 import (
    build_memory_application_request,
    memory_application_request_digest,
)
from runtime.kuuos_memory_family_evaluation_v0_73 import SELECTED, evaluate_memory_family
from runtime.kuuos_memory_policy_v0_73 import MemoryEvaluationPolicy
from runtime.kuuos_memory_review_identity_v0_74 import (
    EXTERNAL_REVIEWER,
    MemoryReviewerIdentity,
)
from runtime.kuuos_memory_review_receipt_v0_74 import (
    APPROVE_MEMORY_SELECTION,
    REJECT_MEMORY_SELECTION,
)
from runtime.kuuos_memory_review_request_v0_74 import build_memory_review_request
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
    return replace(unsigned, request_digest=memory_application_request_digest(unsigned))


def main() -> int:
    leibniz_inputs = leibniz_fixture()
    calculus, module, _, _, gauge, algebra_samples, sections, _ = leibniz_inputs
    base_connection, base_receipt = validate_leibniz_candidate(*leibniz_inputs)
    assert base_receipt.status == "LEIBNIZ_CONNECTION_CANDIDATE_READY"

    capsule_digest = canonical_digest({"memory_capsule": "application-v075"})
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
    assert selection.status == SELECTED

    review_request = build_memory_review_request(
        "memory-review-v075",
        "kuuos-governance",
        selection,
        (EXTERNAL_REVIEWER,),
        100,
        200,
    )
    reviewer = MemoryReviewerIdentity("reviewer-alpha", EXTERNAL_REVIEWER)
    approved = review_memory_selection(
        review_request,
        selection,
        reviewer,
        APPROVE_MEMORY_SELECTION,
        150,
    )
    assert approved.production_application_authority

    source_connection = NonMarkovMemoryConnection(base_connection, source_kernel)
    state = ProductionMemoryState(
        "production-memory-v075",
        0,
        history.digest,
        module.digest,
        source_kernel,
        source_connection,
    )
    state_digest_before = state.digest
    request = build_memory_application_request(
        "memory-application-v075",
        state,
        approved,
        160,
    )
    updated, committed = apply_approved_memory_selection(
        state,
        request,
        approved,
        selected_connection,
    )
    assert committed.status == APPLICATION_COMMITTED
    assert committed.authority_consumed
    assert committed.atomic_commit
    assert committed.state_write_performed
    assert committed.live_application_performed
    assert committed.permission_expansion_performed is False
    assert committed.rollback_target_replaced is False
    assert committed.before_state_digest == state_digest_before
    assert committed.after_state_digest == updated.digest
    assert committed.after_revision == 1
    assert updated.revision == 1
    assert updated.current_kernel.digest == selection.selected_kernel_digest
    assert updated.current_connection.digest == selection.selected_connection_digest
    assert updated.previous_state_digest == state_digest_before
    assert approved.receipt_digest in updated.consumed_review_receipts
    assert state.digest == state_digest_before

    replayed, replay_receipt = apply_approved_memory_selection(
        updated,
        request,
        approved,
        selected_connection,
    )
    assert replay_receipt.status == APPLICATION_BLOCKED
    assert replayed.digest == updated.digest
    assert "memory_application_review_already_consumed" in replay_receipt.issues
    assert replay_receipt.state_write_performed is False

    stale = signed_request(replace(request, expected_revision=9))
    stale_state, stale_receipt = apply_approved_memory_selection(
        state,
        stale,
        approved,
        selected_connection,
    )
    assert stale_receipt.status == APPLICATION_BLOCKED
    assert stale_state.digest == state.digest
    assert "memory_application_revision_mismatch" in stale_receipt.issues

    expired_request = build_memory_application_request(
        "expired-application-v075",
        state,
        approved,
        201,
    )
    expired_state, expired_receipt = apply_approved_memory_selection(
        state,
        expired_request,
        approved,
        selected_connection,
    )
    assert expired_receipt.status == APPLICATION_BLOCKED
    assert expired_state.digest == state.digest
    assert "memory_application_outside_validity_window" in expired_receipt.issues

    payload_state, payload_receipt = apply_approved_memory_selection(
        state,
        request,
        approved,
        source_connection,
    )
    assert payload_receipt.status == APPLICATION_BLOCKED
    assert payload_state.digest == state.digest
    assert "memory_application_review_selected_kernel_mismatch" in payload_receipt.issues

    rejected = review_memory_selection(
        review_request,
        selection,
        reviewer,
        REJECT_MEMORY_SELECTION,
        150,
    )
    rejected_request = build_memory_application_request(
        "rejected-application-v075",
        state,
        rejected,
        160,
    )
    rejected_state, rejected_receipt = apply_approved_memory_selection(
        state,
        rejected_request,
        rejected,
        selected_connection,
    )
    assert rejected_receipt.status == APPLICATION_BLOCKED
    assert rejected_state.digest == state.digest
    assert "memory_application_review_not_approved" in rejected_receipt.issues
    assert "memory_application_authority_missing" in rejected_receipt.issues

    tampered_request = replace(request, selected_kernel_digest="tampered-kernel")
    tampered_state, tampered_receipt = apply_approved_memory_selection(
        state,
        tampered_request,
        approved,
        selected_connection,
    )
    assert tampered_receipt.status == APPLICATION_BLOCKED
    assert tampered_state.digest == state.digest
    assert "memory_application_request_digest_mismatch" in tampered_receipt.issues

    print(json.dumps({
        "status": "KUUOS_MEMORY_APPLICATION_V0_75_VALIDATED",
        "before_state_digest": state.digest,
        "after_state_digest": updated.digest,
        "application_receipt_digest": committed.receipt_digest,
        "selected_kernel_digest": updated.current_kernel.digest,
        "checks": [
            "approved-atomic-compare-and-swap",
            "revision-increment",
            "one-time-authority-consumption",
            "replay-rejected",
            "stale-revision-rejected",
            "expired-authority-rejected",
            "payload-substitution-rejected",
            "nonapproval-rejected",
            "request-tamper-rejected",
            "source-state-immutable",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
