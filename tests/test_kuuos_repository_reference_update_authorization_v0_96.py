from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_object_materialization_receipt_types_v0_95 import (
    repository_object_materialization_receipt_digest,
)
from runtime.kuuos_repository_reference_update_authorization_strict_v0_96 import (
    authorize_repository_reference_update,
    repository_reference_update_authorization_certificate_issues,
)
from runtime.kuuos_repository_reference_update_authorization_types_v0_96 import (
    AUTHORIZATION_GRANTED,
    AUTHORIZATION_REJECTED,
    ZERO_OID,
    repository_reference_ancestry_certificate_digest,
    repository_reference_observation_digest,
    repository_reference_update_authorization_certificate_digest,
    repository_reference_update_nonce_status_receipt_digest,
    repository_reference_update_scope_digest,
)
from runtime.kuuos_repository_reference_update_v0_96 import (
    build_repository_reference_ancestry_certificate,
    build_repository_reference_observation,
    build_repository_reference_update_nonce_status_receipt,
    build_repository_reference_update_policy,
    build_repository_reference_update_scope,
)
from tests.test_kuuos_repository_object_materialization_receipt_v0_95 import (
    RepositoryObjectMaterializationReceiptV095Tests,
)


class RepositoryReferenceUpdateAuthorizationV096Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryObjectMaterializationReceiptV095Tests(
            methodName="test_receipt_is_deterministic_and_committed"
        )
        fixture.setUp()
        self.v095 = fixture
        self.materialization_receipt = fixture._certify()
        self.target_reference = "refs/heads/main"
        self.nonce_authority_id = "kuuos-reference-nonce-authority-v096"
        self.policy = self._policy()
        self.observation = self._observation()
        self.ancestry = self._ancestry()
        self.scope = self._scope()
        self.nonce_status = self._nonce()

    def _policy(self, **overrides):
        values = {
            "policy_id": "repository-reference-update-policy-v096",
            "allowed_repository_ids": (self.materialization_receipt.repository_id,),
            "allowed_references": (self.target_reference,),
            "authorized_nonce_authority_ids": (self.nonce_authority_id,),
            "max_authorization_lifetime_seconds": 120,
            "max_reference_observation_age_seconds": 30,
            "max_ancestry_certificate_age_seconds": 30,
            "max_nonce_status_age_seconds": 30,
            "max_ancestry_depth": 1,
        }
        values.update(overrides)
        return build_repository_reference_update_policy(**values)

    def _observation(self, **overrides):
        values = {
            "observation_id": "reference-observation-v096-001",
            "repository_id": self.materialization_receipt.repository_id,
            "git_dir_fingerprint": self.materialization_receipt.git_dir_fingerprint,
            "target_reference": self.target_reference,
            "observed_oid": self.materialization_receipt.parent_commit_sha,
            "rechecked_oid": self.materialization_receipt.parent_commit_sha,
            "direct": True,
            "symbolic": False,
            "reference_store_read": True,
            "working_tree_read": False,
            "observed_at_epoch_seconds": 10_040,
            "rechecked_at_epoch_seconds": 10_045,
        }
        values.update(overrides)
        return build_repository_reference_observation(**values)

    def _ancestry(
        self,
        materialization_receipt=None,
        post_observation=None,
        target_reference=None,
        **overrides,
    ):
        values = {
            "certificate_id": "reference-ancestry-v096-001",
            "materialization_receipt": (
                materialization_receipt or self.materialization_receipt
            ),
            "candidate_certificate": self.v095.fixture.candidate,
            "object_database_observation": (
                post_observation or self.v095.post_observation
            ),
            "target_reference": target_reference or self.target_reference,
            "object_database_read": True,
            "working_tree_read": False,
            "observed_at_epoch_seconds": 10_046,
        }
        values.update(overrides)
        return build_repository_reference_ancestry_certificate(**values)

    def _scope(
        self,
        materialization_receipt=None,
        policy=None,
        observation=None,
        ancestry=None,
        **overrides,
    ):
        values = {
            "scope_id": "reference-update-scope-v096-001",
            "materialization_receipt": (
                materialization_receipt or self.materialization_receipt
            ),
            "policy": policy or self.policy,
            "observation": observation or self.observation,
            "ancestry_certificate": ancestry or self.ancestry,
            "authorization_nonce": "reference-update-nonce-v096-001",
            "issued_at_epoch_seconds": 10_047,
            "expires_at_epoch_seconds": 10_100,
            "force_update_requested": False,
            "delete_requested": False,
        }
        values.update(overrides)
        return build_repository_reference_update_scope(**values)

    def _nonce(self, scope=None, **overrides):
        values = {
            "status_id": "reference-update-nonce-status-v096-001",
            "scope": scope or self.scope,
            "authority_id": self.nonce_authority_id,
            "checked_at_epoch_seconds": 10_048,
            "registry_snapshot_digest": "a" * 64,
            "consumed": False,
            "revoked": False,
        }
        values.update(overrides)
        return build_repository_reference_update_nonce_status_receipt(**values)

    def _authorization_values(self, **overrides):
        values = {
            "authorization_id": "reference-update-authorization-v096-001",
            "materialization_receipt": self.materialization_receipt,
            "materialization_authorization": self.v095.authorization,
            "candidate_certificate": self.v095.fixture.candidate,
            "application_receipt": self.v095.fixture.application_receipt,
            "snapshot": self.v095.fixture.snapshot,
            "parent_tree_inventory": self.v095.fixture.parent_inventory,
            "candidate_policy": self.v095.fixture.candidate_policy,
            "materialization_authorization_policy": self.v095.fixture.policy,
            "materialization_scope": self.v095.fixture.scope,
            "pre_object_database_observation": self.v095.fixture.observation,
            "pre_materialization_nonce_status": self.v095.fixture.nonce_status,
            "materialization_policy": self.v095.policy,
            "execution_report": self.v095.execution,
            "post_object_database_observation": self.v095.post_observation,
            "nonce_consumption_receipt": self.v095.nonce_consumption,
            "policy": self.policy,
            "observation": self.observation,
            "ancestry_certificate": self.ancestry,
            "scope": self.scope,
            "nonce_status": self.nonce_status,
            "evaluated_at_epoch_seconds": 10_050,
        }
        values.update(overrides)
        return values

    def _authorize(self, **overrides):
        return authorize_repository_reference_update(
            **self._authorization_values(**overrides)
        )

    def _issues(self, certificate, **overrides):
        values = self._authorization_values(**overrides)
        values.pop("authorization_id")
        return repository_reference_update_authorization_certificate_issues(
            certificate, **values
        )

    @staticmethod
    def _resign_observation(observation):
        observation = replace(observation, receipt_digest="")
        return replace(
            observation,
            receipt_digest=repository_reference_observation_digest(observation),
        )

    @staticmethod
    def _resign_ancestry(certificate):
        certificate = replace(certificate, certificate_digest="")
        return replace(
            certificate,
            certificate_digest=repository_reference_ancestry_certificate_digest(
                certificate
            ),
        )

    @staticmethod
    def _resign_scope(scope):
        scope = replace(scope, scope_digest="")
        return replace(scope, scope_digest=repository_reference_update_scope_digest(scope))

    @staticmethod
    def _resign_nonce(receipt):
        receipt = replace(receipt, receipt_digest="")
        return replace(
            receipt,
            receipt_digest=repository_reference_update_nonce_status_receipt_digest(
                receipt
            ),
        )

    def _components_for_observation(self, observation, target_reference=None):
        target = target_reference or observation.target_reference
        ancestry = self._ancestry(target_reference=target)
        scope = self._scope(observation=observation, ancestry=ancestry)
        nonce = self._nonce(scope=scope)
        return ancestry, scope, nonce

    def test_valid_fast_forward_authorization_is_deterministic(self) -> None:
        first = self._authorize()
        second = self._authorize()
        self.assertEqual(first, second)
        self.assertEqual(first.status, AUTHORIZATION_GRANTED)
        self.assertTrue(first.reference_update_authority_granted)
        self.assertTrue(first.single_use_reference_update_eligible)
        self.assertTrue(first.compare_and_swap_required)
        self.assertTrue(first.fast_forward_verified)
        self.assertEqual(self._issues(first), ())

    def test_authorization_binds_exact_repository_and_reference(self) -> None:
        certificate = self._authorize()
        self.assertEqual(certificate.repository_id, self.materialization_receipt.repository_id)
        self.assertEqual(certificate.target_reference, self.target_reference)
        self.assertTrue(certificate.repository_identity_exact)
        self.assertTrue(certificate.reference_observation_bound)

    def test_authorization_binds_exact_old_and_new_oids(self) -> None:
        certificate = self._authorize()
        self.assertEqual(certificate.expected_old_oid, self.materialization_receipt.parent_commit_sha)
        self.assertEqual(certificate.proposed_new_oid, self.materialization_receipt.candidate_commit_oid)
        self.assertTrue(certificate.old_oid_exact)
        self.assertTrue(certificate.new_oid_exact)

    def test_invalid_ref_syntax_is_rejected(self) -> None:
        observation = self._observation(target_reference="refs/heads/bad..name")
        ancestry, scope, nonce = self._components_for_observation(observation)
        certificate = self._authorize(
            observation=observation,
            ancestry_certificate=ancestry,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.reference_name_valid)

    def test_head_tag_and_remote_tracking_refs_are_rejected(self) -> None:
        for target in ("HEAD", "refs/tags/v1", "refs/remotes/origin/main"):
            observation = self._observation(target_reference=target)
            ancestry, scope, nonce = self._components_for_observation(
                observation, target_reference=target
            )
            certificate = self._authorize(
                observation=observation,
                ancestry_certificate=ancestry,
                scope=scope,
                nonce_status=nonce,
            )
            self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_symbolic_ref_is_rejected(self) -> None:
        observation = self._observation(direct=False, symbolic=True)
        ancestry, scope, nonce = self._components_for_observation(observation)
        certificate = self._authorize(
            observation=observation,
            ancestry_certificate=ancestry,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.reference_direct)
        self.assertFalse(certificate.reference_not_symbolic)

    def test_zero_oid_is_rejected(self) -> None:
        observation = self._observation(observed_oid=ZERO_OID, rechecked_oid=ZERO_OID)
        ancestry, scope, nonce = self._components_for_observation(observation)
        certificate = self._authorize(
            observation=observation,
            ancestry_certificate=ancestry,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.reference_not_deleted)
        self.assertFalse(certificate.old_oid_exact)

    def test_old_oid_mismatch_is_rejected(self) -> None:
        observation = self._observation(observed_oid="1" * 40, rechecked_oid="1" * 40)
        ancestry, scope, nonce = self._components_for_observation(observation)
        certificate = self._authorize(
            observation=observation,
            ancestry_certificate=ancestry,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.old_oid_exact)

    def test_new_oid_mismatch_is_rejected(self) -> None:
        scope = self._resign_scope(replace(self.scope, proposed_new_oid="2" * 40))
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(scope=scope, nonce_status=nonce)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.new_oid_exact)

    def test_candidate_commit_absence_is_rejected(self) -> None:
        entries = tuple(
            entry
            for entry in self.v095.post_observation.existing_objects
            if entry.oid != self.materialization_receipt.candidate_commit_oid
        )
        post = self.v095._post_observation(existing_objects=entries)
        receipt = self.v095._certify(post_observation=post)
        ancestry = self._ancestry(
            materialization_receipt=receipt,
            post_observation=post,
        )
        scope = self._scope(materialization_receipt=receipt, ancestry=ancestry)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            materialization_receipt=receipt,
            post_object_database_observation=post,
            ancestry_certificate=ancestry,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.materialization_receipt_committed)
        self.assertFalse(certificate.candidate_commit_present)

    def test_candidate_commit_payload_mismatch_is_rejected(self) -> None:
        entries = list(self.v095.post_observation.existing_objects)
        index = next(
            i
            for i, entry in enumerate(entries)
            if entry.oid == self.materialization_receipt.candidate_commit_oid
        )
        entries[index] = replace(entries[index], payload_digest="e" * 64)
        post = self.v095._post_observation(existing_objects=tuple(entries))
        receipt = self.v095._certify(post_observation=post)
        ancestry = self._ancestry(
            materialization_receipt=receipt,
            post_observation=post,
        )
        scope = self._scope(materialization_receipt=receipt, ancestry=ancestry)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            materialization_receipt=receipt,
            post_object_database_observation=post,
            ancestry_certificate=ancestry,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.candidate_commit_present)

    def test_stale_reference_observation_is_rejected(self) -> None:
        observation = self._observation(
            observed_at_epoch_seconds=9_900,
            rechecked_at_epoch_seconds=9_901,
        )
        ancestry, scope, nonce = self._components_for_observation(observation)
        certificate = self._authorize(
            observation=observation,
            ancestry_certificate=ancestry,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.reference_observation_fresh)

    def test_working_tree_reference_observation_is_rejected(self) -> None:
        observation = self._observation(working_tree_read=True)
        ancestry, scope, nonce = self._components_for_observation(observation)
        certificate = self._authorize(
            observation=observation,
            ancestry_certificate=ancestry,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.reference_working_tree_ignored)

    def test_reference_change_between_observation_and_recheck_is_rejected(self) -> None:
        observation = self._observation(rechecked_oid="4" * 40)
        ancestry, scope, nonce = self._components_for_observation(observation)
        certificate = self._authorize(
            observation=observation,
            ancestry_certificate=ancestry,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.reference_unchanged_since_observation)
        self.assertFalse(certificate.compare_and_swap_required)

    def test_non_fast_forward_ancestry_is_rejected(self) -> None:
        ancestry = self._resign_ancestry(
            replace(
                self.ancestry,
                path_oids=(self.scope.expected_old_oid, "5" * 40, self.scope.proposed_new_oid),
                depth=2,
            )
        )
        scope = self._scope(ancestry=ancestry)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            ancestry_certificate=ancestry,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.fast_forward_verified)
        self.assertFalse(certificate.ancestry_depth_within_policy)

    def test_ancestry_certificate_tamper_is_rejected_before_authorization(self) -> None:
        ancestry = replace(self.ancestry, depth=2)
        with self.assertRaisesRegex(ValueError, "reference_ancestry_certificate_invalid"):
            self._authorize(ancestry_certificate=ancestry)

    def test_consumed_revoked_or_scope_mismatched_nonce_is_rejected(self) -> None:
        consumed = self._nonce(consumed=True)
        self.assertFalse(self._authorize(nonce_status=consumed).nonce_unused)
        revoked = self._nonce(revoked=True)
        self.assertFalse(self._authorize(nonce_status=revoked).nonce_not_revoked)
        mismatched = self._resign_nonce(
            replace(self.nonce_status, authorization_scope_digest="f" * 64)
        )
        self.assertFalse(self._authorize(nonce_status=mismatched).nonce_scope_bound)

    def test_expired_authorization_is_rejected(self) -> None:
        scope = self._scope(expires_at_epoch_seconds=10_049)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(scope=scope, nonce_status=nonce)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.authorization_not_expired)

    def test_future_evidence_is_rejected(self) -> None:
        observation = self._observation(
            observed_at_epoch_seconds=10_055,
            rechecked_at_epoch_seconds=10_056,
        )
        ancestry, scope, nonce = self._components_for_observation(observation)
        certificate = self._authorize(
            observation=observation,
            ancestry_certificate=ancestry,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.no_future_evidence)

    def test_force_and_delete_requests_are_rejected(self) -> None:
        for field in ("force_update_requested", "delete_requested"):
            scope = self._scope(**{field: True})
            nonce = self._nonce(scope=scope)
            certificate = self._authorize(scope=scope, nonce_status=nonce)
            self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
            self.assertFalse(certificate.force_update_authorized)
            self.assertFalse(certificate.reference_delete_authorized)

    def test_authorization_performs_no_repository_effect(self) -> None:
        certificate = self._authorize()
        for field in (
            "reference_update_performed",
            "reference_mutated",
            "branch_updated",
            "head_updated",
            "tag_updated",
            "remote_reference_updated",
            "push_performed",
            "index_write_performed",
            "working_tree_write_performed",
            "object_database_write_performed",
            "signing_performed",
        ):
            self.assertFalse(getattr(certificate, field))

    def test_reference_mutation_effect_tamper_is_detected(self) -> None:
        certificate = self._authorize()
        tampered = replace(
            certificate,
            reference_mutated=True,
            certificate_digest="",
        )
        tampered = replace(
            tampered,
            certificate_digest=repository_reference_update_authorization_certificate_digest(
                tampered
            ),
        )
        issues = self._issues(tampered)
        self.assertIn("reference_update_authorization_recomputation_mismatch", issues)
        self.assertIn("reference_update_authorization_forbidden_effect", issues)

    def test_outer_digest_recomputation_cannot_hide_materialization_tamper(self) -> None:
        receipt = replace(
            self.materialization_receipt,
            candidate_commit_present=False,
            receipt_digest="",
        )
        receipt = replace(
            receipt,
            receipt_digest=repository_object_materialization_receipt_digest(receipt),
        )
        with self.assertRaisesRegex(ValueError, "object_materialization_receipt_invalid"):
            self._authorize(materialization_receipt=receipt)


if __name__ == "__main__":
    unittest.main()
