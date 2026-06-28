#!/usr/bin/env python3
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_pr_entry_check_v0_4 import CHECK_IDS, build_commands


class PrEntryCheckTests(unittest.TestCase):
    def test_registered_ids_have_commands(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.assertEqual(len(CHECK_IDS), 5)
            for check_id in CHECK_IDS:
                commands = build_commands(check_id, root / check_id)
                self.assertTrue(commands)
                self.assertLessEqual(len(commands), 8)

    def test_unknown_id_is_rejected(self):
        with self.assertRaises(ValueError):
            build_commands("unknown", pathlib.Path("artifacts/checks/unknown"))


if __name__ == "__main__":
    unittest.main()
