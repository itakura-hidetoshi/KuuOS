#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_cas_authorization_decision_types_v1_15 import (
    DECISION_DENIED,
    DECISION_GRANTED,
    DECISION_REJECTED,
    EXTERNAL_DENY,
    EXTERNAL_GRANT,
    REASON_INVALID_DECISION,
    REASON_VALID_DENIAL,
    REASON_VALID_GRANT,
    RepositoryCheckpointCasAuthorizationDecisionCertificate,
    RepositoryCheckpointCasAuthorizationDecisionPolicy,
    RepositoryCheckpointCasAuthorizationNonceStatusReceipt,
    RepositoryCheckpointCasExternalAuthorizationDecisionReceipt,
    repository_checkpoint_cas_authorization_decision_certificate_digest,
    repository_checkpoint_cas_authorization_decision_policy_digest,
    repository_checkpoint_cas_authorization_nonce_status_receipt_digest,
    repository_checkpoint_cas_external_authorization_decision_receipt_digest,
)
from runtime.kuuos_repository_checkpoint_cas_authorization_request_types_v1_14 import (
    REQUEST_DENIED,
    REQUEST_READY,
    RepositoryCheckpointCasAuthorizationRequest,
    RepositoryCheckpointCasAuthorizationRequestPolicy,
)
from runtime.kuuos_repository_checkpoint_cas_authorization_request_v1_14 import (
    repository_checkpoint_cas_authorization_request_issues,
    repository_checkpoint_cas_authorization_request_policy_issues,
)
from runtime.kuuos_repository_checkpoint_cas_coherence_types_v1_13 import (
    RepositoryCheckpointCasCoherenceReceipt,
)


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_cas_authorization_decision_policy(
    policy_id: str,
    *,
    authorized_decision_authority_ids: tuple[str, ...],
    authorized_nonce_authority_ids: tuple[str, ...],
    max_decision_lifetime_seconds: int,
    max_nonce_status_age_seconds: int,
) -> RepositoryCheckpointCasAuthorizationDecisionPolicy:
    policy = RepositoryCheckpointCasAuthorizationDecisionPolicy(
        policy_id=policy_id,
        authorized_decision_authority_ids=_canonical(
            authorized_decision_authority_ids
        ),
        authorized_nonce_authority_ids=_canonical(authorized_nonce_authority_ids),
        max_decision_lifetime_seconds=max_decision_lifetime_seconds,
        max_nonce_status_age_seconds=max_nonce_status_age_seconds,
        require_ready_v114_request_for_grant=True,
        require_external_signature_verification=True,
        require_nonce_unused=True,
        require_nonce_not_revoked=True,
        decision_only=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_cas_authorization_decision_policy_digest(
            policy
        ),
    )
    issues = repository_checkpoint_cas_authorization_decision_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_cas_authorization_decision_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_cas_authorization_decision_policy_issues(
    policy: RepositoryCheckpointCasAuthorizationDecisionPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_cas_authorization_decision_policy_id_missing")
    for values, name in (
        (
            policy.authorized_decision_authority_ids,
            "checkpoint_cas_authorization_decision_authorities",
        ),
        (
            policy.authorized_nonce_authority_ids,
            "checkpoint_cas_authorization_nonce_authorities",
        ),
    ):
        if values != _canonical(values):
            issues.append(f"{name}_not_canonical")
        if not values or any(not value for value in values):
            issues.append(f"{name}_empty")
    if policy.max_decision_lifetime_seconds <= 0:
        issues.append("checkpoint_cas_authorization_decision_lifetime_invalid")
    if policy.max_nonce_status_age_seconds <= 0:
        issues.append("checkpoint_cas_authorization_nonce_status_age_invalid")
    if not all(
        (
            policy.require_ready_v114_request_for_grant,
            policy.require_external_signature_verification,
            policy.require_nonce_unused,
            policy.require_nonce_not_revoked,
            policy.decision_only,
        )
    ):
        issues.append("checkpoint_cas_authorization_decision_guard_disabled")
    if policy.policy_digest != (
        repository_checkpoint_cas_authorization_decision_policy_digest(policy)
    ):
        issues.append("checkpoint_cas_authorization_decision_policy_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_cas_external_authorization_decision_receipt(
    decision_id: str,
    request: RepositoryCheckpointCasAuthorizationRequest,
    *,
    authority_id: str,
    decision: str,
    issued_at_epoch_seconds: int,
    expires_at_epoch_seconds: int,
    signature_verification_receipt_digest: str,
    revocation_status_receipt_digest: str,
    signature_valid: bool,
    authority_identity_verified: bool,
    decision_not_revoked: bool,
) -> RepositoryCheckpointCasExternalAuthorizationDecisionReceipt:
    receipt = RepositoryCheckpointCasExternalAuthorizationDecisionReceipt(
        decision_id=decision_id,
        request_digest=request.request_digest,
        request_policy_digest=request.request_policy_digest,
        coherence_digest=request.coherence_digest,
        authorization_nonce=request.authorization_nonce,
        authority_id=authority_id,
        decision=decision,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        expires_at_epoch_seconds=expires_at_epoch_seconds,
        signature_verification_receipt_digest=(
            signature_verification_receipt_digest
        ),
        revocation_status_receipt_digest=revocation_status_receipt_digest,
        signature_valid=signature_valid,
        authority_identity_verified=authority_identity_verified,
        decision_not_revoked=decision_not_revoked,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=(
            repository_checkpoint_cas_external_authorization_decision_receipt_digest(
                receipt
            )
        ),
    )
    issues = repository_checkpoint_cas_external_authorization_decision_receipt_issues(
        receipt
    )
    if issues:
        raise ValueError(f"checkpoint_cas_external_decision_receipt_invalid:{issues[0]}")
    return receipt


def repository_checkpoint_cas_external_authorization_decision_receipt_issues(
    receipt: RepositoryCheckpointCasExternalAuthorizationDecisionReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        receipt.decision_id,
        receipt.request_digest,
        receipt.request_policy_digest,
        receipt.coherence_digest,
        receipt.authorization_nonce,
        receipt.authority_id,
        receipt.signature_verification_receipt_digest,
        receipt.revocation_status_receipt_digest,
    )
    if any(not value for value in required):
        issues.append("checkpoint_cas_external_decision_required_field_missing")
    if receipt.decision not in (EXTERNAL_GRANT, EXTERNAL_DENY):
        issues.append("checkpoint_cas_external_decision_status_invalid")
    if receipt.issued_at_epoch_seconds < 0:
        issues.append("checkpoint_cas_external_decision_issued_at_negative")
    if receipt.expires_at_epoch_seconds <= receipt.issued_at_epoch_seconds:
        issues.append("checkpoint_cas_external_decision_expiry_invalid")
    if receipt.receipt_digest != (
        repository_checkpoint_cas_external_authorization_decision_receipt_digest(
            receipt
        )
    ):
        issues.append("checkpoint_cas_external_decision_receipt_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_cas_authorization_nonce_status_receipt(
    status_id: str,
    request: RepositoryCheckpointCasAuthorizationRequest,
    *,
    authority_id: str,
    checked_at_epoch_seconds: int,
    registry_snapshot_digest: str,
    consumed: bool,
    revoked: bool,
) -> RepositoryCheckpointCasAuthorizationNonceStatusReceipt:
    receipt = RepositoryCheckpointCasAuthorizationNonceStatusReceipt(
        status_id=status_id,
        authorization_nonce=request.authorization_nonce,
        request_digest=request.request_digest,
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
            receipt.request_digest,
            receipt.authority_id,
            receipt.registry_snapshot_digest,
        )
    ):
        issues.append("checkpoint_cas_nonce_status_required_field_missing")
    if receipt.checked_at_epoch_seconds < 0:
        issues.append("checkpoint_cas_nonce_status_checked_at_negative")
    if receipt.receipt_digest != (
        repository_checkpoint_cas_authorization_nonce_status_receipt_digest(receipt)
    ):
        issues.append("checkpoint_cas_nonce_status_receipt_digest_mismatch")
    return tuple(issues)


def repository_checkpoint_cas_authorization_request_valid_for_decision(
    request: RepositoryCheckpointCasAuthorizationRequest,
    coherence_receipt: RepositoryCheckpointCasCoherenceReceipt,
    request_policy: RepositoryCheckpointCasAuthorizationRequestPolicy,
) -> bool:
    try:
        issues = repository_checkpoint_cas_authorization_request_issues(
            request,
            coherence_receipt,
            request_policy,
            requester_id=request.requester_id,
            authorization_nonce=request.authorization_nonce,
            issued_at_epoch_seconds=request.issued_at_epoch_seconds,
            expires_at_epoch_seconds=request.expires_at_epoch_seconds,
        )
    except (AttributeError, TypeError, ValueError):
        return False
    return bool(
        not issues
        and request.status in (REQUEST_READY, REQUEST_DENIED)
        and not request.authorization_granted
        and not request.execution_performed
        and not request.live_git_command_invoked
        and not request.reference_mutated
    )


def construct_repository_checkpoint_cas_authorization_decision_certificate(
    authorization_id: str,
    request: RepositoryCheckpointCasAuthorizationRequest,
    coherence_receipt: RepositoryCheckpointCasCoherenceReceipt,
    request_policy: RepositoryCheckpointCasAuthorizationRequestPolicy,
    decision_policy: RepositoryCheckpointCasAuthorizationDecisionPolicy,
    external_decision: RepositoryCheckpointCasExternalAuthorizationDecisionReceipt,
    nonce_status: RepositoryCheckpointCasAuthorizationNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryCheckpointCasAuthorizationDecisionCertificate:
    request_policy_valid = not repository_checkpoint_cas_authorization_request_policy_issues(
        request_policy
    )
    request_valid = repository_checkpoint_cas_authorization_request_valid_for_decision(
        request,
        coherence_receipt,
        request_policy,
    )
    request_ready = request.status == REQUEST_READY
    request_binding_exact = bool(
        request_policy_valid
        and request.coherence_digest == coherence_receipt.coherence_digest
        and request.request_policy_digest == request_policy.policy_digest
        and request.evidence_digests.get("checkpoint_cas_coherence")
        == coherence_receipt.coherence_digest
        and request.evidence_digests.get("authorization_request_policy")
        == request_policy.policy_digest
    )
    decision_policy_valid = not repository_checkpoint_cas_authorization_decision_policy_issues(
        decision_policy
    )
    external_decision_valid = not (
        repository_checkpoint_cas_external_authorization_decision_receipt_issues(
            external_decision
        )
    )
    decision_binding_exact = bool(
        external_decision.request_digest == request.request_digest
        and external_decision.request_policy_digest == request.request_policy_digest
        and external_decision.coherence_digest == request.coherence_digest
        and external_decision.authorization_nonce == request.authorization_nonce
    )
    decision_authority_authorized = (
        external_decision.authority_id
        in decision_policy.authorized_decision_authority_ids
    )
    signature_verification_valid = bool(external_decision.signature_valid)
    authority_identity_verified = bool(external_decision.authority_identity_verified)
    decision_not_revoked = bool(external_decision.decision_not_revoked)
    decision_lifetime = (
        external_decision.expires_at_epoch_seconds
        - external_decision.issued_at_epoch_seconds
    )
    decision_lifetime_within_policy = bool(
        decision_lifetime > 0
        and decision_lifetime <= decision_policy.max_decision_lifetime_seconds
    )
    decision_within_request_lifetime = bool(
        external_decision.issued_at_epoch_seconds >= request.issued_at_epoch_seconds
        and external_decision.expires_at_epoch_seconds
        <= request.expires_at_epoch_seconds
    )
    authorization_not_expired = bool(
        evaluated_at_epoch_seconds >= external_decision.issued_at_epoch_seconds
        and evaluated_at_epoch_seconds < external_decision.expires_at_epoch_seconds
        and evaluated_at_epoch_seconds < request.expires_at_epoch_seconds
    )
    nonce_status_valid = not (
        repository_checkpoint_cas_authorization_nonce_status_receipt_issues(
            nonce_status
        )
    )
    nonce_scope_bound = bool(
        nonce_status.authorization_nonce == request.authorization_nonce
        and nonce_status.request_digest == request.request_digest
    )
    nonce_authority_authorized = (
        nonce_status.authority_id
        in decision_policy.authorized_nonce_authority_ids
    )
    nonce_age = evaluated_at_epoch_seconds - nonce_status.checked_at_epoch_seconds
    nonce_status_fresh = bool(
        nonce_age >= 0
        and nonce_age <= decision_policy.max_nonce_status_age_seconds
    )
    nonce_unused = not nonce_status.consumed
    nonce_not_revoked = not nonce_status.revoked
    no_future_evidence = bool(
        evaluated_at_epoch_seconds >= 0
        and external_decision.issued_at_epoch_seconds <= evaluated_at_epoch_seconds
        and nonce_status.checked_at_epoch_seconds <= evaluated_at_epoch_seconds
    )
    external_grant = external_decision.decision == EXTERNAL_GRANT

    common_valid = all(
        (
            bool(authorization_id),
            request_valid,
            request_binding_exact,
            decision_policy_valid,
            external_decision_valid,
            decision_binding_exact,
            decision_authority_authorized,
            signature_verification_valid,
            authority_identity_verified,
            decision_not_revoked,
            decision_lifetime_within_policy,
            decision_within_request_lifetime,
            authorization_not_expired,
            nonce_status_valid,
            nonce_scope_bound,
            nonce_authority_authorized,
            nonce_status_fresh,
            nonce_unused,
            nonce_not_revoked,
            no_future_evidence,
        )
    )

    if common_valid and request_ready and external_grant:
        status = DECISION_GRANTED
        reason = REASON_VALID_GRANT
    elif common_valid and external_decision.decision == EXTERNAL_DENY:
        status = DECISION_DENIED
        reason = REASON_VALID_DENIAL
    else:
        status = DECISION_REJECTED
        reason = REASON_INVALID_DECISION

    accepted = status in (DECISION_GRANTED, DECISION_DENIED)
    granted = status == DECISION_GRANTED
    checks = {
        "request_valid": request_valid,
        "request_ready": request_ready,
        "request_binding_exact": request_binding_exact,
        "decision_policy_valid": decision_policy_valid,
        "external_decision_receipt_valid": external_decision_valid,
        "decision_binding_exact": decision_binding_exact,
        "decision_authority_authorized": decision_authority_authorized,
        "signature_verification_valid": signature_verification_valid,
        "authority_identity_verified": authority_identity_verified,
        "decision_not_revoked": decision_not_revoked,
        "decision_lifetime_within_policy": decision_lifetime_within_policy,
        "decision_within_request_lifetime": decision_within_request_lifetime,
        "authorization_not_expired": authorization_not_expired,
        "nonce_status_receipt_valid": nonce_status_valid,
        "nonce_scope_bound": nonce_scope_bound,
        "nonce_authority_authorized": nonce_authority_authorized,
        "nonce_status_fresh": nonce_status_fresh,
        "nonce_unused": nonce_unused,
        "nonce_not_revoked": nonce_not_revoked,
        "no_future_evidence": no_future_evidence,
        "external_grant": external_grant,
        "external_decision_accepted": accepted,
        "authorization_granted": granted,
        "single_use_cas_eligible": granted,
        "nonce_consumed": False,
        "execution_performed": False,
        "live_git_command_invoked": False,
        "reference_mutated": False,
    }
    certificate = RepositoryCheckpointCasAuthorizationDecisionCertificate(
        authorization_id=authorization_id,
        status=status,
        reason=reason,
        request_digest=request.request_digest,
        request_policy_digest=request.request_policy_digest,
        coherence_digest=request.coherence_digest,
        decision_policy_digest=decision_policy.policy_digest,
        external_decision_receipt_digest=external_decision.receipt_digest,
        nonce_status_receipt_digest=nonce_status.receipt_digest,
        requester_id=request.requester_id,
        decision_authority_id=external_decision.authority_id,
        nonce_authority_id=nonce_status.authority_id,
        authorization_nonce=request.authorization_nonce,
        repository_id=request.repository_id,
        git_dir_fingerprint=request.git_dir_fingerprint,
        checkpoint_reference=request.checkpoint_reference,
        expected_current_oid=request.expected_current_oid,
        observed_current_oid=request.observed_current_oid,
        proposed_checkpoint_oid=request.proposed_checkpoint_oid,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        request_valid=request_valid,
        request_ready=request_ready,
        request_binding_exact=request_binding_exact,
        decision_policy_valid=decision_policy_valid,
        external_decision_receipt_valid=external_decision_valid,
        decision_binding_exact=decision_binding_exact,
        decision_authority_authorized=decision_authority_authorized,
        signature_verification_valid=signature_verification_valid,
        authority_identity_verified=authority_identity_verified,
        decision_not_revoked=decision_not_revoked,
        decision_lifetime_within_policy=decision_lifetime_within_policy,
        decision_within_request_lifetime=decision_within_request_lifetime,
        authorization_not_expired=authorization_not_expired,
        nonce_status_receipt_valid=nonce_status_valid,
        nonce_scope_bound=nonce_scope_bound,
        nonce_authority_authorized=nonce_authority_authorized,
        nonce_status_fresh=nonce_status_fresh,
        nonce_unused=nonce_unused,
        nonce_not_revoked=nonce_not_revoked,
        no_future_evidence=no_future_evidence,
        external_grant=external_grant,
        external_decision_accepted=accepted,
        authorization_granted=granted,
        single_use_cas_eligible=granted,
        nonce_consumed=False,
        execution_performed=False,
        live_git_command_invoked=False,
        reference_mutated=False,
        checks=checks,
        evidence_digests={
            "checkpoint_cas_authorization_request": request.request_digest,
            "checkpoint_cas_authorization_request_policy": request_policy.policy_digest,
            "checkpoint_cas_coherence": coherence_receipt.coherence_digest,
            "checkpoint_cas_authorization_decision_policy": decision_policy.policy_digest,
            "external_authorization_decision": external_decision.receipt_digest,
            "authorization_nonce_status": nonce_status.receipt_digest,
        },
        certificate_digest="",
    )
    return replace(
        certificate,
        certificate_digest=(
            repository_checkpoint_cas_authorization_decision_certificate_digest(
                certificate
            )
        ),
    )


def derive_repository_checkpoint_cas_authorization_decision_certificate(
    authorization_id: str,
    request: RepositoryCheckpointCasAuthorizationRequest,
    coherence_receipt: RepositoryCheckpointCasCoherenceReceipt,
    request_policy: RepositoryCheckpointCasAuthorizationRequestPolicy,
    decision_policy: RepositoryCheckpointCasAuthorizationDecisionPolicy,
    external_decision: RepositoryCheckpointCasExternalAuthorizationDecisionReceipt,
    nonce_status: RepositoryCheckpointCasAuthorizationNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryCheckpointCasAuthorizationDecisionCertificate:
    certificate = construct_repository_checkpoint_cas_authorization_decision_certificate(
        authorization_id,
        request,
        coherence_receipt,
        request_policy,
        decision_policy,
        external_decision,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_checkpoint_cas_authorization_decision_certificate_issues(
        certificate,
        request,
        coherence_receipt,
        request_policy,
        decision_policy,
        external_decision,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"checkpoint_cas_authorization_decision_invalid:{issues[0]}")
    return certificate


def repository_checkpoint_cas_authorization_decision_certificate_issues(
    certificate: RepositoryCheckpointCasAuthorizationDecisionCertificate,
    request: RepositoryCheckpointCasAuthorizationRequest,
    coherence_receipt: RepositoryCheckpointCasCoherenceReceipt,
    request_policy: RepositoryCheckpointCasAuthorizationRequestPolicy,
    decision_policy: RepositoryCheckpointCasAuthorizationDecisionPolicy,
    external_decision: RepositoryCheckpointCasExternalAuthorizationDecisionReceipt,
    nonce_status: RepositoryCheckpointCasAuthorizationNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    expected = construct_repository_checkpoint_cas_authorization_decision_certificate(
        certificate.authorization_id,
        request,
        coherence_receipt,
        request_policy,
        decision_policy,
        external_decision,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues: list[str] = []
    if certificate.to_dict() != expected.to_dict():
        issues.append("checkpoint_cas_authorization_decision_recomputation_mismatch")
    if certificate.status not in (
        DECISION_GRANTED,
        DECISION_DENIED,
        DECISION_REJECTED,
    ):
        issues.append("checkpoint_cas_authorization_decision_status_invalid")
    granted = certificate.status == DECISION_GRANTED
    accepted = certificate.status in (DECISION_GRANTED, DECISION_DENIED)
    if certificate.authorization_granted != granted:
        issues.append("checkpoint_cas_authorization_decision_grant_mismatch")
    if certificate.single_use_cas_eligible != granted:
        issues.append("checkpoint_cas_authorization_decision_eligibility_mismatch")
    if certificate.external_decision_accepted != accepted:
        issues.append("checkpoint_cas_authorization_decision_acceptance_mismatch")
    if any(
        (
            certificate.nonce_consumed,
            certificate.execution_performed,
            certificate.live_git_command_invoked,
            certificate.reference_mutated,
        )
    ):
        issues.append("checkpoint_cas_authorization_decision_forbidden_operation")
    if certificate.certificate_digest != (
        repository_checkpoint_cas_authorization_decision_certificate_digest(
            certificate
        )
    ):
        issues.append("checkpoint_cas_authorization_decision_digest_mismatch")
    return tuple(issues)
