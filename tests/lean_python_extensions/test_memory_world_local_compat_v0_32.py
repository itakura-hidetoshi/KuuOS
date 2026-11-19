"""v0.32 scoped MemoryOS↔WORLD source compatibility with true local WORLD.

The WORLD store comes from the ORIGINAL v0.34 committed temp store.
MemoryOS's upstream nonMarkov cognitive episode and blocker validators
are explicitly mocked per original MemoryOS fixture; the WORLD
validator is NOT mocked. NO external issuer or global Lean gluing proof.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

from runtime import kuuos_memoryos_qi_world_blocker_integration_v0_35 as memory
from runtime.kuuos_authorized_atomic_world_commit_entry_v0_34 import (
    make_initial_world_store,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_memory_world_local_compat_v0_32 import (
    audit_memory_world_compatibility,
    SCOPED_STORE, SCOPED_COMMIT, NO_DATA, BLOCKED,
)
from tests.test_authorized_atomic_world_commit_v0_34 import (
    AuthorizedAtomicWorldCommitV034Test,
)
from tests.test_memoryos_qi_world_blocker_integration_v0_35 import (
    MemoryOSQiWorldBlockerIntegrationV035Tests,
)


class NativeMemoryWorldLocalCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-memory-world-v032-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.world_fixture = AuthorizedAtomicWorldCommitV034Test(
            "test_atomic_commit_updates_pointer_and_appends_immutable_receipt")
        cls.disposition = cls.world_fixture.disposition_chain()
        cls.authorization = cls.world_fixture.authorization(cls.disposition)
        cls.request = cls.world_fixture.request(cls.disposition, cls.authorization)
        cls.path = cls.root / "world-store.json"
        cls.world_fixture.initialize_store(cls.path, cls.disposition)
        cls.result = cls.world_fixture.commit(
            cls.path, cls.disposition, cls.authorization, cls.request)
        if cls.result.status != "COMMITTED":
            raise AssertionError("native_world_v034_not_committed")
        cls.memory_fixture = MemoryOSQiWorldBlockerIntegrationV035Tests(
            "test_genesis_snapshot_preserves_three_contexts_without_authority")
        # The real native WORLD validator is used. Only upstream
        # episode and blocker providers are patched, hence no external
        # source authenticity is inferred for MemoryOS.
        with (
            patch.object(memory.memory_v023,
                         "validate_nonmarkov_cognitive_episode", return_value=[]),
            patch.object(memory.blocker_v15,
                         "validate_cross_cycle_blocker_certificate", return_value=[]),
        ):
            cls.snapshot = memory.build_memoryos_qi_world_blocker_snapshot(
                cognitive_episode=cls.memory_fixture.episode(),
                source_cross_cycle_receipt=cls.memory_fixture.source_receipt(),
                blocker_certificate=cls.memory_fixture.blocker_certificate(),
                world_store=cls.result.store,
                created_at_ms=3000,
            )
        cls.retrieval = memory.build_memoryos_conditioned_retrieval(
            snapshot=cls.snapshot, requested_capabilities=["read_context"],
            query_id="v032-source-query", created_at_ms=3001,
        )

    def check(self, *, full=False):
        extras = dict(
            source_disposition_envelope=self.disposition,
            authorization_envelope=self.authorization,
            request_envelope=self.request,
            recorded_commit_receipt_envelope=self.result.receipt,
        ) if full else {}
        return audit_memory_world_compatibility(
            self.snapshot, self.retrieval, self.result.store, **extras)

    def test_original_world_store_and_memory_snapshot_share_exact_source(self):
        x = self.check()
        self.assertEqual(x.status, SCOPED_STORE, x.issues)
        self.assertTrue(x.memory_native_validated)
        self.assertTrue(x.world_store_native_validated)
        self.assertTrue(x.same_exact_world_source_checked)
        self.assertFalse(x.original_world_commit_checked)
        self.assertEqual(self.snapshot["source_world_store_digest"],
                         self.result.store["body_digest"])

    def test_full_original_atomic_world_source_locally_matches_memory(self):
        x = self.check(full=True)
        self.assertEqual(x.status, SCOPED_COMMIT, x.issues)
        self.assertTrue(x.original_world_commit_checked)
        self.assertTrue(x.same_exact_world_source_checked)
        self.assertFalse(x.global_gluing_proved)
        self.assertFalse(x.formal_descent_certified)

    def test_local_compatibility_never_mutates_original_world_file(self):
        before = self.path.read_bytes()
        digest = _fingerprint([self.snapshot, self.retrieval,
                               self.result.store, self.result.receipt])
        self.assertEqual(self.check(full=True).status, SCOPED_COMMIT)
        self.assertEqual(before, self.path.read_bytes())
        self.assertEqual(digest, _fingerprint([
            self.snapshot, self.retrieval, self.result.store,
            self.result.receipt]))

    def test_missing_original_world_store_remains_no_data(self):
        r = audit_memory_world_compatibility(self.snapshot, self.retrieval, None)
        self.assertEqual(r.status, NO_DATA)
        self.assertFalse(r.formal_descent_certified)

    def test_missing_partial_atomic_source_is_no_data_not_global_cert(self):
        r = audit_memory_world_compatibility(
            self.snapshot, self.retrieval, self.result.store,
            authorization_envelope=self.authorization)
        self.assertEqual(r.status, NO_DATA, r.issues)
        self.assertTrue(r.same_exact_world_source_checked)
        self.assertFalse(r.original_world_commit_checked)

    def test_genesis_world_store_mismatches_committed_memory_projection(self):
        body = self.result.store["body"]
        other = make_initial_world_store(
            world_store_id=body["world_store_id"],
            root_lineage_digest=body["root_lineage_digest"],
            current_world_fragment_digest=body["genesis_world_fragment_digest"],
            created_at_ms=225,
        )
        r = audit_memory_world_compatibility(
            self.snapshot, self.retrieval, other)
        self.assertEqual(r.status, BLOCKED, r.issues)

    def test_memory_snapshot_wrong_world_root_blocks_before_projection(self):
        bad = deepcopy(self.snapshot)
        bad["world_context"]["root_lineage_digest"] = "0" * 64
        r = audit_memory_world_compatibility(
            bad, self.retrieval, self.result.store)
        self.assertEqual(r.status, BLOCKED, r.issues)

    def test_original_world_store_digest_tamper_is_blocked(self):
        bad = deepcopy(self.result.store)
        bad["body"]["current_world_fragment_digest"] = "f" * 64
        r = audit_memory_world_compatibility(
            self.snapshot, self.retrieval, bad)
        self.assertEqual(r.status, BLOCKED, r.issues)

    def test_world_commit_foreign_source_is_blocked(self):
        bad = deepcopy(self.request)
        bad["body"]["world_store_id"] = "forged-store"
        r = audit_memory_world_compatibility(
            self.snapshot, self.retrieval, self.result.store,
            source_disposition_envelope=self.disposition,
            authorization_envelope=self.authorization,
            request_envelope=bad,
            recorded_commit_receipt_envelope=self.result.receipt,
        )
        self.assertEqual(r.status, BLOCKED, r.issues)

    def test_even_two_local_native_successes_do_not_grant_descent_or_authority(self):
        r = self.check(full=True)
        self.assertEqual(r.status, SCOPED_COMMIT)
        for key in (
            "complete_external_issuer_authenticated",
            "memory_upstream_blocker_authenticated",
            "formal_descent_certified",
            "global_gluing_proved",
            "whole_program_lean_python_refinement_proved",
            "original_store_modified",
            "world_commit_performed_by_auditor",
            "execution_authority_granted",
            "truth_authority_granted",
            "root_rewrite_authority_granted",
            "history_delete_authority_granted",
        ):
            with self.subTest(field=key):
                self.assertFalse(getattr(r, key))


if __name__ == "__main__":
    unittest.main()
