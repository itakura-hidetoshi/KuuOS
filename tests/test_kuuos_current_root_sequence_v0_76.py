import unittest

from runtime.kuuos_current_root_sequence_v0_76 import (
    CURRENT_STATUS_SURFACE_INDEX_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV076Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_current_status_surface_index_frontier_is_connected(self):
        self.assertEqual(
            "kuuos_current_status_surface_index_v0_76",
            CURRENT_STATUS_SURFACE_INDEX_FRONTIER,
        )
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_current_status_surface_index_v0_76", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_76", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("current-status-surface-index-v0-76", text)
        self.assertIn("current-root-sequence-v0-76", text)


if __name__ == "__main__":
    unittest.main()
