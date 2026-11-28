"""Synthetic fixtures; exercise anchored replay and fresh-context subprocess evidence."""
import copy
from pathlib import Path
import tempfile
import unittest
from runtime import kuuos_verifyos_interpretation_revision_v0_8 as g

b,p,f,r = g.b,g.p,g.f,g.r


class RevisionTests(unittest.TestCase):
    def setUp(self):
        self.question='取得済み台帳について、tip、認証状況を教えて。'.encode()
        analysis=f.analyze(self.question); self.family=analysis['family']; self.candidate=b.canonical(self.family)
        self.spans=[i for i,row in enumerate(analysis['trace']) if row['kind']=='ambiguous_clause']; self.trace=analysis['trace']
        self.request=dict(challenge='a'*64,seq=0,tip='c'*64,expected_hashes={k:'d'*64 for k in ['base/'+b.BASE[2],*('gates/'+x for x in b.GATES)]})
        self.context=self.ctx(self.request,1)
        self.base=r.empty_log(self.family,self.context)
        for i in self.spans:
            es=self.base['events']; seq=len(es)+1
            es.append(dict(schema=r.EVENT_SCHEMA,sequence=seq,parent_sha256=g.digest(es[-1]) if es else self.base['genesis'],event_id=f'{seq:064x}',source='host_captured_explicit_user_confirmation',span_index=i,choice_index=0,span_sha256=self.trace[i]['span_sha256']))
        self.reset()

    def ctx(self,request,turn):
        return dict(turn_id=f'{turn:064x}',question_sha256=b.sha(self.question),challenge=request['challenge'],request_sha256=g.digest(request),audience=p.AUDIENCE)

    def reset(self):
        raw=b.canonical(self.base); self.seed=r.replay(self.question,self.candidate,self.request,self.context,raw,b.sha(raw))
        self.assertEqual(self.seed['status'],'REFINEMENT_CHECKED_BOUNDED_ONLY')
        self.log=g.empty_log(self.seed,self.context); self.current_request=self.request; self.current_context=self.context

    def args(self,**kw):
        base,rev=b.canonical(self.base),b.canonical(self.log)
        args=dict(question=self.question,candidate=self.candidate,base_request=self.request,base_context=self.context,base_log=base,base_anchor=b.sha(base),revision_log=rev,revision_anchor=b.sha(rev),current_request=self.current_request,current_context=self.current_context)
        args.update(kw); return args

    def replay(self,**kw): return g.replay(**self.args(**kw))

    def append(self,i,op,choice,**kw):
        before=self.replay(); self.assertEqual(before['status'],g.OK)
        active={x['span_index']:x['event_sha256'] for x in before['effective_confirmations']}
        es=self.log['events']; seq=len(es)+1
        req=dict(self.request,challenge=f'{100+seq:064x}'); ctx=self.ctx(req,100+seq)
        ev=dict(schema=g.EVENT,sequence=seq,parent_sha256=g.digest(es[-1]) if es else self.log['genesis'],event_id=f'{200+seq:064x}',source='host_captured_explicit_user_revision',operation=op,span_index=i,span_sha256=self.trace[i]['span_sha256'],choice_index=choice,target_event_sha256=active.get(i),next_request=req,next_context=ctx)
        ev.update(kw); es.append(ev); self.current_request=ev['next_request']; self.current_context=ev['next_context']; return ev

    def test_empty_history(self):
        r0=self.replay(); self.assertEqual(r0['status'],g.OK); self.assertEqual(r0['active_ids'],self.seed['active_ids'])

    def test_retract_restores_not_erases(self):
        self.append(self.spans[0],'retract',None); result=self.replay(); self.assertEqual(result['status'],g.OK)
        self.assertEqual(len(result['active_ids']),2); self.assertEqual(len(result['seed']['excluded']),3)
        self.assertEqual(len(result['verified_revisions'][0]['restored_ids']),1); self.assertIn('current_tip',result['active_union_claim_ids'])
        self.assertFalse(result['excluded_interpretations_refuted'])

    def test_replace_reopens_other_branch(self):
        self.append(self.spans[0],'replace',1); result=self.replay(); row=result['verified_revisions'][0]
        self.assertEqual(result['status'],g.OK); self.assertEqual(len(result['active_ids']),1)
        self.assertEqual(row['removed_ids'],self.seed['active_ids']); self.assertEqual(row['restored_ids'],result['active_ids'])

    def test_retract_both_restores_every_branch(self):
        for i in self.spans: self.append(i,'retract',None)
        result=self.replay(); self.assertEqual(result['active_ids'],[x['interpretation_id'] for x in self.family['interpretations']]); self.assertEqual(result['effective_confirmations'],[])

    def test_reconfirm_after_retraction(self):
        self.append(self.spans[0],'retract',None); self.append(self.spans[0],'confirm',1)
        result=self.replay(); self.assertEqual(result['status'],g.OK); self.assertEqual(len(result['verified_revisions']),2); self.assertEqual(len(result['active_ids']),1)

    def test_wrong_target_retains_valid_prefix(self):
        self.append(self.spans[0],'replace',1); before=self.replay()['active_ids']; self.append(self.spans[1],'retract',None,target_event_sha256='f'*64)
        result=self.replay(); self.assertEqual(result['reason'],'STALE_REVISION_TARGET'); self.assertEqual(result['active_ids'],before); self.assertEqual(len(result['verified_revisions']),1); self.assertEqual(result['rejected_event']['sequence'],2)

    def test_stale_context(self):
        self.append(self.spans[0],'retract',None,next_request=self.request,next_context=self.context); self.assertEqual(self.replay()['reason'],'FRESH_CONTEXT_REQUIRED')

    def test_independent_current_context_required(self):
        self.append(self.spans[0],'retract',None); self.assertEqual(self.replay(current_request=self.request,current_context=self.context)['reason'],'CURRENT_CONTEXT_MISMATCH')

    def test_model_preference_rejected(self):
        self.append(self.spans[0],'retract',None,source='model_preference'); self.assertEqual(self.replay()['reason'],'REVISION_CAPTURE_REQUIRED')

    def test_wrong_parent(self):
        self.append(self.spans[0],'retract',None,parent_sha256='f'*64); self.assertEqual(self.replay()['reason'],'EVENT_CHAIN')

    def test_duplicate_id_from_seed(self):
        self.append(self.spans[0],'retract',None,event_id=self.base['events'][0]['event_id']); self.assertEqual(self.replay()['reason'],'REVISION_CAPTURE_REQUIRED')

    def test_revision_truncation(self):
        self.append(self.spans[0],'retract',None); anchor=self.args()['revision_anchor']; self.log['events'].clear(); self.assertEqual(self.replay(revision_anchor=anchor)['reason'],'REVISION_ANCHOR_MISMATCH')

    def test_base_truncation(self):
        self.assertEqual(self.replay(base_anchor='f'*64)['reason'],'INVALID_SEED')

    def test_noop_replacement(self):
        self.append(self.spans[0],'replace',0); self.assertEqual(self.replay()['reason'],'REPLACEMENT_NO_CHANGE')

    def test_changed_original_question(self):
        ev=self.append(self.spans[0],'retract',None); ev['next_context']['question_sha256']='f'*64; self.assertEqual(self.replay()['reason'],'QUESTION_CHANGED')

    def fixture(self):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); root=Path(tmp.name)
        for d in ('base','gates','ledger'): (root/d).mkdir()
        for name in b.BASE: (root/'base'/name).write_text('synthetic fixture')
        ledger=root/'ledger/000000000000.json'; ledger.write_text('synthetic ledger'); tip=b.sha(ledger.read_bytes())
        payloads=[dict(status=s,seq=0,tip_sha256=tip,proof_authority=False,action_authority=False) for s in b.EXPECTED]
        payloads[0].update(rule_count=10,withdrawn_count=0,obstruction_count=2,research_certificate_count=2); payloads[1]['reviews']=dict(candidate=1,held=12,no_use=0)
        for name,payload in zip(b.GATES,payloads): (root/'gates'/name).write_text('import json\nprint(json.dumps('+repr(payload)+'))\n')
        h=b.inventory(root,0); self.request.update(tip=tip,expected_hashes={k:v for k,v in h.items() if k.startswith('gates/') or k=='base/'+b.BASE[2]}); self.context=self.ctx(self.request,1)
        self.base['genesis']=r.genesis(self.family,self.context)
        for i,ev in enumerate(self.base['events']): ev['parent_sha256']=g.digest(self.base['events'][i-1]) if i else self.base['genesis']
        self.reset(); return root,bytes(range(32))

    def evidence(self,root,key,request,context):
        raw,admission=p.execute_and_admit(root,request,context,key); self.assertIsNotNone(admission)
        return dict(raw=raw,admission=admission,key=key,prior_packet=p.publish(raw,admission,request,context,key))

    def test_old_receipt_cannot_follow_correction(self):
        root,key=self.fixture(); old=self.evidence(root,key,self.request,self.context); self.append(self.spans[0],'retract',None)
        out=p.strict(g.publish_question(**old,**self.args())); self.assertEqual(out['status'],'HOLD'); self.assertEqual(len(out['branches']),4); self.assertTrue(all(x['status']=='HOLD' for x in out['claims']))

    def test_new_evidence_preserves_restored_branch(self):
        root,key=self.fixture(); self.append(self.spans[0],'retract',None); new=self.evidence(root,key,self.current_request,self.current_context)
        packet=g.publish_question(**new,**self.args()); out=p.strict(packet)['publication']; self.assertEqual(out['status'],'AMBIGUOUS_PARTIAL'); self.assertEqual(len(out['branches']),4); self.assertEqual(sum(x['active_in_revised_view'] for x in out['branches']),2)
        self.assertEqual(g.verified_display(packet,**new,**self.args()),(packet,2)); self.assertTrue(all(out[k] is False for k in g.BOUNDARY))
        out2=p.strict(packet); out2['publication']['revision']['verified_revisions'][0]['restored_ids']=[]
        blocked,rc=g.verified_display(b.canonical(out2),**new,**self.args()); self.assertEqual((p.strict(blocked)['status'],rc),('HOLD',2))

    def test_new_evidence_single_partial(self):
        root,key=self.fixture(); self.append(self.spans[0],'replace',1); new=self.evidence(root,key,self.current_request,self.current_context)
        packet=g.publish_question(**new,**self.args()); self.assertEqual(p.strict(packet)['publication']['status'],'ACTIVE_VIEW_PARTIAL')


if __name__=='__main__': unittest.main()
