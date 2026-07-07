import unittest

from runtime.kuuos_current_root_sequence_v0_93 import (
    SELECTED_NEXT_ACTION_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV093Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_selected_next_action_frontier_is_connected(self):
        self.assertEqual("kuuos_self_organization_selected_next_action_v0_93", SELECTED_NEXT_ACTION_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_selected_next_action_v0_93", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_93", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("selected-next-action-v0-93", text)
        self.assertIn("current-root-sequence-v0-93", text)


if __name__ == "__main__":
    unittest.main()
