"""v0.58: branch-preserving LOCAL archive and independent replay tests."""
from __future__ import annotations

from copy import deepcopy
import json
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_lean_python_tagged_fork_archive_v0_58 as subject,
    kuuos_lean_python_detached_replay_witness_v0_54 as detached,
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA, ROUTES,
)
# Import the *module*, never expose its unittest.TestCase class as a module
# global: the native extension loader fails closed on duplicate test IDs.
from tests.lean_python_extensions import test_common_ancestor_fork_v0_56 as fork_fixture
from tests.lean_python_extensions.test_local_mac_bound_plan_claims_v0_52 import KEYS
from scripts import check_kuuos_lean_python_tagged_archive_sources_v0_58 as guard


class TaggedForkArchiveV058Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fork_fixture.CommonAncestorForkV056Tests.setUpClass()
        cls.helper = fork_fixture.CommonAncestorForkV056Tests(
            "test_six_native_routes_yield_local_fork_only"
        )

    def _fork(self, route="retain"):
        return self.helper._fork(route)

    def test_six_native_routes_preserve_both_fork_branches(self):
        for route, _, _, _ in ROUTES:
            with self.subTest(route=route):
                old, left, right = self._fork(route)
                record = subject.build_local_tagged_fork_archive(old, left, right)
                self.assertEqual(record.status, subject.ARCHIVED_FORK)
                self.assertTrue(record.both_branches_locally_retained)
                self.assertTrue(record.fork_obstruction_preserved)
                self.assertTrue(record.independently_recomputed_snapshots)
                self.assertEqual(record.archive["branches"][0]["tag"], "left")
                self.assertEqual(record.archive["branches"][1]["tag"], "right")
                self.assertEqual(record.archive["branches"][0]["snapshot"], left)
                self.assertEqual(record.archive["branches"][1]["snapshot"], right)
                self.assertEqual(record.archive["ancestor"], old)
                self.assertFalse(record.independent_archive_custody_authenticated)
                self.assertFalse(record.host_execution_authorized)
                self.assertIsNone(record.selected_successor)

    def test_detached_archive_rechecks_without_ledger(self):
        old, left, right = self._fork()
        build = subject.build_local_tagged_fork_archive(old, left, right)
        payload = json.loads(json.dumps(build.archive))
        checked = subject.verify_local_tagged_fork_archive(payload)
        self.assertEqual(checked.status, subject.ARCHIVED_FORK)
        self.assertEqual(checked.archive_sha256, build.archive_sha256)
        self.assertTrue(checked.fork_obstruction_preserved)
        self.assertFalse(checked.caller_archive_digest_value_matches)

    def test_external_archive_hash_value_matches_without_authentication(self):
        old, left, right = self._fork()
        build = subject.build_local_tagged_fork_archive(old, left, right)
        z = subject.verify_local_tagged_fork_archive(
            build.archive, separately_supplied_archive_sha256=build.archive_sha256,
        )
        self.assertEqual(z.status, subject.ARCHIVED_FORK)
        self.assertTrue(z.caller_archive_digest_value_matches)
        self.assertFalse(z.independent_archive_custody_authenticated)
        self.assertFalse(z.historical_branch_issuers_authenticated)
        self.assertFalse(z.global_descent_certified)

    def test_wrong_separate_archive_hash_preserves_obstruction(self):
        old, left, right = self._fork()
        build = subject.build_local_tagged_fork_archive(old, left, right)
        z = subject.verify_local_tagged_fork_archive(
            build.archive, separately_supplied_archive_sha256="f" * 64,
        )
        self.assertEqual(z.status, subject.ARCHIVE_DIGEST_MISMATCH)
        self.assertTrue(z.fork_obstruction_preserved)
        self.assertIn("caller_archive_digest_disagrees", z.issues)
        self.assertIsNone(z.selected_successor)

    def test_wrong_ancestor_checkpoint_retains_distinct_obstruction(self):
        old, left, right = self._fork()
        build = subject.build_local_tagged_fork_archive(
            old, left, right,
            separately_supplied_ancestor_checkpoint_sha256="f" * 64,
        )
        self.assertEqual(build.status, subject.ARCHIVED_FORK_AND_CHECKPOINT)
        self.assertTrue(build.fork_obstruction_preserved)
        self.assertIn("caller_prior_checkpoint_value_disagrees", build.issues)
        again = subject.verify_local_tagged_fork_archive(build.archive)
        self.assertEqual(again.status, subject.ARCHIVED_FORK_AND_CHECKPOINT)

    def test_matching_ancestor_checkpoint_does_not_erase_fork(self):
        old, left, right = self._fork()
        digest = detached.verify_detached_replay_witness(old).manifest_sha256
        build = subject.build_local_tagged_fork_archive(
            old, left, right,
            separately_supplied_ancestor_checkpoint_sha256=digest,
        )
        self.assertEqual(build.status, subject.ARCHIVED_FORK)
        self.assertTrue(build.caller_prior_checkpoint_value_matches)
        self.assertFalse(build.independent_archive_custody_authenticated)

    def test_comparable_descendants_remain_two_distinct_tags(self):
        old, left, right = self._fork()
        build = subject.build_local_tagged_fork_archive(old, left, deepcopy(left))
        self.assertEqual(build.status, subject.ARCHIVED_COMPARABLE)
        self.assertTrue(build.both_branches_locally_retained)
        self.assertFalse(build.fork_obstruction_preserved)
        self.assertEqual(build.archive["declared_relation"], "comparable")
        self.assertEqual(subject.verify_local_tagged_fork_archive(
            build.archive).status, subject.ARCHIVED_COMPARABLE)

    def test_swap_tags_and_order_rejected_on_independent_recheck(self):
        old, left, right = self._fork()
        build = subject.build_local_tagged_fork_archive(old, left, right)
        fake = deepcopy(build.archive)
        fake["branches"].reverse()
        self.assertEqual(
            subject.verify_local_tagged_fork_archive(fake).status, BLOCKED
        )
        fake = deepcopy(build.archive)
        fake["branches"][0]["tag"] = "right"
        self.assertEqual(
            subject.verify_local_tagged_fork_archive(fake).status, BLOCKED
        )

    def test_tampered_branch_manifest_is_not_recomputed_as_valid(self):
        old, left, right = self._fork()
        build = subject.build_local_tagged_fork_archive(old, left, right)
        fake = deepcopy(build.archive)
        fake["branches"][0]["snapshot"]["entries"][0]["row_sha256"] = "f" * 64
        self.assertEqual(
            subject.verify_local_tagged_fork_archive(fake).status, BLOCKED
        )

    def test_relation_renaming_does_not_change_actual_fork_status(self):
        old, left, right = self._fork()
        build = subject.build_local_tagged_fork_archive(old, left, right)
        fake = deepcopy(build.archive)
        fake["declared_relation"] = "comparable"
        self.assertEqual(
            subject.verify_local_tagged_fork_archive(fake).status, BLOCKED
        )

    def test_absent_or_invalid_inputs_fail_closed(self):
        old, left, right = self._fork()
        self.assertEqual(
            subject.build_local_tagged_fork_archive(None, left, right).status,
            NO_DATA,
        )
        self.assertEqual(
            subject.verify_local_tagged_fork_archive(None).status, NO_DATA,
        )
        self.assertEqual(
            subject.verify_local_tagged_fork_archive({"not": "archive"}).status,
            BLOCKED,
        )
        self.assertEqual(
            subject.build_local_tagged_fork_archive(old, left, []).status,
            BLOCKED,
        )

    def test_branch_not_extending_common_ancestor_is_obstruction(self):
        old, left, right = self._fork()
        z = subject.build_local_tagged_fork_archive(left, old, right)
        self.assertEqual(z.status, subject.ANCESTOR_OBSTRUCTION)
        self.assertIsNone(z.archive)

    def test_untrusted_archive_digest_shape_blocked(self):
        old, left, right = self._fork()
        build = subject.build_local_tagged_fork_archive(old, left, right)
        for bad in (False, 7, "", "F" * 64, "z" * 64, "0" * 63):
            with self.subTest(bad=bad):
                z = subject.verify_local_tagged_fork_archive(
                    build.archive, separately_supplied_archive_sha256=bad,
                )
                self.assertEqual(z.status, BLOCKED)

    def test_no_original_kernel_or_sqlite_access_during_archive_operations(self):
        old, left, right = self._fork()
        with patch.object(
            sqlite3, "connect", side_effect=AssertionError("unexpected SQLite"),
        ), patch.object(
            verify, "build_verifyos_middle_way_conditional_continuity_certificate",
            side_effect=AssertionError("unexpected VerifyOS"),
        ), patch.object(
            plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
            side_effect=AssertionError("unexpected PlanOS"),
        ):
            result = subject.build_local_tagged_fork_archive(old, left, right)
            checked = subject.verify_local_tagged_fork_archive(result.archive)
        self.assertEqual(checked.status, subject.ARCHIVED_FORK)
        self.assertEqual(checked.native_kernel_invocations, 0)

    def test_no_secrets_or_actual_os_result_sets_exported(self):
        old, left, right = self._fork()
        z = subject.build_local_tagged_fork_archive(old, left, right)
        encoded = json.dumps(z.archive, sort_keys=True).encode("ascii")
        for secret in KEYS.values():
            self.assertNotIn(secret, encoded)
        self.assertNotIn(b"mac_sha256", encoded)
        self.assertFalse(z.host_execution_authorized)
        self.assertEqual(z.original_plan_result_state, NO_DATA)

    def test_no_mutation_and_no_imported_testcase_leak(self):
        old, left, right = self._fork()
        original = deepcopy((old, left, right))
        subject.build_local_tagged_fork_archive(old, left, right)
        self.assertEqual((old, left, right), original)
        self.assertNotIn("CommonAncestorForkV056Tests", globals())
        self.assertTrue(hasattr(fork_fixture, "CommonAncestorForkV056Tests"))

    def test_source_guard_exact_blobs(self):
        self.assertEqual(guard.check(), ())

    def test_pinned_formal_v057_mutation_cannot_be_ignored(self):
        target = guard.ROOT / (
            "formal/KUOS/Architecture/LeanPythonLinearForkGluingObstructionV0_57.lean"
        )
        read = Path.read_bytes
        def tampered(path):
            raw = read(path)
            return raw + b"\n" if path == target else raw
        with patch.object(Path, "read_bytes", tampered):
            self.assertIn(
                "changed_pinned_source:formal/KUOS/Architecture/"
                "LeanPythonLinearForkGluingObstructionV0_57.lean",
                guard.check(),
            )


if __name__ == "__main__":
    unittest.main()
