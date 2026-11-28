"""Real SQLite, real signatures, real abrupt child exit. v0.17 is mocked."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing, contextmanager
from pathlib import Path
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import kuuos_verifyos_durable_lifecycle_v0_21 as d
from test_kuuos_verifyos_turn_presentation_v0_19 import ingress
from test_kuuos_verifyos_closed_surface_v0_18_r2 import view

e,g=d.e,d.g


class DurableTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.root=Path(tmp.name)
        self.v,self.p,self.k=(Ed25519PrivateKey.generate() for _ in range(3))
        self.host=d.DurableHost(self.root/'host.db',self.root/'host-anchor.db',self.v.public_key(),self.p,self.k)
        self.binding,self.event=self.host.begin(*ingress())
        self.signer=g.TrustedSigner(self.v)
        self.client=self.open_client(create=True)
        self.assertTrue(self.client.reconnect()); self.assertIsNotNone(self.client.select_turn(*ingress()))

    def open_client(self,create=False,key=None):
        return d.DurableClient(self.root/'client.db',self.root/'client-anchor.db',self.host.session_id,self.host.client_id,
                            key or self.k.public_key(),self.p.public_key(),self.v.public_key(),create=create)

    def retire(self):
        return d.retire_abandoned_host(self.root/'host.db',self.root/'host-anchor.db',self.host.session_id,self.host.client_id,
                                      self.k.public_key(),self.p.public_key(),self.v.public_key())

    def held(self,c=None):
        c=c or self.client; self.assertEqual(c.current().status,g.HOLD); self.assertIn(b'data-status="HOLD"',c.render())

    def envelope(self,binding):
        with patch.object(g,'_run_v017',return_value=(b'synthetic packet',view())):
            return self.signer.issue(binding.challenge,snapshot=None,lean=Path('/synthetic'),question_bytes=b'question',pair_inputs={})

    def show(self,c=None,binding=None):
        c=c or self.client; binding=binding or self.binding
        self.assertEqual(self.host.receive(binding,self.envelope(binding)).status,g.ALL)
        nonce=c.request_checkpoint(); self.assertTrue(c.accept_checkpoint(nonce,self.host.checkpoint(nonce)))
        req,wire=c.request(); frame=self.host.present(wire); self.assertEqual(c.accept(req,frame).status,g.ALL)
        self.assertIn(b'<td>7</td>',c.render()); return req,frame

    def test_positive(self): self.show()

    def test_restart_drops_lease_and_used_turn(self):
        req,frame=self.show(); new=self.open_client(); self.held(new); self.held()
        self.assertTrue(new.reconnect()); self.assertIsNone(new.select_turn(*ingress()))
        self.assertEqual(new.accept(req,frame).status,g.HOLD)
        self.assertEqual(new._inner._seq,1)
        b,ev=self.host.begin(*ingress(2)); self.assertIsNotNone(new.select_turn(*ingress(2))); self.show(new,b)

    def test_persist_revocation(self):
        self.show(); self.assertEqual(self.client.notify(self.host.revoke()),'NEW'); self.held()
        new=self.open_client(); self.assertEqual(new._inner._seq,2); self.assertEqual(new._inner._state['kind'],'REVOKED'); self.held(new)

    def test_persist_remote_close(self):
        self.show(); self.assertEqual(self.client.notify(self.host.close()),'DURABLE_SESSION_CLOSED')
        new=self.open_client(); self.held(new); self.assertFalse(new.reconnect())

    def test_persist_local_close(self):
        self.show(); self.client.close(); new=self.open_client(); self.assertFalse(new.reconnect()); self.held(new)

    def test_persist_equivocation(self):
        self.show(); state=g.strict(self.event)['payload']['state']; state.update(kind='REVOKED',binding=None)
        self.assertEqual(self.client.notify(e.signed(self.k,'EVENT',state)),'DURABLE_SIGNED_EQUIVOCATION')
        self.assertFalse(self.open_client().reconnect())

    def test_old_sequence_fork_is_not_discarded(self):
        self.show(); self.client.notify(self.host.revoke()); self.client.notify(self.host.begin(*ingress(2))[1])
        state=g.strict(self.event)['payload']['state']; state.update(kind='REVOKED',binding=None)
        self.assertEqual(self.client.notify(e.signed(self.k,'EVENT',state)),'DURABLE_SIGNED_EQUIVOCATION')
        self.assertFalse(self.open_client().reconnect())

    def test_late_parent_conflict_detected(self):
        self.show(); missed=self.host.revoke(); b,ev=self.host.begin(*ingress(2)); self.assertEqual(self.client.notify(ev),'GAP')
        state=g.strict(missed)['payload']['state']; state['previous_sha256']='f'*64
        self.assertEqual(self.client.notify(e.signed(self.k,'EVENT',state)),'DURABLE_SIGNED_PARENT_CONFLICT')
        self.assertFalse(self.open_client().reconnect())

    def test_late_valid_event_retained(self):
        self.show(); missed=self.host.revoke(); self.client.notify(self.host.begin(*ingress(2))[1]); self.assertEqual(self.client.notify(missed),'STALE')
        new=self.open_client(); self.assertIn(2,new._replay.states); self.assertEqual(new._replay.seq,3)

    def test_checkpoint_rollback_after_restart(self):
        self.show(); self.client.notify(self.host.revoke()); new=self.open_client(); new.reconnect(); new.select_turn(*ingress(2))
        nonce=new.request_checkpoint(); old=g.strict(self.event)['payload']['state']
        self.assertFalse(new.accept_checkpoint(nonce,e.signed(self.k,'CHECKPOINT',old,nonce))); self.held(new)

    def test_bad_signature_not_journaled(self):
        self.show(); tip=self.client._tip; self.assertEqual(self.client.notify(b'{}'),'INVALID'); self.assertEqual(self.client._tip,tip); self.held()

    def test_same_signed_state_does_not_grow(self):
        self.show(); tip=self.client._tip; self.assertEqual(self.client.notify(self.event),'SAME'); self.assertEqual(self.client._tip,tip)

    def test_old_nonce_does_not_consume_pending(self):
        a=self.client.request_checkpoint(); old=self.host.checkpoint(a); b=self.client.request_checkpoint()
        self.assertFalse(self.client.accept_checkpoint(a,old)); self.assertTrue(self.client.accept_checkpoint(b,self.host.checkpoint(b)))

    def test_expired_checkpoint_not_journaled(self):
        n=self.client.request_checkpoint(); raw=self.host.checkpoint(n); tip=self.client._tip
        with patch.object(d.time,'monotonic',return_value=self.client._inner._deadline+1): self.assertFalse(self.client.accept_checkpoint(n,raw))
        self.assertEqual(self.client._tip,tip); self.held()

    def test_store_rollback_detected_on_live_render(self):
        self.show(); self.client.disconnect(); backup=self.root/'old.db'; shutil.copyfile(self.root/'client.db',backup)
        self.client.reconnect(); self.client.select_turn(*ingress(2)); self.show(binding=self.host.begin(*ingress(2))[0]); shutil.copyfile(backup,self.root/'client.db'); self.held()
        self.assertFalse(self.open_client().reconnect())

    def test_anchor_rollback_detected(self):
        old=self.root/'old-anchor.db'; shutil.copyfile(self.root/'client-anchor.db',old); self.show(); shutil.copyfile(old,self.root/'client-anchor.db'); self.held()
        self.assertFalse(self.open_client().reconnect())

    def test_data_tamper_detected(self):
        self.show()
        with closing(sqlite3.connect(self.root/'client.db')) as db, db:
            db.execute('DROP TRIGGER deny_UPDATE'); db.execute("UPDATE entries SET raw=x'7b7d' WHERE n=1")
        self.held(); self.assertFalse(self.open_client().reconnect())

    def test_append_only_triggers(self):
        with closing(sqlite3.connect(self.root/'client.db')) as db, db:
            with self.assertRaises(sqlite3.IntegrityError): db.execute('DELETE FROM entries')
            with self.assertRaises(sqlite3.IntegrityError): db.execute('UPDATE entries SET parent=parent')

    def test_missing_anchor_never_created(self):
        self.show(); path=self.root/'client-anchor.db'; path.unlink(); self.held(); self.assertFalse(self.open_client().reconnect()); self.assertFalse(path.exists())

    def test_missing_data_never_created(self):
        self.show(); path=self.root/'client.db'; path.unlink(); self.held(); self.assertFalse(self.open_client().reconnect()); self.assertFalse(path.exists())

    def test_wrong_key_refuses_reopen(self):
        self.show(); self.assertFalse(self.open_client(key=Ed25519PrivateKey.generate().public_key()).reconnect()); self.assertEqual(self.client.current().status,g.ALL)

    def test_existing_files_never_reprovisioned(self):
        self.show(); self.assertFalse(self.open_client(create=True).reconnect()); self.assertEqual(self.client.current().status,g.ALL)

    def test_different_identity_file_refused(self):
        self.show(); c=d.DurableClient(self.root/'client.db',self.root/'client-anchor.db','e'*64,self.host.client_id,self.k.public_key(),self.p.public_key(),self.v.public_key()); self.assertFalse(c.reconnect())

    def test_intercommit_fault_poison_and_reopen_hold(self):
        self.show(); event=self.host.revoke()
        with patch.object(self.client.journal,'_after_data_commit',side_effect=OSError('injected')): self.assertEqual(self.client.notify(event),'DURABLE_HOLD')
        self.held(); self.assertFalse(self.open_client().reconnect())

    def test_before_commit_fault_old_pair_still_readable(self):
        self.show(); event=self.host.revoke()
        with patch.object(d._Transaction,'append',side_effect=OSError('injected')): self.assertEqual(self.client.notify(event),'DURABLE_HOLD')
        self.held(); new=self.open_client(); self.assertTrue(new.reconnect()); self.held(new)
        self.assertEqual(new._inner._seq,1); self.assertEqual(new.notify(event),'NEW')

    def test_owner_fence_parallel_boots(self):
        self.show()
        with ThreadPoolExecutor(max_workers=8) as pool: clients=list(pool.map(lambda _:self.open_client(),range(8)))
        self.assertEqual(sum(c.reconnect() for c in clients),1); self.held()

    def test_parallel_observation(self):
        self.show(); event=self.host.revoke()
        with ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(lambda _:self.client.notify(event),range(8)))
        self.assertEqual(results.count('NEW'),1); self.assertEqual(results.count('SAME'),7); self.held()

    def test_retire_abandoned_host_fences_signing(self):
        self.show(); result=self.retire(); self.assertEqual(result['status'],'RETIRED_ONLY'); self.assertEqual(result['last_seq'],1)
        self.assertIsNone(self.host.checkpoint('a'*64)); self.assertIsNone(self.host.begin(*ingress(2)))
        self.assertEqual(self.retire(),result)
        # Remote client cannot observe retirement without notification/recheck.
        self.assertIsNone(self.host.present(b'{}'))

    def test_host_history_close_preserved(self):
        self.host.revoke(); self.host.close(); result=self.retire(); self.assertEqual((result['last_seq'],result['last_kind']),(3,'CLOSED'))

    def test_invalid_host_ingress_persists_revocation(self):
        self.assertIsNone(self.host.begin(b'x',b'{}',b'{}')); self.assertEqual(self.retire()['last_kind'],'REVOKED')

    def test_host_fault_no_unanchored_event_returned(self):
        with patch.object(self.host.journal,'_after_data_commit',side_effect=OSError('injected')): self.assertIsNone(self.host.revoke())
        self.assertIsNone(self.host.checkpoint('a'*64)); self.assertEqual(self.retire()['status'],'HOLD')

    def test_host_data_rollback_no_signature(self):
        old=self.root/'oldhost.db'; shutil.copyfile(self.root/'host.db',old); self.host.revoke(); shutil.copyfile(old,self.root/'host.db')
        self.assertIsNone(self.host.checkpoint('a'*64)); self.assertEqual(self.retire()['status'],'HOLD')

    def test_hardlink_same_file_refused(self):
        path=self.root/'linked.db'; os.link(self.root/'client.db',path)
        j=d.AnchoredJournal(self.root/'client.db',path,{});
        with self.assertRaises(ValueError):
            with j.locked(): pass

    def test_symlink_refused(self):
        path=self.root/'symlink.db'; path.symlink_to(self.root/'client.db'); j=d.AnchoredJournal(path,self.root/'client-anchor.db',{})
        with self.assertRaises(ValueError):
            with j.locked(): pass

    def test_capacity_fails_closed(self):
        self.show(); n=self.client._tip[0]
        with patch.object(d,'MAX_ROWS',n): self.assertEqual(self.client.notify(self.host.revoke()),'DURABLE_HOLD'); self.held()

    def test_child_crash_between_commits(self):
        # Public identity, no private signing key in child. Exercise actual abrupt exit
        # on the storage primitive using a valid local boot record.
        self.show(); script='''import os,sys,json\nimport kuuos_verifyos_durable_lifecycle_v0_21 as d\nj=d.AnchoredJournal(sys.argv[1],sys.argv[2],json.loads(sys.argv[3]))\nj._after_data_commit=lambda:os._exit(73)\nwith j.locked() as tx: tx.append({'type':'boot','id':'c'*64})\n'''
        ident=d.identity('client',self.host.session_id,self.host.client_id,self.k.public_key(),self.p.public_key(),self.v.public_key())
        result=subprocess.run([sys.executable,'-B','-c',script,str(self.root/'client.db'),str(self.root/'client-anchor.db'),g.canonical(ident).decode()],capture_output=True,timeout=10)
        self.assertEqual(result.returncode,73,result.stderr); self.held(); self.assertFalse(self.open_client().reconnect())

    def test_post_commit_expiry_blocks_return(self):
        self.show(); clock=[time.monotonic()]; original=self.client.journal.locked
        @contextmanager
        def delayed(*args,**kwargs):
            with original(*args,**kwargs) as tx: yield tx
            clock[0]+=e.LEASE+1
        with patch.object(d.time,'monotonic',side_effect=lambda:clock[0]), patch.object(self.client.journal,'locked',side_effect=delayed):
            self.assertEqual(self.client.current().status,g.HOLD)
            self.assertIn(b'data-status="HOLD"',self.client.render())

    def test_actual_child_reopen_fences_parent(self):
        self.show(); self.client.notify(self.host.revoke())
        script="""import sys,json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
import kuuos_verifyos_durable_lifecycle_v0_21 as d
from test_kuuos_verifyos_turn_presentation_v0_19 import ingress
keys=[Ed25519PublicKey.from_public_bytes(bytes.fromhex(x)) for x in sys.argv[5:]]
c=d.DurableClient(*sys.argv[1:5],*keys)
assert c.reconnect() and c.current().status==d.g.HOLD
assert c._inner._seq==2 and c._inner._state['kind']=='REVOKED'
assert c.select_turn(*ingress()) is None
print('PUBLIC_KEY_ONLY_RESTART_OK')
"""
        keys=[e.key_bytes(x.public_key()).hex() for x in (self.k,self.p,self.v)]
        out=subprocess.run([sys.executable,'-B','-W','error::ResourceWarning','-c',script,str(self.root/'client.db'),str(self.root/'client-anchor.db'),self.host.session_id,self.host.client_id,*keys],capture_output=True,timeout=10)
        self.assertEqual(out.returncode,0,out.stderr); self.assertEqual(out.stdout.strip(),b'PUBLIC_KEY_ONLY_RESTART_OK'); self.held()

    def test_both_files_rollback_outside_trust_boundary(self):
        # Deliberate negative result: a restored pair is indistinguishable without
        # an independently nonrollbackable anchor. No positive display is restored.
        paths=[self.root/'client.db',self.root/'client-anchor.db']; saved=[x.read_bytes() for x in paths]
        self.show(); self.client.notify(self.host.revoke())
        for path,raw in zip(paths,saved): path.write_bytes(raw)
        new=self.open_client(); self.assertTrue(new.reconnect()); self.assertEqual(new._inner._seq,-1); self.held(new)
        self.assertFalse(d.BOUNDARY['external_anchor_rollback_prevention_verified'])

if __name__=='__main__': unittest.main()
