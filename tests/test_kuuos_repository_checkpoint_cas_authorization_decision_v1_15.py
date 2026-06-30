from dataclasses import replace
import unittest

from runtime.kuuos_repository_checkpoint_cas_authorization_decision_types_v1_15 import (
    DECISION_DENIED,
    DECISION_GRANTED,
    DECISION_REJECTED,
    EXTERNAL_DENY,
    EXTERNAL_GRANT,
    repository_checkpoint_cas_external_authorization_decision_receipt_digest,
)
from runtime.kuuos_repository_checkpoint_cas_authorization_decision_v1_15 import (
    build_repository_checkpoint_cas_authorization_decision_policy,
    build_repository_checkpoint_cas_authorization_nonce_status_receipt,
    build_repository_checkpoint_cas_external_authorization_decision_receipt,
    derive_repository_checkpoint_cas_authorization_decision_certificate,
)
from runtime.kuuos_repository_checkpoint_cas_authorization_request_types_v1_14 import (
    repository_checkpoint_cas_authorization_request_digest,
)
from tests import test_kuuos_repository_checkpoint_cas_authorization_request_v1_14 as v114_tests


class RepositoryCheckpointCasAuthorizationDecisionV115Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = v114_tests.RepositoryCheckpointCasAuthorizationRequestV114Tests(
            methodName="test_same_input_is_deterministic"
        )
        self.helper.setUp()
        self.coherence = self.helper.coherence_receipt()
        self.request = self.helper.request(self.coherence)
        self.policy = build_repository_checkpoint_cas_authorization_decision_policy(
            "checkpoint-cas-authorization-decision-policy-v115-tests",
            authorized_decision_authority_ids=("decision-authority-v115",),
            authorized_nonce_authority_ids=("nonce-authority-v115",),
            max_decision_lifetime_seconds=180,
            max_nonce_status_age_seconds=60,
        )
        self.evaluated_at = self.helper.issued_at + 30

    def external_decision(self, request=None, *, decision=EXTERNAL_GRANT, **changes):
        current = self.request if request is None else request
        values = {
            "authority_id": "decision-authority-v115",
            "decision": decision,
            "issued_at_epoch_seconds": self.helper.issued_at + 5,
            "expires_at_epoch_seconds": self.helper.issued_at + 90,
            "signature_verification_receipt_digest": "signature-receipt-v115",
            "revocation_status_receipt_digest": "revocation-receipt-v115",
            "signature_valid": True,
            "authority_identity_verified": True,
            "decision_not_revoked": True,
        }
        values.update(changes)
        return build_repository_checkpoint_cas_external_authorization_decision_receipt(
            "checkpoint-cas-external-decision-v115",
            current,
            **values,
        )

    def nonce_status(self, request=None, **changes):
        current = self.request if request is None else request
        values = {
            "authority_id": "nonce-authority-v115",
            "checked_at_epoch_seconds": self.helper.issued_at + 20,
            "registry_snapshot_digest": "nonce-registry-snapshot-v115",
            "consumed": False,
            "revoked": False,
        }
        values.update(changes)
        return build_repository_checkpoint_cas_authorization_nonce_status_receipt(
            "checkpoint-cas-nonce-status-v115",
            current,
            **values,
        )

    def certificate(
        self,
        *,
        request=None,
        coherence=None,
        external_decision=None,
        nonce_status=None,
        evaluated_at=None,
    ):
        current_request = self.request if request is None else request
        current_coherence = self.coherence if coherence is None else coherence
        current_decision = (
            self.external_decision(current_request)
            if external_decision is None
            else external_decision
        )
        current_nonce = (
            self.nonce_status(current_request)
            if nonce_status is None
            else nonce_status
        )
        return derive_repository_checkpoint_cas_authorization_decision_certificate(
            "checkpoint-cas-authorization-decision-v115",
            current_request,
            current_coherence,
            self.helper.policy,
            self.policy,
            current_decision,
            current_nonce,
            evaluated_at_epoch_seconds=(
                self.evaluated_at if evaluated_at is None else evaluated_at
            ),
        )

    def test_ready_request_with_valid_external_grant_is_eligible_only(self) -> None:
        certificate = self.certificate()
        self.assertEqual(certificate.status, DECISION_GRANTED)
        self.assertTrue(certificate.external_decision_accepted)
        self.assertTrue(certificate.authorization_granted)
        self.assertTrue(certificate.single_use_cas_eligible)
        self.assertFalse(certificate.nonce_consumed)
        self.assertFalse(certificate.execution_performed)
        self.assertFalse(certificate.live_git_command_invoked)
        self.assertFalse(certificate.reference_mutated)

    def test_valid_external_denial_grants_no_eligibility(self) -> None:
        certificate = self.certificate(
            external_decision=self.external_decision(decision=EXTERNAL_DENY)
        )
        self.assertEqual(certificate.status, DECISION_DENIED)
        self.assertTrue(certificate.external_decision_accepted)
        self.assertFalse(certificate.authorization_granted)
        self.assertFalse(certificate.single_use_cas_eligible)
        self.assertFalse(certificate.nonce_consumed)

    def test_conflict_request_cannot_be_granted(self) -> None:
        conflict_coherence = self.helper.coherence_receipt(
            observed_current_oid=v114_tests.v113_tests.OTHER_OID
        )
        conflict_request = self.helper.request(conflict_coherence)
        certificate = self.certificate(
            request=conflict_request,
            coherence=conflict_coherence,
            external_decision=self.external_decision(conflict_request),
            nonce_status=self.nonce_status(conflict_request),
        )
        self.assertEqual(certificate.status, DECISION_REJECTED)
        self.assertFalse(certificate.request_ready)
        self.assertFalse(certificate.authorization_granted)
        self.assertFalse(certificate.single_use_cas_eligible)

    def test_invalid_evidence_and_request_tamper_are_rejected(self) -> None:
        stale_nonce = self.nonce_status(
            checked_at_epoch_seconds=self.evaluated_at - 61
        )
        consumed_nonce = self.nonce_status(consumed=True)
        unsigned_decision = self.external_decision(signature_valid=False)

        unbound_decision = replace(
            self.external_decision(),
            request_digest="f" * 64,
            receipt_digest="",
        )
        unbound_decision = replace(
            unbound_decision,
            receipt_digest=(
                repository_checkpoint_cas_external_authorization_decision_receipt_digest(
                    unbound_decision
                )
            ),
        )

        tampered_request = replace(
            self.request,
            proposed_checkpoint_oid=v114_tests.v113_tests.OTHER_OID,
            request_digest="",
        )
        tampered_request = replace(
            tampered_request,
            request_digest=repository_checkpoint_cas_authorization_request_digest(
                tampered_request
            ),
        )
        tampered_certificate = self.certificate(
            request=tampered_request,
            external_decision=self.external_decision(tampered_request),
            nonce_status=self.nonce_status(tampered_request),
        )

        cases = (
            self.certificate(nonce_status=stale_nonce),
            self.certificate(nonce_status=consumed_nonce),
            self.certificate(external_decision=unsigned_decision),
            self.certificate(external_decision=unbound_decision),
            tampered_certificate,
        )
        for index, certificate in enumerate(cases):
            with self.subTest(case=index):
                self.assertEqual(certificate.status, DECISION_REJECTED)
                self.assertFalse(certificate.authorization_granted)
                self.assertFalse(certificate.single_use_cas_eligible)
                self.assertFalse(certificate.nonce_consumed)
                self.assertFalse(certificate.reference_mutated)

    def test_same_input_is_deterministic(self) -> None:
        external_decision = self.external_decision()
        nonce_status = self.nonce_status()
        first = self.certificate(
            external_decision=external_decision,
            nonce_status=nonce_status,
        )
        second = self.certificate(
            external_decision=external_decision,
            nonce_status=nonce_status,
        )
        self.assertEqual(first.to_dict(), second.to_dict())


if __name__ == "__main__":
    unittest.main()
