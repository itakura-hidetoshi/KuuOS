import unittest

from runtime.kuuos_current_root_sequence_v0_90 import (
    CANDIDATE_QUEUE_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV090Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_frontier(self):
        self.assertEqual("kuuos_self_organization_candidate_queue_v0_90", CANDIDATE_QUEUE_FRONTIER)

    def test_targets(self):
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_candidate_queue_v0_90", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_90", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("candidate-queue-v0-90", text)
        self.assertIn("current-root-sequence-v0-90", text)


if __name__ == "__main__":
    unittest.main()
