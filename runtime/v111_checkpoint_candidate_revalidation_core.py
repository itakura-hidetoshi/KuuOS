#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    RepositoryCheckpointCandidate,
    RepositoryCheckpointCandidatePolicy,
)
from runtime.kuuos_repository_checkpoint_candidate_revalidation_types_v1_11 import (
    REASON_CANDIDATE_STALE,
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
from runtime.v111_checkpoint_candidate_revalidation_build import (
    construct_repository_checkpoint_candidate_revalidation_receipt,
)


def derive_repository_checkpoint_candidate_revalidation_receipt(
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
    if not receipt_id:
        raise ValueError(
            "checkpoint_candidate_revalidation_receipt_id_missing"
        )
    receipt = construct_repository_checkpoint_candidate_revalidation_receipt(
        receipt_id,
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
        revalidation_policy,
        review_evaluated_at_epoch_seconds=review_evaluated_at_epoch_seconds,
        routed_at_epoch_seconds=routed_at_epoch_seconds,
        gate_evaluated_at_epoch_seconds=gate_evaluated_at_epoch_seconds,
        revalidated_at_epoch_seconds=revalidated_at_epoch_seconds,
    )
    issues = repository_checkpoint_candidate_revalidation_receipt_issues(
        receipt,
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
        revalidation_policy,
        review_evaluated_at_epoch_seconds=review_evaluated_at_epoch_seconds,
        routed_at_epoch_seconds=routed_at_epoch_seconds,
        gate_evaluated_at_epoch_seconds=gate_evaluated_at_epoch_seconds,
        revalidated_at_epoch_seconds=revalidated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(
            f"checkpoint_candidate_revalidation_receipt_invalid:{issues[0]}"
        )
    return receipt


def repository_checkpoint_candidate_revalidation_receipt_issues(
    receipt: RepositoryCheckpointCandidateRevalidationReceipt,
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
) -> tuple[str, ...]:
    expected = construct_repository_checkpoint_candidate_revalidation_receipt(
        receipt.receipt_id,
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
        revalidation_policy,
        review_evaluated_at_epoch_seconds=review_evaluated_at_epoch_seconds,
        routed_at_epoch_seconds=routed_at_epoch_seconds,
        gate_evaluated_at_epoch_seconds=gate_evaluated_at_epoch_seconds,
        revalidated_at_epoch_seconds=revalidated_at_epoch_seconds,
    )
    issues: list[str] = []
    if receipt.to_dict() != expected.to_dict():
        issues.append(
            "checkpoint_candidate_revalidation_recomputation_mismatch"
        )
    if receipt.status not in (REVALIDATION_VALID, REVALIDATION_REJECTED):
        issues.append("checkpoint_candidate_revalidation_status_invalid")
    if receipt.status == REVALIDATION_VALID and not (
        receipt.full_v109_revalidation_passed
        and receipt.repository_binding_exact
        and receipt.candidate_fresh
    ):
        issues.append("checkpoint_candidate_revalidation_validity_mismatch")
    if (
        receipt.reason == REASON_CANDIDATE_STALE
        and not receipt.full_v109_revalidation_passed
    ):
        issues.append("checkpoint_candidate_revalidation_stale_mismatch")
    forbidden = (
        receipt.repository_change_authority_granted,
        receipt.execution_performed,
        receipt.live_git_command_invoked,
    )
    if any(forbidden):
        issues.append("checkpoint_candidate_revalidation_forbidden_claim")
    if (
        receipt.receipt_digest
        != repository_checkpoint_candidate_revalidation_receipt_digest(receipt)
    ):
        issues.append(
            "checkpoint_candidate_revalidation_receipt_digest_mismatch"
        )
    return tuple(issues)
