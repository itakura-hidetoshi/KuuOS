from __future__ import annotations

import unittest

from runtime import kuuos_root_map_ledger_v0_46 as ledger


class RootMapLedgerV046Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(ledger.VERSION, "kuuos_root_map_ledger_v0_46")
        self.assertEqual(ledger.DEPENDS_ON, "kuuos_root_map_v0_45")
        self.assertEqual(ledger.CURRENT_CHECK, "runtime/kuuos_current_check.py")

    def test_rows_are_unique(self) -> None:
        self.assertEqual(len(ledger.row_ids()), len(set(ledger.row_ids())))
        self.assertEqual(len(ledger.row_sources()), len(set(ledger.row_sources())))

    def test_rows_include_current_root_and_map(self) -> None:
        self.assertIn("current-check", ledger.row_ids())
        self.assertIn("root-sequence", ledger.row_ids())
        self.assertIn("root-map", ledger.row_ids())
        self.assertIn("root-map-ledger", ledger.row_ids())

    def test_checks_name_tests(self) -> None:
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_41", ledger.row_checks())
        self.assertIn("tests.test_kuuos_root_map_v0_45", ledger.row_checks())
        self.assertIn("tests.test_kuuos_root_map_ledger_v0_46", ledger.row_checks())

    def test_ledger_verifies(self) -> None:
        self.assertEqual(ledger.ledger_issues(), ())
        self.assertTrue(ledger.verify_root_map_ledger())

    def test_markdown_names_self(self) -> None:
        markdown = ledger.as_markdown()
        self.assertIn("root-map-ledger", markdown)
        self.assertIn("runtime/kuuos_root_map_ledger_v0_46.py", markdown)


if __name__ == "__main__":
    unittest.main()
