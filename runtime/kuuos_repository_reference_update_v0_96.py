#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re
import unicodedata

from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    RepositoryAtomicApplicationReceipt,
)
from runtime.kuuos_repository_commit_candidate_types_v0_93 import (
    RepositoryCommitCandidateCertificate,
    RepositoryCommitCandidatePolicy,
    RepositoryParentTreeInventory,
)
from runtime.kuuos_repository_object_materialization_authorization_types_v0_94 import (
    RepositoryObjectDatabaseObservation,
    RepositoryObjectMaterializationAuthorizationCertificate,
    RepositoryObjectMaterializationAuthorizationPolicy,
    RepositoryObjectMaterializationNonceStatusReceipt,
    RepositoryObjectMaterializationScope,
)
from runtime.kuuos_repository_object_materialization_receipt_types_v0_95 import (
    MATERIALIZATION_COMMITTED,
    RepositoryObjectMaterializationExecutionReport,
    RepositoryObjectMaterializationNonceConsumptionReceipt,
    RepositoryObjectMaterializationPolicy,
    RepositoryObjectMaterializationReceipt,
)
from runtime.kuuos_repository_object_materialization_receipt_v0_95 import (
    repository_object_materialization_receipt_issues,
)
from runtime.kuuos_repository_reference_update_authorization_types_v0_96 import (
    AUTHORIZATION_GRANTED,
    AUTHORIZATION_REJECTED,
    ZERO_OID,
    RepositoryReferenceAncestryCertificate,
    RepositoryReferenceObservation,
    RepositoryReferenceUpdateAuthorizationCertificate,
    RepositoryReferenceUpdateNonceStatusReceipt,
    RepositoryReferenceUpdatePolicy,
    RepositoryReferenceUpdateScope,
    repository_reference_ancestry_certificate_digest,
    repository_reference_observation_digest,
    repository_reference_update_authorization_certificate_digest,
    repository_reference_update_nonce_status_receipt_digest,
    repository_reference_update_policy_digest,
    repository_reference_update_scope_digest,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_SAFE_REF = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")


def _canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def normalize_repository_reference_name(reference: str) -> str | None:
    if not reference or reference != reference.strip():
        return None
    if unicodedata.normalize("NFC", reference) != reference:
        return None
    try:
        reference.encode("ascii")
    except UnicodeEncodeError:
        return None
    if not _SAFE_REF.fullmatch(reference):
        return None
    if not reference.startswith("refs/heads/"):
        return None
    branch = reference.removeprefix("refs/heads/")
    if not branch or branch.endswith(("/", ".")):
        return None
    if any(token in reference for token in ("..", "@{", "//", "\\")):
        return None
    components = branch.split("/")
    if any(
        not component
        or component in (".", "..")
        or component.startswith(".")
        or component.endswith(".lock")
        for component in components
    ):
        return None
    return reference


def build_repository_reference_update_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    allowed_references: tuple[str, ...],
    authorized_nonce_authority_ids: tuple[str, ...],
    max_authorization_lifetime_seconds: int,
    max_reference_observation_age_seconds: int,
    max_ancestry_certificate_age_seconds: int,
    max_nonce_status_age_seconds: int,
    max_ancestry_depth: int,
) -> RepositoryReferenceUpdatePolicy:
    policy = RepositoryReferenceUpdatePolicy(
        policy_id=policy_id,
        allowed_repository_ids=_canonical_strings(allowed_repository_ids),
        allowed_references=_canonical_strings(allowed_references),
        authorized_nonce_authority_ids=_canonical_strings(
            authorized_nonce_authority_ids
        ),
        max_authorization_lifetime_seconds=max_authorization_lifetime_seconds,
        max_reference_observation_age_seconds=max_reference_observation_age_seconds,
        max_ancestry_certificate_age_seconds=max_ancestry_certificate_age_seconds,
        max_nonce_status_age_seconds=max_nonce_status_age_seconds,
        max_ancestry_depth=max_ancestry_depth,
        require_compare_and_swap=True,
        require_fast_forward=True,
        require_direct_local_branch=True,
        require_reference_store_source=True,
        require_object_database_ancestry=True,
        require_working_tree_ignored=True,
        allow_force_update=False,
        allow_reference_delete=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_reference_update_policy_digest(policy),
    )
    issues = repository_reference_update_policy_issues(policy)
    if issues:
        raise ValueError(f"reference_update_policy_invalid:{issues[0]}")
    return policy


def repository_reference_update_policy_issues(
    policy: RepositoryReferenceUpdatePolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("reference_update_policy_id_missing")
    for values, name in (
        (policy.allowed_repository_ids, "allowed_repository_ids"),
        (policy.allowed_references, "allowed_references"),
        (policy.authorized_nonce_authority_ids, "authorized_nonce_authority_ids"),
    ):
        if values != _canonical_strings(values):
            issues.append(f"reference_update_{name}_not_canonical")
        if not values or any(not value for value in values):
            issues.append(f"reference_update_{name}_invalid")
    if any(
        normalize_repository_reference_name(reference) != reference
        for reference in policy.allowed_references
    ):
        issues.append("reference_update_allowed_reference_invalid")
    bounds = (
        policy.max_authorization_lifetime_seconds,
        policy.max_reference_observation_age_seconds,
        policy.max_ancestry_certificate_age_seconds,
        policy.max_nonce_status_age_seconds,
        policy.max_ancestry_depth,
    )
    if any(value <= 0 for value in bounds):
        issues.append("reference_update_policy_bound_invalid")
    required = (
        policy.require_compare_and_swap,
        policy.require_fast_forward,
        policy.require_direct_local_branch,
        policy.require_reference_store_source,
        policy.require_object_database_ancestry,
        policy.require_working_tree_ignored,
    )
    if not all(required):
        issues.append("reference_update_required_safeguard_disabled")
    if policy.allow_force_update:
        issues.append("reference_update_force_policy_forbidden")
    if policy.allow_reference_delete:
        issues.append("reference_update_delete_policy_forbidden")
    if policy.policy_digest != repository_reference_update_policy_digest(policy):
        issues.append("reference_update_policy_digest_mismatch")
    return tuple(issues)


def build_repository_reference_observation(
    observation_id: str,
    *,
    repository_id: str,
    git_dir_fingerprint: str,
    target_reference: str,
    observed_oid: str,
    rechecked_oid: str,
    direct: bool,
    symbolic: bool,
    reference_store_read: bool,
    working_tree_read: bool,
    observed_at_epoch_seconds: int,
    rechecked_at_epoch_seconds: int,
) -> RepositoryReferenceObservation:
    observation = RepositoryReferenceObservation(
        observation_id=observation_id,
        repository_id=repository_id,
        git_dir_fingerprint=git_dir_fingerprint,
        target_reference=target_reference,
        observed_oid=observed_oid,
        rechecked_oid=rechecked_oid,
        direct=direct,
        symbolic=symbolic,
        reference_store_read=reference_store_read,
        working_tree_read=working_tree_read,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        rechecked_at_epoch_seconds=rechecked_at_epoch_seconds,
        receipt_digest="",
    )
    observation = replace(
        observation,
        receipt_digest=repository_reference_observation_digest(observation),
    )
    issues = repository_reference_observation_issues(observation)
    if issues:
        raise ValueError(f"reference_observation_invalid:{issues[0]}")
    return observation


def repository_reference_observation_issues(
    observation: RepositoryReferenceObservation,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        observation.observation_id,
        observation.repository_id,
        observation.git_dir_fingerprint,
        observation.target_reference,
    )
    if any(not value for value in required):
        issues.append("reference_observation_required_field_missing")
    if not _HEX64.fullmatch(observation.git_dir_fingerprint):
        issues.append("reference_observation_git_dir_fingerprint_invalid")
    if not _HEX40.fullmatch(observation.observed_oid):
        issues.append("reference_observation_oid_invalid")
    if not _HEX40.fullmatch(observation.rechecked_oid):
        issues.append("reference_observation_rechecked_oid_invalid")
    if observation.observed_at_epoch_seconds < 0:
        issues.append("reference_observation_time_negative")
    if observation.rechecked_at_epoch_seconds < observation.observed_at_epoch_seconds:
        issues.append("reference_observation_recheck_order_invalid")
    if observation.receipt_digest != repository_reference_observation_digest(
        observation
    ):
        issues.append("reference_observation_digest_mismatch")
    return tuple(issues)


def build_repository_reference_ancestry_certificate(
    certificate_id: str,
    materialization_receipt: RepositoryObjectMaterializationReceipt,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    object_database_observation: RepositoryObjectDatabaseObservation,
    *,
    target_reference: str,
    object_database_read: bool,
    working_tree_read: bool,
    observed_at_epoch_seconds: int,
) -> RepositoryReferenceAncestryCertificate:
    certificate = RepositoryReferenceAncestryCertificate(
        certificate_id=certificate_id,
        repository_id=materialization_receipt.repository_id,
        git_dir_fingerprint=materialization_receipt.git_dir_fingerprint,
        target_reference=target_reference,
        old_oid=materialization_receipt.parent_commit_sha,
        new_oid=materialization_receipt.candidate_commit_oid,
        path_oids=(
            materialization_receipt.parent_commit_sha,
            materialization_receipt.candidate_commit_oid,
        ),
        depth=1,
        candidate_certificate_digest=candidate_certificate.certificate_digest,
        object_database_observation_digest=object_database_observation.receipt_digest,
        object_database_read=object_database_read,
        working_tree_read=working_tree_read,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        certificate_digest="",
    )
    certificate = replace(
        certificate,
        certificate_digest=repository_reference_ancestry_certificate_digest(
            certificate
        ),
    )
    issues = repository_reference_ancestry_certificate_issues(certificate)
    if issues:
        raise ValueError(f"reference_ancestry_certificate_invalid:{issues[0]}")
    return certificate


def repository_reference_ancestry_certificate_issues(
    certificate: RepositoryReferenceAncestryCertificate,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        certificate.certificate_id,
        certificate.repository_id,
        certificate.git_dir_fingerprint,
        certificate.target_reference,
        certificate.candidate_certificate_digest,
        certificate.object_database_observation_digest,
    )
    if any(not value for value in required):
        issues.append("reference_ancestry_required_field_missing")
    for digest in (
        certificate.git_dir_fingerprint,
        certificate.candidate_certificate_digest,
        certificate.object_database_observation_digest,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("reference_ancestry_digest_invalid")
            break
    if not _HEX40.fullmatch(certificate.old_oid) or not _HEX40.fullmatch(
        certificate.new_oid
    ):
        issues.append("reference_ancestry_oid_invalid")
    if any(not _HEX40.fullmatch(oid) for oid in certificate.path_oids):
        issues.append("reference_ancestry_path_oid_invalid")
    if certificate.depth < 0 or certificate.depth != len(certificate.path_oids) - 1:
        issues.append("reference_ancestry_depth_invalid")
    if not certificate.path_oids:
        issues.append("reference_ancestry_path_empty")
    elif (
        certificate.path_oids[0] != certificate.old_oid
        or certificate.path_oids[-1] != certificate.new_oid
    ):
        issues.append("reference_ancestry_endpoints_mismatch")
    if len(set(certificate.path_oids)) != len(certificate.path_oids):
        issues.append("reference_ancestry_path_cycle")
    if certificate.observed_at_epoch_seconds < 0:
        issues.append("reference_ancestry_observed_at_negative")
    if certificate.certificate_digest != (
        repository_reference_ancestry_certificate_digest(certificate)
    ):
        issues.append("reference_ancestry_certificate_digest_mismatch")
    return tuple(issues)


def build_repository_reference_update_scope(
    scope_id: str,
    materialization_receipt: RepositoryObjectMaterializationReceipt,
    policy: RepositoryReferenceUpdatePolicy,
    observation: RepositoryReferenceObservation,
    ancestry_certificate: RepositoryReferenceAncestryCertificate,
    *,
    authorization_nonce: str,
    issued_at_epoch_seconds: int,
    expires_at_epoch_seconds: int,
    force_update_requested: bool = False,
    delete_requested: bool = False,
) -> RepositoryReferenceUpdateScope:
    scope = RepositoryReferenceUpdateScope(
        scope_id=scope_id,
        materialization_receipt_digest=materialization_receipt.receipt_digest,
        authorization_policy_digest=policy.policy_digest,
        reference_observation_digest=observation.receipt_digest,
        ancestry_certificate_digest=ancestry_certificate.certificate_digest,
        repository_id=materialization_receipt.repository_id,
        git_dir_fingerprint=materialization_receipt.git_dir_fingerprint,
        target_reference=observation.target_reference,
        expected_old_oid=observation.rechecked_oid,
        proposed_new_oid=materialization_receipt.candidate_commit_oid,
        force_update_requested=force_update_requested,
        delete_requested=delete_requested,
        authorization_nonce=authorization_nonce,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        expires_at_epoch_seconds=expires_at_epoch_seconds,
        scope_digest="",
    )
    scope = replace(
        scope,
        scope_digest=repository_reference_update_scope_digest(scope),
    )
    issues = repository_reference_update_scope_issues(scope)
    if issues:
        raise ValueError(f"reference_update_scope_invalid:{issues[0]}")
    return scope


def repository_reference_update_scope_issues(
    scope: RepositoryReferenceUpdateScope,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        scope.scope_id,
        scope.materialization_receipt_digest,
        scope.authorization_policy_digest,
        scope.reference_observation_digest,
        scope.ancestry_certificate_digest,
        scope.repository_id,
        scope.git_dir_fingerprint,
        scope.target_reference,
        scope.authorization_nonce,
    )
    if any(not value for value in required):
        issues.append("reference_update_scope_required_field_missing")
    for digest in (
        scope.materialization_receipt_digest,
        scope.authorization_policy_digest,
        scope.reference_observation_digest,
        scope.ancestry_certificate_digest,
        scope.git_dir_fingerprint,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("reference_update_scope_digest_invalid")
            break
    if not _HEX40.fullmatch(scope.expected_old_oid):
        issues.append("reference_update_scope_old_oid_invalid")
    if not _HEX40.fullmatch(scope.proposed_new_oid):
        issues.append("reference_update_scope_new_oid_invalid")
    if scope.issued_at_epoch_seconds < 0:
        issues.append("reference_update_scope_issued_at_negative")
    if scope.expires_at_epoch_seconds <= scope.issued_at_epoch_seconds:
        issues.append("reference_update_scope_expiry_invalid")
    if scope.scope_digest != repository_reference_update_scope_digest(scope):
        issues.append("reference_update_scope_digest_mismatch")
    return tuple(issues)


def build_repository_reference_update_nonce_status_receipt(
    status_id: str,
    scope: RepositoryReferenceUpdateScope,
    *,
    authority_id: str,
    checked_at_epoch_seconds: int,
    registry_snapshot_digest: str,
    consumed: bool,
    revoked: bool,
) -> RepositoryReferenceUpdateNonceStatusReceipt:
    receipt = RepositoryReferenceUpdateNonceStatusReceipt(
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
        receipt_digest=repository_reference_update_nonce_status_receipt_digest(
            receipt
        ),
    )
    issues = repository_reference_update_nonce_status_receipt_issues(receipt)
    if issues:
        raise ValueError(f"reference_update_nonce_status_invalid:{issues[0]}")
    return receipt


def repository_reference_update_nonce_status_receipt_issues(
    receipt: RepositoryReferenceUpdateNonceStatusReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        receipt.status_id,
        receipt.authorization_nonce,
        receipt.authorization_scope_digest,
        receipt.authority_id,
        receipt.registry_snapshot_digest,
    )
    if any(not value for value in required):
        issues.append("reference_update_nonce_required_field_missing")
    if not _HEX64.fullmatch(receipt.authorization_scope_digest):
        issues.append("reference_update_nonce_scope_digest_invalid")
    if not _HEX64.fullmatch(receipt.registry_snapshot_digest):
        issues.append("reference_update_nonce_registry_digest_invalid")
    if receipt.checked_at_epoch_seconds < 0:
        issues.append("reference_update_nonce_checked_at_negative")
    if receipt.receipt_digest != (
        repository_reference_update_nonce_status_receipt_digest(receipt)
    ):
        issues.append("reference_update_nonce_receipt_digest_mismatch")
    return tuple(issues)


def _materialization_chain_issues(
    materialization_receipt: RepositoryObjectMaterializationReceipt,
    materialization_authorization: RepositoryObjectMaterializationAuthorizationCertificate,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    candidate_policy: RepositoryCommitCandidatePolicy,
    materialization_authorization_policy: RepositoryObjectMaterializationAuthorizationPolicy,
    materialization_scope: RepositoryObjectMaterializationScope,
    pre_object_database_observation: RepositoryObjectDatabaseObservation,
    pre_materialization_nonce_status: RepositoryObjectMaterializationNonceStatusReceipt,
    materialization_policy: RepositoryObjectMaterializationPolicy,
    execution_report: RepositoryObjectMaterializationExecutionReport,
    post_object_database_observation: RepositoryObjectDatabaseObservation,
    nonce_consumption_receipt: RepositoryObjectMaterializationNonceConsumptionReceipt,
) -> tuple[str, ...]:
    return repository_object_materialization_receipt_issues(
        materialization_receipt,
        materialization_authorization,
        candidate_certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
        materialization_authorization_policy,
        materialization_scope,
        pre_object_database_observation,
        pre_materialization_nonce_status,
        materialization_policy,
        execution_report,
        post_object_database_observation,
        nonce_consumption_receipt,
    )


def _candidate_commit_present_exact(
    materialization_receipt: RepositoryObjectMaterializationReceipt,
    materialization_authorization: RepositoryObjectMaterializationAuthorizationCertificate,
    post_observation: RepositoryObjectDatabaseObservation,
) -> bool:
    item = next(
        (
            candidate
            for candidate in materialization_authorization.plan_items
            if candidate.kind == "commit"
            and candidate.oid == materialization_receipt.candidate_commit_oid
        ),
        None,
    )
    entry = next(
        (
            candidate
            for candidate in post_observation.existing_objects
            if candidate.oid == materialization_receipt.candidate_commit_oid
        ),
        None,
    )
    return bool(
        item is not None
        and entry is not None
        and entry.kind == item.kind == "commit"
        and entry.payload_size == item.payload_size
        and entry.payload_digest == item.payload_digest
    )


def _construct_authorization_certificate(
    authorization_id: str,
    materialization_receipt: RepositoryObjectMaterializationReceipt,
    materialization_authorization: RepositoryObjectMaterializationAuthorizationCertificate,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    post_object_database_observation: RepositoryObjectDatabaseObservation,
    policy: RepositoryReferenceUpdatePolicy,
    observation: RepositoryReferenceObservation,
    ancestry_certificate: RepositoryReferenceAncestryCertificate,
    scope: RepositoryReferenceUpdateScope,
    nonce_status: RepositoryReferenceUpdateNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryReferenceUpdateAuthorizationCertificate:
    normalized = normalize_repository_reference_name(scope.target_reference)
    reference_name_valid = normalized is not None
    reference_normalized = normalized == scope.target_reference
    reference_not_head = scope.target_reference != "HEAD"
    reference_not_tag = not scope.target_reference.startswith("refs/tags/")
    reference_not_remote = not scope.target_reference.startswith("refs/remotes/")
    reference_not_notes = not scope.target_reference.startswith("refs/notes/")
    reference_not_replace = not scope.target_reference.startswith("refs/replace/")
    reference_allowed = scope.target_reference in policy.allowed_references
    reference_direct = observation.direct and policy.require_direct_local_branch
    reference_not_symbolic = not observation.symbolic
    reference_not_deleted = bool(
        scope.expected_old_oid != ZERO_OID
        and scope.proposed_new_oid != ZERO_OID
        and not scope.delete_requested
        and not policy.allow_reference_delete
    )

    materialization_receipt_committed = bool(
        materialization_receipt.status == MATERIALIZATION_COMMITTED
        and materialization_receipt.object_database_materialization_committed
        and materialization_receipt.atomic_state_transition
    )
    materialization_receipt_binding_exact = bool(
        scope.materialization_receipt_digest == materialization_receipt.receipt_digest
        and scope.proposed_new_oid == materialization_receipt.candidate_commit_oid
        and materialization_receipt.authorization_certificate_digest
        == materialization_authorization.certificate_digest
    )
    repository_allowed = scope.repository_id in policy.allowed_repository_ids
    repository_identity_exact = bool(
        scope.repository_id
        == materialization_receipt.repository_id
        == observation.repository_id
        == ancestry_certificate.repository_id
        == post_object_database_observation.repository_id
        and scope.git_dir_fingerprint
        == materialization_receipt.git_dir_fingerprint
        == observation.git_dir_fingerprint
        == ancestry_certificate.git_dir_fingerprint
        == post_object_database_observation.git_dir_fingerprint
    )
    reference_observation_bound = bool(
        scope.reference_observation_digest == observation.receipt_digest
        and scope.target_reference == observation.target_reference
        and scope.expected_old_oid == observation.rechecked_oid
    )
    observation_age = evaluated_at_epoch_seconds - observation.rechecked_at_epoch_seconds
    reference_observation_fresh = bool(
        0 <= observation_age <= policy.max_reference_observation_age_seconds
    )
    reference_store_source = bool(
        observation.reference_store_read and policy.require_reference_store_source
    )
    reference_working_tree_ignored = bool(
        not observation.working_tree_read and policy.require_working_tree_ignored
    )
    reference_unchanged_since_observation = bool(
        observation.observed_oid == observation.rechecked_oid == scope.expected_old_oid
    )
    old_oid_exact = bool(
        scope.expected_old_oid
        == materialization_receipt.parent_commit_sha
        == candidate_certificate.parent_commit_sha
        == ancestry_certificate.old_oid
        and post_object_database_observation.source_commit_sha
        == materialization_receipt.parent_commit_sha
    )
    new_oid_exact = bool(
        scope.proposed_new_oid
        == materialization_receipt.candidate_commit_oid
        == candidate_certificate.candidate_commit_oid
        == ancestry_certificate.new_oid
    )
    candidate_commit_bound = bool(
        materialization_receipt.candidate_commit_oid
        == materialization_authorization.candidate_commit_oid
        == candidate_certificate.candidate_commit_oid
    )
    candidate_commit_present = bool(
        materialization_receipt.candidate_commit_present
        and _candidate_commit_present_exact(
            materialization_receipt,
            materialization_authorization,
            post_object_database_observation,
        )
    )
    source_parent_unchanged = bool(
        materialization_receipt.parent_commit_preserved
        and materialization_receipt.parent_commit_sha
        == materialization_authorization.parent_commit_sha
        == candidate_certificate.parent_commit_sha
    )
    ancestry_certificate_bound = bool(
        scope.ancestry_certificate_digest == ancestry_certificate.certificate_digest
        and ancestry_certificate.candidate_certificate_digest
        == candidate_certificate.certificate_digest
        and ancestry_certificate.object_database_observation_digest
        == post_object_database_observation.receipt_digest
        and ancestry_certificate.target_reference == scope.target_reference
    )
    fast_forward_verified = bool(
        policy.require_fast_forward
        and ancestry_certificate.path_oids
        == (scope.expected_old_oid, scope.proposed_new_oid)
        and ancestry_certificate.depth == 1
        and old_oid_exact
        and new_oid_exact
    )
    ancestry_depth_within_policy = bool(
        0 < ancestry_certificate.depth <= policy.max_ancestry_depth
    )
    ancestry_age = evaluated_at_epoch_seconds - ancestry_certificate.observed_at_epoch_seconds
    ancestry_fresh = bool(
        0 <= ancestry_age <= policy.max_ancestry_certificate_age_seconds
    )
    ancestry_object_database_source = bool(
        ancestry_certificate.object_database_read
        and policy.require_object_database_ancestry
        and ancestry_fresh
    )
    ancestry_working_tree_ignored = bool(
        not ancestry_certificate.working_tree_read
        and policy.require_working_tree_ignored
    )
    nonce_authority_authorized = (
        nonce_status.authority_id in policy.authorized_nonce_authority_ids
    )
    nonce_scope_bound = bool(
        nonce_status.authorization_nonce == scope.authorization_nonce
        and nonce_status.authorization_scope_digest == scope.scope_digest
    )
    nonce_age = evaluated_at_epoch_seconds - nonce_status.checked_at_epoch_seconds
    nonce_status_fresh = bool(0 <= nonce_age <= policy.max_nonce_status_age_seconds)
    authorization_lifetime_within_policy = bool(
        scope.expires_at_epoch_seconds - scope.issued_at_epoch_seconds
        <= policy.max_authorization_lifetime_seconds
    )
    authorization_not_expired = bool(
        scope.issued_at_epoch_seconds
        <= evaluated_at_epoch_seconds
        <= scope.expires_at_epoch_seconds
    )
    no_future_evidence = all(
        value <= evaluated_at_epoch_seconds
        for value in (
            scope.issued_at_epoch_seconds,
            observation.observed_at_epoch_seconds,
            observation.rechecked_at_epoch_seconds,
            ancestry_certificate.observed_at_epoch_seconds,
            nonce_status.checked_at_epoch_seconds,
        )
    )
    compare_and_swap_required = bool(
        policy.require_compare_and_swap
        and reference_unchanged_since_observation
        and scope.expected_old_oid == observation.rechecked_oid
    )

    grant_inputs = (
        materialization_receipt_committed,
        materialization_receipt_binding_exact,
        repository_allowed,
        repository_identity_exact,
        reference_name_valid,
        reference_normalized,
        reference_allowed,
        reference_direct,
        reference_not_symbolic,
        reference_not_head,
        reference_not_tag,
        reference_not_remote,
        reference_not_notes,
        reference_not_replace,
        reference_not_deleted,
        reference_observation_bound,
        reference_observation_fresh,
        reference_store_source,
        reference_working_tree_ignored,
        reference_unchanged_since_observation,
        old_oid_exact,
        new_oid_exact,
        candidate_commit_bound,
        candidate_commit_present,
        source_parent_unchanged,
        ancestry_certificate_bound,
        fast_forward_verified,
        ancestry_depth_within_policy,
        ancestry_object_database_source,
        ancestry_working_tree_ignored,
        nonce_authority_authorized,
        nonce_scope_bound,
        nonce_status_fresh,
        not nonce_status.consumed,
        not nonce_status.revoked,
        authorization_lifetime_within_policy,
        authorization_not_expired,
        no_future_evidence,
        compare_and_swap_required,
        not scope.force_update_requested,
        not scope.delete_requested,
        not policy.allow_force_update,
        not policy.allow_reference_delete,
    )
    granted = all(grant_inputs)
    certificate = RepositoryReferenceUpdateAuthorizationCertificate(
        authorization_id=authorization_id,
        status=AUTHORIZATION_GRANTED if granted else AUTHORIZATION_REJECTED,
        materialization_receipt_digest=materialization_receipt.receipt_digest,
        authorization_policy_digest=policy.policy_digest,
        reference_update_scope_digest=scope.scope_digest,
        reference_observation_digest=observation.receipt_digest,
        ancestry_certificate_digest=ancestry_certificate.certificate_digest,
        nonce_status_receipt_digest=nonce_status.receipt_digest,
        repository_id=scope.repository_id,
        git_dir_fingerprint=scope.git_dir_fingerprint,
        target_reference=scope.target_reference,
        expected_old_oid=scope.expected_old_oid,
        proposed_new_oid=scope.proposed_new_oid,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        materialization_receipt_valid=True,
        materialization_receipt_committed=materialization_receipt_committed,
        materialization_receipt_binding_exact=materialization_receipt_binding_exact,
        repository_allowed=repository_allowed,
        repository_identity_exact=repository_identity_exact,
        reference_name_valid=reference_name_valid,
        reference_normalized=reference_normalized,
        reference_allowed=reference_allowed,
        reference_direct=reference_direct,
        reference_not_symbolic=reference_not_symbolic,
        reference_not_head=reference_not_head,
        reference_not_tag=reference_not_tag,
        reference_not_remote=reference_not_remote,
        reference_not_notes=reference_not_notes,
        reference_not_replace=reference_not_replace,
        reference_not_deleted=reference_not_deleted,
        reference_observation_bound=reference_observation_bound,
        reference_observation_fresh=reference_observation_fresh,
        reference_store_source=reference_store_source,
        reference_working_tree_ignored=reference_working_tree_ignored,
        reference_unchanged_since_observation=reference_unchanged_since_observation,
        old_oid_exact=old_oid_exact,
        new_oid_exact=new_oid_exact,
        candidate_commit_bound=candidate_commit_bound,
        candidate_commit_present=candidate_commit_present,
        source_parent_unchanged=source_parent_unchanged,
        ancestry_certificate_bound=ancestry_certificate_bound,
        fast_forward_verified=fast_forward_verified,
        ancestry_depth_within_policy=ancestry_depth_within_policy,
        ancestry_object_database_source=ancestry_object_database_source,
        ancestry_working_tree_ignored=ancestry_working_tree_ignored,
        nonce_authority_authorized=nonce_authority_authorized,
        nonce_scope_bound=nonce_scope_bound,
        nonce_status_fresh=nonce_status_fresh,
        nonce_unused=not nonce_status.consumed,
        nonce_not_revoked=not nonce_status.revoked,
        authorization_lifetime_within_policy=authorization_lifetime_within_policy,
        authorization_not_expired=authorization_not_expired,
        no_future_evidence=no_future_evidence,
        compare_and_swap_required=compare_and_swap_required,
        single_use_reference_update_eligible=granted,
        reference_update_authority_granted=granted,
        force_update_authorized=False,
        reference_delete_authorized=False,
        reference_update_performed=False,
        reference_mutated=False,
        branch_updated=False,
        head_updated=False,
        tag_updated=False,
        remote_reference_updated=False,
        push_performed=False,
        index_write_performed=False,
        working_tree_write_performed=False,
        object_database_write_performed=False,
        signing_performed=False,
        certificate_digest="",
    )
    return replace(
        certificate,
        certificate_digest=repository_reference_update_authorization_certificate_digest(
            certificate
        ),
    )


def authorize_repository_reference_update(
    authorization_id: str,
    materialization_receipt: RepositoryObjectMaterializationReceipt,
    materialization_authorization: RepositoryObjectMaterializationAuthorizationCertificate,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    candidate_policy: RepositoryCommitCandidatePolicy,
    materialization_authorization_policy: RepositoryObjectMaterializationAuthorizationPolicy,
    materialization_scope: RepositoryObjectMaterializationScope,
    pre_object_database_observation: RepositoryObjectDatabaseObservation,
    pre_materialization_nonce_status: RepositoryObjectMaterializationNonceStatusReceipt,
    materialization_policy: RepositoryObjectMaterializationPolicy,
    execution_report: RepositoryObjectMaterializationExecutionReport,
    post_object_database_observation: RepositoryObjectDatabaseObservation,
    nonce_consumption_receipt: RepositoryObjectMaterializationNonceConsumptionReceipt,
    policy: RepositoryReferenceUpdatePolicy,
    observation: RepositoryReferenceObservation,
    ancestry_certificate: RepositoryReferenceAncestryCertificate,
    scope: RepositoryReferenceUpdateScope,
    nonce_status: RepositoryReferenceUpdateNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryReferenceUpdateAuthorizationCertificate:
    if not authorization_id:
        raise ValueError("reference_update_authorization_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("reference_update_evaluated_at_negative")
    chain_issues = _materialization_chain_issues(
        materialization_receipt,
        materialization_authorization,
        candidate_certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
        materialization_authorization_policy,
        materialization_scope,
        pre_object_database_observation,
        pre_materialization_nonce_status,
        materialization_policy,
        execution_report,
        post_object_database_observation,
        nonce_consumption_receipt,
    )
    if chain_issues:
        raise ValueError(
            f"object_materialization_receipt_invalid:{chain_issues[0]}"
        )
    for issues, prefix in (
        (repository_reference_update_policy_issues(policy), "reference_update_policy_invalid"),
        (repository_reference_observation_issues(observation), "reference_observation_invalid"),
        (
            repository_reference_ancestry_certificate_issues(ancestry_certificate),
            "reference_ancestry_certificate_invalid",
        ),
        (repository_reference_update_scope_issues(scope), "reference_update_scope_invalid"),
        (
            repository_reference_update_nonce_status_receipt_issues(nonce_status),
            "reference_update_nonce_status_invalid",
        ),
    ):
        if issues:
            raise ValueError(f"{prefix}:{issues[0]}")
    certificate = _construct_authorization_certificate(
        authorization_id,
        materialization_receipt,
        materialization_authorization,
        candidate_certificate,
        post_object_database_observation,
        policy,
        observation,
        ancestry_certificate,
        scope,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_reference_update_authorization_certificate_issues(
        certificate,
        materialization_receipt,
        materialization_authorization,
        candidate_certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
        materialization_authorization_policy,
        materialization_scope,
        pre_object_database_observation,
        pre_materialization_nonce_status,
        materialization_policy,
        execution_report,
        post_object_database_observation,
        nonce_consumption_receipt,
        policy,
        observation,
        ancestry_certificate,
        scope,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"reference_update_certificate_invalid:{issues[0]}")
    return certificate


def repository_reference_update_authorization_certificate_issues(
    certificate: RepositoryReferenceUpdateAuthorizationCertificate,
    materialization_receipt: RepositoryObjectMaterializationReceipt,
    materialization_authorization: RepositoryObjectMaterializationAuthorizationCertificate,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    candidate_policy: RepositoryCommitCandidatePolicy,
    materialization_authorization_policy: RepositoryObjectMaterializationAuthorizationPolicy,
    materialization_scope: RepositoryObjectMaterializationScope,
    pre_object_database_observation: RepositoryObjectDatabaseObservation,
    pre_materialization_nonce_status: RepositoryObjectMaterializationNonceStatusReceipt,
    materialization_policy: RepositoryObjectMaterializationPolicy,
    execution_report: RepositoryObjectMaterializationExecutionReport,
    post_object_database_observation: RepositoryObjectDatabaseObservation,
    nonce_consumption_receipt: RepositoryObjectMaterializationNonceConsumptionReceipt,
    policy: RepositoryReferenceUpdatePolicy,
    observation: RepositoryReferenceObservation,
    ancestry_certificate: RepositoryReferenceAncestryCertificate,
    scope: RepositoryReferenceUpdateScope,
    nonce_status: RepositoryReferenceUpdateNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    chain_issues = _materialization_chain_issues(
        materialization_receipt,
        materialization_authorization,
        candidate_certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
        materialization_authorization_policy,
        materialization_scope,
        pre_object_database_observation,
        pre_materialization_nonce_status,
        materialization_policy,
        execution_report,
        post_object_database_observation,
        nonce_consumption_receipt,
    )
    if chain_issues:
        issues.append("object_materialization_receipt_invalid")
        return tuple(issues)
    for validator, name in (
        (repository_reference_update_policy_issues(policy), "reference_update_policy_invalid"),
        (repository_reference_observation_issues(observation), "reference_observation_invalid"),
        (
            repository_reference_ancestry_certificate_issues(ancestry_certificate),
            "reference_ancestry_certificate_invalid",
        ),
        (repository_reference_update_scope_issues(scope), "reference_update_scope_invalid"),
        (
            repository_reference_update_nonce_status_receipt_issues(nonce_status),
            "reference_update_nonce_status_invalid",
        ),
    ):
        if validator:
            issues.append(name)
            return tuple(issues)
    expected = _construct_authorization_certificate(
        certificate.authorization_id,
        materialization_receipt,
        materialization_authorization,
        candidate_certificate,
        post_object_database_observation,
        policy,
        observation,
        ancestry_certificate,
        scope,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if certificate.to_dict() != expected.to_dict():
        issues.append("reference_update_authorization_recomputation_mismatch")
    if certificate.status not in (AUTHORIZATION_GRANTED, AUTHORIZATION_REJECTED):
        issues.append("reference_update_authorization_status_invalid")
    forbidden_true = (
        certificate.force_update_authorized,
        certificate.reference_delete_authorized,
        certificate.reference_update_performed,
        certificate.reference_mutated,
        certificate.branch_updated,
        certificate.head_updated,
        certificate.tag_updated,
        certificate.remote_reference_updated,
        certificate.push_performed,
        certificate.index_write_performed,
        certificate.working_tree_write_performed,
        certificate.object_database_write_performed,
        certificate.signing_performed,
    )
    if any(forbidden_true):
        issues.append("reference_update_authorization_forbidden_effect")
    if certificate.status == AUTHORIZATION_GRANTED:
        required_true = (
            certificate.materialization_receipt_valid,
            certificate.materialization_receipt_committed,
            certificate.materialization_receipt_binding_exact,
            certificate.repository_allowed,
            certificate.repository_identity_exact,
            certificate.reference_name_valid,
            certificate.reference_normalized,
            certificate.reference_allowed,
            certificate.reference_direct,
            certificate.reference_not_symbolic,
            certificate.reference_not_head,
            certificate.reference_not_tag,
            certificate.reference_not_remote,
            certificate.reference_not_notes,
            certificate.reference_not_replace,
            certificate.reference_not_deleted,
            certificate.reference_observation_bound,
            certificate.reference_observation_fresh,
            certificate.reference_store_source,
            certificate.reference_working_tree_ignored,
            certificate.reference_unchanged_since_observation,
            certificate.old_oid_exact,
            certificate.new_oid_exact,
            certificate.candidate_commit_bound,
            certificate.candidate_commit_present,
            certificate.source_parent_unchanged,
            certificate.ancestry_certificate_bound,
            certificate.fast_forward_verified,
            certificate.ancestry_depth_within_policy,
            certificate.ancestry_object_database_source,
            certificate.ancestry_working_tree_ignored,
            certificate.nonce_authority_authorized,
            certificate.nonce_scope_bound,
            certificate.nonce_status_fresh,
            certificate.nonce_unused,
            certificate.nonce_not_revoked,
            certificate.authorization_lifetime_within_policy,
            certificate.authorization_not_expired,
            certificate.no_future_evidence,
            certificate.compare_and_swap_required,
            certificate.single_use_reference_update_eligible,
            certificate.reference_update_authority_granted,
        )
        if not all(required_true):
            issues.append("reference_update_granted_invariant_false")
    if certificate.certificate_digest != (
        repository_reference_update_authorization_certificate_digest(certificate)
    ):
        issues.append("reference_update_authorization_digest_mismatch")
    return tuple(issues)
