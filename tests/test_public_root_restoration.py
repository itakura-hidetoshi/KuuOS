"""Regression: retiring Gray as foundation must not unpublish existing proofs."""
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PublicRootRestorationTests(unittest.TestCase):
    def test_every_previous_public_root_remains_published(self):
        old = tomllib.loads((ROOT / 'legacy/v5.291/lakefile.toml').read_text())
        new = tomllib.loads((ROOT / 'lakefile.toml').read_text())
        wanted = {r for lib in old['lean_lib'] for r in lib.get('roots', [])}
        actual = {r for lib in new['lean_lib'] for r in lib.get('roots', [])}
        self.assertEqual(wanted - actual, set(),
                         'Existing public proofs were blanket-excluded from the current Lake package')

if __name__ == '__main__':
    unittest.main()
