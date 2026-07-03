from __future__ import annotations

from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_operation_approval_core_v0_13 import (
    artifact_issues as source_artifact_issues,
)
from runtime.kuuos_lifecycle_operation_approval_source_v0_13 import (
    all_source_digests as prior_source_digests,
    prior_actor_ids as prior_approval_actor_ids,
)
from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import (
    LifecycleOperationApprovalArtifactV013,
    LifecycleOperationApprovalEvidenceV013,
    LifecycleOperationApprovalPolicyV013,
    LifecycleOperationApprovalSubmissionV013,
)


def all_source_digests(
    source_approval: LifecycleOperationApprovalSubmissionV013,
    source_evidence: LifecycleOperationApprovalEvidenceV013,
    source_policy: LifecycleOperationApprovalPolicyV013,
    source_record: LifecycleOperationApprovalArtifactV013,
    source_args: tuple[Any, ...],
) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = prior_source_digests(
        source_args[0],
        source_args[1],
        source_args[2],
        source_args[3],
        tuple(source_args[4:]),
    )
    result.update(
        lifecycle_operation_approval=source_approval.approval_digest,
        lifecycle_operation_approval_evidence=source_evidence.evidence_digest,
        lifecycle_operation_approval_policy=source_policy.policy_digest,
        lifecycle_operation_approval_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_approval: LifecycleOperationApprovalSubmissionV013,
    source_evidence: LifecycleOperationApprovalEvidenceV013,
    source_policy: LifecycleOperationApprovalPolicyV013,
    source_record: LifecycleOperationApprovalArtifactV013,
    source_args: tuple[Any, ...],
) -> bool:
    return not source_artifact_issues(
        source_record,
        source_approval,
        source_evidence,
        source_policy,
        *source_args,
    )


def prior_actor_ids(
    subject_id: str,
    source_approval: LifecycleOperationApprovalSubmissionV013,
    source_args: tuple[Any, ...],
) -> set[str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = prior_approval_actor_ids(
        subject_id,
        source_args[0],
        tuple(source_args[4:]),
    )
    result.update(
        {
            source_approval.requester_id,
            source_approval.source_decision_reviewer_id,
            source_approval.source_authorization_decision_maker_id,
            source_approval.operation_approver_id,
            source_approval.future_operator_id,
        }
    )
    return result


def expected_operation_start_route_digest(
    source_approval: LifecycleOperationApprovalSubmissionV013,
    source_evidence: LifecycleOperationApprovalEvidenceV013,
    source_record: LifecycleOperationApprovalArtifactV013,
) -> str:
    return canonical_digest(
        {
            "source_operation_approval_id": source_approval.operation_approval_id,
            "source_operation_approval_record_digest": source_record.record_digest,
            "approved_future_operator_id": source_approval.future_operator_id,
            "operation_approval_route_digest": source_evidence.operation_approval_route_digest,
            "approved_scope_digest": source_evidence.approved_scope_digest,
            "operation_start_deadline_at_epoch_seconds": (
                source_evidence.operation_start_deadline_at_epoch_seconds
            ),
        }
    )
