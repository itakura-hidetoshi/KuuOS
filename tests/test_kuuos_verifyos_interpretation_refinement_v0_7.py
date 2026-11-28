"""Synthetic pinned subprocess fixtures and append-only confirmation tests."""
import copy
from pathlib import Path
import tempfile
import unittest
from runtime import kuuos_verifyos_interpretation_refinement_v0_7 as g

b, p, f = g.b, g.p, g.f


class RefinementTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.root = Path(tmp.name)
        for d in ('base','gates','ledger'): (self.root/d).mkdir()
        for name in b.BASE: (self.root/'base'/name).write_text('synthetic fixture')
        ledger = self.root/'ledger/000000000000.json'; ledger.write_text('synthetic ledger'); tip = b.sha(ledger.read_bytes())
        payloads = [dict(status=s,seq=0,tip_sha256=tip,proof_authority=False,action_authority=False) for s in b.EXPECTED]
        payloads[0].update(rule_count=10,withdrawn_count=0,obstruction_count=2,research_certificate_count=2)
        payloads[1]['reviews'] = dict(candidate=1,held=12,no_use=0)
        for name, payload in zip(b.GATES,payloads): (self.root/'gates'/name).write_text('import json\nprint(json.dumps('+repr(payload)+'))\n')
        h = b.inventory(self.root,0)
        self.request = dict(challenge='a'*64,seq=0,tip=tip,expected_hashes={k:v for k,v in h.items() if k.startswith('gates/') or k=='base/'+b.BASE[2]})
        self.question = '取得済み台帳について、tip、認証状況を教えて。'.encode()
        self.analysis = f.analyze(self.question); self.family = self.analysis['family']; self.candidate = b.canonical(self.family)
        self.context = dict(turn_id='b'*64,question_sha256=b.sha(self.question),challenge=self.request['challenge'],request_sha256=b.sha(b.canonical(self.request)),audience=p.AUDIENCE)
        self.log = g.empty_log(self.family,self.context)
        self.spans = [i for i,r in enumerate(self.analysis['trace']) if r['kind']=='ambiguous_clause']
        self.key = bytes(range(32))
        self.raw,self.admission = p.execute_and_admit(self.root,self.request,self.context,self.key)
        self.prior = p.publish(self.raw,self.admission,self.request,self.context,self.key)

    def append(self, span, choice, **kw):
        events=self.log['events']; seq=len(events)+1
        ev=dict(schema=g.EVENT_SCHEMA,sequence=seq,parent_sha256=b.sha(b.canonical(events[-1])) if events else self.log['genesis'],event_id=f'{seq:064x}',source='host_captured_explicit_user_confirmation',span_index=span,choice_index=choice,span_sha256=self.analysis['trace'][span]['span_sha256'])
        ev.update(kw); events.append(ev)
        return ev

    def args(self, **kw):
        raw=b.canonical(self.log)
        args=dict(question=self.question,candidate=self.candidate,request=self.request,context=self.context,log_bytes=raw,trusted_log_sha256=b.sha(raw),raw=self.raw,admission=self.admission,key=self.key,prior_packet=self.prior)
        args.update(kw); return args

    def replay(self, **kw):
        a=self.args(**kw); return g.replay(*(a[k] for k in ('question','candidate','request','context','log_bytes','trusted_log_sha256')))

    def pub(self, **kw): return g.publish_question(**self.args(**kw))

    def test_empty_log_preserves_family(self):
        r=self.replay(); self.assertEqual(len(r['active_ids']),4); self.assertEqual(r['excluded'],[])
        self.assertEqual(p.strict(self.pub())['publication']['status'],'AMBIGUOUS_PARTIAL')

    def test_every_two_choice_refinement(self):
        for x in (0,1):
            for y in (0,1):
                self.log=g.empty_log(self.family,self.context); self.append(self.spans[0],x); self.append(self.spans[1],y)
                r=self.replay(); self.assertEqual(r['status'],'REFINEMENT_CHECKED_BOUNDED_ONLY')
                wanted=[i['interpretation_id'] for i in self.family['interpretations'] if i['choices'][self.spans[0]]==x and i['choices'][self.spans[1]]==y]
                self.assertEqual(r['active_ids'],wanted); self.assertEqual(len(r['excluded']),3)
                self.assertEqual([e['sequence'] for e in r['excluded']],[1,1,2])
                self.assertEqual(set(r['active_ids'])|{e['interpretation_id'] for e in r['excluded']},{i['interpretation_id'] for i in self.family['interpretations']})

    def test_single_confirmation_keeps_two_branches(self):
        self.append(self.spans[0],0); r=self.replay(); self.assertEqual(len(r['active_ids']),2)
        self.assertEqual(len(r['excluded']),2); self.assertNotIn('current_tip',r['active_union_claim_ids'])

    def test_no_log_anchor(self): self.assertEqual(self.replay(trusted_log_sha256=None)['status'],'HOLD')

    def test_truncation_and_rehash(self):
        self.append(self.spans[0],0); digest=self.args()['trusted_log_sha256']; self.log['events'].clear()
        self.assertEqual(self.replay(trusted_log_sha256=digest)['reason'],'LOG_ANCHOR_MISMATCH')

    def test_model_preference_not_confirmation(self):
        self.append(self.spans[0],0,source='model_preference'); self.assertEqual(self.replay()['reason'],'CONFIRMATION_REQUIRED')

    def test_wrong_parent(self):
        self.append(self.spans[0],0,parent_sha256='d'*64); self.assertEqual(self.replay()['reason'],'EVENT_CHAIN')

    def test_wrong_span(self):
        self.append(self.spans[0],0,span_sha256='d'*64); self.assertEqual(self.replay()['reason'],'SPAN_BINDING')

    def test_invalid_choice(self):
        self.append(self.spans[0],2); self.assertEqual(self.replay()['reason'],'CHOICE_INDEX')

    def test_wrong_context(self):
        self.assertEqual(self.replay(context=dict(self.context,turn_id='d'*64))['reason'],'LOG_CONTEXT_MISMATCH')

    def test_duplicate_event_id(self):
        ev=self.append(self.spans[0],0); self.append(self.spans[1],0,event_id=ev['event_id']); self.assertEqual(self.replay()['reason'],'EVENT_REPLAY')

    def test_conflicting_confirmation_preserves_prefix(self):
        self.append(self.spans[0],0); self.append(self.spans[0],1)
        r=self.replay(); self.assertEqual(r['status'],'HOLD'); self.assertEqual(len(r['verified_events']),1); self.assertEqual(r['rejected_event']['sequence'],2)
        self.assertEqual(len(r['analysis']['family']['interpretations']),4); self.assertEqual(p.strict(self.pub())['status'],'HOLD')

    def test_complete_active_view_not_original_global_pass(self):
        self.append(self.spans[0],0); self.append(self.spans[1],0)
        packet=self.pub(); r=p.strict(packet)['publication']; self.assertEqual(r['status'],'ACTIVE_VIEW_ALL_OBSERVED')
        self.assertEqual(r['original_family_status'],'AMBIGUOUS_PARTIAL'); self.assertEqual(len(r['branches']),4)
        self.assertEqual(sum(x['active_in_confirmed_view'] for x in r['branches']),1)
        self.assertEqual(g.verified_display(packet,**self.args()),(packet,0))
        self.assertTrue(all(r[k] is False for k in g.BOUNDARY))
        self.assertIsNone(r['selected_interpretation'])

    def test_active_freshness_remains_hold(self):
        self.append(self.spans[0],1); self.append(self.spans[1],0)
        packet=self.pub(); r=p.strict(packet)['publication']; self.assertEqual(r['status'],'ACTIVE_VIEW_PARTIAL')
        self.assertEqual(g.verified_display(packet,**self.args()),(packet,2))
        self.assertIn('current_tip',r['refinement']['active_union_claim_ids'])

    def test_missing_evidence_keeps_all_branches(self):
        self.append(self.spans[0],0); obj=p.strict(self.pub(admission=None)); self.assertEqual(obj['status'],'HOLD')
        self.assertEqual(len(obj['branches']),4); self.assertTrue(all(x['status']=='HOLD' for x in obj['claims']))

    def test_display_rejects_removed_exclusion(self):
        self.append(self.spans[0],0); obj=p.strict(self.pub()); obj['publication']['refinement']['excluded'].pop()
        out,rc=g.verified_display(b.canonical(obj),**self.args()); self.assertEqual((p.strict(out)['status'],rc),('HOLD',2))

    def test_display_rejects_omitted_branch(self):
        obj=p.strict(self.pub()); obj['publication']['branches'].pop()
        out,rc=g.verified_display(b.canonical(obj),**self.args()); self.assertEqual((p.strict(out)['status'],rc),('HOLD',2))


if __name__=='__main__': unittest.main()
