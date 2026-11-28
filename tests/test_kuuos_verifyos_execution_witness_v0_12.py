"""Separate spawned executor and real Ed25519/child-process regression fixtures."""
import multiprocessing as mp
import shutil
import unittest
from unittest.mock import patch
import test_kuuos_verifyos_public_receipt_v0_11 as fixture
from runtime import kuuos_verifyos_execution_witness_v0_12 as g

b,p,prior = g.b,g.p,g.g


def worker(queue,args):
    queue.put(g.execute_and_issue(*args))


class WitnessTests(unittest.TestCase):
    def setUp(self):
        self.f=fixture.PublicReceiptTests('test_public_replay'); self.addCleanup(self.f.doCleanups); self.f.setUp()
        self.private=self.f.root/'witness.pem'; self.private.write_bytes(prior.openssl('genpkey','-algorithm','ED25519')); self.public=prior.public_key(self.private)
        self.refresh()

    def refresh(self):
        self.primary=self.f.signed()
        self.snapshot=self.f.root/'witness_snapshot'
        if self.snapshot.exists(): shutil.rmtree(self.snapshot)
        shutil.copytree(self.f.snapshot,self.snapshot)
        self.policy=dict(nonce='e'*64,primary_packet_sha256=b.sha(self.primary['packet']),inventory=b.inventory(self.snapshot,self.f.req['seq']))

    def issue_args(self):
        return (self.snapshot,self.policy,self.f.req,self.f.ctx,self.f.tip,self.f.public,self.public,self.private)

    def issue(self):
        out=g.execute_and_issue(*self.issue_args()); self.assertEqual(out['status'],'SIGNED_EXECUTION_WITNESS_ONLY',out); return out

    def args(self,witness=None,**kw):
        w=self.issue() if witness is None else witness
        args=dict(primary_packet=self.primary['packet'],primary_raw=self.f.raw,revision_log=self.primary['revision_log'],seed=self.f.seed,witness_packet=w['packet'],witness_raw=w['raw'],policy=self.policy,request=self.f.req,context=self.f.ctx,anchor=self.f.tip,primary_key=self.f.public,witness_key=self.public)
        args.update(kw); return args

    def alter_gate(self,code):
        f=self.f; name=b.GATES[0]; path=f.snapshot/'gates'/name
        path.write_text(code+path.read_text())
        f.req['expected_hashes']['gates/'+name]=b.sha(path.read_bytes()); f.ctx=f.context(f.req,1)
        base=b.canonical(prior.v.r.empty_log(f.family,f.ctx)); f.seed.update(base_request=f.req,base_context=f.ctx,base_log=base,base_anchor=b.sha(base))
        f.store=f.root/'modified-store.sqlite'; f.anchor=f.root/'modified-anchor.sqlite'
        genesis=prior.s.initialize(f.store,f.seed)['tip']; f.tip=prior.a.initialize(f.store,f.anchor,f.seed,genesis)['anchor_tip']
        f.evidence(); self.refresh()

    def test_pair_preserves_partial(self):
        out=g.verify_pair(**self.args()); self.assertEqual(out['status'],'SEPARATE_KEY_EXECUTION_REPORTS_AGREE_ONLY'); self.assertEqual(out['answer_status'],'AMBIGUOUS_PARTIAL'); self.assertEqual(out['compared_gate_count'],2)
        self.assertTrue(all(out[k] is False for k in g.BOUNDARY)); self.assertNotEqual(out['primary']['bundle_sha256'],out['witness']['bundle_sha256'])

    def test_spawned_witness_without_primary_secret(self):
        self.f.private.unlink(); self.f.key=None
        ctx=mp.get_context('spawn'); queue=ctx.Queue(); proc=ctx.Process(target=worker,args=(queue,self.issue_args()))
        try:
            proc.start(); witness=queue.get(timeout=30); proc.join(timeout=10); self.assertEqual(proc.exitcode,0)
            self.assertEqual(witness['status'],'SIGNED_EXECUTION_WITNESS_ONLY'); self.private.unlink()
            self.assertEqual(g.verify_pair(**self.args(witness))['status'],'SEPARATE_KEY_EXECUTION_REPORTS_AGREE_ONLY')
        finally:
            if proc.is_alive(): proc.terminate(); proc.join()
            queue.close(); queue.join_thread()

    def test_distinct_keys_required(self):
        self.assertEqual(g.verify_pair(**self.args(witness_key=self.f.public))['reason'],'DISTINCT_PINNED_KEYS_REQUIRED')

    def test_distinct_nonce_required(self):
        self.assertEqual(g.verify_pair(**self.args(policy=dict(self.policy,nonce=self.f.req['challenge'])))['reason'],'WITNESS_CHALLENGE_REQUIRED')

    def test_wrong_nonce(self):
        self.assertEqual(g.verify_pair(**self.args(policy=dict(self.policy,nonce='f'*64)))['status'],'HOLD')

    def test_primary_packet_binding(self):
        self.assertEqual(g.verify_pair(**self.args(primary_packet=b'{}\n'))['reason'],'PRIMARY_PACKET_BINDING')

    def test_wrong_context(self):
        self.assertEqual(g.verify_pair(**self.args(context=dict(self.f.ctx,turn_id='f'*64)))['status'],'HOLD')

    def test_wrong_anchor(self):
        self.assertEqual(g.verify_pair(**self.args(anchor=dict(self.f.tip,sha256='f'*64)))['status'],'HOLD')

    def test_wrong_witness_key(self):
        self.assertEqual(g.verify_pair(**self.args(witness_key=b'x'*32))['status'],'HOLD')

    def test_modified_witness_raw(self):
        self.assertEqual(g.verify_pair(**self.args(witness_raw=b'{}\n'))['status'],'HOLD')

    def test_reusing_primary_raw_rejected(self):
        self.assertEqual(g.verify_pair(**self.args(witness_raw=self.f.raw))['reason'],'WITNESS_REQUEST_MISMATCH')

    def test_snapshot_mismatch_stops_before_execution(self):
        (self.snapshot/'base'/b.BASE[0]).write_text('modified')
        with patch.object(b,'run') as run:
            self.assertEqual(g.execute_and_issue(*self.issue_args())['reason'],'WITNESS_INPUT_MISMATCH'); run.assert_not_called()

    def test_incomplete_inventory(self):
        args=list(self.issue_args()); args[1]=dict(self.policy,inventory={})
        self.assertEqual(g.execute_and_issue(*args)['reason'],'FULL_INVENTORY_REQUIRED')

    def test_real_output_disagreement(self):
        self.alter_gate("import os,sys,json\nif os.path.basename(os.getcwd())=='witness_snapshot':\n print(json.dumps("+repr(dict(status=b.EXPECTED[0],seq=0,tip_sha256=self.f.req['tip'],proof_authority=False,action_authority=False,rule_count=11,withdrawn_count=0,obstruction_count=2,research_certificate_count=2))+")); sys.exit(0)\n")
        out=g.verify_pair(**self.args()); self.assertEqual(out['reason'],'GATE_OUTPUT_DISAGREEMENT'); self.assertEqual(out['disagreeing_gates'],[b.GATES[0]]); self.assertIn('primary',out); self.assertIn('witness',out)

    def test_actual_witness_failure_retained(self):
        self.alter_gate("import os,sys\nif os.path.basename(os.getcwd())=='witness_snapshot': sys.exit(7)\n")
        w=self.issue(); self.assertEqual(p.strict(w['raw'])['receipt']['processes'][0]['exit_code'],7)
        out=g.verify_pair(**self.args(w)); self.assertEqual(out['reason'],'WITNESS_NOT_ADMITTED'); self.assertEqual(out['witness']['execution_status'],'HOLD_EXECUTION_NOT_ADMITTED')

    def test_signed_wrong_witness_projection(self):
        w=self.issue(); obj=p.strict(w['packet']); obj['payload']['proof_authority']=True
        obj['signature_hex']=prior.sign(obj['payload'],self.private,self.public).hex(); w['packet']=b.canonical(obj)
        self.assertEqual(g.verify_pair(**self.args(w))['reason'],'WITNESS_PROJECTION_MISMATCH')


if __name__=='__main__': unittest.main()
