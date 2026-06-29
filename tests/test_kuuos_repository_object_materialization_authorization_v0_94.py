from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_object_materialization_authorization_strict_v0_94 import (
    authorize_repository_object_materialization,
    repository_object_materialization_authorization_certificate_issues,
)
from runtime.kuuos_repository_object_materialization_authorization_types_v0_94 import (
    AUTHORIZATION_GRANTED,
    AUTHORIZATION_REJECTED,
    GIT_OBJECT_FORMAT_SHA1,
    RepositoryObjectDatabaseEntry,
    repository_object_materialization_authorization_certificate_digest,
    repository_object_materialization_nonce_status_receipt_digest,
    repository_object_materialization_scope_digest,
)
from runtime.kuuos_repository_object_materialization_authorization_v0_94 import (
    build_repository_object_database_observation,
    build_repository_object_materialization_authorization_policy,
    build_repository_object_materialization_nonce_status_receipt,
    build_repository_object_materialization_scope,
    derive_repository_candidate_objects,
)
from tests.test_kuuos_repository_commit_candidate_v0_93 import (
    RepositoryCommitCandidateV093Tests,
)


class RepositoryObjectMaterializationAuthorizationV094Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryCommitCandidateV093Tests(
            methodName="test_candidate_is_deterministic_and_exactly_bound"
        )
        fixture.setUp()
        self.fixture = fixture
        self.candidate = fixture._certify()
        self.application_receipt = fixture.application_receipt
        self.snapshot = fixture.snapshot
        self.parent_inventory = fixture.parent_inventory
        self.candidate_policy = fixture.policy
        self.candidate_objects = derive_repository_candidate_objects(
            self.candidate,
            self.application_receipt,
            self.snapshot,
            self.parent_inventory,
            self.candidate_policy,
        )
        self.repository_id = "github:itakura-hidetoshi/KuuOS"
        self.git_dir_fingerprint = "1" * 64
        self.nonce_authority_id = "kuuos-object-materialization-nonce-v094"
        self.evaluated_at = 10_020
        self.policy = self._policy()
        self.observation = self._observation()
        self.scope = self._scope()
        self.nonce_status = self._nonce()

    def _policy(self, **overrides):
        values = {
            "policy_id": "object-materialization-policy-v094",
            "allowed_repository_ids": (self.repository_id,),
            "authorized_nonce_authority_ids": (self.nonce_authority_id,),
            "max_authorization_lifetime_seconds": 300,
            "max_observation_age_seconds": 60,
            "max_nonce_status_age_seconds": 60,
            "max_new_object_count": 512,
            "max_new_payload_bytes": 10_000_000,
        }
        values.update(overrides)
        return build_repository_object_materialization_authorization_policy(**values)

    def _parent_entry(self):
        return RepositoryObjectDatabaseEntry(
            kind="commit",
            oid=self.candidate.parent_commit_sha,
            payload_size=1,
            payload_digest="a" * 64,
        )

    def _queries(self):
        return tuple(item.oid for item in self.candidate_objects) + (
            self.candidate.parent_commit_sha,
        )

    def _observation(self, **overrides):
        values = {
            "observation_id": "object-database-observation-v094",
            "repository_id": self.repository_id,
            "git_dir_fingerprint": self.git_dir_fingerprint,
            "object_format": GIT_OBJECT_FORMAT_SHA1,
            "source_commit_sha": self.candidate.parent_commit_sha,
            "queried_oids": self._queries(),
            "existing_objects": (self._parent_entry(),),
            "object_database_read": True,
            "working_tree_read": False,
            "observed_at_epoch_seconds": 10_000,
        }
        values.update(overrides)
        return build_repository_object_database_observation(**values)

    def _scope(self, **overrides):
        values = {
            "scope_id": "object-materialization-scope-v094",
            "certificate": self.candidate,
            "policy": self.policy,
            "observation": self.observation,
            "authorization_nonce": "materialization-nonce-v094-001",
            "issued_at_epoch_seconds": 10_005,
            "expires_at_epoch_seconds": 10_100,
        }
        values.update(overrides)
        return build_repository_object_materialization_scope(**values)

    def _nonce(self, **overrides):
        values = {
            "status_id": "object-materialization-nonce-status-v094",
            "scope": self.scope,
            "authority_id": self.nonce_authority_id,
            "checked_at_epoch_seconds": 10_010,
            "registry_snapshot_digest": "b" * 64,
            "consumed": False,
            "revoked": False,
        }
        values.update(overrides)
        return build_repository_object_materialization_nonce_status_receipt(**values)

    def _authorize(self, **overrides):
        values = {
            "authorization_id": "object-materialization-authorization-v094-001",
            "candidate_certificate": self.candidate,
            "application_receipt": self.application_receipt,
            "snapshot": self.snapshot,
            "parent_tree_inventory": self.parent_inventory,
            "candidate_policy": self.candidate_policy,
            "policy": self.policy,
            "scope": self.scope,
            "observation": self.observation,
            "nonce_status": self.nonce_status,
            "evaluated_at_epoch_seconds": self.evaluated_at,
        }
        values.update(overrides)
        return authorize_repository_object_materialization(**values)

    def _issues(self, certificate, **overrides):
        values = {
            "candidate_certificate": self.candidate,
            "application_receipt": self.application_receipt,
            "snapshot": self.snapshot,
            "parent_tree_inventory": self.parent_inventory,
            "candidate_policy": self.candidate_policy,
            "policy": self.policy,
            "scope": self.scope,
            "observation": self.observation,
            "nonce_status": self.nonce_status,
            "evaluated_at_epoch_seconds": self.evaluated_at,
        }
        values.update(overrides)
        return repository_object_materialization_authorization_certificate_issues(
            certificate,
            **values,
        )

    def test_candidate_object_set_is_unique_and_dependency_ordered(self) -> None:
        objects = self.candidate_objects
        self.assertEqual(len(objects), len({item.oid for item in objects}))
        self.assertTrue(any(item.kind == "blob" for item in objects))
        self.assertTrue(any(item.kind == "tree" for item in objects))
        self.assertEqual(objects[-1].kind, "commit")
        self.assertEqual(objects[-1].oid, self.candidate.candidate_commit_oid)

    def test_authorization_is_deterministic_and_granted(self) -> None:
        first = self._authorize()
        second = self._authorize()
        self.assertEqual(first, second)
        self.assertEqual(first.status, AUTHORIZATION_GRANTED)
        self.assertTrue(first.materialization_authorization_granted)
        self.assertTrue(first.single_use_materialization_eligible)
        self.assertTrue(first.object_database_write_authority_granted)
        self.assertTrue(first.commit_object_materialization_authority_granted)
        self.assertEqual(first.unique_candidate_object_count, len(self.candidate_objects))
        self.assertEqual(first.new_object_count, len(self.candidate_objects))
        self.assertEqual(first.reused_existing_object_count, 0)
        self.assertEqual(self._issues(first), ())

    def test_authorization_performs_no_repository_effect(self) -> None:
        certificate = self._authorize()
        self.assertFalse(certificate.object_database_write_performed)
        self.assertFalse(certificate.commit_object_written)
        self.assertFalse(certificate.index_write_performed)
        self.assertFalse(certificate.working_tree_write_performed)
        self.assertFalse(certificate.reference_mutation_authority_granted)
        self.assertFalse(certificate.reference_mutated)
        self.assertFalse(certificate.signing_performed)

    def test_existing_exact_candidate_object_is_reused(self) -> None:
        existing_candidate = self.candidate_objects[0]
        exact_entry = RepositoryObjectDatabaseEntry(
            kind=existing_candidate.kind,
            oid=existing_candidate.oid,
            payload_size=existing_candidate.payload_size,
            payload_digest=existing_candidate.payload_digest,
        )
        observation = self._observation(
            existing_objects=(self._parent_entry(), exact_entry)
        )
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_GRANTED)
        self.assertEqual(certificate.reused_existing_object_count, 1)
        self.assertEqual(
            certificate.new_object_count,
            len(self.candidate_objects) - 1,
        )
        reused = next(
            item for item in certificate.plan_items if item.oid == existing_candidate.oid
        )
        self.assertTrue(reused.already_present_exact)
        self.assertFalse(reused.write_required)
        self.assertEqual(reused.write_order, -1)

    def test_existing_oid_payload_collision_is_rejected(self) -> None:
        candidate = self.candidate_objects[0]
        collision = RepositoryObjectDatabaseEntry(
            kind=candidate.kind,
            oid=candidate.oid,
            payload_size=candidate.payload_size,
            payload_digest="f" * 64,
        )
        observation = self._observation(
            existing_objects=(self._parent_entry(), collision)
        )
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.existing_objects_collision_free)
        self.assertFalse(certificate.object_database_write_authority_granted)

    def test_missing_parent_commit_is_rejected(self) -> None:
        observation = self._observation(existing_objects=())
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.source_parent_present)

    def test_incomplete_query_set_is_rejected(self) -> None:
        observation = self._observation(queried_oids=self._queries()[:-1])
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertFalse(certificate.queried_object_set_exact)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_disallowed_repository_is_rejected(self) -> None:
        observation = self._observation(repository_id="github:other/repository")
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertFalse(certificate.repository_allowed)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_scope_repository_identity_mismatch_is_rejected(self) -> None:
        scope = replace(
            self.scope,
            git_dir_fingerprint="2" * 64,
            scope_digest="",
        )
        scope = replace(
            scope,
            scope_digest=repository_object_materialization_scope_digest(scope),
        )
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(scope=scope, nonce_status=nonce)
        self.assertFalse(certificate.repository_identity_exact)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_object_format_mismatch_is_rejected(self) -> None:
        observation = self._observation(object_format="sha256")
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertFalse(certificate.object_format_exact)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_stale_observation_is_rejected(self) -> None:
        observation = self._observation(observed_at_epoch_seconds=9_000)
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertFalse(certificate.observation_fresh)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_non_object_database_observation_is_rejected(self) -> None:
        observation = self._observation(object_database_read=False)
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertFalse(certificate.object_database_source)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_working_tree_observation_is_rejected(self) -> None:
        observation = self._observation(working_tree_read=True)
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertFalse(certificate.working_tree_ignored)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_consumed_or_revoked_nonce_is_rejected(self) -> None:
        for key in ("consumed", "revoked"):
            nonce = self._nonce(**{key: True})
            certificate = self._authorize(nonce_status=nonce)
            self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
            self.assertFalse(
                certificate.nonce_unused if key == "consumed" else certificate.nonce_not_revoked
            )

    def test_unauthorized_nonce_authority_is_rejected(self) -> None:
        nonce = self._nonce(authority_id="unknown-authority")
        certificate = self._authorize(nonce_status=nonce)
        self.assertFalse(certificate.nonce_authority_authorized)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_nonce_scope_mismatch_is_rejected(self) -> None:
        nonce = replace(
            self.nonce_status,
            authorization_scope_digest="c" * 64,
            receipt_digest="",
        )
        nonce = replace(
            nonce,
            receipt_digest=(
                repository_object_materialization_nonce_status_receipt_digest(nonce)
            ),
        )
        certificate = self._authorize(nonce_status=nonce)
        self.assertFalse(certificate.nonce_scope_bound)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_expired_authorization_is_rejected(self) -> None:
        certificate = self._authorize(evaluated_at_epoch_seconds=10_101)
        self.assertFalse(certificate.authorization_not_expired)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_excessive_authorization_lifetime_is_rejected(self) -> None:
        scope = self._scope(expires_at_epoch_seconds=11_000)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(scope=scope, nonce_status=nonce)
        self.assertFalse(certificate.authorization_lifetime_within_policy)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_future_evidence_is_rejected(self) -> None:
        observation = self._observation(observed_at_epoch_seconds=10_030)
        scope = self._scope(observation=observation)
        nonce = self._nonce(scope=scope, checked_at_epoch_seconds=10_031)
        certificate = self._authorize(
            observation=observation,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertFalse(certificate.no_future_evidence)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_object_count_policy_bound_is_enforced(self) -> None:
        policy = self._policy(max_new_object_count=1)
        scope = self._scope(policy=policy)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            policy=policy,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertFalse(certificate.object_count_within_policy)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_payload_byte_policy_bound_is_enforced(self) -> None:
        policy = self._policy(max_new_payload_bytes=1)
        scope = self._scope(policy=policy)
        nonce = self._nonce(scope=scope)
        certificate = self._authorize(
            policy=policy,
            scope=scope,
            nonce_status=nonce,
        )
        self.assertFalse(certificate.payload_bytes_within_policy)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)

    def test_candidate_certificate_tamper_fails_closed(self) -> None:
        tampered = replace(
            self.candidate,
            candidate_commit_oid="f" * 40,
            certificate_digest="",
        )
        with self.assertRaisesRegex(ValueError, "commit_candidate_certificate_invalid"):
            self._authorize(candidate_certificate=tampered)

    def test_plan_tamper_is_detected_after_outer_digest_recomputation(self) -> None:
        certificate = self._authorize()
        plan = list(certificate.plan_items)
        plan[0] = replace(plan[0], write_order=99)
        tampered = replace(
            certificate,
            plan_items=tuple(plan),
            certificate_digest="",
        )
        tampered = replace(
            tampered,
            certificate_digest=(
                repository_object_materialization_authorization_certificate_digest(
                    tampered
                )
            ),
        )
        self.assertIn(
            "object_materialization_recomputation_mismatch",
            self._issues(tampered),
        )

    def test_effect_and_reference_authority_tamper_is_detected(self) -> None:
        certificate = self._authorize()
        tampered = replace(
            certificate,
            object_database_write_performed=True,
            reference_mutation_authority_granted=True,
            reference_mutated=True,
            certificate_digest="",
        )
        tampered = replace(
            tampered,
            certificate_digest=(
                repository_object_materialization_authorization_certificate_digest(
                    tampered
                )
            ),
        )
        issues = self._issues(tampered)
        self.assertIn("unexpected_object_database_write", issues)
        self.assertIn("unexpected_reference_mutation_authority", issues)
        self.assertIn("unexpected_reference_mutation", issues)


if __name__ == "__main__":
    unittest.main()
