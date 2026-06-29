from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_checkpoint_authorization_strict_v101 import (
    authorize_repository_local_frontier_checkpoint_creation,
    repository_local_frontier_checkpoint_authorization_certificate_issues,
)
from runtime.kuuos_repository_local_frontier_checkpoint_authorization_types_v1_01 import (
    AUTHORIZATION_GRANTED,
    AUTHORIZATION_REJECTED,
    ZERO_OID,
    repository_checkpoint_reference_observation_digest,
    repository_local_frontier_checkpoint_authorization_certificate_digest,
    repository_local_frontier_checkpoint_nonce_status_receipt_digest,
    repository_local_frontier_checkpoint_policy_digest,
    repository_local_frontier_checkpoint_scope_digest,
)
from runtime.kuuos_repository_local_frontier_checkpoint_authorization_v1_01 import (
    build_repository_checkpoint_reference_observation,
    build_repository_local_frontier_checkpoint_nonce_status_receipt,
    build_repository_local_frontier_checkpoint_policy,
    build_repository_local_frontier_checkpoint_scope,
    normalize_repository_checkpoint_reference_name,
)
from runtime.kuuos_repository_local_frontier_finality_types_v1_00 import (
    repository_local_frontier_finality_certificate_digest,
)
from tests.test_kuuos_repository_local_frontier_finality_v1_00 import (
    RepositoryLocalFrontierFinalityV100Tests,
)


class RepositoryLocalFrontierCheckpointAuthorizationV101Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryLocalFrontierFinalityV100Tests(
            methodName="test_valid_finality_certificate_is_deterministic"
        )
        fixture.setUp()
        self.v100 = fixture
        self.finality_certificate = fixture._certify()
        self.finality_inputs = fixture._values()
        self.finality_inputs.pop("certificate_id")
        self.checkpoint_reference = "refs/kuuos/checkpoints/frontier-v1-00"
        self.nonce_authority_id = "kuuos-checkpoint-nonce-authority-v101"
        self.policy = self._policy()
        self.observation = self._observation()
        self.scope = self._scope()
        self.nonce_status = self._nonce()
        self.evaluated_at = 10_174

    def _policy(self, **overrides):
        values = {
            "policy_id": "repository-checkpoint-policy-v101",
            "allowed_repository_ids": (
                self.finality_certificate.repository_id,
            ),
            "allowed_checkpoint_references": (self.checkpoint_reference,),
            "authorized_nonce_authority_ids": (self.nonce_authority_id,),
            "max_authorization_lifetime_seconds": 60,
            "max_reference_observation_age_seconds": 30,
            "max_nonce_status_age_seconds": 30,
        }
        values.update(overrides)
        return build_repository_local_frontier_checkpoint_policy(**values)

    def _observation(self, **overrides):
        values = {
            "observation_id": "repository-checkpoint-observation-v101-001",
            "repository_id": self.finality_certificate.repository_id,
            "git_dir_fingerprint": self.finality_certificate.git_dir_fingerprint,
            "checkpoint_reference": self.checkpoint_reference,
            "observed_oid": ZERO_OID,
            "rechecked_oid": ZERO_OID,
            "observed_at_epoch_seconds": 10_170,
            "rechecked_at_epoch_seconds": 10_171,
        }
        values.update(overrides)
        return build_repository_checkpoint_reference_observation(**values)

    def _scope(
        self,
        finality_certificate=None,
        policy=None,
        observation=None,
        **overrides,
    ):
        values = {
            "scope_id": "repository-checkpoint-scope-v101-001",
            "finality_certificate": (
                finality_certificate or self.finality_certificate
            ),
            "policy": policy or self.policy,
            "observation": observation or self.observation,
            "authorization_nonce": "checkpoint-nonce-v101-001",
            "issued_at_epoch_seconds": 10_172,
            "expires_at_epoch_seconds": 10_200,
        }
        values.update(overrides)
        return build_repository_local_frontier_checkpoint_scope(**values)

    def _nonce(self, scope=None, **overrides):
        values = {
            "status_id": "repository-checkpoint-nonce-status-v101-001",
            "scope": scope or self.scope,
            "authority_id": self.nonce_authority_id,
            "checked_at_epoch_seconds": 10_173,
            "registry_snapshot_digest": "a" * 64,
            "consumed": False,
            "revoked": False,
        }
        values.update(overrides)
        return build_repository_local_frontier_checkpoint_nonce_status_receipt(
            **values
        )

    def _values(self, **overrides):
        values = {
            "authorization_id": "repository-checkpoint-authorization-v101-001",
            "finality_certificate": self.finality_certificate,
            "finality_inputs": self.finality_inputs,
            "policy": self.policy,
            "observation": self.observation,
            "scope": self.scope,
            "nonce_status": self.nonce_status,
            "evaluated_at_epoch_seconds": self.evaluated_at,
        }
        values.update(overrides)
        return values

    def _authorize(self, **overrides):
        return authorize_repository_local_frontier_checkpoint_creation(
            **self._values(**overrides)
        )

    def _issues(self, certificate, **overrides):
        values = self._values(**overrides)
        values.pop("authorization_id")
        return repository_local_frontier_checkpoint_authorization_certificate_issues(
            certificate,
            **values,
        )

    @staticmethod
    def _resign_policy(policy):
        policy = replace(policy, policy_digest="")
        return replace(
            policy,
            policy_digest=repository_local_frontier_checkpoint_policy_digest(
                policy
            ),
        )

    @staticmethod
    def _resign_observation(observation):
        observation = replace(observation, observation_digest="")
        return replace(
            observation,
            observation_digest=(
                repository_checkpoint_reference_observation_digest(observation)
            ),
        )

    @staticmethod
    def _resign_scope(scope):
        scope = replace(scope, scope_digest="")
        return replace(
            scope,
            scope_digest=repository_local_frontier_checkpoint_scope_digest(scope),
        )

    @staticmethod
    def _resign_nonce(receipt):
        receipt = replace(receipt, receipt_digest="")
        return replace(
            receipt,
            receipt_digest=(
                repository_local_frontier_checkpoint_nonce_status_receipt_digest(
                    receipt
                )
            ),
        )

    @staticmethod
    def _resign_certificate(certificate):
        certificate = replace(certificate, certificate_digest="")
        return replace(
            certificate,
            certificate_digest=(
                repository_local_frontier_checkpoint_authorization_certificate_digest(
                    certificate
                )
            ),
        )

    @staticmethod
    def _resign_finality(certificate):
        certificate = replace(certificate, certificate_digest="")
        return replace(
            certificate,
            certificate_digest=(
                repository_local_frontier_finality_certificate_digest(certificate)
            ),
        )

    def test_valid_authorization_is_deterministic_and_granted(self) -> None:
        first = self._authorize()
        second = self._authorize()
        self.assertEqual(first, second)
        self.assertEqual(first.status, AUTHORIZATION_GRANTED)
        self.assertTrue(first.checkpoint_creation_authority_granted)
        self.assertTrue(first.checkpoint_creation_authorized)
        self.assertTrue(first.single_use_checkpoint_creation_eligible)
        self.assertEqual(self._issues(first), ())

    def test_authorization_binds_repository_checkpoint_final_tip_and_transaction(self) -> None:
        certificate = self._authorize()
        self.assertEqual(
            certificate.repository_id,
            self.finality_certificate.repository_id,
        )
        self.assertEqual(
            certificate.git_dir_fingerprint,
            self.finality_certificate.git_dir_fingerprint,
        )
        self.assertEqual(certificate.checkpoint_reference, self.checkpoint_reference)
        self.assertEqual(certificate.expected_old_oid, ZERO_OID)
        self.assertEqual(
            certificate.proposed_new_oid,
            self.finality_certificate.final_tip_oid,
        )
        self.assertEqual(
            certificate.transaction_id,
            self.finality_certificate.transaction_id,
        )
        self.assertTrue(certificate.finality_certificate_binding_exact)
        self.assertTrue(certificate.finality_history_bound)
        self.assertTrue(certificate.final_tip_exact)
        self.assertTrue(certificate.final_tip_present)

    def test_checkpoint_reference_normalization_accepts_only_checkpoint_namespace(self) -> None:
        self.assertEqual(
            normalize_repository_checkpoint_reference_name(
                self.checkpoint_reference
            ),
            self.checkpoint_reference,
        )
        invalid = (
            "HEAD",
            "refs/heads/frontier-v1-00",
            "refs/tags/frontier-v1-00",
            "refs/remotes/origin/frontier-v1-00",
            "refs/notes/frontier-v1-00",
            "refs/replace/frontier-v1-00",
            "refs/kuuos/checkpoints/",
            "refs/kuuos/checkpoints/.hidden",
            "refs/kuuos/checkpoints/name.lock",
            "refs/kuuos/checkpoints/a..b",
            "refs/kuuos/checkpoints/日本語",
        )
        for reference in invalid:
            self.assertIsNone(
                normalize_repository_checkpoint_reference_name(reference)
            )

    def test_branch_tag_remote_and_malformed_references_are_rejected(self) -> None:
        for reference in (
            "HEAD",
            "refs/heads/frontier-v1-00",
            "refs/tags/frontier-v1-00",
            "refs/remotes/origin/frontier-v1-00",
            "refs/notes/frontier-v1-00",
            "refs/replace/frontier-v1-00",
            "refs/kuuos/checkpoints/.hidden",
        ):
            observation = self._observation(checkpoint_reference=reference)
            scope = self._scope(observation=observation)
            nonce = self._nonce(scope=scope)
            certificate = self._authorize(
                observation=observation,
                scope=scope,
                nonce_status=nonce,
            )
            self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
            self.assertFalse(certificate.checkpoint_creation_authorized)

    def test_existing_checkpoint_reference_is_rejected(self) -> None:
        existing_oid = "b" * 40
        observation = self._observation(
            observed_oid=existing_oid,
            rechecked_oid=existing_oid,
        )
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.checkpoint_absent)
        self.assertFalse(certificate.compare_and_swap_nonexistence_required)

    def test_reference_change_between_observation_and_recheck_is_rejected(self) -> None:
        observation = self._observation(rechecked_oid="b" * 40)
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.checkpoint_unchanged_since_observation)
        self.assertFalse(certificate.checkpoint_absent)

    def test_checkpoint_observation_must_be_fresh(self) -> None:
        certificate = self._authorize(evaluated_at_epoch_seconds=10_220)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.checkpoint_observation_fresh)

    def test_indirect_symbolic_or_wrong_source_observation_is_rejected(self) -> None:
        cases = (
            {"direct": False},
            {"symbolic": True},
            {"reference_store_read": False},
            {"working_tree_read": True},
            {"reflog_read": True},
            {"remote_read": True},
        )
        for changes in cases:
            observation = self._resign_observation(
                replace(self.observation, **changes)
            )
            scope = self._scope(observation=observation)
            nonce = self._nonce(scope=scope)
            certificate = self._authorize(
                observation=observation,
                scope=scope,
                nonce_status=nonce,
            )
            self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_repository_identity_mismatch_is_rejected(self) -> None:
        observation = self._observation(repository_id="different-repository-v101")
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.repository_identity_exact)

    def test_scope_finality_digest_mismatch_is_rejected(self) -> None:
        scope = self._resign_scope(
            replace(self.scope, finality_certificate_digest="b" * 64)
        )
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(scope=scope, nonce_status=nonce)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.finality_certificate_binding_exact)

    def test_scope_policy_digest_mismatch_is_fail_closed(self) -> None:
        other_policy = self._policy(policy_id="other-checkpoint-policy-v101")
        with self.assertRaisesRegex(
            ValueError,
            "checkpoint_policy_binding_invalid",
        ):
            self._authorize(policy=other_policy)

    def test_proposed_oid_must_equal_v100_final_tip(self) -> None:
        scope = self._resign_scope(
            replace(self.scope, proposed_new_oid="b" * 40)
        )
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(scope=scope, nonce_status=nonce)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.finality_certificate_binding_exact)
        self.assertFalse(certificate.final_tip_exact)

    def test_rejected_v100_certificate_cannot_grant_checkpoint_authority(self) -> None:
        finality_policy = self.v100._policy(min_sample_count=4)
        finality = self.v100._certify(policy=finality_policy)
        finality_inputs = self.v100._values(policy=finality_policy)
        finality_inputs.pop("certificate_id")
        observation = self._observation()
        scope = self._scope(
            finality_certificate=finality,
            observation=observation,
        )
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            finality_certificate=finality,
            finality_inputs=finality_inputs,
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.finality_certificate_committed)

    def test_v100_tamper_is_rejected_after_outer_digest_recompute(self) -> None:
        finality = self._resign_finality(
            replace(
                self.finality_certificate,
                bounded_local_finality_verified=False,
            )
        )
        with self.assertRaisesRegex(ValueError, "local_frontier_finality_invalid"):
            self._authorize(finality_certificate=finality)

    def test_unauthorized_nonce_authority_is_rejected(self) -> None:
        nonce = self._nonce(authority_id="other-nonce-authority-v101")
        certificate = self._authorize(nonce_status=nonce)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.nonce_authority_authorized)

    def test_nonce_scope_mismatch_is_rejected(self) -> None:
        nonce = self._resign_nonce(
            replace(
                self.nonce_status,
                authorization_scope_digest="b" * 64,
            )
        )
        certificate = self._authorize(nonce_status=nonce)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.nonce_scope_bound)

    def test_consumed_or_revoked_nonce_is_rejected(self) -> None:
        for field in ("consumed", "revoked"):
            nonce = self._resign_nonce(
                replace(self.nonce_status, **{field: True})
            )
            certificate = self._authorize(nonce_status=nonce)
            self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
            self.assertFalse(
                certificate.single_use_checkpoint_creation_eligible
            )

    def test_stale_nonce_status_is_rejected(self) -> None:
        certificate = self._authorize(evaluated_at_epoch_seconds=10_220)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.nonce_status_fresh)

    def test_expired_or_overlong_authorization_is_rejected(self) -> None:
        expired = self._authorize(evaluated_at_epoch_seconds=10_201)
        self.assertEqual(expired.status, AUTHORIZATION_REJECTED)
        self.assertFalse(expired.authorization_not_expired)
        scope = self._scope(expires_at_epoch_seconds=10_300)
        nonce = self._nonce(scope=scope)
        overlong = self._authorize(scope=scope, nonce_status=nonce)
        self.assertEqual(overlong.status, AUTHORIZATION_REJECTED)
        self.assertFalse(overlong.authorization_lifetime_within_policy)

    def test_future_evidence_is_rejected(self) -> None:
        certificate = self._authorize(evaluated_at_epoch_seconds=10_169)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.no_future_evidence)

    def test_create_request_is_required(self) -> None:
        scope = self._scope(create_requested=False)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(scope=scope, nonce_status=nonce)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.create_requested)

    def test_overwrite_delete_force_tag_and_push_requests_are_rejected(self) -> None:
        cases = (
            "overwrite_requested",
            "delete_requested",
            "force_update_requested",
            "tag_creation_requested",
            "push_requested",
        )
        for field in cases:
            scope = self._scope(**{field: True})
            nonce = self._nonce(scope=scope)
            certificate = self._authorize(scope=scope, nonce_status=nonce)
            self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
            self.assertFalse(certificate.checkpoint_creation_authorized)

    def test_policy_cannot_enable_forbidden_authority(self) -> None:
        policy = self._resign_policy(
            replace(self.policy, allow_checkpoint_overwrite=True)
        )
        observation = self._observation()
        scope = self._scope(policy=policy, observation=observation)
        nonce = self._nonce(scope=scope)
        with self.assertRaisesRegex(ValueError, "checkpoint_policy_invalid"):
            self._authorize(
                policy=policy,
                observation=observation,
                scope=scope,
                nonce_status=nonce,
            )

    def test_authorization_performs_no_checkpoint_or_repository_effect(self) -> None:
        certificate = self._authorize()
        for field in (
            "checkpoint_overwrite_authorized",
            "force_update_authorized",
            "reference_delete_authorized",
            "tag_creation_authorized",
            "push_authorized",
            "checkpoint_created",
            "checkpoint_reference_mutated",
            "branch_updated",
            "tag_updated",
            "remote_reference_updated",
            "push_performed",
            "index_write_performed",
            "working_tree_write_performed",
            "object_database_write_performed",
            "reflog_write_performed",
            "signing_performed",
        ):
            self.assertFalse(getattr(certificate, field))

    def test_certificate_tamper_is_detected_after_digest_recompute(self) -> None:
        certificate = self._authorize()
        tampered = self._resign_certificate(
            replace(certificate, checkpoint_created=True, push_performed=True)
        )
        issues = self._issues(tampered)
        self.assertIn("checkpoint_authorization_recomputation_mismatch", issues)
        self.assertIn(
            "checkpoint_authorization_forbidden_effect_or_authority",
            issues,
        )


if __name__ == "__main__":
    unittest.main()
