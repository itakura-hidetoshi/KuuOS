import unittest

from runtime.kuuos_current_root_sequence_v0_75 import (
    CURRENT_STATUS_SURFACE_ARTIFACT_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV075Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_current_status_surface_artifact_frontier_is_connected(self):
        self.assertEqual(
            "kuuos_current_status_surface_artifact_v0_75",
            CURRENT_STATUS_SURFACE_ARTIFACT_FRONTIER,
        )
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_current_status_surface_artifact_v0_75", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_75", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("current-status-surface-artifact-v0-75", text)
        self.assertIn("current-root-sequence-v0-75", text)


if __name__ == "__main__":
    unittest.main()
