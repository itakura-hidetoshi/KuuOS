"""Additive v0.24 host-only MCP bridge candidate; not an installed MCP tool.

Preserve upstream v0.1 canonical input bytes (UTF-8 + LF) separately from the
v0.18+ signed transport encoding. No model input selects a ledger, key, verifier,
policy or evidence packet. Real v0.17 execution is necessary for a receipt.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
import copy
import hashlib
import json
from pathlib import Path
import secrets
import threading
import time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
if __package__:
    from . import kuuos_verifyos_host_anchor_v0_23 as h
else:
    import kuuos_verifyos_host_anchor_v0_23 as h
x,d,e,p,g=h.x,h.d,h.e,h.p,h.g
r=p.r
SCHEMA='kuuos.verifyos.mcp-bridge.v0.24.candidate'
DOMAIN=b'KuuOS/VerifyOS/mcp-bridge/v0.24/candidate\0'
BOUNDARY={**h.BOUNDARY,'production_mcp_registered':False,'production_target_authorized':False,
          'complete_runtime_integrity_verified':False,'independent_execution_attested':False}
# Reobserved exact source at predecessor HEAD: v0.1 request schema and v0.2 context schema.
HASH_KEYS=frozenset({'base/kuuos_continuation_20261128_v15.json',
                     'gates/kuuos_inheritance_gate_v16.py','gates/kuuos_scope_guard_v16_1.py'})
PROFILE_SHA='260aa6ad46ee49382c877c43f230f075e91d44b71ba1b9487537fb7809664d85'
# These are code identity pins from v0.17, not private production policy values.
LEAN_SOURCES={
 'MethodSoundCoverage':'177867145b946edbc8851a8176571f0311c82ac4bf842d9812ddcae80a5eb9f5',
 'TypedProjection':'b0577bdc0a74e1108c60b445c7ed8fba4886a491630e06347e3465aec6ecc50c',
 'JsonProjection':'c147594382ed7c2f309eaa594cdbfd7a03045134ab1b24d0491a6dbc10713cbe',
 'ProjectionCLI':'65c76b22d9e1d07d76003c53cf4413a61f8fa6f9a30c2035c6755b80a52033c0',
}
LEAN_VERSION='Lean (version 4.30.0-rc2, x86_64-unknown-linux-gnu, commit 3dc1a088b6d2d8eafe25a7cd7ec7b58d731bd7cc, Release)'


def upstream_canonical(obj):
    return (json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def upstream_strict(raw):
    g.require(type(raw) is bytes and 0<len(raw)<=g.MAX_BYTES,'UPSTREAM_SIZE')
    def unique(items):
        out={}
        for k,v in items:
            g.require(k not in out,'UPSTREAM_DUPLICATE_KEY'); out[k]=v
        return out
    def bad(_): raise ValueError('UPSTREAM_NONFINITE')
    obj=json.loads(raw.decode('utf-8',errors='strict'),object_pairs_hook=unique,parse_constant=bad)
    g.require(upstream_canonical(obj)==raw,'UPSTREAM_NONCANONICAL')
    return obj


def request_check(req):
    g.require(type(req) is dict and set(req)=={'challenge','seq','tip','expected_hashes'},'REQUEST_SCHEMA')
    g.require(g.hex64(req['challenge']) and g.hex64(req['tip']),'REQUEST_BINDING')
    g.require(type(req['seq']) is int and 0<=req['seq']<=100000,'REQUEST_SEQ')
    pins=req['expected_hashes']
    g.require(type(pins) is dict and set(pins)==HASH_KEYS and all(g.hex64(v) for v in pins.values()),'EXPECTED_HASHES')


def exact_turn(question,request,context):
    """Preserve the exact upstream bytes; never re-encode to v0.18 wire JSON."""
    g.require(type(question) is bytes and 0<len(question)<=8192,'QUESTION_BYTES')
    question.decode('utf-8',errors='strict')
    req=upstream_strict(request); request_check(req)
    ctx=upstream_strict(context)
    g.require(type(ctx) is dict and set(ctx)=={'turn_id','question_sha256','challenge','request_sha256','audience'},'CONTEXT_SCHEMA')
    g.require(all(g.hex64(ctx[k]) for k in ('turn_id','question_sha256','challenge','request_sha256')),'CONTEXT_BINDING')
    g.require(ctx['audience']=='private_verification_channel' and ctx['challenge']==req['challenge'],'CONTEXT_AUDIENCE_CHALLENGE')
    t=p.Turn(ctx['turn_id'],g.sha(question),g.sha(request),g.sha(context)); t.validate()
    g.require((ctx['question_sha256'],ctx['request_sha256'])==(t.question_sha256,t.request_sha256),'INGRESS_CONTEXT_BINDING')
    return t


class CanonicalPresentationHost(p.PresentationHost):
    def begin(self,question,request,context):
        with self._lock:
            g.require(not self._closed,'SESSION_CLOSED')
            self._binding=None; self._evidence=None; self._deadline=time.monotonic()+self._ttl
            turn=exact_turn(question,request,context)
            g.require(turn.turn_id not in self._seen_turns,'TURN_ID_REUSE')
            self._seen_turns.add(turn.turn_id); self._epoch+=1
            binding=p.Binding(self.session_id,self.client_id,self._epoch,turn,self._surface.begin(question,request,context))
            binding.validate(); self._binding=binding; return binding


class CanonicalPresentationClient(p.PresentationClient):
    def select_turn(self,question,request,context):
        with self._lock:
            g.require(not self._closed,'CLIENT_CLOSED')
            self._clear('AWAITING_TURN_BINDING'); self._turn=None
            turn=exact_turn(question,request,context)
            g.require(turn.turn_id not in self._seen_turns,'TURN_ID_REUSE')
            self._seen_turns.add(turn.turn_id); self._turn=turn; return turn


class CanonicalConversationHost(e.ConversationHost):
    def __init__(self,verifier_key,presentation_key,event_key,*,ttl_seconds=1800):
        g.require(isinstance(presentation_key,Ed25519PrivateKey) and isinstance(event_key,Ed25519PrivateKey),'HOST_KEYS')
        e.separate(verifier_key,presentation_key.public_key(),event_key.public_key())
        self._host=CanonicalPresentationHost(verifier_key,presentation_key,ttl_seconds=ttl_seconds)
        self.session_id,self.client_id=self._host.session_id,self._host.client_id
        self._event_key=event_key; self._lock=threading.Lock(); self._binding=None
        self._state=e.encode_state(self.session_id,self.client_id,0,e.ZERO,'REVOKED',None)
        self._history=[e.signed(event_key,'EVENT',self._state)]


class CanonicalConversationClient(e.ConversationClient):
    def select_turn(self,question,request,context):
        with self._lock:
            g.require(not self._terminal,'CLIENT_TERMINAL')
            self._clear('LOCAL_TURN_CHANGED'); self._turn=self._ingress=None
            turn=exact_turn(question,request,context)
            g.require(turn.turn_id not in self._seen,'TURN_ID_REUSE')
            self._seen.add(turn.turn_id); self._turn=turn; self._ingress=(question,request,context); return turn

    def accept_checkpoint(self,nonce,raw):
        with self._lock:
            if self._terminal or not self._connected or self._pending is None or nonce!=self._pending: return False
            self._pending=None; deadline=self._deadline
            if time.monotonic()>=deadline:
                self._clear('CHECKPOINT_EXPIRED'); return False
            try:
                s,binding,digest=e.verify(raw,self._event_key,'CHECKPOINT',self._session,self._client,nonce)
                outcome=self._advance(s,digest,checkpoint=True)
                if outcome in ('STALE','FORK','CLOSED'):
                    if not self._terminal: self._clear('CHECKPOINT_ROLLBACK')
                    return False
                g.require(s['kind']=='ACTIVE' and self._turn is not None and binding.turn==self._turn,'CHECKPOINT_TURN_INACTIVE')
                inner=CanonicalPresentationClient(self._session,self._client,self._presentation_key,self._verifier_key)
                inner.select_turn(*self._ingress)
                g.require(inner.activate(binding),'CHECKPOINT_ACTIVATION')
                g.require(time.monotonic()<deadline,'CHECKPOINT_EXPIRED')
                self._inner=inner; self._deadline=deadline; self._reason='AWAITING_PRESENTATION'; return True
            except p.ERRORS:
                self._clear('INVALID_OR_INACTIVE_CHECKPOINT'); return False


class CanonicalExternalHost(h.ExternalHost):
    """Same durable/external-anchor operations as v0.23, corrected ingress only."""
    def __init__(self,data,anchor,verifier_key,presentation_key,event_key,*,authority_key,writer_key,link_provider,ttl_seconds=1800):
        self._host=CanonicalConversationHost(verifier_key,presentation_key,event_key,ttl_seconds=ttl_seconds)
        self.session_id,self.client_id=self._host.session_id,self._host.client_id
        self._lock=threading.Lock(); self._failed=True; self._tip=None
        ident=d.identity('host',self.session_id,self.client_id,event_key.public_key(),presentation_key.public_key(),verifier_key)
        try:
            e.separate(event_key.public_key(),presentation_key.public_key(),verifier_key,authority_key,writer_key)
            link=link_provider(g.sha(g.canonical(ident)))
            h._check_link(link,ident,event_key.public_key(),presentation_key.public_key(),verifier_key,authority_key,writer_key)
            g.require(link.read()==x.GENESIS,'HOST_EXTERNAL_NOT_GENESIS')
            local=d.AnchoredJournal.provision(data,anchor,ident); self.journal=x.ExternallyAnchoredJournal(local,link)
            with self.journal.locked() as tx:
                tx.append(d._observation(self._host.events()[0],'EVENT',None)); tip=tx.tip
            self._tip=tip; self._failed=False
        except x.ERRORS: pass


class CanonicalExternalClient(x.ExternalClient):
    """Same durable/external-anchor operations as v0.22, corrected ingress only."""
    def __init__(self,data,anchor,session,client,event_key,presentation_key,verifier_key,link,*,create=False):
        self._lock=threading.Lock(); self._failed=False; self._tip=None
        self._key,self._session,self._client=event_key,session,client
        self._inner=CanonicalConversationClient(session,client,event_key,presentation_key,verifier_key)
        try:
            e.separate(event_key,presentation_key,verifier_key,link.authority,link.writer.public_key())
            ident=d.identity('client',session,client,event_key,presentation_key,verifier_key)
            g.require(link.ident==g.sha(g.canonical(ident)),'JOURNAL_LINK_IDENTITY')
            if create: g.require(link.read()==x.GENESIS,'EXTERNAL_NOT_GENESIS')
            local=(d.AnchoredJournal.provision(data,anchor,ident) if create else d.AnchoredJournal(data,anchor,ident))
            self.journal=x.ExternallyAnchoredJournal(local,link)
            with self.journal.locked() as tx:
                replay=d.replay_client(tx.records,event_key,session,client)
                if not replay.terminal: tx.append({'type':'boot','id':secrets.token_hex(32)})
                self._tip=tx.tip
            self._inner._seq,self._inner._digest,self._inner._state=replay.seq,replay.digest,replay.state
            self._inner._seen=set(replay.seen); self._inner._terminal=replay.terminal; self._inner._connected=False
            self._inner._clear(replay.reason if replay.terminal else 'RESTART_REQUIRES_NEW_TURN'); self._replay=replay
        except x.ERRORS: self._poison()

    def render(self):
        # A synthetic integration candidate must never present an unqualified
        # production badge. Predecessor display decisions remain typed and local.
        raw=super().render()
        banner=b'<aside role="status">SYNTHETIC ONLY - NOT PRODUCTION</aside>'
        # Insert a fixed banner in the trusted renderer, not caller markup.
        if b'<main>' not in raw:
            return b'<!doctype html><html><meta charset="utf-8"><main>'+banner+b'<p>HOLD</p></main></html>'
        return raw.replace(b'<main>',b'<main>'+banner,1)


@dataclass(frozen=True)
class HostPolicy:
    """Locally provisioned pins; never constructed from MCP arguments or memory."""
    target_id: str
    seq: int
    tip: str
    expected_hashes: tuple[tuple[str,str],...]
    lean_binary_sha256: str
    classification: str = 'SYNTHETIC_ONLY'

    def validate(self):
        g.require(g.hex64(self.target_id) and g.hex64(self.lean_binary_sha256),'POLICY_ID')
        g.require(type(self.expected_hashes) is tuple and len(self.expected_hashes)==len(HASH_KEYS),'POLICY_HASHES')
        g.require(all(type(kv) is tuple and len(kv)==2 for kv in self.expected_hashes),'POLICY_HASHES')
        pins=dict(self.expected_hashes)
        request_check({'challenge':e.ZERO,'seq':self.seq,'tip':self.tip,'expected_hashes':pins})
        g.require(tuple(sorted(pins.items()))==self.expected_hashes,'POLICY_ORDER')
        # Candidate cannot mint a production classification. Production promotion
        # requires an independently authorized service, not a caller's flag.
        g.require(self.classification=='SYNTHETIC_ONLY','PRODUCTION_AUTHORITY_UNAVAILABLE')

    def check(self,req):
        self.validate(); request_check(req)
        g.require((req['seq'],req['tip'],req['expected_hashes'])==(self.seq,self.tip,dict(self.expected_hashes)),'POLICY_REQUEST_MISMATCH')


def _validate_execution(packet,view,binding,policy):
    """Cross-check observed raw v0.17 packet, never a supplied success flag."""
    obj=upstream_strict(packet); ex=obj['execution']; c=binding.challenge
    g.require(obj['schema']=='kuuos.verifyos.lean-egress.v0.17' and obj['status']==g.MATCH,'V017_STATUS')
    g.require(obj['context_sha256']==ex['context_sha256']==c.context_sha256 and ex['request_sha256']==c.request_sha256,'EXECUTION_CONTEXT')
    g.require(g.canonical(view)==g.canonical({k:obj[k] for k in view}),'EXECUTION_VIEW')
    g.require(ex['lean_version']==LEAN_VERSION and ex['lean_binary_sha256']==policy.lean_binary_sha256,'LEAN_BINARY_PIN')
    g.require(type(ex['exit_code']) is int and ex['exit_code']==0,'LEAN_EXIT')
    stages=ex['stages']; g.require(type(stages) is list and len(stages)==len(LEAN_SOURCES),'LEAN_STAGES')
    g.require([s['module'] for s in stages]==list(LEAN_SOURCES),'LEAN_STAGE_ORDER')
    for s in stages:
        g.require(type(s['exit_code']) is int and s['exit_code']==0 and s['source_sha256']==LEAN_SOURCES[s['module']] and g.hex64(s['stdout_sha256']),'LEAN_STAGE_BINDING')
    result=ex['result']; g.require(result['status']=='TYPED_JSON_PROJECTION_ONLY' and result['reason']=='' and all(result[k] is False for k in ('proof_authority','action_authority','complete_python_refinement_proved')),'LEAN_PROJECTION')
    claims=result['claims']; g.require(type(claims) is list and len(claims)==18,'LEAN_CLAIM_COUNT')
    g.require(all(type(row) is dict and set(row)=={'claim_id','value'} for row in claims),'LEAN_CLAIM_SCHEMA')
    values={row['claim_id']:row['value'] for row in claims}
    g.require(len(values)==18 and set(values)==set(r.LABELS),'LEAN_CLAIM_IDS')
    for row in view['claims']:
        g.require(g.canonical(row['value'])==g.canonical(values[row['claim_id']]),'LEAN_CLAIM_MISMATCH')
    g.require(all(g.hex64(ex[k]) for k in ('stdout_sha256','input_sha256','request_sha256','context_sha256')),'EXECUTION_DIGESTS')
    return {'packet_sha256':g.sha(packet),'input_sha256':ex['input_sha256'],'stdout_sha256':ex['stdout_sha256'],
            'projection_sha256':g.sha(upstream_canonical(claims)),'exit_code':0,'lean_binary_sha256':ex['lean_binary_sha256'],
            'source_sha256':dict(LEAN_SOURCES),'claim_count':18}


def _seal(key,payload):
    return g.canonical({'payload':payload,'signature_hex':key.sign(DOMAIN+g.canonical(payload)).hex()})


def hold(reason):
    return {'schema':SCHEMA,'status':'HOLD','reason':reason,'boundary':BOUNDARY.copy()}


class McpBridge:
    """Trusted local controller and challenge-only tool handler candidate.

    Only the authenticated host calls arm/invalidate; only handle is exposed to
    the tool transport. Bind the transport to this user/session before routing.
    No production arm path exists in this candidate; real Lean required even
    for a synthetic receipt. Raw ledger, question, packet and keys stay local.
    """
    def __init__(self,host,policy,verifier_key,receipt_key):
        g.require(type(host) is CanonicalExternalHost and type(policy) is HostPolicy,'HOST_CONFIG')
        policy.validate()
        g.require(isinstance(verifier_key,Ed25519PrivateKey) and isinstance(receipt_key,Ed25519PrivateKey),'HOST_KEYS')
        e.separate(verifier_key.public_key(),receipt_key.public_key())
        # Verify signer identity against the actual provisioned host, not the model.
        g.require(e.key_bytes(verifier_key.public_key())==e.key_bytes(host._host._host._surface._renderer._key),'VERIFIER_PIN')
        self._host=host; self._policy=policy; self._verifier=verifier_key; self._receipt=receipt_key
        self._lock=threading.Lock(); self._pending=None; self._generation=0

    def invalidate(self):
        with self._lock:
            self._generation+=1; self._pending=None; self._host.revoke()

    def arm(self,question,*,snapshot,lean,pair_inputs):
        """Trusted host only. Copy inputs; retain raw data in this process."""
        with self._lock:
            self._generation+=1; self._pending=None
            # Invalid new input cannot retain a previously admitted turn.
            self._host.revoke()
            try:
                args=copy.deepcopy(pair_inputs); req=args['request']; ctx=args['context']
                self._policy.check(req); g.require(args['seed']['question']==question,'ORIGINAL_QUESTION_MISMATCH')
                request,context=upstream_canonical(req),upstream_canonical(ctx)
                exact_turn(question,request,context)
                g.require(isinstance(snapshot,Path) and snapshot.is_absolute() and snapshot.is_dir(),'SNAPSHOT_UNAVAILABLE')
                g.require(isinstance(lean,Path) and lean.is_absolute(),'LEAN_PATH')
                begin=self._host.begin(question,request,context)
                g.require(begin is not None,'HOST_BEGIN_HOLD'); binding,event=begin
                self._pending=(self._generation,binding,snapshot,lean,question,args)
                return binding,event
            except Exception: return None

    def handle(self,args):
        """Candidate MCP handler; exact arguments {challenge}; one-shot execution."""
        if type(args) is not dict or set(args)!={'challenge'} or not g.hex64(args['challenge']): return hold('REQUEST_SCHEMA')
        with self._lock:
            pending=self._pending
            if pending is None or args['challenge']!=pending[1].challenge.nonce: return hold('NO_MATCHING_HOST_CHALLENGE')
            self._pending=None
        generation,binding,snapshot,lean,question,pair_inputs=pending
        try:
            g.require(lean.is_file() and g.sha(lean.resolve().read_bytes())==self._policy.lean_binary_sha256,'PINNED_LEAN_UNAVAILABLE')
            # Fixed existing v0.18 wrapper executes v0.17 publication and display replay.
            packet,view=g._run_v017(snapshot,lean,question,binding.challenge,pair_inputs)
            evidence=_validate_execution(packet,view,binding,self._policy)
            g.require(evidence['input_sha256']==g.sha(pair_inputs['primary_raw']),'RAW_INPUT_BINDING')
            status=g._classify(view); g.require(status!=g.HOLD,'V017_HOLD')
            r.closed_view(g.DisplayDecision(status,'V017_MATCHED',g.canonical(view)))
            v18_payload={'schema':g.SCHEMA,'challenge':asdict(binding.challenge),'predecessor_head':g.PREDECESSOR_HEAD,
                         'packet_sha256':g.sha(packet),'view':view,'status':status,'boundary':g.BOUNDARY.copy()}
            envelope=g.canonical({'payload':v18_payload,'signature_hex':self._verifier.sign(g.DOMAIN+g.canonical(v18_payload)).hex()})
            g.require(len(envelope)<=g.MAX_BYTES,'DISPLAY_SIZE')
            with self._lock:
                g.require(generation==self._generation,'STALE_EXECUTION')
                result=self._host.receive(binding,envelope)
                g.require(result.status==status,'HOST_ADMISSION_HOLD')
                payload={'schema':SCHEMA,'classification':'SYNTHETIC_ONLY','status':'SIGNED_LOCAL_EXECUTION_ONLY',
                         'run_id':secrets.token_hex(32),'binding':asdict(binding),'profile_sha256':PROFILE_SHA,
                         'source_head':g.PREDECESSOR_HEAD,'target_id':self._policy.target_id,'seq':self._policy.seq,
                         'tip':self._policy.tip,'expected_hashes':dict(self._policy.expected_hashes),
                         'display_envelope_sha256':g.sha(envelope),'execution':evidence,'boundary':BOUNDARY.copy()}
                # Do not send raw question, bundle, view or envelope to the model.
                wire=_seal(self._receipt,payload)
                return {'schema':SCHEMA,'status':'SYNTHETIC_EXECUTION_RECEIPT_ONLY','receipt_sha256':g.sha(wire),'signed_receipt':g.strict(wire)}
        except Exception:
            with self._lock:
                if generation==self._generation: self._host.revoke()
            return hold('EXECUTION_OR_ADMISSION_UNAVAILABLE')


def inspect_receipt(response,key,binding,policy):
    """Offline observation check only; never admission or display authority."""
    try:
        g.require(type(response) is dict and set(response)=={'schema','status','receipt_sha256','signed_receipt'},'RESPONSE_SCHEMA')
        g.require(response['schema']==SCHEMA and response['status']=='SYNTHETIC_EXECUTION_RECEIPT_ONLY','RESPONSE_CLASS')
        wire=g.canonical(response['signed_receipt']); g.require(g.sha(wire)==response['receipt_sha256'],'RECEIPT_DIGEST')
        obj=g.strict(wire); g.require(set(obj)=={'payload','signature_hex'},'SIGNATURE_SCHEMA')
        payload=obj['payload']; sig=obj['signature_hex']; g.require(type(sig) is str and len(sig)==128 and sig==sig.lower(),'SIGNATURE_FORMAT')
        key.verify(bytes.fromhex(sig),DOMAIN+g.canonical(payload))
        policy.validate(); binding.validate()
        g.require(set(payload)=={'schema','classification','status','run_id','binding','profile_sha256','source_head','target_id','seq','tip','expected_hashes','display_envelope_sha256','execution','boundary'},'PAYLOAD_SCHEMA')
        g.require(payload['schema']==SCHEMA and payload['classification']=='SYNTHETIC_ONLY' and payload['status']=='SIGNED_LOCAL_EXECUTION_ONLY' and g.hex64(payload['run_id']),'PAYLOAD_CLASS')
        g.require(g.canonical(payload['binding'])==g.canonical(asdict(binding)) and payload['profile_sha256']==PROFILE_SHA and payload['source_head']==g.PREDECESSOR_HEAD,'PAYLOAD_BINDING')
        g.require((payload['target_id'],payload['seq'],payload['tip'],payload['expected_hashes'])==(policy.target_id,policy.seq,policy.tip,dict(policy.expected_hashes)),'TARGET_BINDING')
        g.require(type(payload['seq']) is int and g.canonical(payload['boundary'])==g.canonical(BOUNDARY) and g.hex64(payload['display_envelope_sha256']),'PAYLOAD_BOUNDARY')
        ex=payload['execution']; g.require(set(ex)=={'packet_sha256','input_sha256','stdout_sha256','projection_sha256','exit_code','lean_binary_sha256','source_sha256','claim_count'},'EVIDENCE_SCHEMA')
        g.require(all(g.hex64(ex[k]) for k in ('packet_sha256','input_sha256','stdout_sha256','projection_sha256')),'EVIDENCE_DIGEST')
        g.require(ex['lean_binary_sha256']==policy.lean_binary_sha256 and ex['source_sha256']==LEAN_SOURCES and type(ex['exit_code']) is int and ex['exit_code']==0 and type(ex['claim_count']) is int and ex['claim_count']==18,'EVIDENCE_FIELDS')
        return {'status':'SYNTHETIC_RECEIPT_SIGNATURE_MATCHED_ONLY','production_status':'HOLD','receipt_sha256':response['receipt_sha256']}
    except Exception: return {'status':'HOLD','production_status':'HOLD'}
