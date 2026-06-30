#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re

from runtime.kuuos_repository_checkpoint_cas_authorization_request_types_v1_14 import (
    REASON_COHERENT_CONFLICT,
    REASON_COHERENT_READY,
    REQUEST_DENIED,
    REQUEST_READY,
    RepositoryCheckpointCasAuthorizationRequest,
    repository_checkpoint_cas_authorization_request_digest,
)
from runtime.kuuos_repository_checkpoint_cas_single_use_authorization_types_v1_15 import (
    AUTHORIZATION_DENIED,
    AUTHORIZATION_GRANTED,
    AUTHORIZATION_REJECTED,
    REASON_DENIAL_PRESERVED,
    REASON_INVALID_AUTHORIZATION,
    REASON_READY_AUTHORIZED,
    RepositoryCheckpointCasAuthorizationNonceStatusReceipt,
    RepositoryCheckpointCasAuthorizationPolicy,
    RepositoryCheckpointCasSingleUseAuthorizationCertificate,
    repository_checkpoint_cas_authorization_nonce_status_receipt_digest,
    repository_checkpoint_cas_authorization_policy_digest,
    repository_checkpoint_cas_single_use_authorization_certificate_digest,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_ZERO_OID = "0" * 40


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_cas_authorization_policy(
    policy_id: str,
    *,
    allowed_authority_ids: tuple[str, ...],
    max_nonce_status_age_seconds: int,
) -> RepositoryCheckpointCasAuthorizationPolicy:
    policy = RepositoryCheckpointCasAuthorizationPolicy(
        policy_id=policy_id,
        allowed_authority_ids=_canonical(allowed_authority_ids),
        max_nonce_status_age_seconds=max_nonce_status_age_seconds,
        require_valid_v114_request=True,
        require_exact_nonce_request_binding=True,
        require_unused_nonce=True,
        require_unrevoked_nonce=True,
        require_single_use_scope=True,
        authorization_only=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_cas_authorization_policy_digest(policy),
    )
    issues = repository_checkpoint_cas_authorization_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_cas_authorization_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_cas_authorization_policy_issues(
    policy: RepositoryCheckpointCasAuthorizationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_cas_authorization_policy_id_missing")
    if policy.allowed_authority_ids != _canonical(policy.allowed_authority_ids):
        issues.append("checkpoint_cas_authorization_authority_ids_not_canonical")
    if not policy.allowed_authority_ids or any(
        not value for value in policy.allowed_authority_ids
    ):
        issues.append("checkpoint_cas_authorization_authority_ids_empty")
    if policy.max_nonce_status_age_seconds <= 0:
        issues.append("checkpoint_cas_authorization_nonce_age_invalid")
    if not all(
        (
            policy.require_valid_v114_request,
            policy.require_exact_nonce_request_binding,
            policy.require_unused_nonce,
            policy.require_unrevoked_nonce,
            policy.require_single_use_scope,
            policy.authorization_only,
        )
    ):
        issues.append("checkpoint_cas_authorization_guard_disabled")
    if policy.policy_digest != repository_checkpoint_cas_authorization_policy_digest(
        policy
    ):
        issues.append("checkpoint_cas_authorization_policy_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_cas_authorization_nonce_status_receipt(
    status_id: str,
    *,
    authorization_nonce: str,
    authorization_request_digest: str,
    authority_id: str,
    checked_at_epoch_seconds: int,
    registry_snapshot_digest: str,
    consumed: bool,
    revoked: bool,
) -> RepositoryCheckpointCasAuthorizationNonceStatusReceipt:
    receipt = RepositoryCheckpointCasAuthorizationNonceStatusReceipt(
        status_id=status_id,
        authorization_nonce=authorization_nonce,
        authorization_request_digest=authorization_request_digest,
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
            repository_checkpoint_cas_authorization_nonce_status_receipt_digest(
                receipt
            )
        ),
    )
    issues = repository_checkpoint_cas_authorization_nonce_status_receipt_issues(
        receipt
    )
    if issues:
        raise ValueError(f"checkpoint_cas_authorization_nonce_status_invalid:{issues[0]}")
    return receipt


def repository_checkpoint_cas_authorization_nonce_status_receipt_issues(
    receipt: RepositoryCheckpointCasAuthorizationNonceStatusReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    if any(
        not value
        for value in (
            receipt.status_id,
            receipt.authorization_nonce,
            receipt.authority_id,
        )
    ):
        issues.append("checkpoint_cas_authorization_nonce_required_field_missing")
    if not _HEX64.fullmatch(receipt.authorization_request_digest):
        issues.append("checkpoint_cas_authorization_nonce_request_digest_invalid")
    if not _HEX64.fullmatch(receipt.registry_snapshot_digest):
        issues.append("checkpoint_cas_authorization_registry_digest_invalid")
    if receipt.checked_at_epoch_seconds < 0:
        issues.append("checkpoint_cas_authorization_nonce_time_negative")
    if receipt.receipt_digest != (
        repository_checkpoint_cas_authorization_nonce_status_receipt_digest(receipt)
    ):
        issues.append("checkpoint_cas_authorization_nonce_digest_mismatch")
    return tuple(issues)


def repository_checkpoint_cas_authorization_request_local_validity(
    request: RepositoryCheckpointCasAuthorizationRequest,
) -> bool:
    digest_valid = request.request_digest == (
        repository_checkpoint_cas_authorization_request_digest(request)
    )
    evidence_exact = bool(
        request.evidence_digests.get("checkpoint_cas_coherence")
        == request.coherence_digest
        and request.evidence_digests.get("authorization_request_policy")
        == request.request_policy_digest
    )
    oids = (
        request.expected_current_oid,
        request.observed_current_oid,
        request.proposed_checkpoint_oid,
    )
    oid_valid = bool(
        all(_HEX40.fullmatch(oid) and oid != _ZERO_OID for oid in oids)
        and request.expected_current_oid != request.proposed_checkpoint_oid
    )
    common = all(
        (
            digest_valid,
            request.status in (REQUEST_READY, REQUEST_DENIED),
            bool(request.request_id),
            bool(request.coherence_digest),
            bool(request.request_policy_digest),
            bool(request.requester_id),
            bool(request.authorization_nonce),
            bool(request.repository_id),
            bool(request.git_dir_fingerprint),
            bool(request.checkpoint_reference),
            request.issued_at_epoch_seconds >= 0,
            request.expires_at_epoch_seconds > request.issued_at_epoch_seconds,
            request.coherence_receipt_valid,
            request.repository_allowed,
            request.checkpoint_reference_allowed,
            request.lifetime_within_policy,
            request.request_not_expired_at_issue,
            request.nonce_present,
            not request.authorization_granted,
            not request.execution_performed,
            not request.live_git_command_invoked,
            not request.reference_mutated,
            evidence_exact,
            oid_valid,
            request.checks.get("policy_valid") is True,
            request.checks.get("coherence_receipt_valid")
            == request.coherence_receipt_valid,
            request.checks.get("repository_allowed") == request.repository_allowed,
            request.checks.get("checkpoint_reference_allowed")
            == request.checkpoint_reference_allowed,
            request.checks.get("lifetime_within_policy")
            == request.lifetime_within_policy,
            request.checks.get("request_not_expired_at_issue")
            == request.request_not_expired_at_issue,
            request.checks.get("nonce_present") == request.nonce_present,
            request.checks.get("single_use_authorization_required")
            == request.single_use_authorization_required,
            request.checks.get("authorization_granted")
            == request.authorization_granted,
            request.checks.get("execution_performed") == request.execution_performed,
            request.checks.get("live_git_command_invoked")
            == request.live_git_command_invoked,
            request.checks.get("reference_mutated") == request.reference_mutated,
        )
    )
    if not common:
        return False
    if request.status == REQUEST_READY:
        return bool(
            request.reason == REASON_COHERENT_READY
            and request.single_use_authorization_required
            and request.observed_current_oid == request.expected_current_oid
        )
    return bool(
        request.reason == REASON_COHERENT_CONFLICT
        and not request.single_use_authorization_required
        and request.observed_current_oid != request.expected_current_oid
    )


def construct_repository_checkpoint_cas_single_use_authorization(
    authorization_id: str,
    request: RepositoryCheckpointCasAuthorizationRequest,
    policy: RepositoryCheckpointCasAuthorizationPolicy,
    nonce_status: RepositoryCheckpointCasAuthorizationNonceStatusReceipt | None,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryCheckpointCasSingleUseAuthorizationCertificate:
    request_valid = repository_checkpoint_cas_authorization_request_local_validity(
        request
    )
    policy_valid = not repository_checkpoint_cas_authorization_policy_issues(policy)
    denial_preserved = bool(
        request_valid and policy_valid and request.status == REQUEST_DENIED
    )
    nonce_status_required = bool(
        request_valid and policy_valid and request.status == REQUEST_READY
    )
    nonce_status_valid = bool(
        nonce_status is not None
        and not repository_checkpoint_cas_authorization_nonce_status_receipt_issues(
            nonce_status
        )
    )
    nonce_request_binding_exact = bool(
        nonce_status is not None
        and nonce_status.authorization_request_digest == request.request_digest
        and nonce_status.authorization_nonce == request.authorization_nonce
    )
    nonce_authority_allowed = bool(
        nonce_status is not None
        and nonce_status.authority_id in policy.allowed_authority_ids
    )
    nonce_status_fresh = bool(
        nonce_status is not None
        and evaluated_at_epoch_seconds >= nonce_status.checked_at_epoch_seconds
        and nonce_status.checked_at_epoch_seconds >= request.issued_at_epoch_seconds
        and evaluated_at_epoch_seconds - nonce_status.checked_at_epoch_seconds
        <= policy.max_nonce_status_age_seconds
    )
    nonce_unused = bool(nonce_status is not None and not nonce_status.consumed)
    nonce_not_revoked = bool(nonce_status is not None and not nonce_status.revoked)
    authorization_not_expired = bool(
        evaluated_at_epoch_seconds >= request.issued_at_epoch_seconds
        and evaluated_at_epoch_seconds < request.expires_at_epoch_seconds
    )
    single_use_scope_exact = bool(
        request.single_use_authorization_required
        and policy.require_single_use_scope
    )
    ready_authorized = all(
        (
            bool(authorization_id),
            evaluated_at_epoch_seconds >= 0,
            request_valid,
            policy_valid,
            request.status == REQUEST_READY,
            nonce_status_required,
            nonce_status_valid,
            nonce_request_binding_exact,
            nonce_authority_allowed,
            nonce_status_fresh,
            nonce_unused,
            nonce_not_revoked,
            authorization_not_expired,
            single_use_scope_exact,
        )
    )

    if ready_authorized:
        status = AUTHORIZATION_GRANTED
        reason = REASON_READY_AUTHORIZED
    elif bool(authorization_id) and evaluated_at_epoch_seconds >= 0 and denial_preserved:
        status = AUTHORIZATION_DENIED
        reason = REASON_DENIAL_PRESERVED
    else:
        status = AUTHORIZATION_REJECTED
        reason = REASON_INVALID_AUTHORIZATION

    authorization_granted = status == AUTHORIZATION_GRANTED
    authority_id = nonce_status.authority_id if nonce_status is not None else ""
    nonce_digest = nonce_status.receipt_digest if nonce_status is not None else ""
    certificate = RepositoryCheckpointCasSingleUseAuthorizationCertificate(
        authorization_id=authorization_id,
        status=status,
        reason=reason,
        authorization_request_digest=request.request_digest,
        authorization_policy_digest=policy.policy_digest,
        nonce_status_receipt_digest=nonce_digest,
        authority_id=authority_id,
        authorization_nonce=request.authorization_nonce,
        repository_id=request.repository_id,
        git_dir_fingerprint=request.git_dir_fingerprint,
        checkpoint_reference=request.checkpoint_reference,
        expected_current_oid=request.expected_current_oid,
        observed_current_oid=request.observed_current_oid,
        proposed_checkpoint_oid=request.proposed_checkpoint_oid,
        request_expires_at_epoch_seconds=request.expires_at_epoch_seconds,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        request_valid=request_valid,
        policy_valid=policy_valid,
        denial_preserved=denial_preserved,
        nonce_status_required=nonce_status_required,
        nonce_status_valid=nonce_status_valid,
        nonce_request_binding_exact=nonce_request_binding_exact,
        nonce_authority_allowed=nonce_authority_allowed,
        nonce_status_fresh=nonce_status_fresh,
        nonce_unused=nonce_unused,
        nonce_not_revoked=nonce_not_revoked,
        authorization_not_expired=authorization_not_expired,
        single_use_scope_exact=single_use_scope_exact,
        authorization_granted=authorization_granted,
        execution_performed=False,
        live_git_command_invoked=False,
        reference_mutated=False,
        nonce_consumed=False,
        checks={
            "request_valid": request_valid,
            "policy_valid": policy_valid,
            "denial_preserved": denial_preserved,
            "nonce_status_required": nonce_status_required,
            "nonce_status_valid": nonce_status_valid,
            "nonce_request_binding_exact": nonce_request_binding_exact,
            "nonce_authority_allowed": nonce_authority_allowed,
            "nonce_status_fresh": nonce_status_fresh,
            "nonce_unused": nonce_unused,
            "nonce_not_revoked": nonce_not_revoked,
            "authorization_not_expired": authorization_not_expired,
            "single_use_scope_exact": single_use_scope_exact,
            "authorization_granted": authorization_granted,
            "execution_performed": False,
            "live_git_command_invoked": False,
            "reference_mutated": False,
            "nonce_consumed": False,
        },
        evidence_digests={
            "authorization_request": request.request_digest,
            "authorization_policy": policy.policy_digest,
            **(
                {"nonce_status": nonce_status.receipt_digest}
                if nonce_status is not None
                else {}
            ),
        },
        certificate_digest="",
    )
    return replace(
        certificate,
        certificate_digest=(
            repository_checkpoint_cas_single_use_authorization_certificate_digest(
                certificate
            )
        ),
    )


def derive_repository_checkpoint_cas_single_use_authorization(
    authorization_id: str,
    request: RepositoryCheckpointCasAuthorizationRequest,
    policy: RepositoryCheckpointCasAuthorizationPolicy,
    nonce_status: RepositoryCheckpointCasAuthorizationNonceStatusReceipt | None,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryCheckpointCasSingleUseAuthorizationCertificate:
    certificate = construct_repository_checkpoint_cas_single_use_authorization(
        authorization_id,
        request,
        policy,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_checkpoint_cas_single_use_authorization_issues(
        certificate,
        request,
        policy,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"checkpoint_cas_single_use_authorization_invalid:{issues[0]}")
    return certificate


def repository_checkpoint_cas_single_use_authorization_issues(
    certificate: RepositoryCheckpointCasSingleUseAuthorizationCertificate,
    request: RepositoryCheckpointCasAuthorizationRequest,
    policy: RepositoryCheckpointCasAuthorizationPolicy,
    nonce_status: RepositoryCheckpointCasAuthorizationNonceStatusReceipt | None,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    expected = construct_repository_checkpoint_cas_single_use_authorization(
        certificate.authorization_id,
        request,
        policy,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues: list[str] = []
    if certificate.to_dict() != expected.to_dict():
        issues.append("checkpoint_cas_single_use_authorization_recomputation_mismatch")
    if certificate.status not in (
        AUTHORIZATION_GRANTED,
        AUTHORIZATION_DENIED,
        AUTHORIZATION_REJECTED,
    ):
        issues.append("checkpoint_cas_single_use_authorization_status_invalid")
    if certificate.authorization_granted != (
        certificate.status == AUTHORIZATION_GRANTED
    ):
        issues.append("checkpoint_cas_single_use_authorization_grant_mismatch")
    if any(
        (
            certificate.execution_performed,
            certificate.live_git_command_invoked,
            certificate.reference_mutated,
            certificate.nonce_consumed,
        )
    ):
        issues.append("checkpoint_cas_single_use_authorization_forbidden_claim")
    if certificate.certificate_digest != (
        repository_checkpoint_cas_single_use_authorization_certificate_digest(
            certificate
        )
    ):
        issues.append("checkpoint_cas_single_use_authorization_digest_mismatch")
    return tuple(issues)
