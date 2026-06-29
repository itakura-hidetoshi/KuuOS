#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_evolution_admission_types_v0_89 import (
    ADMISSION_PROPOSED,
    ADMISSION_REJECTED,
    ADMISSION_STABLE_NO_CHANGE,
    RepositoryEvolutionAdmissionCertificate,
    RepositoryShadowReplayReceipt,
    repository_evolution_admission_certificate_digest,
    repository_shadow_replay_receipt_digest,
)
from runtime.kuuos_repository_git_revision_types_v0_83 import (
    GitRevisionObservation,
    git_revision_observation_digest,
)
from runtime.kuuos_repository_self_evolution_shadow_types_v0_88 import (
    SHADOW_PASS,
    SHADOW_REJECT,
    SHADOW_STABLE_NO_CHANGE,
    RepositoryEvolutionShadowAssessment,
    RepositorySelfEvolutionShadowCertificate,
)
from runtime.kuuos_repository_self_evolution_shadow_v0_88 import (
    repository_evolution_shadow_assessment_issues,
    repository_self_evolution_shadow_certificate_issues,
)


def _source_binding_digest(commit_sha: str, snapshot_digest: str) -> str:
    return canonical_digest({
        "source_frontier_commit_sha": commit_sha,
        "source_snapshot_digest": snapshot_digest,
    })


def _source_bindings(
    assessments: tuple[RepositoryEvolutionShadowAssessment, ...],
) -> tuple[tuple[str, str], ...]:
    bindings = tuple(sorted(
        (
            assessment.source_frontier_commit_sha,
            assessment.source_snapshot_digest,
        )
        for assessment in assessments
    ))
    if len({commit_sha for commit_sha, _ in bindings}) != len(bindings):
        raise ValueError("shadow_source_commit_replay")
    return bindings


def repository_shadow_replay_receipt_issues(
    receipt: RepositoryShadowReplayReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not receipt.replay_id:
        issues.append("replay_id_missing")
    if receipt.issued_at_epoch_seconds < 0:
        issues.append("issued_at_negative")
    if repository_self_evolution_shadow_certificate_issues(
        receipt.shadow_certificate
    ):
        issues.append("shadow_certificate_invalid")
    canonical_assessments = tuple(sorted(
        receipt.shadow_assessments,
        key=lambda item: item.evolution_candidate_digest,
    ))
    if canonical_assessments != receipt.shadow_assessments:
        issues.append("shadow_assessments_not_canonical")
    if len({item.evolution_candidate_digest for item in canonical_assessments}) != len(
        canonical_assessments
    ):
        issues.append("shadow_assessment_candidate_replay")
    if any(repository_evolution_shadow_assessment_issues(item) for item in canonical_assessments):
        issues.append("shadow_assessment_invalid")
    certificate = receipt.shadow_certificate
    assessment_digests = tuple(sorted(
        item.assessment_digest for item in canonical_assessments
    ))
    if assessment_digests != certificate.assessment_digests:
        issues.append("assessment_digest_coverage_mismatch")
    if len(canonical_assessments) != certificate.assessment_count:
        issues.append("assessment_count_mismatch")
    source_commits = tuple(sorted(
        item.source_frontier_commit_sha for item in canonical_assessments
    ))
    if source_commits != certificate.source_frontier_commit_shas:
        issues.append("source_commit_coverage_mismatch")
    shadow_snapshots = tuple(sorted(
        item.shadow_snapshot_digest for item in canonical_assessments
    ))
    if shadow_snapshots != certificate.shadow_snapshot_digests:
        issues.append("shadow_snapshot_coverage_mismatch")
    normal_forms = tuple(sorted(
        item.normal_form_certificate_digest for item in canonical_assessments
    ))
    if normal_forms != certificate.normal_form_certificate_digests:
        issues.append("normal_form_coverage_mismatch")
    if certificate.status == SHADOW_STABLE_NO_CHANGE and canonical_assessments:
        issues.append("stable_shadow_has_assessments")
    if certificate.status != SHADOW_STABLE_NO_CHANGE and not canonical_assessments:
        issues.append("nonstable_shadow_missing_assessments")
    if receipt.receipt_digest != repository_shadow_replay_receipt_digest(receipt):
        issues.append("receipt_digest_mismatch")
    return tuple(issues)


def build_repository_shadow_replay_receipt(
    replay_id: str,
    issued_at_epoch_seconds: int,
    shadow_assessments: Iterable[RepositoryEvolutionShadowAssessment],
    shadow_certificate: RepositorySelfEvolutionShadowCertificate,
) -> RepositoryShadowReplayReceipt:
    canonical_assessments = tuple(sorted(
        shadow_assessments,
        key=lambda item: item.evolution_candidate_digest,
    ))
    receipt = RepositoryShadowReplayReceipt(
        replay_id=replay_id,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        shadow_certificate=shadow_certificate,
        shadow_assessments=canonical_assessments,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=repository_shadow_replay_receipt_digest(receipt),
    )
    issues = repository_shadow_replay_receipt_issues(receipt)
    if issues:
        raise ValueError(f"shadow_replay_receipt_invalid:{issues[0]}")
    return receipt


def repository_evolution_admission_certificate_issues(
    certificate: RepositoryEvolutionAdmissionCertificate,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not certificate.admission_id:
        issues.append("admission_id_missing")
    if not certificate.portfolio_certificate_digest:
        issues.append("portfolio_certificate_digest_missing")
    if not certificate.approval_policy_digest:
        issues.append("approval_policy_digest_missing")
    if certificate.status not in (
        ADMISSION_PROPOSED,
        ADMISSION_REJECTED,
        ADMISSION_STABLE_NO_CHANGE,
    ):
        issues.append("admission_status_invalid")
    if certificate.replay_count != len(certificate.replay_receipt_digests):
        issues.append("replay_count_mismatch")
    if certificate.required_replay_count < 2:
        issues.append("required_replay_count_too_small")
    if certificate.evaluated_at_epoch_seconds < 0:
        issues.append("evaluated_at_negative")
    if certificate.max_certificate_age_seconds <= 0:
        issues.append("max_certificate_age_invalid")
    unique_fields = (
        (certificate.replay_receipt_digests, "replay_receipt_digests"),
        (certificate.shadow_certificate_digests, "shadow_certificate_digests"),
        (certificate.selected_candidate_digests, "selected_candidate_digests"),
        (certificate.source_frontier_commit_shas, "source_frontier_commit_shas"),
        (certificate.source_snapshot_digests, "source_snapshot_digests"),
        (certificate.source_revision_binding_digests, "source_revision_binding_digests"),
        (certificate.current_revision_observation_digests, "current_revision_observation_digests"),
    )
    for values, name in unique_fields:
        if values != tuple(sorted(set(values))):
            issues.append(f"{name}_not_canonical")
    for values, name in (
        (certificate.shadow_snapshot_digests, "shadow_snapshot_digests"),
        (certificate.normal_form_certificate_digests, "normal_form_certificate_digests"),
    ):
        if values != tuple(sorted(values)):
            issues.append(f"{name}_not_canonical")
    if not certificate.external_approval_required:
        issues.append("external_approval_not_required")
    if certificate.external_approval_granted:
        issues.append("unexpected_external_approval")
    if certificate.patch_application_authority_granted:
        issues.append("unexpected_patch_application_authority")
    if certificate.commit_authority_granted:
        issues.append("unexpected_commit_authority")
    if certificate.reference_mutation_authority_granted:
        issues.append("unexpected_reference_mutation_authority")

    technical_admissible = all((
        certificate.all_shadow_pass,
        certificate.replay_count_satisfied,
        certificate.replay_receipts_unique,
        certificate.replay_results_identical,
        certificate.certificates_fresh,
        certificate.no_future_certificates,
        certificate.current_revision_observations_complete,
        certificate.source_revisions_unchanged,
        certificate.source_snapshots_unchanged,
        certificate.object_database_sources_only,
        certificate.working_tree_ignored,
    ))
    if certificate.admission_proposal_generated != (
        technical_admissible and not certificate.stable_no_change
    ):
        issues.append("admission_proposal_mismatch")
    if certificate.status == ADMISSION_PROPOSED:
        if not certificate.admission_proposal_generated:
            issues.append("proposed_status_without_proposal")
        if certificate.stable_no_change:
            issues.append("proposed_status_for_stable_state")
    elif certificate.status == ADMISSION_STABLE_NO_CHANGE:
        if not certificate.stable_no_change:
            issues.append("stable_status_without_stable_state")
        if certificate.admission_proposal_generated:
            issues.append("stable_status_with_proposal")
        if certificate.selected_candidate_digests:
            issues.append("stable_status_with_candidates")
    elif certificate.status == ADMISSION_REJECTED:
        if certificate.admission_proposal_generated:
            issues.append("rejected_status_with_proposal")
        if certificate.stable_no_change:
            issues.append("rejected_status_marked_stable")
    if certificate.certificate_digest != (
        repository_evolution_admission_certificate_digest(certificate)
    ):
        issues.append("certificate_digest_mismatch")
    return tuple(issues)


def _receipt_signature(receipt: RepositoryShadowReplayReceipt) -> tuple[object, ...]:
    certificate = receipt.shadow_certificate
    bindings = _source_bindings(receipt.shadow_assessments)
    return (
        certificate.portfolio_certificate_digest,
        certificate.selected_candidate_digests,
        bindings,
        certificate.shadow_snapshot_digests,
        certificate.normal_form_certificate_digests,
    )


def _finalize_admission_certificate(
    certificate: RepositoryEvolutionAdmissionCertificate,
) -> RepositoryEvolutionAdmissionCertificate:
    certificate = replace(
        certificate,
        certificate_digest=(
            repository_evolution_admission_certificate_digest(certificate)
        ),
    )
    issues = repository_evolution_admission_certificate_issues(certificate)
    if issues:
        raise ValueError(f"admission_certificate_invalid:{issues[0]}")
    return certificate


def certify_repository_evolution_admission(
    admission_id: str,
    replay_receipts: Iterable[RepositoryShadowReplayReceipt],
    current_revision_observations: Iterable[GitRevisionObservation],
    *,
    approval_policy_digest: str,
    evaluated_at_epoch_seconds: int,
    max_certificate_age_seconds: int,
    required_replay_count: int = 2,
) -> RepositoryEvolutionAdmissionCertificate:
    if not admission_id:
        raise ValueError("admission_id_missing")
    if not approval_policy_digest:
        raise ValueError("approval_policy_digest_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("evaluated_at_negative")
    if max_certificate_age_seconds <= 0:
        raise ValueError("max_certificate_age_invalid")
    if required_replay_count < 2:
        raise ValueError("required_replay_count_too_small")

    receipts = tuple(sorted(replay_receipts, key=lambda item: item.receipt_digest))
    if not receipts:
        raise ValueError("shadow_replay_receipts_empty")
    for receipt in receipts:
        issues = repository_shadow_replay_receipt_issues(receipt)
        if issues:
            raise ValueError(f"shadow_replay_receipt_invalid:{issues[0]}")

    statuses = {receipt.shadow_certificate.status for receipt in receipts}
    stable_mode = statuses == {SHADOW_STABLE_NO_CHANGE}
    if SHADOW_STABLE_NO_CHANGE in statuses and not stable_mode:
        raise ValueError("shadow_status_mode_mismatch")
    if not statuses.issubset({SHADOW_PASS, SHADOW_REJECT, SHADOW_STABLE_NO_CHANGE}):
        raise ValueError("shadow_status_invalid")

    replay_ids = tuple(receipt.replay_id for receipt in receipts)
    replay_digests = tuple(receipt.receipt_digest for receipt in receipts)
    replay_unique = (
        len(set(replay_ids)) == len(replay_ids)
        and len(set(replay_digests)) == len(replay_digests)
    )
    replay_count_satisfied = len(receipts) >= required_replay_count
    signatures = tuple(_receipt_signature(receipt) for receipt in receipts)
    replay_results_identical = all(signature == signatures[0] for signature in signatures)
    no_future = all(
        receipt.issued_at_epoch_seconds <= evaluated_at_epoch_seconds
        for receipt in receipts
    )
    fresh = all(
        0 <= evaluated_at_epoch_seconds - receipt.issued_at_epoch_seconds
        <= max_certificate_age_seconds
        for receipt in receipts
    )
    all_shadow_pass = statuses == {SHADOW_PASS}

    reference = receipts[0]
    reference_certificate = reference.shadow_certificate
    reference_bindings = _source_bindings(reference.shadow_assessments)
    expected_by_commit = dict(reference_bindings)

    observations = tuple(sorted(
        current_revision_observations,
        key=lambda item: item.current_commit_sha,
    ))
    for observation in observations:
        if observation.observation_digest != git_revision_observation_digest(observation):
            raise ValueError("current_revision_observation_digest_mismatch")
    if len({item.current_commit_sha for item in observations}) != len(observations):
        raise ValueError("current_revision_observation_replay")
    current_by_commit = {
        item.current_commit_sha: item.current_snapshot_digest
        for item in observations
    }
    expected_commits = set(expected_by_commit)
    current_commits = set(current_by_commit)
    observations_complete = current_commits == expected_commits
    revisions_unchanged = observations_complete
    snapshots_unchanged = observations_complete and all(
        current_by_commit[commit_sha] == snapshot_digest
        for commit_sha, snapshot_digest in reference_bindings
    )
    object_database_only = all(item.object_database_read for item in observations)
    working_tree_ignored = all(not item.working_tree_read for item in observations)

    technical_admissible = all((
        all_shadow_pass,
        replay_count_satisfied,
        replay_unique,
        replay_results_identical,
        fresh,
        no_future,
        observations_complete,
        revisions_unchanged,
        snapshots_unchanged,
        object_database_only,
        working_tree_ignored,
    ))
    stable_valid = all((
        stable_mode,
        replay_count_satisfied,
        replay_unique,
        replay_results_identical,
        fresh,
        no_future,
        observations_complete,
        revisions_unchanged,
        snapshots_unchanged,
        object_database_only,
        working_tree_ignored,
        not reference_certificate.selected_candidate_digests,
    ))
    if stable_valid:
        status = ADMISSION_STABLE_NO_CHANGE
        stable_no_change = True
        proposal_generated = False
    elif technical_admissible:
        status = ADMISSION_PROPOSED
        stable_no_change = False
        proposal_generated = True
    else:
        status = ADMISSION_REJECTED
        stable_no_change = False
        proposal_generated = False

    source_snapshot_digests = tuple(sorted(set(expected_by_commit.values())))
    source_binding_digests = tuple(sorted(
        _source_binding_digest(commit_sha, snapshot_digest)
        for commit_sha, snapshot_digest in reference_bindings
    ))
    certificate = RepositoryEvolutionAdmissionCertificate(
        admission_id=admission_id,
        status=status,
        portfolio_certificate_digest=reference_certificate.portfolio_certificate_digest,
        replay_receipt_digests=tuple(sorted(set(replay_digests))),
        shadow_certificate_digests=tuple(sorted(set(
            receipt.shadow_certificate.certificate_digest for receipt in receipts
        ))),
        selected_candidate_digests=reference_certificate.selected_candidate_digests,
        source_frontier_commit_shas=reference_certificate.source_frontier_commit_shas,
        source_snapshot_digests=source_snapshot_digests,
        source_revision_binding_digests=source_binding_digests,
        shadow_snapshot_digests=reference_certificate.shadow_snapshot_digests,
        normal_form_certificate_digests=reference_certificate.normal_form_certificate_digests,
        current_revision_observation_digests=tuple(sorted(set(
            item.observation_digest for item in observations
        ))),
        replay_count=len(receipts),
        required_replay_count=required_replay_count,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        max_certificate_age_seconds=max_certificate_age_seconds,
        all_shadow_pass=all_shadow_pass,
        replay_count_satisfied=replay_count_satisfied,
        replay_receipts_unique=replay_unique,
        replay_results_identical=replay_results_identical,
        certificates_fresh=fresh,
        no_future_certificates=no_future,
        current_revision_observations_complete=observations_complete,
        source_revisions_unchanged=revisions_unchanged,
        source_snapshots_unchanged=snapshots_unchanged,
        object_database_sources_only=object_database_only,
        working_tree_ignored=working_tree_ignored,
        approval_policy_digest=approval_policy_digest,
        external_approval_required=True,
        external_approval_granted=False,
        admission_proposal_generated=proposal_generated,
        stable_no_change=stable_no_change,
        patch_application_authority_granted=False,
        commit_authority_granted=False,
        reference_mutation_authority_granted=False,
        certificate_digest="",
    )
    return _finalize_admission_certificate(certificate)
