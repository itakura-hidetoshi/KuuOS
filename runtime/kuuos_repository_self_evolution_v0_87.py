#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from itertools import combinations
from typing import Iterable

from runtime.kuuos_repository_frontier_certificate_types_v0_86 import (
    RepositoryFrontierCertificate,
)
from runtime.kuuos_repository_frontier_certificate_v0_86 import (
    repository_frontier_certificate_issues,
)
from runtime.kuuos_repository_self_evolution_types_v0_87 import (
    RepositoryEvolutionCandidate,
    RepositoryEvolutionPolicy,
    RepositorySelfEvolutionPortfolioCertificate,
    repository_self_evolution_portfolio_certificate_digest,
)


def repository_self_evolution_portfolio_certificate_issues(
    certificate: RepositorySelfEvolutionPortfolioCertificate,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not certificate.portfolio_id:
        issues.append("portfolio_id_missing")
    if not certificate.frontier_certificate_digest:
        issues.append("frontier_certificate_digest_missing")
    if not certificate.policy_digest:
        issues.append("policy_digest_missing")
    if certificate.certificate_digest != (
        repository_self_evolution_portfolio_certificate_digest(certificate)
    ):
        issues.append("certificate_digest_mismatch")
    if certificate.candidate_count != len(certificate.candidate_digests):
        issues.append("candidate_count_mismatch")
    if certificate.admissible_candidate_count != len(
        certificate.admissible_candidate_digests
    ):
        issues.append("admissible_candidate_count_mismatch")
    if certificate.selected_candidate_count != len(
        certificate.selected_candidate_digests
    ):
        issues.append("selected_candidate_count_mismatch")
    if certificate.selected_candidate_count != len(
        certificate.selected_frontier_commit_shas
    ):
        issues.append("selected_frontier_count_mismatch")
    if certificate.candidate_count > certificate.max_candidates:
        issues.append("candidate_bound_exceeded")
    if certificate.selected_candidate_count > certificate.max_selected_candidates:
        issues.append("selected_candidate_bound_exceeded")
    if certificate.enumerated_portfolio_count > certificate.max_portfolios:
        issues.append("portfolio_bound_exceeded")
    for name, values in (
        ("frontier_commits", certificate.frontier_commit_shas),
        ("candidate_digests", certificate.candidate_digests),
        ("admissible_candidate_digests", certificate.admissible_candidate_digests),
        ("selected_candidate_digests", certificate.selected_candidate_digests),
        ("selected_frontier_commits", certificate.selected_frontier_commit_shas),
        ("selected_changed_paths", certificate.selected_changed_paths),
    ):
        if tuple(sorted(set(values))) != values:
            issues.append(f"{name}_not_canonical")
    if not set(certificate.selected_candidate_digests).issubset(
        certificate.admissible_candidate_digests
    ):
        issues.append("selected_candidate_not_admissible")
    for field_name, valid in (
        ("source_frontier_invalid", certificate.source_frontier_valid),
        ("source_candidates_unbounded", certificate.source_candidates_bound),
        ("admissibility_not_recomputed", certificate.admissibility_recomputed),
        ("score_descent_not_strict", certificate.strict_score_descent),
        ("protected_paths_not_preserved", certificate.protected_paths_preserved),
        ("selection_not_reversible", certificate.reversible_selection),
        ("normal_form_not_preserved", certificate.normal_form_preserved),
        ("selected_paths_conflict", certificate.selected_paths_nonconflicting),
        ("frontier_selected_more_than_once", certificate.one_candidate_per_frontier),
        ("portfolio_not_deterministic_optimum", certificate.deterministic_optimum),
    ):
        if not valid:
            issues.append(field_name)
    if certificate.stable_no_change != (
        certificate.selected_candidate_count == 0
        and certificate.admissible_candidate_count == 0
    ):
        issues.append("stable_no_change_mismatch")
    if certificate.execution_authority_granted:
        issues.append("unexpected_execution_authority")
    return tuple(issues)


def _path_is_canonical(path: str) -> bool:
    if not path or path.startswith("/") or path.endswith("/"):
        return False
    parts = path.split("/")
    return all(part not in ("", ".", "..") for part in parts)


def _paths_conflict(left: str, right: str) -> bool:
    return (
        left == right
        or left.startswith(right + "/")
        or right.startswith(left + "/")
    )


def _candidate_paths_nonconflicting(
    candidates: tuple[RepositoryEvolutionCandidate, ...],
) -> bool:
    paths: list[str] = []
    for candidate in candidates:
        for path in candidate.changed_paths:
            if any(_paths_conflict(path, prior) for prior in paths):
                return False
            paths.append(path)
    return True


def _candidate_is_admissible(
    candidate: RepositoryEvolutionCandidate,
    policy: RepositoryEvolutionPolicy,
) -> bool:
    protected = any(
        _paths_conflict(path, protected_prefix)
        for path in candidate.changed_paths
        for protected_prefix in policy.protected_path_prefixes
    )
    return (
        candidate.score_improvement >= policy.minimum_score_improvement
        and candidate.risk_score <= policy.maximum_risk_score
        and len(candidate.changed_paths) <= policy.max_changed_paths_per_candidate
        and (candidate.reversible or not policy.require_reversible)
        and candidate.protected_paths_preserved
        and not protected
        and candidate.normal_form_preserved
        and not candidate.external_approval_required
    )


def _portfolio_key(
    portfolio: tuple[RepositoryEvolutionCandidate, ...],
) -> tuple[object, ...]:
    improvement = sum(candidate.score_improvement for candidate in portfolio)
    risk = sum(candidate.risk_score for candidate in portfolio)
    changed_path_count = sum(len(candidate.changed_paths) for candidate in portfolio)
    digests = tuple(sorted(candidate.digest for candidate in portfolio))
    return (-improvement, risk, changed_path_count, len(portfolio), digests)


def certify_repository_self_evolution_portfolio(
    portfolio_id: str,
    frontier_certificate: RepositoryFrontierCertificate,
    candidates: Iterable[RepositoryEvolutionCandidate],
    policy: RepositoryEvolutionPolicy,
) -> tuple[
    tuple[RepositoryEvolutionCandidate, ...],
    RepositorySelfEvolutionPortfolioCertificate,
]:
    if not portfolio_id:
        raise ValueError("portfolio_id_missing")
    if policy.max_candidates <= 0:
        raise ValueError("max_candidates_invalid")
    if policy.max_selected_candidates <= 0:
        raise ValueError("max_selected_candidates_invalid")
    if policy.max_changed_paths_per_candidate <= 0:
        raise ValueError("max_changed_paths_per_candidate_invalid")
    if policy.max_portfolios <= 0:
        raise ValueError("max_portfolios_invalid")
    if policy.minimum_score_improvement <= 0:
        raise ValueError("minimum_score_improvement_invalid")
    if policy.maximum_risk_score < 0:
        raise ValueError("maximum_risk_score_invalid")
    if tuple(sorted(set(policy.protected_path_prefixes))) != (
        policy.protected_path_prefixes
    ):
        raise ValueError("protected_path_prefixes_not_canonical")
    if any(not _path_is_canonical(path) for path in policy.protected_path_prefixes):
        raise ValueError("protected_path_prefix_invalid")

    frontier_issues = repository_frontier_certificate_issues(frontier_certificate)
    if frontier_issues:
        raise ValueError(f"frontier_certificate_invalid:{frontier_issues[0]}")

    source_candidates = tuple(candidates)
    if len(source_candidates) > policy.max_candidates:
        raise ValueError("repository_evolution_candidate_bound_exceeded")
    candidate_ids = tuple(candidate.candidate_id for candidate in source_candidates)
    if len(set(candidate_ids)) != len(candidate_ids):
        raise ValueError("repository_evolution_candidate_id_replay")
    candidate_digests = tuple(candidate.digest for candidate in source_candidates)
    if len(set(candidate_digests)) != len(candidate_digests):
        raise ValueError("repository_evolution_candidate_replay")

    frontier_set = set(frontier_certificate.frontier_commit_shas)
    for candidate in source_candidates:
        if not candidate.candidate_id:
            raise ValueError("repository_evolution_candidate_id_missing")
        if candidate.source_frontier_commit_sha not in frontier_set:
            raise ValueError("repository_evolution_source_not_in_frontier")
        if not candidate.proposal_digest:
            raise ValueError("repository_evolution_proposal_digest_missing")
        if not candidate.changed_paths:
            raise ValueError("repository_evolution_changed_paths_empty")
        if tuple(sorted(set(candidate.changed_paths))) != candidate.changed_paths:
            raise ValueError("repository_evolution_changed_paths_not_canonical")
        if any(not _path_is_canonical(path) for path in candidate.changed_paths):
            raise ValueError("repository_evolution_changed_path_invalid")
        if not _candidate_paths_nonconflicting((candidate,)):
            raise ValueError("repository_evolution_candidate_internal_path_conflict")
        if candidate.baseline_score < 0 or candidate.predicted_score < 0:
            raise ValueError("repository_evolution_score_negative")
        if candidate.risk_score < 0:
            raise ValueError("repository_evolution_risk_negative")

    canonical_candidates = tuple(sorted(source_candidates, key=lambda item: item.digest))
    admissible = tuple(
        candidate
        for candidate in canonical_candidates
        if _candidate_is_admissible(candidate, policy)
    )

    coherent_portfolios: list[tuple[RepositoryEvolutionCandidate, ...]] = []
    enumerated_count = 0
    maximum_size = min(policy.max_selected_candidates, len(admissible))
    for size in range(maximum_size + 1):
        for portfolio in combinations(admissible, size):
            enumerated_count += 1
            if enumerated_count > policy.max_portfolios:
                raise ValueError("repository_evolution_portfolio_bound_exceeded")
            tips = tuple(candidate.source_frontier_commit_sha for candidate in portfolio)
            if len(set(tips)) != len(tips):
                continue
            if not _candidate_paths_nonconflicting(portfolio):
                continue
            coherent_portfolios.append(portfolio)

    if not coherent_portfolios:
        raise ValueError("repository_evolution_coherent_portfolio_missing")
    selected = min(coherent_portfolios, key=_portfolio_key)

    selected_digests = tuple(sorted(candidate.digest for candidate in selected))
    selected_tips = tuple(sorted(
        candidate.source_frontier_commit_sha for candidate in selected
    ))
    selected_paths = tuple(sorted(
        path for candidate in selected for path in candidate.changed_paths
    ))
    strict_descent = all(
        candidate.predicted_score < candidate.baseline_score for candidate in selected
    )
    protected_preserved = all(
        candidate.protected_paths_preserved
        and not any(
            _paths_conflict(path, protected_prefix)
            for path in candidate.changed_paths
            for protected_prefix in policy.protected_path_prefixes
        )
        for candidate in selected
    )
    reversible_selection = all(
        candidate.reversible or not policy.require_reversible for candidate in selected
    )
    normal_form_preserved = all(
        candidate.normal_form_preserved for candidate in selected
    )
    paths_nonconflicting = _candidate_paths_nonconflicting(selected)
    one_per_frontier = len(selected_tips) == len(set(selected_tips))

    certificate = RepositorySelfEvolutionPortfolioCertificate(
        portfolio_id,
        frontier_certificate.certificate_digest,
        policy.digest,
        frontier_certificate.frontier_commit_shas,
        tuple(sorted(candidate_digests)),
        tuple(candidate.digest for candidate in admissible),
        selected_digests,
        selected_tips,
        selected_paths,
        len(source_candidates),
        len(admissible),
        len(selected),
        enumerated_count,
        policy.max_candidates,
        policy.max_selected_candidates,
        policy.max_portfolios,
        sum(candidate.score_improvement for candidate in selected),
        sum(candidate.risk_score for candidate in selected),
        True,
        True,
        True,
        strict_descent,
        protected_preserved,
        reversible_selection,
        normal_form_preserved,
        paths_nonconflicting,
        one_per_frontier,
        True,
        len(selected) == 0 and len(admissible) == 0,
        False,
        "",
    )
    certificate = replace(
        certificate,
        certificate_digest=(
            repository_self_evolution_portfolio_certificate_digest(certificate)
        ),
    )
    issues = repository_self_evolution_portfolio_certificate_issues(certificate)
    if issues:
        raise ValueError(f"self_evolution_portfolio_invalid:{issues[0]}")
    return selected, certificate
