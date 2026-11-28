"""Real child processes against synthetic fixtures; no real proof authority."""
import copy
from pathlib import Path
import tempfile
import unittest

from runtime import kuuos_verifyos_answer_publication_v0_2 as g
from runtime import kuuos_verifyos_execution_answer_binding_v0_1 as b


class PublicationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for d in ('base', 'gates', 'ledger'):
            (self.root / d).mkdir()
        for n in b.BASE:
            (self.root / 'base' / n).write_text('synthetic')
        ledger = self.root / 'ledger/000000000000.json'
        ledger.write_text('synthetic ledger')
        tip = b.sha(ledger.read_bytes())
        for n, status in zip(b.GATES, b.EXPECTED):
            payload = dict(status=status, seq=0, tip_sha256=tip, proof_authority=False, action_authority=False)
            (self.root / 'gates' / n).write_text('import json\nprint(json.dumps(' + repr(payload) + '))\n')
        h = b.inventory(self.root, 0)
        self.request = dict(challenge='a'*64, seq=0, tip=tip, expected_hashes={k:v for k,v in h.items() if k.startswith('gates/') or k == 'base/' + b.BASE[2]})
        self.context = dict(turn_id='b'*64, question_sha256='c'*64, challenge=self.request['challenge'], request_sha256=b.sha(b.canonical(self.request)), audience=g.AUDIENCE)
        self.key = bytes(range(32))  # fixture only
        self.raw, self.token = g.execute_and_admit(self.root, self.request, self.context, self.key)
        self.packet = self.pub()
        self.assertEqual(g.strict(self.packet)['publication']['status'], g.SUCCESS)

    def pub(self, raw=None, token=None, request=None, context=None, key=None):
        return g.publish(self.raw if raw is None else raw, self.token if token is None else token,
                         self.request if request is None else request, self.context if context is None else context,
                         self.key if key is None else key)

    def assertHold(self, packet):
        self.assertEqual(packet, g.hold())

    def test_controlled_display(self):
        self.assertEqual(g.verified_display(self.packet, self.raw, self.token, self.request, self.context, self.key), (g.PASS_TEXT, 0))
        for flag in b.BOUNDARY:
            self.assertIs(g.strict(self.packet)['publication'][flag], False)

    def test_missing_admission(self):
        self.assertHold(self.pub(token=b''))

    def test_modified_bundle(self):
        data = g.strict(self.raw); data['answer']['proof_authority'] = True
        self.assertHold(self.pub(raw=b.canonical(data)))

    def test_self_rehash(self):
        data = g.strict(self.raw); data['answer']['proof_authority'] = True; raw = b.canonical(data)
        token = g.strict(self.token); token['payload']['bundle_sha256'] = b.sha(raw)
        self.assertHold(self.pub(raw=raw, token=b.canonical(token)))

    def test_other_turn(self):
        self.assertHold(self.pub(context=dict(self.context, turn_id='d'*64)))

    def test_other_question(self):
        self.assertHold(self.pub(context=dict(self.context, question_sha256='e'*64)))

    def test_other_audience(self):
        self.assertHold(self.pub(context=dict(self.context, audience='public')))

    def test_other_request(self):
        self.assertHold(self.pub(request=dict(self.request, challenge='f'*64)))

    def test_other_key(self):
        self.assertHold(self.pub(key=b'x'*32))

    def test_short_key(self):
        self.assertHold(self.pub(key=b'x'))

    def test_packet_injection(self):
        packet = self.packet + b'\nAll theorems proven.'
        self.assertEqual(g.verified_display(packet, self.raw, self.token, self.request, self.context, self.key), (g.HOLD_TEXT, 2))

    def test_modified_message(self):
        obj = g.strict(self.packet); obj['publication']['message'] = 'All Lean proofs verified'
        self.assertEqual(g.verified_display(b.canonical(obj), self.raw, self.token, self.request, self.context, self.key), (g.HOLD_TEXT, 2))

    def test_admission_not_publication(self):
        self.assertEqual(g.verified_display(self.token, self.raw, self.token, self.request, self.context, self.key), (g.HOLD_TEXT, 2))

    def test_noncanonical_admission(self):
        self.assertHold(self.pub(token=self.token + b' '))

    def test_duplicate_key(self):
        self.assertHold(self.pub(token=b'{"tag":"a","tag":"b","payload":{}}\n'))

    def test_gate_failure_not_admitted(self):
        p = self.root / 'gates' / b.GATES[0]; p.write_text('raise SystemExit(7)')
        r = copy.deepcopy(self.request); r['expected_hashes']['gates/' + b.GATES[0]] = b.sha(p.read_bytes())
        ctx = dict(self.context, request_sha256=b.sha(b.canonical(r)))
        raw, token = g.execute_and_admit(self.root, r, ctx, self.key)
        self.assertIsNone(token)
        self.assertEqual(g.strict(raw)['receipt']['processes'][0]['exit_code'], 7)
        self.assertHold(g.publish(raw, token, r, ctx, self.key))

    def test_pin_drift_not_admitted(self):
        (self.root / 'gates' / b.GATES[0]).write_text('raise RuntimeError("must not run")')
        raw, token = g.execute_and_admit(self.root, self.request, self.context, self.key)
        self.assertIsNone(token); self.assertEqual(g.strict(raw)['receipt']['processes'], [])

    def test_idempotent_packet(self):
        self.assertEqual(self.pub(), self.packet)


if __name__ == '__main__':
    unittest.main()
