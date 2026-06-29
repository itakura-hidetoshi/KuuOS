#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re
import unicodedata
from typing import Any, Mapping

from runtime.kuuos_repository_local_frontier_checkpoint_authorization_types_v1_01 import (
    AUTHORIZATION_GRANTED,
    AUTHORIZATION_REJECTED,
    CHECKPOINT_NAMESPACE,
    ZERO_OID,
    RepositoryCheckpointReferenceObservation,
    RepositoryLocalFrontierCheckpointAuthorizationCertificate,
    RepositoryLocalFrontierCheckpointNonceStatusReceipt,
    RepositoryLocalFrontierCheckpointPolicy,
    RepositoryLocalFrontierCheckpointScope,
    repository_checkpoint_reference_observation_digest,
    repository_local_frontier_checkpoint_authorization_certificate_digest,
    repository_local_frontier_checkpoint_nonce_status_receipt_digest,
    repository_local_frontier_checkpoint_policy_digest,
    repository_local_frontier_checkpoint_scope_digest,
)
from runtime.kuuos_repository_local_frontier_finality_types_v1_00 import (
    CERTIFICATE_COMMITTED as FINALITY_COMMITTED,
    RepositoryLocalFrontierFinalityCertificate,
)
from runtime.kuuos_repository_local_frontier_finality_v1_00 import (
    repository_local_frontier_finality_certificate_issues,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_SAFE_REF = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")


def _canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def normalize_repository_checkpoint_reference_name(reference: str) -> str | None:
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
    if not reference.startswith(CHECKPOINT_NAMESPACE):
        return None
    suffix = reference.removeprefix(CHECKPOINT_NAMESPACE)
    if not suffix or suffix.endswith(("/", ".")):
        return None
    if any(token in reference for token in ("..", "@{", "//", "\\")):
        return None
    components = suffix.split("/")
    if any(
        not component
        or component in (".", "..")
        or component.startswith(".")
        or component.endswith(".lock")
        for component in components
    ):
        return None
    return reference


def build_repository_local_frontier_checkpoint_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    allowed_checkpoint_references: tuple[str, ...],
    authorized_nonce_authority_ids: tuple[str, ...],
    max_authorization_lifetime_seconds: int,
    max_reference_observation_age_seconds: int,
    max_nonce_status_age_seconds: int,
) -> RepositoryLocalFrontierCheckpointPolicy:
    policy = RepositoryLocalFrontierCheckpointPolicy(
        policy_id=policy_id,
        allowed_repository_ids=_canonical_strings(allowed_repository_ids),
        allowed_checkpoint_references=_canonical_strings(
            allowed_checkpoint_references
        ),
        authorized_nonce_authority_ids=_canonical_strings(
            authorized_nonce_authority_ids
        ),
        max_authorization_lifetime_seconds=max_authorization_lifetime_seconds,
        max_reference_observation_age_seconds=(
            max_reference_observation_age_seconds
        ),
        max_nonce_status_age_seconds=max_nonce_status_age_seconds,
        require_compare_and_swap_nonexistence=True,
        require_exact_final_tip=True,
        require_direct_checkpoint_reference=True,
        require_reference_store_source=True,
        require_working_tree_ignored=True,
        require_reflog_ignored=True,
        require_remote_ignored=True,
        allow_checkpoint_overwrite=False,
        allow_reference_delete=False,
        allow_force_update=False,
        allow_tag_creation=False,
        allow_push=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_local_frontier_checkpoint_policy_digest(policy),
    )
    issues = repository_local_frontier_checkpoint_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_policy_invalid:{issues[0]}")
    return policy


def repository_local_frontier_checkpoint_policy_issues(
    policy: RepositoryLocalFrontierCheckpointPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_policy_id_missing")
    for values, name in (
        (policy.allowed_repository_ids, "allowed_repository_ids"),
        (
            policy.allowed_checkpoint_references,
            "allowed_checkpoint_references",
        ),
        (
            policy.authorized_nonce_authority_ids,
            "authorized_nonce_authority_ids",
        ),
    ):
        if values != _canonical_strings(values):
            issues.append(f"checkpoint_policy_{name}_not_canonical")
        if not values or any(not value for value in values):
            issues.append(f"checkpoint_policy_{name}_invalid")
    if any(
        normalize_repository_checkpoint_reference_name(reference) != reference
        for reference in policy.allowed_checkpoint_references
    ):
        issues.append("checkpoint_policy_allowed_reference_invalid")
    if any(
        value <= 0
        for value in (
            policy.max_authorization_lifetime_seconds,
            policy.max_reference_observation_age_seconds,
            policy.max_nonce_status_age_seconds,
        )
    ):
        issues.append("checkpoint_policy_bound_invalid")
    required = (
        policy.require_compare_and_swap_nonexistence,
        policy.require_exact_final_tip,
        policy.require_direct_checkpoint_reference,
        policy.require_reference_store_source,
        policy.require_working_tree_ignored,
        policy.require_reflog_ignored,
        policy.require_remote_ignored,
    )
    if not all(required):
        issues.append("checkpoint_policy_required_safeguard_disabled")
    forbidden = (
        policy.allow_checkpoint_overwrite,
        policy.allow_reference_delete,
        policy.allow_force_update,
        policy.allow_tag_creation,
        policy.allow_push,
    )
    if any(forbidden):
        issues.append("checkpoint_policy_forbidden_authority_enabled")
    if policy.policy_digest != repository_local_frontier_checkpoint_policy_digest(
        policy
    ):
        issues.append("checkpoint_policy_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_reference_observation(
    observation_id: str,
    *,
    repository_id: str,
    git_dir_fingerprint: str,
    checkpoint_reference: str,
    observed_oid: str,
    rechecked_oid: str,
    direct: bool = True,
    symbolic: bool = False,
    reference_store_read: bool = True,
    working_tree_read: bool = False,
    reflog_read: bool = False,
    remote_read: bool = False,
    observed_at_epoch_seconds: int,
    rechecked_at_epoch_seconds: int,
) -> RepositoryCheckpointReferenceObservation:
    observation = RepositoryCheckpointReferenceObservation(
        observation_id=observation_id,
        repository_id=repository_id,
        git_dir_fingerprint=git_dir_fingerprint,
        checkpoint_reference=checkpoint_reference,
        observed_oid=observed_oid,
        rechecked_oid=rechecked_oid,
        direct=direct,
        symbolic=symbolic,
        reference_store_read=reference_store_read,
        working_tree_read=working_tree_read,
        reflog_read=reflog_read,
        remote_read=remote_read,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        rechecked_at_epoch_seconds=rechecked_at_epoch_seconds,
        observation_digest="",
    )
    observation = replace(
        observation,
        observation_digest=repository_checkpoint_reference_observation_digest(
            observation
        ),
    )
    issues = repository_checkpoint_reference_observation_issues(observation)
    if issues:
        raise ValueError(f"checkpoint_observation_invalid:{issues[0]}")
    return observation


def repository_checkpoint_reference_observation_issues(
    observation: RepositoryCheckpointReferenceObservation,
) -> tuple[str, ...]:
    issues: list[str] = []
    if any(
        not value
        for value in (
            observation.observation_id,
            observation.repository_id,
            observation.git_dir_fingerprint,
            observation.checkpoint_reference,
        )
    ):
        issues.append("checkpoint_observation_required_field_missing")
    if not _HEX64.fullmatch(observation.git_dir_fingerprint):
        issues.append("checkpoint_observation_git_dir_invalid")
    if not _HEX40.fullmatch(observation.observed_oid):
        issues.append("checkpoint_observation_oid_invalid")
    if not _HEX40.fullmatch(observation.rechecked_oid):
        issues.append("checkpoint_observation_rechecked_oid_invalid")
    if observation.observed_at_epoch_seconds < 0:
        issues.append("checkpoint_observation_time_negative")
    if observation.rechecked_at_epoch_seconds < observation.observed_at_epoch_seconds:
        issues.append("checkpoint_observation_recheck_order_invalid")
    if observation.observation_digest != (
        repository_checkpoint_reference_observation_digest(observation)
    ):
        issues.append("checkpoint_observation_digest_mismatch")
    return tuple(issues)


def build_repository_local_frontier_checkpoint_scope(
    scope_id: str,
    finality_certificate: RepositoryLocalFrontierFinalityCertificate,
    policy: RepositoryLocalFrontierCheckpointPolicy,
    observation: RepositoryCheckpointReferenceObservation,
    *,
    authorization_nonce: str,
    issued_at_epoch_seconds: int,
    expires_at_epoch_seconds: int,
    create_requested: bool = True,
    overwrite_requested: bool = False,
    delete_requested: bool = False,
    force_update_requested: bool = False,
    tag_creation_requested: bool = False,
    push_requested: bool = False,
) -> RepositoryLocalFrontierCheckpointScope:
    scope = RepositoryLocalFrontierCheckpointScope(
        scope_id=scope_id,
        finality_certificate_digest=finality_certificate.certificate_digest,
        authorization_policy_digest=policy.policy_digest,
        checkpoint_observation_digest=observation.observation_digest,
        repository_id=finality_certificate.repository_id,
        git_dir_fingerprint=finality_certificate.git_dir_fingerprint,
        checkpoint_reference=observation.checkpoint_reference,
        expected_old_oid=observation.rechecked_oid,
        proposed_new_oid=finality_certificate.final_tip_oid,
        transaction_id=finality_certificate.transaction_id,
        create_requested=create_requested,
        overwrite_requested=overwrite_requested,
        delete_requested=delete_requested,
        force_update_requested=force_update_requested,
        tag_creation_requested=tag_creation_requested,
        push_requested=push_requested,
        authorization_nonce=authorization_nonce,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        expires_at_epoch_seconds=expires_at_epoch_seconds,
        scope_digest="",
    )
    scope = replace(
        scope,
        scope_digest=repository_local_frontier_checkpoint_scope_digest(scope),
    )
    issues = repository_local_frontier_checkpoint_scope_issues(scope)
    if issues:
        raise ValueError(f"checkpoint_scope_invalid:{issues[0]}")
    return scope


def repository_local_frontier_checkpoint_scope_issues(
    scope: RepositoryLocalFrontierCheckpointScope,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        scope.scope_id,
        scope.finality_certificate_digest,
        scope.authorization_policy_digest,
        scope.checkpoint_observation_digest,
        scope.repository_id,
        scope.git_dir_fingerprint,
        scope.checkpoint_reference,
        scope.transaction_id,
        scope.authorization_nonce,
    )
    if any(not value for value in required):
        issues.append("checkpoint_scope_required_field_missing")
    for digest in (
        scope.finality_certificate_digest,
        scope.authorization_policy_digest,
        scope.checkpoint_observation_digest,
        scope.git_dir_fingerprint,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("checkpoint_scope_digest_invalid")
            break
    if not _HEX40.fullmatch(scope.expected_old_oid):
        issues.append("checkpoint_scope_old_oid_invalid")
    if not _HEX40.fullmatch(scope.proposed_new_oid):
        issues.append("checkpoint_scope_new_oid_invalid")
    if scope.issued_at_epoch_seconds < 0:
        issues.append("checkpoint_scope_issued_at_negative")
    if scope.expires_at_epoch_seconds <= scope.issued_at_epoch_seconds:
        issues.append("checkpoint_scope_expiry_invalid")
    if scope.scope_digest != repository_local_frontier_checkpoint_scope_digest(scope):
        issues.append("checkpoint_scope_digest_mismatch")
    return tuple(issues)


def build_repository_local_frontier_checkpoint_nonce_status_receipt(
    status_id: str,
    scope: RepositoryLocalFrontierCheckpointScope,
    *,
    authority_id: str,
    checked_at_epoch_seconds: int,
    registry_snapshot_digest: str,
    consumed: bool,
    revoked: bool,
) -> RepositoryLocalFrontierCheckpointNonceStatusReceipt:
    receipt = RepositoryLocalFrontierCheckpointNonceStatusReceipt(
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
        receipt_digest=(
            repository_local_frontier_checkpoint_nonce_status_receipt_digest(
                receipt
            )
        ),
    )
    issues = repository_local_frontier_checkpoint_nonce_status_receipt_issues(
        receipt
    )
    if issues:
        raise ValueError(f"checkpoint_nonce_status_invalid:{issues[0]}")
    return receipt


def repository_local_frontier_checkpoint_nonce_status_receipt_issues(
    receipt: RepositoryLocalFrontierCheckpointNonceStatusReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    if any(
        not value
        for value in (
            receipt.status_id,
            receipt.authorization_nonce,
            receipt.authorization_scope_digest,
            receipt.authority_id,
            receipt.registry_snapshot_digest,
        )
    ):
        issues.append("checkpoint_nonce_required_field_missing")
    if not _HEX64.fullmatch(receipt.authorization_scope_digest):
        issues.append("checkpoint_nonce_scope_digest_invalid")
    if not _HEX64.fullmatch(receipt.registry_snapshot_digest):
        issues.append("checkpoint_nonce_registry_digest_invalid")
    if receipt.checked_at_epoch_seconds < 0:
        issues.append("checkpoint_nonce_checked_at_negative")
    if receipt.receipt_digest != (
        repository_local_frontier_checkpoint_nonce_status_receipt_digest(receipt)
    ):
        issues.append("checkpoint_nonce_receipt_digest_mismatch")
    return tuple(issues)


def _finality_issues(
    certificate: RepositoryLocalFrontierFinalityCertificate,
    inputs: Mapping[str, Any],
) -> tuple[str, ...]:
    try:
        return repository_local_frontier_finality_certificate_issues(
            certificate,
            **dict(inputs),
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("local_frontier_finality_inputs_invalid",)


def _construct_checkpoint_authorization_certificate(
    authorization_id: str,
    finality_certificate: RepositoryLocalFrontierFinalityCertificate,
    finality_inputs: Mapping[str, Any],
    policy: RepositoryLocalFrontierCheckpointPolicy,
    observation: RepositoryCheckpointReferenceObservation,
    scope: RepositoryLocalFrontierCheckpointScope,
    nonce_status: RepositoryLocalFrontierCheckpointNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryLocalFrontierCheckpointAuthorizationCertificate:
    history = finality_inputs.get("history")
    final_sample = history.samples[-1] if history is not None and history.samples else None
    finality_issues = _finality_issues(finality_certificate, finality_inputs)
    finality_certificate_valid = not finality_issues
    finality_certificate_committed = bool(
        finality_certificate_valid
        and finality_certificate.status == FINALITY_COMMITTED
        and finality_certificate.certificate_committed
        and finality_certificate.bounded_local_finality_verified
        and finality_certificate.local_frontier_history_monotone
        and finality_certificate.candidate_reachability_continuous
    )
    finality_certificate_binding_exact = bool(
        scope.finality_certificate_digest == finality_certificate.certificate_digest
        and scope.repository_id == finality_certificate.repository_id
        and scope.git_dir_fingerprint == finality_certificate.git_dir_fingerprint
        and scope.proposed_new_oid == finality_certificate.final_tip_oid
        and scope.transaction_id == finality_certificate.transaction_id
    )
    finality_history_bound = bool(
        final_sample is not None
        and history.history_digest == finality_certificate.history_digest
        and final_sample.repository_id == finality_certificate.repository_id
        and final_sample.git_dir_fingerprint
        == finality_certificate.git_dir_fingerprint
        and final_sample.target_reference
        == finality_certificate.target_reference
        and final_sample.candidate_commit_oid
        == finality_certificate.candidate_commit_oid
        and final_sample.observed_tip_oid == finality_certificate.final_tip_oid
        and final_sample.observed_at_epoch_seconds
        == finality_certificate.final_observed_at_epoch_seconds
    )
    policy_valid = not repository_local_frontier_checkpoint_policy_issues(policy)
    repository_allowed = scope.repository_id in policy.allowed_repository_ids
    repository_identity_exact = bool(
        scope.repository_id
        == finality_certificate.repository_id
        == observation.repository_id
        and scope.git_dir_fingerprint
        == finality_certificate.git_dir_fingerprint
        == observation.git_dir_fingerprint
    )
    normalized = normalize_repository_checkpoint_reference_name(
        scope.checkpoint_reference
    )
    checkpoint_name_valid = normalized is not None
    checkpoint_name_normalized = normalized == scope.checkpoint_reference
    checkpoint_reference_allowed = (
        scope.checkpoint_reference in policy.allowed_checkpoint_references
    )
    checkpoint_namespace_exact = scope.checkpoint_reference.startswith(
        CHECKPOINT_NAMESPACE
    )
    checkpoint_reference_direct = bool(
        observation.direct and policy.require_direct_checkpoint_reference
    )
    checkpoint_reference_not_symbolic = not observation.symbolic
    checkpoint_reference_not_head = scope.checkpoint_reference != "HEAD"
    checkpoint_reference_not_branch = not scope.checkpoint_reference.startswith(
        "refs/heads/"
    )
    checkpoint_reference_not_tag = not scope.checkpoint_reference.startswith(
        "refs/tags/"
    )
    checkpoint_reference_not_remote = not scope.checkpoint_reference.startswith(
        "refs/remotes/"
    )
    checkpoint_reference_not_notes = not scope.checkpoint_reference.startswith(
        "refs/notes/"
    )
    checkpoint_reference_not_replace = not scope.checkpoint_reference.startswith(
        "refs/replace/"
    )
    checkpoint_observation_bound = bool(
        scope.checkpoint_observation_digest == observation.observation_digest
        and scope.checkpoint_reference == observation.checkpoint_reference
        and scope.expected_old_oid == observation.rechecked_oid
    )
    observation_age = (
        evaluated_at_epoch_seconds - observation.rechecked_at_epoch_seconds
    )
    checkpoint_observation_fresh = bool(
        0
        <= observation_age
        <= policy.max_reference_observation_age_seconds
    )
    checkpoint_reference_store_source = bool(
        observation.reference_store_read
        and policy.require_reference_store_source
    )
    checkpoint_working_tree_ignored = bool(
        not observation.working_tree_read and policy.require_working_tree_ignored
    )
    checkpoint_reflog_ignored = bool(
        not observation.reflog_read and policy.require_reflog_ignored
    )
    checkpoint_remote_ignored = bool(
        not observation.remote_read and policy.require_remote_ignored
    )
    checkpoint_unchanged_since_observation = bool(
        observation.observed_oid
        == observation.rechecked_oid
        == scope.expected_old_oid
    )
    checkpoint_absent = bool(
        observation.observed_oid == ZERO_OID
        and observation.rechecked_oid == ZERO_OID
        and scope.expected_old_oid == ZERO_OID
    )
    compare_and_swap_nonexistence_required = bool(
        policy.require_compare_and_swap_nonexistence
        and scope.expected_old_oid == ZERO_OID
    )
    final_tip_exact = bool(
        policy.require_exact_final_tip
        and final_sample is not None
        and scope.proposed_new_oid
        == finality_certificate.final_tip_oid
        == final_sample.observed_tip_oid
    )
    final_tip_present = bool(
        final_sample is not None
        and finality_certificate.tips_present_in_every_sample
        and finality_certificate.final_tip_oid
        in final_sample.object_database_commit_oids
    )
    nonce_authority_authorized = (
        nonce_status.authority_id in policy.authorized_nonce_authority_ids
    )
    nonce_scope_bound = bool(
        nonce_status.authorization_nonce == scope.authorization_nonce
        and nonce_status.authorization_scope_digest == scope.scope_digest
    )
    nonce_age = evaluated_at_epoch_seconds - nonce_status.checked_at_epoch_seconds
    nonce_status_fresh = bool(
        0 <= nonce_age <= policy.max_nonce_status_age_seconds
    )
    nonce_unused = not nonce_status.consumed
    nonce_not_revoked = not nonce_status.revoked
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
            finality_certificate.evaluated_at_epoch_seconds,
            observation.observed_at_epoch_seconds,
            observation.rechecked_at_epoch_seconds,
            nonce_status.checked_at_epoch_seconds,
            scope.issued_at_epoch_seconds,
        )
    )
    create_requested = scope.create_requested
    overwrite_not_requested = bool(
        not scope.overwrite_requested and not policy.allow_checkpoint_overwrite
    )
    delete_not_requested = bool(
        not scope.delete_requested and not policy.allow_reference_delete
    )
    force_update_not_requested = bool(
        not scope.force_update_requested and not policy.allow_force_update
    )
    tag_creation_not_requested = bool(
        not scope.tag_creation_requested and not policy.allow_tag_creation
    )
    push_not_requested = bool(
        not scope.push_requested and not policy.allow_push
    )
    single_use_checkpoint_creation_eligible = all(
        (
            nonce_authority_authorized,
            nonce_scope_bound,
            nonce_status_fresh,
            nonce_unused,
            nonce_not_revoked,
            authorization_lifetime_within_policy,
            authorization_not_expired,
        )
    )
    granted = all(
        (
            finality_certificate_valid,
            finality_certificate_committed,
            finality_certificate_binding_exact,
            finality_history_bound,
            policy_valid,
            repository_allowed,
            repository_identity_exact,
            checkpoint_name_valid,
            checkpoint_name_normalized,
            checkpoint_reference_allowed,
            checkpoint_namespace_exact,
            checkpoint_reference_direct,
            checkpoint_reference_not_symbolic,
            checkpoint_reference_not_head,
            checkpoint_reference_not_branch,
            checkpoint_reference_not_tag,
            checkpoint_reference_not_remote,
            checkpoint_reference_not_notes,
            checkpoint_reference_not_replace,
            checkpoint_observation_bound,
            checkpoint_observation_fresh,
            checkpoint_reference_store_source,
            checkpoint_working_tree_ignored,
            checkpoint_reflog_ignored,
            checkpoint_remote_ignored,
            checkpoint_unchanged_since_observation,
            checkpoint_absent,
            compare_and_swap_nonexistence_required,
            final_tip_exact,
            final_tip_present,
            single_use_checkpoint_creation_eligible,
            no_future_evidence,
            create_requested,
            overwrite_not_requested,
            delete_not_requested,
            force_update_not_requested,
            tag_creation_not_requested,
            push_not_requested,
        )
    )
    certificate = RepositoryLocalFrontierCheckpointAuthorizationCertificate(
        authorization_id=authorization_id,
        status=AUTHORIZATION_GRANTED if granted else AUTHORIZATION_REJECTED,
        finality_certificate_digest=finality_certificate.certificate_digest,
        authorization_policy_digest=policy.policy_digest,
        checkpoint_scope_digest=scope.scope_digest,
        checkpoint_observation_digest=observation.observation_digest,
        nonce_status_receipt_digest=nonce_status.receipt_digest,
        repository_id=scope.repository_id,
        git_dir_fingerprint=scope.git_dir_fingerprint,
        checkpoint_reference=scope.checkpoint_reference,
        expected_old_oid=scope.expected_old_oid,
        proposed_new_oid=scope.proposed_new_oid,
        transaction_id=scope.transaction_id,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        finality_certificate_valid=finality_certificate_valid,
        finality_certificate_committed=finality_certificate_committed,
        finality_certificate_binding_exact=finality_certificate_binding_exact,
        finality_history_bound=finality_history_bound,
        policy_valid=policy_valid,
        repository_allowed=repository_allowed,
        repository_identity_exact=repository_identity_exact,
        checkpoint_name_valid=checkpoint_name_valid,
        checkpoint_name_normalized=checkpoint_name_normalized,
        checkpoint_reference_allowed=checkpoint_reference_allowed,
        checkpoint_namespace_exact=checkpoint_namespace_exact,
        checkpoint_reference_direct=checkpoint_reference_direct,
        checkpoint_reference_not_symbolic=checkpoint_reference_not_symbolic,
        checkpoint_reference_not_head=checkpoint_reference_not_head,
        checkpoint_reference_not_branch=checkpoint_reference_not_branch,
        checkpoint_reference_not_tag=checkpoint_reference_not_tag,
        checkpoint_reference_not_remote=checkpoint_reference_not_remote,
        checkpoint_reference_not_notes=checkpoint_reference_not_notes,
        checkpoint_reference_not_replace=checkpoint_reference_not_replace,
        checkpoint_observation_bound=checkpoint_observation_bound,
        checkpoint_observation_fresh=checkpoint_observation_fresh,
        checkpoint_reference_store_source=checkpoint_reference_store_source,
        checkpoint_working_tree_ignored=checkpoint_working_tree_ignored,
        checkpoint_reflog_ignored=checkpoint_reflog_ignored,
        checkpoint_remote_ignored=checkpoint_remote_ignored,
        checkpoint_unchanged_since_observation=(
            checkpoint_unchanged_since_observation
        ),
        checkpoint_absent=checkpoint_absent,
        compare_and_swap_nonexistence_required=(
            compare_and_swap_nonexistence_required
        ),
        final_tip_exact=final_tip_exact,
        final_tip_present=final_tip_present,
        nonce_authority_authorized=nonce_authority_authorized,
        nonce_scope_bound=nonce_scope_bound,
        nonce_status_fresh=nonce_status_fresh,
        nonce_unused=nonce_unused,
        nonce_not_revoked=nonce_not_revoked,
        authorization_lifetime_within_policy=(
            authorization_lifetime_within_policy
        ),
        authorization_not_expired=authorization_not_expired,
        no_future_evidence=no_future_evidence,
        create_requested=create_requested,
        overwrite_not_requested=overwrite_not_requested,
        delete_not_requested=delete_not_requested,
        force_update_not_requested=force_update_not_requested,
        tag_creation_not_requested=tag_creation_not_requested,
        push_not_requested=push_not_requested,
        single_use_checkpoint_creation_eligible=(
            single_use_checkpoint_creation_eligible
        ),
        checkpoint_creation_authority_granted=granted,
        checkpoint_creation_authorized=granted,
        checkpoint_overwrite_authorized=False,
        force_update_authorized=False,
        reference_delete_authorized=False,
        tag_creation_authorized=False,
        push_authorized=False,
        checkpoint_created=False,
        checkpoint_reference_mutated=False,
        branch_updated=False,
        tag_updated=False,
        remote_reference_updated=False,
        push_performed=False,
        index_write_performed=False,
        working_tree_write_performed=False,
        object_database_write_performed=False,
        reflog_write_performed=False,
        signing_performed=False,
        certificate_digest="",
    )
    return replace(
        certificate,
        certificate_digest=(
            repository_local_frontier_checkpoint_authorization_certificate_digest(
                certificate
            )
        ),
    )


def authorize_repository_local_frontier_checkpoint_creation(
    authorization_id: str,
    finality_certificate: RepositoryLocalFrontierFinalityCertificate,
    finality_inputs: Mapping[str, Any],
    policy: RepositoryLocalFrontierCheckpointPolicy,
    observation: RepositoryCheckpointReferenceObservation,
    scope: RepositoryLocalFrontierCheckpointScope,
    nonce_status: RepositoryLocalFrontierCheckpointNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryLocalFrontierCheckpointAuthorizationCertificate:
    if not authorization_id:
        raise ValueError("checkpoint_authorization_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("checkpoint_authorization_evaluated_at_negative")
    finality_issues = _finality_issues(finality_certificate, finality_inputs)
    if finality_issues:
        raise ValueError(f"local_frontier_finality_invalid:{finality_issues[0]}")
    for issues, prefix in (
        (
            repository_local_frontier_checkpoint_policy_issues(policy),
            "checkpoint_policy_invalid",
        ),
        (
            repository_checkpoint_reference_observation_issues(observation),
            "checkpoint_observation_invalid",
        ),
        (
            repository_local_frontier_checkpoint_scope_issues(scope),
            "checkpoint_scope_invalid",
        ),
        (
            repository_local_frontier_checkpoint_nonce_status_receipt_issues(
                nonce_status
            ),
            "checkpoint_nonce_status_invalid",
        ),
    ):
        if issues:
            raise ValueError(f"{prefix}:{issues[0]}")
    certificate = _construct_checkpoint_authorization_certificate(
        authorization_id,
        finality_certificate,
        finality_inputs,
        policy,
        observation,
        scope,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_local_frontier_checkpoint_authorization_certificate_issues(
        certificate,
        finality_certificate,
        finality_inputs,
        policy,
        observation,
        scope,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"checkpoint_authorization_invalid:{issues[0]}")
    return certificate


def repository_local_frontier_checkpoint_authorization_certificate_issues(
    certificate: RepositoryLocalFrontierCheckpointAuthorizationCertificate,
    finality_certificate: RepositoryLocalFrontierFinalityCertificate,
    finality_inputs: Mapping[str, Any],
    policy: RepositoryLocalFrontierCheckpointPolicy,
    observation: RepositoryCheckpointReferenceObservation,
    scope: RepositoryLocalFrontierCheckpointScope,
    nonce_status: RepositoryLocalFrontierCheckpointNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    if _finality_issues(finality_certificate, finality_inputs):
        issues.append("local_frontier_finality_invalid")
        return tuple(issues)
    for validator, name in (
        (
            repository_local_frontier_checkpoint_policy_issues(policy),
            "checkpoint_policy_invalid",
        ),
        (
            repository_checkpoint_reference_observation_issues(observation),
            "checkpoint_observation_invalid",
        ),
        (
            repository_local_frontier_checkpoint_scope_issues(scope),
            "checkpoint_scope_invalid",
        ),
        (
            repository_local_frontier_checkpoint_nonce_status_receipt_issues(
                nonce_status
            ),
            "checkpoint_nonce_status_invalid",
        ),
    ):
        if validator:
            issues.append(name)
            return tuple(issues)
    expected = _construct_checkpoint_authorization_certificate(
        certificate.authorization_id,
        finality_certificate,
        finality_inputs,
        policy,
        observation,
        scope,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if certificate.to_dict() != expected.to_dict():
        issues.append("checkpoint_authorization_recomputation_mismatch")
    if certificate.status not in (AUTHORIZATION_GRANTED, AUTHORIZATION_REJECTED):
        issues.append("checkpoint_authorization_status_invalid")
    forbidden = (
        certificate.checkpoint_overwrite_authorized,
        certificate.force_update_authorized,
        certificate.reference_delete_authorized,
        certificate.tag_creation_authorized,
        certificate.push_authorized,
        certificate.checkpoint_created,
        certificate.checkpoint_reference_mutated,
        certificate.branch_updated,
        certificate.tag_updated,
        certificate.remote_reference_updated,
        certificate.push_performed,
        certificate.index_write_performed,
        certificate.working_tree_write_performed,
        certificate.object_database_write_performed,
        certificate.reflog_write_performed,
        certificate.signing_performed,
    )
    if any(forbidden):
        issues.append("checkpoint_authorization_forbidden_effect_or_authority")
    if certificate.status == AUTHORIZATION_GRANTED:
        required_true = (
            certificate.finality_certificate_valid,
            certificate.finality_certificate_committed,
            certificate.finality_certificate_binding_exact,
            certificate.finality_history_bound,
            certificate.policy_valid,
            certificate.repository_allowed,
            certificate.repository_identity_exact,
            certificate.checkpoint_name_valid,
            certificate.checkpoint_name_normalized,
            certificate.checkpoint_reference_allowed,
            certificate.checkpoint_namespace_exact,
            certificate.checkpoint_reference_direct,
            certificate.checkpoint_reference_not_symbolic,
            certificate.checkpoint_reference_not_head,
            certificate.checkpoint_reference_not_branch,
            certificate.checkpoint_reference_not_tag,
            certificate.checkpoint_reference_not_remote,
            certificate.checkpoint_reference_not_notes,
            certificate.checkpoint_reference_not_replace,
            certificate.checkpoint_observation_bound,
            certificate.checkpoint_observation_fresh,
            certificate.checkpoint_reference_store_source,
            certificate.checkpoint_working_tree_ignored,
            certificate.checkpoint_reflog_ignored,
            certificate.checkpoint_remote_ignored,
            certificate.checkpoint_unchanged_since_observation,
            certificate.checkpoint_absent,
            certificate.compare_and_swap_nonexistence_required,
            certificate.final_tip_exact,
            certificate.final_tip_present,
            certificate.nonce_authority_authorized,
            certificate.nonce_scope_bound,
            certificate.nonce_status_fresh,
            certificate.nonce_unused,
            certificate.nonce_not_revoked,
            certificate.authorization_lifetime_within_policy,
            certificate.authorization_not_expired,
            certificate.no_future_evidence,
            certificate.create_requested,
            certificate.overwrite_not_requested,
            certificate.delete_not_requested,
            certificate.force_update_not_requested,
            certificate.tag_creation_not_requested,
            certificate.push_not_requested,
            certificate.single_use_checkpoint_creation_eligible,
            certificate.checkpoint_creation_authority_granted,
            certificate.checkpoint_creation_authorized,
        )
        if not all(required_true):
            issues.append("checkpoint_authorization_granted_invariant_false")
    elif (
        certificate.checkpoint_creation_authority_granted
        or certificate.checkpoint_creation_authorized
    ):
        issues.append("checkpoint_authorization_rejected_marked_authorized")
    if certificate.certificate_digest != (
        repository_local_frontier_checkpoint_authorization_certificate_digest(
            certificate
        )
    ):
        issues.append("checkpoint_authorization_certificate_digest_mismatch")
    return tuple(issues)
