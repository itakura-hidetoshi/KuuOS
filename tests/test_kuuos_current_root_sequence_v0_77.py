import unittest

from runtime.kuuos_current_root_sequence_v0_77 import (
    CURRENT_SURFACE_ENTRYPOINT_FRONTIER,
    STABLE_CURRENT_SURFACE_CLI,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV077Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_current_surface_entrypoint_is_connected(self):
        self.assertEqual("kuuos_current_surface_entrypoint_v0_77", CURRENT_SURFACE_ENTRYPOINT_FRONTIER)
        self.assertEqual("runtime/kuuos_current_surface.py", STABLE_CURRENT_SURFACE_CLI)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_current_surface_entrypoint_v0_77", targets)
        self.assertIn("tests.test_kuuos_current_surface_cli_v0_77", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_77", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("current-surface-entrypoint-v0-77", text)
        self.assertIn("current-surface-cli-v0-77", text)
        self.assertIn("current-root-sequence-v0-77", text)


if __name__ == "__main__":
    unittest.main()
