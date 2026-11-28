"""Actual local SQLite transactions with synthetic user revisions and gate scripts."""
from contextlib import closing
import multiprocessing as mp
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from runtime import kuuos_verifyos_interpretation_store_v0_9 as g

v,b,p,r,f = g.v,g.b,g.p,g.r,g.v.f


def worker(queue, barrier, args):
    barrier.wait(timeout=15)
    result = g.append(*args)
    queue.put((result['status'],result.get('reason')))


class StoreTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.root=Path(tmp.name)
        self.path=self.root/'revisions.sqlite'; self.question='取得済み台帳について、tip、認証状況を教えて。'.encode()
        a=f.analyze(self.question); self.family=a['family']; self.trace=a['trace']; self.spans=[i for i,x in enumerate(self.trace) if x['kind']=='ambiguous_clause']
        self.request=dict(challenge='a'*64,seq=0,tip='c'*64,expected_hashes={k:'d'*64 for k in ['base/'+b.BASE[2],*('gates/'+x for x in b.GATES)]})
        self.context=self.ctx(self.request,1); base=r.empty_log(self.family,self.context); raw=b.canonical(base)
        self.seed=dict(question=self.question,candidate=b.canonical(self.family),base_request=self.request,base_context=self.context,base_log=raw,base_anchor=b.sha(raw))
        start=g.initialize(self.path,self.seed); self.assertEqual(start['status'],'LOCAL_SNAPSHOT_REPLAYED_ONLY'); self.tip=start['tip']

    def ctx(self,req,turn):
        return dict(turn_id=f'{turn:064x}',question_sha256=b.sha(self.question),challenge=req['challenge'],request_sha256=v.digest(req),audience=p.AUDIENCE)

    def event(self,span=0,choice=0,nonce=10,operation='confirm',**kw):
        snap=g.read(self.path,self.seed); self.assertEqual(snap['status'],'LOCAL_SNAPSHOT_REPLAYED_ONLY')
        inputs=snap['inputs']; log=p.strict(inputs['revision_log']); check=v.replay(**inputs); i=self.spans[span]
        prev={x['span_index']:x['event_sha256'] for x in check['effective_confirmations']}
        req=dict(self.request,challenge=f'{nonce:064x}'); ctx=self.ctx(req,nonce)
        ev=dict(schema=v.EVENT,sequence=len(log['events'])+1,parent_sha256=v.digest(log['events'][-1]) if log['events'] else log['genesis'],event_id=f'{nonce+100:064x}',source='host_captured_explicit_user_revision',operation=operation,span_index=i,span_sha256=self.trace[i]['span_sha256'],choice_index=choice,target_event_sha256=prev.get(i),next_request=req,next_context=ctx)
        ev.update(kw); raw=b.canonical(ev)
        return (self.path,self.seed,snap['tip'],raw,b.sha(raw),req,ctx)

    def test_reopen(self):
        out=g.append(*self.event()); self.assertEqual(out['status'],'LOCAL_APPEND_COMMITTED'); self.assertEqual(out['tip']['sequence'],1)
        snap=g.read(self.path,self.seed); self.assertEqual(snap['tip'],out['tip']); self.assertEqual(len(snap['active_ids']),2)
        self.assertFalse(snap['local_append_commit_confirmed'])

    def test_two_processes_one_winner(self):
        first=self.event(span=0,nonce=10); second=self.event(span=1,nonce=11)
        ctx=mp.get_context('spawn'); barrier=ctx.Barrier(2); queue=ctx.Queue()
        jobs=[ctx.Process(target=worker,args=(queue,barrier,x)) for x in (first,second)]
        try:
            for j in jobs: j.start()
            results=[queue.get(timeout=25) for _ in jobs]
            for j in jobs: j.join(timeout=10); self.assertEqual(j.exitcode,0)
            self.assertCountEqual(results,[('LOCAL_APPEND_COMMITTED',None),('HOLD','STALE_EXPECTED_TIP')])
            self.assertEqual(g.read(self.path,self.seed)['tip']['sequence'],1)
        finally:
            for j in jobs:
                if j.is_alive(): j.terminate(); j.join()
            queue.close(); queue.join_thread()

    def test_stale_tip_and_replay(self):
        args=self.event(); self.assertEqual(g.append(*args)['status'],'LOCAL_APPEND_COMMITTED')
        self.assertEqual(g.append(*args)['reason'],'STALE_EXPECTED_TIP')
        self.assertEqual(g.read(self.path,self.seed)['tip']['sequence'],1)

    def test_retract_append_preserves_history(self):
        self.assertEqual(g.append(*self.event())['status'],'LOCAL_APPEND_COMMITTED')
        result=g.append(*self.event(operation='retract',choice=None,nonce=11)); self.assertEqual(result['tip']['sequence'],2)
        self.assertEqual(len(result['active_ids']),4)
        log=p.strict(result['inputs']['revision_log']); self.assertEqual([x['operation'] for x in log['events']],['confirm','retract'])

    def test_prior_rows_byte_identical_after_append(self):
        def rows():
            with closing(sqlite3.connect(self.path)) as db:
                return db.execute('SELECT * FROM revision_rows ORDER BY sequence').fetchall()
        old=rows(); self.assertEqual(g.append(*self.event())['status'],'LOCAL_APPEND_COMMITTED')
        new=rows(); self.assertEqual(new[:-1],old)
        self.assertEqual(g.append(*self.event(operation='retract',choice=None,nonce=11))['status'],'LOCAL_APPEND_COMMITTED')
        self.assertEqual(rows()[:-1],new)

    def test_invalid_event_rolls_back(self):
        result=g.append(*self.event(source='model_preference')); self.assertEqual(result['status'],'HOLD')
        self.assertEqual(g.read(self.path,self.seed)['tip'],self.tip)

    def test_fault_after_insert_rolls_back(self):
        original=g.insert; args=self.event()
        def faulty(*a):
            original(*a); raise sqlite3.OperationalError('test after insert before commit')
        with patch.object(g,'insert',faulty): self.assertEqual(g.append(*args)['status'],'HOLD')
        self.assertEqual(g.read(self.path,self.seed)['tip'],self.tip)
        self.assertEqual(g.append(*args)['status'],'LOCAL_APPEND_COMMITTED')

    def test_event_anchor(self):
        args=list(self.event()); args[4]='f'*64; self.assertEqual(g.append(*args)['reason'],'EVENT_ANCHOR_MISMATCH')
        self.assertEqual(g.read(self.path,self.seed)['tip'],self.tip)

    def test_next_context_binding(self):
        args=list(self.event()); args[-1]=self.context; self.assertEqual(g.append(*args)['reason'],'NEXT_CONTEXT_MISMATCH')

    def test_wrong_seed(self):
        self.assertEqual(g.read(self.path,dict(self.seed,base_anchor='f'*64))['status'],'HOLD')

    def test_missing_db_does_not_create(self):
        path=self.root/'missing.sqlite'; args=list(self.event()); args[0]=path
        self.assertEqual(g.append(*args)['status'],'HOLD'); self.assertFalse(path.exists())
        self.assertEqual(g.read(path,self.seed)['status'],'HOLD'); self.assertFalse(path.exists())

    def test_initialization_never_overwrites(self):
        before=self.path.read_bytes(); self.assertEqual(g.initialize(self.path,self.seed)['status'],'HOLD'); self.assertEqual(self.path.read_bytes(),before)

    def test_modified_row_rejected(self):
        with closing(sqlite3.connect(self.path)) as db, db: db.execute("UPDATE revision_rows SET payload=x'00' WHERE sequence=0")
        self.assertEqual(g.read(self.path,self.seed)['reason'],'ROW_CHAIN_MISMATCH')

    def test_unexpected_schema_rejected(self):
        with closing(sqlite3.connect(self.path)) as db, db: db.execute('CREATE TABLE extra (x INTEGER)')
        self.assertEqual(g.read(self.path,self.seed)['reason'],'STORE_SCHEMA_MISMATCH')

    def test_deleted_tail_expected_tip_detected(self):
        out=g.append(*self.event()); newer=out['tip']
        with closing(sqlite3.connect(self.path)) as db, db: db.execute('DELETE FROM revision_rows WHERE sequence=1')
        args=list(self.event()); args[2]=newer
        self.assertEqual(g.append(*args)['reason'],'STALE_EXPECTED_TIP')
        self.assertFalse(g.read(self.path,self.seed)['external_rollback_prevention_verified'])

    def test_boolean_sequence_rejected(self):
        args=list(self.event()); args[2]=dict(self.tip,sequence=False)
        self.assertEqual(g.append(*args)['reason'],'STALE_EXPECTED_TIP')

    def test_snapshot_publication_rejects_stale_tip(self):
        g.append(*self.event()); out=g.publish_snapshot_at_tip(self.path,self.seed,self.tip,None,None,None,None)
        self.assertEqual(out['status'],'HOLD')

    def test_snapshot_publication_keeps_evidence_hold(self):
        out=g.publish_snapshot_at_tip(self.path,self.seed,self.tip,None,None,None,None)
        self.assertEqual(out['status'],'SNAPSHOT_PACKET_ONLY'); self.assertEqual(p.strict(out['packet'])['status'],'HOLD'); self.assertFalse(out['current_at_delivery_verified'])

    def test_live_synthetic_evidence_after_commit(self):
        root=self.root/'snapshot'; root.mkdir()
        for d in ('base','gates','ledger'): (root/d).mkdir()
        for name in b.BASE: (root/'base'/name).write_text('synthetic fixture')
        ledger=root/'ledger/000000000000.json'; ledger.write_text('synthetic ledger'); tip=b.sha(ledger.read_bytes())
        for name,status in zip(b.GATES,b.EXPECTED):
            data=dict(status=status,seq=0,tip_sha256=tip,proof_authority=False,action_authority=False,rule_count=10,withdrawn_count=0,obstruction_count=2,research_certificate_count=2,reviews=dict(candidate=1,held=12,no_use=0))
            (root/'gates'/name).write_text('import json\nprint(json.dumps('+repr(data)+'))\n')
        inv=b.inventory(root,0); self.request.update(tip=tip,expected_hashes={k:z for k,z in inv.items() if k.startswith('gates/') or k=='base/'+b.BASE[2]}); self.context=self.ctx(self.request,1)
        base=r.empty_log(self.family,self.context); raw=b.canonical(base); self.seed.update(base_request=self.request,base_context=self.context,base_log=raw,base_anchor=b.sha(raw))
        self.path=self.root/'live.sqlite'; start=g.initialize(self.path,self.seed); self.assertEqual(start['status'],'LOCAL_SNAPSHOT_REPLAYED_ONLY')
        oldraw,oldadm=p.execute_and_admit(root,self.request,self.context,bytes(range(32))); key=bytes(range(32)); oldprior=p.publish(oldraw,oldadm,self.request,self.context,key)
        result=g.append(*self.event()); self.assertEqual(result['status'],'LOCAL_APPEND_COMMITTED')
        current=result['inputs']; req,ctx=current['current_request'],current['current_context']
        stale=g.publish_snapshot_at_tip(self.path,self.seed,result['tip'],oldraw,oldadm,key,oldprior); self.assertEqual(p.strict(stale['packet'])['status'],'HOLD')
        newraw,newadm=p.execute_and_admit(root,req,ctx,key); self.assertIsNotNone(newadm)
        fresh=g.publish_snapshot_at_tip(self.path,self.seed,result['tip'],newraw,newadm,key,p.publish(newraw,newadm,req,ctx,key))
        self.assertEqual(p.strict(fresh['packet'])['publication']['status'],'AMBIGUOUS_PARTIAL')


if __name__=='__main__': unittest.main()
