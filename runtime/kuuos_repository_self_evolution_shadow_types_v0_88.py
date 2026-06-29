#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_git_revision_types_v0_83 import GitRevisionObservation
from runtime.kuuos_repository_self_evolution_types_v0_87 import RepositoryEvolutionCandidate
from runtime.kuuos_repository_structure_types_v0_79 import (
    RepositoryObservation,
    RepositoryRepairCandidate,
    RepositorySnapshot,
)

VERSION = "kuuos_repository_self_evolution_shadow_v0_88"

SHADOW_PASS = "REPOSITORY_SELF_EVOLUTION_SHADOW_PASS"
SHADOW_REJECT = "REPOSITORY_SELF_EVOLUTION_SHADOW_REJECT"
SHADOW_STABLE_NO_CHANGE = "REPOSITORY_SELF_EVOLUTION_SHADOW_STABLE_NO_CHANGE"


@dataclass(frozen=True)
class RepositoryEvolutionShadowInput:
    evolution_candidate: RepositoryEvolutionCandidate
    revision_observation: GitRevisionObservation
    source_snapshot: RepositorySnapshot
    source_observation: RepositoryObservation
    repair_candidate: RepositoryRepairCandidate


@dataclass(frozen=True)
class RepositoryEvolutionShadowAssessment:
    evolution_candidate_digest: str
    source_frontier_commit_sha: str
    git_revision_observation_digest: str
    repair_candidate_digest: str
    source_snapshot_digest: str
    source_observation_digest: str
    shadow_snapshot_digest: str
    shadow_observation_digest: str
    normal_form_certificate_digest: str
    changed_paths: tuple[str, ...]
    baseline_score: int
    predicted_score: int
    observed_score: int
    prediction_error: int
    prediction_tolerance: int
    proposal_binding_exact: bool
    source_commit_binding_exact: bool
    source_snapshot_binding_exact: bool
    source_observation_binding_exact: bool
    changed_path_binding_exact: bool
    baseline_score_binding_exact: bool
    strict_improvement_observed: bool
    prediction_within_tolerance: bool
    protected_paths_preserved: bool
    reversible: bool
    exact_shadow_rollback: bool
    normal_form_certified: bool
    admissible: bool
    assessment_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_evolution_shadow_assessment_digest(
    assessment: RepositoryEvolutionShadowAssessment,
) -> str:
    payload = assessment.to_dict()
    payload.pop("assessment_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositorySelfEvolutionShadowCertificate:
    shadow_id: str
    portfolio_certificate_digest: str
    status: str
    selected_candidate_digests: tuple[str, ...]
    assessment_digests: tuple[str, ...]
    source_frontier_commit_shas: tuple[str, ...]
    shadow_snapshot_digests: tuple[str, ...]
    normal_form_certificate_digests: tuple[str, ...]
    selected_candidate_count: int
    assessment_count: int
    prediction_tolerance: int
    exact_selected_coverage: bool
    unique_realization_per_candidate: bool
    object_database_sources_only: bool
    working_tree_ignored: bool
    all_bindings_exact: bool
    strict_score_descent_observed: bool
    predictions_within_tolerance: bool
    protected_paths_preserved: bool
    reversible_realizations: bool
    exact_shadow_rollback: bool
    normal_form_certified: bool
    portfolio_shadow_admissible: bool
    stable_no_change: bool
    patch_application_authority_granted: bool
    commit_authority_granted: bool
    reference_mutation_authority_granted: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_self_evolution_shadow_certificate_digest(
    certificate: RepositorySelfEvolutionShadowCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
