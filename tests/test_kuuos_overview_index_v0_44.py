from __future__ import annotations

import unittest

from runtime import kuuos_overview_index_v0_44 as overview


class OverviewIndexV044Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(overview.VERSION, "kuuos_overview_index_v0_44")
        self.assertEqual(overview.DEPENDS_ON, "kuuos_docs_index_v0_43")
        self.assertEqual(overview.CURRENT_CHECK, "runtime/kuuos_current_check.py")

    def test_overview_entries_are_unique(self) -> None:
        self.assertEqual(len(overview.entry_ids()), len(set(overview.entry_ids())))
        self.assertEqual(len(overview.entry_paths()), len(set(overview.entry_paths())))

    def test_overview_entries_include_current_layers(self) -> None:
        self.assertIn("runtime/kuuos_current_check.py", overview.entry_paths())
        self.assertIn("runtime/kuuos_current_root_sequence_v0_41.py", overview.entry_paths())
        self.assertIn("runtime/kuuos_manifest_index_v0_42.py", overview.entry_paths())
        self.assertIn("runtime/kuuos_docs_index_v0_43.py", overview.entry_paths())
        self.assertIn("runtime/kuuos_overview_index_v0_44.py", overview.entry_paths())

    def test_overview_index_verifies(self) -> None:
        self.assertEqual(overview.overview_issues(), ())
        self.assertTrue(overview.verify_overview_index())

    def test_markdown_names_self_check(self) -> None:
        markdown = overview.as_markdown()
        self.assertIn("overview-index", markdown)
        self.assertIn("tests.test_kuuos_overview_index_v0_44", markdown)


if __name__ == "__main__":
    unittest.main()
