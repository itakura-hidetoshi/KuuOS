"""Synthetic pinned subprocesses and bounded translation regression."""
from itertools import combinations
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from runtime import kuuos_verifyos_question_translation_v0_5 as g

b, p, q = g.b, g.p, g.q


def sentence(*clauses, current=False, fresh=False, suffix='を教えて。'):
    prefix = '空OSの現行継承台帳について、' if current else '取得済み台帳について、'
    return (prefix + '、'.join(clauses) + suffix + (g.FRESH if fresh else '')).encode()


class TranslationTests(unittest.TestCase):
    def test_all_504_grammar_combinations(self):
        n = 0
        for size in range(1, len(g.CLAUSES)+1):
            for words in combinations(g.CLAUSES, size):
                for current in (False, True):
                    for fresh in (False, True):
                        for suffix in g.SUFFIXES:
                            original = sentence(*words, current=current, fresh=fresh, suffix=suffix)
                            result = g.analyze(original)
                            self.assertEqual(result['status'], 'TRANSLATION_CANDIDATE')
                            topics = {g.CLAUSES[w] for w in words}
                            if current or fresh: topics.add('current_state')
                            self.assertEqual(set(result['typed_question']['topics']), topics)
                            self.assertEqual(result['contract'], q.compile_question(b.canonical(result['typed_question'])))
                            pos = 0
                            for span in result['trace']:
                                self.assertEqual(span['start_byte'], pos)
                                pos = span['end_byte']
                                self.assertEqual(span['span_sha256'], b.sha(original[span['start_byte']:pos]))
                            self.assertEqual(pos, len(original))
                            self.assertEqual(g.check_translation(original,b.canonical(result['typed_question']))['status'],g.OK)
                            n += 1
        self.assertEqual(n, 504)

    def test_registered_questions(self):
        for text in q.QUESTIONS:
            r = g.analyze(text.encode())
            self.assertEqual(r['contract']['plan'], q.compile_question(text.encode())['plan'])

    def test_typed_preserved(self):
        original = b.canonical({'schema':q.QUESTION_SCHEMA,'topics':['current_state','rule_inventory']})
        self.assertEqual(g.analyze(original)['contract']['plan'], q.compile_question(original)['plan'])

    def test_unknown_clause_retained(self):
        original = sentence('整合性検査結果','未観測の依存も証明済みとする')
        r = g.analyze(original)
        self.assertEqual(r['status'],'HOLD'); self.assertIsNone(r['typed_question'])
        span = r['unresolved'][0]
        self.assertEqual(original[span['start_byte']:span['end_byte']].decode(),'未観測の依存も証明済みとする')

    def test_unknown_and_restricted_suffix(self):
        for extra in ['外部資料を取得しないで。','HOLDを除外して。','\n','ただしCIは起動する。']:
            original = sentence('整合性検査結果') + extra.encode()
            self.assertEqual(g.analyze(original)['status'],'HOLD')

    def test_negation_not_discarded(self):
        self.assertEqual(g.analyze(sentence('最新性は確認しない','整合性検査結果'))['status'],'HOLD')

    def test_duplicate_clause(self):
        self.assertEqual(g.analyze(sentence('整合性検査結果','整合性検査結果'))['status'],'HOLD')

    def test_unknown_prefix(self):
        self.assertEqual(g.analyze('一般的に整合性検査結果を教えて。'.encode())['status'],'HOLD')

    def test_empty_clause(self):
        self.assertEqual(g.analyze(sentence(''))['status'],'HOLD')

    def test_malformed(self):
        for raw in [None,b'',b'\xff',b'{}',b'{"topics":[],"topics":[]}\n',b'x'*8193]:
            self.assertEqual(g.analyze(raw)['status'],'HOLD')

    def test_drop_current(self):
        original = sentence('整合性検査結果',current=True)
        candidate = b.canonical({'schema':q.QUESTION_SCHEMA,'topics':['snapshot_integrity']})
        r = g.check_translation(original,candidate)
        self.assertEqual(r['status'],'HOLD'); self.assertIn('current_tip',r['contract']['plan']['claim_ids'])

    def test_drop_fresh_condition(self):
        original = sentence('整合性検査結果',fresh=True)
        candidate = b.canonical({'schema':q.QUESTION_SCHEMA,'topics':['snapshot_integrity']})
        self.assertEqual(g.check_translation(original,candidate)['status'],'HOLD')

    def test_extra_topic_rejected(self):
        original = sentence('整合性検査結果')
        candidate = b.canonical({'schema':q.QUESTION_SCHEMA,'topics':['snapshot_integrity','full_audit']})
        self.assertEqual(g.check_translation(original,candidate)['status'],'HOLD')

    def test_candidate_bytes_exact(self):
        original = sentence('整合性検査結果')
        typed = b.canonical(g.analyze(original)['typed_question'])
        self.assertEqual(g.check_translation(original,typed+b' ')['status'],'HOLD')
        self.assertEqual(g.check_translation(original,None)['status'],'HOLD')

    def test_invalid_questions_never_execute(self):
        with patch.object(p,'execute_and_admit') as execute:
            raw, admission, result = g.execute_question(None,sentence('整合性検査結果')+'取得禁止。'.encode(),None,None,None,None)
            execute.assert_not_called(); self.assertIsNone(raw); self.assertIsNone(admission)
            self.assertEqual(result['status'],'HOLD')

    def test_wrong_context_never_execute(self):
        original = sentence('整合性検査結果')
        candidate = b.canonical(g.analyze(original)['typed_question'])
        with patch.object(p,'execute_and_admit') as execute:
            raw, admission, result = g.execute_question(None,original,candidate,{}, {},None)
            execute.assert_not_called(); self.assertIsNone(admission); self.assertEqual(result['status'],'HOLD')


class PublicationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for d in ('base','gates','ledger'): (self.root/d).mkdir()
        for name in b.BASE: (self.root/'base'/name).write_text('synthetic fixture')
        f = self.root/'ledger/000000000000.json'; f.write_text('synthetic ledger'); tip = b.sha(f.read_bytes())
        payloads = [dict(status=s,seq=0,tip_sha256=tip,proof_authority=False,action_authority=False) for s in b.EXPECTED]
        payloads[0].update(rule_count=10,withdrawn_count=0,obstruction_count=2,research_certificate_count=2)
        payloads[1]['reviews']=dict(candidate=1,held=12,no_use=0)
        for name, payload in zip(b.GATES,payloads):
            (self.root/'gates'/name).write_text('import json\nprint(json.dumps('+repr(payload)+'))\n')
        h=b.inventory(self.root,0)
        self.request=dict(challenge='a'*64,seq=0,tip=tip,expected_hashes={k:v for k,v in h.items() if k.startswith('gates/') or k=='base/'+b.BASE[2]})
        self.key=bytes(range(32)); self.issue(sentence('全検査結果・認証範囲',current=True))

    def issue(self, original):
        self.original=original; self.candidate=b.canonical(g.analyze(original)['typed_question'])
        self.context=dict(turn_id='b'*64,question_sha256=b.sha(original),challenge=self.request['challenge'],request_sha256=b.sha(b.canonical(self.request)),audience=p.AUDIENCE)
        self.raw,self.admission,self.translation=g.execute_question(self.root,original,self.candidate,self.request,self.context,self.key)
        self.prior=p.publish(self.raw,self.admission,self.request,self.context,self.key)

    def args(self, **overrides):
        d=dict(question=self.original,candidate=self.candidate,raw=self.raw,admission=self.admission,request=self.request,context=self.context,key=self.key,prior_packet=self.prior)
        d.update(overrides); return d

    def test_partial_all_claims(self):
        packet=g.publish_question(**self.args()); result=p.strict(packet)['publication']
        self.assertEqual(result['status'],'PARTIAL'); self.assertEqual(len(result['claims']),18)
        self.assertEqual({r['claim_id'] for r in result['claims'] if r['status']=='HOLD'},set(g.c.UNSUPPORTED))
        self.assertEqual(g.verified_display(packet,**self.args()),(packet,2))
        self.assertTrue(all(result[k] is False for k in g.BOUNDARY))

    def test_complete_snapshot(self):
        self.issue(sentence('整合性検査結果'))
        packet=g.publish_question(**self.args()); self.assertEqual(g.verified_display(packet,**self.args()),(packet,0))

    def test_missing_evidence_retains_rows(self):
        for field in ['raw','admission','prior_packet','context','request','key']:
            result=p.strict(g.publish_question(**self.args(**{field:None})))
            self.assertEqual(result['status'],'HOLD'); self.assertEqual(len(result['claims']),18)
            self.assertTrue(all(r['status']=='HOLD' for r in result['claims']))

    def test_tampered_packet(self):
        obj=p.strict(g.publish_question(**self.args())); obj['publication']['claims'].pop()
        out,rc=g.verified_display(b.canonical(obj),**self.args()); result=p.strict(out)
        self.assertEqual((result['status'],rc),('HOLD',2)); self.assertEqual(len(result['claims']),18)

    def test_typed_bytes_cannot_replace_original(self):
        result=p.strict(g.publish_question(**self.args(question=self.candidate)))
        self.assertEqual(result['status'],'HOLD')

    def test_cli_missing_evidence_preserves_contract(self):
        question=self.root/'q.txt'; question.write_bytes(self.original)
        candidate=self.root/'candidate.json'; candidate.write_bytes(self.candidate)
        proc=subprocess.run([sys.executable,'-B','-m','runtime.kuuos_verifyos_question_translation_v0_5','publish','--question',str(question),'--candidate',str(candidate)],capture_output=True,check=False)
        self.assertEqual(proc.returncode,2); self.assertEqual(proc.stderr,b'')
        self.assertEqual(len(p.strict(proc.stdout)['claims']),18)


if __name__=='__main__': unittest.main()
