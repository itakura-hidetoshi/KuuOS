import unittest

from runtime.kuuos_current_root_sequence_v0_73 import (
    CURRENT_STATUS_MANIFEST_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV073Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_current_status_manifest_frontier_is_connected(self):
        self.assertEqual("kuuos_current_status_manifest_v0_73", CURRENT_STATUS_MANIFEST_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_current_status_manifest_v0_73", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_73", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("current-status-manifest-v0-73", text)
        self.assertIn("current-root-sequence-v0-73", text)


if __name__ == "__main__":
    unittest.main()
