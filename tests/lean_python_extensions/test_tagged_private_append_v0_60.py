"""v0.60: private branch appends preserve tagged overlap (or obstruction)."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_lean_python_tagged_private_append_v0_60 as subject,
    kuuos_lean_python_tagged_fork_archive_v0_58 as tagged,
    kuuos_lean_python_tagged_span_gluing_v0_59 as glued,
    kuuos_lean_python_detached_replay_witness_v0_54 as detached,
    kuuos_lean_python_local_replay_reservation_v0_53 as replay,
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA, ROUTES,
)
# Prior TestCase imported as module alias only; direct class import causes
# duplicate_extension_test_id in the original native unittest discovery.
from tests.lean_python_extensions import test_common_ancestor_fork_v0_56 as fixture
from scripts import check_kuuos_lean_python_private_append_sources_v0_60 as guard


class TaggedPrivateAppendV060Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.CommonAncestorForkV056Tests.setUpClass()
        cls.helper = fixture.CommonAncestorForkV056Tests(
            "test_six_native_routes_yield_local_fork_only"
        )

    @staticmethod
    def _pair_seq(n):
        return {"first": n, "second": n + 1}

    @staticmethod
    def _pair_nonce(n):
        return {
            "first": f"{1000 + n:032x}",
            "second": f"{2000 + n:032x}",
        }

    def _snapshots(self, route="retain", *, extend_left=True, extend_right=True,
                   checkpoint=None):
        """Create actual v0.53 SQLite local reservations before offline audit."""
        with TemporaryDirectory() as folder:
            root = Path(folder)
            ancestor_db = root / "ancestor.sqlite"
            left_db = root / "left.sqlite"
            right_db = root / "right.sqlite"
            self.helper._commit(ancestor_db, route)
            common = self.helper._manifest(ancestor_db)
            shutil.copyfile(ancestor_db, left_db)
            shutil.copyfile(ancestor_db, right_db)
            self.helper._commit(left_db, route, seq=self._pair_seq(9),
                                nonce=self._pair_nonce(9))
            self.helper._commit(right_db, route, seq=self._pair_seq(11),
                                nonce=self._pair_nonce(11))
            old_left, old_right = (self.helper._manifest(left_db),
                                   self.helper._manifest(right_db))
            older = tagged.build_local_tagged_fork_archive(
                common, old_left, old_right,
                separately_supplied_ancestor_checkpoint_sha256=checkpoint,
            )
            self.assertIsNotNone(older.archive, older)
            if extend_left:
                self.helper._commit(left_db, route, seq=self._pair_seq(13),
                                    nonce=self._pair_nonce(13))
            if extend_right:
                self.helper._commit(right_db, route, seq=self._pair_seq(15),
                                    nonce=self._pair_nonce(15))
            newer = tagged.build_local_tagged_fork_archive(
                common, self.helper._manifest(left_db),
                self.helper._manifest(right_db),
                separately_supplied_ancestor_checkpoint_sha256=checkpoint,
            )
            self.assertIsNotNone(newer.archive, newer)
            n = len(common["entries"])
            lv = [f"ancestor-{i}" for i in range(n)]
            rv = list(lv)
            lv += [f"left-{i}" for i in range(len(old_left["entries"]) - n)]
            rv += [f"right-{i}" for i in range(len(old_right["entries"]) - n)]
            new_lv = list(lv)
            new_rv = list(rv)
            new_lv.extend(f"new-left-{i}" for i in
                          range(len(newer.archive["branches"][0]["snapshot"]["entries"])
                                - len(old_left["entries"])))
            new_rv.extend(f"new-right-{i}" for i in
                          range(len(newer.archive["branches"][1]["snapshot"]["entries"])
                                - len(old_right["entries"])))
            return older.archive, newer.archive, lv, rv, new_lv, new_rv

    def _audit(self, data, **opts):
        return subject.audit_tagged_private_append(*data, **opts)

    def test_six_native_routes_preserve_gluing_under_actual_branch_appends(self):
        for route, _, _, _ in ROUTES:
            with self.subTest(route=route):
                parts = self._snapshots(route)
                z = self._audit(parts)
                self.assertEqual(z.status, subject.PRESERVED_COMPATIBILITY)
                self.assertTrue(z.preserved_exact_ancestor)
                self.assertTrue(z.all_old_rows_and_annotations_preserved)
                self.assertTrue(z.overlap_status_invariant_verified)
                self.assertTrue(z.old_overlap_compatible)
                self.assertTrue(z.new_overlap_compatible)
                self.assertTrue(z.old_fork_obstruction_preserved)
                self.assertEqual((z.appended_left_rows, z.appended_right_rows),
                                 (2, 2))
                self.assertIsNotNone(z.newly_glued)
                self.assertFalse(z.linear_history_descended)
                self.assertFalse(z.global_descent_certified)
                self.assertFalse(z.host_execution_authorized)
                self.assertIsNone(z.selected_successor)

    def test_old_mismatch_persists_at_exact_shared_index(self):
        parts = list(self._snapshots())
        parts[3][0] = "right-conflict"
        parts[5][0] = "right-conflict"
        z = self._audit(parts)
        self.assertEqual(z.status, subject.PRESERVED_MISMATCH)
        self.assertEqual(z.mismatch_indices, (0,))
        self.assertFalse(z.old_overlap_compatible)
        self.assertFalse(z.new_overlap_compatible)
        self.assertTrue(z.overlap_status_invariant_verified)
        self.assertIsNone(z.newly_glued)
        self.assertIn("retained_shared_observation_mismatch:0", z.issues)

    def test_two_old_mismatches_are_not_dropped_by_new_private_rows(self):
        parts = list(self._snapshots())
        for idx in (0, 1):
            parts[3][idx] = "conflict-" + str(idx)
            parts[5][idx] = "conflict-" + str(idx)
        z = self._audit(parts)
        self.assertEqual(z.mismatch_indices, (0, 1))
        self.assertEqual(z.status, subject.PRESERVED_MISMATCH)
        self.assertFalse(z.new_overlap_compatible)

    def test_mismatch_cannot_be_cleared_by_rewriting_new_shared_values(self):
        parts = list(self._snapshots())
        parts[3][0] = "disagrees"
        parts[5][0] = parts[2][0]
        z = self._audit(parts)
        self.assertEqual(z.status, subject.OBSERVATION_REWRITE)
        self.assertFalse(z.overlap_status_invariant_verified)
        self.assertIn("old_shared_or_private_observation_changed", z.issues)

    def test_old_private_annotation_rewrite_is_not_certified(self):
        parts = list(self._snapshots())
        n = len(parts[0]["ancestor"]["entries"])
        parts[4][n] = "new-meaning-of-old-left-row"
        z = self._audit(parts)
        self.assertEqual(z.status, subject.OBSERVATION_REWRITE)
        self.assertFalse(z.all_old_rows_and_annotations_preserved)

    def test_right_private_append_only_is_supported(self):
        parts = self._snapshots(extend_left=False)
        z = self._audit(parts)
        self.assertEqual(z.status, subject.PRESERVED_COMPATIBILITY)
        self.assertEqual((z.appended_left_rows, z.appended_right_rows), (0, 2))
        self.assertTrue(z.overlap_status_invariant_verified)

    def test_left_private_append_only_is_supported(self):
        parts = self._snapshots(extend_right=False)
        z = self._audit(parts)
        self.assertEqual(z.status, subject.PRESERVED_COMPATIBILITY)
        self.assertEqual((z.appended_left_rows, z.appended_right_rows), (2, 0))

    def test_zero_extension_is_an_obstruction_not_silent_success(self):
        parts = self._snapshots(extend_left=False, extend_right=False)
        z = self._audit(parts)
        self.assertEqual(z.status, subject.NO_NEW_PRIVATE_ROWS)
        self.assertFalse(z.overlap_status_invariant_verified)

    def test_matching_old_archive_digest_value_is_only_a_value_check(self):
        parts = self._snapshots()
        digest = tagged.verify_local_tagged_fork_archive(parts[0]).archive_sha256
        z = self._audit(parts, separately_supplied_old_archive_sha256=digest)
        self.assertEqual(z.status, subject.PRESERVED_COMPATIBILITY)
        self.assertTrue(z.caller_old_archive_value_matches)
        self.assertFalse(z.independent_custody_authenticated)

    def test_wrong_old_archive_digest_value_and_shared_mismatch_both_survive(self):
        parts = list(self._snapshots())
        parts[3][1] = "difference"
        parts[5][1] = "difference"
        z = self._audit(parts, separately_supplied_old_archive_sha256="f" * 64)
        self.assertEqual(z.status, subject.PRESERVED_MULTIPLE_OBSTRUCTIONS)
        self.assertIn("retained_shared_observation_mismatch:1", z.issues)
        self.assertIn("caller_old_archive_digest_disagrees", z.issues)

    def test_wrong_prior_checkpoint_value_is_not_erased_by_compatible_gluing(self):
        parts = self._snapshots(checkpoint="f" * 64)
        z = self._audit(parts)
        self.assertEqual(z.status, subject.PRESERVED_COMPATIBILITY_WITH_CHECKPOINT)
        self.assertTrue(z.new_overlap_compatible)
        self.assertIsNotNone(z.newly_glued)
        self.assertIn("caller_prior_checkpoint_value_disagrees", z.issues)
        self.assertFalse(z.host_execution_authorized)

    def test_new_ancestor_or_checkpoint_claim_cannot_be_substituted(self):
        parts = list(self._snapshots())
        fake = deepcopy(parts[1])
        fake["prior_checkpoint_sha256"] = "f" * 64
        parts[1] = fake
        z = self._audit(parts)
        self.assertEqual(z.status, subject.ANCESTOR_CHANGE)
        self.assertIn("prior_checkpoint_value_was_replaced", z.issues)

    def test_resealed_rewrite_of_old_private_row_fails_prefix(self):
        parts = list(self._snapshots())
        fake = deepcopy(parts[1])
        old_common = len(parts[0]["ancestor"]["entries"])
        rows = fake["branches"][0]["snapshot"]["entries"]
        rows[old_common]["message_sha256"] = "a" * 64
        prev = rows[old_common-1]["row_sha256"]
        for row in rows[old_common:]:
            row["previous_row_sha256"] = prev
            row["row_sha256"] = replay._hash_row(
                prev, row["key_id"], row["context_id"], row["sequence"],
                row["nonce_hex"], row["message_sha256"],
            )
            prev = row["row_sha256"]
        fake["branches"][0]["snapshot"]["declared_chain_head"] = prev
        rechecked = tagged.build_local_tagged_fork_archive(
            fake["ancestor"], fake["branches"][0]["snapshot"],
            fake["branches"][1]["snapshot"],
        )
        self.assertIsNotNone(rechecked.archive, rechecked)
        parts[1] = rechecked.archive
        z = self._audit(parts)
        self.assertEqual(z.status, subject.HISTORY_REWRITE)
        self.assertFalse(z.all_old_rows_and_annotations_preserved)

    def test_comparable_to_fork_transition_is_not_a_no_change_certificate(self):
        parts = list(self._snapshots())
        old = tagged.build_local_tagged_fork_archive(
            parts[0]["ancestor"],
            parts[0]["branches"][0]["snapshot"],
            deepcopy(parts[0]["branches"][0]["snapshot"]),
        )
        self.assertIsNotNone(old.archive)
        parts[0] = old.archive
        z = self._audit(parts)
        self.assertEqual(z.status, subject.RELATION_CHANGE)

    def test_invalid_truncated_or_corrupted_new_archive_blocks(self):
        parts = list(self._snapshots())
        fake = deepcopy(parts[1])
        fake["branches"][0]["snapshot"]["entries"][0]["row_sha256"] = "e"*64
        parts[1] = fake
        self.assertEqual(self._audit(parts).status, BLOCKED)

    def test_missing_input_is_no_data(self):
        parts = list(self._snapshots())
        for i in range(6):
            copied = list(parts)
            copied[i] = None
            self.assertEqual(self._audit(copied).status, NO_DATA)

    def test_no_original_os_kernel_or_sqlite_access_during_comparison(self):
        parts = self._snapshots()
        with patch.object(
            sqlite3, "connect", side_effect=AssertionError("SQLite called"),
        ), patch.object(
            verify, "build_verifyos_middle_way_conditional_continuity_certificate",
            side_effect=AssertionError("VerifyOS re-execution"),
        ), patch.object(
            plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
            side_effect=AssertionError("PlanOS re-execution"),
        ):
            z = self._audit(parts)
        self.assertEqual(z.status, subject.PRESERVED_COMPATIBILITY)
        self.assertEqual(z.native_kernel_invocations, 0)

    def test_old_and_new_inputs_remain_bytewise_equal_to_copies(self):
        parts = self._snapshots()
        before = deepcopy(parts)
        self._audit(parts)
        self.assertEqual(parts, before)

    def test_no_secrets_or_external_authority_promoted(self):
        parts = self._snapshots()
        z = self._audit(parts)
        self.assertEqual(z.original_plan_result_state, NO_DATA)
        self.assertFalse(z.actual_historical_issuance_authenticated)
        self.assertFalse(z.original_lean_python_refinement_proved)
        self.assertFalse(z.independent_custody_authenticated)
        self.assertFalse(z.host_execution_authorized)
        self.assertIsNone(z.selected_successor)

    def test_source_checker_validates_exact_historical_blobs(self):
        self.assertEqual(guard.check(), ())

    def test_original_v059_blob_mutation_is_reported(self):
        target = guard.ROOT / (
            "formal/KUOS/Architecture/LeanPythonTaggedSpanObservationGluingV0_59.lean"
        )
        reading = Path.read_bytes
        def altered(path):
            raw = reading(path)
            return raw + b"\n" if path == target else raw
        with patch.object(Path, "read_bytes", altered):
            self.assertIn(
                "changed_pinned_source:formal/KUOS/Architecture/"
                "LeanPythonTaggedSpanObservationGluingV0_59.lean",
                guard.check(),
            )

    def test_prior_testcase_is_not_exported_for_duplicate_registration(self):
        self.assertNotIn("CommonAncestorForkV056Tests", globals())
        self.assertTrue(hasattr(fixture, "CommonAncestorForkV056Tests"))


if __name__ == "__main__":
    unittest.main()
