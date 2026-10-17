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

class RestoredWiringTests(unittest.TestCase):
    def test_publication_and_consumer_routes_are_restored(self):
        from scripts.check_public_proof_roots import check
        report = check(ROOT)
        self.assertTrue(report['ok'], report['errors'])
        self.assertEqual(report['previous_public_roots'], 107)

    def test_original_theorem_files_are_unmodified(self):
        # Byte preservation is not a request to re-prove the old theorems.
        before = ROOT / 'legacy/v5.291/formal'
        for old in before.rglob('*.lean'):
            rel = old.relative_to(before)
            if str(rel) == 'KuuOSFormal.lean':
                continue  # aggregate imports restored alongside the independent core
            with self.subTest(path=str(rel)):
                self.assertEqual((ROOT / 'formal' / rel).read_bytes(), old.read_bytes())

    def test_lean_mathlib_pins_are_unchanged(self):
        for name in ('lean-toolchain', 'lake-manifest.json'):
            self.assertEqual((ROOT / name).read_bytes(),
                             (ROOT / 'legacy/v5.291' / name).read_bytes())

    def test_retained_theorems_are_current_package_targets(self):
        from scripts.formal_package_boundary import validate_targets, CURRENT
        validate_targets(ROOT, CURRENT, [
            'KUOS.DependentOriginationContextualCoreV1_0',
            'KUOS.DependentOriginationAdmissibleNonfactorizationV4_01',
            'KuuOSCodeAIV0_1'])

    def test_gray_is_not_a_prerequisite_of_independent_core(self):
        from scripts.check_kuu_foundation import check
        report = check(ROOT)
        self.assertTrue(report['ok'], report['errors'])
        self.assertNotIn('KuuOSFormal', report['current_modules'])

if __name__ == '__main__':
    unittest.main()
