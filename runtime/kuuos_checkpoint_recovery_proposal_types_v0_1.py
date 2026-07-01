#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_checkpoint_recovery_proposal_v0_1"

RECOVERY_PROPOSAL_PROPOSED = "CHECKPOINT_RECOVERY_PROPOSAL_PROPOSED"
RECOVERY_PROPOSAL_REJECTED = "CHECKPOINT_RECOVERY_PROPOSAL_REJECTED"

RECOVERY_OBJECTIVE_COMPARE_ONLY = "COMPARE_CHECKPOINT_WITH_TARGET_ONLY"


@dataclass(frozen=True)
class CheckpointRecoveryProposalPolicy:
    policy_id: str
    authorized_requestor_ids: tuple[str, ...]
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    allowed_target_references: tuple[str, ...]
    allowed_objectives: tuple[str, ...]
    max_rationale_bytes: int
    require_accepted_v124_result: bool
    require_exact_source_binding: bool
    require_exact_target_allowlist: bool
    require_distinct_source_and_target: bool
    require_source_target_comparison: bool
    require_external_review: bool
    require_explicit_authorization_decision: bool
    require_read_only_proposal: bool
    continue_v124_mutation_series: bool
    allow_live_git_execution: bool
    allow_repository_mutation: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for field_name in (
            "authorized_requestor_ids",
            "allowed_repository_ids",
            "allowed_checkpoint_references",
            "allowed_target_references",
            "allowed_objectives",
        ):
            payload[field_name] = list(getattr(self, field_name))
        return payload


def checkpoint_recovery_proposal_policy_digest(
    policy: CheckpointRecoveryProposalPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class CheckpointRecoveryProposal:
    proposal_id: str
    status: str
    reason: str
    policy_digest: str
    source_v124_result_digest: str
    source_v124_status: str
    repository_id: str
    git_dir_fingerprint: str
    source_checkpoint_reference: str
    source_checkpoint_oid: str
    target_reference: str
    objective: str
    requestor_id: str
    rationale_digest: str
    proposed_at_epoch_seconds: int
    source_result_valid: bool
    source_result_accepted: bool
    source_binding_exact: bool
    requestor_authorized: bool
    target_reference_allowed: bool
    source_target_distinct: bool
    objective_allowed: bool
    rationale_valid: bool
    comparison_required: bool
    source_target_comparison_performed: bool
    external_review_required: bool
    explicit_authorization_decision_required: bool
    recovery_authority_granted: bool
    live_git_execution_performed: bool
    repository_mutation_performed: bool
    continues_v124_mutation_series: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    proposal_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def checkpoint_recovery_proposal_digest(
    proposal: CheckpointRecoveryProposal,
) -> str:
    payload = proposal.to_dict()
    payload.pop("proposal_digest", None)
    return canonical_digest(payload)
