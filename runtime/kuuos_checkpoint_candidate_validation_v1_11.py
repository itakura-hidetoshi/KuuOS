#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    CANDIDATE_READY,
    RepositoryCheckpointCandidate,
    repository_checkpoint_candidate_digest,
)
from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import ZERO_OID

VERSION = "kuuos_checkpoint_candidate_validation_v1_11"
VALID = "CHECKPOINT_CANDIDATE_VALID"
REJECTED = "CHECKPOINT_CANDIDATE_REJECTED"


@dataclass(frozen=True)
class CheckpointCandidateValidation:
    validation_id: str
    status: str
    candidate_digest: str
    repository_id: str
    checkpoint_reference: str
    expected_current_oid: str
    proposed_checkpoint_oid: str
    digest_matches: bool
    ready_candidate: bool
    repository_matches: bool
    checkpoint_matches: bool
    distinct_nonzero_oids: bool
    operation_performed: bool
    checks: dict[str, bool]
    validation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validation_digest(value: CheckpointCandidateValidation) -> str:
    payload = value.to_dict()
    payload.pop("validation_digest", None)
    return canonical_digest(payload)


def derive_checkpoint_candidate_validation(
    validation_id: str,
    candidate: RepositoryCheckpointCandidate,
    *,
    expected_repository_id: str,
    expected_checkpoint_reference: str,
) -> CheckpointCandidateValidation:
    digest_matches = candidate.candidate_digest == repository_checkpoint_candidate_digest(candidate)
    ready_candidate = bool(
        candidate.status == CANDIDATE_READY
        and candidate.dedicated_checkpoint_interface_required
        and not candidate.execution_performed
    )
    repository_matches = candidate.repository_id == expected_repository_id
    checkpoint_matches = candidate.checkpoint_reference == expected_checkpoint_reference
    distinct_nonzero_oids = bool(
        candidate.expected_current_oid != ZERO_OID
        and candidate.proposed_checkpoint_oid != ZERO_OID
        and candidate.expected_current_oid != candidate.proposed_checkpoint_oid
    )
    accepted = all((
        bool(validation_id),
        digest_matches,
        ready_candidate,
        repository_matches,
        checkpoint_matches,
        distinct_nonzero_oids,
    ))
    value = CheckpointCandidateValidation(
        validation_id=validation_id,
        status=VALID if accepted else REJECTED,
        candidate_digest=candidate.candidate_digest,
        repository_id=candidate.repository_id,
        checkpoint_reference=candidate.checkpoint_reference,
        expected_current_oid=candidate.expected_current_oid,
        proposed_checkpoint_oid=candidate.proposed_checkpoint_oid,
        digest_matches=digest_matches,
        ready_candidate=ready_candidate,
        repository_matches=repository_matches,
        checkpoint_matches=checkpoint_matches,
        distinct_nonzero_oids=distinct_nonzero_oids,
        operation_performed=False,
        checks={
            "digest_matches": digest_matches,
            "ready_candidate": ready_candidate,
            "repository_matches": repository_matches,
            "checkpoint_matches": checkpoint_matches,
            "distinct_nonzero_oids": distinct_nonzero_oids,
            "operation_performed": False,
        },
        validation_digest="",
    )
    return replace(value, validation_digest=validation_digest(value))
