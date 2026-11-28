"""Additive trusted conversation-event adapter for VerifyOS v0.19.

Local reference only. Ingress, event signing, key provisioning and transport
must be controlled outside the model. No ChatGPT hook or remote-currentness proof.
"""
from __future__ import annotations
from dataclasses import asdict
import re
import secrets
import threading
import time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

if __package__:
    from . import kuuos_verifyos_turn_presentation_v0_19 as p
else:
    import kuuos_verifyos_turn_presentation_v0_19 as p

g = p.g
SCHEMA = 'kuuos.verifyos.conversation-events.v0.20.candidate'
DOMAIN = b'KuuOS/VerifyOS/conversation-events/v0.20/candidate\0'
LEASE = 3  # seconds from local request, not arrival; research default
ZERO = '0'*64
BOUNDARY = {**p.BOUNDARY, 'instant_remote_revocation_verified':False,
            'complete_event_history_verified':False, 'durable_rollback_prevention_verified':False}


def key_bytes(key):
    return key.public_bytes(Encoding.Raw, PublicFormat.Raw)


def separate(*keys):
    g.require(all(isinstance(k,Ed25519PublicKey) for k in keys) and
              len({key_bytes(k) for k in keys}) == len(keys), 'DISTINCT_PUBLIC_KEYS')


def encode_state(session, client, seq, previous, kind, binding):
    return {'session_id':session,'client_id':client,'seq':seq,'previous_sha256':previous,
            'kind':kind,'binding':asdict(binding) if binding is not None else None}


def decode_state(s, session, client):
    g.require(type(s) is dict and set(s)=={'session_id','client_id','seq','previous_sha256','kind','binding'},'STATE_SCHEMA')
    g.require(s['session_id']==session and s['client_id']==client and
              g.hex64(session) and g.hex64(client),'STATE_IDENTITY')
    g.require(type(s['seq']) is int and 0<=s['seq']<2**63 and g.hex64(s['previous_sha256']), 'STATE_SEQUENCE')
    g.require((s['seq']==0)==(s['previous_sha256']==ZERO), 'GENESIS_PARENT')
    kind=s['kind']
    g.require(kind in ('ACTIVE','REVOKED','CLOSED') and (s['seq']!=0 or kind=='REVOKED'),'STATE_KIND')
    if kind!='ACTIVE':
        g.require(s['binding'] is None,'INACTIVE_BINDING')
        return None
    binding=p.wire_request(g.canonical({'binding':s['binding'],'nonce':ZERO})).binding
    g.require(binding.session_id==session and binding.client_id==client,'BINDING_IDENTITY')
    return binding


def signed(key, purpose, state, nonce=None):
    payload={'schema':SCHEMA,'purpose':purpose,'state':state,'nonce':nonce,'boundary':BOUNDARY.copy()}
    return g.canonical({'payload':payload,'signature_hex':key.sign(DOMAIN+g.canonical(payload)).hex()})


def verify(raw,key,purpose,session,client,nonce=None):
    obj=g.strict(raw)
    g.require(type(obj) is dict and set(obj)=={'payload','signature_hex'},'EVENT_ENVELOPE')
    sig=obj['signature_hex']; payload=obj['payload']
    g.require(type(sig) is str and re.fullmatch('[0-9a-f]{128}',sig),'EVENT_SIGNATURE')
    key.verify(bytes.fromhex(sig),DOMAIN+g.canonical(payload))
    g.require(type(payload) is dict and set(payload)=={'schema','purpose','state','nonce','boundary'},'EVENT_PAYLOAD')
    g.require(payload['schema']==SCHEMA and payload['purpose']==purpose and payload['nonce']==nonce and
              g.canonical(payload['boundary'])==g.canonical(BOUNDARY),'EVENT_BINDING')
    s=payload['state']; binding=decode_state(s,session,client)
    return s,binding,g.sha(g.canonical(s))


class ConversationHost:
    """Sole trusted ingress and event-signing adapter; no arbitrary sign endpoint.

    Serialized, in-memory, append-only state observations. All present/receive
    operations use the active binding. External authentication is a prerequisite.
    """
    def __init__(self, verifier_key, presentation_key, event_key, *, ttl_seconds=1800):
        g.require(isinstance(presentation_key,Ed25519PrivateKey) and isinstance(event_key,Ed25519PrivateKey),'HOST_KEYS')
        separate(verifier_key,presentation_key.public_key(),event_key.public_key())
        self._host=p.PresentationHost(verifier_key,presentation_key,ttl_seconds=ttl_seconds)
        self.session_id=self._host.session_id; self.client_id=self._host.client_id
        self._event_key=event_key; self._lock=threading.Lock(); self._binding=None
        self._state=encode_state(self.session_id,self.client_id,0,ZERO,'REVOKED',None)
        self._history=[signed(event_key,'EVENT',self._state)]

    def _append(self,kind,binding=None):
        self._state=encode_state(self.session_id,self.client_id,self._state['seq']+1,
                                 g.sha(g.canonical(self._state)),kind,binding)
        self._binding=binding
        self._history.append(signed(self._event_key,'EVENT',self._state))
        return self._history[-1]

    def begin(self,question,request,context):
        with self._lock:
            g.require(self._state['kind']!='CLOSED','SESSION_CLOSED')
            try:
                binding=self._host.begin(question,request,context)
            except p.ERRORS:
                self._append('REVOKED')
                raise
            return binding,self._append('ACTIVE',binding)

    def revoke(self):
        with self._lock:
            g.require(self._state['kind']!='CLOSED','SESSION_CLOSED')
            return self._append('REVOKED')

    def close(self):
        with self._lock:
            if self._state['kind']=='CLOSED': return self._history[-1]
            self._host.close()
            return self._append('CLOSED')

    def events(self):
        with self._lock: return tuple(self._history)

    def checkpoint(self,nonce):
        """A fresh challenge-bound checkpoint, not a historical completeness proof."""
        if not g.hex64(nonce): return None
        with self._lock: return signed(self._event_key,'CHECKPOINT',self._state,nonce)

    def receive(self,binding,envelope):
        with self._lock:
            if self._binding is None or binding!=self._binding: return g.hold('EVENT_BINDING_INACTIVE')
            return self._host.receive(binding,envelope)

    def present(self,wire):
        with self._lock:
            try:
                req=p.wire_request(wire)
                if self._binding is None or req.binding!=self._binding: return None
                return self._host.present(wire)
            except p.ERRORS: return None


class ConversationClient:
    """Only this wrapper may render. Notifications invalidate, never grant admission.

    Checkpoint nonces and lease deadlines are locally generated. Reconnect keeps
    the high-water mark but drops all display state. Process restart needs fresh
    identity; no persistent rollback defense is asserted.
    """
    def __init__(self,session,client,event_key,presentation_key,verifier_key):
        g.require(g.hex64(session) and g.hex64(client),'CLIENT_IDENTITY')
        separate(event_key,presentation_key,verifier_key)
        self._session=session; self._client=client; self._event_key=event_key
        self._presentation_key=presentation_key; self._verifier_key=verifier_key
        self._lock=threading.Lock(); self._connected=True; self._terminal=False
        self._seq=-1; self._digest=None; self._state=None
        self._turn=None; self._ingress=None; self._seen=set()
        self._pending=None; self._deadline=0.0; self._inner=None
        self._reason='NO_CHECKPOINT'

    def _clear(self,reason):
        if self._inner is not None: self._inner.close()
        self._inner=None; self._pending=None; self._deadline=0.0; self._reason=reason

    def select_turn(self,question,request,context):
        with self._lock:
            g.require(not self._terminal,'CLIENT_TERMINAL')
            self._clear('LOCAL_TURN_CHANGED'); self._turn=self._ingress=None
            turn=p.exact_turn(question,request,context)
            g.require(turn.turn_id not in self._seen,'TURN_ID_REUSE')
            self._seen.add(turn.turn_id); self._turn=turn; self._ingress=(question,request,context)
            return turn

    def disconnect(self):
        with self._lock:
            self._connected=False; self._clear('DISCONNECTED')

    def close(self):
        with self._lock:
            self._terminal=True; self._connected=False
            self._turn=self._ingress=None; self._clear('CLIENT_CLOSED')

    def reconnect(self):
        with self._lock:
            if self._terminal: return False
            self._clear('RECONNECT_REQUIRES_CHECKPOINT'); self._connected=True; return True

    def _advance(self,s,digest,*,checkpoint=False):
        """Signed observations are monotonic; forks at observed seq fail terminally.
        A checkpoint may cross a gap; that does not validate missing events.
        """
        seq=s['seq']
        if seq<self._seq: return 'STALE'
        if seq==self._seq:
            if digest!=self._digest:
                self._terminal=True; self._clear('SIGNED_EQUIVOCATION'); return 'FORK'
            return 'SAME'
        # Check the known immediate parent, including on checkpoint.
        if seq==self._seq+1 and self._seq>=0 and s['previous_sha256']!=self._digest:
            self._terminal=True; self._clear('SIGNED_PARENT_CONFLICT'); return 'FORK'
        gap=seq>self._seq+1
        self._seq=seq; self._digest=digest; self._state=s
        if s['kind']=='CLOSED':
            self._terminal=True; self._clear('SESSION_CLOSED'); return 'CLOSED'
        if not checkpoint: self._clear('EVENT_GAP' if gap else 'NEW_EVENT_REQUIRES_CHECKPOINT')
        return 'GAP' if gap else 'NEW'

    def notify(self,raw):
        with self._lock:
            if self._terminal or not self._connected: return 'INACTIVE'
            try:
                s,_,digest=verify(raw,self._event_key,'EVENT',self._session,self._client)
                return self._advance(s,digest)
            except p.ERRORS:
                self._clear('INVALID_EVENT'); return 'INVALID'

    def request_checkpoint(self):
        with self._lock:
            if not self._connected or self._terminal: return None
            self._clear('AWAITING_CHECKPOINT')
            nonce=secrets.token_hex(32); self._pending=nonce
            self._deadline=time.monotonic()+LEASE
            return nonce

    def accept_checkpoint(self,nonce,raw):
        with self._lock:
            if self._terminal or not self._connected or self._pending is None or nonce!=self._pending: return False
            self._pending=None
            deadline=self._deadline
            if time.monotonic()>=deadline:
                self._clear('CHECKPOINT_EXPIRED'); return False
            try:
                s,binding,digest=verify(raw,self._event_key,'CHECKPOINT',self._session,self._client,nonce)
                outcome=self._advance(s,digest,checkpoint=True)
                if outcome in ('STALE','FORK','CLOSED'):
                    if not self._terminal: self._clear('CHECKPOINT_ROLLBACK')
                    return False
                g.require(s['kind']=='ACTIVE' and self._turn is not None and binding.turn==self._turn,'CHECKPOINT_TURN_INACTIVE')
                inner=p.PresentationClient(self._session,self._client,self._presentation_key,self._verifier_key)
                inner.select_turn(*self._ingress)
                g.require(inner.activate(binding),'CHECKPOINT_ACTIVATION')
                g.require(time.monotonic()<deadline,'CHECKPOINT_EXPIRED')
                self._inner=inner; self._deadline=deadline; self._reason='AWAITING_PRESENTATION'
                return True
            except p.ERRORS:
                self._clear('INVALID_OR_INACTIVE_CHECKPOINT'); return False

    def _live(self):
        if not self._connected or self._terminal or self._inner is None: return False
        if time.monotonic()>=self._deadline:
            self._clear('EVENT_LEASE_EXPIRED'); return False
        return True

    def request(self):
        with self._lock: return self._inner.request() if self._live() else None

    def accept(self,req,raw):
        with self._lock:
            if not self._live(): return g.hold(self._reason)
            decision=self._inner.accept(req,raw)
            return decision if self._live() else g.hold(self._reason)

    def current(self):
        with self._lock:
            if not self._live(): return g.hold(self._reason)
            d=self._inner.current()
            return d if self._live() else g.hold(self._reason)

    def render(self):
        with self._lock:
            if self._live():
                result=self._inner.render()
                if self._live(): return result
            return b'<!doctype html><html lang="en"><meta charset="utf-8"><main><p data-status="HOLD">HOLD: No active event-bound presentation.</p></main></html>'
