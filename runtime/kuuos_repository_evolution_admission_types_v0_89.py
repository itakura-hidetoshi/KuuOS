#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_git_revision_types_v0_83 import GitRevisionObservation
from runtime.kuuos_repository_self_evolution_shadow_types_v0_88 import (
    RepositoryEvolutionShadowAssessment,
    RepositorySelfEvolutionShadowCertificate,
)

VERSION = "kuuos_repository_evolution_admission_v0_89"

ADMISSION_PROPOSED = "REPOSITORY_EVOLUTION_ADMISSION_PROPOSED"
ADMISSION_REJECTED = "REPOSITORY_EVOLUTION_ADMISSION_REJECTED"
ADMISSION_STABLE_NO_CHANGE = "REPOSITORY_EVOLUTION_ADMISSION_STABLE_NO_CHANGE"


@dataclass(frozen=True)
class RepositoryShadowReplayReceipt:
    replay_id: str
    issued_at_epoch_seconds: int
    shadow_certificate: RepositorySelfEvolutionShadowCertificate
    shadow_assessments: tuple[RepositoryEvolutionShadowAssessment, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_shadow_replay_receipt_digest(
    receipt: RepositoryShadowReplayReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryEvolutionAdmissionCertificate:
    admission_id: str
    status: str
    portfolio_certificate_digest: str
    replay_receipt_digests: tuple[str, ...]
    shadow_certificate_digests: tuple[str, ...]
    selected_candidate_digests: tuple[str, ...]
    source_frontier_commit_shas: tuple[str, ...]
    source_snapshot_digests: tuple[str, ...]
    shadow_snapshot_digests: tuple[str, ...]
    normal_form_certificate_digests: tuple[str, ...]
    current_revision_observation_digests: tuple[str, ...]
    replay_count: int
    required_replay_count: int
    evaluated_at_epoch_seconds: int
    max_certificate_age_seconds: int
    all_shadow_pass: bool
    replay_count_satisfied: bool
    replay_receipts_unique: bool
    replay_results_identical: bool
    certificates_fresh: bool
    no_future_certificates: bool
    current_revision_observations_complete: bool
    source_revisions_unchanged: bool
    source_snapshots_unchanged: bool
    object_database_sources_only: bool
    working_tree_ignored: bool
    approval_policy_digest: str
    external_approval_required: bool
    external_approval_granted: bool
    admission_proposal_generated: bool
    stable_no_change: bool
    patch_application_authority_granted: bool
    commit_authority_granted: bool
    reference_mutation_authority_granted: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_evolution_admission_certificate_digest(
    certificate: RepositoryEvolutionAdmissionCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
