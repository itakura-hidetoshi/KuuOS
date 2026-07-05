import unittest

from runtime.kuuos_current_root_sequence_v0_70 import (
    CURRENT_STATUS_POINTER_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV070Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_current_status_pointer_frontier_is_connected(self):
        self.assertEqual("kuuos_current_status_pointer_v0_70", CURRENT_STATUS_POINTER_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_current_status_pointer_v0_70", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_70", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("current-status-pointer-v0-70", text)
        self.assertIn("current-root-sequence-v0-70", text)


if __name__ == "__main__":
    unittest.main()
