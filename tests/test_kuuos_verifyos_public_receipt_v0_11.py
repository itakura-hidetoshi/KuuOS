"""Real Ed25519 operations, external verifier process, synthetic gate evidence."""
from pathlib import Path
import multiprocessing as mp
import shutil
import tempfile
import unittest
from runtime import kuuos_verifyos_public_receipt_v0_11 as g

b,p,a,s,v,f,r = g.b,g.p,g.a,g.s,g.v,g.f,g.v.r


def public_worker(queue, args):
    out = g.verify(*args)
    queue.put((out['status'],out.get('payload',{}).get('answer_status')))


class PublicReceiptTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.root=Path(tmp.name)
        self.snapshot=self.root/'snapshot'; self.snapshot.mkdir()
        for d in ('base','gates','ledger'): (self.snapshot/d).mkdir()
        for name in b.BASE: (self.snapshot/'base'/name).write_text('fixture')
        ledger=self.snapshot/'ledger/000000000000.json'; ledger.write_text('synthetic'); tip=b.sha(ledger.read_bytes())
        for name,status in zip(b.GATES,b.EXPECTED):
            data=dict(status=status,seq=0,tip_sha256=tip,proof_authority=False,action_authority=False,rule_count=10,withdrawn_count=0,obstruction_count=2,research_certificate_count=2,reviews=dict(candidate=1,held=12,no_use=0))
            (self.snapshot/'gates'/name).write_text('import json\nprint(json.dumps('+repr(data)+'))\n')
        inv=b.inventory(self.snapshot,0)
        self.req=dict(challenge='a'*64,seq=0,tip=tip,expected_hashes={k:z for k,z in inv.items() if k.startswith('gates/') or k=='base/'+b.BASE[2]})
        self.question='取得済み台帳について、tip、認証状況を教えて。'.encode()
        analysis=f.analyze(self.question); self.family=analysis['family']; self.trace=analysis['trace']; self.spans=[i for i,x in enumerate(self.trace) if x['kind']=='ambiguous_clause']
        self.ctx=self.context(self.req,1); base=b.canonical(r.empty_log(self.family,self.ctx))
        self.seed=dict(question=self.question,candidate=b.canonical(self.family),base_request=self.req,base_context=self.ctx,base_log=base,base_anchor=b.sha(base))
        self.store=self.root/'store.sqlite'; self.anchor=self.root/'anchor.sqlite'; genesis=s.initialize(self.store,self.seed)['tip']
        self.tip=a.initialize(self.store,self.anchor,self.seed,genesis)['anchor_tip']
        self.key=bytes(range(32)); self.private=self.root/'private.pem'; self.private.write_bytes(g.openssl('genpkey','-algorithm','ED25519')); self.public=g.public_key(self.private)
        self.evidence()

    def context(self,req,turn):
        return dict(turn_id=f'{turn:064x}',question_sha256=b.sha(self.question),challenge=req['challenge'],request_sha256=v.digest(req),audience=p.AUDIENCE)

    def evidence(self):
        self.raw,self.admission=p.execute_and_admit(self.snapshot,self.req,self.ctx,self.key); self.assertIsNotNone(self.admission)
        self.prior=p.publish(self.raw,self.admission,self.req,self.ctx,self.key)

    def advance(self,span=0,choice=0,nonce=10):
        snap=a.read(self.store,self.anchor,self.seed,self.tip); log=p.strict(snap['inputs']['revision_log']); i=self.spans[span]
        req=dict(self.req,challenge=f'{nonce:064x}'); ctx=self.context(req,nonce)
        event=dict(schema=v.EVENT,sequence=len(log['events'])+1,parent_sha256=v.digest(log['events'][-1]) if log['events'] else log['genesis'],event_id=f'{nonce+100:064x}',source='host_captured_explicit_user_revision',operation='confirm',span_index=i,span_sha256=self.trace[i]['span_sha256'],choice_index=choice,target_event_sha256=None,next_request=req,next_context=ctx)
        raw=b.canonical(event); args=(raw,b.sha(raw),req,ctx)
        out=a.prepare(self.store,self.anchor,self.seed,self.tip,*args); self.assertEqual(out['status'],'INTENT_PREPARED_NOT_COMMITTED')
        out=a.resume(self.store,self.anchor,self.seed,out['anchor_tip'],*args); self.assertEqual(out['status'],'ANCHOR_SEALED'); self.tip=out['anchor_tip']; self.req,self.ctx=req,ctx

    def issue(self,**kw):
        args=dict(store=self.store,anchor=self.anchor,seed=self.seed,expected_anchor=self.tip,raw=self.raw,admission=self.admission,host_key=self.key,prior_packet=self.prior,private_key=self.private,expected_key=self.public,current_request=self.req,current_context=self.ctx); args.update(kw)
        return g.issue(**args)

    def signed(self):
        out=self.issue(); self.assertEqual(out['status'],'SIGNED_SNAPSHOT_ONLY',out); return out

    def args(self,**kw):
        out=self.signed(); args=dict(packet=out['packet'],raw=self.raw,revision_log=out['revision_log'],seed=self.seed,current_request=self.req,current_context=self.ctx,expected_anchor=self.tip,expected_key=self.public); args.update(kw); return args

    def test_public_replay(self):
        args=self.args(); out=g.verify(**args); self.assertEqual(out['status'],'PUBLIC_SIGNATURE_AND_REPLAY_MATCHED_ONLY')
        self.assertEqual(out['payload']['answer_status'],'AMBIGUOUS_PARTIAL'); self.assertTrue(all(out[k] is False for k in g.BOUNDARY))
        self.assertEqual(len(out['payload']['branches']),4)

    def test_separate_process_without_secrets(self):
        args=self.args(); self.private.unlink(); self.key=None
        ctx=mp.get_context('spawn'); queue=ctx.Queue(); proc=ctx.Process(target=public_worker,args=(queue,tuple(args.values())))
        try:
            proc.start(); self.assertEqual(queue.get(timeout=25),('PUBLIC_SIGNATURE_AND_REPLAY_MATCHED_ONLY','AMBIGUOUS_PARTIAL'))
            proc.join(timeout=10); self.assertEqual(proc.exitcode,0)
        finally:
            if proc.is_alive(): proc.terminate(); proc.join()
            queue.close(); queue.join_thread()

    def test_wrong_public_key(self): self.assertEqual(g.verify(**self.args(expected_key=b'x'*32))['status'],'HOLD')

    def test_tampered_signature(self):
        args=self.args(); obj=p.strict(args['packet']); obj['signature_hex']='00'*64; args['packet']=b.canonical(obj)
        self.assertEqual(g.verify(**args)['status'],'HOLD')

    def test_tampered_claim(self):
        args=self.args(); obj=p.strict(args['packet']); obj['payload']['claims'].pop(); args['packet']=b.canonical(obj)
        self.assertEqual(g.verify(**args)['status'],'HOLD')

    def test_valid_signature_wrong_claim_still_rejected(self):
        args=self.args(); obj=p.strict(args['packet']); obj['payload']['claims'].pop()
        obj['signature_hex']=g.sign(obj['payload'],self.private,self.public).hex(); args['packet']=b.canonical(obj)
        self.assertEqual(g.verify(**args)['reason'],'SIGNED_PROJECTION_MISMATCH')

    def test_valid_signature_authority_escalation_rejected(self):
        args=self.args(); obj=p.strict(args['packet']); obj['payload']['proof_authority']=True
        obj['signature_hex']=g.sign(obj['payload'],self.private,self.public).hex(); args['packet']=b.canonical(obj)
        self.assertEqual(g.verify(**args)['reason'],'SIGNED_PROJECTION_MISMATCH')

    def test_wrong_bundle(self): self.assertEqual(g.verify(**self.args(raw=b'{}\n'))['status'],'HOLD')

    def test_wrong_context(self): self.assertEqual(g.verify(**self.args(current_context=dict(self.ctx,turn_id='f'*64)))['status'],'HOLD')

    def test_wrong_anchor(self): self.assertEqual(g.verify(**self.args(expected_anchor=dict(self.tip,sha256='f'*64)))['reason'],'SEALED_ANCHOR_MISMATCH')

    def test_missing_admission_no_sign(self): self.assertEqual(self.issue(admission=None)['reason'],'HOST_ADMISSION_INVALID')

    def test_wrong_signer_key(self): self.assertEqual(self.issue(expected_key=b'x'*32)['reason'],'SIGNER_KEY_MISMATCH')

    def test_pending_or_rolled_back_store_no_sign(self):
        backup=self.root/'backup'; shutil.copyfile(self.store,backup); self.advance(); self.evidence(); self.signed()
        shutil.copyfile(backup,self.store); self.assertEqual(self.issue()['reason'],'ANCHOR_NOT_MATCHED')

    def test_revised_anchor_and_context(self):
        old=self.args(); self.advance(); self.assertEqual(self.issue()['reason'],'HOST_ADMISSION_INVALID'); self.evidence()
        fresh=self.args(); result=g.verify(**fresh); self.assertEqual(result['status'],'PUBLIC_SIGNATURE_AND_REPLAY_MATCHED_ONLY')
        self.assertEqual(result['payload']['anchor_tip']['sequence'],2); self.assertEqual(result['payload']['committed_tip']['sequence'],1)
        self.assertEqual(g.verify(**dict(old,expected_anchor=self.tip))['reason'],'SEALED_ANCHOR_MISMATCH')

    def test_revision_log_omission(self):
        self.advance(); self.evidence(); args=self.args(); log=p.strict(args['revision_log']); log['events']=[]; args['revision_log']=b.canonical(log)
        self.assertEqual(g.verify(**args)['status'],'HOLD')

    def test_noncanonical_packet(self):
        args=self.args(); args['packet']+=b' '; self.assertEqual(g.verify(**args)['status'],'HOLD')


if __name__=='__main__': unittest.main()
