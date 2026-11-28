"""Actual Ed25519, SQLite, spawned service process; synthetic v0.17 input."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path
import multiprocessing as mp
import shutil, sqlite3, tempfile, time, unittest, os
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
import kuuos_verifyos_external_anchor_v0_22 as x
from test_kuuos_verifyos_turn_presentation_v0_19 import ingress
from test_kuuos_verifyos_closed_surface_v0_18_r2 import view

d,e,g=x.d,x.e,x.g

def worker(path,ident,secret,writer,conn):
    service=x.AnchorService(path,ident,Ed25519PrivateKey.from_private_bytes(secret),Ed25519PublicKey.from_public_bytes(writer))
    try:
        while True:
            wire=conn.recv_bytes()
            if wire==b'quit': break
            try: conn.send_bytes(service.handle(wire))
            except Exception: conn.send_bytes(b'')
    finally: conn.close()

def crash_before_remote_cas(root,ident,session,client,event,presentation,verifier,authority,writer_secret,service_secret):
    # Fault injector in an actual spawned process: local journal and local anchor
    # already committed when the remote CAS request is about to leave.
    keys=[Ed25519PublicKey.from_public_bytes(raw) for raw in (event,presentation,verifier,authority)]
    writer=Ed25519PrivateKey.from_private_bytes(writer_secret)
    service=x.AnchorService(root/'external.db',ident,Ed25519PrivateKey.from_private_bytes(service_secret),writer.public_key())
    def transport(wire):
        if g.strict(wire)['payload']['op']=='CAS': os._exit(73)
        return service.handle(wire)
    link=x.AnchorLink(ident,keys[3],writer,transport)
    x.ExternalClient(root/'client.db',root/'client-anchor.db',session,client,*keys[:3],link)
    os._exit(74)

class ExternalTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.root=Path(tmp.name)
        self.v,self.p,self.k,self.a,self.w=(Ed25519PrivateKey.generate() for _ in range(5))
        self.host=d.DurableHost(self.root/'host.db',self.root/'host-anchor.db',self.v.public_key(),self.p,self.k)
        self.binding,self.event=self.host.begin(*ingress()); self.signer=g.TrustedSigner(self.v)
        ident=d.identity('client',self.host.session_id,self.host.client_id,self.k.public_key(),self.p.public_key(),self.v.public_key())
        self.ident=g.sha(g.canonical(ident)); self.db=self.root/'external.db'
        self.service=x.AnchorService.provision(self.db,self.ident,self.a,self.w.public_key())
        self.link=x.AnchorLink(self.ident,self.a.public_key(),self.w,self.service.handle)
        self.client=self.open(create=True); self.assertTrue(self.client.reconnect()); self.assertIsNotNone(self.client.select_turn(*ingress()))
    def open(self,create=False,link=None):
        return x.ExternalClient(self.root/'client.db',self.root/'client-anchor.db',self.host.session_id,self.host.client_id,self.k.public_key(),self.p.public_key(),self.v.public_key(),link or self.link,create=create)
    def show(self):
        with patch.object(g,'_run_v017',return_value=(b'synthetic packet',view())):
            env=self.signer.issue(self.binding.challenge,snapshot=None,lean=Path('/synthetic'),question_bytes=b'question',pair_inputs={})
        self.assertEqual(self.host.receive(self.binding,env).status,g.ALL)
        n=self.client.request_checkpoint(); self.assertTrue(self.client.accept_checkpoint(n,self.host.checkpoint(n)))
        req,wire=self.client.request(); self.assertEqual(self.client.accept(req,self.host.present(wire)).status,g.ALL)
        self.assertIn(b'<td>7</td>',self.client.render())
    def held(self,c=None):
        c=c or self.client; self.assertEqual(c.current().status,g.HOLD); self.assertIn(b'data-status="HOLD"',c.render())
    def backup(self,files):
        for f in files: shutil.copyfile(self.root/f,self.root/(f+'.bak'))
    def restore(self,files):
        for f in files: shutil.copyfile(self.root/(f+'.bak'),self.root/f)
    def test_positive(self): self.show(); self.assertEqual(self.link.read(),self.client._tip)
    def test_restart_fences_old(self):
        self.show(); fresh=self.open(); self.held(fresh); self.held(); self.assertTrue(fresh.reconnect()); self.assertIsNone(fresh.select_turn(*ingress()))
    def test_dual_local_rollback(self):
        files=['client.db','client-anchor.db']; self.backup(files); self.show(); self.client.notify(self.host.revoke()); self.restore(files)
        self.held(); self.assertFalse(self.open().reconnect())
    def test_all_three_rollback_limitation(self):
        files=['client.db','client-anchor.db','external.db']; self.backup(files); self.show(); self.client.notify(self.host.revoke()); self.restore(files)
        # Negative control: a rollback of every trusted store is undetectable.
        fresh=self.open(); self.assertTrue(fresh.reconnect()); self.held(fresh); self.assertEqual(fresh._inner._seq,-1)
    def test_external_only_rollback(self):
        self.backup(['external.db']); self.show(); self.restore(['external.db']); self.held(); self.assertFalse(self.open().reconnect())
    def test_freshly_signed_wrong_tip(self):
        self.show()
        def wrong(w):
            obj=g.strict(self.service.handle(w))['payload']; obj['tip']=list(x.GENESIS)
            return x.seal(self.a,x.RESPONSE,obj)
        self.link.transport=wrong; self.held()
    def test_actual_crash_before_remote_cas(self):
        self.show(); ctx=mp.get_context('spawn')
        def raw(k): return k.private_bytes(Encoding.Raw,PrivateFormat.Raw,NoEncryption())
        proc=ctx.Process(target=crash_before_remote_cas,args=(self.root,self.ident,self.host.session_id,self.host.client_id,*[e.key_bytes(k.public_key()) for k in (self.k,self.p,self.v,self.a)],raw(self.w),raw(self.a)))
        proc.start(); proc.join(8)
        try:
            self.assertEqual(proc.exitcode,73); self.held(); self.assertFalse(self.open().reconnect())
        finally:
            if proc.is_alive(): proc.terminate(); proc.join()
    def test_missing_external_no_recreate(self):
        self.show(); self.db.unlink(); self.held(); self.assertFalse(self.open().reconnect()); self.assertFalse(self.db.exists())
    def test_unavailable_service(self):
        self.show(); self.link.transport=lambda _: (_ for _ in ()).throw(ConnectionError('down')); self.held()
    def test_wrong_authority_key(self):
        bad=x.AnchorLink(self.ident,Ed25519PrivateKey.generate().public_key(),self.w,self.service.handle); self.assertFalse(self.open(link=bad).reconnect())
    def test_wrong_writer_key(self):
        bad=x.AnchorLink(self.ident,self.a.public_key(),Ed25519PrivateKey.generate(),self.service.handle); self.assertFalse(self.open(link=bad).reconnect())
    def test_wrong_identity(self):
        bad=x.AnchorLink('f'*64,self.a.public_key(),self.w,self.service.handle); self.assertFalse(self.open(link=bad).reconnect())
    def test_replayed_response(self):
        reply=self.link.transport; captured=[]
        def capture(w):
            r=reply(w); captured.append(r); return r
        self.link.transport=capture; self.link.read(); self.link.transport=lambda _:captured[0]
        with self.assertRaisesRegex(ValueError,'RESPONSE_BINDING'): self.link.read()
        self.held()
    def test_reply_tamper(self):
        def tamper(w):
            obj=g.strict(self.service.handle(w)); obj['payload']['tip']=[4,'f'*64]; return g.canonical(obj)
        self.link.transport=tamper; self.held()
    def test_late_reply(self):
        self.link.deadline=.001
        def late(w):
            r=self.service.handle(w); time.sleep(.01); return r
        self.link.transport=late; self.held()
    def test_cas_race(self):
        old=self.link.read()
        def attempt(i):
            try: return self.link.cas(old,(old[0]+1,g.sha(str(i).encode())))
            except ValueError: return None
        with ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(attempt,range(8)))
        self.assertEqual(sum(r is not None for r in results),1); self.held()
    def test_stale_cas(self):
        old=self.link.read(); new=(old[0]+1,'f'*64); self.link.cas(old,new)
        with self.assertRaisesRegex(ValueError,'ANCHOR_CONFLICT'): self.link.cas(old,(old[0]+1,'e'*64))
    def test_backward_cas(self):
        with self.assertRaisesRegex(ValueError,'NONMONOTONIC_CAS'): self.link.cas(self.link.read(),x.GENESIS)
    def test_no_reprovision(self):
        with self.assertRaises(FileExistsError): x.AnchorService.provision(self.db,self.ident,self.a,self.w.public_key())
        self.assertFalse(self.open(create=True).reconnect())
    def test_lost_before_cas(self):
        self.show(); orig=self.service.handle
        def fail(w):
            if g.strict(w)['payload']['op']=='CAS': raise OSError('lost before commit')
            return orig(w)
        self.link.transport=fail; self.assertEqual(self.client.notify(self.host.revoke()),'DURABLE_HOLD'); self.held()
        self.link.transport=orig; self.assertFalse(self.open().reconnect())
    def test_lost_after_cas(self):
        self.show(); orig=self.service.handle
        def fail(w):
            reply=orig(w)
            if g.strict(w)['payload']['op']=='CAS': raise OSError('lost after commit')
            return reply
        self.link.transport=fail; self.assertEqual(self.client.notify(self.host.revoke()),'DURABLE_HOLD'); self.held()
        self.link.transport=orig; fresh=self.open(); self.assertTrue(fresh.reconnect()); self.held(fresh); self.assertEqual(fresh._inner._state['kind'],'REVOKED')
    def test_service_chain_tamper(self):
        with closing(sqlite3.connect(self.db)) as c,c:
            c.execute('DROP TRIGGER deny_UPDATE'); c.execute('UPDATE advances SET previous_digest=? WHERE n>0',('f'*64,))
        self.held()
    def test_no_raw_records_on_wire(self):
        seen=[]
        def inspect(w):
            q=g.strict(w)['payload']; seen.append(q); self.assertEqual(set(q),{'schema','identity','nonce','op','old','new'}); return self.service.handle(w)
        self.link.transport=inspect; self.show(); self.assertTrue(seen)
    def test_separate_process(self):
        ctx=mp.get_context('spawn'); parent,child=ctx.Pipe()
        secret=self.a.private_bytes(Encoding.Raw,PrivateFormat.Raw,NoEncryption())
        proc=ctx.Process(target=worker,args=(self.db,self.ident,secret,e.key_bytes(self.w.public_key()),child)); proc.start(); child.close()
        try:
            def transport(w):
                parent.send_bytes(w)
                if not parent.poll(2): raise TimeoutError('service timeout')
                return parent.recv_bytes()
            self.link.transport=transport; self.show(); self.client.notify(self.host.revoke()); self.held()
            parent.send_bytes(b'quit'); proc.join(5); self.assertEqual(proc.exitcode,0)
        finally:
            parent.close()
            if proc.is_alive(): proc.terminate(); proc.join()
    def test_key_separation(self):
        with self.assertRaises(ValueError): x.AnchorLink(self.ident,self.w.public_key(),self.w,self.service.handle)
    def test_expiry_during_external_roundtrip(self):
        self.show(); orig=self.service.handle
        def wait(w):
            result=orig(w); time.sleep(.02); return result
        self.link.transport=wait
        with self.client._inner._lock: self.client._inner._deadline=time.monotonic()+.01
        self.held()

if __name__=='__main__': unittest.main()
