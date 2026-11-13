"""Fail-closed full-source diagnostic evidence tests (no repo writes or network)."""
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_kuuos_lean_mcp_fullsource_v1 as x


class FullSourceCausalEvidenceTests(unittest.TestCase):
    def fixture(self, temporary):
        root = pathlib.Path(temporary) / 'root'
        root.mkdir()
        (root / 'lean-toolchain').write_text(x.TOOLCHAIN + '\n')
        (root / 'lake-manifest.json').write_text(json.dumps({
            'packages': [{'name': 'mathlib', 'rev': x.MATHLIB_REV}] }))
        p1 = root / 'formal/KUOS/Child.lean'
        p1.parent.mkdir(parents=True)
        p2 = root / 'formal/KUOS/Parent.lean'
        p1.write_text('import KUOS.Parent\nnamespace KUOS\ntheorem child : Nat.succ 0 = 1 := by\n  exact parent\nend KUOS\n')
        p2.write_text('import Mathlib\nnamespace KUOS\ntheorem parent : Nat.succ 0 = 1 := by\n  rfl\nend KUOS\n')
        plan = {'schema_version': x.SCHEMA, 'source_head': 'a' * 40,
                'scope': 'all-changed', 'changed_lean_files': ['formal/KUOS/Child.lean'],
                'targets': [{'path': 'formal/KUOS/Child.lean', 'git_blob_sha': x.git_blob(p1.read_bytes())}],
                'api_probes': [{'name': 'Nat.add_comm', 'import_module': 'Mathlib'}]}
        return root, plan

    def test_whole_source_imports_signatures_and_reasoned_ci(self):
        with tempfile.TemporaryDirectory() as t:
            root, plan = self.fixture(t)
            log = '''2026-11-14T00:00:00Z error: formal/KUOS/Child.lean:4:2: Type mismatch: After simplification, term has type Foo but expected Bar
2026-11-14T00:01:00Z error: formal/KUOS/Parent.lean:4:3: Unknown identifier `parent`
'''
            out = pathlib.Path(t) / 'out'
            r = x.create_report(root, plan, log, out, max_deps=10, probe_api=False, api_timeout=5)
            self.assertEqual(r['status'], 'SOURCE_OBSERVATION_READY')
            self.assertEqual(r['full_source_snapshot_count'], 2)
            self.assertTrue(r['changed_lean_coverage_all_claimed'])
            self.assertTrue(r['source_file_git_blobs_verified'])
            self.assertFalse(r['head_verified_using_live_git_ref'])
            self.assertFalse(r['theorem_proof_certified'])
            self.assertFalse(r['ci_certified'])
            self.assertEqual([e['kind'] for e in r['ci_errors']], ['type_mismatch', 'unresolved_identifier'])
            self.assertEqual(r['ci_errors'][0]['enclosing_declaration_lexical'], 'KUOS.Child.child')
            self.assertTrue(r['ci_errors'][0]['file_read_in_full'])
            self.assertEqual(r['sources']['formal/KUOS/Child.lean']['direct_imports_local'], ['formal/KUOS/Parent.lean'])
            self.assertEqual(r['sources']['formal/KUOS/Parent.lean']['external_imports_not_verified'], ['Mathlib'])
            self.assertTrue(any(d['referenced_name_lexical']=='parent' for d in r['dependent_signatures_lexical']))
            self.assertEqual(r['api_probes'][0]['status'], 'NO_DATA_NOT_RUN')
            self.assertEqual((out / 'full_sources/formal/KUOS/Child.lean').read_bytes(),
                             (root / 'formal/KUOS/Child.lean').read_bytes())
            self.assertEqual(len((out / 'causal_casebook.jsonl').read_text().splitlines()), 2)
            self.assertIn('INFERRED_NOT_KERNEL_VERIFIED', (out / 'full_source_evidence.json').read_text())

    def test_reject_wrong_blob_no_partial_output(self):
        with tempfile.TemporaryDirectory() as t:
            root, plan = self.fixture(t)
            plan['targets'][0]['git_blob_sha'] = 'f' * 40
            out = pathlib.Path(t) / 'out'
            with self.assertRaisesRegex(x.EvidenceObstruction, 'blob mismatch'):
                x.create_report(root, plan, None, out, max_deps=10, probe_api=False, api_timeout=5)
            self.assertFalse(out.exists())

    def test_all_changed_claim_must_cover_each_changed_file(self):
        with tempfile.TemporaryDirectory() as t:
            root, plan = self.fixture(t)
            plan['changed_lean_files'].append('formal/KUOS/Parent.lean')
            with self.assertRaisesRegex(x.EvidenceObstruction, 'all-changed'):
                x.validate_plan(root, plan)
            plan['scope'] = 'scoped'
            self.assertFalse(x.validate_plan(root, plan)[1])

    def test_pinned_mathlib_and_lean_cannot_drift(self):
        with tempfile.TemporaryDirectory() as t:
            root, plan = self.fixture(t)
            (root / 'lean-toolchain').write_text('leanprover/lean4:stable\n')
            with self.assertRaisesRegex(x.EvidenceObstruction, 'Lean pin mismatch'):
                x.get_pins(root)
            (root / 'lean-toolchain').write_text(x.TOOLCHAIN)
            (root / 'lake-manifest.json').write_text(json.dumps({'packages': [{'name': 'mathlib', 'rev': 'f'*40}]}))
            with self.assertRaisesRegex(x.EvidenceObstruction, 'mathlib manifest pin mismatch'):
                x.get_pins(root)

    def test_classification_structural_reasons_not_automatic_proof(self):
        samples = {
            'Invalid field `σ_apply`': 'field_missing',
            'Unknown identifier `scaling_eq_of_le_antisymm`': 'unresolved_identifier',
            'AddConstAsyncResult.commitConst: constant has level params [u, u_1] but expected [u_1]': 'universe_mismatch',
            'Type mismatch: After simplification': 'type_mismatch',
            'Tactic `rewrite` failed: Did not find an occurrence of the pattern': 'rewrite_normal_form',
            'unsolved goals': 'remaining_goals',
            'something unfamiliar': 'other',
        }
        for message, expected in samples.items():
            with self.subTest(message=message):
                result = x.classify_diagnostic(message)
                self.assertEqual(result['kind'], expected)
                self.assertEqual(result['authority'], 'INFERRED_NOT_KERNEL_VERIFIED')
                self.assertTrue(result['next_experiments_not_proofs'])
        self.assertTrue(x.ci_diagnostics('"return_code": 124')[1])

    def test_feedback_is_bound_to_exact_source_and_is_not_authority(self):
        with tempfile.TemporaryDirectory() as t:
            root, plan = self.fixture(t)
            source_hash=x.sha256((root/'formal/KUOS/Child.lean').read_bytes())
            history=pathlib.Path(t)/'prior.jsonl'
            earlier={'classification':'type_mismatch',
                     'location':{'path':'formal/KUOS/Child.lean','line':4},
                     'source_blob_sha256':source_hash,
                     'outcome':'CI_FAILED', 'candidate':'exact h',
                     'receipt':'https://github.com/itakura-hidetoshi/KuuOS/actions/runs/1'}
            history.write_text(json.dumps(earlier)+'\n'+json.dumps({**earlier,'source_blob_sha256':'bad'})+'\n')
            log='error: formal/KUOS/Child.lean:4:2: Type mismatch'
            report=x.create_report(root, plan, log, pathlib.Path(t)/'out',
                                   max_deps=10,probe_api=False,api_timeout=2,previous_casebook=history)
            self.assertEqual(report['prior_cases_matched_same_source'],1)
            self.assertEqual(report['ci_errors'][0]['prior_attempts_same_source_unverified'][0]['outcome'], 'CI_FAILED')
            self.assertFalse(report['ci_certified'])

    def test_kernel_probe_result_cannot_be_replaced_by_documentation(self):
        from subprocess import CompletedProcess
        with tempfile.TemporaryDirectory() as t:
            root, _ = self.fixture(t)
            with patch.object(x.subprocess, 'run',return_value=CompletedProcess([],1,'','unknown constant')):
                result=x.api_probes(root,[{'name':'SSet.stdSimplex.σ_apply','import_module':'Mathlib'}],execute=True,timeout=2)
                self.assertEqual(result[0]['status'],'COMPILER_REJECTED')
                self.assertEqual(result[0]['exit_code'],1)
            with patch.object(x.subprocess, 'run',return_value=CompletedProcess([],0,'Nat.add_comm : ...','')):
                result=x.api_probes(root,[{'name':'Nat.add_comm','import_module':'Mathlib'}],execute=True,timeout=2)
                self.assertEqual(result[0]['status'],'COMPILER_PRESENT')
                self.assertEqual(result[0]['authority'],'PINNED_LEAN_COMMAND_OBSERVED')

    def test_api_probe_injection_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root, _ = self.fixture(t)
            with self.assertRaisesRegex(x.EvidenceObstruction, 'injectable'):
                x.api_probes(root, [{'name':'Nat.add_comm;#eval bad', 'import_module':'Mathlib'}],execute=False,timeout=2)

    def test_output_must_not_be_inside_checkout(self):
        with tempfile.TemporaryDirectory() as t:
            root, plan = self.fixture(t)
            with self.assertRaisesRegex(x.EvidenceObstruction, 'outside source tree'):
                x.create_report(root, plan, None, root / 'generated', max_deps=10,probe_api=False,api_timeout=5)

    def test_transitive_missing_module_is_obstruction_not_green(self):
        with tempfile.TemporaryDirectory() as t:
            root, plan = self.fixture(t)
            p=root/'formal/KUOS/Parent.lean'
            p.write_text('import KUOS.Missing\ntheorem parent : True := by trivial\n')
            r=x.create_report(root,plan,None,pathlib.Path(t)/'out',max_deps=10,probe_api=False,api_timeout=5)
            self.assertEqual(r['status'], 'SOURCE_OBSERVATION_WITH_OBSTRUCTIONS')
            self.assertFalse(r['full_import_closure_captured'])
            self.assertTrue(any('KUOS.Missing' in z for z in r['obstructions']))

if __name__ == '__main__':
    unittest.main(verbosity=2)
