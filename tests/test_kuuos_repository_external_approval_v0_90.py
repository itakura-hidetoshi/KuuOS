from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_external_approval_types_v0_90 import (
    APPROVAL_ACCEPTED,
    APPROVAL_REJECTED,
    DECISION_APPROVE,
    DECISION_REJECT,
    repository_approval_revocation_status_receipt_digest,
    repository_external_approval_attestation_digest,
    repository_external_approval_signed_payload_digest,
    repository_signature_verification_receipt_digest,
)
from runtime.kuuos_repository_external_approval_v0_90 import (
    build_repository_approval_revocation_status_receipt,
    build_repository_external_approval_attestation,
    build_repository_external_approval_policy,
    build_repository_signature_verification_receipt,
    certify_repository_evolution_external_approval,
    repository_evolution_external_approval_certificate_issues,
    repository_external_approval_policy_issues,
)
from tests.test_kuuos_repository_evolution_admission_v0_89 import (
    RepositoryEvolutionAdmissionV089Tests,
)


class RepositoryExternalApprovalV090Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = self._policy()
        self.admission, self.admission_fixture = self._admission_for_policy(self.policy)
        self.attestation = self._attestation()
        self.verification = build_repository_signature_verification_receipt(
            "verification-v090",
            self.attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        self.revocation = build_repository_approval_revocation_status_receipt(
            "revocation-status-v090",
            self.attestation,
            self.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest({"registry": "snapshot-1220"}),
            revoked=False,
        )

    def _policy(
        self,
        *,
        authorized_approver_ids=("approver-1",),
        authorized_verifier_ids=("verifier-1",),
        authorized_revocation_authority_ids=("revocation-authority-1",),
        authorized_approver_key_bindings=(("approver-1", "key-1"),),
        allowed_signature_algorithms=("EXTERNAL-ED25519-RECEIPT",),
        max_admission_certificate_age_seconds=500,
        max_approval_lifetime_seconds=1000,
        max_verification_age_seconds=100,
        max_revocation_status_age_seconds=100,
        require_distinct_approver_and_verifier=True,
    ):
        return build_repository_external_approval_policy(
            "external-approval-policy-v090",
            authorized_approver_ids=authorized_approver_ids,
            authorized_verifier_ids=authorized_verifier_ids,
            authorized_revocation_authority_ids=authorized_revocation_authority_ids,
            authorized_approver_key_bindings=authorized_approver_key_bindings,
            allowed_signature_algorithms=allowed_signature_algorithms,
            max_admission_certificate_age_seconds=max_admission_certificate_age_seconds,
            max_approval_lifetime_seconds=max_approval_lifetime_seconds,
            max_verification_age_seconds=max_verification_age_seconds,
            max_revocation_status_age_seconds=max_revocation_status_age_seconds,
            require_distinct_approver_and_verifier=require_distinct_approver_and_verifier,
        )

    def _admission_for_policy(self, policy):
        fixture = RepositoryEvolutionAdmissionV089Tests(
            methodName="test_two_fresh_identical_replays_generate_proposal"
        )
        fixture.setUp()
        fixture.approval_policy_digest = policy.policy_digest
        return fixture._certify(), fixture

    def _attestation(
        self,
        *,
        admission=None,
        policy=None,
        approver_id="approver-1",
        decision=DECISION_APPROVE,
        issued_at_epoch_seconds=1200,
        expires_at_epoch_seconds=1800,
        signature_algorithm="EXTERNAL-ED25519-RECEIPT",
        signing_key_id="key-1",
    ):
        return build_repository_external_approval_attestation(
            "approval-v090",
            self.admission if admission is None else admission,
            self.policy if policy is None else policy,
            approver_id=approver_id,
            decision=decision,
            issued_at_epoch_seconds=issued_at_epoch_seconds,
            expires_at_epoch_seconds=expires_at_epoch_seconds,
            signature_algorithm=signature_algorithm,
            signing_key_id=signing_key_id,
            signature_digest=canonical_digest({
                "signature": "external-fixture",
                "approver": approver_id,
                "key": signing_key_id,
            }),
        )

    def _certify(
        self,
        *,
        admission=None,
        policy=None,
        attestation=None,
        verification=None,
        revocation=None,
        evaluated_at_epoch_seconds=1250,
    ):
        return certify_repository_evolution_external_approval(
            "external-approval-receipt-v090",
            self.admission if admission is None else admission,
            self.policy if policy is None else policy,
            self.attestation if attestation is None else attestation,
            self.verification if verification is None else verification,
            self.revocation if revocation is None else revocation,
            evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        )

    def test_valid_external_receipts_accept_approval_without_mutation_authority(self) -> None:
        certificate = self._certify()
        self.assertEqual(certificate.status, APPROVAL_ACCEPTED)
        self.assertTrue(certificate.external_approval_granted)
        self.assertTrue(certificate.application_authorization_eligible)
        self.assertTrue(certificate.signature_verified)
        self.assertTrue(certificate.not_revoked)
        self.assertFalse(certificate.patch_application_authority_granted)
        self.assertFalse(certificate.commit_authority_granted)
        self.assertFalse(certificate.reference_mutation_authority_granted)
        self.assertEqual(
            repository_evolution_external_approval_certificate_issues(certificate),
            (),
        )

    def test_explicit_reject_decision_is_certified_reject(self) -> None:
        attestation = self._attestation(decision=DECISION_REJECT)
        verification = build_repository_signature_verification_receipt(
            "verification-reject",
            attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-reject",
            attestation,
            self.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-reject"),
            revoked=False,
        )
        certificate = self._certify(
            attestation=attestation,
            verification=verification,
            revocation=revocation,
        )
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.decision_approve)
        self.assertFalse(certificate.external_approval_granted)

    def test_unauthorized_approver_is_certified_reject(self) -> None:
        attestation = self._attestation(
            approver_id="approver-unknown",
            signing_key_id="key-unknown",
        )
        verification = build_repository_signature_verification_receipt(
            "verification-unknown-approver",
            attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-unknown-approver",
            attestation,
            self.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-unknown-approver"),
            revoked=False,
        )
        certificate = self._certify(
            attestation=attestation,
            verification=verification,
            revocation=revocation,
        )
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.approver_authorized)
        self.assertFalse(certificate.approver_key_authorized)

    def test_unauthorized_verifier_is_certified_reject(self) -> None:
        verification = build_repository_signature_verification_receipt(
            "verification-unknown",
            self.attestation,
            verifier_id="verifier-unknown",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        certificate = self._certify(verification=verification)
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.verifier_authorized)

    def test_unauthorized_revocation_authority_is_certified_reject(self) -> None:
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-unknown-authority",
            self.attestation,
            self.policy,
            authority_id="revocation-authority-unknown",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-unknown-authority"),
            revoked=False,
        )
        certificate = self._certify(revocation=revocation)
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.revocation_authority_authorized)

    def test_unauthorized_signing_key_is_certified_reject(self) -> None:
        attestation = self._attestation(signing_key_id="key-unknown")
        verification = build_repository_signature_verification_receipt(
            "verification-unknown-key",
            attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-unknown-key",
            attestation,
            self.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-unknown-key"),
            revoked=False,
        )
        certificate = self._certify(
            attestation=attestation,
            verification=verification,
            revocation=revocation,
        )
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.approver_key_authorized)

    def test_unallowed_signature_algorithm_is_certified_reject(self) -> None:
        attestation = self._attestation(signature_algorithm="UNLISTED-ALGORITHM")
        verification = build_repository_signature_verification_receipt(
            "verification-unlisted-algorithm",
            attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-unlisted-algorithm",
            attestation,
            self.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-unlisted-algorithm"),
            revoked=False,
        )
        certificate = self._certify(
            attestation=attestation,
            verification=verification,
            revocation=revocation,
        )
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.signature_algorithm_allowed)

    def test_failed_external_signature_verification_is_certified_reject(self) -> None:
        verification = build_repository_signature_verification_receipt(
            "verification-failed",
            self.attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=False,
        )
        certificate = self._certify(verification=verification)
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.signature_verified)

    def test_expired_approval_is_certified_reject(self) -> None:
        attestation = self._attestation(expires_at_epoch_seconds=1240)
        verification = build_repository_signature_verification_receipt(
            "verification-expired",
            attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-expired",
            attestation,
            self.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-expired"),
            revoked=False,
        )
        certificate = self._certify(
            attestation=attestation,
            verification=verification,
            revocation=revocation,
        )
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.approval_not_expired)

    def test_approval_lifetime_above_policy_is_certified_reject(self) -> None:
        attestation = self._attestation(expires_at_epoch_seconds=2300)
        verification = build_repository_signature_verification_receipt(
            "verification-long-lived",
            attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-long-lived",
            attestation,
            self.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-long-lived"),
            revoked=False,
        )
        certificate = self._certify(
            attestation=attestation,
            verification=verification,
            revocation=revocation,
        )
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.approval_lifetime_within_policy)

    def test_stale_admission_certificate_is_certified_reject(self) -> None:
        certificate = self._certify(evaluated_at_epoch_seconds=1700)
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.admission_certificate_fresh)

    def test_stale_signature_verification_is_certified_reject(self) -> None:
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-late-check",
            self.attestation,
            self.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1390,
            registry_snapshot_digest=canonical_digest("registry-late-check"),
            revoked=False,
        )
        certificate = self._certify(
            revocation=revocation,
            evaluated_at_epoch_seconds=1400,
        )
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.verification_fresh)
        self.assertTrue(certificate.revocation_status_fresh)

    def test_stale_revocation_status_is_certified_reject(self) -> None:
        policy = self._policy(
            max_verification_age_seconds=1000,
            max_revocation_status_age_seconds=100,
        )
        admission, _ = self._admission_for_policy(policy)
        attestation = self._attestation(admission=admission, policy=policy)
        verification = build_repository_signature_verification_receipt(
            "verification-stale-revocation",
            attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-stale",
            attestation,
            policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-stale"),
            revoked=False,
        )
        certificate = self._certify(
            admission=admission,
            policy=policy,
            attestation=attestation,
            verification=verification,
            revocation=revocation,
            evaluated_at_epoch_seconds=1400,
        )
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertTrue(certificate.verification_fresh)
        self.assertFalse(certificate.revocation_status_fresh)

    def test_revoked_approval_is_certified_reject(self) -> None:
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-active",
            self.attestation,
            self.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-revoked"),
            revoked=True,
            revocation_effective_at_epoch_seconds=1215,
            revocation_reason_digest=canonical_digest("approval withdrawn"),
        )
        certificate = self._certify(revocation=revocation)
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.not_revoked)

    def test_distinct_approver_and_verifier_policy_is_enforced(self) -> None:
        policy = self._policy(
            authorized_verifier_ids=("approver-1",),
        )
        admission, _ = self._admission_for_policy(policy)
        attestation = self._attestation(admission=admission, policy=policy)
        verification = build_repository_signature_verification_receipt(
            "verification-same-role",
            attestation,
            verifier_id="approver-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-same-role",
            attestation,
            policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-same-role"),
            revoked=False,
        )
        certificate = self._certify(
            admission=admission,
            policy=policy,
            attestation=attestation,
            verification=verification,
            revocation=revocation,
        )
        self.assertEqual(certificate.status, APPROVAL_REJECTED)
        self.assertFalse(certificate.distinct_approval_roles)

    def test_admission_binding_mismatch_fails_closed(self) -> None:
        attestation = replace(
            self.attestation,
            admission_certificate_digest="0" * 64,
            signed_payload_digest="",
            attestation_digest="",
        )
        attestation = replace(
            attestation,
            signed_payload_digest=repository_external_approval_signed_payload_digest(
                attestation
            ),
        )
        attestation = replace(
            attestation,
            attestation_digest=repository_external_approval_attestation_digest(
                attestation
            ),
        )
        verification = build_repository_signature_verification_receipt(
            "verification-wrong-admission",
            attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-wrong-admission",
            attestation,
            self.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-wrong-admission"),
            revoked=False,
        )
        with self.assertRaisesRegex(ValueError, "approval_admission_binding_mismatch"):
            self._certify(
                attestation=attestation,
                verification=verification,
                revocation=revocation,
            )

    def test_policy_binding_mismatch_fails_closed(self) -> None:
        attestation = replace(
            self.attestation,
            approval_policy_digest="f" * 64,
            signed_payload_digest="",
            attestation_digest="",
        )
        attestation = replace(
            attestation,
            signed_payload_digest=repository_external_approval_signed_payload_digest(
                attestation
            ),
        )
        attestation = replace(
            attestation,
            attestation_digest=repository_external_approval_attestation_digest(
                attestation
            ),
        )
        verification = build_repository_signature_verification_receipt(
            "verification-wrong-policy",
            attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = replace(
            self.revocation,
            attestation_digest=attestation.attestation_digest,
            receipt_digest="",
        )
        revocation = replace(
            revocation,
            receipt_digest=repository_approval_revocation_status_receipt_digest(
                revocation
            ),
        )
        with self.assertRaisesRegex(ValueError, "approval_policy_binding_mismatch"):
            self._certify(
                attestation=attestation,
                verification=verification,
                revocation=revocation,
            )

    def test_signature_metadata_mismatch_fails_closed(self) -> None:
        verification = replace(
            self.verification,
            signing_key_id="different-key",
            receipt_digest="",
        )
        verification = replace(
            verification,
            receipt_digest=repository_signature_verification_receipt_digest(
                verification
            ),
        )
        with self.assertRaisesRegex(ValueError, "signature_verification_metadata_mismatch"):
            self._certify(verification=verification)

    def test_revocation_target_mismatch_fails_closed(self) -> None:
        revocation = replace(
            self.revocation,
            attestation_digest="0" * 64,
            receipt_digest="",
        )
        revocation = replace(
            revocation,
            receipt_digest=repository_approval_revocation_status_receipt_digest(
                revocation
            ),
        )
        with self.assertRaisesRegex(ValueError, "revocation_attestation_binding_mismatch"):
            self._certify(revocation=revocation)

    def test_tampered_verification_receipt_fails_closed(self) -> None:
        tampered = replace(self.verification, signature_verified=False)
        with self.assertRaisesRegex(ValueError, "signature_verification_receipt_invalid"):
            self._certify(verification=tampered)

    def test_nonproposed_admission_cannot_be_approved(self) -> None:
        self.admission_fixture.approval_policy_digest = self.policy.policy_digest
        rejected = self.admission_fixture._certify(
            receipts=(self.admission_fixture.receipts[0],)
        )
        attestation = self._attestation(admission=rejected)
        verification = build_repository_signature_verification_receipt(
            "verification-rejected-admission",
            attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-rejected-admission",
            attestation,
            self.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-rejected-admission"),
            revoked=False,
        )
        with self.assertRaisesRegex(ValueError, "admission_certificate_not_proposed"):
            self._certify(
                admission=rejected,
                attestation=attestation,
                verification=verification,
                revocation=revocation,
            )

    def test_policy_and_certificate_tamper_detection(self) -> None:
        self.assertEqual(repository_external_approval_policy_issues(self.policy), ())
        bad_policy = replace(self.policy, max_approval_lifetime_seconds=1)
        self.assertIn(
            "policy_digest_mismatch",
            repository_external_approval_policy_issues(bad_policy),
        )
        certificate = self._certify()
        bad_certificate = replace(certificate, commit_authority_granted=True)
        issues = repository_evolution_external_approval_certificate_issues(
            bad_certificate
        )
        self.assertIn("unexpected_commit_authority", issues)
        self.assertIn("external_approval_certificate_digest_mismatch", issues)


if __name__ == "__main__":
    unittest.main()
