"""Capture/adapter tests with explicitly synthetic compiler fixtures."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import tempfile
import unittest
from test_codeai_memoryos_lean_repair_v0_1 import context
try:
    from scripts import kuuos_codeai_memoryos_lean_v0_1 as c
except ImportError:
    c=None

class CaptureTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(c,'capture adapter must exist')
    def fixture(self,p,log='formal/KUOS/Test.lean:1:1: error: unsolved goals\n⊢ 1 = 2\n'):
        row={'variant':'fixture','candidate_blob':'b'*40,'status':'FAILURE',
             'exit_code':1,'olean_exists':False,'error_count':1,
             'log_sha256':hashlib.sha256(log.encode()).hexdigest()}
        data={'source_head':context()['source_head'],'source_tree':context()['source_tree'],
              'source_restored':True,'candidates':[row]}
        (p/'portfolio.json').write_text(json.dumps(data));(p/'fixture.log').write_text(log)
        return data
    def test_capture_full_log_not_error_excerpt(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.fixture(p)
            rows=c.capture(p,{'fixture':context()},{'run_id':1,'job_id':2})
            self.assertEqual(len(rows),1);self.assertIn('⊢ 1 = 2',c.memory.diagnostic(rows[0]))
    def test_capture_hash_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.fixture(p);(p/'fixture.log').write_text('forged')
            with self.assertRaises(ValueError):c.capture(p,{'fixture':context()},{'run_id':1})
    def test_capture_wrong_head_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.fixture(p);ctx=context();ctx['source_head']='a'*40
            with self.assertRaises(ValueError):c.capture(p,{'fixture':ctx},{'run_id':1})
    def test_capture_incomplete_log_preserves_no_data(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.fixture(p);(p/'fixture.log').unlink()
            rows=c.capture(p,{'fixture':context()},{'run_id':1})
            self.assertEqual(rows[0]['outcome'],'inconclusive')
            self.assertIs(rows[0]['diagnostic_complete'],False)
    def test_workflow_green_does_not_override_direct_red(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.fixture(p)
            rows=c.capture(p,{'fixture':context()},{'run_id':1,'workflow_conclusion':'success'})
            self.assertEqual(rows[0]['outcome'],'direct_failure')
    def test_no_source_restoration_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);x=self.fixture(p);x['source_restored']=False
            (p/'portfolio.json').write_text(json.dumps(x))
            with self.assertRaises(ValueError):c.capture(p,{'fixture':context()},{'run_id':1})
    def test_duplicate_candidate_identity_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);x=self.fixture(p);x['candidates']*=2
            (p/'portfolio.json').write_text(json.dumps(x))
            with self.assertRaises(ValueError):c.capture(p,{'fixture':context()},{'run_id':1})
    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);x=self.fixture(p);x['candidates'][0]['variant']='../secret'
            (p/'portfolio.json').write_text(json.dumps(x))
            with self.assertRaises(ValueError):c.capture(p,{'../secret':context()},{'run_id':1})

if __name__=='__main__':unittest.main()
