"""Synthetic process fixtures, not real inherited proof/CI certificates."""
import copy
from pathlib import Path
import tempfile
import unittest

from runtime import kuuos_verifyos_execution_answer_binding_v0_1 as g


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for d in ('base', 'gates', 'ledger'):
            (self.root / d).mkdir()
        for name in g.BASE:
            (self.root / 'base' / name).write_text('fixture')
        ledger = self.root / 'ledger/000000000000.json'
        ledger.write_text('synthetic ledger')
        tip = g.sha(ledger.read_bytes())
        for name, status in zip(g.GATES, g.EXPECTED):
            payload = dict(status=status, seq=0, tip_sha256=tip, proof_authority=False, action_authority=False)
            (self.root / 'gates' / name).write_text('import json\nprint(json.dumps(' + repr(payload) + '))\n')
        h = g.inventory(self.root, 0)
        self.request = dict(challenge='a'*64, seq=0, tip=tip,
                            expected_hashes={k:v for k,v in h.items() if k.startswith('gates/') or k == 'base/' + g.BASE[2]})
        self.bundle = g.run(self.root, self.request)
        self.raw = g.canonical(self.bundle)
        self.trusted = g.sha(self.raw)
        self.assertEqual(self.bundle['answer']['status'], 'PASS_LOCAL_EXECUTION_STRUCTURE_ONLY')

    def hold(self, bundle, rehash=False, request=None):
        raw = g.canonical(bundle)
        self.assertEqual(g.verify(raw, request or self.request, g.sha(raw) if rehash else self.trusted)['status'], 'HOLD')

    def test_real_processes(self):
        self.assertEqual(g.verify(self.raw, self.request, self.trusted), self.bundle['answer'])
        self.assertEqual([r['exit_code'] for r in self.bundle['receipt']['processes']], [0, 0])
        self.assertFalse(self.bundle['answer']['external_truth_verified'])

    def test_answer_edit(self):
        b = copy.deepcopy(self.bundle); b['answer']['gate_results'] = ['ALL_LEAN_PROOFS_VERIFIED']; self.hold(b, True)

    def test_self_rehash_does_not_admit(self):
        b = copy.deepcopy(self.bundle); b['receipt']['obstruction'] = 'changed'; b['answer'] = g.render(b['receipt'], self.request); self.hold(b)

    def test_wrong_challenge(self):
        r = dict(self.request, challenge='b'*64); self.hold(self.bundle, request=r)

    def test_missing_process(self):
        b = copy.deepcopy(self.bundle); b['receipt']['processes'].pop(); b['answer'] = g.render(b['receipt'], self.request); self.hold(b, True)

    def test_nonzero(self):
        b = copy.deepcopy(self.bundle); b['receipt']['processes'][0]['exit_code'] = 1; b['answer'] = g.render(b['receipt'], self.request); self.hold(b, True)

    def test_bad_output(self):
        b = copy.deepcopy(self.bundle); b['receipt']['processes'][0]['stdout'] += 'extra'; b['answer'] = g.render(b['receipt'], self.request); self.hold(b, True)

    def test_command_mismatch(self):
        b = copy.deepcopy(self.bundle); b['receipt']['processes'][0]['argv'] = ['echo', 'PASS']; b['answer'] = g.render(b['receipt'], self.request); self.hold(b, True)

    def test_authority(self):
        b = copy.deepcopy(self.bundle); b['answer']['proof_authority'] = True; self.hold(b, True)

    def test_drift(self):
        b = copy.deepcopy(self.bundle); b['receipt']['after'] = {}; b['answer'] = g.render(b['receipt'], self.request); self.hold(b, True)

    def test_pin_before_execution(self):
        (self.root / 'gates' / g.GATES[0]).write_text('raise RuntimeError("must not run")')
        b = g.run(self.root, self.request); self.assertEqual(b['receipt']['processes'], []); self.hold(b, True)

    def test_real_nonzero(self):
        p = self.root / 'gates' / g.GATES[0]; p.write_text('raise SystemExit(7)')
        self.request['expected_hashes']['gates/' + g.GATES[0]] = g.sha(p.read_bytes())
        b = g.run(self.root, self.request); self.assertEqual(b['receipt']['processes'][0]['exit_code'], 7); self.hold(b, True)

    def test_missing_ledger(self):
        (self.root / 'ledger/000000000000.json').unlink(); b = g.run(self.root, self.request); self.hold(b, True)

    def test_duplicate_key(self):
        raw = b'{"receipt":{},"receipt":{},"answer":{}}'; self.assertEqual(g.verify(raw, self.request, g.sha(raw))['status'], 'HOLD')


if __name__ == '__main__':
    unittest.main()
