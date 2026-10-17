"""Package selection must never repair missing old roots by importing them."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts.formal_package_boundary import (
    CURRENT, LEGACY, SNAPSHOT_BLOBS, git_blob_sha, package_directory, historical_aggregate,
    historical_lakefile, validate_targets,
)

class FormalPackageBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for package in ('', 'legacy/v5.291'):
            base = self.root / package
            base.mkdir(parents=True, exist_ok=True)
            (base / 'lakefile.toml').write_text(
                '[[lean_lib]]\nname = "KuuOSFormal"\nroots = ["KuuOSFormal", "Kuu", "KuuOSStrict", "KUOS", "KuuOSOld"]\n')
            (base / 'lean-toolchain').write_text('leanprover/lean4:v4.30.0-rc2\n')
            (base / 'lake-manifest.json').write_text('{}\n')
        for name in ('formal/KuuOSFormal.lean', 'legacy/v5.291/formal/KuuOSFormal.lean'):
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('import KuuOSStrict\n' if name.startswith('formal/') else 'import KUOS\n')

    def test_current_is_default_and_keeps_independent_root(self):
        self.assertEqual(package_directory(self.root, CURRENT), self.root)
        validate_targets(self.root, CURRENT, ['KuuOSFormal', 'Kuu.Strict'])

    def test_retained_target_in_current_package_is_available(self):
        validate_targets(self.root, CURRENT, ['KUOS.WORLD.Old'])

    def test_unknown_target_is_rejected_instead_of_fallback(self):
        with self.assertRaises(ValueError):
            validate_targets(self.root, CURRENT, ['SomethingElse'])

    def test_explicit_legacy_uses_separate_directory(self):
        self.assertEqual(package_directory(self.root, LEGACY), self.root / 'legacy/v5.291')
        path = self.root / 'legacy/v5.291/lakefile.toml'
        with patch.dict(SNAPSHOT_BLOBS, {'lakefile.toml': git_blob_sha(path.read_bytes())}):
            validate_targets(self.root, LEGACY, ['KUOS.WORLD.Old', 'KuuOSOld'])

    def test_new_core_cannot_be_built_as_legacy(self):
        path = self.root / 'legacy/v5.291/lakefile.toml'
        with patch.dict(SNAPSHOT_BLOBS, {'lakefile.toml': git_blob_sha(path.read_bytes())}):
            with self.assertRaisesRegex(ValueError, 'not a published target'):
                validate_targets(self.root, LEGACY, ['NotAnArchivedRoot.Strict'])

    def test_historical_aggregate_does_not_read_current_imports(self):
        expected = git_blob_sha(b'import KUOS\n')
        with patch.dict(SNAPSHOT_BLOBS, {'formal/KuuOSFormal.lean': expected}):
            historical = historical_aggregate(self.root)
        self.assertEqual(historical.read_text(), 'import KUOS\n')
        self.assertEqual((self.root / 'formal/KuuOSFormal.lean').read_text(), 'import KuuOSStrict\n')

    def test_historical_lakefile_is_selected_explicitly(self):
        path = self.root / 'legacy/v5.291/lakefile.toml'
        with patch.dict(SNAPSHOT_BLOBS, {'lakefile.toml': git_blob_sha(path.read_bytes())}):
            self.assertEqual(historical_lakefile(self.root), path)

    def test_fabricated_snapshot_fails_integrity_check(self):
        with self.assertRaisesRegex(ValueError, 'snapshot'):
            historical_aggregate(self.root)
        with self.assertRaisesRegex(ValueError, 'snapshot'):
            historical_lakefile(self.root)

    def test_no_directory_traversal_target(self):
        with self.assertRaises(ValueError):
            validate_targets(self.root, LEGACY, ['../KuuOSFormal'])

    def test_missing_archive_is_not_replaced_with_current(self):
        (self.root / 'legacy/v5.291/formal/KuuOSFormal.lean').unlink()
        with self.assertRaises((ValueError, FileNotFoundError)):
            historical_aggregate(self.root)

class LakeInvocationBoundaryTests(unittest.TestCase):
    setUp = FormalPackageBoundaryTests.setUp

    def test_current_command_has_no_legacy_fallback(self):
        from scripts.run_formal_package import lake_command
        directory, command = lake_command(self.root, False, ['--', '-KleanArgs=-DsorryAsError=true', 'build', 'Kuu.Strict'])
        self.assertEqual(directory, self.root)
        self.assertEqual(command[-2:], ['build', 'Kuu.Strict'])

    def test_explicit_legacy_cwd_preserves_current_entry(self):
        from scripts.run_formal_package import lake_command
        updates={name:git_blob_sha((self.root/'legacy/v5.291'/name).read_bytes()) for name in SNAPSHOT_BLOBS}
        with patch.dict(SNAPSHOT_BLOBS, updates):
            directory, command=lake_command(self.root, True, ['build','KUOS.WORLD.Old'])
        self.assertEqual(directory,self.root/'legacy/v5.291')
        self.assertEqual(command,['lake','build','KUOS.WORLD.Old'])
        self.assertEqual((self.root/'formal/KuuOSFormal.lean').read_text(),'import KuuOSStrict\n')

    def test_no_package_escape(self):
        from scripts.run_formal_package import lake_command
        for flag in ['--dir=..', '--file=other.toml', '--old']:
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                lake_command(self.root, False, [flag,'build','Kuu.Strict'])

if __name__ == '__main__':
    unittest.main()
