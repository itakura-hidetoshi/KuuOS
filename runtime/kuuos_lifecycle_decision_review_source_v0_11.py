from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import (
    LifecycleBoundedRequestArtifactV010,
    LifecycleBoundedRequestEvidenceV010,
    LifecycleBoundedRequestPolicyV010,
    LifecycleBoundedRequestSubmissionV010,
)
from runtime.kuuos_lifecycle_request_core_v0_10 import artifact_issues as source_artifact_issues
from runtime.kuuos_lifecycle_source_chain_v0_10 import (
    all_source_digests as prior_source_digests,
    prior_actor_ids as prior_request_actor_ids,
)


def all_source_digests(
    source_request: LifecycleBoundedRequestSubmissionV010,
    source_evidence: LifecycleBoundedRequestEvidenceV010,
    source_policy: LifecycleBoundedRequestPolicyV010,
    source_record: LifecycleBoundedRequestArtifactV010,
    source_args: tuple[Any, ...],
) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    review_request, review_evidence, review_policy, review_record = source_args[:4]
    result = prior_source_digests(
        review_request,
        review_evidence,
        review_policy,
        review_record,
        tuple(source_args[4:]),
    )
    result.update(
        bounded_request=source_request.request_digest,
        bounded_request_evidence=source_evidence.evidence_digest,
        bounded_request_policy=source_policy.policy_digest,
        bounded_request_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_request: LifecycleBoundedRequestSubmissionV010,
    source_evidence: LifecycleBoundedRequestEvidenceV010,
    source_policy: LifecycleBoundedRequestPolicyV010,
    source_record: LifecycleBoundedRequestArtifactV010,
    source_args: tuple[Any, ...],
) -> bool:
    return not source_artifact_issues(
        source_record,
        source_request,
        source_evidence,
        source_policy,
        *source_args,
    )


def prior_actor_ids(
    subject_id: str,
    source_request: LifecycleBoundedRequestSubmissionV010,
    source_args: tuple[Any, ...],
) -> set[str]:
    if len(source_args) < 8:
        raise ValueError("source_argument_count_invalid")
    review_record = source_args[3]
    result = prior_request_actor_ids(subject_id, review_record, tuple(source_args[4:]))
    result.add(source_request.requester_id)
    return result
