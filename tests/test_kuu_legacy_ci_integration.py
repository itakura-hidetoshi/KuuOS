"""Regressions for the legacy CI failures observed on PR2338.

These tests retain historical assertions without adding imports to current Kuu.
They do not replace strict Lean compilation or exact-head integrated CI.
"""
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / '.github/workflows'
LEGACY = 'legacy/v5.291/'
FOCUSED = (
    'qi-yinyang-wuxing-fibonacci-history-v2-5-validation.yml',
    'qi-wuxing-generation-control-coherence-v2-6-validation.yml',
    'qi-wuxing-relation-word-protected-history-v2-7-validation.yml',
    'qi-wuxing-phase-projection-quotient-kernel-v2-8-validation.yml',
    'qi-wuxing-addcon-first-isomorphism-v2-9-validation.yml',
    'qi-wuxing-phase-observation-universal-property-v3-0-validation.yml',
)
BRIDGES = (
    'kuuos-github-mcp-server-bridge-formal-v0-1-validation.yml',
    'kuuos-github-mcp-server-bridge-formal-v0-2-validation.yml',
    'kuuos-github-mcp-live-write-verification-formal-v0-3-validation.yml',
)
REGISTRATIONS = (
    ('kuuos-gauge-field-self-organization-v0-60.yml',
     'KUOS.WORLD.KuuOSGaugeFieldSelfOrganizationV0_60', 'KuuOSFormalV0_60'),
    ('kuuos-os-associated-gauge-fields-v0-61.yml',
     'KUOS.WORLD.KuuOSOSAssociatedGaugeFieldsV0_61', 'KuuOSFormalV0_61'),
)


def workflow(name: str) -> str:
    return (WORKFLOWS / name).read_text(encoding='utf-8')


def job_bodies(text: str) -> list[str]:
    """Separate the explicitly indented jobs in these fixed workflow fixtures."""
    jobs = text.split('\njobs:\n', 1)[1]
    return re.split(r'(?m)^  [A-Za-z0-9_-]+:\n', jobs)[1:]


def registration_command(name: str) -> str:
    match = re.search(
        r'^      - name: Verify canonical registration\n'
        r'        shell: bash\n        run: \|\n'
        r'(?P<run>(?:          .*\n)+)', workflow(name), re.MULTILINE)
    if match is None:
        raise AssertionError('historical registration step was removed or changed')
    return '\n'.join(line[10:] for line in match['run'].splitlines())


class LegacyCIIntegrationTests(unittest.TestCase):
    def test_python_setup_precedes_execution_in_each_legacy_job(self):
        for name in FOCUSED + BRIDGES:
            bodies = [body for body in job_bodies(workflow(name))
                      if 'scripts/run_formal_package.py' in body]
            self.assertTrue(bodies, name)
            for index, body in enumerate(bodies):
                with self.subTest(workflow=name, job=index):
                    setup = re.search(
                        r'uses: actions/setup-python@[^\n]+\n'
                        r'        with:\n          python-version: [\'"]3\.12[\'"]', body)
                    self.assertIsNotNone(setup, 'the same job needs Python with tomllib')
                    self.assertLess(setup.start(), body.index('scripts/run_formal_package.py'))

    def test_conditional_dependency_updates_use_legacy_package(self):
        for name in FOCUSED:
            with self.subTest(workflow=name):
                text = workflow(name)
                self.assertIn('if python3 scripts/run_formal_package.py --legacy -- update; then', text)
                self.assertNotRegex(text, r'\bif\s+lake\s+update\b')

    def test_focused_caches_match_legacy_working_directory(self):
        for name in FOCUSED:
            with self.subTest(workflow=name):
                text = workflow(name)
                self.assertIn('            legacy/v5.291/.lake/packages\n', text)
                self.assertIn('            legacy/v5.291/.lake/build\n', text)
                self.assertIn('key: kuuos-legacy-v5291-lean-v2-', text)
                self.assertIn("hashFiles('legacy/v5.291/lean-toolchain', 'legacy/v5.291/lake-manifest.json')", text)

    def test_registration_keeps_all_original_assertions(self):
        for name, module, target in REGISTRATIONS:
            with self.subTest(workflow=name):
                command = registration_command(name)
                self.assertEqual(command.count('grep -Fq'), 3)
                self.assertEqual(command.count('import ' + module), 2)
                self.assertIn('"' + target + '"', command)

    def run_registration(self, name: str, module: str, target: str,
                         *, missing_legacy_import: bool) -> subprocess.CompletedProcess:
        token = 'import ' + module
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = {
                'formal/KUOS.lean': token + '\n',
                'formal/KuuOSFormal.lean': 'import KuuOSStrict\n',
                'lakefile.toml': 'name = "KuuOS"\n',
                LEGACY + 'formal/KUOS.lean': token + '\n',
                LEGACY + 'formal/KuuOSFormal.lean': '' if missing_legacy_import else token + '\n',
                LEGACY + 'lakefile.toml': 'roots = ["' + target + '"]\n',
            }
            for path, content in files.items():
                destination = root / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(content, encoding='utf-8')
            return subprocess.run(['bash', '-euo', 'pipefail', '-c', registration_command(name)],
                                  cwd=root, text=True, capture_output=True, check=False)

    def test_registration_accepts_legacy_without_current_imports(self):
        for name, module, target in REGISTRATIONS:
            with self.subTest(workflow=name):
                result = self.run_registration(name, module, target, missing_legacy_import=False)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_registration_still_rejects_missing_legacy_import(self):
        for name, module, target in REGISTRATIONS:
            with self.subTest(workflow=name):
                result = self.run_registration(name, module, target, missing_legacy_import=True)
                self.assertNotEqual(result.returncode, 0)

    def test_diagnostics_can_read_lake_version(self):
        text = workflow(BRIDGES[0])
        self.assertIn('            command lake --version || true\n', text)
        self.assertNotIn('scripts/run_formal_package.py --legacy -- --version', text)

    def test_f112_parent_cache_is_seeded_only_after_strict_validation(self):
        text = workflow('lean-formal-validation.yml')
        self.assertIn('      - formal/v5-293-f112-independent-total-change\n', text)
        self.assertIn('runs-on: ubuntu-24.04', text)
        self.assertIn('uses: actions/cache/restore@v5', text)
        self.assertIn('uses: actions/cache/save@v5', text)
        self.assertIn('Save verified main Lake workspace cache', text)
        self.assertIn('Save verified F112 parent project build cache', text)
        self.assertIn('Restore prior verified F112 parent project build', text)
        self.assertIn('path: .lake/build', text)
        self.assertIn("steps.f112-parent-build.outputs.cache-primary-key", text)
        self.assertIn('Warm latest F112 historical bridge for child PRs', text)
        self.assertIn('HistoricalF36F40BridgeP([0-9]+)', text)
        self.assertIn('bash scripts/build_lean4.sh --no-update --no-cache', text)
        self.assertIn('Resolve pinned Lake dependencies only when missing', text)
        self.assertIn('git diff --exit-code -- lake-manifest.json lean-toolchain', text)

    def test_child_pr_lean_checks_read_exact_base_before_fallback(self):
        text = workflow('pr-governance-gate.yml')
        self.assertIn('Restore validated parent/main Lake workspace cache', text)
        self.assertIn('key: kuuos-lake-', text)
        self.assertIn("hashFiles('lake-manifest.json') }}-${{ github.event.pull_request.base.sha || github.sha }}", text)
        self.assertIn('uses: actions/cache/restore@v5', text)
        self.assertIn('Restore verified F112 parent project build overlay', text)
        self.assertIn('kuuos-f112-base-build-', text)
        self.assertIn('Save PR-local Lean build overlay', text)
        self.assertIn('path: .lake/build', text)
        self.assertIn('use-mathlib-cache: false', text)
        self.assertIn('use-github-cache: false', text)

    def test_independent_ci_restores_shared_cache_without_duplicate_save(self):
        text = workflow('kuu-independent-foundation.yml')
        self.assertIn('Restore base-branch Lake workspace (read-only)', text)
        self.assertIn('Restore shared lean-action Lake snapshot (read-only)', text)
        self.assertEqual(text.count('uses: actions/cache/restore@v5'), 3)
        self.assertIn('Restore validated F112 parent project build (read-only)', text)
        self.assertIn('kuuos-f112-base-build-', text)
        self.assertNotIn('uses: actions/cache/save@v5', text)
        self.assertNotIn('use-github-cache: true', text)
        self.assertIn('use-github-cache: false', text)
        self.assertIn('use-mathlib-cache: false', text)
        self.assertIn('Resolve pinned Lake dependencies only when missing', text)
        self.assertIn('build KuuOSStrict', text)
        self.assertIn('scripts/run_kuu_foundation_check.py', text)

    def test_cold_cache_recovery_verifies_real_pinned_files(self):
        # A prefix cache match is insufficient when the local Mathlib checkout
        # or its compiled oleans are absent; keep the canonical pins unchanged.
        for name in ('lean-formal-validation.yml', 'pr-governance-gate.yml',
                     'kuu-independent-foundation.yml'):
            with self.subTest(workflow=name):
                text = workflow(name)
                self.assertIn('Resolve pinned Lake dependencies only when missing', text)
                self.assertIn('if [[ ! -d .lake/packages/mathlib ]]; then', text)
                self.assertIn('lake update', text)
                self.assertIn(
                    'if [[ ! -f .lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ]]; then',
                    text)
                self.assertIn('lake exe cache get', text)
                self.assertIn('git diff --exit-code -- lake-manifest.json lean-toolchain',
                              text)

    def test_full_audit_cold_build_has_sufficient_timeout(self):
        # Workflow/cache changes select the whole strict aggregate even when
        # the F47 source heuristic is false, so avoid the previous 30m kill.
        text = workflow('pr-governance-gate.yml')
        self.assertIn("needs.select.outputs.full_audit_required == 'true'", text)
        self.assertIn("&& 100 ||", text)
        self.assertIn("needs.select.outputs.lean_fastpath == 'true' && 50 || 30",
                      text)

    def test_kudos_formal_aggregate_import_gets_cold_build_budget(self):
        # An import-only KuuOSStrict change can select full KuuOSFormal
        # without having historical F47 in the *changed path* set.
        text = workflow('pr-governance-gate.yml')
        self.assertIn('lean_aggregate_heavy: ${{ steps.fastpath.outputs.lean_aggregate_heavy }}', text)
        self.assertIn('aggregate_heavy = "KuuOSFormal" in lean_targets', text)
        self.assertIn('lean_aggregate_heavy={str(aggregate_heavy).lower()}', text)
        self.assertIn("needs.select.outputs.lean_aggregate_heavy == 'true'", text)
        self.assertIn("needs.select.outputs.lean_fastpath == 'true' && 50 || 30", text)

    def test_cancelled_lean_does_not_publish_incomplete_pr_cache(self):
        text = workflow('pr-governance-gate.yml')
        self.assertIn(
            "if: always() && !cancelled() && github.event_name == 'pull_request'",
            text)

    def test_no_bare_lake_reenters_the_recorded_migration(self):
        # Keep the existing migration verifier idempotent, including diagnostics.
        pattern = r'(?m)^(\s*(?:-\s+)?(?:run:\s*)?)lake(?=\s)'
        for name in FOCUSED + BRIDGES + tuple(item[0] for item in REGISTRATIONS):
            with self.subTest(workflow=name):
                self.assertNotRegex(workflow(name), pattern)

    def test_job_split_does_not_borrow_python_from_another_job(self):
        text = ('name: fixture\njobs:\n  python:\n    steps:\n'
                '      - uses: actions/setup-python@v5\n  lean:\n    steps:\n'
                '      - run: python3 scripts/run_formal_package.py --legacy -- build KUOS\n')
        bodies = job_bodies(text)
        self.assertEqual(len(bodies), 2)
        self.assertNotIn('setup-python', bodies[1])


if __name__ == '__main__':
    unittest.main()
