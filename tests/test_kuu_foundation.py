"""Actual Gray dependencies are rejected; existing non-Gray proof imports are retained."""
import tempfile
import unittest
from pathlib import Path
from scripts.check_kuu_foundation import check, lean_imports

class FoundationBoundaryTest(unittest.TestCase):
    def fixture(self, files):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for name, text in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        return root

    def base(self, source='import Kuu.Presentation\n'):
        return {
            'lakefile.toml': 'name = "KuuOS"\ndefaultTargets = ["KuuOSFormal"]\n[[lean_lib]]\nname = "KuuOSFormal"\nsrcDir = "formal"\nroots = ["KuuOSFormal", "KuuOSStrict", "Kuu"]\n',
            'formal/KuuOSFormal.lean': 'import KuuOSStrict\n',
            'formal/KuuOSStrict.lean': source,
            'formal/Kuu.lean': 'import Kuu.Presentation\n',
            'formal/Kuu/Presentation.lean': 'import Mathlib.CategoryTheory.Quotient\n',
        }

    def test_independent_core_passes(self):
        self.assertTrue(check(self.fixture(self.base()))['ok'])

    def test_direct_legacy_import_is_rejected(self):
        files = self.base('import KUOS.GrayOld\n')
        files['formal/KUOS/GrayOld.lean'] = '-- Historical Gray comparison\n'
        report = check(self.fixture(files))
        self.assertFalse(report['ok'])
        self.assertIn('KUOS.GrayOld', str(report['errors']))

    def test_indirect_legacy_import_is_rejected(self):
        files = self.base()
        files['formal/Kuu/Presentation.lean'] = 'import Kuu.Hidden\n'
        files['formal/Kuu/Hidden.lean'] = 'import KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249\n'
        self.assertFalse(check(self.fixture(files))['ok'])

    def test_umbrella_mathlib_import_is_allowed(self):
        files = self.base()
        files['formal/Kuu/Presentation.lean'] = 'import Mathlib\n'
        self.assertTrue(check(self.fixture(files))['ok'])

    def test_mathlib_and_non_gray_import_can_coexist(self):
        files = self.base('import Mathlib\nimport KUOS.ExistingTransport\n')
        files['formal/KUOS/ExistingTransport.lean'] = 'import Mathlib.CategoryTheory.Functor.Basic\n'
        self.assertTrue(check(self.fixture(files))['ok'])

    def test_gray_still_rejected_with_full_mathlib_import(self):
        files = self.base('import Mathlib\nimport KUOS.GraySource\n')
        files['formal/KUOS/GraySource.lean'] = 'import Mathlib\n'
        self.assertFalse(check(self.fixture(files))['ok'])

    def test_all_mathlib_import_styles_preserve_boundary(self):
        files = self.base('import Mathlib Mathlib.CategoryTheory.Quotient\n')
        report = check(self.fixture(files))
        self.assertTrue(report['ok'], report['errors'])
        self.assertIn(['KuuOSStrict', 'Mathlib'], report['import_edges'])

    def test_unused_current_module_is_also_checked(self):
        files = self.base()
        files['formal/Kuu/Unused.lean'] = 'import KUOS.Old\n'
        self.assertFalse(check(self.fixture(files))['ok'])

    def test_unreferenced_library_root_is_checked(self):
        files = self.base()
        files['formal/Kuu.lean'] = 'import KUOS.Old\n'
        self.assertFalse(check(self.fixture(files))['ok'])

    def test_new_axiom_or_sorry_is_rejected(self):
        for bad in ['axiom fabricated : False', 'theorem fabricated : False := by sorry',
                    'theorem fabricated : False := by admit', 'example : True := by native_decide']:
            with self.subTest(bad=bad):
                files = self.base()
                files['formal/Kuu/Presentation.lean'] += bad + '\n'
                self.assertFalse(check(self.fixture(files))['ok'])

    def test_nested_comments_and_strings_do_not_become_imports(self):
        source = '/- import KUOS.Bad /- nested -/ -/\n-- import KUOS.Bad\n' \
                 'def message := "import KUOS.Bad sorry"\nimport\n  Kuu.Presentation\n'
        self.assertEqual(lean_imports(source), ['Kuu.Presentation'])
        self.assertTrue(check(self.fixture(self.base(source)))['ok'])

    def test_multiple_imports_and_public_imports_are_all_checked(self):
        self.assertEqual(lean_imports('public import Kuu.A Kuu.B\nimport Kuu.C\n'),
                         ['Kuu.A', 'Kuu.B', 'Kuu.C'])

    def test_missing_local_module_fails_closed(self):
        self.assertFalse(check(self.fixture(self.base('import Kuu.DoesNotExist\n')))['ok'])

    def test_legacy_default_target_is_rejected(self):
        files = self.base()
        files['lakefile.toml'] = files['lakefile.toml'].replace('["KuuOSFormal"]', '["KuuOSLegacy"]')
        self.assertFalse(check(self.fixture(files))['ok'])

    def test_legacy_files_are_not_destroyed_or_promoted(self):
        files = self.base()
        files['formal/KUOS/Old.lean'] = 'import KUOS.Earlier\n'
        root = self.fixture(files)
        report = check(root)
        self.assertTrue(report['ok'])
        self.assertEqual(report['legacy_source_files'], 1)
        self.assertTrue((root / 'formal/KUOS/Old.lean').exists())

    def test_current_source_cannot_escape_formal_directory(self):
        self.assertFalse(check(self.fixture(self.base('import ../KUOS/Old\n')))['ok'])

    def test_non_gray_existing_proof_can_be_used_without_namespace_ban(self):
        files = self.base('import KUOS.ExistingTransport\n')
        files['formal/KUOS/ExistingTransport.lean'] = 'import Mathlib\n'
        self.assertTrue(check(self.fixture(files))['ok'])

    def test_gray_cannot_hide_behind_a_non_gray_module_name(self):
        files = self.base('import KUOS.ExistingTransport\n')
        files['formal/KUOS/ExistingTransport.lean'] = 'import KUOS.GraySource\n'
        files['formal/KUOS/GraySource.lean'] = 'import Mathlib\n'
        self.assertFalse(check(self.fixture(files))['ok'])

    def test_public_aggregate_cannot_become_a_core_dependency(self):
        files = self.base('import KuuOSFormal\n')
        self.assertFalse(check(self.fixture(files))['ok'])

if __name__ == '__main__':
    unittest.main()
