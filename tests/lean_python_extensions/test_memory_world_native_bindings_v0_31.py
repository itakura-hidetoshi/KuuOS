"""Native MemoryOS and WORLD v0.35/v0.34 source-bound Lean data tests.

MemoryOS upstream source fixtures explicitly mock external validators, so
these tests certify only the ORIGINAL MemoryOS snapshot/retrieval kernel
and source-local conditions, NOT external source authentication.

WORLD uses the existing original full v0.34 source disposition,
authorization, request, persisted atomic commit and stored receipt in
an isolated temporary local file. No mock successful WORLD validators.
No original WORLD kernel is edited by these additive tests.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime import kuuos_memoryos_qi_world_blocker_integration_v0_35 as memory_native
from runtime.kuuos_authorized_atomic_world_commit_entry_v0_34 import read_world_store
from runtime.kuuos_lean_python_memory_world_native_v0_31 import PASS, NO_DATA, BLOCKED
from runtime.kuuos_lean_python_memory_native_binding_v0_31 import (
    audit_native_memory_blocker,
)
from runtime.kuuos_lean_python_world_native_binding_v0_31 import (
    audit_original_world_commit,
)
from tests.test_memoryos_qi_world_blocker_integration_v0_35 import (
    MemoryOSQiWorldBlockerIntegrationV035Tests,
)
from tests.test_authorized_atomic_world_commit_v0_34 import (
    AuthorizedAtomicWorldCommitV034Test,
)


class NativeMemoryWorldSourceBindingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temp = TemporaryDirectory(prefix="kuuos-lean-python-v031-native-")
        cls.addClassCleanup(cls._temp.cleanup)
        cls.root = Path(cls._temp.name)
        # This helper *mocks upstream sources* exactly as in original
        # unit tests; the resulting MemoryOS snapshot is native.
        cls.mem_fixture = MemoryOSQiWorldBlockerIntegrationV035Tests(
            "test_genesis_snapshot_preserves_three_contexts_without_authority")
        cls.memory = cls.mem_fixture.build_snapshot()
        cls.retrieval = memory_native.build_memoryos_conditioned_retrieval(
            snapshot=cls.memory,
            requested_capabilities=["read_context"],
            query_id="v031-query",
            created_at_ms=2000,
        )
        cls.world_fixture = AuthorizedAtomicWorldCommitV034Test(
            "test_atomic_commit_updates_pointer_and_appends_immutable_receipt")
        cls.disposition = cls.world_fixture.disposition_chain()
        cls.authorization = cls.world_fixture.authorization(cls.disposition)
        cls.request = cls.world_fixture.request(cls.disposition, cls.authorization)
        cls.world_path = cls.root / "world-store.json"
        cls.world_fixture.initialize_store(cls.world_path, cls.disposition)
        cls.committed = cls.world_fixture.commit(
            cls.world_path, cls.disposition, cls.authorization, cls.request)
        if cls.committed.status != "COMMITTED":
            raise AssertionError("original_world_native_source_not_committed")

    def world_check(self):
        return audit_original_world_commit(
            self.disposition, self.authorization, self.request,
            self.committed.receipt, self.committed.store,
        )

    def test_original_memoryos_snapshots_are_source_bound_locally(self):
        report = audit_native_memory_blocker(self.memory, self.retrieval)
        self.assertEqual(report.status, PASS, report.issues)
        self.assertTrue(report.local_native_validator_passed)
        self.assertTrue(report.lean_selected_data_conditions_checked)
        self.assertIn("MemoryOS.snapshot.blocker_context.active_blockers",
                      report.checked_source_field_paths)
        self.assertFalse(report.nested_lean_proof_structures_constructed)

    def test_original_memory_retrieval_is_pure_read_only(self):
        before = _fingerprint([self.memory, self.retrieval])
        report = audit_native_memory_blocker(self.memory, self.retrieval)
        self.assertEqual(report.status, PASS, report.issues)
        self.assertEqual(before, _fingerprint([self.memory, self.retrieval]))
        self.assertFalse(report.original_source_mutated)

    def test_original_memoryos_incomplete_blocker_remains_no_data(self):
        incomplete = self.mem_fixture.build_snapshot(complete=False)
        retrieve = memory_native.build_memoryos_conditioned_retrieval(
            snapshot=incomplete, requested_capabilities=["read_context"],
            query_id="v031-incomplete", created_at_ms=2001)
        result = audit_native_memory_blocker(incomplete, retrieve)
        self.assertEqual(result.status, NO_DATA, result.issues)
        self.assertFalse(result.lean_selected_data_conditions_checked)

    def test_missing_snapshot_or_retrieval_never_claims_certification(self):
        self.assertEqual(audit_native_memory_blocker(
            None, self.retrieval).status, NO_DATA)
        self.assertEqual(audit_native_memory_blocker(
            self.memory, None).status, NO_DATA)

    def test_wrong_retrieval_snapshot_binding_blocks(self):
        altered = deepcopy(self.retrieval)
        altered["source_memory_snapshot_digest"] = "forged"
        self.assertEqual(audit_native_memory_blocker(
            self.memory, altered).status, BLOCKED)

    def test_memory_cannot_silently_discharge_blocker(self):
        altered = deepcopy(self.memory)
        altered["blocker_context"]["memory_may_discharge_blocker"] = True
        self.assertEqual(audit_native_memory_blocker(
            altered, self.retrieval).status, BLOCKED)

    def test_memory_world_write_claim_is_not_permitted(self):
        altered = deepcopy(self.memory)
        altered["world_context"]["memory_may_commit_world"] = True
        self.assertEqual(audit_native_memory_blocker(
            altered, self.retrieval).status, BLOCKED)

    def test_original_world_persisted_commit_binds_lean_data_conditions(self):
        report = self.world_check()
        self.assertEqual(report.status, PASS, report.issues)
        self.assertTrue(report.local_native_validator_passed)
        self.assertTrue(report.lean_selected_data_conditions_checked)
        self.assertIn("WORLD.store.body.commits[-1].body_digest",
                      report.checked_source_field_paths)
        self.assertFalse(report.new_world_commit_performed)

    def test_original_world_audit_is_purely_read_only(self):
        before = self.world_path.read_bytes()
        fingerprint = _fingerprint([
            self.disposition, self.authorization, self.request,
            self.committed.receipt, self.committed.store,
        ])
        result = self.world_check()
        self.assertEqual(result.status, PASS, result.issues)
        self.assertEqual(before, self.world_path.read_bytes())
        self.assertEqual(fingerprint, _fingerprint([
            self.disposition, self.authorization, self.request,
            self.committed.receipt, self.committed.store,
        ]))

    def test_original_world_missing_persisted_commit_is_no_data(self):
        self.assertEqual(audit_original_world_commit(
            self.disposition, self.authorization, self.request,
            self.committed.receipt, None).status, NO_DATA)

    def test_wrong_authorization_source_digest_is_blocked(self):
        altered = deepcopy(self.authorization)
        altered["body"]["source_disposition_digest"] = "0" * 64
        self.assertEqual(audit_original_world_commit(
            self.disposition, altered, self.request,
            self.committed.receipt, self.committed.store).status, BLOCKED)

    def test_world_tampered_immutable_commit_receipt_fails(self):
        altered = deepcopy(self.committed.receipt)
        altered["body"]["append_only_history_preserved"] = False
        self.assertEqual(audit_original_world_commit(
            self.disposition, self.authorization, self.request,
            altered, self.committed.store).status, BLOCKED)

    def test_world_commit_incompatible_store_is_rejected(self):
        altered = deepcopy(self.committed.store)
        altered["body"]["root_lineage_digest"] = "f" * 64
        self.assertEqual(audit_original_world_commit(
            self.disposition, self.authorization, self.request,
            self.committed.receipt, altered).status, BLOCKED)

    def test_world_source_after_original_replay_is_still_single_commit(self):
        original = self.world_path.read_bytes()
        replay = self.world_fixture.commit(
            self.world_path, self.disposition, self.authorization,
            self.request, committed_at_ms=999)
        self.assertEqual(replay.status, "REPLAYED")
        self.assertEqual(original, self.world_path.read_bytes())
        self.assertEqual(self.world_check().status, PASS)

    def test_memory_and_world_success_do_not_establish_global_gluing(self):
        for report in (
            audit_native_memory_blocker(self.memory, self.retrieval),
            self.world_check(),
        ):
            self.assertEqual(report.status, PASS, report.issues)
            for key in ("nested_lean_proof_structures_constructed",
                        "complete_lean_python_semantic_refinement",
                        "external_source_issuer_authenticated",
                        "external_blocker_certificate_authenticated",
                        "external_authorization_issuer_authenticated",
                        "new_world_commit_performed",
                        "original_source_mutated",
                        "truth_authority_granted",
                        "execution_authority_granted",
                        "git_authority_granted"):
                with self.subTest(os=report.os_name, field=key):
                    self.assertFalse(getattr(report, key))


if __name__ == "__main__":
    unittest.main()
