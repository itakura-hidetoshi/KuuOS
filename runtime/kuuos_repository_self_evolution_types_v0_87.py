#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_self_evolution_portfolio_v0_87"


@dataclass(frozen=True)
class RepositoryEvolutionCandidate:
    candidate_id: str
    source_frontier_commit_sha: str
    proposal_digest: str
    changed_paths: tuple[str, ...]
    baseline_score: int
    predicted_score: int
    risk_score: int
    reversible: bool
    protected_paths_preserved: bool
    normal_form_preserved: bool
    external_approval_required: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def score_improvement(self) -> int:
        return self.baseline_score - self.predicted_score

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryEvolutionPolicy:
    max_candidates: int = 16
    max_selected_candidates: int = 4
    max_changed_paths_per_candidate: int = 8
    max_portfolios: int = 65536
    minimum_score_improvement: int = 1
    maximum_risk_score: int = 100
    require_reversible: bool = True
    protected_path_prefixes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositorySelfEvolutionPortfolioCertificate:
    portfolio_id: str
    frontier_certificate_digest: str
    policy_digest: str
    frontier_commit_shas: tuple[str, ...]
    candidate_digests: tuple[str, ...]
    admissible_candidate_digests: tuple[str, ...]
    selected_candidate_digests: tuple[str, ...]
    selected_frontier_commit_shas: tuple[str, ...]
    selected_changed_paths: tuple[str, ...]
    candidate_count: int
    admissible_candidate_count: int
    selected_candidate_count: int
    enumerated_portfolio_count: int
    max_candidates: int
    max_selected_candidates: int
    max_portfolios: int
    aggregate_score_improvement: int
    aggregate_risk_score: int
    source_frontier_valid: bool
    source_candidates_bound: bool
    admissibility_recomputed: bool
    strict_score_descent: bool
    protected_paths_preserved: bool
    reversible_selection: bool
    normal_form_preserved: bool
    selected_paths_nonconflicting: bool
    one_candidate_per_frontier: bool
    deterministic_optimum: bool
    stable_no_change: bool
    execution_authority_granted: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_self_evolution_portfolio_certificate_digest(
    certificate: RepositorySelfEvolutionPortfolioCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
