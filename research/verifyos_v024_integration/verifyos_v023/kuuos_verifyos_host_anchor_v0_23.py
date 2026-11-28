"""Additive host anchor and bounded authenticated local IPC reference.
No deployment, remote storage independence, or ChatGPT interception claimed.
"""
from __future__ import annotations
from pathlib import Path
import os, socket, struct, threading, time, math
if __package__:
    from . import kuuos_verifyos_external_anchor_v0_22 as x
else:
    import kuuos_verifyos_external_anchor_v0_22 as x
d,e,p,g=x.d,x.e,x.p,x.g
SCHEMA='kuuos.verifyos.host-anchor.v0.23.candidate'
BOUNDARY={**x.BOUNDARY,'production_transport_verified':False,
          'production_key_custody_verified':False,'host_event_source_authenticated':False,
          'actual_chatgpt_interception_verified':False,'continuous_remote_freshness_verified':False}
MAX_WIRE=8192


def _remaining(end):
    left=end-time.monotonic()
    if left<=0: raise TimeoutError('IPC_DEADLINE')
    return left


def _read(sock,n,end):
    parts=bytearray()
    while len(parts)<n:
        sock.settimeout(_remaining(end)); part=sock.recv(n-len(parts))
        if not part: raise EOFError('IPC_TRUNCATED')
        parts.extend(part)
    return bytes(parts)


def _receive(sock,end):
    n=struct.unpack('!I',_read(sock,4,end))[0]
    g.require(0<n<=MAX_WIRE,'IPC_FRAME_SIZE')
    return _read(sock,n,end)


def _send(sock,raw,end):
    g.require(type(raw) is bytes and 0<len(raw)<=MAX_WIRE,'IPC_FRAME_SIZE')
    sock.settimeout(_remaining(end)); sock.sendall(struct.pack('!I',len(raw))+raw)
    _remaining(end)


class UnixTransport:
    """One request per connection, bounded total I/O, no automatic retry of CAS.
    v0.22 authenticates the exact request and response with pinned Ed25519 keys.
    Unix socket permissions are additional local access control, not remote TLS.
    """
    def __init__(self,path,*,timeout=1.0):
        self.path=Path(path).absolute()
        g.require(type(timeout) in (int,float) and math.isfinite(timeout) and 0<timeout<=5,'IPC_TIMEOUT_CONFIG')
        self.timeout=timeout
    def __call__(self,wire):
        end=time.monotonic()+self.timeout
        with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as conn:
            conn.settimeout(_remaining(end)); conn.connect(str(self.path))
            _send(conn,wire,end); result=_receive(conn,end); _remaining(end)
            return result


def serve_local(path,service,stop,ready,*,io_timeout=1.0):
    """Run in a service-owned directory. Call with pre-provisioned AnchorService.
    Never accept raw journal data, arbitrary commands, or unauthenticated CAS.
    Invalid frames/signatures close the connection without state change.
    A blocked DB handler may finish after the client times out: client holds.
    """
    path=Path(path).absolute()
    g.require(type(io_timeout) in (int,float) and math.isfinite(io_timeout) and 0<io_timeout<=5,'IPC_TIMEOUT_CONFIG')
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as listener:
        # Trusted owner-only parent, no unlink or replace of an existing endpoint.
        g.require(path.parent.is_dir() and not path.parent.is_symlink() and path.parent.stat().st_uid==os.geteuid() and path.parent.stat().st_mode&0o077==0,'IPC_DIRECTORY')
        listener.bind(str(path)); inode=path.lstat().st_ino
        try:
            path.chmod(0o600); listener.listen(8); listener.settimeout(.05); ready.set()
            while not stop.is_set():
                try: conn,_=listener.accept()
                except TimeoutError: continue
                with conn:
                    try:
                        end=time.monotonic()+io_timeout
                        wire=_receive(conn,end); response=service.handle(wire)
                        _send(conn,response,end)
                    except x.ERRORS: continue
        finally:
            if path.exists() and path.lstat().st_ino==inode: path.unlink()


def _check_link(link,ident,event_key,presentation_key,verifier_key,authority_key,writer_key):
    g.require(isinstance(link,x.AnchorLink) and link.ident==g.sha(g.canonical(ident)),'HOST_ANCHOR_IDENTITY')
    g.require(e.key_bytes(link.authority)==e.key_bytes(authority_key) and e.key_bytes(link.writer.public_key())==e.key_bytes(writer_key),'HOST_ANCHOR_PIN')
    e.separate(event_key,presentation_key,verifier_key,authority_key,writer_key)


class ExternalHost(d.DurableHost):
    """Host events are withheld until local journal and external CAS agree.
    New host only. Trusted provisioner returns a separately provisioned link
    for the newly generated identity. No adoption of a non-genesis remote tip.
    No resurrection of old signing state after interruption.
    """
    def __init__(self,data,anchor,verifier_key,presentation_key,event_key,*,authority_key,writer_key,link_provider,ttl_seconds=1800):
        self._host=e.ConversationHost(verifier_key,presentation_key,event_key,ttl_seconds=ttl_seconds)
        self.session_id,self.client_id=self._host.session_id,self._host.client_id
        self._lock=threading.Lock(); self._failed=True; self._tip=None
        ident=d.identity('host',self.session_id,self.client_id,event_key.public_key(),presentation_key.public_key(),verifier_key)
        try:
            # The callback is trusted deployment configuration, not model input.
            e.separate(event_key.public_key(),presentation_key.public_key(),verifier_key,authority_key,writer_key)
            link=link_provider(g.sha(g.canonical(ident)))
            _check_link(link,ident,event_key.public_key(),presentation_key.public_key(),verifier_key,authority_key,writer_key)
            g.require(link.read()==x.GENESIS,'HOST_EXTERNAL_NOT_GENESIS')
            local=d.AnchoredJournal.provision(data,anchor,ident)
            self.journal=x.ExternallyAnchoredJournal(local,link)
            with self.journal.locked() as tx:
                tx.append(d._observation(self._host.events()[0],'EVENT',None)); tip=tx.tip
            self._tip=tip; self._failed=False
        except x.ERRORS: pass


def retire_external_host(data,anchor,session,client,event_key,presentation_key,verifier_key,link,*,authority_key,writer_key):
    """Retire only an externally admitted host history. Never repair or rehydrate.
    A returned retirement observation is not a remote revocation delivery proof.
    """
    try:
        ident=d.identity('host',session,client,event_key,presentation_key,verifier_key)
        _check_link(link,ident,event_key,presentation_key,verifier_key,authority_key,writer_key)
        journal=x.ExternallyAnchoredJournal(d.AnchoredJournal(data,anchor,ident),link)
        with journal.locked() as tx:
            last,retired=d.replay_host(tx.records,event_key,session,client)
            if not retired: tx.append({'type':'retire'})
            tip=tx.tip
        return {'status':'RETIRED_ONLY','last_seq':last['seq'],'last_kind':last['kind'],'tip':tip,'boundary':BOUNDARY.copy()}
    except x.ERRORS: return {'status':'HOLD','boundary':BOUNDARY.copy()}
