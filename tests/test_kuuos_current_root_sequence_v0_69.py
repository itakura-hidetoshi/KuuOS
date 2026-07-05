import unittest

from runtime.kuuos_current_root_sequence_v0_69 import (
    STATUS_INDEX_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV069Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_status_index_frontier_is_connected(self):
        self.assertEqual("kuuos_status_index_v0_69", STATUS_INDEX_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_status_index_v0_69", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_69", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("status-index-v0-69", text)
        self.assertIn("current-root-sequence-v0-69", text)


if __name__ == "__main__":
    unittest.main()
