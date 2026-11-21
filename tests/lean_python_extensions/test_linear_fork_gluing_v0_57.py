"""v0.57 strict one-list non-gluing obstruction and local witness checking."""
from __future__ import annotations

from copy import deepcopy
import json
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_lean_python_linear_fork_gluing_v0_57 as subject,
    kuuos_lean_python_detached_replay_witness_v0_54 as detached,
    kuuos_lean_python_local_replay_reservation_v0_53 as replay,
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA, ROUTES,
)
from tests.lean_python_extensions.test_common_ancestor_fork_v0_56 import (
    CommonAncestorForkV056Tests,
)
from tests.lean_python_extensions.test_local_mac_bound_plan_claims_v0_52 import KEYS
from scripts import check_kuuos_lean_python_linear_fork_sources_v0_57 as guard


class LocalLinearForkGluingV057Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        CommonAncestorForkV056Tests.setUpClass()
        cls.helper = CommonAncestorForkV056Tests(
            "test_six_native_routes_yield_local_fork_only"
        )

    def _fork(self, route="retain"):
        return self.helper._fork(route)

    @staticmethod
    def _continuation(manifest):
        later = deepcopy(manifest)
        last_two = deepcopy(later["entries"][-2:])
        previous = later["declared_chain_head"]
        idx_start = len(later["entries"]) + 1
        for position, row in enumerate(last_two, start=idx_start):
            row["entry_id"] = position
            row["sequence"] += 100
            row["nonce_hex"] = f"{900 + position:032x}"
            row["previous_row_sha256"] = previous
            row["row_sha256"] = replay._hash_row(
                previous, row["key_id"], row["context_id"],
                row["sequence"], row["nonce_hex"], row["message_sha256"],
            )
            later["entries"].append(row)
            previous = row["row_sha256"]
        later["declared_chain_head"] = previous
        assert detached.verify_detached_replay_witness(later).status == (
            detached.DETACHED_UNANCHORED
        )
        return later

    def test_six_native_routes_detect_fork_non_gluing(self):
        for route, _, _, _ in ROUTES:
            with self.subTest(route=route):
                old, left, right = self._fork(route)
                result = subject.audit_local_linear_fork_gluing(old, left, right)
                self.assertEqual(result.status, subject.NO_LINEAR_GLUE)
                self.assertTrue(result.declared_linear_fork)
                self.assertFalse(
                    result.common_linear_successor_possible_in_this_model)
                self.assertFalse(result.supplied_successor_verifies_both_exact_prefixes)
                self.assertFalse(result.independently_authenticated_history)
                self.assertFalse(result.host_execution_authorized)

    def test_fork_with_wrong_old_checkpoint_preserves_both_obstructions(self):
        old, left, right = self._fork()
        result = subject.audit_local_linear_fork_gluing(
            old, left, right,
            separately_supplied_ancestor_checkpoint_sha256="f"*64,
        )
        self.assertEqual(result.status, subject.NO_LINEAR_GLUE_AND_CHECKPOINT)
        self.assertTrue(result.declared_linear_fork)
        self.assertIn("caller_prior_checkpoint_value_disagrees", result.issues)
        self.assertIn(
            "no_common_exact_prefix_successor_in_one_linear_list",
            result.issues,
        )

    def test_fork_is_still_impossible_with_declared_future_candidate(self):
        old, left, right = self._fork()
        result = subject.audit_local_linear_fork_gluing(
            old, left, right, declared_future_manifest=left,
        )
        self.assertEqual(result.status, subject.NO_LINEAR_GLUE)
        self.assertFalse(result.supplied_successor_verifies_both_exact_prefixes)
        self.assertIsNone(result.local_declared_preferred_witness)

    def test_matching_old_checkpoint_never_removes_fork(self):
        old, left, right = self._fork()
        digest = detached.verify_detached_replay_witness(old).manifest_sha256
        result = subject.audit_local_linear_fork_gluing(
            old, left, right, separately_supplied_ancestor_checkpoint_sha256=digest
        )
        self.assertEqual(result.status, subject.NO_LINEAR_GLUE)
        self.assertTrue(result.caller_checkpoint_value_matches)
        self.assertFalse(result.independent_checkpoint_custody_authenticated)

    def test_identical_successors_have_existing_common_witness(self):
        old, left, _ = self._fork()
        result = subject.audit_local_linear_fork_gluing(old, left, deepcopy(left))
        self.assertEqual(result.status, subject.COMPARABLE_LOCAL)
        self.assertTrue(result.common_linear_successor_possible_in_this_model)
        self.assertEqual(result.local_declared_preferred_witness, "left")
        self.assertFalse(result.declared_linear_fork)

    def test_explicit_same_manifest_future_is_accepted_only_locally(self):
        old, left, _ = self._fork()
        result = subject.audit_local_linear_fork_gluing(
            old, left, deepcopy(left), declared_future_manifest=deepcopy(left),
        )
        self.assertEqual(result.status, subject.MATCHED_LOCAL_WITNESS)
        self.assertTrue(result.supplied_successor_verifies_both_exact_prefixes)
        self.assertIsNotNone(result.supplied_successor_sha256)
        self.assertFalse(result.host_execution_authorized)
        self.assertFalse(result.original_lean_match_proved)

    def test_comparable_successors_are_gluable_by_longer_one(self):
        old, left, _ = self._fork()
        later = self._continuation(left)
        result = subject.audit_local_linear_fork_gluing(old, left, later)
        self.assertEqual(result.status, subject.COMPARABLE_LOCAL)
        self.assertEqual(result.local_declared_preferred_witness, "right")
        self.assertTrue(result.common_linear_successor_possible_in_this_model)

    def test_explicit_longer_future_witness_passes_both_prefixes(self):
        old, left, _ = self._fork()
        later = self._continuation(left)
        result = subject.audit_local_linear_fork_gluing(
            old, left, later, declared_future_manifest=deepcopy(later),
        )
        self.assertEqual(result.status, subject.MATCHED_LOCAL_WITNESS)
        self.assertTrue(result.supplied_successor_verifies_both_exact_prefixes)
        self.assertFalse(result.independently_authenticated_history)

    def test_too_short_future_witness_is_obstruction(self):
        old, left, _ = self._fork()
        later = self._continuation(left)
        result = subject.audit_local_linear_fork_gluing(
            old, left, later, declared_future_manifest=deepcopy(left),
        )
        self.assertEqual(result.status, subject.WITNESS_OBSTRUCTION)
        self.assertFalse(result.supplied_successor_verifies_both_exact_prefixes)
        self.assertIn("declared_future_not_both_exact_prefixes", result.issues)

    def test_invalid_future_manifest_is_blocked_not_glued(self):
        old, left, _ = self._fork()
        altered = deepcopy(left)
        altered["entries"][0]["row_sha256"] = "f" * 64
        result = subject.audit_local_linear_fork_gluing(
            old, left, deepcopy(left), declared_future_manifest=altered,
        )
        self.assertEqual(result.status, BLOCKED)

    def test_wrong_old_checkpoint_on_comparable_history_is_obstruction(self):
        old, left, _ = self._fork()
        z = subject.audit_local_linear_fork_gluing(
            old, left, deepcopy(left),
            separately_supplied_ancestor_checkpoint_sha256="f" * 64,
            declared_future_manifest=deepcopy(left),
        )
        self.assertEqual(z.status, subject.CHECKPOINT_OBSTRUCTION)
        self.assertTrue(z.supplied_successor_verifies_both_exact_prefixes)
        self.assertFalse(z.caller_checkpoint_value_matches)

    def test_no_common_ancestor_blocks_claim(self):
        old, left, right = self._fork()
        z = subject.audit_local_linear_fork_gluing(left, old, right)
        self.assertEqual(z.status, subject.ANCESTOR_OBSTRUCTION)
        self.assertFalse(z.common_linear_successor_possible_in_this_model)

    def test_missing_or_corrupt_snapshot_never_passes(self):
        old, left, right = self._fork()
        self.assertEqual(subject.audit_local_linear_fork_gluing(
            None, left, right).status, NO_DATA)
        corrupted = deepcopy(right)
        corrupted["entries"].pop()
        self.assertEqual(subject.audit_local_linear_fork_gluing(
            old, left, corrupted).status, BLOCKED)

    def test_invalid_prior_checkpoint_value_fails_closed(self):
        old, left, right = self._fork()
        for value in (False, 17, "", "F"*64, "1"*63):
            with self.subTest(value=value):
                z = subject.audit_local_linear_fork_gluing(
                    old, left, right,
                    separately_supplied_ancestor_checkpoint_sha256=value,
                )
                self.assertEqual(z.status, BLOCKED)

    def test_no_sqlite_or_original_kernel_execution(self):
        old, left, right = self._fork()
        with patch.object(
            sqlite3, "connect", side_effect=AssertionError("SQLite access"),
        ), patch.object(
            verify, "build_verifyos_middle_way_conditional_continuity_certificate",
            side_effect=AssertionError("VerifyOS run"),
        ), patch.object(
            plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
            side_effect=AssertionError("PlanOS run"),
        ):
            z = subject.audit_local_linear_fork_gluing(old, left, right)
        self.assertEqual(z.status, subject.NO_LINEAR_GLUE)
        self.assertEqual(z.native_kernel_invocations, 0)

    def test_input_unchanged_and_no_key_material_leaks(self):
        old, left, right = self._fork()
        originals = deepcopy((old, left, right))
        subject.audit_local_linear_fork_gluing(old, left, right)
        self.assertEqual((old, left, right), originals)
        blob = json.dumps([old, left, right]).encode("ascii")
        for secret in KEYS.values():
            self.assertNotIn(secret, blob)
        self.assertNotIn(b"mac_sha256", blob)

    def test_source_checker_passes(self):
        self.assertEqual(guard.check(), ())

    def test_historical_v056_blob_mutation_fails_closed(self):
        target = guard.ROOT / (
            "formal/KUOS/Architecture/LeanPythonCommonAncestorForkBoundaryV0_56.lean"
        )
        raw_read = Path.read_bytes
        def altered(path):
            raw = raw_read(path)
            return raw + b"\n" if path == target else raw
        with patch.object(Path, "read_bytes", altered):
            self.assertIn(
                "changed_pinned_source:formal/KUOS/Architecture/"
                "LeanPythonCommonAncestorForkBoundaryV0_56.lean",
                guard.check(),
            )


if __name__ == "__main__":
    unittest.main()
