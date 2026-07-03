from __future__ import annotations

from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_operation_completion_core_v0_15 import (
    artifact_issues as source_artifact_issues,
)
from runtime.kuuos_lifecycle_operation_completion_source_v0_15 import (
    all_source_digests as prior_source_digests,
)
from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    LifecycleOperationCompletionArtifactV015,
    LifecycleOperationCompletionEvidenceV015,
    LifecycleOperationCompletionPolicyV015,
    LifecycleOperationCompletionSubmissionV015,
)


def all_source_digests(
    source_completion: LifecycleOperationCompletionSubmissionV015,
    source_evidence: LifecycleOperationCompletionEvidenceV015,
    source_policy: LifecycleOperationCompletionPolicyV015,
    source_record: LifecycleOperationCompletionArtifactV015,
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
        lifecycle_operation_completion=source_completion.completion_digest,
        lifecycle_operation_completion_evidence=source_evidence.evidence_digest,
        lifecycle_operation_completion_policy=source_policy.policy_digest,
        lifecycle_operation_completion_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_completion: LifecycleOperationCompletionSubmissionV015,
    source_evidence: LifecycleOperationCompletionEvidenceV015,
    source_policy: LifecycleOperationCompletionPolicyV015,
    source_record: LifecycleOperationCompletionArtifactV015,
    source_args: tuple[Any, ...],
) -> bool:
    return not source_artifact_issues(
        source_record,
        source_completion,
        source_evidence,
        source_policy,
        *source_args,
    )


def prior_actor_ids(
    source_completion: LifecycleOperationCompletionSubmissionV015,
) -> set[str]:
    return {
        source_completion.subject_id,
        source_completion.requester_id,
        source_completion.source_decision_reviewer_id,
        source_completion.source_authorization_decision_maker_id,
        source_completion.source_operation_approver_id,
        source_completion.source_operator_id,
        source_completion.completion_reviewer_id,
    }


def expected_post_operation_review_route_digest(
    source_completion: LifecycleOperationCompletionSubmissionV015,
    source_evidence: LifecycleOperationCompletionEvidenceV015,
    source_record: LifecycleOperationCompletionArtifactV015,
) -> str:
    return canonical_digest(
        {
            "source_operation_completion_id": (
                source_completion.operation_completion_id
            ),
            "source_operation_completion_record_digest": (
                source_record.record_digest
            ),
            "source_completion_reviewer_id": (
                source_completion.completion_reviewer_id
            ),
            "source_operation_completion_route_digest": (
                source_evidence.operation_completion_route_digest
            ),
            "source_operation_execution_result_digest": (
                source_evidence.operation_execution_result_digest
            ),
            "source_target_resource_post_state_digest": (
                source_evidence.target_resource_post_state_digest
            ),
            "source_completed_at_epoch_seconds": (
                source_completion.completed_at_epoch_seconds
            ),
        }
    )
