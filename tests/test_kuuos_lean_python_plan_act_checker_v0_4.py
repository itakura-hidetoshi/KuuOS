"""Static-checker mechanism tests with explicit synthetic source pins."""
from __future__ import annotations
import hashlib
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

CHECKER = 'scripts.check_kuuos_lean_python_plan_act_bindings_v0_4'


class CheckerAvailability(unittest.TestCase):
    def test_checker_exists(self):
        self.assertIsNotNone(importlib.util.find_spec(CHECKER))


class CheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = __import__(CHECKER, fromlist=['check_sources'])

    def sample(self, root, source=b'def validate():\n    return []\n'):
        path = root / 'source.py'
        path.write_bytes(source)
        sha = hashlib.sha1(b'blob ' + str(len(source)).encode() + b'\0' + source).hexdigest()
        return {'source.py': sha}

    def test_missing_sources_are_no_data(self):
        with TemporaryDirectory() as folder, patch.object(self.m, 'SOURCE_BLOBS', {'missing': '0'*40}):
            result = self.m.check_sources(Path(folder), check_registration=False)
        self.assertEqual(result['status'], 'NO_DATA')
        self.assertFalse(result['formal_certified'])

    def test_drift_takes_precedence_over_missing(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            self.sample(root)
            with patch.object(self.m, 'SOURCE_BLOBS', {'source.py': '0'*40, 'missing': '0'*40}):
                result = self.m.check_sources(root, check_registration=False)
        self.assertEqual(result['status'], 'BLOCKED')
        self.assertTrue(result['missing'])

    def test_exact_pinned_test_bytes_match(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            pins = self.sample(root)
            with patch.object(self.m, 'SOURCE_BLOBS', pins):
                result = self.m.check_sources(root, check_registration=False)
        self.assertEqual(result['status'], 'SOURCE_BYTES_MATCH')
        self.assertFalse(result['formal_certified'])

    def test_comments_do_not_register_tests(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            p = root / self.m.RUNNER
            p.parent.mkdir(parents=True)
            p.write_text('# ' + repr(self.m.EXPECTED_STEPS) + '\nFRONTIER_STEPS_AFTER_V095 = ()\n')
            with patch.object(self.m, 'SOURCE_BLOBS', {}):
                result = self.m.check_sources(root)
        self.assertEqual(result['status'], 'BLOCKED')

    def test_actual_ast_registration_is_required(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            p = root / self.m.RUNNER
            p.parent.mkdir(parents=True)
            p.write_text('FRONTIER_STEPS_AFTER_V095: tuple = ' + repr(self.m.EXPECTED_STEPS) + '\n')
            for module in self.m.REQUIRED_TEST_MODULES:
                q = root / (module.replace('.', '/') + '.py')
                q.parent.mkdir(parents=True, exist_ok=True)
                q.write_text('import unittest\n')
            with patch.object(self.m, 'SOURCE_BLOBS', {}):
                result = self.m.check_sources(root)
        self.assertEqual(result['status'], 'STATIC_MATCH')

    def test_removing_prior_regression_is_blocked(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            p = root / self.m.RUNNER
            p.parent.mkdir(parents=True)
            p.write_text('FRONTIER_STEPS_AFTER_V095 = ' + repr(self.m.EXPECTED_STEPS[1:]) + '\n')
            with patch.object(self.m, 'SOURCE_BLOBS', {}):
                result = self.m.check_sources(root)
        self.assertEqual(result['status'], 'BLOCKED')


if __name__ == '__main__':
    unittest.main()
