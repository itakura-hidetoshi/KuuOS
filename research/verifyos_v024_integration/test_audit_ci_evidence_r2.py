"""Synthetic evidence-shape regressions; not actual Lean or GitHub CI runs."""
import os
import subprocess
import tempfile
from pathlib import Path
import unittest
import audit_ci_evidence_r2 as a


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.path=Path(self.tmp.name)
        self.sources='a'*64
        self.identity={'repository':a.REPO,'pr':123,'run_id':'99','run_attempt':'1','head_sha':'1'*40,
                       'base_sha':a.BASE,'test_merge_sha':'2'*40,'source_tree':'3'*40,'test_merge_tree':'3'*40,'job':'sandbox'}
        self.receipt={'classification':'SYNTHETIC_ONLY','production_status':'HOLD','mode':'real','source_head':a.BASE,
            'manifest_sha256':a.MANIFEST_SHA,'base_files_checked':23,'candidate_files_checked':19,'groups':[],
            'status':'ACTUAL_SYNTHETIC_INTEGRATION_MATCHED','obstructions':[],'exit_code':0,
            'lean_version':'Lean (version 4.30.0-rc2, x86_64-unknown-linux-gnu, commit 3dc1a088b6d2d8eafe25a7cd7ec7b58d731bd7cc, Release)',
            'lean_binary_sha256':'b'*64}
        for name,n in a.GROUPS:
            raw=('Illustrative fixture, not a Lean run\n'+''.join(f'test_{i} (Fixture.test_{i}) ... ok\n' for i in range(n))+f'Ran {n} tests in 1.0s\n\nOK\n').encode()
            (self.path/(name+'.log')).write_bytes(raw)
            self.receipt['groups'].append(dict(group=name,exit_code=0,expected_count=n,observed_count=n,log_sha256=a.sha(raw),matched=True))
        self.save()
    def save(self): (self.path/'receipt.json').write_bytes(a.canonical(self.receipt))
    def audit(self): return a.audit_result(self.path)
    def seal(self): (self.path/'runner_evidence.json').write_bytes(a.canonical(a.envelope(self.path,self.identity,self.sources)))
    def independent(self,**change):return {**self.identity,'job':'independent',**change}
    def reject(self,reason):
        self.save()
        with self.assertRaisesRegex(ValueError,reason):self.audit()
    def test_complete_fixture(self):self.assertEqual(self.audit()['total_tests'],260)
    def test_status_only_rejected(self):self.receipt['groups']=[];self.reject('GROUP_COUNT')
    def test_group_exit_rejected(self):self.receipt['groups'][1]['exit_code']=2;self.reject('GROUP_FAILURE')
    def test_group_boolean_exit_rejected(self):self.receipt['groups'][1]['exit_code']=False;self.reject('GROUP_FAILURE')
    def test_group_matched_integer_rejected(self):self.receipt['groups'][1]['matched']=1;self.reject('GROUP_FAILURE')
    def test_missing_group_log(self):
        (self.path/'actual_v017.log').unlink()
        with self.assertRaisesRegex(ValueError,'MISSING_OR_UNSAFE'):self.audit()
    def test_log_tamper(self):
        (self.path/'actual_v017.log').write_text('tamper')
        with self.assertRaisesRegex(ValueError,'GROUP_LOG_SHA'):self.audit()
    def test_wrong_count(self):self.receipt['groups'][1]['observed_count']=9;self.reject('GROUP_TEST_COUNT')
    def test_log_count_mismatch_even_rehashed(self):
        raw=b'Ran 9 tests in 1.0s\nOK\n';(self.path/'actual_v017.log').write_bytes(raw);self.receipt['groups'][1]['log_sha256']=a.sha(raw);self.reject('GROUP_LOG_RESULT')
    def test_log_skip_even_rehashed(self):
        raw=b'Ran 10 tests in 1.0s\nOK (skipped=1)\n';(self.path/'actual_v017.log').write_bytes(raw);self.receipt['groups'][1]['log_sha256']=a.sha(raw);self.reject('GROUP_LOG_RESULT')
    def test_log_extra_output_even_rehashed(self):
        raw=b'Ran 10 tests in 1.0s\nOK\nFAILED\n';(self.path/'actual_v017.log').write_bytes(raw);self.receipt['groups'][1]['log_sha256']=a.sha(raw);self.reject('GROUP_LOG_RESULT')
    def test_log_summary_only_rejected(self):
        raw=b'Ran 10 tests in 1.0s\nOK\n';(self.path/'actual_v017.log').write_bytes(raw);self.receipt['groups'][1]['log_sha256']=a.sha(raw);self.reject('GROUP_LOG_TEST_ROWS')
    def test_receipt_failure(self):self.receipt['exit_code']=2;self.reject('RECEIPT_FAILURE')
    def test_production_promotion(self):self.receipt['production_status']='PASS';self.reject('RECEIPT_SCOPE')
    def test_duplicate_key(self):
        (self.path/'receipt.json').write_bytes(b'{"status":"HOLD","status":"PASS"}')
        with self.assertRaisesRegex(ValueError,'DUPLICATE_JSON_KEY'):self.audit()
    def test_exact_prior_fixture(self):self.seal();self.assertEqual(a.verify_prior(self.path,self.independent(),self.sources)['total_tests'],260)
    def test_other_run(self):
        self.seal()
        with self.assertRaisesRegex(ValueError,'SANDBOX_EVIDENCE_MISMATCH'):a.verify_prior(self.path,self.independent(run_id='100'),self.sources)
    def test_other_attempt(self):
        self.seal()
        with self.assertRaisesRegex(ValueError,'SANDBOX_EVIDENCE_MISMATCH'):a.verify_prior(self.path,self.independent(run_attempt='2'),self.sources)
    def test_other_tree(self):
        self.seal()
        with self.assertRaisesRegex(ValueError,'SANDBOX_EVIDENCE_MISMATCH'):a.verify_prior(self.path,self.independent(test_merge_tree='4'*40),self.sources)
    def test_other_source_fingerprint(self):
        self.seal()
        with self.assertRaisesRegex(ValueError,'SANDBOX_EVIDENCE_MISMATCH'):a.verify_prior(self.path,self.independent(),'d'*64)
    def test_receipt_rewritten_after_seal(self):
        self.seal();self.receipt['lean_binary_sha256']='e'*64;self.save()
        with self.assertRaisesRegex(ValueError,'SANDBOX_EVIDENCE_MISMATCH'):a.verify_prior(self.path,self.independent(),self.sources)
    def test_unsigned_forgery_boundary(self):
        # Anyone able to alter the trusted artifact and seal together can forge
        # this documentary check. The transport/runner trust assumption remains.
        self.seal();self.receipt['lean_binary_sha256']='e'*64;self.save();self.seal()
        self.assertEqual(a.verify_prior(self.path,self.independent(),self.sources)['lean_binary_sha256'],'e'*64)
    def test_ci_not_available(self):
        from unittest.mock import patch
        with patch.dict(a.os.environ,{},clear=True):
            with self.assertRaisesRegex(ValueError,'CI_CONTEXT_REQUIRED'):a.ci_identity(self.path,'sandbox')

class LocalCheckoutTests(unittest.TestCase):
    """Actual temporary Git object/merge tree inspection, no GitHub remote."""
    def setUp(self):
        from unittest.mock import patch
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.root=Path(tmp.name)
        self.repo=self.root/'synthetic';self.repo.mkdir(); self.event=self.root/'event.json'
        self.git('init','-q');self.git('config','user.email','fixture@example.invalid');self.git('config','user.name','Fixture')
        (self.repo/'fixture.txt').write_text('base');self.git('add','fixture.txt');self.git('commit','-qm','base');self.base=self.git('rev-parse','HEAD')
        (self.repo/'fixture.txt').write_text('head');self.git('add','fixture.txt');self.git('commit','-qm','head');self.head=self.git('rev-parse','HEAD')
        self.head_tree=self.git('rev-parse','HEAD^{tree}'); self.merge=self.git('commit-tree',self.head_tree,'-p',self.base,'-p',self.head,'-m','synthetic merge');self.git('checkout','--detach','-q',self.merge)
        self.event.write_bytes(a.canonical({'pull_request':{'number':1,'head':{'sha':self.head,'repo':{'full_name':a.REPO}},'base':{'sha':self.base,'repo':{'full_name':a.REPO}}}}))
        self.env={'GITHUB_ACTIONS':'true','GITHUB_EVENT_NAME':'pull_request','GITHUB_REPOSITORY':a.REPO,'GITHUB_JOB':'sandbox','GITHUB_SHA':self.merge,'GITHUB_EVENT_PATH':str(self.event),'GITHUB_RUN_ID':'1','GITHUB_RUN_ATTEMPT':'1'}
        self.addCleanup(patch.stopall);patch.object(a,'BASE',self.base).start();patch.dict(os.environ,self.env).start()
    def git(self,*args):
        return subprocess.check_output(['git','-C',str(self.repo),*args],stderr=subprocess.PIPE).decode().strip()
    def test_identical_tree(self):
        got=a.ci_identity(self.repo,'sandbox');self.assertEqual(got['source_tree'],self.head_tree);self.assertEqual(got['test_merge_tree'],self.head_tree)
    def test_modified_tracked_file(self):
        (self.repo/'fixture.txt').write_text('drift')
        with self.assertRaisesRegex(ValueError,'CI_TRACKED_SOURCE_DRIFT'):a.ci_identity(self.repo,'sandbox')
    def test_different_merge_tree(self):
        other=self.git('rev-parse',self.base+'^{tree}');merge=self.git('commit-tree',other,'-p',self.base,'-p',self.head,'-m','synthetic different tree');self.git('checkout','--detach','-q',merge);os.environ['GITHUB_SHA']=merge
        with self.assertRaisesRegex(ValueError,'CI_TREE_MISMATCH'):a.ci_identity(self.repo,'sandbox')
    def test_wrong_checkout(self):
        os.environ['GITHUB_SHA']='4'*40
        with self.assertRaisesRegex(ValueError,'CI_CHECKOUT_SHA'):a.ci_identity(self.repo,'sandbox')

if __name__=='__main__':unittest.main()
