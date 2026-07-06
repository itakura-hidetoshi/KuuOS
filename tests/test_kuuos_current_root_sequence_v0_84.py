import unittest

from runtime.kuuos_current_root_sequence_v0_84 import (
    NEXT_REQUEST_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV084Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_next_request_frontier_is_connected(self):
        self.assertEqual("kuuos_self_organization_next_request_v0_84", NEXT_REQUEST_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_next_request_v0_84", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_84", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("next-request-v0-84", text)
        self.assertIn("current-root-sequence-v0-84", text)


if __name__ == "__main__":
    unittest.main()
