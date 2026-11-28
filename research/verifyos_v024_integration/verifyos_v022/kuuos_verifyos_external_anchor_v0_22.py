"""Reference external anchor for v0.21 client journals. No remote deployment.
Trust: independently protected monotonic service store and keys; trusted writer.
Only journal identities and digests cross the service boundary, never raw records.
"""
from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
import secrets, time, threading, sqlite3
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
if __package__:
    from . import kuuos_verifyos_durable_lifecycle_v0_21 as d
else:
    import kuuos_verifyos_durable_lifecycle_v0_21 as d
e,p,g=d.e,d.p,d.g
SCHEMA='kuuos.verifyos.external-anchor.v0.22.candidate'
REQUEST=b'KuuOS/VerifyOS/external-anchor/v0.22/request\0'
RESPONSE=b'KuuOS/VerifyOS/external-anchor/v0.22/response\0'
GENESIS=(0,d.ZERO)
ERRORS=(*d.ERRORS, EOFError, TimeoutError)
BOUNDARY={**d.BOUNDARY,'independent_service_storage_verified':False,'global_monotonicity_proved':False,
          'remote_current_at_delivery_verified':False,'cross_service_atomicity_verified':False}

def tip(x):
    g.require(type(x) in (list,tuple) and len(x)==2 and type(x[0]) is int and 0<=x[0]<=d.MAX_ROWS and g.hex64(x[1]) and ((x[0]==0)==(x[1]==d.ZERO)), 'TIP')
    return tuple(x)

def seal(key,domain,payload):
    return g.canonical({'payload':payload,'signature_hex':key.sign(domain+g.canonical(payload)).hex()})

def unseal(raw,key,domain):
    g.require(type(raw) is bytes and len(raw)<=8192,'WIRE_LIMIT')
    x=g.strict(raw)
    g.require(type(x) is dict and set(x)=={'payload','signature_hex'},'ENVELOPE')
    s=x['signature_hex']; g.require(type(s) is str and len(s)==128 and all(c in '0123456789abcdef' for c in s),'SIGNATURE_FORMAT')
    key.verify(bytes.fromhex(s),domain+g.canonical(x['payload']))
    return x['payload']

class AnchorService:
    """One explicitly provisioned journal; separately managed service key and DB.
    No reset, no implicit adoption, no client-selected authority. Trusted filesystem.
    Signed READ/CAS responses bind exact request. CAS serializes in SQLite.
    """
    def __init__(self,path,ident,service_key,writer_key):
        self.path=Path(path); self.ident=ident; self.key=service_key; self.writer=writer_key
        g.require(g.hex64(ident) and isinstance(service_key,Ed25519PrivateKey),'SERVICE_CONFIG')
        e.separate(service_key.public_key(),writer_key)
        self.config=g.sha(g.canonical({'schema':SCHEMA,'identity':ident,'authority':g.sha(e.key_bytes(service_key.public_key())), 'writer':g.sha(e.key_bytes(writer_key))}))
    @classmethod
    def provision(cls,path,ident,service_key,writer_key):
        s=cls(path,ident,service_key,writer_key); d._exclusive(s.path)
        db=d._connect(s.path)
        try:
            db.execute('BEGIN IMMEDIATE'); db.execute('CREATE TABLE config (id TEXT PRIMARY KEY)'); db.execute('INSERT INTO config VALUES (?)',(s.config,))
            db.execute('CREATE TABLE advances (n INTEGER PRIMARY KEY, digest TEXT NOT NULL UNIQUE, previous_n INTEGER NOT NULL, previous_digest TEXT NOT NULL)')
            db.execute('INSERT INTO advances VALUES (0,?,0,?)',(d.ZERO,d.ZERO))
            for op in ('UPDATE','DELETE'): db.execute(f"CREATE TRIGGER deny_{op} BEFORE {op} ON advances BEGIN SELECT RAISE(ABORT,'APPEND_ONLY'); END")
            db.commit()
        finally: db.close()
        return s
    def handle(self,wire):
        q=unseal(wire,self.writer,REQUEST)
        g.require(type(q) is dict and set(q)=={'schema','identity','nonce','op','old','new'} and q['schema']==SCHEMA and q['identity']==self.ident and g.hex64(q['nonce']),'REQUEST_BINDING')
        op=q['op']; g.require(op in ('READ','CAS'),'OP')
        if op=='READ': g.require(q['old'] is None and q['new'] is None,'READ_SCHEMA')
        else:
            old,new=tip(q['old']),tip(q['new']); g.require(new[0]>old[0] and new[1]!=old[1],'NONMONOTONIC_CAS')
        db=d._connect(self.path)
        try:
            db.execute('BEGIN IMMEDIATE')
            g.require(db.execute('SELECT id FROM config').fetchall()==[(self.config,)],'SERVICE_IDENTITY')
            rows=db.execute('SELECT n,digest,previous_n,previous_digest FROM advances ORDER BY n LIMIT ?',(d.MAX_ROWS+1,)).fetchall()
            g.require(bool(rows) and rows[0]==(0,d.ZERO,0,d.ZERO),'SERVICE_GENESIS')
            current=GENESIS
            for n,h,pn,ph in rows[1:]:
                nxt=tip((n,h)); g.require(n>current[0] and h!=current[1] and (pn,ph)==current,'SERVICE_CHAIN'); current=nxt
            status='READ'
            if op=='CAS':
                if current!=old: status='CONFLICT'
                else:
                    db.execute('INSERT INTO advances VALUES (?,?,?,?)',(*new,*old)); current=new; status='ADVANCED'
            db.commit()
        finally: db.close()
        return seal(self.key,RESPONSE,{'schema':SCHEMA,'identity':self.ident,'request_sha256':g.sha(wire),'nonce':q['nonce'],'status':status,'tip':list(current)})

class AnchorLink:
    """Pinned keys and trusted transport adapter, outside model control.
    Deadline detects late returns; transport itself must implement a hard timeout.
    """
    def __init__(self,ident,authority_key,writer_key,transport,*,deadline=2.0):
        g.require(g.hex64(ident) and isinstance(writer_key,Ed25519PrivateKey) and 0<deadline<=10,'LINK_CONFIG')
        e.separate(authority_key,writer_key.public_key())
        self.ident,self.authority,self.writer,self.transport,self.deadline=ident,authority_key,writer_key,transport,deadline
    def _call(self,op,old=None,new=None):
        nonce=secrets.token_hex(32); start=time.monotonic()
        wire=seal(self.writer,REQUEST,{'schema':SCHEMA,'identity':self.ident,'nonce':nonce,'op':op,'old':old,'new':new})
        try: response=self.transport(wire)
        except Exception as exc: raise ValueError('ANCHOR_TRANSPORT_UNAVAILABLE') from exc
        a=unseal(response,self.authority,RESPONSE)
        g.require(type(a) is dict and set(a)=={'schema','identity','request_sha256','nonce','status','tip'} and a['schema']==SCHEMA and a['identity']==self.ident and a['nonce']==nonce and a['request_sha256']==g.sha(wire),'RESPONSE_BINDING')
        t=tip(a['tip']); g.require(time.monotonic()-start<self.deadline,'ANCHOR_TIMEOUT')
        g.require(a['status']==('READ' if op=='READ' else 'ADVANCED'),'ANCHOR_CONFLICT')
        if op=='CAS': g.require(t==new,'CAS_RESULT')
        return t
    def read(self): return self._call('READ')
    def cas(self,old,new):
        old,new=tip(old),tip(new); g.require(new[0]>old[0] and new[1]!=old[1],'NONMONOTONIC_CAS'); return self._call('CAS',old,new)

class ExternallyAnchoredJournal:
    """Guard v0.21 transaction before and after local commit. A failed external
    CAS leaves the committed local suffix unadmitted. No auto-recovery.
    """
    def __init__(self,local,link):
        g.require(local.ident==link.ident,'JOURNAL_LINK_IDENTITY'); self.local,self.link=local,link
    @contextmanager
    def locked(self,expected=None):
        with self.local.locked(expected) as tx:
            old=tx.tip; g.require(self.link.read()==old,'EXTERNAL_TIP_MISMATCH')
            yield tx
            new=tx.tip
        if new!=old: self.link.cas(old,new)
        g.require(self.link.read()==new,'EXTERNAL_POSTCOMMIT_MISMATCH')

class ExternalClient(d.DurableClient):
    """Additive v0.21 client with explicitly provisioned external anchor.
    The v0.21 host is unchanged; this does not protect host rollback by itself.
    """
    def __init__(self,data,anchor,session,client,event_key,presentation_key,verifier_key,link,*,create=False):
        self._lock=threading.Lock(); self._failed=False; self._tip=None
        self._key,self._session,self._client=event_key,session,client
        self._inner=e.ConversationClient(session,client,event_key,presentation_key,verifier_key)
        try:
            e.separate(event_key,presentation_key,verifier_key,link.authority,link.writer.public_key())
            ident=d.identity('client',session,client,event_key,presentation_key,verifier_key)
            g.require(link.ident==g.sha(g.canonical(ident)),'JOURNAL_LINK_IDENTITY')
            if create: g.require(link.read()==GENESIS,'EXTERNAL_NOT_GENESIS')
            local=(d.AnchoredJournal.provision(data,anchor,ident) if create else d.AnchoredJournal(data,anchor,ident))
            self.journal=ExternallyAnchoredJournal(local,link)
            with self.journal.locked() as tx:
                replay=d.replay_client(tx.records,event_key,session,client)
                if not replay.terminal: tx.append({'type':'boot','id':secrets.token_hex(32)})
                self._tip=tx.tip
            self._inner._seq,self._inner._digest,self._inner._state=replay.seq,replay.digest,replay.state
            self._inner._seen=set(replay.seen); self._inner._terminal=replay.terminal; self._inner._connected=False
            self._inner._clear(replay.reason if replay.terminal else 'RESTART_REQUIRES_NEW_TURN'); self._replay=replay
        except ERRORS: self._poison()
