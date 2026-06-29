#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from pathlib import PurePosixPath

from runtime.kuuos_repository_external_approval_types_v0_90 import (
    APPROVAL_ACCEPTED,
    RepositoryEvolutionExternalApprovalCertificate,
)
from runtime.kuuos_repository_external_approval_v0_90 import (
    repository_evolution_external_approval_certificate_issues,
)
from runtime.kuuos_repository_git_revision_types_v0_83 import (
    git_revision_observation_digest,
)
from runtime.kuuos_repository_application_authorization_types_v0_91 import (
    AUTHORIZATION_GRANTED,
    AUTHORIZATION_REJECTED,
    RepositoryApplicationAuthorizationCertificate,
    RepositoryApplicationAuthorizationPolicy,
    RepositoryApplicationScope,
    RepositoryApplicationSourceStateReceipt,
    RepositoryAuthorizationNonceStatusReceipt,
    repository_application_authorization_certificate_digest,
    repository_application_authorization_policy_digest,
    repository_application_scope_digest,
    repository_application_source_state_receipt_digest,
    repository_authorization_nonce_status_receipt_digest,
)


def _path_valid(path: str) -> bool:
    if not path or path.startswith("/") or "\\" in path:
        return False
    parts = PurePosixPath(path).parts
    return bool(parts) and all(part not in ("", ".", "..") for part in parts)


def _canonical_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(paths)))


def _path_within(path: str, scope_path: str) -> bool:
    normalized = scope_path.rstrip("/")
    return path == normalized or path.startswith(normalized + "/")


def repository_application_authorization_policy_issues(
    policy: RepositoryApplicationAuthorizationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("authorization_policy_id_missing")
    for values, name in (
        (policy.authorized_nonce_authority_ids, "authorized_nonce_authority_ids"),
        (policy.protected_paths, "protected_paths"),
    ):
        if values != _canonical_paths(values):
            issues.append(f"{name}_not_canonical")
        if any(not value for value in values):
            issues.append(f"{name}_contains_empty")
    if not policy.authorized_nonce_authority_ids:
        issues.append("authorized_nonce_authority_ids_empty")
    if any(not _path_valid(path) for path in policy.protected_paths):
        issues.append("protected_path_invalid")
    if any(value <= 0 for value in (
        policy.max_authorization_lifetime_seconds,
        policy.max_source_observation_age_seconds,
        policy.max_nonce_status_age_seconds,
        policy.max_allowed_path_count,
        policy.max_patch_count,
    )):
        issues.append("authorization_policy_bound_invalid")
    if policy.policy_digest != repository_application_authorization_policy_digest(policy):
        issues.append("authorization_policy_digest_mismatch")
    return tuple(issues)


def build_repository_application_authorization_policy(
    policy_id: str,
    *,
    authorized_nonce_authority_ids: tuple[str, ...],
    protected_paths: tuple[str, ...],
    max_authorization_lifetime_seconds: int,
    max_source_observation_age_seconds: int,
    max_nonce_status_age_seconds: int,
    max_allowed_path_count: int,
    max_patch_count: int,
) -> RepositoryApplicationAuthorizationPolicy:
    policy = RepositoryApplicationAuthorizationPolicy(
        policy_id=policy_id,
        authorized_nonce_authority_ids=_canonical_paths(
            authorized_nonce_authority_ids
        ),
        protected_paths=_canonical_paths(protected_paths),
        max_authorization_lifetime_seconds=max_authorization_lifetime_seconds,
        max_source_observation_age_seconds=max_source_observation_age_seconds,
        max_nonce_status_age_seconds=max_nonce_status_age_seconds,
        max_allowed_path_count=max_allowed_path_count,
        max_patch_count=max_patch_count,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_application_authorization_policy_digest(policy),
    )
    issues = repository_application_authorization_policy_issues(policy)
    if issues:
        raise ValueError(f"application_authorization_policy_invalid:{issues[0]}")
    return policy


def repository_application_scope_issues(
    scope: RepositoryApplicationScope,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        scope.scope_id,
        scope.external_approval_certificate_digest,
        scope.admission_certificate_digest,
        scope.authorization_policy_digest,
        scope.patch_bundle_digest,
        scope.source_commit_sha,
        scope.source_snapshot_digest,
        scope.authorization_nonce,
    )
    if any(not value for value in required):
        issues.append("application_scope_required_field_missing")
    if scope.patch_count <= 0:
        issues.append("application_scope_patch_count_invalid")
    if scope.allowed_paths != _canonical_paths(scope.allowed_paths):
        issues.append("application_scope_allowed_paths_not_canonical")
    if scope.expected_changed_paths != _canonical_paths(scope.expected_changed_paths):
        issues.append("application_scope_expected_paths_not_canonical")
    if not scope.allowed_paths:
        issues.append("application_scope_allowed_paths_empty")
    if not scope.expected_changed_paths:
        issues.append("application_scope_expected_paths_empty")
    if any(not _path_valid(path) for path in scope.allowed_paths):
        issues.append("application_scope_allowed_path_invalid")
    if any(not _path_valid(path) for path in scope.expected_changed_paths):
        issues.append("application_scope_expected_path_invalid")
    if scope.issued_at_epoch_seconds < 0:
        issues.append("application_scope_issued_at_negative")
    if scope.expires_at_epoch_seconds <= scope.issued_at_epoch_seconds:
        issues.append("application_scope_expiry_invalid")
    if scope.scope_digest != repository_application_scope_digest(scope):
        issues.append("application_scope_digest_mismatch")
    return tuple(issues)


def build_repository_application_scope(
    scope_id: str,
    external_approval: RepositoryEvolutionExternalApprovalCertificate,
    policy: RepositoryApplicationAuthorizationPolicy,
    *,
    patch_bundle_digest: str,
    patch_count: int,
    source_commit_sha: str,
    source_snapshot_digest: str,
    allowed_paths: tuple[str, ...],
    expected_changed_paths: tuple[str, ...],
    authorization_nonce: str,
    issued_at_epoch_seconds: int,
    expires_at_epoch_seconds: int,
) -> RepositoryApplicationScope:
    scope = RepositoryApplicationScope(
        scope_id=scope_id,
        external_approval_certificate_digest=external_approval.certificate_digest,
        admission_certificate_digest=external_approval.admission_certificate_digest,
        authorization_policy_digest=policy.policy_digest,
        patch_bundle_digest=patch_bundle_digest,
        patch_count=patch_count,
        source_commit_sha=source_commit_sha,
        source_snapshot_digest=source_snapshot_digest,
        allowed_paths=_canonical_paths(allowed_paths),
        expected_changed_paths=_canonical_paths(expected_changed_paths),
        authorization_nonce=authorization_nonce,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        expires_at_epoch_seconds=expires_at_epoch_seconds,
        scope_digest="",
    )
    scope = replace(scope, scope_digest=repository_application_scope_digest(scope))
    issues = repository_application_scope_issues(scope)
    if issues:
        raise ValueError(f"application_scope_invalid:{issues[0]}")
    return scope


def repository_application_source_state_receipt_issues(
    receipt: RepositoryApplicationSourceStateReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not receipt.source_state_id:
        issues.append("source_state_id_missing")
    if receipt.observed_at_epoch_seconds < 0:
        issues.append("source_state_observed_at_negative")
    observation = receipt.revision_observation
    if observation.observation_digest != git_revision_observation_digest(observation):
        issues.append("source_revision_observation_digest_mismatch")
    if receipt.receipt_digest != repository_application_source_state_receipt_digest(
        receipt
    ):
        issues.append("source_state_receipt_digest_mismatch")
    return tuple(issues)


def build_repository_application_source_state_receipt(
    source_state_id: str,
    revision_observation,
    *,
    observed_at_epoch_seconds: int,
) -> RepositoryApplicationSourceStateReceipt:
    receipt = RepositoryApplicationSourceStateReceipt(
        source_state_id=source_state_id,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        revision_observation=revision_observation,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=repository_application_source_state_receipt_digest(receipt),
    )
    issues = repository_application_source_state_receipt_issues(receipt)
    if issues:
        raise ValueError(f"application_source_state_receipt_invalid:{issues[0]}")
    return receipt


def repository_authorization_nonce_status_receipt_issues(
    receipt: RepositoryAuthorizationNonceStatusReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    if any(not value for value in (
        receipt.status_id,
        receipt.authorization_nonce,
        receipt.authorization_scope_digest,
        receipt.authority_id,
        receipt.registry_snapshot_digest,
    )):
        issues.append("nonce_status_required_field_missing")
    if receipt.checked_at_epoch_seconds < 0:
        issues.append("nonce_status_checked_at_negative")
    if receipt.receipt_digest != repository_authorization_nonce_status_receipt_digest(
        receipt
    ):
        issues.append("nonce_status_receipt_digest_mismatch")
    return tuple(issues)


def build_repository_authorization_nonce_status_receipt(
    status_id: str,
    scope: RepositoryApplicationScope,
    *,
    authority_id: str,
    checked_at_epoch_seconds: int,
    registry_snapshot_digest: str,
    consumed: bool,
    revoked: bool,
) -> RepositoryAuthorizationNonceStatusReceipt:
    receipt = RepositoryAuthorizationNonceStatusReceipt(
        status_id=status_id,
        authorization_nonce=scope.authorization_nonce,
        authorization_scope_digest=scope.scope_digest,
        authority_id=authority_id,
        checked_at_epoch_seconds=checked_at_epoch_seconds,
        registry_snapshot_digest=registry_snapshot_digest,
        consumed=consumed,
        revoked=revoked,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=repository_authorization_nonce_status_receipt_digest(receipt),
    )
    issues = repository_authorization_nonce_status_receipt_issues(receipt)
    if issues:
        raise ValueError(f"authorization_nonce_status_receipt_invalid:{issues[0]}")
    return receipt


def repository_application_authorization_certificate_issues(
    certificate: RepositoryApplicationAuthorizationCertificate,
) -> tuple[str, ...]:
    issues: list[str] = []
    if certificate.status not in (AUTHORIZATION_GRANTED, AUTHORIZATION_REJECTED):
        issues.append("application_authorization_status_invalid")
    expected_granted = all((
        certificate.external_approval_bound,
        certificate.admission_binding_exact,
        certificate.policy_binding_exact,
        certificate.scope_binding_exact,
        certificate.patch_bundle_bound,
        certificate.paths_canonical,
        certificate.expected_paths_nonempty,
        certificate.expected_paths_within_allowed_scope,
        certificate.protected_paths_excluded,
        certificate.path_count_within_policy,
        certificate.patch_count_within_policy,
        certificate.source_commit_unchanged,
        certificate.source_snapshot_unchanged,
        certificate.source_observation_fresh,
        certificate.object_database_source,
        certificate.working_tree_ignored,
        certificate.nonce_authority_authorized,
        certificate.nonce_status_fresh,
        certificate.nonce_unused,
        certificate.nonce_not_revoked,
        certificate.authorization_lifetime_within_policy,
        certificate.authorization_not_expired,
        certificate.no_future_evidence,
    ))
    if certificate.application_authorization_granted != expected_granted:
        issues.append("application_authorization_grant_mismatch")
    if certificate.single_use_application_eligible != expected_granted:
        issues.append("single_use_application_eligibility_mismatch")
    if certificate.status == AUTHORIZATION_GRANTED and not expected_granted:
        issues.append("granted_status_without_valid_authorization")
    if certificate.status == AUTHORIZATION_REJECTED and expected_granted:
        issues.append("rejected_status_with_valid_authorization")
    if certificate.patch_application_executed:
        issues.append("unexpected_patch_application_execution")
    if certificate.commit_authority_granted:
        issues.append("unexpected_commit_authority")
    if certificate.reference_mutation_authority_granted:
        issues.append("unexpected_reference_mutation_authority")
    if certificate.certificate_digest != (
        repository_application_authorization_certificate_digest(certificate)
    ):
        issues.append("application_authorization_certificate_digest_mismatch")
    return tuple(issues)


def certify_repository_application_authorization(
    authorization_id: str,
    external_approval: RepositoryEvolutionExternalApprovalCertificate,
    policy: RepositoryApplicationAuthorizationPolicy,
    scope: RepositoryApplicationScope,
    source_state: RepositoryApplicationSourceStateReceipt,
    nonce_status: RepositoryAuthorizationNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryApplicationAuthorizationCertificate:
    if not authorization_id:
        raise ValueError("application_authorization_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("application_authorization_evaluated_at_negative")

    approval_issues = repository_evolution_external_approval_certificate_issues(
        external_approval
    )
    if approval_issues:
        raise ValueError(f"external_approval_certificate_invalid:{approval_issues[0]}")
    if external_approval.status != APPROVAL_ACCEPTED:
        raise ValueError("external_approval_not_accepted")
    if not external_approval.external_approval_granted:
        raise ValueError("external_approval_not_granted")
    if not external_approval.application_authorization_eligible:
        raise ValueError("external_approval_not_authorization_eligible")

    policy_issues = repository_application_authorization_policy_issues(policy)
    if policy_issues:
        raise ValueError(f"application_authorization_policy_invalid:{policy_issues[0]}")
    scope_issues = repository_application_scope_issues(scope)
    if scope_issues:
        raise ValueError(f"application_scope_invalid:{scope_issues[0]}")
    source_issues = repository_application_source_state_receipt_issues(source_state)
    if source_issues:
        raise ValueError(f"application_source_state_receipt_invalid:{source_issues[0]}")
    nonce_issues = repository_authorization_nonce_status_receipt_issues(nonce_status)
    if nonce_issues:
        raise ValueError(f"authorization_nonce_status_receipt_invalid:{nonce_issues[0]}")

    if scope.external_approval_certificate_digest != external_approval.certificate_digest:
        raise ValueError("application_scope_external_approval_binding_mismatch")
    if scope.admission_certificate_digest != external_approval.admission_certificate_digest:
        raise ValueError("application_scope_admission_binding_mismatch")
    if scope.authorization_policy_digest != policy.policy_digest:
        raise ValueError("application_scope_policy_binding_mismatch")
    if nonce_status.authorization_scope_digest != scope.scope_digest:
        raise ValueError("nonce_status_scope_binding_mismatch")
    if nonce_status.authorization_nonce != scope.authorization_nonce:
        raise ValueError("nonce_status_nonce_binding_mismatch")

    observation = source_state.revision_observation
    paths_canonical = (
        scope.allowed_paths == _canonical_paths(scope.allowed_paths)
        and scope.expected_changed_paths == _canonical_paths(
            scope.expected_changed_paths
        )
        and all(_path_valid(path) for path in scope.allowed_paths)
        and all(_path_valid(path) for path in scope.expected_changed_paths)
    )
    expected_paths_within_scope = all(
        any(_path_within(path, allowed) for allowed in scope.allowed_paths)
        for path in scope.expected_changed_paths
    )
    protected_paths_excluded = all(
        not any(_path_within(path, protected) for protected in policy.protected_paths)
        for path in scope.expected_changed_paths
    )
    source_commit_unchanged = observation.current_commit_sha == scope.source_commit_sha
    source_snapshot_unchanged = (
        observation.current_snapshot_digest == scope.source_snapshot_digest
    )
    source_observation_fresh = (
        source_state.observed_at_epoch_seconds <= evaluated_at_epoch_seconds
        and evaluated_at_epoch_seconds - source_state.observed_at_epoch_seconds
        <= policy.max_source_observation_age_seconds
    )
    nonce_status_fresh = (
        nonce_status.checked_at_epoch_seconds <= evaluated_at_epoch_seconds
        and evaluated_at_epoch_seconds - nonce_status.checked_at_epoch_seconds
        <= policy.max_nonce_status_age_seconds
    )
    authorization_lifetime = (
        scope.expires_at_epoch_seconds - scope.issued_at_epoch_seconds
    )
    authorization_lifetime_within_policy = (
        0 < authorization_lifetime
        <= policy.max_authorization_lifetime_seconds
    )
    no_future_evidence = (
        external_approval.evaluated_at_epoch_seconds
        <= scope.issued_at_epoch_seconds
        <= source_state.observed_at_epoch_seconds
        <= nonce_status.checked_at_epoch_seconds
        <= evaluated_at_epoch_seconds
    )
    approval_reuse_within_bound = (
        scope.issued_at_epoch_seconds - external_approval.evaluated_at_epoch_seconds
        <= policy.max_authorization_lifetime_seconds
        if external_approval.evaluated_at_epoch_seconds <= scope.issued_at_epoch_seconds
        else False
    )
    no_future_evidence = no_future_evidence and approval_reuse_within_bound

    values = dict(
        external_approval_bound=True,
        admission_binding_exact=True,
        policy_binding_exact=True,
        scope_binding_exact=True,
        patch_bundle_bound=bool(scope.patch_bundle_digest),
        paths_canonical=paths_canonical,
        expected_paths_nonempty=bool(scope.expected_changed_paths),
        expected_paths_within_allowed_scope=expected_paths_within_scope,
        protected_paths_excluded=protected_paths_excluded,
        path_count_within_policy=len(scope.allowed_paths)
        <= policy.max_allowed_path_count,
        patch_count_within_policy=scope.patch_count <= policy.max_patch_count,
        source_commit_unchanged=source_commit_unchanged,
        source_snapshot_unchanged=source_snapshot_unchanged,
        source_observation_fresh=source_observation_fresh,
        object_database_source=observation.object_database_read,
        working_tree_ignored=not observation.working_tree_read,
        nonce_authority_authorized=(
            nonce_status.authority_id in policy.authorized_nonce_authority_ids
        ),
        nonce_status_fresh=nonce_status_fresh,
        nonce_unused=not nonce_status.consumed,
        nonce_not_revoked=not nonce_status.revoked,
        authorization_lifetime_within_policy=(
            authorization_lifetime_within_policy
        ),
        authorization_not_expired=(
            evaluated_at_epoch_seconds < scope.expires_at_epoch_seconds
        ),
        no_future_evidence=no_future_evidence,
    )
    granted = all(values.values())
    certificate = RepositoryApplicationAuthorizationCertificate(
        authorization_id=authorization_id,
        status=AUTHORIZATION_GRANTED if granted else AUTHORIZATION_REJECTED,
        external_approval_certificate_digest=external_approval.certificate_digest,
        admission_certificate_digest=external_approval.admission_certificate_digest,
        authorization_policy_digest=policy.policy_digest,
        application_scope_digest=scope.scope_digest,
        patch_bundle_digest=scope.patch_bundle_digest,
        source_state_receipt_digest=source_state.receipt_digest,
        nonce_status_receipt_digest=nonce_status.receipt_digest,
        source_commit_sha=scope.source_commit_sha,
        source_snapshot_digest=scope.source_snapshot_digest,
        allowed_paths=scope.allowed_paths,
        expected_changed_paths=scope.expected_changed_paths,
        authorization_nonce=scope.authorization_nonce,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        application_authorization_granted=granted,
        single_use_application_eligible=granted,
        patch_application_executed=False,
        commit_authority_granted=False,
        reference_mutation_authority_granted=False,
        certificate_digest="",
        **values,
    )
    certificate = replace(
        certificate,
        certificate_digest=(
            repository_application_authorization_certificate_digest(certificate)
        ),
    )
    issues = repository_application_authorization_certificate_issues(certificate)
    if issues:
        raise ValueError(f"application_authorization_certificate_invalid:{issues[0]}")
    return certificate
