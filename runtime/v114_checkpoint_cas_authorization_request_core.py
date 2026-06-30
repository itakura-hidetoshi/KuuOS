#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_cas_authorization_request_types_v1_14 import (
    REASON_COHERENT_CONFLICT,
    REASON_COHERENT_READY,
    REASON_INVALID_REQUEST,
    REQUEST_DENIED,
    REQUEST_READY,
    REQUEST_REJECTED,
    RepositoryCheckpointCasAuthorizationRequest,
    RepositoryCheckpointCasAuthorizationRequestPolicy,
    repository_checkpoint_cas_authorization_request_digest,
    repository_checkpoint_cas_authorization_request_policy_digest,
)
from runtime.kuuos_repository_checkpoint_cas_coherence_types_v1_13 import (
    COHERENCE_CONFLICT,
    COHERENCE_READY,
    REASON_COHERENT_CONFLICT as COHERENCE_REASON_CONFLICT,
    REASON_COHERENT_READY as COHERENCE_REASON_READY,
    RepositoryCheckpointCasCoherenceReceipt,
    repository_checkpoint_cas_coherence_digest,
)


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_cas_authorization_request_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    allowed_checkpoint_references: tuple[str, ...],
    max_request_lifetime_seconds: int,
) -> RepositoryCheckpointCasAuthorizationRequestPolicy:
    policy = RepositoryCheckpointCasAuthorizationRequestPolicy(
        policy_id=policy_id,
        allowed_repository_ids=_canonical(allowed_repository_ids),
        allowed_checkpoint_references=_canonical(allowed_checkpoint_references),
        max_request_lifetime_seconds=max_request_lifetime_seconds,
        require_coherent_v113_receipt=True,
        require_ready_status_for_request=True,
        require_single_use_authorization=True,
        request_only=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_cas_authorization_request_policy_digest(
            policy
        ),
    )
    issues = repository_checkpoint_cas_authorization_request_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_cas_authorization_request_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_cas_authorization_request_policy_issues(
    policy: RepositoryCheckpointCasAuthorizationRequestPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_cas_authorization_request_policy_id_missing")
    if policy.allowed_repository_ids != _canonical(policy.allowed_repository_ids):
        issues.append("checkpoint_cas_authorization_request_repository_ids_not_canonical")
    if not policy.allowed_repository_ids or any(
        not value for value in policy.allowed_repository_ids
    ):
        issues.append("checkpoint_cas_authorization_request_repository_ids_empty")
    if policy.allowed_checkpoint_references != _canonical(
        policy.allowed_checkpoint_references
    ):
        issues.append("checkpoint_cas_authorization_request_references_not_canonical")
    if not policy.allowed_checkpoint_references or any(
        not value for value in policy.allowed_checkpoint_references
    ):
        issues.append("checkpoint_cas_authorization_request_references_empty")
    if policy.max_request_lifetime_seconds <= 0:
        issues.append("checkpoint_cas_authorization_request_lifetime_invalid")
    if not all(
        (
            policy.require_coherent_v113_receipt,
            policy.require_ready_status_for_request,
            policy.require_single_use_authorization,
            policy.request_only,
        )
    ):
        issues.append("checkpoint_cas_authorization_request_guard_disabled")
    if policy.policy_digest != (
        repository_checkpoint_cas_authorization_request_policy_digest(policy)
    ):
        issues.append("checkpoint_cas_authorization_request_policy_digest_mismatch")
    return tuple(issues)


def repository_checkpoint_cas_coherence_receipt_valid_for_request(
    receipt: RepositoryCheckpointCasCoherenceReceipt,
) -> bool:
    digest_valid = receipt.coherence_digest == repository_checkpoint_cas_coherence_digest(
        receipt
    )
    evidence_exact = bool(
        receipt.evidence_digests.get("checkpoint_cas_contract")
        == receipt.contract_digest
        and receipt.evidence_digests.get("validated_cas_intake")
        == receipt.intake_digest
    )
    common = all(
        (
            digest_valid,
            receipt.status in (COHERENCE_READY, COHERENCE_CONFLICT),
            bool(receipt.receipt_id),
            bool(receipt.contract_digest),
            bool(receipt.intake_digest),
            bool(receipt.candidate_digest),
            bool(receipt.repository_id),
            bool(receipt.git_dir_fingerprint),
            bool(receipt.checkpoint_reference),
            receipt.contract_digest_valid,
            receipt.contract_local_coherence,
            receipt.intake_digest_valid,
            receipt.intake_local_coherence,
            receipt.exact_contract_intake_binding,
            not receipt.repository_change_authority_granted,
            not receipt.execution_performed,
            not receipt.live_git_command_invoked,
            evidence_exact,
            receipt.checks.get("contract_digest_valid")
            == receipt.contract_digest_valid,
            receipt.checks.get("contract_local_coherence")
            == receipt.contract_local_coherence,
            receipt.checks.get("intake_digest_valid") == receipt.intake_digest_valid,
            receipt.checks.get("intake_local_coherence")
            == receipt.intake_local_coherence,
            receipt.checks.get("exact_contract_intake_binding")
            == receipt.exact_contract_intake_binding,
            receipt.checks.get("compare_and_swap_required")
            == receipt.compare_and_swap_required,
            receipt.checks.get("repository_change_authority_granted")
            == receipt.repository_change_authority_granted,
            receipt.checks.get("execution_performed")
            == receipt.execution_performed,
            receipt.checks.get("live_git_command_invoked")
            == receipt.live_git_command_invoked,
        )
    )
    if not common:
        return False
    if receipt.status == COHERENCE_READY:
        return bool(
            receipt.reason == COHERENCE_REASON_READY
            and receipt.compare_and_swap_required
        )
    return bool(
        receipt.reason == COHERENCE_REASON_CONFLICT
        and not receipt.compare_and_swap_required
    )


def construct_repository_checkpoint_cas_authorization_request(
    request_id: str,
    coherence_receipt: RepositoryCheckpointCasCoherenceReceipt,
    policy: RepositoryCheckpointCasAuthorizationRequestPolicy,
    *,
    requester_id: str,
    authorization_nonce: str,
    issued_at_epoch_seconds: int,
    expires_at_epoch_seconds: int,
) -> RepositoryCheckpointCasAuthorizationRequest:
    policy_valid = not repository_checkpoint_cas_authorization_request_policy_issues(
        policy
    )
    coherence_valid = repository_checkpoint_cas_coherence_receipt_valid_for_request(
        coherence_receipt
    )
    repository_allowed = coherence_receipt.repository_id in policy.allowed_repository_ids
    reference_allowed = (
        coherence_receipt.checkpoint_reference in policy.allowed_checkpoint_references
    )
    lifetime = expires_at_epoch_seconds - issued_at_epoch_seconds
    lifetime_within_policy = bool(
        issued_at_epoch_seconds >= 0
        and lifetime > 0
        and lifetime <= policy.max_request_lifetime_seconds
    )
    request_not_expired_at_issue = expires_at_epoch_seconds > issued_at_epoch_seconds
    nonce_present = bool(authorization_nonce)
    common_valid = all(
        (
            bool(request_id),
            bool(requester_id),
            policy_valid,
            coherence_valid,
            repository_allowed,
            reference_allowed,
            lifetime_within_policy,
            request_not_expired_at_issue,
            nonce_present,
        )
    )

    if common_valid and coherence_receipt.status == COHERENCE_READY:
        status = REQUEST_READY
        reason = REASON_COHERENT_READY
    elif common_valid and coherence_receipt.status == COHERENCE_CONFLICT:
        status = REQUEST_DENIED
        reason = REASON_COHERENT_CONFLICT
    else:
        status = REQUEST_REJECTED
        reason = REASON_INVALID_REQUEST

    single_use_required = status == REQUEST_READY
    request = RepositoryCheckpointCasAuthorizationRequest(
        request_id=request_id,
        status=status,
        reason=reason,
        coherence_digest=coherence_receipt.coherence_digest,
        request_policy_digest=policy.policy_digest,
        requester_id=requester_id,
        authorization_nonce=authorization_nonce,
        repository_id=coherence_receipt.repository_id,
        git_dir_fingerprint=coherence_receipt.git_dir_fingerprint,
        checkpoint_reference=coherence_receipt.checkpoint_reference,
        expected_current_oid=coherence_receipt.expected_current_oid,
        observed_current_oid=coherence_receipt.observed_current_oid,
        proposed_checkpoint_oid=coherence_receipt.proposed_checkpoint_oid,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        expires_at_epoch_seconds=expires_at_epoch_seconds,
        coherence_receipt_valid=coherence_valid,
        repository_allowed=repository_allowed,
        checkpoint_reference_allowed=reference_allowed,
        lifetime_within_policy=lifetime_within_policy,
        request_not_expired_at_issue=request_not_expired_at_issue,
        nonce_present=nonce_present,
        single_use_authorization_required=single_use_required,
        authorization_granted=False,
        execution_performed=False,
        live_git_command_invoked=False,
        reference_mutated=False,
        checks={
            "policy_valid": policy_valid,
            "coherence_receipt_valid": coherence_valid,
            "repository_allowed": repository_allowed,
            "checkpoint_reference_allowed": reference_allowed,
            "lifetime_within_policy": lifetime_within_policy,
            "request_not_expired_at_issue": request_not_expired_at_issue,
            "nonce_present": nonce_present,
            "single_use_authorization_required": single_use_required,
            "authorization_granted": False,
            "execution_performed": False,
            "live_git_command_invoked": False,
            "reference_mutated": False,
        },
        evidence_digests={
            "checkpoint_cas_coherence": coherence_receipt.coherence_digest,
            "authorization_request_policy": policy.policy_digest,
        },
        request_digest="",
    )
    return replace(
        request,
        request_digest=repository_checkpoint_cas_authorization_request_digest(request),
    )


def derive_repository_checkpoint_cas_authorization_request(
    request_id: str,
    coherence_receipt: RepositoryCheckpointCasCoherenceReceipt,
    policy: RepositoryCheckpointCasAuthorizationRequestPolicy,
    *,
    requester_id: str,
    authorization_nonce: str,
    issued_at_epoch_seconds: int,
    expires_at_epoch_seconds: int,
) -> RepositoryCheckpointCasAuthorizationRequest:
    request = construct_repository_checkpoint_cas_authorization_request(
        request_id,
        coherence_receipt,
        policy,
        requester_id=requester_id,
        authorization_nonce=authorization_nonce,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        expires_at_epoch_seconds=expires_at_epoch_seconds,
    )
    issues = repository_checkpoint_cas_authorization_request_issues(
        request,
        coherence_receipt,
        policy,
        requester_id=requester_id,
        authorization_nonce=authorization_nonce,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        expires_at_epoch_seconds=expires_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"checkpoint_cas_authorization_request_invalid:{issues[0]}")
    return request


def repository_checkpoint_cas_authorization_request_issues(
    request: RepositoryCheckpointCasAuthorizationRequest,
    coherence_receipt: RepositoryCheckpointCasCoherenceReceipt,
    policy: RepositoryCheckpointCasAuthorizationRequestPolicy,
    *,
    requester_id: str,
    authorization_nonce: str,
    issued_at_epoch_seconds: int,
    expires_at_epoch_seconds: int,
) -> tuple[str, ...]:
    expected = construct_repository_checkpoint_cas_authorization_request(
        request.request_id,
        coherence_receipt,
        policy,
        requester_id=requester_id,
        authorization_nonce=authorization_nonce,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        expires_at_epoch_seconds=expires_at_epoch_seconds,
    )
    issues: list[str] = []
    if request.to_dict() != expected.to_dict():
        issues.append("checkpoint_cas_authorization_request_recomputation_mismatch")
    if request.status not in (REQUEST_READY, REQUEST_DENIED, REQUEST_REJECTED):
        issues.append("checkpoint_cas_authorization_request_status_invalid")
    if request.single_use_authorization_required != (
        request.status == REQUEST_READY
    ):
        issues.append("checkpoint_cas_authorization_request_single_use_mismatch")
    if any(
        (
            request.authorization_granted,
            request.execution_performed,
            request.live_git_command_invoked,
            request.reference_mutated,
        )
    ):
        issues.append("checkpoint_cas_authorization_request_forbidden_claim")
    if request.request_digest != repository_checkpoint_cas_authorization_request_digest(
        request
    ):
        issues.append("checkpoint_cas_authorization_request_digest_mismatch")
    return tuple(issues)
