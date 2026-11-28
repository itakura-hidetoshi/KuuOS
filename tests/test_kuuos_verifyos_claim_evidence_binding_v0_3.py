"""Actual subprocess regressions with synthetic pinned gates, not Lean proofs."""
import copy
from pathlib import Path
import tempfile
import unittest
from runtime import kuuos_verifyos_claim_evidence_binding_v0_3 as g

b, p = g.b, g.p


class ClaimTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for d in ('base', 'gates', 'ledger'):
            (self.root / d).mkdir()
        for n in b.BASE:
            (self.root / 'base' / n).write_text('synthetic fixture')
        f = self.root / 'ledger/000000000000.json'
        f.write_text('synthetic ledger')
        self.tip = b.sha(f.read_bytes())
        self.key = bytes(range(32))
        self.plan = {'claim_ids': ['integrity_status', 'rule_count', 'scope_held_count']}
        self.issue()

    def issue(self, change=None):
        payloads = [dict(status=s, seq=0, tip_sha256=self.tip, proof_authority=False, action_authority=False) for s in b.EXPECTED]
        payloads[0].update(rule_count=10, withdrawn_count=0, obstruction_count=2, research_certificate_count=2)
        payloads[1]['reviews'] = dict(candidate=1, held=12, no_use=0)
        if change:
            change(payloads)
        for name, payload in zip(b.GATES, payloads):
            (self.root / 'gates' / name).write_text('import json\nprint(json.dumps(' + repr(payload) + '))\n')
        h = b.inventory(self.root, 0)
        self.request = dict(challenge='a'*64, seq=0, tip=self.tip, expected_hashes={k:v for k,v in h.items() if k.startswith('gates/') or k == 'base/' + b.BASE[2]})
        self.context = dict(turn_id='b'*64, question_sha256='c'*64, challenge=self.request['challenge'], request_sha256=b.sha(b.canonical(self.request)), audience=p.AUDIENCE)
        self.raw, self.admission = p.execute_and_admit(self.root, self.request, self.context, self.key)
        self.prior = p.publish(self.raw, self.admission, self.request, self.context, self.key)

    def args(self, **kw):
        args = dict(raw=self.raw, admission=self.admission, request=self.request, context=self.context, key=self.key, prior_packet=self.prior, plan=self.plan)
        args.update(kw)
        return args

    def publish(self, **kw):
        return g.publish_claims(**self.args(**kw))

    def rows(self, **kw):
        return p.strict(self.publish(**kw))['publication']['claims']

    def test_values_and_evidence(self):
        rows = self.rows()
        self.assertEqual([x['value'] for x in rows], ['PASS_INTEGRITY_ONLY', 10, 12])
        receipt = p.strict(self.raw)['receipt']
        for row in rows:
            ev = row['evidence']; rec = receipt['processes'][ev['process_index']]
            self.assertEqual(ev['stdout_sha256'], b.sha(rec['stdout'].encode()))
            self.assertEqual(ev['process_sha256'], b.sha(b.canonical(rec)))
            self.assertEqual(ev['bundle_sha256'], b.sha(self.raw))
            self.assertEqual(ev['receipt_sha256'], b.sha(b.canonical(receipt)))
        self.assertEqual(rows[2]['evidence']['field_path'], ['reviews', 'held'])

    def test_all_supported(self):
        packet = self.publish(plan={'claim_ids': list(g.FIELDS)})
        self.assertEqual(p.strict(packet)['publication']['status'], 'ALL_OBSERVED')

    def test_partial(self):
        plan = {'claim_ids': ['rule_count', 'lean_proof', 'current_tip']}
        rows = self.rows(plan=plan)
        self.assertEqual([r['status'] for r in rows], ['OBSERVED_IN_ADMITTED_RECEIPT', 'HOLD', 'HOLD'])
        self.assertEqual([r['evidence'] for r in rows[1:]], [None, None])
        self.assertEqual(p.strict(self.publish(plan=plan))['publication']['status'], 'PARTIAL')

    def test_unsupported_all(self):
        self.assertEqual(p.strict(self.publish(plan={'claim_ids': sorted(g.UNSUPPORTED)}))['publication']['status'], 'HOLD')

    def test_missing_field(self):
        self.issue(lambda x: x[0].pop('rule_count'))
        self.assertEqual(self.rows()[1]['reason'], 'FIELD_MISSING_OR_INVALID')
        self.assertIsNone(self.rows()[1]['value'])

    def test_bool_not_count(self):
        self.issue(lambda x: x[0].update(rule_count=True))
        self.assertEqual(self.rows()[1]['status'], 'HOLD')

    def test_negative_count(self):
        self.issue(lambda x: x[1]['reviews'].update(held=-1))
        self.assertEqual(self.rows()[2]['status'], 'HOLD')

    def test_unknown_id(self):
        self.assertEqual(self.publish(plan={'claim_ids': ['All theorems proven']}), g.hold())

    def test_duplicate(self):
        self.assertEqual(self.publish(plan={'claim_ids': ['rule_count', 'rule_count']}), g.hold())

    def test_empty(self):
        self.assertEqual(self.publish(plan={'claim_ids': []}), g.hold())

    def test_extra_plan_fields(self):
        self.assertEqual(self.publish(plan={'claim_ids': ['rule_count'], 'value': 999}), g.hold())

    def test_prior_packet_tamper(self):
        self.assertEqual(self.publish(prior_packet=self.prior + b'\n'), g.hold())

    def test_bundle_tamper(self):
        obj = p.strict(self.raw); obj['receipt']['before'] = {}
        self.assertEqual(self.publish(raw=b.canonical(obj)), g.hold())

    def test_missing_admission(self):
        self.assertEqual(self.publish(admission=b''), g.hold())

    def test_wrong_context(self):
        self.assertEqual(self.publish(context=dict(self.context, turn_id='d'*64)), g.hold())

    def test_display_verified(self):
        packet = self.publish()
        self.assertEqual(g.verified_display(packet, **self.args()), (packet, 0))
        self.assertTrue(all(p.strict(packet)['publication'][k] is False for k in b.BOUNDARY))

    def test_display_tamper(self):
        obj = p.strict(self.publish()); obj['publication']['claims'][1]['value'] = 99
        self.assertEqual(g.verified_display(b.canonical(obj), **self.args()), (g.hold(), 2))

    def test_display_omission(self):
        obj = p.strict(self.publish()); obj['publication']['claims'].pop()
        self.assertEqual(g.verified_display(b.canonical(obj), **self.args()), (g.hold(), 2))

    def test_display_plan_substitution(self):
        packet = self.publish(plan={'claim_ids': ['rule_count']})
        self.assertEqual(g.verified_display(packet, **self.args()), (g.hold(), 2))

    def test_display_partial_no_global_pass(self):
        args = self.args(plan={'claim_ids': ['rule_count', 'current_tip']})
        packet = g.publish_claims(**args)
        self.assertEqual(g.verified_display(packet, **args), (packet, 2))


if __name__ == '__main__':
    unittest.main()
