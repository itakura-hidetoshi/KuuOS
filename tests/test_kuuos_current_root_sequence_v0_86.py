import unittest

from runtime.kuuos_current_root_sequence_v0_86 import (
    REVIEW_DECISION_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV086Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_review_decision_frontier_is_connected(self):
        self.assertEqual("kuuos_self_organization_review_decision_v0_86", REVIEW_DECISION_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_review_decision_v0_86", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_86", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("review-decision-v0-86", text)
        self.assertIn("current-root-sequence-v0-86", text)


if __name__ == "__main__":
    unittest.main()
