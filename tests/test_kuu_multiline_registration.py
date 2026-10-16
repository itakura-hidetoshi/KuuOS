"""Historical registration checks must inspect the same package they compile."""
from pathlib import Path
import json
import re
import shutil
import subprocess
import tempfile
import unittest

from tests.test_kuu_legacy_ci_integration import FOCUSED

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ('world-four-great-phase-dynamics-v0-59.yml', 'Verify aggregate formal registration', 2),
    ('qi-process-tensor-local-real-yinyang-v2-4-validation.yml',
     'Verify formal registration and dependency boundary', 5),
    ('qi-world-yinyang-process-blocker-v2-3-validation.yml',
     'Verify formal registration and dependencies', 3),
)

DIAGNOSTICS_CASES = CASES
CASES += tuple((name, 'Verify package-local formal boundary', 2) for name in FOCUSED)


def command(name, step):
    text = (ROOT / '.github/workflows' / name).read_text()
    block = text.split('      - name: ' + step + '\n', 1)[1].split('        run: |\n', 1)[1]
    lines = []
    for line in block.splitlines():
        if line and not line.startswith('          '):
            break
        lines.append(line[10:] if line else '')
    return '\n'.join(lines)


class MultilineRegistrationTests(unittest.TestCase):
    def test_all_scoped_registration_commands_use_compiled_package(self):
        paths = json.loads((ROOT / 'ci/kuu_legacy_consumer_scope.json').read_text())['paths']
        for name in paths:
            if not name.startswith('.github/workflows/'):
                continue
            text = re.sub(r'\\\n\s*', ' ', (ROOT / name).read_text())
            for line in text.splitlines():
                if re.search(r'\bgrep\b', line):
                    with self.subTest(path=name, line=line.strip()):
                        self.assertNotRegex(line, r'(?<![\w/.])formal/[^\s]+\.lean')

    def test_original_assertions_are_retained(self):
        for name, step, count in CASES:
            with self.subTest(path=name):
                self.assertEqual(command(name, step).count('grep -Fq'), count)
                self.assertIn('set -euo pipefail', command(name, step))

    def run_registration(self, name, step, missing=None):
        # Use actual preserved source, but leave the current formal tree absent.
        body = command(name, step)
        logical = re.sub(r'\\\n\s*', ' ', body)
        paths = re.findall(r'legacy/v5\.291/formal/[^\s]+\.lean', logical)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'artifacts/diagnostics').mkdir(parents=True)
            for path in paths:
                dst = root / path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, dst)
            if missing is not None:
                (root / paths[missing]).write_text('')
            result = subprocess.run(['bash', '-euo', 'pipefail', '-c', body],
                                    cwd=root, text=True, capture_output=True, check=False)
        return result, paths

    def test_registration_succeeds_with_legacy_only(self):
        for name, step, _ in CASES:
            with self.subTest(path=name):
                result, _ = self.run_registration(name, step)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_every_missing_legacy_input_is_rejected(self):
        for name, step, _ in CASES:
            _, paths = self.run_registration(name, step)
            self.assertTrue(paths, 'registration must inspect the compiled legacy sources')
            for index, path in enumerate(paths):
                with self.subTest(workflow=name, missing=path):
                    result, _ = self.run_registration(name, step, missing=index)
                    self.assertNotEqual(result.returncode, 0)

    def test_version_diagnostics_do_not_call_unsupported_runner_subcommand(self):
        for name, _, _ in DIAGNOSTICS_CASES:
            with self.subTest(path=name):
                text = (ROOT / '.github/workflows' / name).read_text()
                self.assertIn('command lake --version || true', text)
                self.assertNotIn('scripts/run_formal_package.py --legacy -- --version', text)


if __name__ == '__main__':
    unittest.main()
