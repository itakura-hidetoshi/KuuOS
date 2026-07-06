import unittest

from runtime.kuuos_current_root_sequence_v0_87 import (
    BOUNDED_CHANGE_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV087Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_frontier_and_targets(self):
        self.assertEqual("kuuos_self_organization_bounded_change_v0_87", BOUNDED_CHANGE_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_bounded_change_v0_87", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_87", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("bounded-change-v0-87", text)
        self.assertIn("current-root-sequence-v0-87", text)


if __name__ == "__main__":
    unittest.main()
