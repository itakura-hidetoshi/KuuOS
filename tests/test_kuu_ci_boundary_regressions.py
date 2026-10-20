"""PR2338 regressions for fixture scope and the historical Lean-LSP workspace.

External MCP execution is mocked only in CLI wiring tests. These do not claim
that a real Lean server or compiler ran; the live workflow remains mandatory.
"""
from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import re
import shlex
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import check_workflow_consolidation_integrity as integrity
from scripts import check_kuuos_lean_lsp_mcp_compatibility_v7_17 as lsp

WORKFLOWS = Path('.github') / 'workflows'
LSP_WORKFLOW = ROOT / WORKFLOWS / 'lean-lsp-mcp-compatibility-v7-17.yml'
MIGRATION_TEST = 'tests/test_kuu_consumer_migration.py'
LEGACY = Path('legacy') / 'v5.291'
RECEIPT = 'lean_lsp_mcp_compatibility_receipt_v7_17.json'
PROBE_SCRIPT = 'scripts/check_kuuos_lean_lsp_mcp_compatibility_v7_17.py'


def step_text(name: str) -> str:
    match = re.search(
        r'^      - name: ' + re.escape(name) + r'\n(.*?)(?=^      - |\Z)',
        LSP_WORKFLOW.read_text(encoding='utf-8'), re.MULTILINE | re.DOTALL)
    if match is None:
        raise AssertionError('required workflow step is missing: ' + name)
    return match[1]


def run_text(name: str) -> str:
    body = step_text(name).split('        run: |\n', 1)[1]
    return '\n'.join(line[10:] for line in body.splitlines())


def probe_arguments() -> list[str]:
    tokens = shlex.split(run_text('Run live MCP and LSP compatibility probe').replace('\\\n', ''))
    start = tokens.index(PROBE_SCRIPT) + 1
    end = min((tokens.index(token) for token in ('2>&1', '|') if token in tokens),
              default=len(tokens))
    return [os.path.expandvars(value) for value in tokens[start:end]]


class FixtureReferenceScopeTests(unittest.TestCase):
    def check_references(self, source: str, names: tuple[str, ...],
                         existing: tuple[str, ...] = ()) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / source
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('\n'.join(str(WORKFLOWS / name) for name in names),
                            encoding='utf-8')
            for name in existing:
                target = root / WORKFLOWS / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('name: fixture\n', encoding='utf-8')
            errors: list[str] = []
            with patch.object(integrity, 'ROOT', root), patch.dict(
                    os.environ, {'KUUOS_FULL_WORKFLOW_SCAN': '1'}):
                integrity.check_workflow_references(errors)
            return errors

    def test_migration_virtual_members_are_not_repository_dependencies(self):
        self.assertEqual(self.check_references(MIGRATION_TEST,
                         ('old.yml', 'new-current.yml')), [])

    def test_virtual_path_exception_is_source_scoped(self):
        for name in ('old.yml', 'new-current.yml'):
            with self.subTest(name=name):
                errors = self.check_references('tests/test_other.py', (name,))
                self.assertEqual(len(errors), 1)
                self.assertIn(str(WORKFLOWS / name), errors[0])

    def test_unlisted_missing_member_still_fails_in_migration_test(self):
        self.assertEqual(len(self.check_references(MIGRATION_TEST,
                         ('unlisted.yml',))), 1)

    def test_virtual_names_in_runtime_still_fail(self):
        self.assertEqual(len(self.check_references('runtime/example.py',
                         ('old.yml', 'new-current.yml'))), 2)

    def test_existing_real_workflow_remains_valid(self):
        self.assertEqual(self.check_references('scripts/example.py',
                         ('real.yml',), ('real.yml',)), [])

    def test_exception_lists_exactly_the_two_virtual_members(self):
        expected = frozenset(str(WORKFLOWS / name)
                             for name in ('old.yml', 'new-current.yml'))
        self.assertEqual(integrity.VIRTUAL_FIXTURE_WORKFLOW_REFERENCES.get(
                         MIGRATION_TEST), expected)


class HistoricalLSPWorkspaceTests(unittest.TestCase):
    def test_probe_root_matches_the_prepared_legacy_package(self):
        arguments = probe_arguments()
        self.assertEqual(arguments[arguments.index('--repository-root') + 1],
                         LEGACY.as_posix())
        self.assertIn('lake-package-directory: ' + LEGACY.as_posix(),
                      step_text('Set up pinned Lean and Lake'))
        self.assertIn('--live-probe', arguments)

    def test_cache_uses_legacy_path_and_pins_not_current_cache(self):
        text = step_text('Restore Lake workspace cache')
        self.assertIn('path: ' + (LEGACY / '.lake').as_posix() + '\n', text)
        self.assertIn('key: kuuos-legacy-v5291-lean-lsp-mcp-', text)
        self.assertIn("hashFiles('legacy/v5.291/lean-toolchain')", text)
        self.assertIn("hashFiles('legacy/v5.291/lake-manifest.json')", text)
        self.assertNotIn('kuuos-lake-', text)

    def test_pin_verification_reads_the_same_legacy_package(self):
        text = run_text('Verify exact KuuOS pins')
        self.assertIn('cat legacy/v5.291/lean-toolchain', text)
        self.assertIn('open("legacy/v5.291/lake-manifest.json")', text)
        self.assertIn(lsp.EXPECTED_MATHLIB_SHA, text)
        self.assertIn(lsp.EXPECTED_LEAN_TOOLCHAIN, text)

    def test_receipt_remains_at_the_upload_location(self):
        with patch.dict(os.environ, {'GITHUB_WORKSPACE': '/tmp/kuu-workspace'}):
            arguments = probe_arguments()
        destination = arguments[arguments.index('--receipt') + 1]
        self.assertEqual(destination, '/tmp/kuu-workspace/' + RECEIPT)
        self.assertIn(RECEIPT, step_text('Upload compatibility receipt'))

    def run_cli(self, *, fail: bool) -> tuple[int | None, Path, dict]:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            package = workspace / LEGACY
            package.mkdir(parents=True)
            (package / 'lean-toolchain').write_text(lsp.EXPECTED_LEAN_TOOLCHAIN)
            (package / 'lake-manifest.json').write_text(json.dumps({'packages': [
                {'name': 'mathlib', 'rev': lsp.EXPECTED_MATHLIB_SHA}]}))
            probe = package / lsp.PROBE_FILE
            probe.parent.mkdir(parents=True)
            probe.write_text('import Mathlib\n')
            result = {'required_tools_present': True, 'disabled_tools_absent': True,
                      'diagnostics_call_succeeded': True}
            with patch.dict(os.environ, {'GITHUB_WORKSPACE': str(workspace)}):
                arguments = probe_arguments()
            previous = Path.cwd()
            try:
                os.chdir(workspace)
                with patch.object(sys, 'argv', [PROBE_SCRIPT, *arguments]), \
                     patch.object(lsp, 'server_version', return_value='lean-lsp-mcp 0.30.0'), \
                     patch.object(lsp, 'live_probe', return_value=result,
                                  side_effect=RuntimeError('synthetic probe failure') if fail else None) as live, \
                     redirect_stdout(io.StringIO()):
                    if fail:
                        with self.assertRaisesRegex(RuntimeError, 'synthetic probe failure'):
                            lsp.main()
                        self.assertFalse((workspace / RECEIPT).exists())
                        return None, package, {}
                    code = lsp.main()
                    live.assert_called_once()
                    self.assertEqual(live.call_args.args[0], package)
                    self.assertIn('--transport', live.call_args.kwargs['command'])
                    receipt = json.loads((workspace / RECEIPT).read_text())
                    self.assertFalse((package / RECEIPT).exists())
                    return code, package, receipt
            finally:
                os.chdir(previous)

    def test_real_cli_wiring_needs_only_legacy_pins_and_writes_expected_receipt(self):
        code, _, receipt = self.run_cli(fail=False)
        self.assertEqual(code, 0)
        self.assertEqual(receipt['status'], 'KUUOS_LEAN_LSP_MCP_COMPATIBILITY_VERIFIED')
        self.assertFalse(receipt['boundary']['compatibility_receipt_is_theorem_authority'])

    def test_failed_live_probe_cannot_write_a_success_receipt(self):
        self.run_cli(fail=True)

    def test_live_failure_has_a_log_and_is_not_masked(self):
        text = run_text('Run live MCP and LSP compatibility probe')
        self.assertIn('set -euo pipefail', text)
        self.assertIn('2>&1 | tee lean_lsp_mcp_compatibility_probe_v7_17.log', text)
        self.assertNotIn('|| true', text)
        self.assertIn('lean_lsp_mcp_compatibility_probe_v7_17.log',
                      step_text('Upload compatibility receipt'))



class IndependentKuuCICacheConsolidationTests(unittest.TestCase):
    """Ensure CI de-duplication does not silently remove independent proof checks."""

    def test_pr_governance_still_owns_strict_lean_and_foundation_regressions(self):
        from scripts import select_impacted_checks as selector

        registry = selector.load_registry(selector.DEFAULT_REGISTRY)
        for changed in ('formal/Kuu/F112/Physical.lean',
                        'formal/KuuOSStrict.lean'):
            with self.subTest(changed=changed):
                plan = selector.select(registry, [changed], None)
                selected = {item['id'] for item in plan['selected_checks']}
                self.assertTrue(plan['lean_required'])
                self.assertIn('lean-formal', selected)
                self.assertIn('kuu-independent-foundation', selected)
                self.assertIn('KuuOSFormal', plan['lean_targets'])
                self.assertFalse(plan['full_audit_required'])
        aggregate = (ROOT / 'formal/KuuOSFormal.lean').read_text(encoding='utf-8')
        self.assertIn('import KuuOSStrict', aggregate)

    def test_manual_foundation_audit_keeps_its_full_lean_proof(self):
        dedicated = (ROOT / WORKFLOWS / 'kuu-independent-foundation.yml').read_text(
            encoding='utf-8')
        triggers = dedicated.split('on:\n', 1)[1].split('\npermissions:', 1)[0]
        self.assertIn('workflow_dispatch:', triggers)
        self.assertNotIn('pull_request:', triggers)
        self.assertIn('scripts/run_kuu_foundation_check.py', dedicated)
        self.assertIn('leanprover/lean-action@v1', dedicated)
        self.assertIn('Focused incremental Kuu module compilation', dedicated)
        self.assertIn('KuuOSStrict', dedicated)
        self.assertIn('git diff --exit-code', dedicated)

    def test_f112_parent_cache_is_validated_before_sibling_reuse(self):
        prewarm = (ROOT / WORKFLOWS / 'lean-formal-validation.yml').read_text(
            encoding='utf-8')
        governance = (ROOT / WORKFLOWS / 'pr-governance-gate.yml').read_text(
            encoding='utf-8')
        self.assertIn('formal/v5-293-f112-independent-total-change', prewarm)
        self.assertIn('refs/heads/formal/v5-293-f112-independent-total-change', prewarm)
        self.assertIn('Warm F112 theorem bridge on the authoritative working branch', prewarm)
        self.assertIn('HistoricalF36F40BridgeP([0-9]+)', prewarm)
        self.assertIn('lean-f112-cache-warm.log', prewarm)
        self.assertIn('runs-on: ubuntu-24.04', prewarm)
        self.assertIn('runs-on: ubuntu-24.04', governance)
        key = 'kuuos-lake-${{ runner.os }}-${{ runner.arch }}-'
        self.assertIn(key, prewarm)
        self.assertIn(key, governance)
        self.assertIn('Restore trusted main Lake workspace cache', governance)
        self.assertIn('build "${latest}"', prewarm)
        self.assertIn('-DwarningAsError=true', prewarm)
        self.assertIn('-DsorryAsError=true', prewarm)


if __name__ == '__main__':
    unittest.main()
