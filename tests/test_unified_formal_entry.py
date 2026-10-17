"""The published proof universe has one canonical Lake entry, not distinct ranks of authority."""
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]

class UnifiedFormalEntryTests(unittest.TestCase):
    def test_previous_roots_preserved_with_no_separate_kuu_root(self):
        baseline = tomllib.loads((ROOT / 'legacy/v5.291/lakefile.toml').read_text())
        current = tomllib.loads((ROOT / 'lakefile.toml').read_text())
        prior = [r for lib in baseline['lean_lib'] for r in lib['roots']]
        now = [r for lib in current['lean_lib'] for r in lib['roots']]
        self.assertTrue(set(prior).issubset(set(now)))
        self.assertFalse({"Kuu", "KuuOSStrict"} & set(now))
        self.assertEqual(current['defaultTargets'], ['KuuOSFormal'])

    def test_kuu_proofs_reachable_from_same_standard_aggregate(self):
        content = (ROOT / 'formal/KuuOSFormal.lean').read_text()
        self.assertIn('import KuuOSStrict', content)
        internal = (ROOT / 'formal/KuuOSStrict.lean').read_text()
        self.assertIn('import Kuu.Presentation', internal)
        self.assertIn('import Kuu.Strict', internal)
        self.assertIn('import Kuu.Incidence', internal)

if __name__ == '__main__':
    unittest.main()
