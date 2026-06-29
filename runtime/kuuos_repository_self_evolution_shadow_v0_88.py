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
    for field_name, value in (
        ("evolution_candidate_digest", assessment.evolution_candidate_digest),
        ("source_frontier_commit_sha", assessment.source_frontier_commit_sha),
        ("git_revision_observation_digest", assessment.git_revision_observation_digest),
        ("repair_candidate_digest", assessment.repair_candidate_digest),
        ("source_snapshot_digest", assessment.source_snapshot_digest),
        ("source_observation_digest", assessment.source_observation_digest),
        ("shadow_snapshot_digest", assessment.shadow_snapshot_digest),
        ("shadow_observation_digest", assessment.shadow_observation_digest),
        ("normal_form_certificate_digest", assessment.normal_form_certificate_digest),
    ):
        if not value:
            issues.append(f"{field_name}_missing")
    if tuple(sorted(set(assessment.changed_paths))) != assessment.changed_paths:
        issues.append("changed_paths_not_canonical")
    if assessment.baseline_score < 0:
        issues.append("baseline_score_negative")
    if assessment.predicted_score < 0:
        issues.append("predicted_score_negative")
    if assessment.observed_score < 0:
        issues.append("observed_score_negative")
    if assessment.prediction_tolerance < 0:
        issues.append("prediction_tolerance_negative")
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
    if certificate.selected_candidate_count != len(
        certificate.selected_candidate_digests
    ):
        issues.append("selected_candidate_count_mismatch")
    if certificate.assessment_count != len(certificate.assessment_digests):
        issues.append("assessment_count_mismatch")
    if certificate.assessment_count != len(
        certificate.source_frontier_commit_shas
    ):
        issues.append("source_frontier_count_mismatch")
    if certificate.assessment_count != len(certificate.shadow_snapshot_digests):
        issues.append("shadow_snapshot_count_mismatch")
    if certificate.assessment_count != len(
        certificate.normal_form_certificate_digests
    ):
        issues.append("normal_form_count_mismatch")
    for name, values, require_unique in (
        ("selected_candidate_digests", certificate.selected_candidate_digests, True),
        ("assessment_digests", certificate.assessment_digests, True),
        ("source_frontier_commit_shas", certificate.source_frontier_commit_shas, True),
        ("shadow_snapshot_digests", certificate.shadow_snapshot_digests, False),
        ("normal_form_certificate_digests", certificate.normal_form_certificate_digests, False),
    ):
        expected = tuple(sorted(set(values))) if require_unique else tuple(sorted(values))
        if values != expected:
            issues.append(f"{name}_not_canonical")
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
            shadow_id,
            portfolio_certificate.certificate_digest,
            SHADOW_STABLE_NO_CHANGE,
            selected_digests,
            (),
            (),
            (),
            (),
            0,
            0,
            prediction_tolerance,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            "",
        )
        certificate = replace(
            certificate,
            certificate_digest=(
                repository_self_evolution_shadow_certificate_digest(certificate)
            ),
        )
        issues = repository_self_evolution_shadow_certificate_issues(certificate)
        if issues:
            raise ValueError(f"shadow_certificate_invalid:{issues[0]}")
        return (), certificate

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
    object_database_sources_only = True
    working_tree_ignored = True

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
        object_database_sources_only = (
            object_database_sources_only and revision.object_database_read
        )
        working_tree_ignored = working_tree_ignored and not revision.working_tree_read

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
            evolution.digest,
            evolution.source_frontier_commit_sha,
            revision.observation_digest,
            repair.digest,
            source_snapshot.digest,
            source_observation.digest,
            shadow_snapshot.digest,
            shadow_observation.digest,
            normal_form.certificate_digest,
            evolution.changed_paths,
            evolution.baseline_score,
            evolution.predicted_score,
            observed_score,
            prediction_error,
            prediction_tolerance,
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
            admissible,
            "",
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

    canonical_assessments = tuple(
        sorted(assessments, key=lambda assessment: assessment.evolution_candidate_digest)
    )
    all_bindings_exact = all(
        all((
            assessment.proposal_binding_exact,
            assessment.source_commit_binding_exact,
            assessment.source_snapshot_binding_exact,
            assessment.source_observation_binding_exact,
            assessment.changed_path_binding_exact,
            assessment.baseline_score_binding_exact,
        ))
        for assessment in canonical_assessments
    )
    strict_descent = all(
        assessment.strict_improvement_observed
        for assessment in canonical_assessments
    )
    predictions_within_tolerance = all(
        assessment.prediction_within_tolerance
        for assessment in canonical_assessments
    )
    protected_paths_preserved = all(
        assessment.protected_paths_preserved
        for assessment in canonical_assessments
    )
    reversible_realizations = all(
        assessment.reversible for assessment in canonical_assessments
    )
    exact_rollback = all(
        assessment.exact_shadow_rollback for assessment in canonical_assessments
    )
    normal_form_certified = all(
        assessment.normal_form_certified for assessment in canonical_assessments
    )
    portfolio_admissible = all(
        assessment.admissible for assessment in canonical_assessments
    )
    status = SHADOW_PASS if portfolio_admissible else SHADOW_REJECT

    certificate = RepositorySelfEvolutionShadowCertificate(
        shadow_id,
        portfolio_certificate.certificate_digest,
        status,
        selected_digests,
        tuple(sorted(
            assessment.assessment_digest for assessment in canonical_assessments
        )),
        tuple(sorted(
            assessment.source_frontier_commit_sha
            for assessment in canonical_assessments
        )),
        tuple(sorted(
            assessment.shadow_snapshot_digest
            for assessment in canonical_assessments
        )),
        tuple(sorted(
            assessment.normal_form_certificate_digest
            for assessment in canonical_assessments
        )),
        len(selected_digests),
        len(canonical_assessments),
        prediction_tolerance,
        set(input_digests) == set(selected_digests),
        len(set(input_digests)) == len(input_digests),
        object_database_sources_only,
        working_tree_ignored,
        all_bindings_exact,
        strict_descent,
        predictions_within_tolerance,
        protected_paths_preserved,
        reversible_realizations,
        exact_rollback,
        normal_form_certified,
        portfolio_admissible,
        False,
        False,
        False,
        False,
        "",
    )
    certificate = replace(
        certificate,
        certificate_digest=(
            repository_self_evolution_shadow_certificate_digest(certificate)
        ),
    )
    issues = repository_self_evolution_shadow_certificate_issues(certificate)
    if issues:
        raise ValueError(f"shadow_certificate_invalid:{issues[0]}")
    return canonical_assessments, certificate
