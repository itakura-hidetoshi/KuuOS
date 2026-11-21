"""v0.59: exact overlap agreement iff tagged observation gluing."""
from __future__ import annotations

from copy import deepcopy
import json
import sqlite3
from pathlib import Path
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_lean_python_tagged_span_gluing_v0_59 as subject,
    kuuos_lean_python_tagged_fork_archive_v0_58 as archived,
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA, ROUTES,
)
# A module alias is crucial: importing a previous TestCase directly into this
# module produces duplicate test IDs in the retained native discovery loader.
from tests.lean_python_extensions import test_tagged_fork_archive_v0_58 as fixture
from scripts import check_kuuos_lean_python_tagged_span_sources_v0_59 as source_check


class TaggedSpanObservationGluingV059Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.TaggedForkArchiveV058Tests.setUpClass()
        cls.fixture = fixture.TaggedForkArchiveV058Tests(
            "test_six_native_routes_preserve_both_fork_branches"
        )

    def _archive(self, route="retain", *, comparable=False, checkpoint=None):
        old, left, right = self.fixture._fork(route)
        if comparable:
            right = deepcopy(left)
        result = archived.build_local_tagged_fork_archive(
            old, left, right,
            separately_supplied_ancestor_checkpoint_sha256=checkpoint,
        )
        self.assertIsNotNone(result.archive)
        return result.archive

    @staticmethod
    def _observations(archive):
        common = archive["ancestor"]["entries"]
        left_rows = archive["branches"][0]["snapshot"]["entries"]
        right_rows = archive["branches"][1]["snapshot"]["entries"]
        n = len(common)
        shared = [f"shared-{i}" for i in range(n)]
        left = shared + [f"left-{i}" for i in range(len(left_rows)-n)]
        right = shared + [f"right-{i}" for i in range(len(right_rows)-n)]
        return left, right

    def test_six_native_routes_glue_on_shared_ancestor_without_linear_descent(self):
        for route, _, _, _ in ROUTES:
            with self.subTest(route=route):
                archive = self._archive(route)
                lv, rv = self._observations(archive)
                result = subject.glue_tagged_observations(archive, lv, rv)
                self.assertEqual(result.status, subject.LOCAL_GLUED)
                self.assertTrue(result.shared_value_agreement_checked)
                self.assertTrue(result.common_observations_compatible)
                self.assertTrue(result.tagged_gluing_constructed)
                self.assertTrue(result.branch_projections_preserved)
                self.assertTrue(result.fork_obstruction_preserved)
                self.assertFalse(result.linear_history_descended)
                self.assertFalse(result.global_descent_certified)
                self.assertFalse(result.archive_custody_authenticated)
                self.assertFalse(result.host_execution_authorized)
                self.assertIsNone(result.selected_successor)

    def test_branch_projection_values_reconstruct_exactly(self):
        archive = self._archive()
        left, right = self._observations(archive)
        z = subject.glue_tagged_observations(archive, left, right)
        slots = z.glued["positions"]
        n = z.shared_count
        m = z.left_only_count
        self.assertEqual([v["value"] for v in slots[:n+m]], left)
        self.assertEqual(
            [v["value"] for v in slots[:n]] +
            [v["value"] for v in slots[n+m:]],
            right,
        )
        self.assertEqual(len(slots), n+m+z.right_only_count)
        self.assertEqual(len({v["id"] for v in slots}), len(slots))

    def test_coincident_branch_values_do_not_merge_private_positions(self):
        archive = self._archive()
        left, right = self._observations(archive)
        n = len(archive["ancestor"]["entries"])
        left[n:] = ["same"] * (len(left)-n)
        right[n:] = ["same"] * (len(right)-n)
        z = subject.glue_tagged_observations(archive, left, right)
        self.assertEqual(z.status, subject.LOCAL_GLUED)
        slots = z.glued["positions"]
        self.assertTrue(any(v["id"].startswith("left:") for v in slots))
        self.assertTrue(any(v["id"].startswith("right:") for v in slots))
        self.assertNotEqual(
            next(v for v in slots if v["id"] == "left:000000")["id"],
            next(v for v in slots if v["id"] == "right:000000")["id"],
        )

    def test_single_common_value_disagreement_is_obstruction(self):
        archive = self._archive()
        left, right = self._observations(archive)
        right[0] = "different"
        z = subject.glue_tagged_observations(archive, left, right)
        self.assertEqual(z.status, subject.OVERLAP_OBSTRUCTION)
        self.assertFalse(z.common_observations_compatible)
        self.assertFalse(z.tagged_gluing_constructed)
        self.assertIsNone(z.glued)
        self.assertIn("shared_observation_disagreement:0", z.issues)
        self.assertTrue(z.fork_obstruction_preserved)

    def test_multiple_common_disagreements_are_all_preserved(self):
        archive = self._archive()
        left, right = self._observations(archive)
        right[0], right[1] = "X", "Y"
        z = subject.glue_tagged_observations(archive, left, right)
        self.assertEqual(z.status, subject.OVERLAP_OBSTRUCTION)
        self.assertIn("shared_observation_disagreement:0", z.issues)
        self.assertIn("shared_observation_disagreement:1", z.issues)
        self.assertIsNone(z.glued)

    def test_private_value_disagreement_is_not_shared_obstruction(self):
        archive = self._archive()
        left, right = self._observations(archive)
        n = len(archive["ancestor"]["entries"])
        left[n], right[n] = "only-left", "only-right"
        z = subject.glue_tagged_observations(archive, left, right)
        self.assertEqual(z.status, subject.LOCAL_GLUED)
        self.assertTrue(z.branch_projections_preserved)
        self.assertEqual(z.glued["positions"][n]["value"], "only-left")
        self.assertEqual(
            z.glued["positions"][n+z.left_only_count]["value"], "only-right",
        )

    def test_comparable_branches_still_use_distinct_tagged_slots(self):
        archive = self._archive(comparable=True)
        left, right = self._observations(archive)
        z = subject.glue_tagged_observations(archive, left, right)
        self.assertEqual(z.status, subject.LOCAL_GLUED)
        self.assertFalse(z.fork_obstruction_preserved)
        self.assertTrue(z.tagged_gluing_constructed)
        self.assertFalse(z.linear_history_descended)

    def test_inherited_prior_checkpoint_obstruction_is_not_erased(self):
        archive = self._archive(checkpoint="f"*64)
        left, right = self._observations(archive)
        z = subject.glue_tagged_observations(archive, left, right)
        self.assertEqual(z.status, subject.CHECKPOINT_OBSTRUCTION)
        self.assertTrue(z.tagged_gluing_constructed)
        self.assertTrue(z.fork_obstruction_preserved)
        self.assertIn("caller_prior_checkpoint_value_disagrees", z.issues)
        self.assertFalse(z.archive_custody_authenticated)

    def test_overlap_and_prior_checkpoint_both_obstructions(self):
        archive = self._archive(checkpoint="f"*64)
        left, right = self._observations(archive)
        right[1] = "foreign"
        z = subject.glue_tagged_observations(archive, left, right)
        self.assertEqual(z.status, subject.COMPOSITE_OBSTRUCTION)
        self.assertIn("caller_prior_checkpoint_value_disagrees", z.issues)
        self.assertIn("shared_observation_disagreement:1", z.issues)
        self.assertFalse(z.tagged_gluing_constructed)

    def test_separate_correct_archive_digest_does_not_grant_authority(self):
        archive = self._archive()
        left, right = self._observations(archive)
        checked = archived.verify_local_tagged_fork_archive(archive)
        z = subject.glue_tagged_observations(
            archive, left, right,
            separately_supplied_archive_sha256=checked.archive_sha256,
        )
        self.assertEqual(z.status, subject.LOCAL_GLUED)
        self.assertTrue(z.tagged_gluing_constructed)
        self.assertFalse(z.global_descent_certified)
        self.assertFalse(z.host_execution_authorized)

    def test_wrong_separate_archive_digest_is_not_silent_success(self):
        archive = self._archive()
        left, right = self._observations(archive)
        z = subject.glue_tagged_observations(
            archive, left, right, separately_supplied_archive_sha256="f"*64,
        )
        self.assertEqual(z.status, subject.CHECKPOINT_OBSTRUCTION)
        self.assertTrue(z.tagged_gluing_constructed)
        self.assertIn("caller_archive_digest_disagrees", z.issues)

    def test_invalid_archive_or_wrong_tag_blocks(self):
        archive = self._archive()
        left, right = self._observations(archive)
        broken = deepcopy(archive)
        broken["branches"][0]["tag"] = "right"
        z = subject.glue_tagged_observations(broken, left, right)
        self.assertEqual(z.status, BLOCKED)
        self.assertIsNone(z.glued)

    def test_archive_without_original_input_is_no_data(self):
        archive = self._archive()
        left, right = self._observations(archive)
        self.assertEqual(subject.glue_tagged_observations(
            None, left, right).status, NO_DATA)
        self.assertEqual(subject.glue_tagged_observations(
            archive, None, right).status, NO_DATA)
        self.assertEqual(subject.glue_tagged_observations(
            archive, left, None).status, NO_DATA)

    def test_wrong_shape_or_alignment_blocks(self):
        archive = self._archive()
        left, right = self._observations(archive)
        for bad in (False, {}, (), left[:-1], 42, ""):
            with self.subTest(bad=repr(bad)[:50]):
                self.assertEqual(
                    subject.glue_tagged_observations(archive, bad, right).status,
                    BLOCKED,
                )

    def test_bad_annotation_scalar_or_excessive_size_blocks(self):
        archive = self._archive()
        left, right = self._observations(archive)
        for bad in (None, 0, True, "", "z"*1025, "\ud800"):
            new = list(left)
            new[0] = bad
            with self.subTest(bad=repr(bad)[:50]):
                self.assertEqual(
                    subject.glue_tagged_observations(archive, new, right).status,
                    BLOCKED,
                )

    def test_unicode_annotations_canonicalize_stably(self):
        archive = self._archive()
        left, right = self._observations(archive)
        left[0] = right[0] = "陰陽縁起"
        first = subject.glue_tagged_observations(archive, left, right)
        second = subject.glue_tagged_observations(
            deepcopy(archive), deepcopy(left), deepcopy(right),
        )
        self.assertEqual(first.status, subject.LOCAL_GLUED)
        self.assertEqual(first.glued_sha256, second.glued_sha256)

    def test_pure_gluing_no_db_or_original_kernel_invocations(self):
        archive = self._archive()
        left, right = self._observations(archive)
        with patch.object(
            sqlite3, "connect", side_effect=AssertionError("SQLite call"),
        ), patch.object(
            verify, "build_verifyos_middle_way_conditional_continuity_certificate",
            side_effect=AssertionError("VerifyOS rerun"),
        ), patch.object(
            plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
            side_effect=AssertionError("PlanOS rerun"),
        ):
            z = subject.glue_tagged_observations(archive, left, right)
        self.assertEqual(z.status, subject.LOCAL_GLUED)
        self.assertEqual(z.native_kernel_invocations, 0)

    def test_inputs_not_mutated(self):
        archive = self._archive()
        left, right = self._observations(archive)
        before = deepcopy((archive, left, right))
        subject.glue_tagged_observations(archive, left, right)
        self.assertEqual((archive, left, right), before)

    def test_source_guard_passes(self):
        self.assertEqual(source_check.check(), ())

    def test_prior_v058_source_blob_mutation_detected(self):
        path = source_check.ROOT / (
            "formal/KUOS/Architecture/LeanPythonTaggedForkArchiveBoundaryV0_58.lean"
        )
        original = Path.read_bytes

        def altered(p):
            data = original(p)
            return data + b"\n" if p == path else data

        with patch.object(Path, "read_bytes", altered):
            self.assertIn(
                "changed_pinned_source:formal/KUOS/Architecture/"
                "LeanPythonTaggedForkArchiveBoundaryV0_58.lean",
                source_check.check(),
            )

    def test_does_not_export_prior_unittest_testcase(self):
        self.assertNotIn("TaggedForkArchiveV058Tests", globals())
        self.assertTrue(hasattr(fixture, "TaggedForkArchiveV058Tests"))


if __name__ == "__main__":
    unittest.main()
