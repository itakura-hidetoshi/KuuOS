"""Actual triple Ed25519 signing and event transitions; v0.17 result mocked."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from pathlib import Path
import socket
import struct
import time
import unittest
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import kuuos_verifyos_conversation_events_v0_20 as e
from test_kuuos_verifyos_turn_presentation_v0_19 import ingress
from test_kuuos_verifyos_closed_surface_v0_18_r2 import view

g,p=e.g,e.p


class ConversationEventTests(unittest.TestCase):
    def setUp(self):
        self.verifier,self.presenter,self.events=(Ed25519PrivateKey.generate() for _ in range(3))
        self.signer=g.TrustedSigner(self.verifier)
        self.host=e.ConversationHost(self.verifier.public_key(),self.presenter,self.events)
        self.client=self.client_for(self.host)
        self.binding,self.event=self.host.begin(*ingress())
        self.client.select_turn(*ingress())

    def client_for(self,host):
        return e.ConversationClient(host.session_id,host.client_id,self.events.public_key(),
                                    self.presenter.public_key(),self.verifier.public_key())

    def checkpoint(self,expected=True):
        n=self.client.request_checkpoint(); self.assertIsNotNone(n)
        self.assertEqual(self.client.accept_checkpoint(n,self.host.checkpoint(n)),expected)

    def envelope(self,binding=None,v=None):
        with patch.object(g,'_run_v017',return_value=(b'synthetic packet',v if v is not None else view())):
            return self.signer.issue((binding or self.binding).challenge,snapshot=None,lean=Path('/synthetic'),
                                     question_bytes=b'question',pair_inputs={})

    def admitted(self,binding=None):
        b=binding or self.binding
        self.assertEqual(self.host.receive(b,self.envelope(b)).status,g.ALL)

    def frame(self):
        req,wire=self.client.request(); return req,self.host.present(wire)

    def show(self):
        self.admitted(); self.checkpoint(); req,raw=self.frame()
        self.assertEqual(self.client.accept(req,raw).status,g.ALL)
        self.assertEqual(self.client.current().status,g.ALL)
        self.assertIn(b'<td>7</td>',self.client.render())
        return req,raw

    def held(self):
        self.assertEqual(self.client.current().status,g.HOLD)
        self.assertIn(b'data-status="HOLD"',self.client.render())
        self.assertNotIn(b'<td>7</td>',self.client.render())

    def test_three_keys_and_positive(self): self.show()

    def test_notification_alone_does_not_admit(self):
        self.admitted(); self.assertEqual(self.client.notify(self.event),'GAP')
        self.held(); self.assertIsNone(self.client.request())

    def test_delivered_revocation(self):
        self.show(); event=self.host.revoke()
        self.assertEqual(self.client.notify(event),'NEW'); self.held()
        self.checkpoint(False); self.held()

    def test_remote_turn_change(self):
        self.show(); b,event=self.host.begin(*ingress(2)); self.client.notify(event)
        self.held(); self.checkpoint(False)
        self.client.select_turn(*ingress(2)); self.admitted(b); self.checkpoint()
        req,raw=self.frame(); self.assertEqual(self.client.accept(req,raw).status,g.ALL)

    def test_lost_event_lease_bound(self):
        self.show(); self.host.revoke()
        # No remote revocation claim without notification or a fresh checkpoint.
        self.assertEqual(self.client.current().status,g.ALL)
        now=time.monotonic()
        with patch.object(e.time,'monotonic',return_value=now+e.LEASE+1):
            self.held(); self.assertIsNone(self.client.request())
        self.checkpoint(False)

    def test_gap_and_resync(self):
        self.show(); self.host.revoke(); b,event=self.host.begin(*ingress(2))
        self.assertEqual(self.client.notify(event),'GAP'); self.held()
        self.client.select_turn(*ingress(2)); self.admitted(b); self.checkpoint()
        req,raw=self.frame(); self.assertEqual(self.client.accept(req,raw).status,g.ALL)

    def test_old_event_does_not_clear_newer_view(self):
        self.show(); old=self.event; self.host.revoke(); b,event=self.host.begin(*ingress(2))
        self.client.notify(event); self.client.select_turn(*ingress(2)); self.admitted(b); self.checkpoint()
        req,raw=self.frame(); self.assertEqual(self.client.accept(req,raw).status,g.ALL)
        self.assertEqual(self.client.notify(old),'STALE'); self.assertEqual(self.client.current().status,g.ALL)

    def test_duplicate_event_no_renewal(self):
        self.show(); self.assertEqual(self.client.notify(self.event),'SAME')
        now=time.monotonic()
        with patch.object(e.time,'monotonic',return_value=now+e.LEASE+1): self.held()

    def test_old_checkpoint_callback_cannot_consume_new(self):
        a=self.client.request_checkpoint(); old=self.host.checkpoint(a)
        b=self.client.request_checkpoint(); self.assertFalse(self.client.accept_checkpoint(a,old))
        self.assertTrue(self.client.accept_checkpoint(b,self.host.checkpoint(b)))

    def test_checkpoint_replay_rejected(self):
        n=self.client.request_checkpoint(); raw=self.host.checkpoint(n)
        self.assertTrue(self.client.accept_checkpoint(n,raw)); self.assertFalse(self.client.accept_checkpoint(n,raw))
        new=self.client.request_checkpoint(); self.assertFalse(self.client.accept_checkpoint(new,raw)); self.held()

    def test_checkpoint_not_event(self):
        n=self.client.request_checkpoint(); self.assertEqual(self.client.notify(self.host.checkpoint(n)),'INVALID'); self.held()

    def test_event_not_checkpoint(self):
        n=self.client.request_checkpoint(); self.assertFalse(self.client.accept_checkpoint(n,self.event)); self.held()

    def test_notification_cancels_pending_checkpoint(self):
        n=self.client.request_checkpoint(); raw=self.host.checkpoint(n)
        self.client.notify(self.host.revoke()); self.assertFalse(self.client.accept_checkpoint(n,raw)); self.held()

    def test_notification_cancels_pending_presentation(self):
        self.admitted(); self.checkpoint(); req,raw=self.frame()
        self.client.notify(self.host.revoke()); self.assertEqual(self.client.accept(req,raw).status,g.HOLD); self.held()

    def test_disconnect_and_reconnect(self):
        req,raw=self.show(); self.client.disconnect(); self.held(); self.assertIsNone(self.client.request_checkpoint())
        self.assertTrue(self.client.reconnect()); self.held()
        self.assertEqual(self.client.accept(req,raw).status,g.HOLD)
        self.checkpoint(); new,frame=self.frame(); self.assertNotEqual(req,new)
        self.assertEqual(self.client.accept(new,frame).status,g.ALL)

    def test_reconnect_after_missed_revocation(self):
        self.show(); self.client.disconnect(); self.host.revoke(); self.client.reconnect(); self.checkpoint(False); self.held()

    def test_reconnect_after_missed_close(self):
        self.show(); self.client.disconnect(); self.host.close(); self.client.reconnect(); self.checkpoint(False)
        self.held(); self.assertFalse(self.client.reconnect()); self.assertIsNone(self.client.request_checkpoint())

    def test_delivered_close_terminal(self):
        self.show(); closed=self.host.close(); self.assertEqual(self.client.notify(closed),'CLOSED'); self.held()
        self.assertFalse(self.client.reconnect()); self.assertEqual(self.host.close(),closed)
        with self.assertRaises(ValueError): self.host.begin(*ingress(2))

    def test_local_close_terminal(self):
        self.show(); self.client.close(); self.held(); self.assertFalse(self.client.reconnect())
        with self.assertRaises(ValueError): self.client.select_turn(*ingress(2))

    def test_cross_session_event(self):
        self.show(); other=e.ConversationHost(self.verifier.public_key(),self.presenter,self.events)
        _,event=other.begin(*ingress()); self.assertEqual(self.client.notify(event),'INVALID'); self.held()

    def test_cross_session_checkpoint(self):
        other=e.ConversationHost(self.verifier.public_key(),self.presenter,self.events)
        other.begin(*ingress()); n=self.client.request_checkpoint()
        self.assertFalse(self.client.accept_checkpoint(n,other.checkpoint(n))); self.held()

    def test_presentation_key_cannot_sign_event(self):
        self.show(); obj=g.strict(self.event); obj['signature_hex']=self.presenter.sign(e.DOMAIN+g.canonical(obj['payload'])).hex()
        self.assertEqual(self.client.notify(g.canonical(obj)),'INVALID'); self.held()

    def test_unsigned_or_noncanonical_event(self):
        self.show(); self.assertEqual(self.client.notify(b'{"status":"SUCCESS"}'),'INVALID'); self.held()
        self.checkpoint(); self.assertEqual(self.client.notify(self.event+b' '),'INVALID'); self.held()

    def test_tampered_state(self):
        self.show(); self.assertEqual(self.client.notify(self.event.replace(b'"seq":1',b'"seq":2')),'INVALID'); self.held()

    def test_signed_equivocation_terminal(self):
        self.show(); s=g.strict(self.event)['payload']['state']; s['kind']='REVOKED'; s['binding']=None
        self.assertEqual(self.client.notify(e.signed(self.events,'EVENT',s)),'FORK'); self.held(); self.assertFalse(self.client.reconnect())

    def test_signed_parent_conflict_terminal(self):
        self.show(); s=g.strict(self.host.revoke())['payload']['state']; s['previous_sha256']='a'*64
        self.assertEqual(self.client.notify(e.signed(self.events,'EVENT',s)),'FORK'); self.held(); self.assertFalse(self.client.reconnect())

    def test_signed_checkpoint_rollback(self):
        self.show(); old=g.strict(self.event)['payload']['state']; self.client.notify(self.host.revoke()); n=self.client.request_checkpoint()
        self.assertFalse(self.client.accept_checkpoint(n,e.signed(self.events,'CHECKPOINT',old,n))); self.held()

    def test_checkpoint_expired_before_delivery(self):
        n=self.client.request_checkpoint(); raw=self.host.checkpoint(n); now=time.monotonic()
        with patch.object(e.time,'monotonic',return_value=now+e.LEASE+1): self.assertFalse(self.client.accept_checkpoint(n,raw))
        self.held()

    def test_frame_expired_before_delivery(self):
        self.admitted(); self.checkpoint(); req,raw=self.frame(); now=time.monotonic()
        with patch.object(e.time,'monotonic',return_value=now+e.LEASE+1): self.assertEqual(self.client.accept(req,raw).status,g.HOLD)
        self.held()

    def test_new_local_turn_cannot_display_old_host(self):
        self.show(); self.client.select_turn(*ingress(2)); self.held(); self.checkpoint(False)

    def test_malformed_host_ingress_revokes(self):
        self.show()
        with self.assertRaises(ValueError): self.host.begin(b'wrong',*ingress(2)[1:])
        self.client.notify(self.host.events()[-1]); self.held(); self.checkpoint(False)

    def test_malformed_client_ingress_revokes(self):
        self.show()
        with self.assertRaises(ValueError): self.client.select_turn(b'wrong',*ingress(2)[1:])
        self.held(); self.checkpoint(False)

    def test_inactive_host_rejects_late_evidence_and_requests(self):
        self.admitted(); self.checkpoint(); req,wire=self.client.request(); self.host.revoke()
        self.assertIsNone(self.host.present(wire)); self.assertEqual(self.host.receive(self.binding,self.envelope()).status,g.HOLD)

    def test_all_events_append_hash_chain(self):
        self.host.revoke(); self.host.begin(*ingress(2)); self.host.close(); previous=e.ZERO
        for i,raw in enumerate(self.host.events()):
            s,_,digest=e.verify(raw,self.events.public_key(),'EVENT',self.host.session_id,self.host.client_id)
            self.assertEqual(s['seq'],i); self.assertEqual(s['previous_sha256'],previous); previous=digest

    def test_distinct_keys(self):
        with self.assertRaises(ValueError): e.ConversationHost(self.verifier.public_key(),self.presenter,self.presenter)
        with self.assertRaises(ValueError): e.ConversationClient(self.host.session_id,self.host.client_id,self.events.public_key(),self.events.public_key(),self.verifier.public_key())

    def test_parallel_checkpoint_one_admission(self):
        n=self.client.request_checkpoint(); raw=self.host.checkpoint(n)
        with ThreadPoolExecutor(max_workers=8) as pool: result=list(pool.map(lambda _:self.client.accept_checkpoint(n,raw),range(8)))
        self.assertEqual(sum(result),1)

    def test_parallel_frame_one_admission(self):
        self.admitted(); self.checkpoint(); req,raw=self.frame()
        with ThreadPoolExecutor(max_workers=8) as pool: result=list(pool.map(lambda _:self.client.accept(req,raw).status,range(8)))
        self.assertEqual(result.count(g.ALL),1)

    def test_real_socket_delivery_and_revocation(self):
        self.show(); a,b=socket.socketpair()
        with a,b:
            raw=self.host.revoke(); a.sendall(struct.pack('!I',len(raw))+raw)
            def read(n):
                out=b''
                while len(out)<n:
                    part=b.recv(n-len(out))
                    if not part: raise EOFError('short event')
                    out+=part
                return out
            packet=read(struct.unpack('!I',read(4))[0]); self.assertEqual(self.client.notify(packet),'NEW'); self.held()
            a.shutdown(socket.SHUT_WR); self.assertEqual(b.recv(1),b''); self.client.disconnect(); self.held()

if __name__=='__main__': unittest.main()
