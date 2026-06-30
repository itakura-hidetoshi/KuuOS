#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    RepositoryCheckpointCandidate,
    RepositoryCheckpointCandidatePolicy,
)
from runtime.kuuos_repository_checkpoint_candidate_revalidation_types_v1_11 import (
    REASON_CANDIDATE_STALE,
    REASON_FULL_REVALIDATION_PASSED,
    REASON_INVALID_EVIDENCE,
    REVALIDATION_REJECTED,
    REVALIDATION_VALID,
    RepositoryCheckpointCandidateRevalidationPolicy,
    RepositoryCheckpointCandidateRevalidationReceipt,
    repository_checkpoint_candidate_revalidation_receipt_digest,
)
from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import (
    RepositoryCheckpointReviewObservation,
    RepositoryCheckpointReviewPolicy,
    RepositoryCheckpointReviewRecord,
)
from runtime.kuuos_repository_checkpoint_namespace_gate_types_v1_08 import (
    RepositoryCheckpointNamespaceGateDecision,
    RepositoryCheckpointNamespaceGatePolicy,
)
from runtime.kuuos_repository_checkpoint_repair_routing_types_v1_07 import (
    RepositoryCheckpointRepairRoute,
    RepositoryCheckpointRepairRoutingPolicy,
)
from runtime.v111_checkpoint_candidate_revalidation_policy import (
    repository_checkpoint_candidate_revalidation_policy_issues,
)
from runtime.v111_checkpoint_candidate_revalidation_replay import (
    complete_v109_candidate_revalidation_issues,
)


def construct_repository_checkpoint_candidate_revalidation_receipt(
    receipt_id: str,
    candidate: RepositoryCheckpointCandidate,
    decision: RepositoryCheckpointNamespaceGateDecision,
    route: RepositoryCheckpointRepairRoute,
    record: RepositoryCheckpointReviewRecord,
    stability_certificate: Any,
    v105_context: Mapping[str, Any],
    review_policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    routing_policy: RepositoryCheckpointRepairRoutingPolicy,
    gate_policy: RepositoryCheckpointNamespaceGatePolicy,
    candidate_policy: RepositoryCheckpointCandidatePolicy,
    revalidation_policy: RepositoryCheckpointCandidateRevalidationPolicy,
    *,
    review_evaluated_at_epoch_seconds: int,
    routed_at_epoch_seconds: int,
    gate_evaluated_at_epoch_seconds: int,
    revalidated_at_epoch_seconds: int,
) -> RepositoryCheckpointCandidateRevalidationReceipt:
    replay_issues = complete_v109_candidate_revalidation_issues(
        candidate,
        decision,
        route,
        record,
        stability_certificate,
        v105_context,
        review_policy,
        observation,
        routing_policy,
        gate_policy,
        candidate_policy,
        review_evaluated_at_epoch_seconds=review_evaluated_at_epoch_seconds,
        routed_at_epoch_seconds=routed_at_epoch_seconds,
        gate_evaluated_at_epoch_seconds=gate_evaluated_at_epoch_seconds,
    )
    full_revalidation_passed = not replay_issues
    policy_valid = not repository_checkpoint_candidate_revalidation_policy_issues(
        revalidation_policy
    )
    binding_exact = bool(
        candidate.repository_id in revalidation_policy.allowed_repository_ids
        and candidate.checkpoint_reference
        in revalidation_policy.allowed_checkpoint_references
    )
    candidate_fresh = bool(
        0
        <= revalidated_at_epoch_seconds - candidate.evaluated_at_epoch_seconds
        <= revalidation_policy.max_candidate_age_seconds
    )

    if full_revalidation_passed and policy_valid and binding_exact and candidate_fresh:
        status = REVALIDATION_VALID
        reason = REASON_FULL_REVALIDATION_PASSED
    elif full_revalidation_passed and policy_valid and binding_exact:
        status = REVALIDATION_REJECTED
        reason = REASON_CANDIDATE_STALE
    else:
        status = REVALIDATION_REJECTED
        reason = REASON_INVALID_EVIDENCE

    checks = {
        "complete_v109_revalidation_passed": full_revalidation_passed,
        "revalidation_policy_valid": policy_valid,
        "repository_binding_exact": binding_exact,
        "candidate_fresh": candidate_fresh,
        "repository_change_authority_granted": False,
        "execution_performed": False,
        "live_git_command_invoked": False,
    }
    receipt = RepositoryCheckpointCandidateRevalidationReceipt(
        receipt_id=receipt_id,
        status=status,
        reason=reason,
        candidate_digest=candidate.candidate_digest,
        revalidation_policy_digest=revalidation_policy.policy_digest,
        repository_id=candidate.repository_id,
        git_dir_fingerprint=candidate.git_dir_fingerprint,
        checkpoint_reference=candidate.checkpoint_reference,
        candidate_evaluated_at_epoch_seconds=candidate.evaluated_at_epoch_seconds,
        revalidated_at_epoch_seconds=revalidated_at_epoch_seconds,
        full_v109_revalidation_passed=full_revalidation_passed,
        repository_binding_exact=binding_exact,
        candidate_fresh=candidate_fresh,
        repository_change_authority_granted=False,
        execution_performed=False,
        live_git_command_invoked=False,
        checks=checks,
        evidence_digests={
            "candidate": candidate.candidate_digest,
            "namespace_gate_decision": decision.decision_digest,
            "repair_route": route.route_digest,
            "review_record": record.record_digest,
            "stability_certificate": stability_certificate.certificate_digest,
            "v105_context": canonical_digest(dict(v105_context)),
            "review_policy": review_policy.policy_digest,
            "review_observation": observation.observation_digest,
            "routing_policy": routing_policy.policy_digest,
            "gate_policy": gate_policy.policy_digest,
            "candidate_policy": candidate_policy.policy_digest,
            "revalidation_policy": revalidation_policy.policy_digest,
        },
        receipt_digest="",
    )
    return replace(
        receipt,
        receipt_digest=repository_checkpoint_candidate_revalidation_receipt_digest(
            receipt
        ),
    )
