from __future__ import annotations

from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_operation_start_core_v0_14 import (
    artifact_issues as source_artifact_issues,
)
from runtime.kuuos_lifecycle_operation_start_source_v0_14 import (
    all_source_digests as prior_source_digests,
)
from runtime.kuuos_lifecycle_operation_start_types_v0_14 import (
    LifecycleOperationStartArtifactV014,
    LifecycleOperationStartEvidenceV014,
    LifecycleOperationStartPolicyV014,
    LifecycleOperationStartSubmissionV014,
)


def all_source_digests(
    source_start: LifecycleOperationStartSubmissionV014,
    source_evidence: LifecycleOperationStartEvidenceV014,
    source_policy: LifecycleOperationStartPolicyV014,
    source_record: LifecycleOperationStartArtifactV014,
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
        lifecycle_operation_start=source_start.start_digest,
        lifecycle_operation_start_evidence=source_evidence.evidence_digest,
        lifecycle_operation_start_policy=source_policy.policy_digest,
        lifecycle_operation_start_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_start: LifecycleOperationStartSubmissionV014,
    source_evidence: LifecycleOperationStartEvidenceV014,
    source_policy: LifecycleOperationStartPolicyV014,
    source_record: LifecycleOperationStartArtifactV014,
    source_args: tuple[Any, ...],
) -> bool:
    return not source_artifact_issues(
        source_record,
        source_start,
        source_evidence,
        source_policy,
        *source_args,
    )


def prior_actor_ids(
    source_start: LifecycleOperationStartSubmissionV014,
) -> set[str]:
    return {
        source_start.subject_id,
        source_start.requester_id,
        source_start.source_decision_reviewer_id,
        source_start.source_authorization_decision_maker_id,
        source_start.source_operation_approver_id,
        source_start.operator_id,
    }


def expected_operation_completion_route_digest(
    source_start: LifecycleOperationStartSubmissionV014,
    source_evidence: LifecycleOperationStartEvidenceV014,
    source_record: LifecycleOperationStartArtifactV014,
) -> str:
    return canonical_digest(
        {
            "source_operation_start_id": source_start.operation_start_id,
            "source_operation_start_record_digest": source_record.record_digest,
            "source_operator_id": source_start.operator_id,
            "operation_start_route_digest": source_evidence.operation_start_route_digest,
            "approved_scope_digest": source_evidence.approved_scope_digest,
            "operation_completion_deadline_at_epoch_seconds": (
                source_start.operation_completion_deadline_at_epoch_seconds
            ),
        }
    )
