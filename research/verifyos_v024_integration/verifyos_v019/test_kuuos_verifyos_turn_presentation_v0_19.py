"""Real Ed25519 twice, bounded local final-renderer protocol; mocked v0.17."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, replace
from pathlib import Path
import copy
import unittest
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import kuuos_verifyos_display_gate_v0_18 as g
import kuuos_verifyos_turn_presentation_v0_19 as p
from test_kuuos_verifyos_closed_surface_v0_18_r2 import view


def ingress(n=1, question=b'question', request=b'{}'):
    return question, request, g.canonical({'turn_id':f'{n:064x}',
        'question_sha256':g.sha(question),'request_sha256':g.sha(request)})


class TurnPresentationTests(unittest.TestCase):
    def setUp(self):
        self.verify = Ed25519PrivateKey.generate()
        self.presentation = Ed25519PrivateKey.generate()
        self.signer = g.TrustedSigner(self.verify)
        self.host = p.PresentationHost(self.verify.public_key(), self.presentation)
        self.client = self.client_for(self.host)
        self.binding = self.begin()

    def client_for(self, host):
        return p.PresentationClient(host.session_id, host.client_id,
                                    self.presentation.public_key(),self.verify.public_key())

    def begin(self,n=1):
        args=ingress(n)
        self.client.select_turn(*args)
        b=self.host.begin(*args)
        self.assertTrue(self.client.activate(b))
        return b

    def envelope(self, binding=None, v=None, key=None):
        with patch.object(g,'_run_v017',return_value=(b'synthetic predecessor packet', v if v is not None else view())):
            return (self.signer if key is None else g.TrustedSigner(key)).issue(
                (binding or self.binding).challenge,snapshot=None,lean=Path('/not-real-lean'),
                question_bytes=b'question',pair_inputs={})

    def admit(self, binding=None, v=None):
        b=binding or self.binding
        return self.host.receive(b,self.envelope(b,v))

    def frame(self):
        req, raw=self.client.request()
        return req, self.host.present(raw)

    def show(self, expected=g.ALL):
        req, raw=self.frame()
        self.assertEqual(self.client.accept(req,raw).status,expected)
        self.assertEqual(self.client.current().status,expected)
        out=self.client.render()
        self.assertIn(('data-status="'+expected+'"').encode(),out)
        return out

    def resign(self, raw, mutate, key=None):
        obj=g.strict(raw); mutate(obj['payload'])
        obj['signature_hex']=(key or self.presentation).sign(p.DOMAIN+g.canonical(obj['payload'])).hex()
        return g.canonical(obj)

    def test_positive_dual_signature(self):
        self.assertEqual(self.admit().status,g.ALL)
        self.assertIn(b'<td>7</td>',self.show())

    def test_pending_host_hold(self):
        self.assertNotIn(b'<td>7</td>',self.show(g.HOLD))

    def test_untrusted_prose(self):
        req,_=self.frame(); self.assertEqual(self.client.accept(req,b'{"status":"SUCCESS"}').status,g.HOLD)

    def test_tampering_unsigned(self):
        self.admit(); req,raw=self.frame(); self.assertIn(b'"value":7',raw)
        self.assertEqual(self.client.accept(req,raw.replace(b'"value":7',b'"value":8')).status,g.HOLD)

    def test_wrong_presentation_key(self):
        self.admit(); req,raw=self.frame(); raw=self.resign(raw,lambda x:None,Ed25519PrivateKey.generate())
        self.assertEqual(self.client.accept(req,raw).status,g.HOLD)

    def test_presentation_signer_cannot_change_evidence_value(self):
        self.admit(); req,raw=self.frame(); bad=self.resign(raw,lambda x:x['view']['claims'][0].update(value=8))
        self.assertEqual(self.client.accept(req,bad).status,g.HOLD)

    def test_presentation_signer_cannot_omit_evidence(self):
        self.admit(); req,raw=self.frame(); bad=self.resign(raw,lambda x:x.update(evidence=None))
        self.assertEqual(self.client.accept(req,bad).status,g.HOLD)

    def test_forged_verifier_key(self):
        self.admit(); req,raw=self.frame(); other=g.strict(self.envelope(key=Ed25519PrivateKey.generate()))
        bad=self.resign(raw,lambda x:x.update(evidence=other))
        self.assertEqual(self.client.accept(req,bad).status,g.HOLD)

    def test_signed_model_metadata_not_rendered(self):
        v=view(); v['claims'][0]['reason']='<script>SUCCESS</script>'; v['branches'][0]['label']='FAKE'
        self.admit(v=v); out=self.show(); self.assertNotIn(b'<script>',out); self.assertNotIn(b'FAKE',out)

    def test_extra_signed_frame_prose_rejected(self):
        self.admit(); req,raw=self.frame(); bad=self.resign(raw,lambda x:x['view']['claims'][0].update(prose='SUCCESS'))
        self.assertEqual(self.client.accept(req,bad).status,g.HOLD)

    def test_partial_and_inactive_retained(self):
        v=view(); v['original_family_status']='AMBIGUOUS_PARTIAL'
        v['claims'].append(dict(claim_id='current_tip',status=g.HOLD,value=None))
        v['branches'].append(dict(interpretation_id='b'*64,active_in_revised_view=False,status='PARTIAL',required_claim_ids=['rule_count','current_tip'],conditional_claim_ids=['current_tip']))
        self.assertEqual(self.admit(v=v).status,g.LIMITED)
        out=self.show(g.LIMITED); self.assertIn(b'Inactive (retained)',out); self.assertIn(b'Current tip</th><td>HOLD',out)

    def test_late_old_frame_does_not_consume_new_request(self):
        self.admit(); old,raw=self.frame(); new=self.begin(2); self.admit(new); req,frame=self.frame()
        self.assertEqual(self.client.accept(old,raw).status,g.HOLD)
        self.assertEqual(self.client.accept(req,frame).status,g.ALL)

    def test_old_frame_mislabeled_as_new(self):
        self.admit(); _,raw=self.frame(); new=self.begin(2); self.admit(new); req,_=self.frame()
        self.assertEqual(self.client.accept(req,raw).status,g.HOLD)

    def test_local_turn_changes_before_host(self):
        self.admit(); old,raw=self.frame(); self.client.select_turn(*ingress(2))
        self.assertEqual(self.client.current().status,g.HOLD)
        self.assertEqual(self.client.accept(old,raw).status,g.HOLD)
        self.assertFalse(self.client.activate(self.binding))

    def test_late_activation_does_not_clear_current(self):
        old=self.binding; self.binding=self.begin(2); self.admit(); self.show()
        self.assertFalse(self.client.activate(old)); self.assertEqual(self.client.current().status,g.ALL)

    def test_epoch_reuse_refused(self):
        self.admit(); self.show(); self.assertFalse(self.client.activate(self.binding))
        self.assertEqual(self.client.current().status,g.ALL)

    def test_duplicate_turn_id_clears_client(self):
        self.admit(); self.show()
        with self.assertRaisesRegex(ValueError,'TURN_ID_REUSE'): self.client.select_turn(*ingress())
        self.assertEqual(self.client.current().status,g.HOLD)

    def test_duplicate_turn_id_invalidates_host(self):
        self.admit(); req,raw=self.client.request()
        with self.assertRaisesRegex(ValueError,'TURN_ID_REUSE'): self.host.begin(*ingress())
        self.assertIsNone(self.host.present(raw))

    def test_foreign_session_same_keys(self):
        other=p.PresentationHost(self.verify.public_key(),self.presentation)
        b=other.begin(*ingress())
        self.assertFalse(self.client.activate(b))
        self.admit(); req,raw=self.client.request(); self.assertIsNone(other.present(raw))

    def test_foreign_client_id(self):
        self.assertFalse(self.client.activate(replace(self.binding,client_id='f'*64,epoch=2)))

    def test_foreign_client_forged_frame_rejected(self):
        self.admit(); req,raw=self.frame()
        bad=self.resign(raw,lambda x:x['request']['binding'].update(client_id='f'*64))
        self.assertEqual(self.client.accept(req,bad).status,g.HOLD)

    def test_same_request_replay(self):
        self.admit(); req,raw=self.frame(); self.assertEqual(self.client.accept(req,raw).status,g.ALL)
        self.assertEqual(self.client.accept(req,raw).status,g.HOLD); self.assertEqual(self.client.current().status,g.ALL)

    def test_eight_parallel_accepts(self):
        self.admit(); req,raw=self.frame()
        with ThreadPoolExecutor(max_workers=8) as pool:
            results=list(pool.map(lambda _:self.client.accept(req,raw).status,range(8)))
        self.assertEqual(results.count(g.ALL),1); self.assertEqual(results.count(g.HOLD),7)

    def test_refresh_invalidates_prior_display(self):
        self.admit(); req,raw=self.frame(); self.assertEqual(self.client.accept(req,raw).status,g.ALL)
        req2,raw2=self.frame(); self.assertEqual(self.client.current().status,g.HOLD)
        self.assertEqual(self.client.accept(req,raw).status,g.HOLD)
        self.assertEqual(self.client.accept(req2,raw2).status,g.ALL)

    def test_refresh_failed_has_no_cached_pass(self):
        self.admit(); self.show(); req,_=self.frame()
        self.assertEqual(self.client.accept(req,None).status,g.HOLD)
        self.assertNotIn(b'<td>7</td>',self.client.render())

    def test_request_deadline_measured_from_send(self):
        self.admit(); req,raw=self.frame()
        with patch.object(p.time,'monotonic',return_value=p.time.monotonic()+p.MAX_TTL+1):
            self.assertEqual(self.client.accept(req,raw).status,g.HOLD)

    def test_expired_display_hold(self):
        self.admit(); self.show()
        with patch.object(p.time,'monotonic',return_value=p.time.monotonic()+p.MAX_TTL+1):
            self.assertEqual(self.client.current().status,g.HOLD); self.assertNotIn(b'<td>7</td>',self.client.render())

    def test_host_near_expiry_signed_hold(self):
        self.admit(); req,raw=self.client.request()
        with patch.object(p.time,'monotonic',return_value=p.time.monotonic()+1799):
            self.assertEqual(g.strict(self.host.present(raw))['payload']['status'],g.HOLD)

    def test_remote_host_turn_clears_on_next_refresh(self):
        self.admit(); self.show(); self.host.begin(*ingress(2))
        # Existing display is a bounded historical snapshot until local ingress/expiry;
        # no unsupported instantaneous revocation claim.
        self.assertEqual(self.client.current().status,g.ALL)
        req,wire=self.client.request(); self.assertIsNone(self.host.present(wire))
        self.assertEqual(self.client.accept(req,None).status,g.HOLD)

    def test_local_disconnect(self):
        self.admit(); req,raw=self.frame(); self.client.invalidate()
        self.assertEqual(self.client.accept(req,raw).status,g.HOLD); self.assertIsNone(self.client.request())

    def test_closed_client_terminal(self):
        self.admit(); self.show(); self.client.close()
        self.assertEqual(self.client.current().status,g.HOLD); self.assertFalse(self.client.activate(self.binding))
        with self.assertRaises(ValueError): self.client.select_turn(*ingress(2))

    def test_closed_host_terminal(self):
        self.admit(); req,wire=self.client.request(); self.host.close()
        self.assertIsNone(self.host.present(wire)); self.assertEqual(self.host.receive(self.binding,None).status,g.HOLD)

    def test_malformed_ingress_clears_client(self):
        self.admit(); self.show()
        with self.assertRaises(ValueError): self.client.select_turn(b'changed',*ingress(2)[1:])
        self.assertEqual(self.client.current().status,g.HOLD)

    def test_malformed_ingress_clears_host(self):
        self.admit(); req,raw=self.client.request()
        with self.assertRaises(ValueError): self.host.begin(b'changed',*ingress(2)[1:])
        self.assertIsNone(self.host.present(raw))

    def test_wrong_question_binding_rejected(self):
        fake=replace(self.binding,epoch=2,turn=replace(self.binding.turn,question_sha256='f'*64))
        self.assertFalse(self.client.activate(fake))

    def test_wire_roundtrip_and_strictness(self):
        req,raw=self.client.request(); self.assertEqual(p.wire_request(raw),req)
        self.assertIsNone(self.host.present(raw+b' ')); self.assertIsNone(self.host.present(b'{"binding":{},"nonce":"x","nonce":"y"}'))

    def test_separate_keys(self):
        with self.assertRaises(ValueError): p.PresentationHost(self.verify.public_key(),self.verify)
        with self.assertRaises(ValueError): p.PresentationClient(self.host.session_id,self.host.client_id,self.verify.public_key(),self.verify.public_key())

    def test_cross_turn_evidence_rewrapped_by_presentation_host(self):
        self.admit(); _,raw=self.frame(); old_evidence=g.strict(raw)['payload']['evidence']
        self.binding=self.begin(2); self.admit(); req,new=self.frame()
        bad=self.resign(new,lambda x:x.update(evidence=old_evidence))
        self.assertEqual(self.client.accept(req,bad).status,g.HOLD)

if __name__=='__main__': unittest.main()
