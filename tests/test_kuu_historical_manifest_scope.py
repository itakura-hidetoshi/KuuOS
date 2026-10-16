"""All recorded historical formal contracts have an explicit package, not auto-repair rights."""
import json
from pathlib import Path
import unittest
import tomllib

from scripts.check_kuuos_repository_live_v079 import MANIFESTS

ROOT = Path(__file__).resolve().parents[1]


class HistoricalManifestScopeTests(unittest.TestCase):
    def test_all_recorded_contracts_have_explicit_legacy_scope(self):
        for name in MANIFESTS:
            with self.subTest(manifest=name):
                payload = json.loads((ROOT / name).read_text(encoding='utf-8'))
                self.assertEqual(payload.get('formal_package'), 'legacy-v5.291')

    def test_formal_scope_does_not_opt_read_only_contracts_into_auto_repair(self):
        # v0.86--v0.95 are read-only formal contracts. Tagging their package is
        # not permission to execute a repair or change a repository reference.
        for name in MANIFESTS:
            if int(name.rsplit('_', 1)[1].removesuffix('.json')) < 86:
                continue
            with self.subTest(manifest=name):
                payload = json.loads((ROOT / name).read_text(encoding='utf-8'))
                self.assertIsNot(payload.get('repository_autorepair_contract'), True)
                self.assertTrue(payload['strict_formal_root'].startswith('KuuOSRepository'))
                self.assertTrue(all(x.startswith('KUOS.WORLD.')
                                    for x in payload['aggregate_lean_modules']))


class CurrentLeanCompilerOptionsTests(unittest.TestCase):
    def test_actual_library_compiler_rejects_warnings(self):
        config = tomllib.loads((ROOT / 'lakefile.toml').read_text(encoding='utf-8'))
        library = next(lib for lib in config['lean_lib'] if lib['name'] == 'KuuOSFormal')
        self.assertIs(library.get('leanOptions', {}).get('warningAsError'), True)


if __name__ == '__main__':
    unittest.main()
