"""Local R2 tests; real Ed25519, mock v0.17 and real loopback WSGI HTTP."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import threading
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from wsgiref.simple_server import make_server, WSGIRequestHandler
import unittest
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import kuuos_verifyos_display_gate_v0_18 as g
import kuuos_verifyos_closed_surface_v0_18_r2 as r


def view(ident='rule_count', value=7, status=g.OBSERVED):
    return {'answer_status':'ACTIVE_VIEW_ALL_OBSERVED', 'original_family_status':'ALL_OBSERVED',
            'claims':[dict(claim_id=ident,status=status,value=value)],
            'branches':[dict(interpretation_id='a'*64, active_in_revised_view=True, status='ALL_OBSERVED', required_claim_ids=[ident], conditional_claim_ids=[])], 'selected_interpretation':None}


class QuietHandler(WSGIRequestHandler):
    def log_message(self,*args): pass


class ClosedSurfaceTests(unittest.TestCase):
    def setUp(self):
        self.key=Ed25519PrivateKey.generate()
        self.signer=g.TrustedSigner(self.key)
        self.surface=r.ClosedSurface(self.key.public_key())
        self.ch=self.surface.begin(b'q',b'{}',b'{}')

    def issue(self,v=None,ch=None):
        with patch.object(g,'_run_v017',return_value=(b'synthetic packet',v if v is not None else view())):
            return self.signer.issue(ch or self.ch,snapshot=None,lean=Path('/synthetic/lean'),question_bytes=b'q',pair_inputs={})

    def assert_display(self,status):
        out=self.surface.render()
        self.assertIn(('data-status="'+status+'"').encode(),out)
        return out

    def test_valid_typed_view(self):
        self.assertEqual(self.surface.receive(self.ch,self.issue()).status,g.ALL)
        self.assertIn(b'<td>7</td>',self.assert_display(g.ALL))

    def test_pending_is_hold(self): self.assert_display(g.HOLD)
    def test_unsigned_model_claim(self):
        self.assertEqual(self.surface.receive(self.ch,b'{"status":"SUCCESS"}').status,g.HOLD)
        self.assert_display(g.HOLD)

    def test_old_callback_does_not_consume_new(self):
        old=self.issue(); new=self.surface.begin(b'new',b'{}',b'{}')
        self.assertEqual(self.surface.receive(self.ch,old).reason,'STALE_CALLBACK')
        self.assertEqual(self.surface.receive(new,self.issue(ch=new)).status,g.ALL)
        self.assert_display(g.ALL)

    def test_new_turn_clears_verified_view(self):
        self.surface.receive(self.ch,self.issue()); self.surface.begin(b'new',b'{}',b'{}')
        self.assertNotIn(b'<td>7</td>',self.assert_display(g.HOLD))

    def test_replay_has_no_new_acceptance(self):
        e=self.issue(); self.assertEqual(self.surface.receive(self.ch,e).status,g.ALL)
        self.assertEqual(self.surface.receive(self.ch,e).status,g.HOLD)
        self.assert_display(g.ALL) # previously admitted same active snapshot, not a new pass

    def test_unknown_claim_rejected_even_signed(self):
        self.assertEqual(self.surface.receive(self.ch,self.issue(view('unknown',7))).status,g.HOLD)
        self.assert_display(g.HOLD)

    def test_unsupported_observed_rejected_even_signed(self):
        self.assertEqual(self.surface.receive(self.ch,self.issue(view('current_tip','a'*64))).status,g.HOLD)
        self.assert_display(g.HOLD)

    def test_boolean_not_nat(self):
        self.assertEqual(self.surface.receive(self.ch,self.issue(view(value=True))).status,g.HOLD)
        self.assert_display(g.HOLD)

    def test_nonzero_exit(self):
        self.assertEqual(self.surface.receive(self.ch,self.issue(view('integrity_exit_code',1))).status,g.HOLD)

    def test_malformed_digest(self):
        self.assertEqual(self.surface.receive(self.ch,self.issue(view('snapshot_tip','a'*63))).status,g.HOLD)

    def test_literal_injection(self):
        self.assertEqual(self.surface.receive(self.ch,self.issue(view('scope_status','<script>SUCCESS</script>'))).status,g.HOLD)
        self.assertNotIn(b'<script>',self.assert_display(g.HOLD))

    def test_extra_model_text_not_rendered(self):
        v=view(); v['claims'][0]['reason']='<script>SUCCESS</script>'; v['branches'][0]['label']='FORGED AUTHORITY'
        self.assertEqual(self.surface.receive(self.ch,self.issue(v)).status,g.ALL)
        out=self.assert_display(g.ALL); self.assertNotIn(b'<script>',out); self.assertNotIn(b'FORGED AUTHORITY',out)

    def test_partial_held_row_retained(self):
        v=view(); v['answer_status']='AMBIGUOUS_PARTIAL'; v['original_family_status']='AMBIGUOUS_PARTIAL'; v['branches'].append(dict(interpretation_id='b'*64,active_in_revised_view=True,status='PARTIAL',required_claim_ids=['rule_count','current_tip'],conditional_claim_ids=['current_tip']))
        v['claims'].append(dict(claim_id='current_tip',status=g.HOLD,value=None))
        self.assertEqual(self.surface.receive(self.ch,self.issue(v)).status,g.LIMITED)
        out=self.assert_display(g.LIMITED); self.assertIn(b'Current tip</th><td>HOLD',out); self.assertIn(b'Current tip (conditional)',out); self.assertIn(b'Retained interpretation branches',out)

    def test_branch_count_mismatch(self):
        v=view(); v['answer_status']='AMBIGUOUS_ALL_OBSERVED'
        self.assertEqual(self.surface.receive(self.ch,self.issue(v)).status,g.HOLD)
        self.assert_display(g.HOLD)

    def test_signed_false_branch_status_rejected(self):
        v=view(); v['branches'][0]['status']='PARTIAL'
        self.assertEqual(self.surface.receive(self.ch,self.issue(v)).status,g.HOLD)

    def test_signed_missing_branch_coverage_rejected(self):
        v=view(); v['claims'].append(dict(claim_id='snapshot_seq',status=g.OBSERVED,value=1))
        self.assertEqual(self.surface.receive(self.ch,self.issue(v)).status,g.HOLD)

    def test_signed_wrong_conditional_membership_rejected(self):
        v=view(); v['branches'][0]['conditional_claim_ids']=['rule_count']
        self.assertEqual(self.surface.receive(self.ch,self.issue(v)).status,g.HOLD)

    def test_signed_false_original_family_status_rejected(self):
        v=view(); v['original_family_status']='AMBIGUOUS_PARTIAL'
        self.assertEqual(self.surface.receive(self.ch,self.issue(v)).status,g.HOLD)

    def test_inactive_branch_held_row_not_promoted(self):
        v=view(); v['original_family_status']='AMBIGUOUS_PARTIAL'
        v['claims'].append(dict(claim_id='current_tip',status=g.HOLD,value=None))
        v['branches'].append(dict(interpretation_id='b'*64,active_in_revised_view=False,status='PARTIAL',required_claim_ids=['rule_count','current_tip'],conditional_claim_ids=['current_tip']))
        self.assertEqual(self.surface.receive(self.ch,self.issue(v)).status,g.LIMITED)
        self.assertIn(b'Inactive (retained)',self.assert_display(g.LIMITED))

    def test_concurrent_same_envelope(self):
        e=self.issue()
        with ThreadPoolExecutor(max_workers=8) as pool:
            results=list(pool.map(lambda _:self.surface.receive(self.ch,e).status,range(8)))
        self.assertEqual(results.count(g.ALL),1); self.assertEqual(results.count(g.HOLD),7)

    def test_expiry_no_cached_success(self):
        self.surface.receive(self.ch,self.issue())
        with patch.object(g.time,'monotonic',return_value=g.time.monotonic()+1801): self.assert_display(g.HOLD)

    def test_real_http_no_mutation_and_no_cache(self):
        server=make_server('127.0.0.1',0,self.surface,handler_class=QuietHandler)
        t=threading.Thread(target=server.serve_forever,daemon=True); t.start()
        try:
            base=f'http://127.0.0.1:{server.server_port}'
            with urlopen(base+'/verifyos',timeout=3) as res:
                self.assertEqual(res.status,200); self.assertEqual(res.headers['Cache-Control'],'no-store')
                self.assertIn("default-src 'none'",res.headers['Content-Security-Policy']); self.assertIn(b'data-status="HOLD"',res.read())
            for req,code in [(Request(base+'/verifyos',data=b'SUCCESS'),405),
                             (base+'/verifyos?status=SUCCESS',404),(base+'/sign',404)]:
                with self.assertRaises(HTTPError) as caught: urlopen(req,timeout=3)
                self.assertEqual(caught.exception.code,code); caught.exception.close()
            self.assert_display(g.HOLD)
            self.surface.receive(self.ch,self.issue())
            with urlopen(base+'/verifyos',timeout=3) as res: self.assertIn(b'<td>7</td>',res.read())
            self.surface.begin(b'new',b'{}',b'{}')
            with urlopen(base+'/verifyos',timeout=3) as res: self.assertIn(b'data-status="HOLD"',res.read())
        finally:
            server.shutdown(); t.join(timeout=3); server.server_close()

if __name__=='__main__': unittest.main()
