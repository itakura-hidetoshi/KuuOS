from __future__ import annotations

import unittest

from runtime import kuuos_root_map_adoption_deferral_v0_52 as deferral
from runtime import kuuos_root_map_deferral_receipt_v0_53 as receipt


class RootMapDeferralReceiptV053Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(receipt.VERSION, "kuuos_root_map_deferral_receipt_v0_53")
        self.assertEqual(receipt.DEPENDS_ON, deferral.VERSION)
        self.assertTrue(receipt.READ_ONLY)
        self.assertTrue(receipt.METADATA_ONLY)
        self.assertTrue(receipt.RECEIPT_ONLY)
        self.assertFalse(receipt.REPOSITORY_CHANGE_RECORDED)

    def test_required_items_are_present(self) -> None:
        ids = set(receipt.receipt_item_ids())
        for item_id in receipt.REQUIRED_RECEIPT_ITEMS:
            self.assertIn(item_id, ids)

    def test_all_receipt_items_pass(self) -> None:
        self.assertEqual(receipt.failed_receipt_items(), ())

    def test_receipt_verifies(self) -> None:
        self.assertEqual(receipt.receipt_issues(), ())
        self.assertTrue(receipt.verify_deferral_receipt())

    def test_markdown_names_future_layer(self) -> None:
        markdown = receipt.as_markdown()
        self.assertIn("deferral_verified", markdown)
        self.assertIn("repository_change_not_recorded", markdown)
        self.assertIn("future_layer_required", markdown)


if __name__ == "__main__":
    unittest.main()
