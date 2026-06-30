#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    RepositoryCheckpointCandidate,
    RepositoryCheckpointCandidatePolicy,
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
from runtime.v109_checkpoint_candidate_core import (
    repository_checkpoint_candidate_issues,
)


def complete_v109_candidate_revalidation_issues(
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
    *,
    review_evaluated_at_epoch_seconds: int,
    routed_at_epoch_seconds: int,
    gate_evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    try:
        return repository_checkpoint_candidate_issues(
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
            evaluated_at_epoch_seconds=candidate.evaluated_at_epoch_seconds,
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("checkpoint_candidate_revalidation_inputs_invalid",)
