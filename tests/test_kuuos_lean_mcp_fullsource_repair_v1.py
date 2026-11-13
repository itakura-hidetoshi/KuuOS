"""Read-only fulltext and exact-signature guards before calling Lean MCP repair."""
import json
import pathlib
import tempfile
import unittest

from scripts import check_kuuos_lean_mcp_fullsource_v1 as scanner
from scripts import check_kuuos_lean_mcp_fullsource_repair_v1 as repair


class FullSourceRepairGateTests(unittest.TestCase):
    def fixture(self, t):
        root = pathlib.Path(t) / 'work'
        root.mkdir()
        (root / 'lean-toolchain').write_text(scanner.TOOLCHAIN)
        (root / 'lake-manifest.json').write_text(json.dumps({'packages': [
            {'name': 'mathlib', 'rev': scanner.MATHLIB_REV}]}))
        path='formal/KUOS/Proof.lean'
        q=root/path
        q.parent.mkdir(parents=True)
        q.write_text('import Mathlib\nnamespace Demo\ntheorem demo : True := by\n  skip\nend Demo\n')
        plan={'schema_version':scanner.SCHEMA,'source_head':'a'*40,
              'scope':'all-changed','changed_lean_files':[path],
              'targets':[{'path':path,'git_blob_sha':scanner.git_blob(q.read_bytes())}],
              'api_probes':[]}
        return root,path,plan

    def test_readonly_preflight_never_calls_repair(self):
        with tempfile.TemporaryDirectory() as t:
            root,path,plan=self.fixture(t)
            def forbidden(**_):
                raise AssertionError('repair invoked without permission')
            r=repair.gate_repair(root=root,plan=plan,output_dir=pathlib.Path(t)/'outside',
                                 target=path,acknowledged_isolated=False,runner=forbidden)
            self.assertEqual(r['repair_status'],'READ_ONLY_FULL_SOURCE_PREFLIGHT_COMPLETE')
            self.assertIsNone(r['source_restored'])
            self.assertFalse(r['github_write_performed'])

    def test_bounded_repair_proof_only_candidate_can_pass_locally_not_ci(self):
        with tempfile.TemporaryDirectory() as t:
            root,path,plan=self.fixture(t)
            before=(root/path).read_bytes()
            def fake_green(**kw):
                out=kw['output_dir']
                out.mkdir(parents=True)
                (out/'candidate.lean').write_bytes(before.replace(b'  skip\n',b'  trivial\n'))
                return {'status':'LOCAL_LEAN_GREEN_CANDIDATE_ONLY','source_restored':True,
                        'independent_ci_success':False,'git_write_performed':False}
            r=repair.gate_repair(root=root,plan=plan,output_dir=pathlib.Path(t)/'outside',
                                 target=path,acknowledged_isolated=True,runner=fake_green,
                                 provider=lambda *_: {})
            self.assertEqual(r['repair_status'],'LOCAL_FULLSOURCE_AND_LEAN_GREEN_CANDIDATE_ONLY')
            self.assertTrue(r['source_restored'])
            self.assertTrue(r['source_signature_unchanged'])
            self.assertTrue(r['imports_unchanged'])
            self.assertEqual((root/path).read_bytes(),before)
            self.assertFalse(r['ci_certified'])

    def test_changed_statement_is_rejected_despite_reported_local_green(self):
        with tempfile.TemporaryDirectory() as t:
            root,path,plan=self.fixture(t)
            before=(root/path).read_bytes()
            def fake_bad(**kw):
                out=kw['output_dir']
                out.mkdir(parents=True)
                (out/'candidate.lean').write_bytes(before.replace(b'theorem demo : True',b'theorem demo : False'))
                return {'status':'LOCAL_LEAN_GREEN_CANDIDATE_ONLY','source_restored':True}
            r=repair.gate_repair(root=root,plan=plan,output_dir=pathlib.Path(t)/'outside',
                                 target=path,acknowledged_isolated=True,runner=fake_bad,
                                 provider=lambda *_:{})
            self.assertEqual(r['repair_status'],'PROOF_INTERFACE_OBSTRUCTION')
            self.assertFalse(r['source_signature_unchanged'])
            self.assertFalse(r['ci_certified'])

    def test_import_change_is_rejected_despite_reported_local_green(self):
        with tempfile.TemporaryDirectory() as t:
            root,path,plan=self.fixture(t)
            before=(root/path).read_bytes()
            def fake_bad(**kw):
                out=kw['output_dir']
                out.mkdir(parents=True)
                (out/'candidate.lean').write_bytes(before.replace(b'import Mathlib',b'import Lean'))
                return {'status':'LOCAL_LEAN_GREEN_CANDIDATE_ONLY','source_restored':True}
            r=repair.gate_repair(root=root,plan=plan,output_dir=pathlib.Path(t)/'outside',
                                 target=path,acknowledged_isolated=True,runner=fake_bad,
                                 provider=lambda *_:{})
            self.assertEqual(r['repair_status'],'PROOF_INTERFACE_OBSTRUCTION')
            self.assertFalse(r['imports_unchanged'])

    def test_wrong_source_blob_must_block_runner(self):
        with tempfile.TemporaryDirectory() as t:
            root,path,plan=self.fixture(t)
            plan['targets'][0]['git_blob_sha']='b'*40
            def no_call(**kw):
                raise AssertionError('should never call broken source')
            with self.assertRaisesRegex(scanner.EvidenceObstruction,'blob mismatch'):
                repair.gate_repair(root=root,plan=plan,output_dir=pathlib.Path(t)/'outside',
                                  target=path,acknowledged_isolated=True,runner=no_call,
                                  provider=lambda *_:{})

    def test_target_outside_verified_set_cannot_run(self):
        with tempfile.TemporaryDirectory() as t:
            root,path,plan=self.fixture(t)
            r=repair.gate_repair(root=root,plan=plan,output_dir=pathlib.Path(t)/'outside',
                                 target='formal/KUOS/Other.lean',acknowledged_isolated=True,
                                 runner=lambda **_: None, provider=lambda *_:{})
            self.assertEqual(r['repair_status'],'TARGET_OUTSIDE_EXACT_CHANGED_SOURCE_SET')

if __name__ == '__main__':
    unittest.main(verbosity=2)
