import unittest

from runtime.kuuos_current_root_sequence_v0_72 import (
    RESOLVED_STATUS_ARTIFACT_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV072Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_resolved_status_artifact_frontier_is_connected(self):
        self.assertEqual(
            "kuuos_current_resolved_status_artifact_v0_72",
            RESOLVED_STATUS_ARTIFACT_FRONTIER,
        )
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_current_resolved_status_artifact_v0_72", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_72", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("current-resolved-status-artifact-v0-72", text)
        self.assertIn("current-root-sequence-v0-72", text)


if __name__ == "__main__":
    unittest.main()
