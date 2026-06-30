from dataclasses import replace
import unittest

from runtime.kuuos_repository_checkpoint_cas_authorization_request_types_v1_14 import (
    REQUEST_DENIED,
    REQUEST_READY,
    REQUEST_REJECTED,
)
from runtime.kuuos_repository_checkpoint_cas_authorization_request_v1_14 import (
    build_repository_checkpoint_cas_authorization_request_policy,
    derive_repository_checkpoint_cas_authorization_request,
)
from runtime.kuuos_repository_checkpoint_cas_coherence_types_v1_13 import (
    repository_checkpoint_cas_coherence_digest,
)
from runtime.v113_checkpoint_cas_coherence_core import (
    derive_repository_checkpoint_cas_coherence_receipt,
)
from tests.test_kuuos_repository_checkpoint_cas_coherence_v1_13 import (
    OTHER_OID,
    RepositoryCheckpointCasCoherenceV113Tests,
)


class RepositoryCheckpointCasAuthorizationRequestV114Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = RepositoryCheckpointCasCoherenceV113Tests(
            methodName="test_same_input_is_deterministic"
        )
        self.helper.setUp()
        self.policy = build_repository_checkpoint_cas_authorization_request_policy(
            "checkpoint-cas-authorization-request-policy-v114-tests",
            allowed_repository_ids=(self.helper.stability.repository_id,),
            allowed_checkpoint_references=(
                self.helper.stability.checkpoint_reference,
            ),
            max_request_lifetime_seconds=300,
        )
        self.issued_at = 1_800_000_000
        self.expires_at = self.issued_at + 120

    def coherence_receipt(self, *, observed_current_oid=None):
        contract, intake = self.helper.artifacts(
            observed_current_oid=observed_current_oid
        )
        return derive_repository_checkpoint_cas_coherence_receipt(
            "checkpoint-cas-coherence-v113-for-v114",
            contract,
            intake,
        )

    def request(self, receipt, *, policy=None, nonce="nonce-v114"):
        return derive_repository_checkpoint_cas_authorization_request(
            "checkpoint-cas-authorization-request-v114",
            receipt,
            self.policy if policy is None else policy,
            requester_id="requester-v114",
            authorization_nonce=nonce,
            issued_at_epoch_seconds=self.issued_at,
            expires_at_epoch_seconds=self.expires_at,
        )

    def test_coherent_ready_produces_request_without_grant_or_execution(self) -> None:
        request = self.request(self.coherence_receipt())
        self.assertEqual(request.status, REQUEST_READY)
        self.assertTrue(request.coherence_receipt_valid)
        self.assertTrue(request.single_use_authorization_required)
        self.assertFalse(request.authorization_granted)
        self.assertFalse(request.execution_performed)
        self.assertFalse(request.live_git_command_invoked)
        self.assertFalse(request.reference_mutated)

    def test_coherent_conflict_is_denied_without_authorization_candidate(self) -> None:
        request = self.request(
            self.coherence_receipt(observed_current_oid=OTHER_OID)
        )
        self.assertEqual(request.status, REQUEST_DENIED)
        self.assertTrue(request.coherence_receipt_valid)
        self.assertFalse(request.single_use_authorization_required)
        self.assertFalse(request.authorization_granted)

    def test_invalid_nonce_lifetime_and_policy_binding_are_rejected(self) -> None:
        receipt = self.coherence_receipt()
        cases = []
        cases.append(
            derive_repository_checkpoint_cas_authorization_request(
                "checkpoint-cas-authorization-request-empty-nonce",
                receipt,
                self.policy,
                requester_id="requester-v114",
                authorization_nonce="",
                issued_at_epoch_seconds=self.issued_at,
                expires_at_epoch_seconds=self.expires_at,
            )
        )
        cases.append(
            derive_repository_checkpoint_cas_authorization_request(
                "checkpoint-cas-authorization-request-long-lifetime",
                receipt,
                self.policy,
                requester_id="requester-v114",
                authorization_nonce="nonce-v114-long",
                issued_at_epoch_seconds=self.issued_at,
                expires_at_epoch_seconds=self.issued_at + 301,
            )
        )
        other_policy = build_repository_checkpoint_cas_authorization_request_policy(
            "checkpoint-cas-authorization-request-policy-other",
            allowed_repository_ids=("repository-other",),
            allowed_checkpoint_references=("refs/kuuos/checkpoints/other",),
            max_request_lifetime_seconds=300,
        )
        cases.append(self.request(receipt, policy=other_policy))

        for index, request in enumerate(cases):
            with self.subTest(case=index):
                self.assertEqual(request.status, REQUEST_REJECTED)
                self.assertFalse(request.single_use_authorization_required)
                self.assertFalse(request.authorization_granted)

    def test_self_consistent_ready_oid_tamper_is_rejected(self) -> None:
        receipt = self.coherence_receipt()
        changed = replace(
            receipt,
            observed_current_oid=OTHER_OID,
            coherence_digest="",
        )
        changed = replace(
            changed,
            coherence_digest=repository_checkpoint_cas_coherence_digest(changed),
        )
        request = self.request(changed)
        self.assertEqual(request.status, REQUEST_REJECTED)
        self.assertFalse(request.coherence_receipt_valid)
        self.assertFalse(request.single_use_authorization_required)
        self.assertFalse(request.authorization_granted)

    def test_same_input_is_deterministic(self) -> None:
        receipt = self.coherence_receipt()
        first = self.request(receipt)
        second = self.request(receipt)
        self.assertEqual(first.to_dict(), second.to_dict())


if __name__ == "__main__":
    unittest.main()
