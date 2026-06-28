#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_leibniz_candidate_validation_v0_71 import validate_leibniz_candidate
from runtime.kuuos_memory_family_evaluation_v0_73 import SELECTED, evaluate_memory_family
from runtime.kuuos_memory_policy_v0_73 import MemoryEvaluationPolicy
from runtime.kuuos_memory_review_identity_v0_74 import (
    EXTERNAL_REVIEWER,
    GOVERNANCE_REVIEWER,
    MemoryReviewerIdentity,
)
from runtime.kuuos_memory_review_receipt_v0_74 import (
    APPROVE_MEMORY_SELECTION,
    REJECT_MEMORY_SELECTION,
    REQUEST_REEVALUATION,
)
from runtime.kuuos_memory_review_request_v0_74 import (
    build_memory_review_request,
    memory_review_request_digest,
)
from runtime.kuuos_memory_selection_review_v0_74 import (
    REVIEW_APPROVED,
    REVIEW_BLOCKED,
    REVIEW_REEVALUATION_REQUESTED,
    REVIEW_REJECTED,
    review_memory_selection,
)
from runtime.kuuos_nonmarkov_memory_kernel_v0_72 import (
    FiniteMemoryKernel,
    MemoryKernelTerm,
)
from scripts.check_kuuos_memory_evaluation_v073 import build_family
from scripts.check_kuuos_noncommutative_leibniz_v071 import (
    fixture as leibniz_fixture,
    square_matrix,
)
from scripts.check_kuuos_nonmarkov_memory_v072 import history_fixture


def main() -> int:
    leibniz_inputs = leibniz_fixture()
    calculus, module, _, _, gauge, algebra_samples, sections, _ = leibniz_inputs
    base_connection, base_receipt = validate_leibniz_candidate(*leibniz_inputs)
    assert base_receipt.status == "LEIBNIZ_CONNECTION_CANDIDATE_READY"

    capsule_digest = canonical_digest({"memory_capsule": "review-v074"})
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
    _, selection = evaluate_memory_family(
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

    request = build_memory_review_request(
        "memory-review-v074",
        "kuuos-governance",
        selection,
        (EXTERNAL_REVIEWER,),
        100,
        200,
    )
    reviewer = MemoryReviewerIdentity("reviewer-alpha", EXTERNAL_REVIEWER)
    approved = review_memory_selection(
        request,
        selection,
        reviewer,
        APPROVE_MEMORY_SELECTION,
        150,
    )
    assert approved.status == REVIEW_APPROVED
    assert approved.production_application_authority
    assert approved.writes_enabled is False
    assert approved.live_application_enabled is False
    assert approved.permission_expansion_enabled is False
    assert approved.rollback_target_replacement_enabled is False
    assert approved.rollback_target_digest == selection.source_kernel_digest
    assert approved.selected_kernel_digest == selection.selected_kernel_digest
    assert approved.receipt_digest
    assert not approved.issues

    rejected = review_memory_selection(
        request,
        selection,
        reviewer,
        REJECT_MEMORY_SELECTION,
        150,
    )
    assert rejected.status == REVIEW_REJECTED
    assert rejected.production_application_authority is False

    reevaluation = review_memory_selection(
        request,
        selection,
        reviewer,
        REQUEST_REEVALUATION,
        150,
    )
    assert reevaluation.status == REVIEW_REEVALUATION_REQUESTED
    assert reevaluation.production_application_authority is False

    expired = review_memory_selection(
        request,
        selection,
        reviewer,
        APPROVE_MEMORY_SELECTION,
        201,
    )
    assert expired.status == REVIEW_BLOCKED
    assert expired.production_application_authority is False
    assert "memory_review_outside_validity_window" in expired.issues

    request_tamper = replace(request, selected_kernel_digest=canonical_digest({"tamper": 1}))
    tampered = review_memory_selection(
        request_tamper,
        selection,
        reviewer,
        APPROVE_MEMORY_SELECTION,
        150,
    )
    assert tampered.status == REVIEW_BLOCKED
    assert "memory_review_request_digest_mismatch" in tampered.issues
    assert "memory_review_selected_kernel_binding_mismatch" in tampered.issues

    selection_tamper = replace(
        selection,
        selected_kernel_digest=canonical_digest({"tamper": 2}),
    )
    tampered_selection = review_memory_selection(
        request,
        selection_tamper,
        reviewer,
        APPROVE_MEMORY_SELECTION,
        150,
    )
    assert tampered_selection.status == REVIEW_BLOCKED
    assert "memory_selection_record_digest_mismatch" in tampered_selection.issues

    governance_reviewer = MemoryReviewerIdentity(
        "reviewer-governance",
        GOVERNANCE_REVIEWER,
    )
    scope_blocked = review_memory_selection(
        request,
        selection,
        governance_reviewer,
        APPROVE_MEMORY_SELECTION,
        150,
    )
    assert scope_blocked.status == REVIEW_BLOCKED
    assert "memory_review_reviewer_scope_mismatch" in scope_blocked.issues

    rollback_tamper = replace(
        request,
        rollback_target_digest=canonical_digest({"rollback": "replacement"}),
        request_digest="",
    )
    rollback_tamper = replace(
        rollback_tamper,
        request_digest=memory_review_request_digest(rollback_tamper),
    )
    rollback_blocked = review_memory_selection(
        rollback_tamper,
        selection,
        reviewer,
        APPROVE_MEMORY_SELECTION,
        150,
    )
    assert rollback_blocked.status == REVIEW_BLOCKED
    assert "memory_review_rollback_target_mismatch" in rollback_blocked.issues

    print(json.dumps({
        "status": "KUUOS_MEMORY_REVIEW_V0_74_VALIDATED",
        "request_digest": request.request_digest,
        "selection_record_digest": selection.record_digest,
        "approved_receipt_digest": approved.receipt_digest,
        "selected_kernel_digest": approved.selected_kernel_digest,
        "checks": [
            "exact-selection-binding",
            "reviewer-identity-and-class-binding",
            "finite-validity-window",
            "approve-grants-production-application-authority",
            "reject-and-reevaluation-deny-authority",
            "request-and-selection-tamper-rejected",
            "reviewer-scope-widening-rejected",
            "rollback-target-replacement-rejected",
            "no-immediate-write-or-live-application",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
