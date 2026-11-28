"""Local protocol tests ONLY. No actual Lean; _run_v017 is mocked explicitly."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import unittest
from unittest.mock import patch

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import kuuos_verifyos_display_gate_v0_18 as g

Q, R, C = b'synthetic question', b'{"tip":"synthetic"}', b'{"turn":"synthetic"}'


def view(status='ACTIVE_VIEW_ALL_OBSERVED', observed=True):
    rows = [{'claim_id': 'synthetic', 'status': g.OBSERVED, 'value': 7}]
    if not observed:
        rows.insert(0, {'claim_id': 'unknown', 'status': g.HOLD, 'value': None})
    return {'answer_status': status, 'original_family_status': 'ALL_OBSERVED' if observed else 'PARTIAL',
            'claims': rows, 'branches': [{'active_in_revised_view': True}], 'selected_interpretation': None}


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.key = Ed25519PrivateKey.generate()
        self.signer = g.TrustedSigner(self.key)
        self.renderer = g.TrustedRenderer(self.key.public_key())
        self.challenge = self.renderer.begin(Q, R, C)

    def issue(self, v=None, signer=None, challenge=None):
        with patch.object(g, '_run_v017', return_value=(b'synthetic packet', v or view())) as run:
            envelope = (signer or self.signer).issue(challenge or self.challenge, snapshot=None,
                            lean=Path('/synthetic/lean'), question_bytes=Q, pair_inputs={})
            run.assert_called_once()
        return envelope

    def assert_hold(self, envelope):
        decision = self.renderer.consume(envelope)
        self.assertEqual(decision.status, g.HOLD)
        self.assertIsNone(decision.view_json)

    def resign(self, envelope, change):
        obj = g.strict(envelope)
        change(obj['payload'])
        obj['signature_hex'] = self.key.sign(g.DOMAIN + g.canonical(obj['payload'])).hex()
        return g.canonical(obj)

    def test_valid_synthetic_envelope(self):
        decision = self.renderer.consume(self.issue())
        self.assertEqual(decision.status, g.ALL)
        self.assertEqual(g.strict(decision.view_json)['claims'][0]['value'], 7)

    def test_model_text_has_no_authority(self):
        self.assertEqual(self.renderer.untrusted_model_output('SUCCESS / 認証済み').status, g.HOLD)
        self.assert_hold(b'{"status":"MATCHED_ALL_OBSERVED_ONLY"}')

    def test_no_envelope(self): self.assert_hold(None)
    def test_unsigned_payload(self): self.assert_hold(g.canonical(g.strict(self.issue())['payload']))

    def test_value_tampering(self):
        obj = g.strict(self.issue()); obj['payload']['view']['claims'][0]['value'] = 8
        self.assert_hold(g.canonical(obj))

    def test_wrong_signing_key(self):
        self.assert_hold(self.issue(signer=g.TrustedSigner(Ed25519PrivateKey.generate())))

    def test_replay_after_consumption(self):
        envelope = self.issue()
        self.assertEqual(self.renderer.consume(envelope).status, g.ALL)
        self.assert_hold(envelope)

    def test_new_turn_rejects_old_envelope(self):
        envelope = self.issue(); self.renderer.begin(Q, R, C)
        self.assert_hold(envelope)

    def test_different_question(self):
        envelope = self.issue(); self.renderer.begin(b'other', R, C)
        self.assert_hold(envelope)

    def test_wrong_request_binding_even_if_signed(self):
        self.assert_hold(self.resign(self.issue(), lambda x: x['challenge'].update(request_sha256='a'*64)))

    def test_wrong_context_binding_even_if_signed(self):
        self.assert_hold(self.resign(self.issue(), lambda x: x['challenge'].update(context_sha256='b'*64)))

    def test_duplicate_json_key(self):
        envelope = self.issue(); self.assert_hold(envelope[:-1] + b',"signature_hex":"00"}')

    def test_noncanonical_json(self): self.assert_hold(b' ' + self.issue())

    def test_wrong_profile_even_if_signed(self):
        self.assert_hold(self.resign(self.issue(), lambda x: x.update(predecessor_head='c'*40)))

    def test_authority_promotion_even_if_signed(self):
        self.assert_hold(self.resign(self.issue(), lambda x: x['boundary'].update(proof_authority=True)))

    def test_partial_remains_limited(self):
        decision = self.renderer.consume(self.issue(view('AMBIGUOUS_PARTIAL', False)))
        self.assertEqual(decision.status, g.LIMITED)
        self.assertEqual(g.strict(decision.view_json)['claims'][0]['status'], g.HOLD)

    def test_ambiguity_never_all(self):
        self.assertEqual(self.renderer.consume(self.issue(view('AMBIGUOUS_ALL_OBSERVED'))).status, g.LIMITED)

    def test_partial_status_forgery_even_if_signed(self):
        envelope = self.issue(view('ACTIVE_VIEW_PARTIAL', False))
        self.assert_hold(self.resign(envelope, lambda x: x.update(status=g.ALL)))

    def test_retained_hold_tightens_active_view(self):
        self.assertEqual(self.renderer.consume(self.issue(view(observed=False))).status, g.LIMITED)

    def test_verifier_hold_has_no_envelope(self): self.assert_hold(self.issue(view(g.HOLD, False)))

    def test_verifier_exception(self):
        with patch.object(g, '_run_v017', side_effect=RuntimeError('synthetic failure')):
            self.assert_hold(self.signer.issue(self.challenge, snapshot=None, lean=Path('/absent'),
                                              question_bytes=Q, pair_inputs={}))

    def test_expiration(self):
        envelope = self.issue()
        with patch.object(g.time, 'monotonic', return_value=g.time.monotonic()+1801):
            self.assert_hold(envelope)

    def test_concurrent_consume_at_most_one(self):
        envelope = self.issue()
        with ThreadPoolExecutor(max_workers=8) as pool:
            statuses = list(pool.map(lambda _: self.renderer.consume(envelope).status, range(8)))
        self.assertEqual(statuses.count(g.ALL), 1)
        self.assertEqual(statuses.count(g.HOLD), 7)

    def test_invalid_attempt_consumes_challenge(self):
        envelope = self.issue(); self.assert_hold(b'bad'); self.assert_hold(envelope)

    def test_restart_old_receipt_not_reused(self):
        envelope = self.issue(); self.renderer = g.TrustedRenderer(self.key.public_key())
        self.assert_hold(envelope)

    def test_new_turn_during_verification(self):
        envelope = self.issue(); original = self.renderer._verify_envelope
        def switch(raw, challenge):
            self.new = self.renderer.begin(b'new question', R, C)
            return original(raw, challenge)
        with patch.object(self.renderer, '_verify_envelope', side_effect=switch):
            self.assert_hold(envelope)
        self.assertEqual(self.renderer.current(self.new).status, g.HOLD)
        self.assertEqual(self.renderer.current(self.challenge).reason, 'STALE_TURN')

    def test_display_state_cleared_on_new_turn(self):
        self.assertEqual(self.renderer.consume(self.issue()).status, g.ALL)
        self.assertEqual(self.renderer.current(self.challenge).status, g.ALL)
        new = self.renderer.begin(Q, R, C)
        self.assertEqual(self.renderer.current(new).status, g.HOLD)
        self.assertEqual(self.renderer.current(self.challenge).status, g.HOLD)

    def test_expiration_during_verification(self):
        envelope = self.issue(); now = g.time.monotonic()
        with patch.object(g.time, 'monotonic', side_effect=[now, now + 1801]):
            self.assert_hold(envelope)

    def test_all_claims_hold_cannot_get_limited_label(self):
        v = view('AMBIGUOUS_PARTIAL', False); v['claims'].pop()
        self.assert_hold(self.issue(v))

    def test_missing_real_predecessor_fails_closed(self):
        # Actual wrapper call in this standalone container, no mock and no Lean.
        self.assert_hold(self.signer.issue(self.challenge, snapshot=None, lean=Path('/absent'),
                                          question_bytes=Q, pair_inputs={}))


if __name__ == '__main__': unittest.main()
