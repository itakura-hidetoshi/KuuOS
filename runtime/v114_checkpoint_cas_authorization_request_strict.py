#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re

from runtime.kuuos_repository_checkpoint_cas_authorization_request_types_v1_14 import (
    REASON_INVALID_REQUEST,
    REQUEST_READY,
    REQUEST_REJECTED,
    RepositoryCheckpointCasAuthorizationRequest,
    RepositoryCheckpointCasAuthorizationRequestPolicy,
    repository_checkpoint_cas_authorization_request_digest,
)
from runtime.kuuos_repository_checkpoint_cas_coherence_types_v1_13 import (
    COHERENCE_CONFLICT,
    COHERENCE_READY,
    RepositoryCheckpointCasCoherenceReceipt,
)
from runtime.v114_checkpoint_cas_authorization_request_core import (
    build_repository_checkpoint_cas_authorization_request_policy,
    construct_repository_checkpoint_cas_authorization_request as _construct,
    repository_checkpoint_cas_authorization_request_policy_issues,
    repository_checkpoint_cas_coherence_receipt_valid_for_request as _base_receipt_valid,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_ZERO_OID = "0" * 40


def repository_checkpoint_cas_coherence_receipt_valid_for_request(
    receipt: RepositoryCheckpointCasCoherenceReceipt,
) -> bool:
    if not _base_receipt_valid(receipt):
        return False
    oids = (
        receipt.expected_current_oid,
        receipt.observed_current_oid,
        receipt.proposed_checkpoint_oid,
    )
    if any(not _HEX40.fullmatch(oid) or oid == _ZERO_OID for oid in oids):
        return False
    if receipt.expected_current_oid == receipt.proposed_checkpoint_oid:
        return False
    if receipt.status == COHERENCE_READY:
        return bool(
            receipt.compare_and_swap_required
            and receipt.observed_current_oid == receipt.expected_current_oid
        )
    if receipt.status == COHERENCE_CONFLICT:
        return bool(
            not receipt.compare_and_swap_required
            and receipt.observed_current_oid != receipt.expected_current_oid
        )
    return False


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
    request = _construct(
        request_id,
        coherence_receipt,
        policy,
        requester_id=requester_id,
        authorization_nonce=authorization_nonce,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        expires_at_epoch_seconds=expires_at_epoch_seconds,
    )
    strict_valid = repository_checkpoint_cas_coherence_receipt_valid_for_request(
        coherence_receipt
    )
    if strict_valid:
        return request

    checks = dict(request.checks)
    checks["coherence_receipt_valid"] = False
    checks["single_use_authorization_required"] = False
    rejected = replace(
        request,
        status=REQUEST_REJECTED,
        reason=REASON_INVALID_REQUEST,
        coherence_receipt_valid=False,
        single_use_authorization_required=False,
        checks=checks,
        request_digest="",
    )
    return replace(
        rejected,
        request_digest=repository_checkpoint_cas_authorization_request_digest(rejected),
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
    if request.single_use_authorization_required != (request.status == REQUEST_READY):
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


__all__ = [
    "build_repository_checkpoint_cas_authorization_request_policy",
    "repository_checkpoint_cas_authorization_request_policy_issues",
    "repository_checkpoint_cas_coherence_receipt_valid_for_request",
    "construct_repository_checkpoint_cas_authorization_request",
    "derive_repository_checkpoint_cas_authorization_request",
    "repository_checkpoint_cas_authorization_request_issues",
]
