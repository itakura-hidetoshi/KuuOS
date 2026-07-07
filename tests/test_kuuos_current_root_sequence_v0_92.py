import unittest

from runtime.kuuos_current_root_sequence_v0_92 import (
    SELECTION_POLICY_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV092Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_policy_frontier_is_connected(self):
        self.assertEqual("kuuos_self_organization_selection_policy_v0_92", SELECTION_POLICY_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_selection_policy_v0_92", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_92", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("selection-policy-v0-92", text)
        self.assertIn("current-root-sequence-v0-92", text)


if __name__ == "__main__":
    unittest.main()
