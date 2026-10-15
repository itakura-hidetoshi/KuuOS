"""The migration changes formal scope, not assertions or test commands."""
import unittest
from scripts.migrate_kuu_consumers import transform_sources

class KuuConsumerMigrationTests(unittest.TestCase):
    def test_legacy_assertions_are_retained_at_explicit_path(self):
        path='scripts/check_example.py'
        old='aggregate_root = ROOT / "formal/KuuOSFormal.lean"\nrequire_tokens(aggregate_root, ("KUOS.Example",))\n'
        got=transform_sources({path:old})[path]
        self.assertIn('legacy/v5.291/formal/KuuOSFormal.lean',got)
        self.assertIn('require_tokens(aggregate_root, ("KUOS.Example",))',got)
    def test_live_ci_selector_is_not_redirected(self):
        p='scripts/select_impacted_checks.py'
        self.assertNotIn(p, transform_sources({p:'LAKEFILE = ROOT / "lakefile.toml"\n"formal/KuuOSFormal.lean"\n'}))
    def test_existing_workflow_calls_explicit_legacy_and_keeps_python(self):
        p='.github/workflows/old.yml'
        old='name: old\non:\n  pull_request:\njobs:\n  test:\n    steps:\n      - run: python3 tests/test_old.py\n      - run: lake -KleanArgs=-DsorryAsError=true build KUOS.Example\n      - run: git diff --exit-code -- lake-manifest.json\n'
        got=transform_sources({p:old})[p]
        self.assertIn('pull_request:',got)
        self.assertIn('run: python3 tests/test_old.py',got)
        self.assertIn('python3 scripts/run_formal_package.py --legacy -- -KleanArgs=-DsorryAsError=true build KUOS.Example',got)
        self.assertIn('lake-manifest.json legacy/v5.291/lake-manifest.json',got)
    def test_current_foundation_workflow_is_not_redirected(self):
        p='.github/workflows/kuu-independent-foundation.yml'
        self.assertNotIn(p,transform_sources({p:'run: lake build KuuOSFormal\n'}))
    def test_governance_workflow_is_not_redirected(self):
        p='.github/workflows/pr-governance-gate.yml'
        self.assertNotIn(p,transform_sources({p:'run: lake build KuuOSFormal\n'}))
    def test_contract_scope_is_explicit_not_a_current_fallback(self):
        p='manifests/example.json'
        old='{"repository_autorepair_contract": true, "aggregate_formal_root": "formal/KuuOSFormal.lean"}\n'
        import json
        got=json.loads(transform_sources({p:old})[p])
        self.assertEqual(got['formal_package'],'legacy-v5.291')
        self.assertEqual(got['aggregate_formal_root'],'legacy/v5.291/formal/KuuOSFormal.lean')
    def test_legacy_sources_and_old_fixture_semantics_are_unchanged(self):
        inputs={'legacy/v5.291/scripts/check_example.py':'ROOT / "formal/KuuOSFormal.lean"',
                'tests/test_old.py':'ROOT / "formal/KuuOSFormal.lean"'}
        self.assertEqual(transform_sources(inputs),{})
    def test_transformation_is_idempotent(self):
        p='scripts/check_example.py'; inputs={p:'ROOT / "formal/KuuOSFormal.lean"\n'}
        once=transform_sources(inputs)
        self.assertEqual(transform_sources(once),{})
    def test_new_archive_files_are_never_generated(self):
        p='.github/workflows/old.yml'; inputs={p:'run: lake build KUOS.Example\n'}
        self.assertTrue(all(not x.endswith(('.zip','.tar','.gz')) for x in transform_sources(inputs)))
    def test_named_lean_action_retains_valid_property_indentation(self):
        p='.github/workflows/old.yml'
        old='name: old\njobs:\n  a:\n    steps:\n      - name: Lean\n        uses: leanprover/lean-action@v1\n        with:\n          build: false\n      - run: lake build KUOS.Example\n'
        got=transform_sources({p:old})[p]
        self.assertEqual(got.count('with:'),1)
        self.assertIn('        with:\n          lake-package-directory: legacy/v5.291\n',got)
    def test_lean_action_package_is_explicit(self):
        p='.github/workflows/old.yml'
        old='name: old\njobs:\n  a:\n    steps:\n      - uses: leanprover/lean-action@v1\n        with:\n          build: false\n      - run: lake build KUOS.Example\n'
        got=transform_sources({p:old})[p]
        self.assertIn('lake-package-directory: legacy/v5.291',got)
        self.assertIn('build: false',got)
if __name__=='__main__': unittest.main()
