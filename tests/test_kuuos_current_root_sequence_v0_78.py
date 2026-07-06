import unittest

from runtime.kuuos_current_root_sequence_v0_78 import (
    README_SURFACE_EXPOSURE_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV078Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_readme_surface_exposure_frontier_is_connected(self):
        self.assertEqual("kuuos_readme_surface_exposure_v0_78", README_SURFACE_EXPOSURE_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_readme_surface_status_v0_78", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_78", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("readme-surface-exposure-v0-78", text)
        self.assertIn("current-root-sequence-v0-78", text)


if __name__ == "__main__":
    unittest.main()
