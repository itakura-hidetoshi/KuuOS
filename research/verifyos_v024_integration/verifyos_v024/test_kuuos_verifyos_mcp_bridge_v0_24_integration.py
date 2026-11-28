"""Unexecuted actual-Lean integration candidate, synthetic fixtures only.
Place v0.18--v0.24 modules in runtime/ of the exact v0.17 research tree and
this file in tests/. Requires actual pinned Lean, no skipped green result.
No mocks, no external ledger or production signing keys.
"""
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from runtime import kuuos_verifyos_lean_egress_v0_17 as predecessor
from runtime import kuuos_verifyos_mcp_bridge_v0_24 as m
import test_kuuos_verifyos_diverse_ledger_audit_v0_13 as fixture

g,p,r,e,d,x,h=m.g,m.p,m.r,m.e,m.d,m.x,m.h


class ActualMcpBridgeIntegration(unittest.TestCase):
    def setUp(self):
        source=Path(predecessor.__file__).read_bytes()
        self.assertEqual(hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest(),g.PREDECESSOR_BLOB)
        lean=os.environ.get('KUUOS_V024_LEAN_BINARY') or shutil.which('lean')
        if lean is None: raise RuntimeError('Actual pinned Lean required; no skipped success')
        self.lean=Path(lean).absolute().resolve(strict=True)
        self.assertTrue(self.lean.is_file())
        # Only a synthetic integration pin. Production needs an independent
        # trusted pin, never an observed binary's self-selected digest.
        self.lean_sha=g.sha(self.lean.read_bytes())
        self.fixture=fixture.PairTests('test_real_pair_and_diverse_match'); self.addCleanup(self.fixture.doCleanups)
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.dir=Path(tmp.name)
        self.verifier,self.presenter,self.event_key,self.receipt_key=(Ed25519PrivateKey.generate() for _ in range(4))
        self.ha,self.hw=(Ed25519PrivateKey.generate() for _ in range(2))
        def provision(ident):
            self.hs=x.AnchorService.provision(self.dir/'host-external.db',ident,self.ha,self.hw.public_key())
            self.hl=x.AnchorLink(ident,self.ha.public_key(),self.hw,self.hs.handle); return self.hl
        self.host=m.CanonicalExternalHost(self.dir/'host.db',self.dir/'host-anchor.db',self.verifier.public_key(),self.presenter,self.event_key,
            authority_key=self.ha.public_key(),writer_key=self.hw.public_key(),link_provider=provision)
        self.assertFalse(self.host._failed)
        ca,cw=(Ed25519PrivateKey.generate() for _ in range(2))
        ident=d.identity('client',self.host.session_id,self.host.client_id,self.event_key.public_key(),self.presenter.public_key(),self.verifier.public_key())
        digest=g.sha(g.canonical(ident));self.cs=x.AnchorService.provision(self.dir/'client-external.db',digest,ca,cw.public_key())
        self.cl=x.AnchorLink(digest,ca.public_key(),cw,self.cs.handle)
        self.client=self.open_client(create=True); self.assertTrue(self.client.reconnect())

    def open_client(self,create=False):
        return m.CanonicalExternalClient(self.dir/'client.db',self.dir/'client-anchor.db',self.host.session_id,self.host.client_id,
            self.event_key.public_key(),self.presenter.public_key(),self.verifier.public_key(),self.cl,create=create)

    def run_fixture(self,mode,missing_lean=False):
        root,args=self.fixture.pair(mode); req=args['request']; question=args['seed']['question']; b=predecessor.b
        inputs=(question,b.canonical(req),b.canonical(args['context']))
        self.assertEqual(inputs[1],m.upstream_canonical(req)); self.assertEqual(inputs[2],m.upstream_canonical(args['context']))
        self.assertIsNotNone(self.client.select_turn(*inputs))
        self.policy=m.HostPolicy(g.sha(b'synthetic target'),req['seq'],req['tip'],tuple(sorted(req['expected_hashes'].items())),self.lean_sha)
        self.bridge=m.McpBridge(self.host,self.policy,self.verifier,self.receipt_key)
        armed=self.bridge.arm(question,snapshot=Path(root).absolute(),lean=self.dir/'missing' if missing_lean else self.lean,pair_inputs=args)
        self.assertIsNotNone(armed);self.binding,event=armed;self.client.notify(event)
        self.tool_args={'challenge':self.binding.challenge.nonce}
        response=self.bridge.handle(self.tool_args)
        nonce=self.client.request_checkpoint();self.assertIsNotNone(nonce)
        if not self.client.accept_checkpoint(nonce,self.host.checkpoint(nonce)):
            return response,self.client.current(),inputs
        req,wire=self.client.request();shown=self.client.accept(req,self.host.present(wire))
        return response,shown,inputs

    def test_actual_lean_and_signed_synthetic_receipt(self):
        response,shown,inputs=self.run_fixture('correct')
        self.assertEqual(response['status'],'SYNTHETIC_EXECUTION_RECEIPT_ONLY',response)
        checked=m.inspect_receipt(response,self.receipt_key.public_key(),self.binding,self.policy)
        self.assertEqual(checked['status'],'SYNTHETIC_RECEIPT_SIGNATURE_MATCHED_ONLY'); self.assertEqual(checked['production_status'],'HOLD')
        self.assertEqual(shown.status,g.LIMITED)
        rows,branches=r.closed_view(shown);self.assertEqual(len(rows),18); self.assertEqual(sum(row.status==g.OBSERVED for row in rows),13)
        self.assertGreater(sum(branch.active for branch in branches),1)
        self.assertIn(b'SYNTHETIC ONLY - NOT PRODUCTION',self.client.render())
        self.assertEqual(self.bridge.handle(self.tool_args)['status'],'HOLD')
        self.client.notify(self.host.revoke());self.assertEqual(self.client.current().status,g.HOLD)
        restarted=self.open_client();self.assertTrue(restarted.reconnect());self.assertIsNone(restarted.select_turn(*inputs))

    def test_actual_common_mode_error_holds(self):
        response,shown,_=self.run_fixture('wrong_count');self.assertEqual((response['status'],shown.status),('HOLD',g.HOLD))

    def test_missing_lean_holds(self):
        response,shown,_=self.run_fixture('correct',missing_lean=True);self.assertEqual((response['status'],shown.status),('HOLD',g.HOLD))

if __name__=='__main__':unittest.main()
