"""Spawned final renderer, receives public keys and JSON bytes only.
Local trusted test channel; no production transport authentication asserted.
"""
import multiprocessing as mp
import os
from pathlib import Path
import unittest
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import kuuos_verifyos_display_gate_v0_18 as g
import kuuos_verifyos_turn_presentation_v0_19 as p
from test_kuuos_verifyos_turn_presentation_v0_19 import ingress
from test_kuuos_verifyos_closed_surface_v0_18_r2 import view


def renderer(pipe, sid, cid, presentation_pub, verifier_pub):
    client=p.PresentationClient(sid,cid,Ed25519PublicKey.from_public_bytes(presentation_pub),
                                Ed25519PublicKey.from_public_bytes(verifier_pub))
    pending={}
    try:
        pipe.send_bytes(g.canonical({'pid':os.getpid()}))
        while True:
            cmd=g.strict(pipe.recv_bytes())
            op=cmd['op']
            if op=='close': break
            if op=='turn':
                client.select_turn(*(bytes.fromhex(x) for x in cmd['ingress']))
                result={'status':client.current().status}
            elif op=='activate':
                b=p.wire_request(g.canonical({'binding':cmd['binding'],'nonce':'0'*64})).binding
                result={'activated':client.activate(b)}
            elif op=='request':
                req,raw=client.request(); pending[req.nonce]=req
                result={'wire':raw.hex(),'nonce':req.nonce}
            elif op=='accept':
                req=pending[cmd['nonce']]
                result={'accepted':client.accept(req,bytes.fromhex(cmd['frame'])).status,
                        'current':client.current().status,'render':client.render().hex()}
            else:
                raise ValueError('invalid test command')
            pipe.send_bytes(g.canonical(result))
    finally:
        client.close(); pipe.close()


class ProcessBoundaryTests(unittest.TestCase):
    def test_spawned_client_dual_signatures_and_late_delivery(self):
        verifier=Ed25519PrivateKey.generate(); presenter=Ed25519PrivateKey.generate()
        host=p.PresentationHost(verifier.public_key(),presenter)
        ctx=mp.get_context('spawn'); parent,child=ctx.Pipe()
        def raw(k): return k.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
        proc=ctx.Process(target=renderer,args=(child,host.session_id,host.client_id,raw(presenter),raw(verifier)))
        proc.start(); child.close()
        def read():
            self.assertTrue(parent.poll(10),'renderer process did not respond'); return g.strict(parent.recv_bytes())
        def call(op,**kwargs): parent.send_bytes(g.canonical({'op':op,**kwargs})); return read()
        def begin(n):
            args=ingress(n); self.assertEqual(call('turn',ingress=[x.hex() for x in args])['status'],g.HOLD)
            b=host.begin(*args)
            from dataclasses import asdict
            self.assertTrue(call('activate',binding=asdict(b))['activated'])
            with patch.object(g,'_run_v017',return_value=(b'synthetic predecessor',view())):
                env=g.TrustedSigner(verifier).issue(b.challenge,snapshot=None,lean=Path('/not-real-lean'),question_bytes=args[0],pair_inputs={})
            self.assertEqual(host.receive(b,env).status,g.ALL)
        def request():
            req=call('request'); return req['nonce'],host.present(bytes.fromhex(req['wire']))
        def accept(nonce,frame): return call('accept',nonce=nonce,frame=frame.hex())
        try:
            self.assertNotEqual(read()['pid'],os.getpid())
            begin(1); nonce,frame=request(); self.assertEqual(accept(nonce,frame)['accepted'],g.ALL)
            late,old=request(); begin(2); current,new=request()
            self.assertEqual(accept(late,old)['current'],g.HOLD)
            self.assertEqual(accept(current,new)['accepted'],g.ALL)
            forged_nonce,forged=request(); obj=g.strict(forged); obj['payload']['view']['claims'][0]['value']=999
            obj['signature_hex']=presenter.sign(p.DOMAIN+g.canonical(obj['payload'])).hex()
            blocked=accept(forged_nonce,g.canonical(obj))
            self.assertEqual(blocked['accepted'],g.HOLD); self.assertNotIn(b'999',bytes.fromhex(blocked['render']))
            parent.send_bytes(g.canonical({'op':'close'})); proc.join(10)
            self.assertEqual(proc.exitcode,0)
        finally:
            parent.close()
            if proc.is_alive(): proc.terminate(); proc.join(5)

if __name__=='__main__': unittest.main()
