#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
)
from runtime.kuuos_repository_git_revision_types_v0_83 import (
    git_revision_observation_digest,
)
from runtime.kuuos_repository_self_evolution_shadow_types_v0_88 import (
    SHADOW_PASS,
    SHADOW_REJECT,
    SHADOW_STABLE_NO_CHANGE,
    RepositoryEvolutionShadowAssessment,
    RepositoryEvolutionShadowInput,
    RepositorySelfEvolutionShadowCertificate,
    repository_evolution_shadow_assessment_digest,
    repository_self_evolution_shadow_certificate_digest,
)
from runtime.kuuos_repository_self_evolution_types_v0_87 import (
    RepositorySelfEvolutionPortfolioCertificate,
)
from runtime.kuuos_repository_self_evolution_v0_87 import (
    repository_self_evolution_portfolio_certificate_issues,
)
from runtime.kuuos_repository_shadow_repair_v0_79 import (
    compare_repository_candidate_in_shadow,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def repository_evolution_shadow_assessment_issues(
    assessment: RepositoryEvolutionShadowAssessment,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        assessment.evolution_candidate_digest,
        assessment.source_frontier_commit_sha,
        assessment.git_revision_observation_digest,
        assessment.repair_candidate_digest,
        assessment.source_snapshot_digest,
        assessment.source_observation_digest,
        assessment.shadow_snapshot_digest,
        assessment.shadow_observation_digest,
        assessment.normal_form_certificate_digest,
    )
    if any(not value for value in required):
        issues.append("required_digest_missing")
    if tuple(sorted(set(assessment.changed_paths))) != assessment.changed_paths:
        issues.append("changed_paths_not_canonical")
    if min(
        assessment.baseline_score,
        assessment.predicted_score,
        assessment.observed_score,
        assessment.prediction_tolerance,
    ) < 0:
        issues.append("negative_numeric_field")
    if assessment.prediction_error != abs(
        assessment.observed_score - assessment.predicted_score
    ):
        issues.append("prediction_error_mismatch")
    if assessment.prediction_within_tolerance != (
        assessment.prediction_error <= assessment.prediction_tolerance
    ):
        issues.append("prediction_tolerance_mismatch")
    if assessment.strict_improvement_observed != (
        assessment.observed_score < assessment.baseline_score
    ):
        issues.append("strict_improvement_mismatch")
    expected_admissible = all((
        assessment.proposal_binding_exact,
        assessment.source_commit_binding_exact,
        assessment.source_snapshot_binding_exact,
        assessment.source_observation_binding_exact,
        assessment.changed_path_binding_exact,
        assessment.baseline_score_binding_exact,
        assessment.strict_improvement_observed,
        assessment.prediction_within_tolerance,
        assessment.protected_paths_preserved,
        assessment.reversible,
        assessment.exact_shadow_rollback,
        assessment.normal_form_certified,
    ))
    if assessment.admissible != expected_admissible:
        issues.append("admissibility_mismatch")
    if assessment.assessment_digest != (
        repository_evolution_shadow_assessment_digest(assessment)
    ):
        issues.append("assessment_digest_mismatch")
    return tuple(issues)


def repository_self_evolution_shadow_certificate_issues(
    certificate: RepositorySelfEvolutionShadowCertificate,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not certificate.shadow_id:
        issues.append("shadow_id_missing")
    if not certificate.portfolio_certificate_digest:
        issues.append("portfolio_certificate_digest_missing")
    if certificate.status not in (
        SHADOW_PASS,
        SHADOW_REJECT,
        SHADOW_STABLE_NO_CHANGE,
    ):
        issues.append("shadow_status_invalid")
    if certificate.prediction_tolerance < 0:
        issues.append("prediction_tolerance_negative")
    if certificate.certificate_digest != (
        repository_self_evolution_shadow_certificate_digest(certificate)
    ):
        issues.append("certificate_digest_mismatch")
    count_pairs = (
        (certificate.selected_candidate_count, certificate.selected_candidate_digests, "selected_candidate_count_mismatch"),
        (certificate.assessment_count, certificate.assessment_digests, "assessment_count_mismatch"),
        (certificate.assessment_count, certificate.source_frontier_commit_shas, "source_frontier_count_mismatch"),
        (certificate.assessment_count, certificate.shadow_snapshot_digests, "shadow_snapshot_count_mismatch"),
        (certificate.assessment_count, certificate.normal_form_certificate_digests, "normal_form_count_mismatch"),
    )
    for expected, values, issue in count_pairs:
        if expected != len(values):
            issues.append(issue)
    unique_sequences = (
        (certificate.selected_candidate_digests, "selected_candidate_digests_not_canonical"),
        (certificate.assessment_digests, "assessment_digests_not_canonical"),
        (certificate.source_frontier_commit_shas, "source_frontier_commit_shas_not_canonical"),
    )
    for values, issue in unique_sequences:
        if values != tuple(sorted(set(values))):
            issues.append(issue)
    for values, issue in (
        (certificate.shadow_snapshot_digests, "shadow_snapshot_digests_not_canonical"),
        (certificate.normal_form_certificate_digests, "normal_form_certificate_digests_not_canonical"),
    ):
        if values != tuple(sorted(values)):
            issues.append(issue)
    expected_admissible = all((
        certificate.exact_selected_coverage,
        certificate.unique_realization_per_candidate,
        certificate.object_database_sources_only,
        certificate.working_tree_ignored,
        certificate.all_bindings_exact,
        certificate.strict_score_descent_observed,
        certificate.predictions_within_tolerance,
        certificate.protected_paths_preserved,
        certificate.reversible_realizations,
        certificate.exact_shadow_rollback,
        certificate.normal_form_certified,
    ))
    if certificate.portfolio_shadow_admissible != expected_admissible:
        issues.append("portfolio_admissibility_mismatch")
    expected_stable = (
        certificate.selected_candidate_count == 0
        and certificate.assessment_count == 0
    )
    if certificate.stable_no_change != expected_stable:
        issues.append("stable_no_change_mismatch")
    if certificate.status == SHADOW_STABLE_NO_CHANGE:
        if not certificate.stable_no_change:
            issues.append("stable_status_without_fixed_point")
        if not certificate.portfolio_shadow_admissible:
            issues.append("stable_status_not_admissible")
    elif certificate.status == SHADOW_PASS:
        if certificate.stable_no_change:
            issues.append("pass_status_for_empty_portfolio")
        if not certificate.portfolio_shadow_admissible:
            issues.append("pass_status_not_admissible")
    elif certificate.status == SHADOW_REJECT:
        if certificate.stable_no_change:
            issues.append("reject_status_for_empty_portfolio")
        if certificate.portfolio_shadow_admissible:
            issues.append("reject_status_admissible")
    if certificate.patch_application_authority_granted:
        issues.append("unexpected_patch_application_authority")
    if certificate.commit_authority_granted:
        issues.append("unexpected_commit_authority")
    if certificate.reference_mutation_authority_granted:
        issues.append("unexpected_reference_mutation_authority")
    return tuple(issues)


def _restore_shadow_to_source(
    shadow_snapshot: RepositorySnapshot,
    source_snapshot: RepositorySnapshot,
    changed_paths: tuple[str, ...],
) -> bool:
    if shadow_snapshot.root_label != source_snapshot.root_label:
        return False
    if shadow_snapshot.all_paths != source_snapshot.all_paths:
        return False
    restored = shadow_snapshot.texts
    source_texts = source_snapshot.texts
    for path in changed_paths:
        if path not in restored or path not in source_texts:
            return False
        restored[path] = source_texts[path]
    reconstructed = RepositorySnapshot(
        shadow_snapshot.root_label,
        shadow_snapshot.all_paths,
        tuple(sorted(restored.items())),
    )
    return reconstructed.digest == source_snapshot.digest


def _finalize_certificate(
    certificate: RepositorySelfEvolutionShadowCertificate,
) -> RepositorySelfEvolutionShadowCertificate:
    certificate = replace(
        certificate,
        certificate_digest=(
            repository_self_evolution_shadow_certificate_digest(certificate)
        ),
    )
    issues = repository_self_evolution_shadow_certificate_issues(certificate)
    if issues:
        raise ValueError(f"shadow_certificate_invalid:{issues[0]}")
    return certificate


def certify_repository_self_evolution_shadow(
    shadow_id: str,
    portfolio_certificate: RepositorySelfEvolutionPortfolioCertificate,
    realizations: Iterable[RepositoryEvolutionShadowInput],
    *,
    prediction_tolerance: int = 0,
    max_states: int = 4096,
) -> tuple[
    tuple[RepositoryEvolutionShadowAssessment, ...],
    RepositorySelfEvolutionShadowCertificate,
]:
    if not shadow_id:
        raise ValueError("shadow_id_missing")
    if prediction_tolerance < 0:
        raise ValueError("prediction_tolerance_negative")
    if max_states <= 0:
        raise ValueError("max_states_invalid")
    portfolio_issues = repository_self_evolution_portfolio_certificate_issues(
        portfolio_certificate
    )
    if portfolio_issues:
        raise ValueError(f"portfolio_certificate_invalid:{portfolio_issues[0]}")

    inputs = tuple(realizations)
    selected_digests = portfolio_certificate.selected_candidate_digests
    if portfolio_certificate.stable_no_change:
        if inputs:
            raise ValueError("stable_portfolio_realization_forbidden")
        certificate = RepositorySelfEvolutionShadowCertificate(
            shadow_id=shadow_id,
            portfolio_certificate_digest=portfolio_certificate.certificate_digest,
            status=SHADOW_STABLE_NO_CHANGE,
            selected_candidate_digests=selected_digests,
            assessment_digests=(),
            source_frontier_commit_shas=(),
            shadow_snapshot_digests=(),
            normal_form_certificate_digests=(),
            selected_candidate_count=0,
            assessment_count=0,
            prediction_tolerance=prediction_tolerance,
            exact_selected_coverage=True,
            unique_realization_per_candidate=True,
            object_database_sources_only=True,
            working_tree_ignored=True,
            all_bindings_exact=True,
            strict_score_descent_observed=True,
            predictions_within_tolerance=True,
            protected_paths_preserved=True,
            reversible_realizations=True,
            exact_shadow_rollback=True,
            normal_form_certified=True,
            portfolio_shadow_admissible=True,
            stable_no_change=True,
            patch_application_authority_granted=False,
            commit_authority_granted=False,
            reference_mutation_authority_granted=False,
            certificate_digest="",
        )
        return (), _finalize_certificate(certificate)

    if not selected_digests:
        raise ValueError("selected_portfolio_empty_without_stable_flag")
    if len(inputs) != len(selected_digests):
        raise ValueError("shadow_realization_count_mismatch")
    input_digests = tuple(item.evolution_candidate.digest for item in inputs)
    if len(set(input_digests)) != len(input_digests):
        raise ValueError("shadow_realization_candidate_replay")
    if set(input_digests) != set(selected_digests):
        raise ValueError("shadow_selected_coverage_mismatch")

    assessments: list[RepositoryEvolutionShadowAssessment] = []
    for item in sorted(inputs, key=lambda value: value.evolution_candidate.digest):
        evolution = item.evolution_candidate
        revision = item.revision_observation
        source_snapshot = item.source_snapshot
        source_observation = item.source_observation
        repair = item.repair_candidate

        if revision.observation_digest != git_revision_observation_digest(revision):
            raise ValueError("git_revision_observation_digest_mismatch")
        if not revision.object_database_read:
            raise ValueError("shadow_source_not_from_object_database")
        if revision.working_tree_read:
            raise ValueError("shadow_working_tree_source_forbidden")

        proposal_binding = evolution.proposal_digest == repair.digest
        source_commit_binding = (
            evolution.source_frontier_commit_sha == revision.current_commit_sha
        )
        source_snapshot_binding = (
            revision.current_snapshot_digest == source_snapshot.digest
        )
        source_observation_binding = (
            source_observation.snapshot_digest == source_snapshot.digest
            and repair.source_snapshot_digest == source_snapshot.digest
            and repair.source_observation_digest == source_observation.digest
        )
        patch_paths = tuple(sorted(patch.path for patch in repair.patches))
        if len(set(patch_paths)) != len(patch_paths):
            raise ValueError("shadow_repair_patch_path_replay")
        changed_path_binding = patch_paths == evolution.changed_paths
        baseline_binding = (
            evolution.baseline_score == source_observation.weighted_defect_score
        )
        for name, valid in (
            ("proposal_binding_mismatch", proposal_binding),
            ("source_commit_binding_mismatch", source_commit_binding),
            ("source_snapshot_binding_mismatch", source_snapshot_binding),
            ("source_observation_binding_mismatch", source_observation_binding),
            ("changed_path_binding_mismatch", changed_path_binding),
            ("baseline_score_binding_mismatch", baseline_binding),
        ):
            if not valid:
                raise ValueError(name)

        shadow_snapshot, shadow_observation, repair_assessment = (
            compare_repository_candidate_in_shadow(
                source_snapshot,
                source_observation,
                repair,
            )
        )
        normal_form = certify_repository_alignment_normal_form(
            shadow_snapshot,
            max_states=max_states,
        )
        normal_form_certified = all((
            normal_form.all_transitions_strictly_decreasing,
            normal_form.all_terminals_fixed_points,
            normal_form.unique_terminal,
            normal_form.deterministic_trace_matches_terminal,
            not normal_form.external_approval_required,
        ))
        observed_score = shadow_observation.weighted_defect_score
        prediction_error = abs(observed_score - evolution.predicted_score)
        prediction_within_tolerance = prediction_error <= prediction_tolerance
        strict_improvement = observed_score < evolution.baseline_score
        protected_paths_preserved = all((
            evolution.protected_paths_preserved,
            repair.protected_paths_preserved,
            repair_assessment.protected_paths_preserved,
        ))
        exact_rollback = _restore_shadow_to_source(
            shadow_snapshot,
            source_snapshot,
            evolution.changed_paths,
        )
        reversible = evolution.reversible and exact_rollback
        admissible = all((
            proposal_binding,
            source_commit_binding,
            source_snapshot_binding,
            source_observation_binding,
            changed_path_binding,
            baseline_binding,
            strict_improvement,
            prediction_within_tolerance,
            protected_paths_preserved,
            reversible,
            exact_rollback,
            normal_form_certified,
        ))
        assessment = RepositoryEvolutionShadowAssessment(
            evolution_candidate_digest=evolution.digest,
            source_frontier_commit_sha=evolution.source_frontier_commit_sha,
            git_revision_observation_digest=revision.observation_digest,
            repair_candidate_digest=repair.digest,
            source_snapshot_digest=source_snapshot.digest,
            source_observation_digest=source_observation.digest,
            shadow_snapshot_digest=shadow_snapshot.digest,
            shadow_observation_digest=shadow_observation.digest,
            normal_form_certificate_digest=normal_form.certificate_digest,
            changed_paths=evolution.changed_paths,
            baseline_score=evolution.baseline_score,
            predicted_score=evolution.predicted_score,
            observed_score=observed_score,
            prediction_error=prediction_error,
            prediction_tolerance=prediction_tolerance,
            proposal_binding_exact=proposal_binding,
            source_commit_binding_exact=source_commit_binding,
            source_snapshot_binding_exact=source_snapshot_binding,
            source_observation_binding_exact=source_observation_binding,
            changed_path_binding_exact=changed_path_binding,
            baseline_score_binding_exact=baseline_binding,
            strict_improvement_observed=strict_improvement,
            prediction_within_tolerance=prediction_within_tolerance,
            protected_paths_preserved=protected_paths_preserved,
            reversible=reversible,
            exact_shadow_rollback=exact_rollback,
            normal_form_certified=normal_form_certified,
            admissible=admissible,
            assessment_digest="",
        )
        assessment = replace(
            assessment,
            assessment_digest=(
                repository_evolution_shadow_assessment_digest(assessment)
            ),
        )
        issues = repository_evolution_shadow_assessment_issues(assessment)
        if issues:
            raise ValueError(f"shadow_assessment_invalid:{issues[0]}")
        assessments.append(assessment)

    canonical = tuple(sorted(
        assessments,
        key=lambda assessment: assessment.evolution_candidate_digest,
    ))
    all_bindings_exact = all(
        all((
            item.proposal_binding_exact,
            item.source_commit_binding_exact,
            item.source_snapshot_binding_exact,
            item.source_observation_binding_exact,
            item.changed_path_binding_exact,
            item.baseline_score_binding_exact,
        ))
        for item in canonical
    )
    strict_descent = all(item.strict_improvement_observed for item in canonical)
    predictions_bounded = all(item.prediction_within_tolerance for item in canonical)
    protected = all(item.protected_paths_preserved for item in canonical)
    reversible = all(item.reversible for item in canonical)
    exact_rollback = all(item.exact_shadow_rollback for item in canonical)
    normal_form = all(item.normal_form_certified for item in canonical)
    portfolio_admissible = all(item.admissible for item in canonical)
    status = SHADOW_PASS if portfolio_admissible else SHADOW_REJECT

    certificate = RepositorySelfEvolutionShadowCertificate(
        shadow_id=shadow_id,
        portfolio_certificate_digest=portfolio_certificate.certificate_digest,
        status=status,
        selected_candidate_digests=selected_digests,
        assessment_digests=tuple(sorted(item.assessment_digest for item in canonical)),
        source_frontier_commit_shas=tuple(sorted(item.source_frontier_commit_sha for item in canonical)),
        shadow_snapshot_digests=tuple(sorted(item.shadow_snapshot_digest for item in canonical)),
        normal_form_certificate_digests=tuple(sorted(item.normal_form_certificate_digest for item in canonical)),
        selected_candidate_count=len(selected_digests),
        assessment_count=len(canonical),
        prediction_tolerance=prediction_tolerance,
        exact_selected_coverage=set(input_digests) == set(selected_digests),
        unique_realization_per_candidate=len(set(input_digests)) == len(input_digests),
        object_database_sources_only=all(item.revision_observation.object_database_read for item in inputs),
        working_tree_ignored=all(not item.revision_observation.working_tree_read for item in inputs),
        all_bindings_exact=all_bindings_exact,
        strict_score_descent_observed=strict_descent,
        predictions_within_tolerance=predictions_bounded,
        protected_paths_preserved=protected,
        reversible_realizations=reversible,
        exact_shadow_rollback=exact_rollback,
        normal_form_certified=normal_form,
        portfolio_shadow_admissible=portfolio_admissible,
        stable_no_change=False,
        patch_application_authority_granted=False,
        commit_authority_granted=False,
        reference_mutation_authority_granted=False,
        certificate_digest="",
    )
    return canonical, _finalize_certificate(certificate)
