"""Host rollback/fencing and real bounded Unix socket transport; synthetic only."""
from pathlib import Path
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
import json, shutil, socket, struct, tempfile, threading, time, unittest
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
import kuuos_verifyos_host_anchor_v0_23 as h
from test_kuuos_verifyos_turn_presentation_v0_19 import ingress
from test_kuuos_verifyos_closed_surface_v0_18_r2 import view
x,d,e,g=h.x,h.d,h.e,h.g

def service_process(path,db,ident,secret,writer,stop,ready):
    service=x.AnchorService(db,ident,Ed25519PrivateKey.from_private_bytes(secret),Ed25519PublicKey.from_public_bytes(writer))
    h.serve_local(path,service,stop,ready)

class HostTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.root=Path(tmp.name)
        self.v,self.p,self.k,self.a,self.w=(Ed25519PrivateKey.generate() for _ in range(5))
        self.host=self.make_host(self.provider)
        self.assertFalse(self.host._failed)
    def make_host(self,provider):
        return h.ExternalHost(self.root/'host.db',self.root/'host-anchor.db',self.v.public_key(),self.p,self.k,
                              authority_key=self.a.public_key(),writer_key=self.w.public_key(),link_provider=provider)
    def provider(self,ident):
        self.service=x.AnchorService.provision(self.root/'external.db',ident,self.a,self.w.public_key())
        self.link=x.AnchorLink(ident,self.a.public_key(),self.w,self.service.handle)
        return self.link
    def begin(self):
        result=self.host.begin(*ingress()); self.assertIsNotNone(result); return result
    def retire(self):
        return h.retire_external_host(self.root/'host.db',self.root/'host-anchor.db',self.host.session_id,self.host.client_id,self.k.public_key(),self.p.public_key(),self.v.public_key(),self.link,authority_key=self.a.public_key(),writer_key=self.w.public_key())
    def backup(self,files):
        for f in files: shutil.copyfile(self.root/f,self.root/(f+'.bak'))
    def restore(self,files):
        for f in files: shutil.copyfile(self.root/(f+'.bak'),self.root/f)
    def test_genesis_and_monotonic_host(self):
        old=self.link.read(); self.assertEqual(old[0],1); self.begin(); self.assertEqual(self.link.read()[0],2); self.host.revoke(); self.assertEqual(self.link.read()[0],3); self.assertEqual(self.link.read(),self.host._tip)
    def test_host_rollback_dual_local(self):
        files=['host.db','host-anchor.db']; self.backup(files); self.begin(); self.host.revoke(); self.restore(files)
        self.assertIsNone(self.host.checkpoint('a'*64)); self.assertEqual(self.retire()['status'],'HOLD')
    def test_host_external_rollback(self):
        self.backup(['external.db']); self.begin(); self.restore(['external.db']); self.assertIsNone(self.host.checkpoint('a'*64)); self.assertEqual(self.retire()['status'],'HOLD')
    def test_host_retirement_fences_live_instance(self):
        self.begin(); old=self.link.read(); result=self.retire(); self.assertEqual(result['status'],'RETIRED_ONLY'); self.assertEqual(self.link.read()[0],old[0]+1)
        self.assertIsNone(self.host.checkpoint('a'*64)); self.assertEqual(self.retire()['tip'],result['tip'])
    def test_host_retirement_requires_remote(self):
        self.link.transport=lambda _: (_ for _ in ()).throw(TimeoutError('down')); self.assertEqual(self.retire()['status'],'HOLD')
    def test_event_withheld_if_remote_cas_fails(self):
        original=self.service.handle
        def lose(wire):
            if g.strict(wire)['payload']['op']=='CAS': raise TimeoutError('lost')
            return original(wire)
        self.link.transport=lose; self.assertIsNone(self.host.begin(*ingress())); self.assertTrue(self.host._failed)
        self.link.transport=original; self.assertEqual(self.retire()['status'],'HOLD')
    def test_event_withheld_if_remote_committed_but_reply_lost(self):
        original=self.service.handle
        def lose(wire):
            result=original(wire)
            if g.strict(wire)['payload']['op']=='CAS': raise TimeoutError('lost')
            return result
        self.link.transport=lose; self.assertIsNone(self.host.begin(*ingress())); self.assertTrue(self.host._failed)
        self.link.transport=original; self.assertEqual(self.retire()['status'],'RETIRED_ONLY')
        self.assertIsNone(self.host.checkpoint('a'*64))
    def test_no_reprovision(self):
        original=self.link.read(); bad=self.make_host(lambda _:self.link); self.assertTrue(bad._failed); self.assertEqual(original,self.link.read())
    def test_host_close_is_persisted(self):
        self.begin(); self.assertIsNotNone(self.host.close()); self.assertIsNone(self.host.begin(*ingress())); self.assertEqual(self.retire()['last_kind'],'CLOSED')
    def test_host_and_client_independently_anchored(self):
        a2,w2=(Ed25519PrivateKey.generate() for _ in range(2)); ident=g.sha(g.canonical(d.identity('client',self.host.session_id,self.host.client_id,self.k.public_key(),self.p.public_key(),self.v.public_key())))
        service=x.AnchorService.provision(self.root/'client-external.db',ident,a2,w2.public_key()); link=x.AnchorLink(ident,a2.public_key(),w2,service.handle)
        c=x.ExternalClient(self.root/'client.db',self.root/'client-anchor.db',self.host.session_id,self.host.client_id,self.k.public_key(),self.p.public_key(),self.v.public_key(),link,create=True)
        self.assertTrue(c.reconnect()); self.assertIsNotNone(c.select_turn(*ingress())); binding,event=self.begin(); c.notify(event)
        signer=g.TrustedSigner(self.v)
        with patch.object(g,'_run_v017',return_value=(b'synthetic packet',view())):
            env=signer.issue(binding.challenge,snapshot=None,lean=Path('/synthetic'),question_bytes=b'question',pair_inputs={})
        self.assertEqual(self.host.receive(binding,env).status,g.ALL)
        n=c.request_checkpoint(); self.assertTrue(c.accept_checkpoint(n,self.host.checkpoint(n))); req,wire=c.request(); self.assertEqual(c.accept(req,self.host.present(wire)).status,g.ALL)
        c.notify(self.host.revoke()); self.assertEqual(c.current().status,g.HOLD); self.assertEqual(self.link.read(),self.host._tip); self.assertEqual(link.read(),c._tip)
    def test_actual_mcp_pilot_response_is_not_production_envelope(self):
        binding,_=self.begin(); raw=Path(__file__).with_name('mcp_pilot_observation.json').read_bytes().rstrip(b'\n')
        # A recorded response from the actual synthetic-only MCP call, not a
        # production signed egress packet. No external call during the tests.
        parsed=json.loads(raw)
        self.assertEqual(parsed['classification'],'SYNTHETIC_ONLY')
        self.assertEqual(self.host.receive(binding,raw).status,g.HOLD)
        # Even canonical JSON cannot substitute for the required signed envelope.
        self.assertEqual(self.host.receive(binding,g.canonical(parsed)).status,g.HOLD)
    def test_host_via_real_socket_service(self):
        root=self.root/'host-socket'; root.mkdir(mode=0o700)
        ctx=mp.get_context('spawn'); stop,ready=ctx.Event(),ctx.Event()
        def provider(ident):
            db=root/'external.db'; path=root/'anchor.sock'
            x.AnchorService.provision(db,ident,self.a,self.w.public_key())
            secret=self.a.private_bytes(Encoding.Raw,PrivateFormat.Raw,NoEncryption())
            proc=ctx.Process(target=service_process,args=(path,db,ident,secret,e.key_bytes(self.w.public_key()),stop,ready)); proc.start()
            def cleanup():
                stop.set(); proc.join(4)
                if proc.is_alive(): proc.terminate(); proc.join()
            self.addCleanup(cleanup); self.assertTrue(ready.wait(5)); self.socket_proc=proc
            self.socket_link=x.AnchorLink(ident,self.a.public_key(),self.w,h.UnixTransport(path),deadline=2)
            return self.socket_link
        host=h.ExternalHost(root/'host.db',root/'host-anchor.db',self.v.public_key(),self.p,self.k,authority_key=self.a.public_key(),writer_key=self.w.public_key(),link_provider=provider)
        self.assertFalse(host._failed); self.assertIsNotNone(host.begin(*ingress())); self.assertEqual(self.socket_link.read()[0],2)
        self.assertIsNotNone(host.revoke()); self.assertEqual(self.socket_link.read()[0],3)
        stop.set(); self.socket_proc.join(4); self.assertEqual(self.socket_proc.exitcode,0)
        self.assertIsNone(host.checkpoint('a'*64)); self.assertTrue(host._failed)
    def test_wrong_pin_prevents_host_creation(self):
        root=self.root/'other'; root.mkdir()
        def wrong(ident):
            k=Ed25519PrivateKey.generate(); s=x.AnchorService.provision(root/'ext.db',ident,k,self.w.public_key()); return x.AnchorLink(ident,k.public_key(),self.w,s.handle)
        bad=h.ExternalHost(root/'h.db',root/'a.db',self.v.public_key(),self.p,self.k,authority_key=self.a.public_key(),writer_key=self.w.public_key(),link_provider=wrong)
        self.assertTrue(bad._failed); self.assertFalse((root/'h.db').exists()); self.assertIsNone(bad.checkpoint('b'*64))

class IpcTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.root=Path(tmp.name)
        self.path=self.root/'anchor.sock'; self.db=self.root/'external.db'; self.ident='d'*64
        self.a,self.w=(Ed25519PrivateKey.generate() for _ in range(2)); self.service=x.AnchorService.provision(self.db,self.ident,self.a,self.w.public_key())
        self.transport=h.UnixTransport(self.path,timeout=.8); self.link=x.AnchorLink(self.ident,self.a.public_key(),self.w,self.transport,deadline=1)
    def launch(self):
        ctx=mp.get_context('spawn'); stop,ready=ctx.Event(),ctx.Event()
        secret=self.a.private_bytes(Encoding.Raw,PrivateFormat.Raw,NoEncryption())
        proc=ctx.Process(target=service_process,args=(self.path,self.db,self.ident,secret,e.key_bytes(self.w.public_key()),stop,ready)); proc.start()
        def cleanup():
            stop.set(); proc.join(4)
            if proc.is_alive(): proc.terminate(); proc.join()
        self.addCleanup(cleanup); self.assertTrue(ready.wait(5)); return proc,stop
    def test_real_process_authenticated_read_and_cas(self):
        proc,stop=self.launch(); self.assertEqual(self.path.stat().st_mode&0o777,0o600)
        self.assertEqual(self.link.read(),x.GENESIS); new=(1,'f'*64); self.assertEqual(self.link.cas(x.GENESIS,new),new); self.assertEqual(self.link.read(),new)
        stop.set(); proc.join(4); self.assertEqual(proc.exitcode,0)
    def test_unauthorized_writer_on_real_socket(self):
        self.launch(); bad=x.AnchorLink(self.ident,self.a.public_key(),Ed25519PrivateKey.generate(),self.transport)
        with self.assertRaisesRegex(ValueError,'ANCHOR_TRANSPORT_UNAVAILABLE'): bad.cas(x.GENESIS,(1,'a'*64))
        self.assertEqual(self.link.read(),x.GENESIS)
    def test_oversize_frame_does_not_change_store(self):
        self.launch()
        with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
            s.settimeout(2); s.connect(str(self.path)); s.sendall(struct.pack('!I',h.MAX_WIRE+1)); self.assertEqual(s.recv(1),b'')
        self.assertEqual(self.link.read(),x.GENESIS)
    def test_socket_missing_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'ANCHOR_TRANSPORT_UNAVAILABLE'): self.link.read()
    def test_hard_timeout_without_response(self):
        with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as listener:
            listener.bind(str(self.path)); listener.listen(1)
            transport=h.UnixTransport(self.path,timeout=.06); start=time.monotonic()
            with self.assertRaises(TimeoutError): transport(b'fixture')
            self.assertLess(time.monotonic()-start,.6)
    def test_partial_frame_not_accepted(self):
        self.launch()
        with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
            s.connect(str(self.path)); s.sendall(struct.pack('!I',5)+b'x'); s.shutdown(socket.SHUT_WR); s.settimeout(2); self.assertEqual(s.recv(1),b'')
        self.assertEqual(self.link.read(),x.GENESIS)
    def test_ipc_competing_cas(self):
        self.launch()
        def attempt(i):
            try: return self.link.cas(x.GENESIS,(1,g.sha(str(i).encode())))
            except ValueError: return None
        with ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(attempt,range(8)))
        self.assertEqual(sum(r is not None for r in results),1)

if __name__=='__main__': unittest.main()
