from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
)
from runtime.kuuos_repository_alignment_scopes_v0_81 import (
    GLOBAL_SCOPE_ID,
    compare_alignment_scope_indexes,
)
from runtime.kuuos_repository_incremental_preservation_v0_81 import (
    preserve_repository_normal_form_incrementally,
)
from runtime.kuuos_repository_structure_observer_v0_79 import (
    observe_repository_structure,
)
from tests.kuuos_repository_incremental_fixture_v0_81 import (
    add_text_path,
    normal_dual_contract_snapshot,
    remove_path,
    replace_text,
)


class RepositoryIncrementalPreservationV081Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.previous = normal_dual_contract_snapshot()
        self.previous_certificate = certify_repository_alignment_normal_form(
            self.previous
        )
        self.assertEqual(
            observe_repository_structure(self.previous).weighted_defect_score,
            0,
        )

    def test_unrelated_change_reuses_all_scopes(self) -> None:
        current = replace_text(
            self.previous,
            "notes/unrelated.txt",
            "unrelated-v2\n",
        )
        certificate = preserve_repository_normal_form_incrementally(
            self.previous,
            current,
            self.previous_certificate,
        )
        self.assertEqual(len(certificate.reused_scope_ids), 3)
        self.assertEqual(certificate.rechecked_scope_ids, ())
        self.assertFalse(certificate.full_recheck_performed)
        self.assertTrue(certificate.current_normal_form_preserved)
        self.assertEqual(certificate.current_score, 0)

    def test_one_contract_change_rechecks_only_that_contract(self) -> None:
        current = replace_text(
            self.previous,
            "runtime/alpha_v0_81.py",
            "ALPHA = 2\n",
        )
        _, _, delta = compare_alignment_scope_indexes(self.previous, current)
        self.assertEqual(
            delta.invalidated_scope_ids,
            ("contract:manifests/alpha_v0_81.json",),
        )
        self.assertIn(GLOBAL_SCOPE_ID, delta.reused_scope_ids)
        self.assertIn(
            "contract:manifests/beta_v0_81.json",
            delta.reused_scope_ids,
        )
        self.assertFalse(delta.full_recheck_required)
        certificate = preserve_repository_normal_form_incrementally(
            self.previous,
            current,
            self.previous_certificate,
        )
        self.assertEqual(
            certificate.rechecked_scope_ids,
            ("contract:manifests/alpha_v0_81.json",),
        )
        self.assertFalse(certificate.full_recheck_performed)
        self.assertTrue(certificate.all_rechecked_scopes_at_zero)
        self.assertTrue(certificate.current_normal_form_preserved)

    def test_root_change_forces_full_recheck(self) -> None:
        current = replace_text(
            self.previous,
            "lakefile.toml",
            self.previous.texts["lakefile.toml"] + "\n# harmless change\n",
        )
        certificate = preserve_repository_normal_form_incrementally(
            self.previous,
            current,
            self.previous_certificate,
        )
        self.assertTrue(certificate.full_recheck_performed)
        self.assertTrue(certificate.full_certificate_digest)
        self.assertEqual(len(certificate.rechecked_scope_ids), 3)
        self.assertTrue(certificate.current_normal_form_preserved)

    def test_missing_contract_path_breaks_preservation(self) -> None:
        current = remove_path(self.previous, "runtime/alpha_v0_81.py")
        certificate = preserve_repository_normal_form_incrementally(
            self.previous,
            current,
            self.previous_certificate,
        )
        self.assertFalse(certificate.full_recheck_performed)
        self.assertFalse(certificate.all_rechecked_scopes_at_zero)
        self.assertFalse(certificate.current_normal_form_preserved)
        self.assertEqual(certificate.current_score, 100)

    def test_workflow_drift_forces_full_recheck_and_detects_defect(self) -> None:
        current = replace_text(
            self.previous,
            ".github/workflows/alignment-fixture-v081.yml",
            "name: alignment fixture\n\non:\n  workflow_dispatch:\n  pull_request:\n",
        )
        certificate = preserve_repository_normal_form_incrementally(
            self.previous,
            current,
            self.previous_certificate,
        )
        self.assertTrue(certificate.full_recheck_performed)
        self.assertFalse(certificate.all_rechecked_scopes_at_zero)
        self.assertFalse(certificate.current_normal_form_preserved)
        self.assertEqual(certificate.current_score, 10)

    def test_added_unrelated_path_does_not_invalidate_scopes(self) -> None:
        current = add_text_path(
            self.previous,
            "notes/new-unrelated.txt",
            "new\n",
        )
        _, _, delta = compare_alignment_scope_indexes(self.previous, current)
        self.assertEqual(delta.added_paths, ("notes/new-unrelated.txt",))
        self.assertEqual(delta.invalidated_scope_ids, ())
        self.assertFalse(delta.full_recheck_required)
        certificate = preserve_repository_normal_form_incrementally(
            self.previous,
            current,
            self.previous_certificate,
        )
        self.assertTrue(certificate.current_normal_form_preserved)

    def test_stale_previous_certificate_is_rejected(self) -> None:
        stale = replace(
            self.previous_certificate,
            initial_snapshot_digest="stale",
        )
        with self.assertRaisesRegex(
            ValueError,
            "previous_normal_form_certificate_invalid",
        ):
            preserve_repository_normal_form_incrementally(
                self.previous,
                self.previous,
                stale,
            )


if __name__ == "__main__":
    unittest.main()
