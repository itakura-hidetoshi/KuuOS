import unittest

from runtime.kuuos_current_root_sequence_v0_71 import (
    CURRENT_STATUS_RESOLVER_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV071Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_current_status_resolver_frontier_is_connected(self):
        self.assertEqual("kuuos_current_status_resolver_v0_71", CURRENT_STATUS_RESOLVER_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_current_status_resolver_v0_71", targets)
        self.assertIn("tests.test_kuuos_current_status_cli_v0_71", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_71", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("current-status-resolver-v0-71", text)
        self.assertIn("current-status-cli-v0-71", text)
        self.assertIn("current-root-sequence-v0-71", text)


if __name__ == "__main__":
    unittest.main()
