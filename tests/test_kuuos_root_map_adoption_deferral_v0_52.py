from __future__ import annotations

import unittest

from runtime import kuuos_root_map_adoption_deferral_v0_52 as deferral
from runtime import kuuos_root_map_pre_adoption_review_v0_51 as review


class RootMapAdoptionDeferralV052Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(deferral.VERSION, "kuuos_root_map_adoption_deferral_v0_52")
        self.assertEqual(deferral.DEPENDS_ON, review.VERSION)
        self.assertTrue(deferral.READ_ONLY)
        self.assertTrue(deferral.METADATA_ONLY)
        self.assertTrue(deferral.ADOPTION_DEFERRED)
        self.assertFalse(deferral.CHANGE_PERFORMED)

    def test_required_items_are_present(self) -> None:
        ids = set(deferral.deferral_item_ids())
        for item_id in deferral.REQUIRED_DEFERRAL_ITEMS:
            self.assertIn(item_id, ids)

    def test_all_deferral_items_pass(self) -> None:
        self.assertEqual(deferral.failed_deferral_items(), ())

    def test_deferral_verifies(self) -> None:
        self.assertEqual(deferral.deferral_issues(), ())
        self.assertTrue(deferral.verify_adoption_deferral())

    def test_markdown_names_future_layer(self) -> None:
        markdown = deferral.as_markdown()
        self.assertIn("pre_review_verified", markdown)
        self.assertIn("change_not_performed", markdown)
        self.assertIn("separate_future_layer_required", markdown)


if __name__ == "__main__":
    unittest.main()
