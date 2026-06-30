#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import (
    DISCREPANCY_LOST,
    DISCREPANCY_NONE,
    DISCREPANCY_SUBSTITUTED,
    REVIEW_AUTOMATIC_REPAIR_ELIGIBLE,
    REVIEW_CLEAN,
    ZERO_OID,
    RepositoryCheckpointReviewObservation,
    RepositoryCheckpointReviewPolicy,
    RepositoryCheckpointReviewRecord,
)
from runtime.kuuos_repository_checkpoint_repair_routing_types_v1_07 import (
    PRIMITIVE_ATOMIC_CHECKPOINT_CREATION_V1_02,
    PRIMITIVE_NONE,
    ROUTE_AUTOMATIC,
    ROUTE_NOOP,
    ROUTE_REJECTED,
    RepositoryCheckpointRepairRoute,
    RepositoryCheckpointRepairRoutingPolicy,
    repository_checkpoint_repair_route_digest,
    repository_checkpoint_repair_routing_policy_digest,
)
from runtime.v106_review_strict import repository_checkpoint_review_record_issues


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_repair_routing_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    allowed_checkpoint_references: tuple[str, ...],
    max_review_age_seconds: int,
) -> RepositoryCheckpointRepairRoutingPolicy:
    policy = RepositoryCheckpointRepairRoutingPolicy(
        policy_id=policy_id,
        allowed_repository_ids=_canonical(allowed_repository_ids),
        allowed_checkpoint_references=_canonical(allowed_checkpoint_references),
        max_review_age_seconds=max_review_age_seconds,
        allow_checkpoint_creation_route=True,
        allow_reference_update_route=False,
        require_complete_v106_revalidation=True,
        require_exact_repository_binding=True,
        require_read_only_routing=True,
        execute_live_git=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_repair_routing_policy_digest(policy),
    )
    issues = repository_checkpoint_repair_routing_policy_issues(policy)
    if issues:
        raise ValueError(f"repair_routing_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_repair_routing_policy_issues(
    policy: RepositoryCheckpointRepairRoutingPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("routing_policy_id_missing")
    if policy.allowed_repository_ids != _canonical(policy.allowed_repository_ids):
        issues.append("routing_repository_ids_not_canonical")
    if not policy.allowed_repository_ids:
        issues.append("routing_repository_ids_empty")
    if policy.allowed_checkpoint_references != _canonical(
        policy.allowed_checkpoint_references
    ):
        issues.append("routing_references_not_canonical")
    if not policy.allowed_checkpoint_references:
        issues.append("routing_references_empty")
    if policy.max_review_age_seconds <= 0:
        issues.append("routing_age_bound_invalid")
    if not all(
        (
            policy.allow_checkpoint_creation_route,
            policy.require_complete_v106_revalidation,
            policy.require_exact_repository_binding,
            policy.require_read_only_routing,
        )
    ):
        issues.append("routing_required_guard_disabled")
    if policy.allow_reference_update_route:
        issues.append("routing_incompatible_route_enabled")
    if policy.execute_live_git:
        issues.append("routing_not_read_only")
    if policy.policy_digest != repository_checkpoint_repair_routing_policy_digest(
        policy
    ):
        issues.append("routing_policy_digest_mismatch")
    return tuple(issues)


def _upstream_issues(
    record: RepositoryCheckpointReviewRecord,
    stability_certificate,
    v105_context: Mapping[str, Any],
    review_policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    evaluated_at: int,
) -> tuple[str, ...]:
    try:
        return repository_checkpoint_review_record_issues(
            record,
            stability_certificate,
            v105_context,
            review_policy,
            observation,
            evaluated_at_epoch_seconds=evaluated_at,
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("upstream_review_inputs_invalid",)


def construct_repository_checkpoint_repair_route(
    route_id: str,
    record: RepositoryCheckpointReviewRecord,
    stability_certificate,
    v105_context: Mapping[str, Any],
    review_policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    routing_policy: RepositoryCheckpointRepairRoutingPolicy,
    *,
    review_evaluated_at_epoch_seconds: int,
    routed_at_epoch_seconds: int,
) -> RepositoryCheckpointRepairRoute:
    upstream_valid = not _upstream_issues(
        record,
        stability_certificate,
        v105_context,
        review_policy,
        observation,
        review_evaluated_at_epoch_seconds,
    )
    policy_valid = not repository_checkpoint_repair_routing_policy_issues(
        routing_policy
    )
    binding_exact = bool(
        record.repository_id == stability_certificate.repository_id
        and record.git_dir_fingerprint == stability_certificate.git_dir_fingerprint
        and record.checkpoint_reference == stability_certificate.checkpoint_reference
        and record.repository_id in routing_policy.allowed_repository_ids
        and record.checkpoint_reference
        in routing_policy.allowed_checkpoint_references
    )
    fresh = bool(
        0 <= routed_at_epoch_seconds - record.evaluated_at_epoch_seconds
        <= routing_policy.max_review_age_seconds
    )
    base_valid = upstream_valid and policy_valid and binding_exact and fresh
    automatic = bool(
        record.status == REVIEW_AUTOMATIC_REPAIR_ELIGIBLE
        and record.automatic_repair_eligible
        and not record.human_review_required
    )
    clean = bool(
        record.status == REVIEW_CLEAN
        and record.discrepancy_kind == DISCREPANCY_NONE
        and record.expected_current_oid == record.expected_target_oid
        and not record.automatic_repair_eligible
    )
    lost = bool(
        automatic
        and record.discrepancy_kind == DISCREPANCY_LOST
        and record.expected_current_oid == ZERO_OID
        and record.expected_target_oid != ZERO_OID
    )
    substituted = bool(
        automatic
        and record.discrepancy_kind == DISCREPANCY_SUBSTITUTED
        and record.expected_current_oid != ZERO_OID
        and record.expected_target_oid != ZERO_OID
        and record.expected_current_oid != record.expected_target_oid
    )

    eligible = False
    if not base_valid:
        status, primitive = ROUTE_REJECTED, PRIMITIVE_NONE
    elif clean:
        status, primitive = ROUTE_NOOP, PRIMITIVE_NONE
    elif lost:
        status = ROUTE_AUTOMATIC
        primitive = PRIMITIVE_ATOMIC_CHECKPOINT_CREATION_V1_02
        eligible = True
    else:
        status, primitive = ROUTE_REJECTED, PRIMITIVE_NONE

    checks = {
        "upstream_review_valid": upstream_valid,
        "routing_policy_valid": policy_valid,
        "binding_exact": binding_exact,
        "review_fresh": fresh,
        "clean_shape": clean,
        "lost_shape": lost,
        "substituted_shape": substituted,
        "compatible_substitution_primitive_available": False,
        "automatic_route_eligible": eligible,
        "human_review_required": False,
        "side_effect_performed": False,
    }
    route = RepositoryCheckpointRepairRoute(
        route_id=route_id,
        status=status,
        primitive=primitive,
        review_record_digest=record.record_digest,
        routing_policy_digest=routing_policy.policy_digest,
        repository_id=record.repository_id,
        git_dir_fingerprint=record.git_dir_fingerprint,
        checkpoint_reference=record.checkpoint_reference,
        expected_old_oid=record.expected_current_oid,
        proposed_new_oid=record.expected_target_oid,
        automatic_route_eligible=eligible,
        human_review_required=False,
        repository_change_authority_granted=False,
        live_git_execution_performed=False,
        routed_at_epoch_seconds=routed_at_epoch_seconds,
        checks=checks,
        evidence_digests={
            "review_record": record.record_digest,
            "routing_policy": routing_policy.policy_digest,
        },
        route_digest="",
    )
    return replace(route, route_digest=repository_checkpoint_repair_route_digest(route))


def route_repository_checkpoint_repair(
    route_id: str,
    record: RepositoryCheckpointReviewRecord,
    stability_certificate,
    v105_context: Mapping[str, Any],
    review_policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    routing_policy: RepositoryCheckpointRepairRoutingPolicy,
    *,
    review_evaluated_at_epoch_seconds: int,
    routed_at_epoch_seconds: int,
) -> RepositoryCheckpointRepairRoute:
    if not route_id:
        raise ValueError("repair_route_id_missing")
    route = construct_repository_checkpoint_repair_route(
        route_id,
        record,
        stability_certificate,
        v105_context,
        review_policy,
        observation,
        routing_policy,
        review_evaluated_at_epoch_seconds=review_evaluated_at_epoch_seconds,
        routed_at_epoch_seconds=routed_at_epoch_seconds,
    )
    issues = repository_checkpoint_repair_route_issues(
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
    if issues:
        raise ValueError(f"repair_route_invalid:{issues[0]}")
    return route


def repository_checkpoint_repair_route_issues(
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
    expected = construct_repository_checkpoint_repair_route(
        route.route_id,
        record,
        stability_certificate,
        v105_context,
        review_policy,
        observation,
        routing_policy,
        review_evaluated_at_epoch_seconds=review_evaluated_at_epoch_seconds,
        routed_at_epoch_seconds=routed_at_epoch_seconds,
    )
    issues: list[str] = []
    if route.to_dict() != expected.to_dict():
        issues.append("repair_route_recomputation_mismatch")
    if route.status not in (ROUTE_NOOP, ROUTE_AUTOMATIC, ROUTE_REJECTED):
        issues.append("repair_route_status_invalid")
    if route.primitive not in (
        PRIMITIVE_NONE,
        PRIMITIVE_ATOMIC_CHECKPOINT_CREATION_V1_02,
    ):
        issues.append("repair_route_primitive_invalid")
    if route.automatic_route_eligible != (route.status == ROUTE_AUTOMATIC):
        issues.append("repair_route_eligibility_mismatch")
    if route.human_review_required:
        issues.append("repair_route_human_review_invalid")
    if route.repository_change_authority_granted:
        issues.append("repair_route_authority_invalid")
    if route.live_git_execution_performed:
        issues.append("repair_route_execution_invalid")
    if route.checks.get("side_effect_performed", False):
        issues.append("repair_route_side_effect_invalid")
    if route.route_digest != repository_checkpoint_repair_route_digest(route):
        issues.append("repair_route_digest_mismatch")
    return tuple(issues)
