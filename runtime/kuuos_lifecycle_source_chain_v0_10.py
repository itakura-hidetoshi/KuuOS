from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_review_chain_v0_9 import named_source, source_digests
from runtime.kuuos_lifecycle_review_core_v0_9 import artifact_issues as review_artifact_issues
from runtime.kuuos_lifecycle_review_types_v0_9 import (
    LifecycleReviewArtifactV09,
    LifecycleReviewEvidenceV09,
    LifecycleReviewPolicyV09,
    LifecycleReviewRequestV09,
)


def _value_by_suffix(value: Any, suffix: str) -> Any:
    payload = value.to_dict()
    matches = [item for name, item in payload.items() if name.endswith(suffix)]
    if len(matches) != 1:
        raise ValueError(f"source_field_resolution_invalid:{suffix}")
    return matches[0]


def source_authority(record: LifecycleReviewArtifactV09) -> str:
    return _value_by_suffix(record, "authority_id")


def source_operator(record: LifecycleReviewArtifactV09) -> str:
    return _value_by_suffix(record, "operator_id")


def source_scope(evidence: LifecycleReviewEvidenceV09, suffix: str) -> Any:
    return _value_by_suffix(evidence, suffix)


def all_source_digests(
    review_request: LifecycleReviewRequestV09,
    review_evidence: LifecycleReviewEvidenceV09,
    review_policy: LifecycleReviewPolicyV09,
    review_record: LifecycleReviewArtifactV09,
    source_args: tuple[Any, ...],
) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    preparation_request, preparation_evidence, preparation_policy, preparation_record = (
        source_args[:4]
    )
    result = source_digests(
        preparation_request,
        preparation_evidence,
        preparation_policy,
        preparation_record,
        tuple(source_args[4:]),
    )
    result.update(
        review_request=review_request.request_digest,
        review_evidence=review_evidence.evidence_digest,
        review_policy=review_policy.policy_digest,
        review_record=review_record.record_digest,
    )
    return result


def source_recomputed_valid(
    review_request: LifecycleReviewRequestV09,
    review_evidence: LifecycleReviewEvidenceV09,
    review_policy: LifecycleReviewPolicyV09,
    review_record: LifecycleReviewArtifactV09,
    source_args: tuple[Any, ...],
) -> bool:
    return not review_artifact_issues(
        review_record,
        review_request,
        review_evidence,
        review_policy,
        *source_args,
    )


def prior_actor_ids(
    subject_id: str,
    review_record: LifecycleReviewArtifactV09,
    source_args: tuple[Any, ...],
) -> set[str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    preparation_record = source_args[3]
    named = named_source(tuple(source_args[4:]))
    return {
        subject_id,
        named["candidate_record"].issuer_id,
        named["dependency_record"].reviewer_id,
        named["authority_record"].reviewer_id,
        named["authority_evidence"].responsible_authority_id,
        named["quiescence_record"].reviewer_id,
        named["external_record"].reviewer_id,
        named["external_evidence"].quiescence_evidence_producer_id,
        named["authorization_record"].authority_id,
        preparation_record.preparer_id,
        review_record.reviewer_id,
    }
