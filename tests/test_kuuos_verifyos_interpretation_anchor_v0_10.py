"""Separate local SQLite files; synthetic confirmations, real transactions."""
from contextlib import closing
import multiprocessing as mp
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from runtime import kuuos_verifyos_interpretation_anchor_v0_10 as g

s, v, b, p, r, f = g.s, g.v, g.b, g.p, g.v.r, g.v.f


def compete(queue, barrier, args):
    barrier.wait(timeout=15)
    out = g.prepare(*args)
    queue.put((out['status'], out.get('reason')))


class AnchorTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.root = Path(tmp.name)
        (self.root/'anchors').mkdir()
        self.store = self.root/'store.sqlite'; self.anchor = self.root/'anchors'/'anchor.sqlite'
        self.question = '取得済み台帳について、tip、認証状況を教えて。'.encode()
        a = f.analyze(self.question); self.family = a['family']; self.trace = a['trace']
        self.spans = [i for i,x in enumerate(self.trace) if x['kind']=='ambiguous_clause']
        self.req = dict(challenge='a'*64,seq=0,tip='c'*64,expected_hashes={k:'d'*64 for k in ['base/'+b.BASE[2],*('gates/'+x for x in b.GATES)]})
        self.ctx = self.context(self.req,1); base = b.canonical(r.empty_log(self.family,self.ctx))
        self.seed = dict(question=self.question,candidate=b.canonical(self.family),base_request=self.req,base_context=self.ctx,base_log=base,base_anchor=b.sha(base))
        self.genesis = s.initialize(self.store,self.seed)['tip']
        out = g.initialize(self.store,self.anchor,self.seed,self.genesis)
        self.assertEqual(out['status'],'ANCHOR_GENESIS_RECORDED'); self.anchor_tip = out['anchor_tip']

    def context(self,req,turn):
        return dict(turn_id=f'{turn:064x}',question_sha256=b.sha(self.question),challenge=req['challenge'],request_sha256=v.digest(req),audience=p.AUDIENCE)

    def event(self,span=0,choice=0,nonce=10,op='confirm',**kw):
        snap=s.read(self.store,self.seed); inputs=snap['inputs']; log=p.strict(inputs['revision_log']); checked=v.replay(**inputs)
        i=self.spans[span]; prev={x['span_index']:x['event_sha256'] for x in checked['effective_confirmations']}
        req=dict(self.req,challenge=f'{nonce:064x}'); ctx=self.context(req,nonce)
        ev=dict(schema=v.EVENT,sequence=len(log['events'])+1,parent_sha256=v.digest(log['events'][-1]) if log['events'] else log['genesis'],event_id=f'{nonce+100:064x}',source='host_captured_explicit_user_revision',operation=op,span_index=i,span_sha256=self.trace[i]['span_sha256'],choice_index=choice,target_event_sha256=prev.get(i),next_request=req,next_context=ctx)
        ev.update(kw); raw=b.canonical(ev); return raw,b.sha(raw),req,ctx

    def read(self,tip=None): return g.read(self.store,self.anchor,self.seed,self.anchor_tip if tip is None else tip)

    def prepare(self,event=None):
        event=self.event() if event is None else event
        out=g.prepare(self.store,self.anchor,self.seed,self.anchor_tip,*event)
        self.assertEqual(out['status'],'INTENT_PREPARED_NOT_COMMITTED'); self.anchor_tip=out['anchor_tip']; return event,out

    def resume(self,event):
        return g.resume(self.store,self.anchor,self.seed,self.anchor_tip,*event)

    def seal(self,event):
        out=self.resume(event); self.assertEqual(out['status'],'ANCHOR_SEALED'); self.anchor_tip=out['anchor_tip']; return out

    def advance(self,event=None):
        event,_=self.prepare(event); return self.seal(event)

    def raw_append(self,event,previous=None):
        return s.append(self.store,self.seed,self.genesis if previous is None else previous,*event)

    def test_genesis_read(self):
        out=self.read(); self.assertEqual(out['status'],'ANCHOR_MATCHED_SNAPSHOT_ONLY'); self.assertTrue(out['anchor_snapshot_matched'])
        self.assertFalse(out['external_rollback_prevention_verified'])

    def test_prepare_holds_without_append(self):
        _,out=self.prepare(); self.assertEqual(out['committed_tip'],self.genesis)
        self.assertEqual(s.read(self.store,self.seed)['tip'],self.genesis)
        self.assertEqual(self.read()['reason'],'PENDING_INTENT_REQUIRES_EXPLICIT_RECOVERY')

    def test_seal_and_reopen(self):
        out=self.advance(); self.assertEqual(out['committed_tip']['sequence'],1)
        self.assertEqual(self.read()['committed_tip'],out['committed_tip'])

    def test_two_updates_preserve_anchor_rows(self):
        def rows():
            with closing(sqlite3.connect(self.anchor)) as db:
                return db.execute('SELECT * FROM anchor_rows ORDER BY sequence').fetchall()
        old=rows(); self.advance(); new=rows(); self.assertEqual(new[:-2],old)
        self.advance(self.event(op='retract',choice=None,nonce=11))
        self.assertEqual(rows()[:-2],new); self.assertEqual(self.read()['committed_tip']['sequence'],2)

    def test_restore_old_store_detected(self):
        backup=self.root/'backup'; shutil.copyfile(self.store,backup); self.advance()
        shutil.copyfile(backup,self.store)
        self.assertEqual(self.read()['reason'],'STORE_ROLLBACK_RELATIVE_TO_ANCHOR')

    def test_same_height_fork_detected(self):
        backup=self.root/'backup'; shutil.copyfile(self.store,backup); self.advance()
        shutil.copyfile(backup,self.store); self.assertEqual(self.raw_append(self.event(choice=1,nonce=12))['status'],'LOCAL_APPEND_COMMITTED')
        self.assertEqual(self.read()['reason'],'STORE_DIVERGED_AT_ANCHORED_SEQUENCE')

    def test_unanchored_ahead_not_adopted(self):
        self.assertEqual(self.raw_append(self.event())['status'],'LOCAL_APPEND_COMMITTED')
        self.assertEqual(self.read()['reason'],'STORE_UNANCHORED_AHEAD')
        self.assertEqual(g.initialize(self.store,self.root/'new.sqlite',self.seed,self.genesis)['reason'],'STORE_UNANCHORED_AHEAD')

    def test_anchor_rollback_detected_by_retained_head(self):
        backup=self.root/'anchor_backup'; shutil.copyfile(self.anchor,backup); self.advance()
        shutil.copyfile(backup,self.anchor); self.assertEqual(self.read()['reason'],'ANCHOR_EXPECTATION_MISMATCH')

    def test_prepared_resume_after_store_commit(self):
        event,prepared=self.prepare(); target=self.raw_append(event)['tip']
        self.assertEqual(target,prepared['pending']['target']); self.assertEqual(self.read()['status'],'HOLD')
        self.assertEqual(self.seal(event)['committed_tip'],target)
        self.assertEqual(s.read(self.store,self.seed)['tip']['sequence'],1)

    def test_injected_seal_failure_retains_intent(self):
        event,prepared=self.prepare(); original=g.insert
        def fail(*args):
            if args[4]=='SEAL': raise sqlite3.OperationalError('injected before seal')
            return original(*args)
        with patch.object(g,'insert',fail): self.assertEqual(self.resume(event)['status'],'HOLD')
        self.assertEqual(s.read(self.store,self.seed)['tip'],prepared['pending']['target'])
        self.assertEqual(self.read()['reason'],'PENDING_INTENT_REQUIRES_EXPLICIT_RECOVERY')
        self.seal(event); self.assertEqual(self.read()['committed_tip']['sequence'],1)

    def test_wrong_recovery_event_rejected(self):
        event,_=self.prepare(); other=self.event(choice=1,nonce=12)
        self.assertEqual(self.resume(other)['reason'],'PREPARED_INTENT_MISMATCH'); self.seal(event)

    def test_unplanned_fork_while_pending_rejected(self):
        event,_=self.prepare(); self.raw_append(self.event(choice=1,nonce=12))
        self.assertEqual(self.resume(event)['reason'],'STORE_DIVERGED_AT_ANCHORED_SEQUENCE')
        self.assertEqual(self.read()['status'],'HOLD')

    def test_stale_anchor_after_prepare(self):
        old=self.anchor_tip; event,_=self.prepare()
        self.assertEqual(g.resume(self.store,self.anchor,self.seed,old,*event)['reason'],'ANCHOR_EXPECTATION_MISMATCH')

    def test_invalid_event_does_not_prepare(self):
        out=g.prepare(self.store,self.anchor,self.seed,self.anchor_tip,*self.event(source='model_preference'))
        self.assertEqual(out['reason'],'REVISION_INVALID'); self.assertEqual(self.read()['anchor_tip'],self.anchor_tip)

    def test_wrong_event_digest(self):
        raw,_,req,ctx=self.event()
        self.assertEqual(g.prepare(self.store,self.anchor,self.seed,self.anchor_tip,raw,'f'*64,req,ctx)['reason'],'EVENT_ANCHOR_MISMATCH')

    def test_schema_and_chain_checks(self):
        with closing(sqlite3.connect(self.anchor)) as db, db: db.execute('UPDATE anchor_rows SET payload=? WHERE sequence=0',(b'bad',))
        self.assertEqual(self.read()['reason'],'ANCHOR_CHAIN')

    def test_exclusive_initialization_and_alias(self):
        before=self.anchor.read_bytes()
        self.assertEqual(g.initialize(self.store,self.anchor,self.seed,self.genesis)['status'],'HOLD'); self.assertEqual(self.anchor.read_bytes(),before)
        self.assertEqual(g.read(self.store,self.store,self.seed,self.anchor_tip)['reason'],'SEPARATE_PATHS_REQUIRED')

    def test_two_competing_prepare_processes(self):
        args=[(self.store,self.anchor,self.seed,self.anchor_tip,*self.event(span=i,nonce=10+i)) for i in range(2)]
        ctx=mp.get_context('spawn'); queue=ctx.Queue(); barrier=ctx.Barrier(2)
        jobs=[ctx.Process(target=compete,args=(queue,barrier,x)) for x in args]
        try:
            for job in jobs: job.start()
            outcomes=[queue.get(timeout=25) for _ in jobs]
            for job in jobs: job.join(timeout=10); self.assertEqual(job.exitcode,0)
            self.assertCountEqual(outcomes,[('INTENT_PREPARED_NOT_COMMITTED',None),('HOLD','ANCHOR_EXPECTATION_MISMATCH')])
            self.assertEqual(s.read(self.store,self.seed)['tip'],self.genesis)
        finally:
            for job in jobs:
                if job.is_alive(): job.terminate(); job.join()
            queue.close(); queue.join_thread()

    def test_pending_cannot_publish(self):
        self.prepare(); out=g.publish_snapshot(self.store,self.anchor,self.seed,self.anchor_tip,None,None,None,None)
        self.assertEqual(out['status'],'HOLD')

    def test_matching_anchor_not_evidence_pass(self):
        out=g.publish_snapshot(self.store,self.anchor,self.seed,self.anchor_tip,None,None,None,None)
        self.assertEqual(out['status'],'ANCHORED_SNAPSHOT_PACKET_ONLY'); self.assertEqual(p.strict(out['packet'])['status'],'HOLD')
        self.assertFalse(out['current_at_delivery_verified'])


    def test_egress_bound_to_anchored_revision(self):
        root=self.root/'snapshot'; root.mkdir()
        for d in ('base','gates','ledger'): (root/d).mkdir()
        for name in b.BASE: (root/'base'/name).write_text('synthetic fixture')
        ledger=root/'ledger/000000000000.json'; ledger.write_text('synthetic ledger'); tip=b.sha(ledger.read_bytes())
        for name,status in zip(b.GATES,b.EXPECTED):
            data=dict(status=status,seq=0,tip_sha256=tip,proof_authority=False,action_authority=False,rule_count=10,withdrawn_count=0,obstruction_count=2,research_certificate_count=2,reviews=dict(candidate=1,held=12,no_use=0))
            (root/'gates'/name).write_text('import json\nprint(json.dumps('+repr(data)+'))\n')
        inv=b.inventory(root,0); self.req.update(tip=tip,expected_hashes={k:z for k,z in inv.items() if k.startswith('gates/') or k=='base/'+b.BASE[2]}); self.ctx=self.context(self.req,1)
        base=b.canonical(r.empty_log(self.family,self.ctx)); self.seed.update(base_request=self.req,base_context=self.ctx,base_log=base,base_anchor=b.sha(base))
        self.store=self.root/'live.sqlite'; self.anchor=self.root/'anchors'/'live.sqlite'
        self.genesis=s.initialize(self.store,self.seed)['tip']; self.anchor_tip=g.initialize(self.store,self.anchor,self.seed,self.genesis)['anchor_tip']
        key=bytes(range(32)); raw,adm=p.execute_and_admit(root,self.req,self.ctx,key); self.assertIsNotNone(adm)
        prior=p.publish(raw,adm,self.req,self.ctx,key)
        self.advance(); snap=self.read(); inputs=snap['inputs']
        stale=g.publish_snapshot(self.store,self.anchor,self.seed,self.anchor_tip,raw,adm,key,prior)
        self.assertEqual(p.strict(stale['packet'])['status'],'HOLD')
        req,ctx=inputs['current_request'],inputs['current_context']
        raw,adm=p.execute_and_admit(root,req,ctx,key); self.assertIsNotNone(adm)
        fresh=g.publish_snapshot(self.store,self.anchor,self.seed,self.anchor_tip,raw,adm,key,p.publish(raw,adm,req,ctx,key))
        self.assertEqual(p.strict(fresh['packet'])['publication']['status'],'AMBIGUOUS_PARTIAL')
        self.assertTrue(fresh['anchor_snapshot_matched']); self.assertFalse(fresh['current_at_delivery_verified'])


if __name__=='__main__': unittest.main()
