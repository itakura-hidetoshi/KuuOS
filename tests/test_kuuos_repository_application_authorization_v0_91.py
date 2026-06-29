from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_external_approval_types_v0_90 import DECISION_REJECT
from runtime.kuuos_repository_external_approval_v0_90 import (
    build_repository_approval_revocation_status_receipt,
    build_repository_signature_verification_receipt,
)
from runtime.kuuos_repository_git_revision_types_v0_83 import (
    GitRevisionObservation,
    git_revision_observation_digest,
)
from runtime.kuuos_repository_application_authorization_types_v0_91 import (
    AUTHORIZATION_GRANTED,
    AUTHORIZATION_REJECTED,
    repository_application_scope_digest,
    repository_authorization_nonce_status_receipt_digest,
)
from runtime.kuuos_repository_application_authorization_v0_91 import (
    build_repository_application_authorization_policy,
    build_repository_application_scope,
    build_repository_application_source_state_receipt,
    build_repository_authorization_nonce_status_receipt,
    certify_repository_application_authorization,
    repository_application_authorization_certificate_issues,
    repository_application_authorization_policy_issues,
)
from tests.test_kuuos_repository_external_approval_v0_90 import (
    RepositoryExternalApprovalV090Tests,
)


class RepositoryApplicationAuthorizationV091Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.approval_fixture = RepositoryExternalApprovalV090Tests(
            methodName=(
                "test_valid_external_receipts_accept_approval_without_mutation_authority"
            )
        )
        self.approval_fixture.setUp()
        self.external_approval = self.approval_fixture._certify()
        self.policy = self._policy()
        self.source_commit_sha = "a" * 40
        self.source_snapshot_digest = canonical_digest({"snapshot": "source-v091"})
        self.scope = self._scope()
        self.source_state = self._source_state()
        self.nonce_status = self._nonce_status()

    def _policy(self, **overrides):
        values = {
            "authorized_nonce_authority_ids": ("nonce-authority-1",),
            "protected_paths": (
                ".github/workflows",
                "formal/KUOS/Constitution.lean",
            ),
            "max_authorization_lifetime_seconds": 300,
            "max_source_observation_age_seconds": 60,
            "max_nonce_status_age_seconds": 30,
            "max_allowed_path_count": 8,
            "max_patch_count": 4,
        }
        values.update(overrides)
        return build_repository_application_authorization_policy(
            "application-authorization-policy-v091",
            **values,
        )

    def _scope(self, *, external_approval=None, policy=None, **overrides):
        values = {
            "patch_bundle_digest": canonical_digest({"patches": ["repair-1"]}),
            "patch_count": 1,
            "source_commit_sha": getattr(self, "source_commit_sha", "a" * 40),
            "source_snapshot_digest": getattr(
                self,
                "source_snapshot_digest",
                canonical_digest({"snapshot": "source-v091"}),
            ),
            "allowed_paths": ("docs", "runtime"),
            "expected_changed_paths": ("runtime/repair.py",),
            "authorization_nonce": "nonce-v091-001",
            "issued_at_epoch_seconds": 1260,
            "expires_at_epoch_seconds": 1500,
        }
        values.update(overrides)
        return build_repository_application_scope(
            "application-scope-v091",
            self.external_approval if external_approval is None else external_approval,
            self.policy if policy is None else policy,
            **values,
        )

    def _observation(self, **overrides):
        values = {
            "repository_label": "KuuOS",
            "parent_commit_sha": "b" * 40,
            "current_commit_sha": self.scope.source_commit_sha,
            "current_parent_shas": ("b" * 40,),
            "changed_paths": ("README.md",),
            "inventory_paths": ("README.md", "runtime/repair.py"),
            "parent_snapshot_digest": canonical_digest({"snapshot": "parent"}),
            "current_snapshot_digest": self.scope.source_snapshot_digest,
            "object_database_read": True,
            "working_tree_read": False,
            "observation_digest": "",
        }
        values.update(overrides)
        observation = GitRevisionObservation(**values)
        return replace(
            observation,
            observation_digest=git_revision_observation_digest(observation),
        )

    def _source_state(self, *, observation=None, observed_at_epoch_seconds=1270):
        return build_repository_application_source_state_receipt(
            "source-state-v091",
            self._observation() if observation is None else observation,
            observed_at_epoch_seconds=observed_at_epoch_seconds,
        )

    def _nonce_status(
        self,
        *,
        scope=None,
        authority_id="nonce-authority-1",
        checked_at_epoch_seconds=1280,
        consumed=False,
        revoked=False,
    ):
        return build_repository_authorization_nonce_status_receipt(
            "nonce-status-v091",
            self.scope if scope is None else scope,
            authority_id=authority_id,
            checked_at_epoch_seconds=checked_at_epoch_seconds,
            registry_snapshot_digest=canonical_digest(
                {
                    "nonce_registry": "snapshot-1280",
                    "consumed": consumed,
                    "revoked": revoked,
                }
            ),
            consumed=consumed,
            revoked=revoked,
        )

    def _certify(self, **overrides):
        values = {
            "external_approval": self.external_approval,
            "policy": self.policy,
            "scope": self.scope,
            "source_state": self.source_state,
            "nonce_status": self.nonce_status,
            "evaluated_at_epoch_seconds": 1290,
        }
        values.update(overrides)
        return certify_repository_application_authorization(
            "application-authorization-v091",
            values["external_approval"],
            values["policy"],
            values["scope"],
            values["source_state"],
            values["nonce_status"],
            evaluated_at_epoch_seconds=values["evaluated_at_epoch_seconds"],
        )

    def test_valid_scope_grants_single_use_authorization_without_execution(self) -> None:
        certificate = self._certify()
        self.assertEqual(certificate.status, AUTHORIZATION_GRANTED)
        self.assertTrue(certificate.application_authorization_granted)
        self.assertTrue(certificate.single_use_application_eligible)
        self.assertFalse(certificate.patch_application_executed)
        self.assertFalse(certificate.commit_authority_granted)
        self.assertFalse(certificate.reference_mutation_authority_granted)
        self.assertEqual(
            repository_application_authorization_certificate_issues(certificate),
            (),
        )

    def test_consumed_nonce_is_certified_reject(self) -> None:
        certificate = self._certify(nonce_status=self._nonce_status(consumed=True))
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.nonce_unused)

    def test_revoked_nonce_is_certified_reject(self) -> None:
        certificate = self._certify(nonce_status=self._nonce_status(revoked=True))
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.nonce_not_revoked)

    def test_unauthorized_nonce_authority_is_certified_reject(self) -> None:
        certificate = self._certify(
            nonce_status=self._nonce_status(authority_id="nonce-authority-unknown")
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.nonce_authority_authorized)

    def test_stale_nonce_status_is_certified_reject(self) -> None:
        certificate = self._certify(evaluated_at_epoch_seconds=1320)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.nonce_status_fresh)

    def test_stale_source_observation_is_certified_reject(self) -> None:
        policy = self._policy(max_nonce_status_age_seconds=1000)
        scope = self._scope(policy=policy)
        source_state = self._source_state(observed_at_epoch_seconds=1270)
        nonce_status = self._nonce_status(scope=scope, checked_at_epoch_seconds=1390)
        certificate = self._certify(
            policy=policy,
            scope=scope,
            source_state=source_state,
            nonce_status=nonce_status,
            evaluated_at_epoch_seconds=1400,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.source_observation_fresh)

    def test_expired_authorization_is_certified_reject(self) -> None:
        scope = self._scope(expires_at_epoch_seconds=1285)
        certificate = self._certify(
            scope=scope,
            nonce_status=self._nonce_status(scope=scope),
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.authorization_not_expired)

    def test_authorization_lifetime_above_policy_is_certified_reject(self) -> None:
        scope = self._scope(expires_at_epoch_seconds=1600)
        certificate = self._certify(
            scope=scope,
            nonce_status=self._nonce_status(scope=scope),
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.authorization_lifetime_within_policy)

    def test_source_commit_drift_is_certified_reject(self) -> None:
        source_state = self._source_state(
            observation=self._observation(current_commit_sha="c" * 40)
        )
        certificate = self._certify(source_state=source_state)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.source_commit_unchanged)

    def test_source_snapshot_drift_is_certified_reject(self) -> None:
        source_state = self._source_state(
            observation=self._observation(
                current_snapshot_digest=canonical_digest("drifted-snapshot")
            )
        )
        certificate = self._certify(source_state=source_state)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.source_snapshot_unchanged)

    def test_non_object_database_source_is_certified_reject(self) -> None:
        source_state = self._source_state(
            observation=self._observation(object_database_read=False)
        )
        certificate = self._certify(source_state=source_state)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.object_database_source)

    def test_working_tree_observation_is_certified_reject(self) -> None:
        source_state = self._source_state(
            observation=self._observation(working_tree_read=True)
        )
        certificate = self._certify(source_state=source_state)
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.working_tree_ignored)

    def test_path_outside_allowed_scope_is_certified_reject(self) -> None:
        scope = self._scope(expected_changed_paths=("tests/repair.py",))
        certificate = self._certify(
            scope=scope,
            nonce_status=self._nonce_status(scope=scope),
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.expected_paths_within_allowed_scope)

    def test_protected_path_is_certified_reject(self) -> None:
        scope = self._scope(
            allowed_paths=("formal", "runtime"),
            expected_changed_paths=("formal/KUOS/Constitution.lean",),
        )
        certificate = self._certify(
            scope=scope,
            nonce_status=self._nonce_status(scope=scope),
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.protected_paths_excluded)

    def test_patch_count_above_policy_is_certified_reject(self) -> None:
        scope = self._scope(patch_count=5)
        certificate = self._certify(
            scope=scope,
            nonce_status=self._nonce_status(scope=scope),
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.patch_count_within_policy)

    def test_allowed_path_count_above_policy_is_certified_reject(self) -> None:
        policy = self._policy(max_allowed_path_count=1)
        scope = self._scope(policy=policy)
        certificate = self._certify(
            policy=policy,
            scope=scope,
            nonce_status=self._nonce_status(scope=scope),
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.path_count_within_policy)

    def test_delayed_reuse_of_external_approval_is_certified_reject(self) -> None:
        policy = self._policy(
            max_authorization_lifetime_seconds=100,
            max_source_observation_age_seconds=1000,
            max_nonce_status_age_seconds=1000,
        )
        scope = self._scope(
            policy=policy,
            issued_at_epoch_seconds=1400,
            expires_at_epoch_seconds=1490,
        )
        certificate = self._certify(
            policy=policy,
            scope=scope,
            source_state=self._source_state(observed_at_epoch_seconds=1410),
            nonce_status=self._nonce_status(
                scope=scope,
                checked_at_epoch_seconds=1420,
            ),
            evaluated_at_epoch_seconds=1430,
        )
        self.assertEqual(certificate.status, AUTHORIZATION_REJECTED)
        self.assertFalse(certificate.no_future_evidence)

    def test_rejected_external_approval_cannot_authorize(self) -> None:
        fixture = self.approval_fixture
        attestation = fixture._attestation(decision=DECISION_REJECT)
        verification = build_repository_signature_verification_receipt(
            "verification-rejected-v091",
            attestation,
            verifier_id="verifier-1",
            verified_at_epoch_seconds=1210,
            signature_verified=True,
        )
        revocation = build_repository_approval_revocation_status_receipt(
            "revocation-rejected-v091",
            attestation,
            fixture.policy,
            authority_id="revocation-authority-1",
            checked_at_epoch_seconds=1220,
            registry_snapshot_digest=canonical_digest("registry-rejected-v091"),
            revoked=False,
        )
        rejected_approval = fixture._certify(
            attestation=attestation,
            verification=verification,
            revocation=revocation,
        )
        scope = self._scope(external_approval=rejected_approval)
        with self.assertRaisesRegex(ValueError, "external_approval_not_accepted"):
            self._certify(
                external_approval=rejected_approval,
                scope=scope,
                nonce_status=self._nonce_status(scope=scope),
            )

    def test_scope_approval_binding_mismatch_fails_closed(self) -> None:
        scope = replace(
            self.scope,
            external_approval_certificate_digest="0" * 64,
            scope_digest="",
        )
        scope = replace(scope, scope_digest=repository_application_scope_digest(scope))
        with self.assertRaisesRegex(
            ValueError,
            "application_scope_external_approval_binding_mismatch",
        ):
            self._certify(
                scope=scope,
                nonce_status=self._nonce_status(scope=scope),
            )

    def test_nonce_scope_binding_mismatch_fails_closed(self) -> None:
        nonce_status = replace(
            self.nonce_status,
            authorization_scope_digest="0" * 64,
            receipt_digest="",
        )
        nonce_status = replace(
            nonce_status,
            receipt_digest=repository_authorization_nonce_status_receipt_digest(
                nonce_status
            ),
        )
        with self.assertRaisesRegex(ValueError, "nonce_status_scope_binding_mismatch"):
            self._certify(nonce_status=nonce_status)

    def test_tampered_source_state_receipt_fails_closed(self) -> None:
        tampered = replace(self.source_state, observed_at_epoch_seconds=1269)
        with self.assertRaisesRegex(
            ValueError,
            "application_source_state_receipt_invalid",
        ):
            self._certify(source_state=tampered)

    def test_policy_and_certificate_tamper_detection(self) -> None:
        self.assertEqual(
            repository_application_authorization_policy_issues(self.policy),
            (),
        )
        bad_policy = replace(self.policy, max_patch_count=1)
        self.assertIn(
            "authorization_policy_digest_mismatch",
            repository_application_authorization_policy_issues(bad_policy),
        )
        certificate = self._certify()
        bad_certificate = replace(certificate, patch_application_executed=True)
        issues = repository_application_authorization_certificate_issues(
            bad_certificate
        )
        self.assertIn("unexpected_patch_application_execution", issues)
        self.assertIn(
            "application_authorization_certificate_digest_mismatch",
            issues,
        )


if __name__ == "__main__":
    unittest.main()
