"""Subprocess fixtures and finite contract coverage, not open-language semantics."""
from itertools import combinations
from pathlib import Path
import tempfile
import unittest
from runtime import kuuos_verifyos_question_claim_contract_v0_4 as g

b, p = g.b, g.p


class QuestionTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for d in ('base', 'gates', 'ledger'):
            (self.root / d).mkdir()
        for n in b.BASE:
            (self.root / 'base' / n).write_text('synthetic fixture')
        f = self.root / 'ledger/000000000000.json'
        f.write_text('synthetic ledger')
        self.tip = b.sha(f.read_bytes())
        self.key = bytes(range(32))
        self.issue(self.typed('full_audit'))

    def typed(self, *topics):
        return b.canonical({'schema': g.QUESTION_SCHEMA, 'topics': list(topics)})

    def issue(self, question, change=None):
        self.question = question
        payloads = [dict(status=s, seq=0, tip_sha256=self.tip, proof_authority=False, action_authority=False) for s in b.EXPECTED]
        payloads[0].update(rule_count=10, withdrawn_count=0, obstruction_count=2, research_certificate_count=2)
        payloads[1]['reviews'] = dict(candidate=1, held=12, no_use=0)
        if change:
            change(payloads)
        for name, payload in zip(b.GATES, payloads):
            (self.root / 'gates' / name).write_text('import json\nprint(json.dumps(' + repr(payload) + '))\n')
        h = b.inventory(self.root, 0)
        self.request = dict(challenge='a'*64, seq=0, tip=self.tip, expected_hashes={k:v for k,v in h.items() if k.startswith('gates/') or k == 'base/' + b.BASE[2]})
        self.context = dict(turn_id='b'*64, question_sha256=b.sha(question), challenge=self.request['challenge'], request_sha256=b.sha(b.canonical(self.request)), audience=p.AUDIENCE)
        self.raw, self.admission = p.execute_and_admit(self.root, self.request, self.context, self.key)
        self.prior = p.publish(self.raw, self.admission, self.request, self.context, self.key)

    def args(self, **kw):
        args = dict(question=self.question, raw=self.raw, admission=self.admission, request=self.request,
                    context=self.context, key=self.key, prior_packet=self.prior)
        args.update(kw)
        return args

    def pub(self, **kw):
        return g.publish_question(**self.args(**kw))

    def test_all_63_nonempty_topic_subsets(self):
        names = list(g.TOPICS)
        count = 0
        for n in range(1, len(names)+1):
            for ts in combinations(names, n):
                c = g.compile_question(self.typed(*ts))
                expected = set(g.BASELINE).union(*(g.TOPICS[t] for t in ts))
                self.assertEqual(set(c['plan']['claim_ids']), expected)
                self.assertEqual(len(c['plan']['claim_ids']), len(expected))
                self.assertEqual(c['policy_sha256'], g.policy_digest())
                count += 1
        self.assertEqual(count, 63)

    def test_all_registered_texts(self):
        for q, topics in g.QUESTIONS.items():
            c = g.compile_question(q.encode())
            self.assertEqual(c['plan'], g.compile_question(self.typed(*topics))['plan'])

    def test_full_audit_retains_all_holds(self):
        obj = p.strict(self.pub())['publication']
        self.assertEqual(obj['status'], 'PARTIAL')
        self.assertEqual(len(obj['claims']), 18)
        self.assertEqual({r['claim_id'] for r in obj['claims'] if r['status']=='HOLD'}, set(g.claims.UNSUPPORTED))
        self.assertFalse(obj['open_language_completeness_verified'])

    def test_current_question_retains_freshness_hold(self):
        q = next(q for q, ts in g.QUESTIONS.items() if ts == ('current_state',)).encode()
        self.issue(q)
        obj = p.strict(self.pub())['publication']
        self.assertEqual(obj['status'], 'PARTIAL')
        self.assertEqual(obj['claims'][-1]['claim_id'], 'current_tip')
        self.assertEqual(obj['claims'][-1]['status'], 'HOLD')

    def test_rule_inventory_requires_withdrawals_and_obstructions(self):
        self.issue(self.typed('rule_inventory'))
        obj = p.strict(self.pub())['publication']
        self.assertEqual(obj['status'], 'ALL_OBSERVED')
        self.assertIn('withdrawn_count', obj['contract']['plan']['claim_ids'])
        self.assertIn('obstruction_count', obj['contract']['plan']['claim_ids'])

    def test_missing_required_value_is_hold(self):
        self.issue(self.typed('rule_inventory'), lambda ps: ps[0].pop('withdrawn_count'))
        obj = p.strict(self.pub())['publication']
        self.assertEqual(obj['status'], 'PARTIAL')
        self.assertEqual(next(r for r in obj['claims'] if r['claim_id']=='withdrawn_count')['status'], 'HOLD')

    def test_unknown_text_no_compile(self):
        self.issue('自由文の意味を推測せよ'.encode())
        self.assertEqual(p.strict(self.pub())['status'], 'HOLD')

    def test_text_suffix_not_ignored(self):
        q = next(iter(g.QUESTIONS)).encode()+b'\n'
        self.issue(q)
        self.assertEqual(p.strict(self.pub())['status'], 'HOLD')

    def test_unknown_topic(self):
        with self.assertRaises(ValueError): g.compile_question(self.typed('not_registered'))

    def test_duplicate_topic(self):
        with self.assertRaises(ValueError): g.compile_question(self.typed('scope_reviews','scope_reviews'))

    def test_empty_topics(self):
        with self.assertRaises(ValueError): g.compile_question(self.typed())

    def test_extra_claim_plan_rejected(self):
        with self.assertRaises(ValueError):
            g.compile_question(b.canonical({'schema':g.QUESTION_SCHEMA,'topics':['full_audit'],'claim_ids':['rule_count']}))

    def test_wrong_question_same_turn(self):
        self.assertEqual(p.strict(self.pub(question=self.typed('snapshot_integrity')))['status'], 'HOLD')

    def test_wrong_context(self):
        self.assertEqual(p.strict(self.pub(context=dict(self.context, question_sha256='f'*64)))['status'], 'HOLD')

    def test_missing_admission_preserves_required_rows(self):
        obj = p.strict(self.pub(admission=b''))
        self.assertEqual(obj['status'], 'HOLD')
        self.assertEqual([r['claim_id'] for r in obj['claims']], list(g.ORDER))
        self.assertTrue(all(r['status']=='HOLD' for r in obj['claims']))

    def test_display_partial(self):
        packet = self.pub()
        self.assertEqual(g.verified_display(packet, **self.args()), (packet, 2))

    def test_display_complete(self):
        self.issue(self.typed('snapshot_integrity'))
        packet = self.pub()
        self.assertEqual(g.verified_display(packet, **self.args()), (packet, 0))

    def test_display_omits_hold(self):
        obj = p.strict(self.pub()); obj['publication']['claims'].pop()
        out, rc = g.verified_display(b.canonical(obj), **self.args())
        self.assertEqual((p.strict(out)['status'], rc), ('HOLD',2))

    def test_display_substitute_smaller_contract(self):
        obj = p.strict(self.pub()); obj['publication']['contract'] = g.compile_question(self.typed('snapshot_integrity'))
        out, rc = g.verified_display(b.canonical(obj), **self.args())
        self.assertEqual((p.strict(out)['status'], rc), ('HOLD',2))

    def test_duplicate_json_key(self):
        with self.assertRaises(ValueError):
            g.compile_question(b'{"schema":"x","topics":[],"topics":[]}\n')

    def test_noncanonical_typed_bytes(self):
        with self.assertRaises(ValueError): g.compile_question(self.typed('scope_reviews')+b' ')

    def test_boundary_no_authority(self):
        obj = p.strict(self.pub())['publication']
        self.assertTrue(all(obj[k] is False for k in g.BOUNDARY))


if __name__ == '__main__':
    unittest.main()
