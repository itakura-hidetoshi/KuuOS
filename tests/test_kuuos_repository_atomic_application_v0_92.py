from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_atomic_application_contracts_v0_92 import (
    build_repository_atomic_application_policy,
    build_repository_authorization_nonce_registry,
    build_repository_authorized_patch_bundle,
)
from runtime.kuuos_repository_atomic_application_receipt_v0_92 import (
    repository_atomic_application_receipt_issues,
    repository_nonce_consumption_receipt_issues,
)
from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    APPLICATION_ABORTED,
    APPLICATION_APPLIED,
    RepositoryAuthorizationNonceEntry,
    repository_atomic_application_receipt_digest,
    repository_authorization_nonce_registry_digest,
    repository_authorized_patch_bundle_digest,
)
from runtime.kuuos_repository_atomic_application_v0_92 import (
    apply_repository_authorized_patch_atomically,
)
from runtime.kuuos_repository_git_revision_types_v0_83 import (
    GitRevisionObservation,
    git_revision_observation_digest,
)
from runtime.kuuos_repository_structure_observer_v0_79 import (
    observe_repository_structure,
)
from runtime.kuuos_repository_structure_types_v0_79 import (
    RepositoryPatch,
    RepositorySnapshot,
)
from tests.kuuos_repository_repair_fixture_v0_79 import (
    defective_repository_snapshot,
)
from tests.test_kuuos_repository_application_authorization_v0_91 import (
    RepositoryApplicationAuthorizationV091Tests,
)


class RepositoryAtomicApplicationV092Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = self._source_snapshot()
        self.source_commit = "d" * 40
        self.patch = self._runtime_patch()
        self.bundle = build_repository_authorized_patch_bundle(
            "patch-bundle-v092",
            self.source,
            (self.patch,),
        )
        self.scope, self.authorization = self._authorization_for(self.bundle)
        self.policy = build_repository_atomic_application_policy(
            "atomic-application-policy-v092",
            authorized_executor_ids=("executor-1",),
            max_application_duration_seconds=60,
            max_patch_count=4,
            max_changed_path_count=4,
        )
        self.revision = self._revision()
        self.registry = self._registry()

    def _source_snapshot(self) -> RepositorySnapshot:
        snapshot = defective_repository_snapshot()
        texts = snapshot.texts
        texts[".github/workflows/fixture-v079.yml"] = (
            "name: fixture\n\non:\n  workflow_dispatch:\n\n"
            "permissions:\n  contents: read\n"
        )
        texts["formal/KuuOSFormal.lean"] = (
            "import KUOS\nimport KUOS.WORLD.FixtureV0_79\n"
        )
        texts["lakefile.toml"] = (
            "[[lean_lib]]\nname = \"KuuOSFormal\"\nroots = [\n"
            "  \"KuuOSFormal\",\n  \"FixtureFormalV0_79\"\n]\n"
        )
        source = RepositorySnapshot(
            snapshot.root_label,
            snapshot.all_paths,
            tuple(sorted(texts.items())),
        )
        self.assertEqual(observe_repository_structure(source).weighted_defect_score, 20)
        return source

    def _runtime_patch(self, *, after_text: str | None = None, before_digest=None):
        path = "scripts/run_kuuos_runtime_full_check_v0_55.py"
        before = self.source.texts[path]
        after = after_text or (
            "VALIDATORS_AFTER_V055: tuple[str, ...] = (\n"
            "    \"scripts/check_fixture_v079.py\",\n"
            ")\n\n\ndef _runtime_environment():\n    return {}\n"
        )
        return RepositoryPatch(
            path=path,
            before_digest=canonical_digest(before)
            if before_digest is None
            else before_digest,
            after_text=after,
            repair_kind="authorized_runtime_registration_v0_92",
            reason="register the manifest-declared validator",
        )

    def _authorization_for(self, bundle, *, nonce="nonce-v092-001"):
        fixture = RepositoryApplicationAuthorizationV091Tests(
            methodName=(
                "test_valid_scope_grants_single_use_authorization_without_execution"
            )
        )
        fixture.setUp()
        fixture.source_commit_sha = self.source_commit
        fixture.source_snapshot_digest = self.source.digest
        expected_paths = tuple(patch.path for patch in bundle.patches)
        scope = fixture._scope(
            patch_bundle_digest=bundle.bundle_digest,
            patch_count=len(bundle.patches),
            source_commit_sha=self.source_commit,
            source_snapshot_digest=self.source.digest,
            allowed_paths=("scripts",),
            expected_changed_paths=expected_paths,
            authorization_nonce=nonce,
            issued_at_epoch_seconds=1260,
            expires_at_epoch_seconds=1500,
        )
        fixture.scope = scope
        source_state = fixture._source_state(
            observation=fixture._observation(
                current_commit_sha=self.source_commit,
                current_snapshot_digest=self.source.digest,
                inventory_paths=self.source.all_paths,
            )
        )
        nonce_status = fixture._nonce_status(scope=scope)
        authorization = fixture._certify(
            scope=scope,
            source_state=source_state,
            nonce_status=nonce_status,
            evaluated_at_epoch_seconds=1290,
        )
        return scope, authorization

    def _revision(self, **overrides):
        values = {
            "repository_label": "KuuOS-v092-fixture",
            "parent_commit_sha": "c" * 40,
            "current_commit_sha": self.source_commit,
            "current_parent_shas": ("c" * 40,),
            "changed_paths": (),
            "inventory_paths": self.source.all_paths,
            "parent_snapshot_digest": canonical_digest("parent-v092"),
            "current_snapshot_digest": self.source.digest,
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

    def _registry(self, *, consumed=False, revoked=False, scope=None):
        bound_scope = self.scope if scope is None else scope
        return build_repository_authorization_nonce_registry(
            "nonce-registry-v092",
            (
                RepositoryAuthorizationNonceEntry(
                    authorization_nonce=bound_scope.authorization_nonce,
                    authorization_scope_digest=bound_scope.scope_digest,
                    consumed=consumed,
                    revoked=revoked,
                ),
            ),
        )

    def _apply(self, **overrides):
        values = {
            "authorization": self.authorization,
            "scope": self.scope,
            "policy": self.policy,
            "patch_bundle": self.bundle,
            "source_revision": self.revision,
            "source_snapshot": self.source,
            "nonce_registry": self.registry,
            "executor_id": "executor-1",
            "started_at_epoch_seconds": 1300,
            "completed_at_epoch_seconds": 1310,
        }
        values.update(overrides)
        return apply_repository_authorized_patch_atomically(
            "atomic-application-v092",
            values["authorization"],
            values["scope"],
            values["policy"],
            values["patch_bundle"],
            values["source_revision"],
            values["source_snapshot"],
            values["nonce_registry"],
            executor_id=values["executor_id"],
            started_at_epoch_seconds=values["started_at_epoch_seconds"],
            completed_at_epoch_seconds=values["completed_at_epoch_seconds"],
        )

    def test_success_commits_snapshot_and_nonce_together(self) -> None:
        final, registry, receipt, nonce_receipt, rollback = self._apply()
        self.assertEqual(receipt.status, APPLICATION_APPLIED)
        self.assertEqual(observe_repository_structure(final).weighted_defect_score, 0)
        self.assertNotEqual(final.digest, self.source.digest)
        self.assertNotEqual(registry.registry_digest, self.registry.registry_digest)
        self.assertTrue(registry.entries[0].consumed)
        self.assertTrue(receipt.application_effect_committed)
        self.assertTrue(receipt.nonce_consumption_committed)
        self.assertTrue(receipt.atomic_state_transition)
        self.assertTrue(receipt.rollback_material_exact)
        self.assertFalse(receipt.live_repository_write_performed)
        self.assertFalse(receipt.commit_created)
        self.assertFalse(receipt.reference_mutated)
        self.assertEqual(repository_atomic_application_receipt_issues(receipt), ())
        self.assertEqual(repository_nonce_consumption_receipt_issues(nonce_receipt), ())
        self.assertEqual(rollback.source_snapshot_digest, self.source.digest)

    def test_replay_with_used_nonce_aborts_without_effect(self) -> None:
        _, used_registry, _, _, _ = self._apply()
        final, registry, receipt, nonce_receipt, _ = self._apply(
            nonce_registry=used_registry
        )
        self.assertEqual(receipt.status, APPLICATION_ABORTED)
        self.assertFalse(receipt.nonce_unused_before)
        self.assertTrue(receipt.failure_no_effect)
        self.assertEqual(final.digest, self.source.digest)
        self.assertEqual(registry.registry_digest, used_registry.registry_digest)
        self.assertFalse(nonce_receipt.application_committed)

    def test_revoked_nonce_aborts_without_effect(self) -> None:
        final, registry, receipt, _, _ = self._apply(
            nonce_registry=self._registry(revoked=True)
        )
        self.assertEqual(receipt.status, APPLICATION_ABORTED)
        self.assertFalse(receipt.nonce_not_revoked)
        self.assertEqual(final.digest, self.source.digest)
        self.assertEqual(registry.registry_digest, self._registry(revoked=True).registry_digest)

    def test_source_commit_drift_aborts_without_effect(self) -> None:
        final, registry, receipt, _, _ = self._apply(
            source_revision=self._revision(current_commit_sha="e" * 40)
        )
        self.assertEqual(receipt.status, APPLICATION_ABORTED)
        self.assertFalse(receipt.source_commit_unchanged)
        self.assertEqual(final.digest, self.source.digest)
        self.assertEqual(registry.registry_digest, self.registry.registry_digest)

    def test_source_snapshot_drift_aborts_without_effect(self) -> None:
        final, _, receipt, _, _ = self._apply(
            source_revision=self._revision(
                current_snapshot_digest=canonical_digest("drifted-v092")
            )
        )
        self.assertEqual(receipt.status, APPLICATION_ABORTED)
        self.assertFalse(receipt.source_snapshot_unchanged)
        self.assertEqual(final.digest, self.source.digest)

    def test_working_tree_source_aborts_without_effect(self) -> None:
        final, _, receipt, _, _ = self._apply(
            source_revision=self._revision(working_tree_read=True)
        )
        self.assertEqual(receipt.status, APPLICATION_ABORTED)
        self.assertFalse(receipt.working_tree_ignored)
        self.assertEqual(final.digest, self.source.digest)

    def test_non_object_database_source_aborts_without_effect(self) -> None:
        final, _, receipt, _, _ = self._apply(
            source_revision=self._revision(object_database_read=False)
        )
        self.assertEqual(receipt.status, APPLICATION_ABORTED)
        self.assertFalse(receipt.object_database_source)
        self.assertEqual(final.digest, self.source.digest)

    def test_unauthorized_executor_aborts_without_effect(self) -> None:
        final, _, receipt, _, _ = self._apply(executor_id="executor-unknown")
        self.assertEqual(receipt.status, APPLICATION_ABORTED)
        self.assertFalse(receipt.executor_authorized)
        self.assertEqual(final.digest, self.source.digest)

    def test_expired_authorization_aborts_without_effect(self) -> None:
        final, _, receipt, _, _ = self._apply(
            started_at_epoch_seconds=1490,
            completed_at_epoch_seconds=1500,
        )
        self.assertEqual(receipt.status, APPLICATION_ABORTED)
        self.assertFalse(receipt.authorization_not_expired_at_completion)
        self.assertEqual(final.digest, self.source.digest)

    def test_excess_duration_aborts_without_effect(self) -> None:
        final, _, receipt, _, _ = self._apply(
            started_at_epoch_seconds=1300,
            completed_at_epoch_seconds=1400,
        )
        self.assertEqual(receipt.status, APPLICATION_ABORTED)
        self.assertFalse(receipt.duration_within_policy)
        self.assertEqual(final.digest, self.source.digest)

    def test_before_digest_mismatch_aborts_without_effect(self) -> None:
        bad_bundle = build_repository_authorized_patch_bundle(
            "bad-before-v092",
            self.source,
            (self._runtime_patch(before_digest="0" * 64),),
        )
        scope, authorization = self._authorization_for(bad_bundle)
        final, registry, receipt, _, _ = self._apply(
            authorization=authorization,
            scope=scope,
            patch_bundle=bad_bundle,
            nonce_registry=self._registry(scope=scope),
        )
        self.assertEqual(receipt.status, APPLICATION_ABORTED)
        self.assertFalse(receipt.patch_before_digests_exact)
        self.assertEqual(final.digest, self.source.digest)
        self.assertEqual(registry.registry_digest, self._registry(scope=scope).registry_digest)

    def test_non_normal_result_aborts_after_isolated_evaluation(self) -> None:
        unchanged_defect_text = self.source.texts[
            "scripts/run_kuuos_runtime_full_check_v0_55.py"
        ] + "\n# unrelated text\n"
        bundle = build_repository_authorized_patch_bundle(
            "non-normal-v092",
            self.source,
            (self._runtime_patch(after_text=unchanged_defect_text),),
        )
        scope, authorization = self._authorization_for(bundle)
        final, registry, receipt, _, rollback = self._apply(
            authorization=authorization,
            scope=scope,
            patch_bundle=bundle,
            nonce_registry=self._registry(scope=scope),
        )
        self.assertEqual(receipt.status, APPLICATION_ABORTED)
        self.assertFalse(receipt.result_normal_form_certified)
        self.assertTrue(receipt.rollback_material_exact)
        self.assertEqual(final.digest, self.source.digest)
        self.assertEqual(registry.registry_digest, self._registry(scope=scope).registry_digest)
        self.assertNotEqual(rollback.candidate_snapshot_digest, self.source.digest)

    def test_patch_bundle_tamper_fails_closed(self) -> None:
        tampered = replace(self.bundle, bundle_id="tampered-v092")
        with self.assertRaisesRegex(ValueError, "authorized_patch_bundle_invalid"):
            self._apply(patch_bundle=tampered)

    def test_nonce_registry_tamper_fails_closed(self) -> None:
        tampered = replace(self.registry, registry_digest="0" * 64)
        with self.assertRaisesRegex(ValueError, "authorization_nonce_registry_invalid"):
            self._apply(nonce_registry=tampered)

    def test_source_revision_tamper_fails_closed(self) -> None:
        tampered = replace(self.revision, current_commit_sha="f" * 40)
        with self.assertRaisesRegex(
            ValueError,
            "atomic_application_source_revision_digest_mismatch",
        ):
            self._apply(source_revision=tampered)

    def test_receipt_tamper_detection(self) -> None:
        _, _, receipt, _, _ = self._apply()
        tampered = replace(
            receipt,
            commit_created=True,
            receipt_digest="",
        )
        tampered = replace(
            tampered,
            receipt_digest=repository_atomic_application_receipt_digest(tampered),
        )
        self.assertIn(
            "atomic_application_unexpected_commit",
            repository_atomic_application_receipt_issues(tampered),
        )

    def test_registry_builder_tamper_detection(self) -> None:
        tampered = replace(self.registry, registry_id="changed")
        self.assertNotEqual(
            tampered.registry_digest,
            repository_authorization_nonce_registry_digest(tampered),
        )

    def test_bundle_builder_tamper_detection(self) -> None:
        tampered = replace(self.bundle, bundle_id="changed")
        self.assertNotEqual(
            tampered.bundle_digest,
            repository_authorized_patch_bundle_digest(tampered),
        )


if __name__ == "__main__":
    unittest.main()
