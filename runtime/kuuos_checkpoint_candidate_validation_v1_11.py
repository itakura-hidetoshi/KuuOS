#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any, Mapping

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    CANDIDATE_READY,
    RepositoryCheckpointCandidate,
)
from runtime.kuuos_repository_checkpoint_candidate_v1_09 import (
    repository_checkpoint_candidate_issues,
)
from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import ZERO_OID

VERSION = "kuuos_checkpoint_candidate_validation_v1_11"
VALID = "CHECKPOINT_CANDIDATE_VALIDATION_VALID"
REJECTED = "CHECKPOINT_CANDIDATE_VALIDATION_REJECTED"


@dataclass(frozen=True)
class CheckpointCandidateValidationReceipt:
    validation_id: str
    status: str
    candidate_digest: str
    repository_id: str
    checkpoint_reference: str
    expected_current_oid: str
    proposed_checkpoint_oid: str
    upstream_chain_revalidated: bool
    ready_candidate: bool
    repository_matches: bool
    checkpoint_matches: bool
    distinct_nonzero_oids: bool
    operation_performed: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    validation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def checkpoint_candidate_validation_digest(
    value: CheckpointCandidateValidationReceipt,
) -> str:
    payload = value.to_dict()
    payload.pop("validation_digest", None)
    return canonical_digest(payload)


def derive_checkpoint_candidate_validation(
    validation_id: str,
    candidate: RepositoryCheckpointCandidate,
    decision,
    route,
    record,
    stability_certificate,
    v105_context: Mapping[str, Any],
    review_policy,
    observation,
    routing_policy,
    gate_policy,
    candidate_policy,
    *,
    review_evaluated_at_epoch_seconds: int,
    routed_at_epoch_seconds: int,
    gate_evaluated_at_epoch_seconds: int,
    candidate_evaluated_at_epoch_seconds: int,
    expected_repository_id: str,
    expected_checkpoint_reference: str,
) -> CheckpointCandidateValidationReceipt:
    try:
        upstream_issues = repository_checkpoint_candidate_issues(
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
            evaluated_at_epoch_seconds=candidate_evaluated_at_epoch_seconds,
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        upstream_issues = ("checkpoint_candidate_upstream_inputs_invalid",)

    upstream_chain_revalidated = not upstream_issues
    ready_candidate = bool(
        candidate.status == CANDIDATE_READY
        and candidate.dedicated_checkpoint_interface_required
        and not candidate.human_review_required
        and not candidate.repository_change_authority_granted
        and not candidate.execution_performed
    )
    repository_matches = candidate.repository_id == expected_repository_id
    checkpoint_matches = candidate.checkpoint_reference == expected_checkpoint_reference
    distinct_nonzero_oids = bool(
        candidate.expected_current_oid != ZERO_OID
        and candidate.proposed_checkpoint_oid != ZERO_OID
        and candidate.expected_current_oid != candidate.proposed_checkpoint_oid
    )
    accepted = all(
        (
            bool(validation_id),
            upstream_chain_revalidated,
            ready_candidate,
            repository_matches,
            checkpoint_matches,
            distinct_nonzero_oids,
        )
    )
    value = CheckpointCandidateValidationReceipt(
        validation_id=validation_id,
        status=VALID if accepted else REJECTED,
        candidate_digest=candidate.candidate_digest,
        repository_id=candidate.repository_id,
        checkpoint_reference=candidate.checkpoint_reference,
        expected_current_oid=candidate.expected_current_oid,
        proposed_checkpoint_oid=candidate.proposed_checkpoint_oid,
        upstream_chain_revalidated=upstream_chain_revalidated,
        ready_candidate=ready_candidate,
        repository_matches=repository_matches,
        checkpoint_matches=checkpoint_matches,
        distinct_nonzero_oids=distinct_nonzero_oids,
        operation_performed=False,
        checks={
            "upstream_chain_revalidated": upstream_chain_revalidated,
            "ready_candidate": ready_candidate,
            "repository_matches": repository_matches,
            "checkpoint_matches": checkpoint_matches,
            "distinct_nonzero_oids": distinct_nonzero_oids,
            "operation_performed": False,
        },
        evidence_digests={
            "candidate": candidate.candidate_digest,
            "namespace_gate_decision": candidate.namespace_gate_decision_digest,
            "candidate_policy": candidate.candidate_policy_digest,
        },
        validation_digest="",
    )
    return replace(
        value,
        validation_digest=checkpoint_candidate_validation_digest(value),
    )
