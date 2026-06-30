#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    CANDIDATE_NONE,
    CANDIDATE_READY,
    CANDIDATE_REJECTED,
    REASON_CHECKPOINT_INTERFACE_REQUIRED,
    REASON_CLEAN_NOOP,
    REASON_CREATION_ROUTE_AVAILABLE,
    REASON_INVALID_EVIDENCE,
    RepositoryCheckpointCandidate,
    RepositoryCheckpointCandidatePolicy,
    repository_checkpoint_candidate_digest,
    repository_checkpoint_candidate_policy_digest,
)
from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import (
    ZERO_OID,
    RepositoryCheckpointReviewObservation,
    RepositoryCheckpointReviewPolicy,
    RepositoryCheckpointReviewRecord,
)
from runtime.kuuos_repository_checkpoint_namespace_gate_types_v1_08 import (
    GATE_ACCEPTED,
    GATE_NOOP,
    GATE_REJECTED,
    REASON_NAMESPACE_MISMATCH,
    RepositoryCheckpointNamespaceGateDecision,
    RepositoryCheckpointNamespaceGatePolicy,
)
from runtime.kuuos_repository_checkpoint_namespace_gate_v1_08 import (
    repository_checkpoint_namespace_gate_decision_issues,
)
from runtime.kuuos_repository_checkpoint_repair_routing_types_v1_07 import (
    PRIMITIVE_ATOMIC_REFERENCE_UPDATE_V0_97,
    RepositoryCheckpointRepairRoute,
    RepositoryCheckpointRepairRoutingPolicy,
)


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_candidate_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    allowed_checkpoint_references: tuple[str, ...],
    max_gate_age_seconds: int,
) -> RepositoryCheckpointCandidatePolicy:
    policy = RepositoryCheckpointCandidatePolicy(
        policy_id=policy_id,
        allowed_repository_ids=_canonical(allowed_repository_ids),
        allowed_checkpoint_references=_canonical(allowed_checkpoint_references),
        max_gate_age_seconds=max_gate_age_seconds,
        require_complete_v108_revalidation=True,
        require_exact_repository_binding=True,
        require_distinct_nonzero_oids=True,
        read_only=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_candidate_policy_digest(policy),
    )
    issues = repository_checkpoint_candidate_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_candidate_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_candidate_policy_issues(
    policy: RepositoryCheckpointCandidatePolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_candidate_policy_id_missing")
    if policy.allowed_repository_ids != _canonical(policy.allowed_repository_ids):
        issues.append("checkpoint_candidate_repository_ids_not_canonical")
    if not policy.allowed_repository_ids:
        issues.append("checkpoint_candidate_repository_ids_empty")
    if policy.allowed_checkpoint_references != _canonical(
        policy.allowed_checkpoint_references
    ):
        issues.append("checkpoint_candidate_references_not_canonical")
    if not policy.allowed_checkpoint_references:
        issues.append("checkpoint_candidate_references_empty")
    if policy.max_gate_age_seconds <= 0:
        issues.append("checkpoint_candidate_age_bound_invalid")
    required = (
        policy.require_complete_v108_revalidation,
        policy.require_exact_repository_binding,
        policy.require_distinct_nonzero_oids,
        policy.read_only,
    )
    if not all(required):
        issues.append("checkpoint_candidate_guard_disabled")
    if policy.policy_digest != repository_checkpoint_candidate_policy_digest(policy):
        issues.append("checkpoint_candidate_policy_digest_mismatch")
    return tuple(issues)


def _gate_issues(
    decision: RepositoryCheckpointNamespaceGateDecision,
    route: RepositoryCheckpointRepairRoute,
    record: RepositoryCheckpointReviewRecord,
    stability_certificate,
    v105_context: Mapping[str, Any],
    review_policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    routing_policy: RepositoryCheckpointRepairRoutingPolicy,
    gate_policy: RepositoryCheckpointNamespaceGatePolicy,
    *,
    review_evaluated_at_epoch_seconds: int,
    routed_at_epoch_seconds: int,
    gate_evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    try:
        return repository_checkpoint_namespace_gate_decision_issues(
            decision,
            route,
            record,
            stability_certificate,
            v105_context,
            review_policy,
            observation,
            routing_policy,
            gate_policy,
            review_evaluated_at_epoch_seconds=review_evaluated_at_epoch_seconds,
            routed_at_epoch_seconds=routed_at_epoch_seconds,
            evaluated_at_epoch_seconds=gate_evaluated_at_epoch_seconds,
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("checkpoint_candidate_gate_inputs_invalid",)


def construct_repository_checkpoint_candidate(
    candidate_id: str,
    decision: RepositoryCheckpointNamespaceGateDecision,
    route: RepositoryCheckpointRepairRoute,
    record: RepositoryCheckpointReviewRecord,
    stability_certificate,
    v105_context: Mapping[str, Any],
    review_policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    routing_policy: RepositoryCheckpointRepairRoutingPolicy,
    gate_policy: RepositoryCheckpointNamespaceGatePolicy,
    candidate_policy: RepositoryCheckpointCandidatePolicy,
    *,
    review_evaluated_at_epoch_seconds: int,
    routed_at_epoch_seconds: int,
    gate_evaluated_at_epoch_seconds: int,
    evaluated_at_epoch_seconds: int,
) -> RepositoryCheckpointCandidate:
    gate_valid = not _gate_issues(
        decision,
        route,
        record,
        stability_certificate,
        v105_context,
        review_policy,
        observation,
        routing_policy,
        gate_policy,
        review_evaluated_at_epoch_seconds=review_evaluated_at_epoch_seconds,
        routed_at_epoch_seconds=routed_at_epoch_seconds,
        gate_evaluated_at_epoch_seconds=gate_evaluated_at_epoch_seconds,
    )
    policy_valid = not repository_checkpoint_candidate_policy_issues(
        candidate_policy
    )
    binding_exact = bool(
        decision.repository_id in candidate_policy.allowed_repository_ids
        and decision.checkpoint_reference
        in candidate_policy.allowed_checkpoint_references
    )
    gate_fresh = bool(
        0 <= evaluated_at_epoch_seconds - decision.evaluated_at_epoch_seconds
        <= candidate_policy.max_gate_age_seconds
    )
    clean_noop = decision.status == GATE_NOOP
    creation_available = decision.status == GATE_ACCEPTED and decision.compatible
    checkpoint_interface_required = bool(
        decision.status == GATE_REJECTED
        and decision.reason == REASON_NAMESPACE_MISMATCH
        and decision.selected_route == PRIMITIVE_ATOMIC_REFERENCE_UPDATE_V0_97
        and decision.expected_old_oid != ZERO_OID
        and decision.proposed_new_oid != ZERO_OID
        and decision.expected_old_oid != decision.proposed_new_oid
    )
    base_valid = gate_valid and policy_valid and binding_exact and gate_fresh

    dedicated_required = False
    if not base_valid:
        status = CANDIDATE_REJECTED
        reason = REASON_INVALID_EVIDENCE
    elif clean_noop:
        status = CANDIDATE_NONE
        reason = REASON_CLEAN_NOOP
    elif creation_available:
        status = CANDIDATE_NONE
        reason = REASON_CREATION_ROUTE_AVAILABLE
    elif checkpoint_interface_required:
        status = CANDIDATE_READY
        reason = REASON_CHECKPOINT_INTERFACE_REQUIRED
        dedicated_required = True
    else:
        status = CANDIDATE_REJECTED
        reason = REASON_INVALID_EVIDENCE

    checks = {
        "namespace_gate_valid": gate_valid,
        "candidate_policy_valid": policy_valid,
        "repository_binding_exact": binding_exact,
        "namespace_gate_fresh": gate_fresh,
        "clean_noop": clean_noop,
        "creation_route_available": creation_available,
        "checkpoint_interface_required": checkpoint_interface_required,
        "dedicated_checkpoint_interface_required": dedicated_required,
        "human_review_required": False,
        "repository_change_authority_granted": False,
        "execution_performed": False,
    }
    candidate = RepositoryCheckpointCandidate(
        candidate_id=candidate_id,
        status=status,
        reason=reason,
        namespace_gate_decision_digest=decision.decision_digest,
        candidate_policy_digest=candidate_policy.policy_digest,
        repository_id=decision.repository_id,
        git_dir_fingerprint=decision.git_dir_fingerprint,
        checkpoint_reference=decision.checkpoint_reference,
        expected_current_oid=decision.expected_old_oid,
        proposed_checkpoint_oid=decision.proposed_new_oid,
        dedicated_checkpoint_interface_required=dedicated_required,
        human_review_required=False,
        repository_change_authority_granted=False,
        execution_performed=False,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        checks=checks,
        evidence_digests={
            "namespace_gate_decision": decision.decision_digest,
            "candidate_policy": candidate_policy.policy_digest,
        },
        candidate_digest="",
    )
    return replace(
        candidate,
        candidate_digest=repository_checkpoint_candidate_digest(candidate),
    )


def derive_repository_checkpoint_candidate(
    candidate_id: str,
    decision: RepositoryCheckpointNamespaceGateDecision,
    route: RepositoryCheckpointRepairRoute,
    record: RepositoryCheckpointReviewRecord,
    stability_certificate,
    v105_context: Mapping[str, Any],
    review_policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    routing_policy: RepositoryCheckpointRepairRoutingPolicy,
    gate_policy: RepositoryCheckpointNamespaceGatePolicy,
    candidate_policy: RepositoryCheckpointCandidatePolicy,
    *,
    review_evaluated_at_epoch_seconds: int,
    routed_at_epoch_seconds: int,
    gate_evaluated_at_epoch_seconds: int,
    evaluated_at_epoch_seconds: int,
) -> RepositoryCheckpointCandidate:
    if not candidate_id:
        raise ValueError("checkpoint_candidate_id_missing")
    candidate = construct_repository_checkpoint_candidate(
        candidate_id,
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
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_checkpoint_candidate_issues(
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
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"checkpoint_candidate_invalid:{issues[0]}")
    return candidate


def repository_checkpoint_candidate_issues(
    candidate: RepositoryCheckpointCandidate,
    decision: RepositoryCheckpointNamespaceGateDecision,
    route: RepositoryCheckpointRepairRoute,
    record: RepositoryCheckpointReviewRecord,
    stability_certificate,
    v105_context: Mapping[str, Any],
    review_policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    routing_policy: RepositoryCheckpointRepairRoutingPolicy,
    gate_policy: RepositoryCheckpointNamespaceGatePolicy,
    candidate_policy: RepositoryCheckpointCandidatePolicy,
    *,
    review_evaluated_at_epoch_seconds: int,
    routed_at_epoch_seconds: int,
    gate_evaluated_at_epoch_seconds: int,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    expected = construct_repository_checkpoint_candidate(
        candidate.candidate_id,
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
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues: list[str] = []
    if candidate.to_dict() != expected.to_dict():
        issues.append("checkpoint_candidate_recomputation_mismatch")
    if candidate.status not in (
        CANDIDATE_NONE,
        CANDIDATE_READY,
        CANDIDATE_REJECTED,
    ):
        issues.append("checkpoint_candidate_status_invalid")
    if candidate.dedicated_checkpoint_interface_required != (
        candidate.status == CANDIDATE_READY
    ):
        issues.append("checkpoint_candidate_interface_boundary_mismatch")
    forbidden = (
        candidate.human_review_required,
        candidate.repository_change_authority_granted,
        candidate.execution_performed,
    )
    if any(forbidden):
        issues.append("checkpoint_candidate_forbidden_claim")
    if candidate.candidate_digest != repository_checkpoint_candidate_digest(
        candidate
    ):
        issues.append("checkpoint_candidate_digest_mismatch")
    return tuple(issues)
