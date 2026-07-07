import unittest

from runtime.kuuos_current_root_sequence_v0_91 import (
    CANDIDATE_RECEIPT_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV091Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_frontier(self):
        self.assertEqual("kuuos_self_organization_candidate_receipt_v0_91", CANDIDATE_RECEIPT_FRONTIER)

    def test_targets(self):
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_candidate_receipt_v0_91", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_91", targets)

    def test_summary(self):
        text = as_markdown()
        self.assertIn("candidate-receipt-v0-91", text)
        self.assertIn("current-root-sequence-v0-91", text)


if __name__ == "__main__":
    unittest.main()
