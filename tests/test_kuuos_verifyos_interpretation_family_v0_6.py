"""Finite grammar and actual subprocess fixtures; not general semantics."""
from itertools import combinations, product
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from runtime import kuuos_verifyos_interpretation_family_v0_6 as g

b, p, q, t = g.b, g.p, g.q, g.t


def sentence(*words, current=False, fresh=False, suffix='を教えて。'):
    prefix = '空OSの現行継承台帳について、' if current else '取得済み台帳について、'
    return (prefix + '、'.join(words) + suffix + (t.FRESH if fresh else '')).encode()


class FamilyTests(unittest.TestCase):
    def test_all_120_registered_ambiguity_combinations(self):
        n = total_branches = 0
        for size in range(1, len(g.AMBIGUOUS)+1):
            for words in combinations(g.AMBIGUOUS, size):
                for current, fresh, suffix in product((False, True), (False, True), t.SUFFIXES):
                    question = sentence(*words, current=current, fresh=fresh, suffix=suffix)
                    result = g.analyze(question); self.assertEqual(result['status'], 'FAMILY_CANDIDATE')
                    f = result['family']; branches = f['interpretations']
                    expected = {frozenset(xs) | ({'current_state'} if current or fresh else set()) for xs in product(*(g.AMBIGUOUS[w] for w in words))}
                    self.assertEqual({frozenset(x['typed_question']['topics']) for x in branches}, expected)
                    self.assertEqual(len(branches), 2**size)
                    self.assertEqual(len({x['interpretation_id'] for x in branches}), len(branches))
                    sets = [set(x['contract']['plan']['claim_ids']) for x in branches]
                    self.assertEqual(set(f['common_claim_ids']), set.intersection(*sets))
                    self.assertEqual(set(f['union_claim_ids']), set.union(*sets))
                    cursor = 0
                    for row in result['trace']:
                        self.assertEqual(row['start_byte'], cursor); cursor = row['end_byte']
                        self.assertEqual(row['span_sha256'], b.sha(question[row['start_byte']:cursor]))
                    self.assertEqual(cursor, len(question))
                    self.assertEqual(g.check_family(question, b.canonical(f))['status'], g.OK)
                    n += 1; total_branches += len(branches)
        self.assertEqual((n,total_branches), (120,640))

    def test_predecessor_registered_preserved(self):
        for text in q.QUESTIONS:
            result = g.analyze(text.encode()); f = result['family']
            self.assertEqual(len(f['interpretations']), 1)
            self.assertEqual(f['interpretations'][0]['contract']['plan'], q.compile_question(text.encode())['plan'])

    def test_distinct_witnesses_same_plan_retained(self):
        f = g.analyze(sentence('検査結果','記録状況'))['family']
        self.assertEqual(len(f['interpretations']), 4)
        self.assertLess(len({b.sha(b.canonical(x['contract']['plan'])) for x in f['interpretations']}), 4)

    def test_current_condition_in_every_branch(self):
        for options in [{'current':True},{'fresh':True}]:
            f = g.analyze(sentence('記録状況', **options))['family']
            self.assertIn('current_tip',f['common_claim_ids'])

    def test_mixed_exact_ambiguous(self):
        f = g.analyze(sentence('規則数・撤回数・障害数・研究認証記録数','認証状況'))['family']
        self.assertEqual(len(f['interpretations']),2); self.assertIn('withdrawn_count',f['common_claim_ids'])

    def test_unknown_clause_retained(self):
        question = sentence('認証状況','取得禁止')
        result = g.analyze(question); self.assertEqual(result['status'],'HOLD')
        row = result['unresolved'][0]; self.assertEqual(question[row['start_byte']:row['end_byte']], '取得禁止'.encode())

    def test_invalid_requests(self):
        for question in [None,b'',b'\xff',b'{}',sentence('tip','tip'),sentence('tip')+'外部取得禁止。'.encode(),sentence('tip','')]:
            self.assertEqual(g.analyze(question)['status'],'HOLD')

    def test_limit_no_truncation(self):
        with patch.object(g,'LIMIT',1):
            result=g.analyze(sentence('tip')); self.assertEqual(result['reason'],'FAMILY_LIMIT_EXCEEDED_NO_TRUNCATION'); self.assertIsNone(result['family'])
            self.assertTrue(result['trace'])

    def test_candidate_omission(self):
        question = sentence('認証状況'); f=g.analyze(question)['family']; f['interpretations'].pop()
        self.assertEqual(g.check_family(question,b.canonical(f))['status'],'HOLD')

    def test_candidate_selection_or_extra_rejected(self):
        question=sentence('tip'); f=g.analyze(question)['family']; f['selected_interpretation']='one'
        self.assertEqual(g.check_family(question,b.canonical(f))['status'],'HOLD')

    def test_restricted_no_execute(self):
        with patch.object(p,'execute_and_admit') as run:
            raw, admission, result=g.execute_question(None,sentence('tip','取得禁止'),None,None,None,None)
            run.assert_not_called(); self.assertIsNone(raw); self.assertIsNone(admission); self.assertEqual(result['status'],'HOLD')

    def test_wrong_context_no_execute(self):
        question=sentence('tip'); candidate=b.canonical(g.analyze(question)['family'])
        with patch.object(p,'execute_and_admit') as run:
            raw, admission, result=g.execute_question(None,question,candidate,{}, {},None)
            run.assert_not_called(); self.assertEqual(result['status'],'HOLD')


class PublicationTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.root=Path(tmp.name)
        for d in ('base','gates','ledger'): (self.root/d).mkdir()
        for name in b.BASE: (self.root/'base'/name).write_text('synthetic fixture')
        f=self.root/'ledger/000000000000.json'; f.write_text('synthetic ledger'); tip=b.sha(f.read_bytes())
        payloads=[dict(status=s,seq=0,tip_sha256=tip,proof_authority=False,action_authority=False) for s in b.EXPECTED]
        payloads[0].update(rule_count=10,withdrawn_count=0,obstruction_count=2,research_certificate_count=2)
        payloads[1]['reviews']=dict(candidate=1,held=12,no_use=0)
        for name,payload in zip(b.GATES,payloads): (self.root/'gates'/name).write_text('import json\nprint(json.dumps('+repr(payload)+'))\n')
        h=b.inventory(self.root,0)
        self.request=dict(challenge='a'*64,seq=0,tip=tip,expected_hashes={k:v for k,v in h.items() if k.startswith('gates/') or k=='base/'+b.BASE[2]})
        self.key=bytes(range(32)); self.issue(sentence('tip','認証状況'))

    def issue(self, question):
        self.question=question; self.candidate=b.canonical(g.analyze(question)['family'])
        self.context=dict(turn_id='b'*64,question_sha256=b.sha(question),challenge=self.request['challenge'],request_sha256=b.sha(b.canonical(self.request)),audience=p.AUDIENCE)
        self.raw,self.admission,_=g.execute_question(self.root,question,self.candidate,self.request,self.context,self.key)
        self.prior=p.publish(self.raw,self.admission,self.request,self.context,self.key)

    def args(self, **kw):
        args=dict(question=self.question,candidate=self.candidate,raw=self.raw,admission=self.admission,request=self.request,context=self.context,key=self.key,prior_packet=self.prior); args.update(kw); return args

    def pub(self, **kw): return g.publish_question(**self.args(**kw))

    def test_partial_ambiguity_preserved(self):
        packet=self.pub(); result=p.strict(packet)['publication']; family=result['analysis']['family']
        self.assertEqual(result['status'],'AMBIGUOUS_PARTIAL'); self.assertEqual(len(result['branches']),4)
        self.assertIsNone(result['selected_interpretation']); self.assertTrue(result['ambiguity_unresolved'])
        self.assertEqual([x['claim_id'] for x in result['claims']],family['union_claim_ids'])
        self.assertIn('current_tip',{x['claim_id'] for x in result['claims'] if x['status']=='HOLD'})
        self.assertEqual(g.verified_display(packet,**self.args()),(packet,2))

    def test_all_observed_still_ambiguous(self):
        self.issue(sentence('記録状況')); packet=self.pub(); result=p.strict(packet)['publication']
        self.assertEqual(result['status'],'AMBIGUOUS_ALL_OBSERVED'); self.assertEqual(len(result['branches']),2)
        self.assertEqual(g.verified_display(packet,**self.args()),(packet,2))

    def test_single_complete(self):
        self.issue(sentence('整合性検査結果')); packet=self.pub()
        self.assertEqual(p.strict(packet)['publication']['status'],'ALL_OBSERVED')
        self.assertEqual(g.verified_display(packet,**self.args()),(packet,0))

    def test_common_is_intersection_not_union(self):
        result=p.strict(self.pub())['publication']; family=result['analysis']['family']
        self.assertNotIn('current_tip',family['common_claim_ids'])
        self.assertIn('current_tip',family['union_claim_ids'])
        for branch in result['branches']:
            self.assertEqual(set(branch['required_claim_ids'])-set(family['common_claim_ids']),set(branch['conditional_claim_ids']))

    def test_missing_evidence_preserves_every_branch(self):
        for field in ['raw','admission','prior_packet','context','request','key']:
            result=p.strict(self.pub(**{field:None})); self.assertEqual(result['status'],'HOLD')
            self.assertEqual(len(result['branches']),4); self.assertTrue(all(x['status']=='HOLD' for x in result['claims']))

    def test_omitted_branch_rejected(self):
        result=p.strict(self.pub()); result['publication']['branches'].pop()
        out,rc=g.verified_display(b.canonical(result),**self.args()); obj=p.strict(out)
        self.assertEqual((obj['status'],rc),('HOLD',2)); self.assertEqual(len(obj['branches']),4)

    def test_common_promotion_rejected(self):
        result=p.strict(self.pub()); result['publication']['analysis']['family']['common_claim_ids'].append('current_tip')
        out,rc=g.verified_display(b.canonical(result),**self.args()); self.assertEqual((p.strict(out)['status'],rc),('HOLD',2))

    def test_selected_branch_rejected(self):
        result=p.strict(self.pub()); result['publication']['selected_interpretation']=result['publication']['branches'][0]['interpretation_id']
        out,rc=g.verified_display(b.canonical(result),**self.args()); self.assertEqual((p.strict(out)['status'],rc),('HOLD',2))

    def test_boundary(self):
        result=p.strict(self.pub())['publication']; self.assertTrue(all(result[k] is False for k in g.BOUNDARY))


if __name__=='__main__': unittest.main()
