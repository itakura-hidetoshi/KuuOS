import unittest

from runtime.kuuos_current_root_sequence_v0_88 import (
    COMPLETION_RECEIPT_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV088Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_frontier(self):
        self.assertEqual("kuuos_self_organization_completion_receipt_v0_88", COMPLETION_RECEIPT_FRONTIER)

    def test_targets(self):
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_completion_receipt_v0_88", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_88", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("completion-receipt-v0-88", text)
        self.assertIn("current-root-sequence-v0-88", text)


if __name__ == "__main__":
    unittest.main()
