"""Additive durable lifecycle reference. Trusted, separately protected anchor required.
No ChatGPT hook, rollback-proof hardware, or cross-database atomicity claim.
"""
from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
import os
import sqlite3
import threading
import time
import secrets

if __package__:
    from . import kuuos_verifyos_conversation_events_v0_20 as e
else:
    import kuuos_verifyos_conversation_events_v0_20 as e
p, g = e.p, e.g
SCHEMA = 'kuuos.verifyos.durable-lifecycle.v0.21.candidate'
DOMAIN = b'KuuOS/VerifyOS/durable-lifecycle/v0.21\0'
ZERO = e.ZERO
MAX_ROWS = 4096  # fail closed rather than discard anti-replay evidence
MAX_RECORD = 16384
ERRORS = (*p.ERRORS, OSError, sqlite3.Error, RuntimeError)
HOLD_HTML = b'<!doctype html><html><meta charset="utf-8"><main><p data-status="HOLD">HOLD: Durable lifecycle not admitted.</p></main></html>'
BOUNDARY = {**e.BOUNDARY, 'cross_database_atomicity_verified':False,
            'external_anchor_rollback_prevention_verified':False,
            'physical_power_loss_recovery_verified':False}


def identity(role, session, client, event_key, presentation_key, verifier_key):
    e.separate(event_key, presentation_key, verifier_key)
    g.require(role in ('host','client') and g.hex64(session) and g.hex64(client), 'IDENTITY')
    return {'schema':SCHEMA, 'role':role, 'session':session, 'client':client,
            'event_key':g.sha(e.key_bytes(event_key)),
            'presentation_key':g.sha(e.key_bytes(presentation_key)),
            'verifier_key':g.sha(e.key_bytes(verifier_key))}


def row_digest(ident, seq, parent, raw):
    return g.sha(DOMAIN + g.canonical({'identity':ident,'seq':seq,'parent':parent,'record_sha256':g.sha(raw)}))


def _connect(path):
    g.require(path.is_file() and not path.is_symlink(), 'STORE_MISSING_OR_SYMLINK')
    db = sqlite3.connect(path.absolute().as_uri()+'?mode=rw', uri=True, timeout=3, isolation_level=None)
    try:
        db.execute('PRAGMA trusted_schema=OFF')
        db.execute('PRAGMA synchronous=FULL')
        return db
    except BaseException:
        db.close(); raise


def _exclusive(path):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(fd)


class AnchoredJournal:
    """Separate anchor CAS serializes cooperative local callers. Both files must exist.
    The anchor must be protected against rollback independently of the journal.
    Neither file is reset, repaired, or advanced from unanchored data on open.
    """
    def __init__(self, data, anchor, ident):
        self.data, self.anchor = Path(data).absolute(), Path(anchor).absolute()
        self.ident = g.sha(g.canonical(ident))
        g.require(self.data != self.anchor, 'SEPARATE_PATHS')

    @classmethod
    def provision(cls, data, anchor, ident):
        j=cls(data,anchor,ident)
        # Explicit creation only; a partial creation is an obstruction, not a reset.
        _exclusive(j.data); _exclusive(j.anchor)
        for path, is_anchor in ((j.data,False),(j.anchor,True)):
            db=_connect(path)
            try:
                db.execute('BEGIN IMMEDIATE')
                db.execute('CREATE TABLE meta (id TEXT PRIMARY KEY)')
                db.execute('INSERT INTO meta VALUES (?)',(j.ident,))
                if is_anchor:
                    db.execute('CREATE TABLE tip (singleton INTEGER PRIMARY KEY CHECK(singleton=1), n INTEGER NOT NULL, digest TEXT NOT NULL)')
                    db.execute('INSERT INTO tip VALUES (1,0,?)',(ZERO,))
                else:
                    db.execute('CREATE TABLE entries (n INTEGER PRIMARY KEY, parent TEXT NOT NULL, digest TEXT NOT NULL UNIQUE, raw BLOB NOT NULL)')
                    for op in ('UPDATE','DELETE'):
                        db.execute(f"CREATE TRIGGER deny_{op} BEFORE {op} ON entries BEGIN SELECT RAISE(ABORT,'APPEND_ONLY'); END")
                db.commit()
            finally: db.close()
        return j

    def _same_storage(self):
        g.require(not self.data.is_symlink() and not self.anchor.is_symlink() and
                  not os.path.samefile(self.data,self.anchor),'SEPARATE_STORAGE')

    @contextmanager
    def locked(self, expected=None):
        """Return a verified, bounded append transaction. Data commits before anchor.
        If interrupted in between, mismatch blocks all subsequent access. A separate
        trusted anchor service is a deployment prerequisite, not provided here.
        """
        self._same_storage()
        a=_connect(self.anchor)
        d=None
        try:
            a.execute('BEGIN IMMEDIATE')
            d=_connect(self.data); d.execute('BEGIN IMMEDIATE')
            for db in (a,d):
                g.require(db.execute('SELECT id FROM meta').fetchall()==[(self.ident,)],'STORE_IDENTITY')
            tip=a.execute('SELECT singleton,n,digest FROM tip').fetchall()
            g.require(len(tip)==1 and tip[0][0]==1,'ANCHOR_SCHEMA')
            _,n,digest=tip[0]
            g.require(type(n) is int and 0<=n<=MAX_ROWS and g.hex64(digest),'ANCHOR_TIP')
            if expected is not None: g.require(expected==(n,digest),'STALE_OWNER')
            rows=d.execute('SELECT n,parent,digest,length(raw),raw FROM entries ORDER BY n LIMIT ?', (MAX_ROWS+1,)).fetchall()
            g.require(len(rows)==n,'ANCHOR_LENGTH_MISMATCH')
            parent=ZERO; records=[]
            for index,(seq,prev,actual,size,raw) in enumerate(rows,1):
                g.require(seq==index and prev==parent and type(raw) is bytes and 0<size<=MAX_RECORD,'JOURNAL_CHAIN')
                g.require(actual==row_digest(self.ident,seq,prev,raw),'JOURNAL_DIGEST')
                records.append(g.strict(raw)); parent=actual
            g.require(parent==digest,'ANCHOR_DIGEST_MISMATCH')
            tx=_Transaction(self,d,a,(n,digest),records)
            yield tx
            # Anchor lock is held until both commits; never expose an unanchored result.
            if tx.tip!=(n,digest):
                cur=a.execute('UPDATE tip SET n=?,digest=? WHERE singleton=1 AND n=? AND digest=?',(*tx.tip,n,digest))
                g.require(cur.rowcount==1,'ANCHOR_CAS')
            d.commit()
            if tx.tip!=(n,digest): self._after_data_commit()
            a.commit()
        finally:
            if d is not None: d.close()
            a.close()

    def _after_data_commit(self):
        """Fault-injection seam; no recovery or callback input from a model."""


class _Transaction:
    def __init__(self,journal,data,anchor,tip,records):
        self.journal,self.data,self.anchor,self.tip,self.records=journal,data,anchor,tip,records

    def append(self,record):
        n,parent=self.tip; raw=g.canonical(record)
        g.require(n<MAX_ROWS and 0<len(raw)<=MAX_RECORD,'JOURNAL_LIMIT')
        digest=row_digest(self.journal.ident,n+1,parent,raw)
        self.data.execute('INSERT INTO entries VALUES (?,?,?,?)',(n+1,parent,digest,raw))
        self.records.append(g.strict(raw)); self.tip=(n+1,digest)


def _observation(raw,purpose,nonce):
    return {'type':'observation','purpose':purpose,'nonce':nonce,'raw':raw.decode('ascii')}


def _decode_observation(record,key,session,client):
    g.require(type(record) is dict and set(record)=={'type','purpose','nonce','raw'} and record['type']=='observation','OBS_RECORD')
    purpose,nonce=record['purpose'],record['nonce']
    g.require((purpose=='EVENT' and nonce is None) or (purpose=='CHECKPOINT' and g.hex64(nonce)), 'OBS_PURPOSE')
    return e.verify(record['raw'].encode('ascii'),key,purpose,session,client,nonce)


class ClientReplay:
    def __init__(self, key, session, client):
        self.key,self.session,self.client=key,session,client
        self.states={}; self.seen=set(); self.seq=-1; self.digest=None; self.state=None
        self.terminal=False; self.reason='NO_CHECKPOINT'

    def observe(self,state,digest):
        seq=state['seq']; known=self.states.get(seq)
        if known is not None and known[1]!=digest:
            self.terminal=True; self.reason='DURABLE_SIGNED_EQUIVOCATION'; return
        prev=self.states.get(seq-1); nxt=self.states.get(seq+1)
        if ((prev is not None and state['previous_sha256']!=prev[1]) or
            (nxt is not None and nxt[0]['previous_sha256']!=digest)):
            self.terminal=True; self.reason='DURABLE_SIGNED_PARENT_CONFLICT'; return
        self.states[seq]=(state,digest)
        if state['kind']=='CLOSED':
            self.terminal=True; self.reason='DURABLE_SESSION_CLOSED'
        if seq>self.seq: self.seq,self.digest,self.state=seq,digest,state

    def apply(self,record):
        typ=record.get('type')
        if typ=='observation':
            g.require(not self.terminal,'POST_TERMINAL_OBSERVATION')
            s,_,digest=_decode_observation(record,self.key,self.session,self.client); self.observe(s,digest)
        elif typ=='boot':
            g.require(set(record)=={'type','id'} and g.hex64(record['id']) and not self.terminal,'BOOT_RECORD')
        elif typ=='turn':
            g.require(set(record)=={'type','id'} and g.hex64(record['id']) and record['id'] not in self.seen and not self.terminal,'TURN_RECORD')
            self.seen.add(record['id'])
        elif typ=='close':
            g.require(set(record)=={'type'} and not self.terminal,'CLOSE_RECORD')
            self.terminal=True; self.reason='DURABLE_CLIENT_CLOSED'
        else: raise ValueError('UNKNOWN_RECORD')


def replay_client(records,key,session,client):
    replay=ClientReplay(key,session,client)
    for record in records: replay.apply(record)
    return replay


class DurableClient:
    """One live owner per anchored client journal. New boot fences old owners.
    Restores high-water/terminal/used turns, never a display, nonce, or lease.
    A new turn ID is required after restart. Snapshot rendering remains bounded.
    """
    def __init__(self,data,anchor,session,client,event_key,presentation_key,verifier_key,*,create=False):
        self._lock=threading.Lock(); self._failed=False; self._tip=None
        self._key,self._session,self._client=event_key,session,client
        self._inner=e.ConversationClient(session,client,event_key,presentation_key,verifier_key)
        ident=identity('client',session,client,event_key,presentation_key,verifier_key)
        try:
            self.journal=(AnchoredJournal.provision(data,anchor,ident) if create else AnchoredJournal(data,anchor,ident))
            with self.journal.locked() as tx:
                replay=replay_client(tx.records,event_key,session,client)
                if not replay.terminal: tx.append({'type':'boot','id':secrets.token_hex(32)})
                self._tip=tx.tip
            self._inner._seq,self._inner._digest,self._inner._state=replay.seq,replay.digest,replay.state
            self._inner._seen=set(replay.seen)
            self._inner._terminal=replay.terminal
            self._inner._connected=False
            self._inner._clear(replay.reason if replay.terminal else 'RESTART_REQUIRES_NEW_TURN')
            self._replay=replay
        except ERRORS: self._poison()

    def _poison(self):
        self._failed=True; self._inner.close()

    def _call(self,fn,default,*,display=False):
        with self._lock:
            if self._failed: return default
            try:
                with self.journal.locked(self._tip) as tx:
                    result=fn(tx); tip=tx.tip
                self._tip=tip
                # Storage commits may block. Recheck local expiry after commit;
                # this is still a snapshot, not a proof of future delivery.
                if display:
                    with self._inner._lock:
                        if not self._inner._live(): return default
                return result
            except ERRORS:
                self._poison(); return default

    def _record(self,tx,raw,purpose,nonce):
        # Store valid signed observations, including evidence of equivocation,
        # before returning any positive admission. Invalid input is not authority.
        try: s,_,digest=e.verify(raw,self._key,purpose,self._session,self._client,nonce)
        except p.ERRORS: return False
        known=self._replay.states.get(s['seq'])
        if known is not None and known[1]==digest: return True
        record=_observation(raw,purpose,nonce)
        tx.append(record); self._replay.apply(record)
        if self._replay.terminal: self._inner.close()
        return True

    def reconnect(self): return self._call(lambda tx:self._inner.reconnect(),False)
    def disconnect(self): return self._call(lambda tx:self._inner.disconnect(),None)
    def close(self):
        def op(tx):
            if not self._replay.terminal:
                row={'type':'close'}; tx.append(row); self._replay.apply(row)
            self._inner.close()
        return self._call(op,None)

    def select_turn(self,question,request,context):
        def op(tx):
            if self._replay.terminal: return None
            try: turn=self._inner.select_turn(question,request,context)
            except p.ERRORS: return None  # predecessor already invalidated display
            row={'type':'turn','id':turn.turn_id}; tx.append(row); self._replay.apply(row)
            return turn
        return self._call(op,None)

    def notify(self,raw):
        def op(tx):
            if self._inner._terminal or not self._inner._connected: return 'INACTIVE'
            self._record(tx,raw,'EVENT',None)
            if self._replay.terminal: return self._replay.reason
            return self._inner.notify(raw)
        return self._call(op,'DURABLE_HOLD')

    def request_checkpoint(self): return self._call(lambda tx:self._inner.request_checkpoint(),None)
    def accept_checkpoint(self,nonce,raw):
        def op(tx):
            if self._inner._terminal or not self._inner._connected: return False
            if nonce!=self._inner._pending or nonce is None: return False
            if time.monotonic()<self._inner._deadline:
                self._record(tx,raw,'CHECKPOINT',nonce)
                if self._replay.terminal: return False
            return self._inner.accept_checkpoint(nonce,raw)
        return self._call(op,False)
    def request(self): return self._call(lambda tx:self._inner.request(),None)
    def accept(self,req,raw): return self._call(lambda tx:self._inner.accept(req,raw),g.hold('DURABLE_HOLD'),display=True)
    def current(self): return self._call(lambda tx:self._inner.current(),g.hold('DURABLE_HOLD'),display=True)
    def render(self): return self._call(lambda tx:self._inner.render(),HOLD_HTML,display=True)


def replay_host(records,key,session,client):
    """Complete contiguous host event history, no restored active presentation."""
    parent=ZERO; last=None; retired=False
    for record in records:
        g.require(not retired,'AFTER_RETIREMENT')
        if record=={'type':'retire'}:
            retired=True; continue
        g.require(last is None or last['kind']!='CLOSED','AFTER_CLOSE')
        s,_,digest=_decode_observation(record,key,session,client)
        g.require(record['purpose']=='EVENT' and s['seq']==(0 if last is None else last['seq']+1) and s['previous_sha256']==parent,'HOST_HISTORY_CHAIN')
        last,parent=s,digest
    g.require(last is not None,'HOST_GENESIS_REQUIRED')
    return last,retired


class DurableHost:
    """Persists signed events before exposure. Old host cannot be rehydrated.
    Recovery retires abandoned identity, fencing cooperative older instances.
    A fresh host identity and new evidence are required for continued operation.
    """
    def __init__(self,data,anchor,verifier_key,presentation_key,event_key,*,ttl_seconds=1800):
        self._host=e.ConversationHost(verifier_key,presentation_key,event_key,ttl_seconds=ttl_seconds)
        self.session_id,self.client_id=self._host.session_id,self._host.client_id
        ident=identity('host',self.session_id,self.client_id,event_key.public_key(),presentation_key.public_key(),verifier_key)
        self._lock=threading.Lock(); self._failed=False
        self.journal=AnchoredJournal.provision(data,anchor,ident)
        with self.journal.locked() as tx:
            tx.append(_observation(self._host.events()[0],'EVENT',None)); self._tip=tx.tip

    def _call(self,fn,default):
        with self._lock:
            if self._failed: return default
            try:
                with self.journal.locked(self._tip) as tx:
                    before=len(self._host.events())
                    try: result=fn()
                    except p.ERRORS: result=default
                    for raw in self._host.events()[before:]: tx.append(_observation(raw,'EVENT',None))
                    tip=tx.tip
                self._tip=tip; return result
            except ERRORS:
                self._failed=True; return default

    def begin(self,*args): return self._call(lambda:self._host.begin(*args),None)
    def revoke(self): return self._call(self._host.revoke,None)
    def close(self): return self._call(self._host.close,None)
    def checkpoint(self,nonce): return self._call(lambda:self._host.checkpoint(nonce),None)
    def receive(self,binding,envelope): return self._call(lambda:self._host.receive(binding,envelope),g.hold('DURABLE_HOST_HOLD'))
    def present(self,wire): return self._call(lambda:self._host.present(wire),None)
    def events(self): return self._call(self._host.events,())


def retire_abandoned_host(data,anchor,session,client,event_key,presentation_key,verifier_key):
    """Trusted recovery operation: full replay and durable retirement, not a new
    signed remote revocation, nor authorization to restore old signing state."""
    try:
        j=AnchoredJournal(data,anchor,identity('host',session,client,event_key,presentation_key,verifier_key))
        with j.locked() as tx:
            last,retired=replay_host(tx.records,event_key,session,client)
            if not retired: tx.append({'type':'retire'})
            result={'status':'RETIRED_ONLY','last_seq':last['seq'],'last_kind':last['kind'],'tip':tx.tip,'boundary':BOUNDARY.copy()}
        return result
    except ERRORS: return {'status':'HOLD','boundary':BOUNDARY.copy()}
