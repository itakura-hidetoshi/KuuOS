from __future__ import annotations

import unittest

from runtime import kuuos_root_map_status_v0_47 as status


class RootMapStatusV047Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(status.VERSION, "kuuos_root_map_status_v0_47")
        self.assertEqual(status.DEPENDS_ON, "kuuos_root_map_ledger_v0_46")
        self.assertEqual(status.CURRENT_CHECK, "runtime/kuuos_current_check.py")

    def test_rows_are_unique(self) -> None:
        self.assertEqual(len(status.row_ids()), len(set(status.row_ids())))
        self.assertEqual(len(status.items()), len(set(status.items())))

    def test_rows_include_current_layers(self) -> None:
        self.assertIn("root", status.row_ids())
        self.assertIn("sequence", status.row_ids())
        self.assertIn("map", status.row_ids())
        self.assertIn("ledger", status.row_ids())
        self.assertIn("status", status.row_ids())

    def test_checks_name_current_tests(self) -> None:
        self.assertIn("tests.test_kuuos_root_map_v0_45", status.checks())
        self.assertIn("tests.test_kuuos_root_map_ledger_v0_46", status.checks())
        self.assertIn("tests.test_kuuos_root_map_status_v0_47", status.checks())

    def test_status_verifies(self) -> None:
        self.assertEqual(status.status_issues(), ())
        self.assertTrue(status.verify_root_map_status())

    def test_markdown_names_self(self) -> None:
        markdown = status.as_markdown()
        self.assertIn("status", markdown)
        self.assertIn("runtime/kuuos_root_map_status_v0_47.py", markdown)


if __name__ == "__main__":
    unittest.main()
