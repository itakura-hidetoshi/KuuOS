import unittest

from runtime.kuuos_current_root_sequence_v0_80 import (
    CANDIDATE_RECEIPT_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV080Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_receipt_frontier_is_connected(self):
        self.assertEqual("kuuos_self_organization_candidate_receipt_v0_80", CANDIDATE_RECEIPT_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_candidate_receipt_v0_80", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_80", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("candidate-receipt-v0-80", text)
        self.assertIn("current-root-sequence-v0-80", text)


if __name__ == "__main__":
    unittest.main()
