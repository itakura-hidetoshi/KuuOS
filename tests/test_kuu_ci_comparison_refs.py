"""Exercise CI comparisons against real Git repositories, not mocked fetches."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/ensure_ci_comparison.py'


class CIComparisonTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.remote = self.root / 'remote'
        self.remote.mkdir()
        self.git(self.remote, 'init', '-q', '-b', 'main')
        self.git(self.remote, 'config', 'user.name', 'CI test')
        self.git(self.remote, 'config', 'user.email', 'ci@example.invalid')
        (self.remote / 'file').write_text('base\n')
        self.git(self.remote, 'add', '.')
        self.git(self.remote, 'commit', '-qm', 'base')
        self.base = self.git(self.remote, 'rev-parse', 'HEAD').stdout.strip()
        self.git(self.remote, 'checkout', '-qb', 'feature')
        (self.remote / 'file').write_text('head\n')
        self.git(self.remote, 'commit', '-qam', 'head')
        self.head = self.git(self.remote, 'rev-parse', 'HEAD').stdout.strip()
        self.local = self.root / 'local'
        self.local.mkdir()
        self.git(self.local, 'init', '-q')
        # No fetch refspec: a fetch of an object cannot create origin/main.
        self.git(self.local, 'config', 'remote.origin.url', str(self.remote))

    def git(self, directory, *args, check=True):
        return subprocess.run(['git', *args], cwd=directory, text=True,
                              capture_output=True, check=check)

    def ensure(self, base=None, head=None):
        return subprocess.run([sys.executable, str(SCRIPT),
                               '--base', base or self.base, '--head', head or self.head],
                              cwd=self.local, text=True, capture_output=True)

    def test_all_check_registry_fragments_parse(self):
        fragments = sorted((ROOT / 'ci/check_registry.d').glob('*.json'))
        self.assertTrue(fragments)
        for path in fragments:
            with self.subTest(path=path.name):
                payload = json.loads(path.read_text(encoding='utf-8'))
                self.assertEqual(payload['schema_version'], '0.2')
                self.assertTrue(payload['checks'])

    def test_missing_objects_are_fetched_without_tracking_aliases(self):
        result = self.ensure()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git(self.local, 'rev-parse', self.base).stdout.strip(), self.base)
        self.assertEqual(self.git(self.local, 'rev-parse', self.head).stdout.strip(), self.head)
        self.assertNotEqual(self.git(self.local, 'rev-parse', '--verify',
                                    'refs/remotes/origin/main', check=False).returncode, 0)
        self.assertEqual(self.git(self.local, 'diff', '--name-only',
                                 f'{self.base}...{self.head}').stdout.strip(), 'file')

    def test_present_objects_do_not_require_network(self):
        self.git(self.local, 'fetch', '-q', '--no-tags', 'origin', self.head)
        self.git(self.local, 'config', 'remote.origin.url', str(self.root / 'unavailable'))
        result = self.ensure()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unavailable_exact_object_does_not_use_fetch_head(self):
        self.git(self.local, 'fetch', '-q', '--no-tags', 'origin', self.head)
        result = self.ensure(base='a' * 40)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('comparison', result.stderr.lower())

    def test_untrusted_ref_name_is_rejected_before_git(self):
        result = self.ensure(base='--upload-pack=wrong')
        self.assertNotEqual(result.returncode, 0)

    def test_tree_object_cannot_substitute_for_a_commit(self):
        tree = self.git(self.remote, 'rev-parse', 'HEAD^{tree}').stdout.strip()
        result = self.ensure(base=tree)
        self.assertNotEqual(result.returncode, 0)

    def test_unrelated_histories_cannot_be_used_for_three_dot_diff(self):
        self.git(self.remote, 'checkout', '--orphan', 'unrelated')
        self.git(self.remote, 'commit', '-qm', 'unrelated')
        unrelated = self.git(self.remote, 'rev-parse', 'HEAD').stdout.strip()
        result = self.ensure(base=unrelated)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('comparison', result.stderr.lower())


if __name__ == '__main__':
    unittest.main()
