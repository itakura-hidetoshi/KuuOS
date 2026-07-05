from __future__ import annotations

import unittest

from runtime import kuuos_root_map_deferral_closeout_v0_54 as closeout
from runtime import kuuos_root_map_deferral_receipt_v0_53 as receipt


class RootMapDeferralCloseoutV054Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(closeout.VERSION, "kuuos_root_map_deferral_closeout_v0_54")
        self.assertEqual(closeout.DEPENDS_ON, receipt.VERSION)
        self.assertTrue(closeout.READ_ONLY)
        self.assertTrue(closeout.METADATA_ONLY)
        self.assertTrue(closeout.CLOSEOUT_ONLY)
        self.assertFalse(closeout.FOLLOWUP_OPENED)

    def test_required_items_are_present(self) -> None:
        ids = set(closeout.closeout_item_ids())
        for item_id in closeout.REQUIRED_CLOSEOUT_ITEMS:
            self.assertIn(item_id, ids)

    def test_all_closeout_items_pass(self) -> None:
        self.assertEqual(closeout.failed_closeout_items(), ())

    def test_closeout_verifies(self) -> None:
        self.assertEqual(closeout.closeout_issues(), ())
        self.assertTrue(closeout.verify_deferral_closeout())

    def test_markdown_names_audit_ready(self) -> None:
        markdown = closeout.as_markdown()
        self.assertIn("receipt_verified", markdown)
        self.assertIn("followup_not_opened", markdown)
        self.assertIn("audit_ready", markdown)


if __name__ == "__main__":
    unittest.main()
