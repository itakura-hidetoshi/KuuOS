import unittest

from runtime.kuuos_current_root_sequence_v0_79 import (
    SELF_ORGANIZATION_CANDIDATE_QUEUE_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV079Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_candidate_queue_frontier_is_connected(self):
        self.assertEqual(
            "kuuos_self_organization_candidate_queue_v0_79",
            SELF_ORGANIZATION_CANDIDATE_QUEUE_FRONTIER,
        )
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_candidate_queue_v0_79", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_79", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("self-organization-candidate-queue-v0-79", text)
        self.assertIn("current-root-sequence-v0-79", text)


if __name__ == "__main__":
    unittest.main()
