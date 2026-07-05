import unittest

from runtime.kuuos_current_root_sequence_v0_74 import (
    CURRENT_STATUS_SURFACE_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV074Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_current_status_surface_frontier_is_connected(self):
        self.assertEqual("kuuos_current_status_surface_v0_74", CURRENT_STATUS_SURFACE_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_current_status_surface_v0_74", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_74", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("current-status-surface-v0-74", text)
        self.assertIn("current-root-sequence-v0-74", text)


if __name__ == "__main__":
    unittest.main()
