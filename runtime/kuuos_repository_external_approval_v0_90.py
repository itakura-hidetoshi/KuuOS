#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_evolution_admission_types_v0_89 import (
    ADMISSION_PROPOSED,
    RepositoryEvolutionAdmissionCertificate,
)
from runtime.kuuos_repository_evolution_admission_v0_89 import (
    repository_evolution_admission_certificate_issues,
)
from runtime.kuuos_repository_external_approval_types_v0_90 import (
    APPROVAL_ACCEPTED,
    APPROVAL_REJECTED,
    DECISION_APPROVE,
    DECISION_REJECT,
    RepositoryApprovalRevocationStatusReceipt,
    RepositoryEvolutionExternalApprovalCertificate,
    RepositoryExternalApprovalAttestation,
    RepositoryExternalApprovalPolicy,
    RepositorySignatureVerificationReceipt,
    repository_approval_revocation_status_receipt_digest,
    repository_approver_key_binding_digest,
    repository_evolution_external_approval_certificate_digest,
    repository_external_approval_attestation_digest,
    repository_external_approval_policy_digest,
    repository_external_approval_signed_payload_digest,
    repository_signature_verification_receipt_digest,
)


def repository_external_approval_policy_issues(
    policy: RepositoryExternalApprovalPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("policy_id_missing")
    canonical_fields = (
        (policy.authorized_approver_ids, "authorized_approver_ids"),
        (policy.authorized_verifier_ids, "authorized_verifier_ids"),
        (policy.authorized_revocation_authority_ids, "authorized_revocation_authority_ids"),
        (policy.authorized_approver_key_binding_digests, "authorized_approver_key_binding_digests"),
        (policy.allowed_signature_algorithms, "allowed_signature_algorithms"),
    )
    for values, name in canonical_fields:
        if values != tuple(sorted(set(values))):
            issues.append(f"{name}_not_canonical")
        if not values:
            issues.append(f"{name}_empty")
        if any(not value for value in values):
            issues.append(f"{name}_contains_empty")
    durations = (
        policy.max_admission_certificate_age_seconds,
        policy.max_approval_lifetime_seconds,
        policy.max_verification_age_seconds,
        policy.max_revocation_status_age_seconds,
    )
    if any(value <= 0 for value in durations):
        issues.append("policy_duration_invalid")
    if policy.policy_digest != repository_external_approval_policy_digest(policy):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def build_repository_external_approval_policy(
    policy_id: str,
    *,
    authorized_approver_ids: tuple[str, ...],
    authorized_verifier_ids: tuple[str, ...],
    authorized_revocation_authority_ids: tuple[str, ...],
    authorized_approver_key_bindings: tuple[tuple[str, str], ...],
    allowed_signature_algorithms: tuple[str, ...],
    max_admission_certificate_age_seconds: int,
    max_approval_lifetime_seconds: int,
    max_verification_age_seconds: int,
    max_revocation_status_age_seconds: int,
    require_distinct_approver_and_verifier: bool = True,
) -> RepositoryExternalApprovalPolicy:
    key_bindings = tuple(sorted(set(
        repository_approver_key_binding_digest(approver_id, signing_key_id)
        for approver_id, signing_key_id in authorized_approver_key_bindings
    )))
    policy = RepositoryExternalApprovalPolicy(
        policy_id=policy_id,
        authorized_approver_ids=tuple(sorted(set(authorized_approver_ids))),
        authorized_verifier_ids=tuple(sorted(set(authorized_verifier_ids))),
        authorized_revocation_authority_ids=tuple(sorted(set(
            authorized_revocation_authority_ids
        ))),
        authorized_approver_key_binding_digests=key_bindings,
        allowed_signature_algorithms=tuple(sorted(set(allowed_signature_algorithms))),
        max_admission_certificate_age_seconds=max_admission_certificate_age_seconds,
        max_approval_lifetime_seconds=max_approval_lifetime_seconds,
        max_verification_age_seconds=max_verification_age_seconds,
        max_revocation_status_age_seconds=max_revocation_status_age_seconds,
        require_distinct_approver_and_verifier=require_distinct_approver_and_verifier,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_external_approval_policy_digest(policy),
    )
    issues = repository_external_approval_policy_issues(policy)
    if issues:
        raise ValueError(f"external_approval_policy_invalid:{issues[0]}")
    return policy


def repository_external_approval_attestation_issues(
    attestation: RepositoryExternalApprovalAttestation,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        attestation.approval_id,
        attestation.admission_certificate_digest,
        attestation.approval_policy_digest,
        attestation.approver_id,
        attestation.signature_algorithm,
        attestation.signing_key_id,
        attestation.signed_payload_digest,
        attestation.signature_digest,
    )
    if any(not value for value in required):
        issues.append("approval_attestation_required_field_missing")
    if attestation.decision not in (DECISION_APPROVE, DECISION_REJECT):
        issues.append("approval_decision_invalid")
    if attestation.issued_at_epoch_seconds < 0:
        issues.append("approval_issued_at_negative")
    if attestation.expires_at_epoch_seconds <= attestation.issued_at_epoch_seconds:
        issues.append("approval_expiry_invalid")
    if attestation.signed_payload_digest != (
        repository_external_approval_signed_payload_digest(attestation)
    ):
        issues.append("approval_signed_payload_digest_mismatch")
    if attestation.attestation_digest != (
        repository_external_approval_attestation_digest(attestation)
    ):
        issues.append("approval_attestation_digest_mismatch")
    return tuple(issues)


def build_repository_external_approval_attestation(
    approval_id: str,
    admission_certificate: RepositoryEvolutionAdmissionCertificate,
    policy: RepositoryExternalApprovalPolicy,
    *,
    approver_id: str,
    decision: str,
    issued_at_epoch_seconds: int,
    expires_at_epoch_seconds: int,
    signature_algorithm: str,
    signing_key_id: str,
    signature_digest: str,
) -> RepositoryExternalApprovalAttestation:
    attestation = RepositoryExternalApprovalAttestation(
        approval_id=approval_id,
        admission_certificate_digest=admission_certificate.certificate_digest,
        approval_policy_digest=policy.policy_digest,
        approver_id=approver_id,
        decision=decision,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        expires_at_epoch_seconds=expires_at_epoch_seconds,
        signature_algorithm=signature_algorithm,
        signing_key_id=signing_key_id,
        signed_payload_digest="",
        signature_digest=signature_digest,
        attestation_digest="",
    )
    attestation = replace(
        attestation,
        signed_payload_digest=(
            repository_external_approval_signed_payload_digest(attestation)
        ),
    )
    attestation = replace(
        attestation,
        attestation_digest=(
            repository_external_approval_attestation_digest(attestation)
        ),
    )
    issues = repository_external_approval_attestation_issues(attestation)
    if issues:
        raise ValueError(f"external_approval_attestation_invalid:{issues[0]}")
    return attestation


def repository_signature_verification_receipt_issues(
    receipt: RepositorySignatureVerificationReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        receipt.verification_id,
        receipt.attestation_digest,
        receipt.verifier_id,
        receipt.signature_algorithm,
        receipt.signing_key_id,
        receipt.signed_payload_digest,
        receipt.signature_digest,
    )
    if any(not value for value in required):
        issues.append("signature_verification_required_field_missing")
    if receipt.verified_at_epoch_seconds < 0:
        issues.append("signature_verified_at_negative")
    if receipt.receipt_digest != repository_signature_verification_receipt_digest(receipt):
        issues.append("signature_verification_receipt_digest_mismatch")
    return tuple(issues)


def build_repository_signature_verification_receipt(
    verification_id: str,
    attestation: RepositoryExternalApprovalAttestation,
    *,
    verifier_id: str,
    verified_at_epoch_seconds: int,
    signature_verified: bool,
) -> RepositorySignatureVerificationReceipt:
    receipt = RepositorySignatureVerificationReceipt(
        verification_id=verification_id,
        attestation_digest=attestation.attestation_digest,
        verifier_id=verifier_id,
        verified_at_epoch_seconds=verified_at_epoch_seconds,
        signature_algorithm=attestation.signature_algorithm,
        signing_key_id=attestation.signing_key_id,
        signed_payload_digest=attestation.signed_payload_digest,
        signature_digest=attestation.signature_digest,
        signature_verified=signature_verified,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=repository_signature_verification_receipt_digest(receipt),
    )
    issues = repository_signature_verification_receipt_issues(receipt)
    if issues:
        raise ValueError(f"signature_verification_receipt_invalid:{issues[0]}")
    return receipt


def repository_approval_revocation_status_receipt_issues(
    receipt: RepositoryApprovalRevocationStatusReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        receipt.status_id,
        receipt.attestation_digest,
        receipt.approval_policy_digest,
        receipt.authority_id,
        receipt.registry_snapshot_digest,
    )
    if any(not value for value in required):
        issues.append("revocation_status_required_field_missing")
    if receipt.checked_at_epoch_seconds < 0:
        issues.append("revocation_checked_at_negative")
    if receipt.revoked:
        if receipt.revocation_effective_at_epoch_seconds <= 0:
            issues.append("revocation_effective_at_missing")
        if receipt.revocation_effective_at_epoch_seconds > receipt.checked_at_epoch_seconds:
            issues.append("revocation_effective_after_check")
        if not receipt.revocation_reason_digest:
            issues.append("revocation_reason_digest_missing")
    else:
        if receipt.revocation_effective_at_epoch_seconds != 0:
            issues.append("nonrevoked_effective_at_present")
        if receipt.revocation_reason_digest:
            issues.append("nonrevoked_reason_present")
    if receipt.receipt_digest != (
        repository_approval_revocation_status_receipt_digest(receipt)
    ):
        issues.append("revocation_status_receipt_digest_mismatch")
    return tuple(issues)


def build_repository_approval_revocation_status_receipt(
    status_id: str,
    attestation: RepositoryExternalApprovalAttestation,
    policy: RepositoryExternalApprovalPolicy,
    *,
    authority_id: str,
    checked_at_epoch_seconds: int,
    registry_snapshot_digest: str,
    revoked: bool,
    revocation_effective_at_epoch_seconds: int = 0,
    revocation_reason_digest: str = "",
) -> RepositoryApprovalRevocationStatusReceipt:
    receipt = RepositoryApprovalRevocationStatusReceipt(
        status_id=status_id,
        attestation_digest=attestation.attestation_digest,
        approval_policy_digest=policy.policy_digest,
        authority_id=authority_id,
        checked_at_epoch_seconds=checked_at_epoch_seconds,
        registry_snapshot_digest=registry_snapshot_digest,
        revoked=revoked,
        revocation_effective_at_epoch_seconds=revocation_effective_at_epoch_seconds,
        revocation_reason_digest=revocation_reason_digest,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=(
            repository_approval_revocation_status_receipt_digest(receipt)
        ),
    )
    issues = repository_approval_revocation_status_receipt_issues(receipt)
    if issues:
        raise ValueError(f"revocation_status_receipt_invalid:{issues[0]}")
    return receipt


def repository_evolution_external_approval_certificate_issues(
    certificate: RepositoryEvolutionExternalApprovalCertificate,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        certificate.receipt_id,
        certificate.admission_certificate_digest,
        certificate.approval_policy_digest,
        certificate.approval_attestation_digest,
        certificate.signature_verification_receipt_digest,
        certificate.revocation_status_receipt_digest,
    )
    if any(not value for value in required):
        issues.append("external_approval_certificate_required_field_missing")
    if certificate.status not in (APPROVAL_ACCEPTED, APPROVAL_REJECTED):
        issues.append("external_approval_status_invalid")
    if certificate.evaluated_at_epoch_seconds < 0:
        issues.append("external_approval_evaluated_at_negative")
    expected_granted = all((
        certificate.admission_proposal_bound,
        certificate.policy_binding_exact,
        certificate.attestation_binding_exact,
        certificate.decision_approve,
        certificate.approver_authorized,
        certificate.approver_key_authorized,
        certificate.verifier_authorized,
        certificate.revocation_authority_authorized,
        certificate.signature_algorithm_allowed,
        certificate.distinct_approval_roles,
        certificate.signed_payload_binding_exact,
        certificate.signature_metadata_binding_exact,
        certificate.signature_verified,
        certificate.time_order_valid,
        certificate.admission_certificate_fresh,
        certificate.approval_lifetime_within_policy,
        certificate.approval_not_expired,
        certificate.verification_fresh,
        certificate.revocation_status_fresh,
        certificate.no_future_evidence,
        certificate.revocation_status_valid,
        certificate.not_revoked,
    ))
    if certificate.external_approval_granted != expected_granted:
        issues.append("external_approval_grant_mismatch")
    if certificate.application_authorization_eligible != expected_granted:
        issues.append("application_authorization_eligibility_mismatch")
    if certificate.status == APPROVAL_ACCEPTED and not expected_granted:
        issues.append("accepted_status_without_valid_approval")
    if certificate.status == APPROVAL_REJECTED and expected_granted:
        issues.append("rejected_status_with_valid_approval")
    if certificate.patch_application_authority_granted:
        issues.append("unexpected_patch_application_authority")
    if certificate.commit_authority_granted:
        issues.append("unexpected_commit_authority")
    if certificate.reference_mutation_authority_granted:
        issues.append("unexpected_reference_mutation_authority")
    if certificate.certificate_digest != (
        repository_evolution_external_approval_certificate_digest(certificate)
    ):
        issues.append("external_approval_certificate_digest_mismatch")
    return tuple(issues)


def _finalize_external_approval_certificate(
    certificate: RepositoryEvolutionExternalApprovalCertificate,
) -> RepositoryEvolutionExternalApprovalCertificate:
    certificate = replace(
        certificate,
        certificate_digest=(
            repository_evolution_external_approval_certificate_digest(certificate)
        ),
    )
    issues = repository_evolution_external_approval_certificate_issues(certificate)
    if issues:
        raise ValueError(f"external_approval_certificate_invalid:{issues[0]}")
    return certificate


def certify_repository_evolution_external_approval(
    receipt_id: str,
    admission_certificate: RepositoryEvolutionAdmissionCertificate,
    policy: RepositoryExternalApprovalPolicy,
    attestation: RepositoryExternalApprovalAttestation,
    signature_verification: RepositorySignatureVerificationReceipt,
    revocation_status: RepositoryApprovalRevocationStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryEvolutionExternalApprovalCertificate:
    if not receipt_id:
        raise ValueError("external_approval_receipt_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("external_approval_evaluated_at_negative")

    admission_issues = repository_evolution_admission_certificate_issues(
        admission_certificate
    )
    if admission_issues:
        raise ValueError(f"admission_certificate_invalid:{admission_issues[0]}")
    if admission_certificate.status != ADMISSION_PROPOSED:
        raise ValueError("admission_certificate_not_proposed")
    if not admission_certificate.admission_proposal_generated:
        raise ValueError("admission_proposal_missing")
    if not admission_certificate.external_approval_required:
        raise ValueError("admission_external_approval_not_required")
    if admission_certificate.external_approval_granted:
        raise ValueError("admission_external_approval_already_granted")

    policy_issues = repository_external_approval_policy_issues(policy)
    if policy_issues:
        raise ValueError(f"external_approval_policy_invalid:{policy_issues[0]}")
    attestation_issues = repository_external_approval_attestation_issues(attestation)
    if attestation_issues:
        raise ValueError(f"external_approval_attestation_invalid:{attestation_issues[0]}")
    verification_issues = repository_signature_verification_receipt_issues(
        signature_verification
    )
    if verification_issues:
        raise ValueError(
            f"signature_verification_receipt_invalid:{verification_issues[0]}"
        )
    revocation_issues = repository_approval_revocation_status_receipt_issues(
        revocation_status
    )
    if revocation_issues:
        raise ValueError(f"revocation_status_receipt_invalid:{revocation_issues[0]}")

    if admission_certificate.approval_policy_digest != policy.policy_digest:
        raise ValueError("admission_policy_binding_mismatch")
    if attestation.admission_certificate_digest != admission_certificate.certificate_digest:
        raise ValueError("approval_admission_binding_mismatch")
    if attestation.approval_policy_digest != policy.policy_digest:
        raise ValueError("approval_policy_binding_mismatch")
    if signature_verification.attestation_digest != attestation.attestation_digest:
        raise ValueError("signature_verification_attestation_binding_mismatch")
    if revocation_status.attestation_digest != attestation.attestation_digest:
        raise ValueError("revocation_attestation_binding_mismatch")
    if revocation_status.approval_policy_digest != policy.policy_digest:
        raise ValueError("revocation_policy_binding_mismatch")

    metadata_exact = all((
        signature_verification.signature_algorithm == attestation.signature_algorithm,
        signature_verification.signing_key_id == attestation.signing_key_id,
        signature_verification.signed_payload_digest == attestation.signed_payload_digest,
        signature_verification.signature_digest == attestation.signature_digest,
    ))
    if not metadata_exact:
        raise ValueError("signature_verification_metadata_mismatch")

    decision_approve = attestation.decision == DECISION_APPROVE
    approver_authorized = attestation.approver_id in policy.authorized_approver_ids
    approver_key_authorized = (
        repository_approver_key_binding_digest(
            attestation.approver_id,
            attestation.signing_key_id,
        ) in policy.authorized_approver_key_binding_digests
    )
    verifier_authorized = (
        signature_verification.verifier_id in policy.authorized_verifier_ids
    )
    revocation_authority_authorized = (
        revocation_status.authority_id
        in policy.authorized_revocation_authority_ids
    )
    signature_algorithm_allowed = (
        attestation.signature_algorithm in policy.allowed_signature_algorithms
    )
    distinct_roles = (
        not policy.require_distinct_approver_and_verifier
        or attestation.approver_id != signature_verification.verifier_id
    )
    signed_payload_exact = (
        attestation.signed_payload_digest
        == repository_external_approval_signed_payload_digest(attestation)
    )

    admission_time = admission_certificate.evaluated_at_epoch_seconds
    issued_time = attestation.issued_at_epoch_seconds
    verified_time = signature_verification.verified_at_epoch_seconds
    revocation_time = revocation_status.checked_at_epoch_seconds
    time_order_valid = (
        admission_time <= issued_time <= verified_time <= revocation_time
        <= evaluated_at_epoch_seconds
    )
    no_future_evidence = all((
        admission_time <= evaluated_at_epoch_seconds,
        issued_time <= evaluated_at_epoch_seconds,
        verified_time <= evaluated_at_epoch_seconds,
        revocation_time <= evaluated_at_epoch_seconds,
    ))
    admission_fresh = (
        admission_time <= evaluated_at_epoch_seconds
        and evaluated_at_epoch_seconds - admission_time
        <= policy.max_admission_certificate_age_seconds
    )
    approval_lifetime = (
        attestation.expires_at_epoch_seconds - issued_time
    )
    approval_lifetime_within_policy = (
        0 < approval_lifetime <= policy.max_approval_lifetime_seconds
    )
    approval_not_expired = evaluated_at_epoch_seconds < (
        attestation.expires_at_epoch_seconds
    )
    verification_fresh = (
        verified_time <= evaluated_at_epoch_seconds
        and evaluated_at_epoch_seconds - verified_time
        <= policy.max_verification_age_seconds
    )
    revocation_fresh = (
        revocation_time <= evaluated_at_epoch_seconds
        and evaluated_at_epoch_seconds - revocation_time
        <= policy.max_revocation_status_age_seconds
    )
    revocation_status_valid = (
        revocation_time >= verified_time
        and revocation_status.registry_snapshot_digest != ""
    )
    not_revoked = not revocation_status.revoked

    granted = all((
        decision_approve,
        approver_authorized,
        approver_key_authorized,
        verifier_authorized,
        revocation_authority_authorized,
        signature_algorithm_allowed,
        distinct_roles,
        signed_payload_exact,
        metadata_exact,
        signature_verification.signature_verified,
        time_order_valid,
        admission_fresh,
        approval_lifetime_within_policy,
        approval_not_expired,
        verification_fresh,
        revocation_fresh,
        no_future_evidence,
        revocation_status_valid,
        not_revoked,
    ))
    status = APPROVAL_ACCEPTED if granted else APPROVAL_REJECTED
    certificate = RepositoryEvolutionExternalApprovalCertificate(
        receipt_id=receipt_id,
        status=status,
        admission_certificate_digest=admission_certificate.certificate_digest,
        approval_policy_digest=policy.policy_digest,
        approval_attestation_digest=attestation.attestation_digest,
        signature_verification_receipt_digest=signature_verification.receipt_digest,
        revocation_status_receipt_digest=revocation_status.receipt_digest,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        admission_proposal_bound=True,
        policy_binding_exact=True,
        attestation_binding_exact=True,
        decision_approve=decision_approve,
        approver_authorized=approver_authorized,
        approver_key_authorized=approver_key_authorized,
        verifier_authorized=verifier_authorized,
        revocation_authority_authorized=revocation_authority_authorized,
        signature_algorithm_allowed=signature_algorithm_allowed,
        distinct_approval_roles=distinct_roles,
        signed_payload_binding_exact=signed_payload_exact,
        signature_metadata_binding_exact=metadata_exact,
        signature_verified=signature_verification.signature_verified,
        time_order_valid=time_order_valid,
        admission_certificate_fresh=admission_fresh,
        approval_lifetime_within_policy=approval_lifetime_within_policy,
        approval_not_expired=approval_not_expired,
        verification_fresh=verification_fresh,
        revocation_status_fresh=revocation_fresh,
        no_future_evidence=no_future_evidence,
        revocation_status_valid=revocation_status_valid,
        not_revoked=not_revoked,
        external_approval_granted=granted,
        application_authorization_eligible=granted,
        patch_application_authority_granted=False,
        commit_authority_granted=False,
        reference_mutation_authority_granted=False,
        certificate_digest="",
    )
    return _finalize_external_approval_certificate(certificate)
