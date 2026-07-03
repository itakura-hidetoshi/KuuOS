from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_authorization_decision_core_v0_12 import (
    artifact_issues as source_artifact_issues,
)
from runtime.kuuos_lifecycle_authorization_decision_source_v0_12 import (
    all_source_digests as prior_source_digests,
    prior_actor_ids as prior_authorization_actor_ids,
)
from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    LifecycleAuthorizationDecisionArtifactV012,
    LifecycleAuthorizationDecisionEvidenceV012,
    LifecycleAuthorizationDecisionPolicyV012,
    LifecycleAuthorizationDecisionSubmissionV012,
)


def all_source_digests(
    source_decision: LifecycleAuthorizationDecisionSubmissionV012,
    source_evidence: LifecycleAuthorizationDecisionEvidenceV012,
    source_policy: LifecycleAuthorizationDecisionPolicyV012,
    source_record: LifecycleAuthorizationDecisionArtifactV012,
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
        lifecycle_authorization_decision=source_decision.decision_digest,
        lifecycle_authorization_decision_evidence=source_evidence.evidence_digest,
        lifecycle_authorization_decision_policy=source_policy.policy_digest,
        lifecycle_authorization_decision_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_decision: LifecycleAuthorizationDecisionSubmissionV012,
    source_evidence: LifecycleAuthorizationDecisionEvidenceV012,
    source_policy: LifecycleAuthorizationDecisionPolicyV012,
    source_record: LifecycleAuthorizationDecisionArtifactV012,
    source_args: tuple[Any, ...],
) -> bool:
    return not source_artifact_issues(
        source_record,
        source_decision,
        source_evidence,
        source_policy,
        *source_args,
    )


def prior_actor_ids(
    subject_id: str,
    source_decision: LifecycleAuthorizationDecisionSubmissionV012,
    source_args: tuple[Any, ...],
) -> set[str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = prior_authorization_actor_ids(
        subject_id,
        source_args[0],
        tuple(source_args[4:]),
    )
    result.update(
        {
            source_decision.requester_id,
            source_decision.source_decision_reviewer_id,
            source_decision.authorization_decision_maker_id,
            source_decision.future_operator_id,
        }
    )
    return result
