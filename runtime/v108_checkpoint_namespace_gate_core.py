#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from runtime.kuuos_repository_checkpoint_namespace_gate_types_v1_08 import (
    GATE_ACCEPTED,
    GATE_NOOP,
    GATE_REJECTED,
    REASON_CLEAN,
    REASON_CREATION_ROUTE,
    REASON_INVALID_ROUTE,
    REASON_NAMESPACE_MISMATCH,
    RepositoryCheckpointNamespaceGateDecision,
    RepositoryCheckpointNamespaceGatePolicy,
    repository_checkpoint_namespace_gate_decision_digest,
    repository_checkpoint_namespace_gate_policy_digest,
)
from runtime.kuuos_repository_checkpoint_repair_routing_types_v1_07 import (
    PRIMITIVE_ATOMIC_CHECKPOINT_CREATION_V1_02,
    PRIMITIVE_ATOMIC_REFERENCE_UPDATE_V0_97,
    PRIMITIVE_NONE,
    ROUTE_AUTOMATIC,
    ROUTE_NOOP,
    RepositoryCheckpointRepairRoute,
    RepositoryCheckpointRepairRoutingPolicy,
)
from runtime.kuuos_repository_checkpoint_repair_routing_v1_07 import (
    repository_checkpoint_repair_route_issues,
)
from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import (
    ZERO_OID,
    RepositoryCheckpointReviewObservation,
    RepositoryCheckpointReviewPolicy,
    RepositoryCheckpointReviewRecord,
)
from runtime.kuuos_repository_local_frontier_checkpoint_authorization_v1_01 import (
    normalize_repository_checkpoint_reference_name,
)


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_namespace_gate_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    allowed_checkpoint_references: tuple[str, ...],
    max_route_age_seconds: int,
) -> RepositoryCheckpointNamespaceGatePolicy:
    policy = RepositoryCheckpointNamespaceGatePolicy(
        policy_id=policy_id,
        allowed_repository_ids=_canonical(allowed_repository_ids),
        allowed_checkpoint_references=_canonical(
            allowed_checkpoint_references
        ),
        max_route_age_seconds=max_route_age_seconds,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_namespace_gate_policy_digest(policy),
    )
    issues = repository_checkpoint_namespace_gate_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_namespace_gate_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_namespace_gate_policy_issues(
    policy: RepositoryCheckpointNamespaceGatePolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_namespace_gate_policy_id_missing")
    if policy.allowed_repository_ids != _canonical(policy.allowed_repository_ids):
        issues.append("checkpoint_namespace_gate_repository_ids_not_canonical")
    if not policy.allowed_repository_ids:
        issues.append("checkpoint_namespace_gate_repository_ids_empty")
    if policy.allowed_checkpoint_references != _canonical(
        policy.allowed_checkpoint_references
    ):
        issues.append("checkpoint_namespace_gate_references_not_canonical")
    if not policy.allowed_checkpoint_references:
        issues.append("checkpoint_namespace_gate_references_empty")
    if any(
        normalize_repository_checkpoint_reference_name(reference) != reference
        for reference in policy.allowed_checkpoint_references
    ):
        issues.append("checkpoint_namespace_gate_reference_invalid")
    if policy.max_route_age_seconds <= 0:
        issues.append("checkpoint_namespace_gate_age_bound_invalid")
    if policy.policy_digest != repository_checkpoint_namespace_gate_policy_digest(
        policy
    ):
        issues.append("checkpoint_namespace_gate_policy_digest_mismatch")
    return tuple(issues)


def _route_issues(
    route: RepositoryCheckpointRepairRoute,
    record: RepositoryCheckpointReviewRecord,
    stability_certificate,
    v105_context: Mapping[str, Any],
    review_policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    routing_policy: RepositoryCheckpointRepairRoutingPolicy,
    *,
    review_evaluated_at_epoch_seconds: int,
    routed_at_epoch_seconds: int,
) -> tuple[str, ...]:
    try:
        return repository_checkpoint_repair_route_issues(
            route,
            record,
            stability_certificate,
            v105_context,
            review_policy,
            observation,
            routing_policy,
            review_evaluated_at_epoch_seconds=(
                review_evaluated_at_epoch_seconds
            ),
            routed_at_epoch_seconds=routed_at_epoch_seconds,
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("checkpoint_namespace_gate_route_inputs_invalid",)


def construct_repository_checkpoint_namespace_gate_decision(
    decision_id: str,
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
    evaluated_at_epoch_seconds: int,
) -> RepositoryCheckpointNamespaceGateDecision:
    route_valid = not _route_issues(
        route,
        record,
        stability_certificate,
        v105_context,
        review_policy,
        observation,
        routing_policy,
        review_evaluated_at_epoch_seconds=review_evaluated_at_epoch_seconds,
        routed_at_epoch_seconds=routed_at_epoch_seconds,
    )
    policy_valid = not repository_checkpoint_namespace_gate_policy_issues(
        gate_policy
    )
    binding_exact = bool(
        route.repository_id in gate_policy.allowed_repository_ids
        and route.checkpoint_reference
        in gate_policy.allowed_checkpoint_references
    )
    checkpoint_namespace = bool(
        normalize_repository_checkpoint_reference_name(
            route.checkpoint_reference
        )
        == route.checkpoint_reference
    )
    fresh = bool(
        0 <= evaluated_at_epoch_seconds - route.routed_at_epoch_seconds
        <= gate_policy.max_route_age_seconds
    )
    clean_noop = bool(
        route.status == ROUTE_NOOP and route.primitive == PRIMITIVE_NONE
    )
    creation_compatible = bool(
        route.status == ROUTE_AUTOMATIC
        and route.primitive == PRIMITIVE_ATOMIC_CHECKPOINT_CREATION_V1_02
        and route.expected_old_oid == ZERO_OID
        and route.proposed_new_oid != ZERO_OID
    )
    namespace_mismatch = bool(
        route.status == ROUTE_AUTOMATIC
        and route.primitive == PRIMITIVE_ATOMIC_REFERENCE_UPDATE_V0_97
        and checkpoint_namespace
    )
    base_valid = route_valid and policy_valid and binding_exact and fresh

    compatible = False
    if not base_valid:
        status = GATE_REJECTED
        reason = REASON_INVALID_ROUTE
    elif clean_noop:
        status = GATE_NOOP
        reason = REASON_CLEAN
    elif creation_compatible:
        status = GATE_ACCEPTED
        reason = REASON_CREATION_ROUTE
        compatible = True
    elif namespace_mismatch:
        status = GATE_REJECTED
        reason = REASON_NAMESPACE_MISMATCH
    else:
        status = GATE_REJECTED
        reason = REASON_INVALID_ROUTE

    checks = {
        "route_valid": route_valid,
        "policy_valid": policy_valid,
        "binding_exact": binding_exact,
        "checkpoint_namespace": checkpoint_namespace,
        "route_fresh": fresh,
        "clean_noop": clean_noop,
        "creation_route_compatible": creation_compatible,
        "namespace_mismatch": namespace_mismatch,
        "compatible": compatible,
    }
    decision = RepositoryCheckpointNamespaceGateDecision(
        decision_id=decision_id,
        status=status,
        reason=reason,
        route_digest=route.route_digest,
        policy_digest=gate_policy.policy_digest,
        repository_id=route.repository_id,
        git_dir_fingerprint=route.git_dir_fingerprint,
        checkpoint_reference=route.checkpoint_reference,
        expected_old_oid=route.expected_old_oid,
        proposed_new_oid=route.proposed_new_oid,
        selected_route=route.primitive,
        compatible=compatible,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        checks=checks,
        evidence_digests={
            "repair_route": route.route_digest,
            "gate_policy": gate_policy.policy_digest,
        },
        decision_digest="",
    )
    return replace(
        decision,
        decision_digest=(
            repository_checkpoint_namespace_gate_decision_digest(decision)
        ),
    )


def evaluate_repository_checkpoint_namespace_gate(
    decision_id: str,
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
    evaluated_at_epoch_seconds: int,
) -> RepositoryCheckpointNamespaceGateDecision:
    if not decision_id:
        raise ValueError("checkpoint_namespace_gate_decision_id_missing")
    decision = construct_repository_checkpoint_namespace_gate_decision(
        decision_id,
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
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_checkpoint_namespace_gate_decision_issues(
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
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"checkpoint_namespace_gate_decision_invalid:{issues[0]}")
    return decision


def repository_checkpoint_namespace_gate_decision_issues(
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
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    expected = construct_repository_checkpoint_namespace_gate_decision(
        decision.decision_id,
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
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues: list[str] = []
    if decision.to_dict() != expected.to_dict():
        issues.append("checkpoint_namespace_gate_recomputation_mismatch")
    if decision.status not in (GATE_NOOP, GATE_ACCEPTED, GATE_REJECTED):
        issues.append("checkpoint_namespace_gate_status_invalid")
    if decision.reason not in (
        REASON_CLEAN,
        REASON_CREATION_ROUTE,
        REASON_NAMESPACE_MISMATCH,
        REASON_INVALID_ROUTE,
    ):
        issues.append("checkpoint_namespace_gate_reason_invalid")
    if decision.compatible != (decision.status == GATE_ACCEPTED):
        issues.append("checkpoint_namespace_gate_compatibility_mismatch")
    if decision.decision_digest != (
        repository_checkpoint_namespace_gate_decision_digest(decision)
    ):
        issues.append("checkpoint_namespace_gate_digest_mismatch")
    return tuple(issues)
