"""Additive v0.19 reference: bind a bounded presentation to trusted ingress.

This is a host/client protocol, not an interception hook for ChatGPT or a
production authentication service. Only authenticated transport/application
code may call the ingress and host APIs. The model has no host capabilities.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
import html
import re
import secrets
import threading
import time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

if __package__:
    from . import kuuos_verifyos_display_gate_v0_18 as g
    from . import kuuos_verifyos_closed_surface_v0_18_r2 as r
else:
    import kuuos_verifyos_display_gate_v0_18 as g
    import kuuos_verifyos_closed_surface_v0_18_r2 as r

SCHEMA = 'kuuos.verifyos.turn-presentation.v0.19.candidate'
DOMAIN = b'KuuOS/VerifyOS/turn-presentation/v0.19/candidate\0'
MAX_TTL = 5  # seconds on client clock, measured from request, not arrival
BOUNDARY = {**g.BOUNDARY, 'live_browser_revocation_verified': False,
            'authenticated_transport_verified': False,
            'historical_execution_attested': False}
ERRORS = (ValueError, TypeError, KeyError, AttributeError, OverflowError,
          UnicodeError, RecursionError, InvalidSignature)


@dataclass(frozen=True)
class Turn:
    turn_id: str
    question_sha256: str
    request_sha256: str
    context_sha256: str

    def validate(self):
        g.require(all(g.hex64(v) for v in asdict(self).values()), 'TURN_FORMAT')


def exact_turn(question, request, context):
    """Match original host bytes to the v0.17 context, never model guesses."""
    obj = g.strict(context)
    g.require(type(obj) is dict, 'CONTEXT_TYPE')
    t = Turn(obj['turn_id'], g.sha(question), g.sha(request), g.sha(context))
    t.validate()
    g.require(obj['question_sha256'] == t.question_sha256 and
              obj['request_sha256'] == t.request_sha256, 'INGRESS_CONTEXT_BINDING')
    return t


@dataclass(frozen=True)
class Binding:
    session_id: str
    client_id: str
    epoch: int
    turn: Turn
    challenge: g.Challenge

    def validate(self):
        g.require(g.hex64(self.session_id) and g.hex64(self.client_id) and
                  type(self.epoch) is int and 0 < self.epoch < 2**63 and
                  type(self.turn) is Turn and type(self.challenge) is g.Challenge, 'BINDING_FORMAT')
        self.turn.validate(); self.challenge.validate()
        g.require((self.turn.question_sha256, self.turn.request_sha256, self.turn.context_sha256) ==
                  (self.challenge.question_sha256, self.challenge.request_sha256,
                   self.challenge.context_sha256), 'CHALLENGE_TURN_BINDING')


@dataclass(frozen=True)
class PresentationRequest:
    binding: Binding
    nonce: str

    def validate(self):
        g.require(type(self.binding) is Binding and g.hex64(self.nonce), 'REQUEST_FORMAT')
        self.binding.validate()


def wire_request(raw):
    """Strict JSON transport decode. The parsed request is NOT authentication."""
    obj = g.strict(raw)
    g.require(type(obj) is dict and set(obj) == {'binding','nonce'}, 'REQUEST_SCHEMA')
    b = obj['binding']
    g.require(type(b) is dict and set(b) == {'session_id','client_id','epoch','turn','challenge'}, 'BINDING_SCHEMA')
    req = PresentationRequest(Binding(b['session_id'], b['client_id'], b['epoch'],
                                      Turn(**b['turn']), g.Challenge(**b['challenge'])), obj['nonce'])
    req.validate()
    g.require(g.canonical(asdict(req)) == raw, 'REQUEST_RECONSTRUCTION')
    return req


def _clean_view(rows, branches):
    """Copy only R2's typed, rechecked projection, including inactive branches."""
    def aggregate(ids):
        n = sum(x.status == g.OBSERVED for x in rows if x.claim_id in ids)
        return 'ALL_OBSERVED' if n == len(ids) else 'PARTIAL' if n else 'HOLD'
    active = [x for x in branches if x.active]
    active_ids = set().union(*(set(x.required) for x in active))
    original = aggregate({x.claim_id for x in rows})
    answer = aggregate(active_ids)
    if len(branches) > 1 and original != g.HOLD:
        original = 'AMBIGUOUS_' + original
    if answer != g.HOLD:
        answer = ('AMBIGUOUS_' if len(active) > 1 else 'ACTIVE_VIEW_') + answer
    return {'claims':[asdict(x) for x in rows],
            'branches':[{'interpretation_id':x.interpretation_id,
                         'active_in_revised_view':x.active, 'status':x.status,
                         'required_claim_ids':list(x.required),
                         'conditional_claim_ids':list(x.conditional)} for x in branches],
            'answer_status':answer, 'original_family_status':original,
            'selected_interpretation':None}


class PresentationHost:
    """One authenticated session/client pair, provisioned by trusted host code.

    The presentation key is separate from the v0.18 verification key. No public
    mutation or arbitrary-signing API. The R2 surface is exclusively owned here.
    """
    def __init__(self, verifier_key, presentation_key, *, ttl_seconds=1800):
        g.require(isinstance(verifier_key, Ed25519PublicKey) and
                  isinstance(presentation_key, Ed25519PrivateKey), 'HOST_KEYS')
        from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
        def raw(key): return key.public_bytes(Encoding.Raw, PublicFormat.Raw)
        g.require(raw(verifier_key) != raw(presentation_key.public_key()), 'SEPARATE_KEYS_REQUIRED')
        self.session_id = secrets.token_hex(32)
        self.client_id = secrets.token_hex(32)
        self._surface = r.ClosedSurface(verifier_key, ttl_seconds=ttl_seconds)
        self._key = presentation_key
        self._lock = threading.Lock()
        self._epoch = 0
        self._binding = None
        self._evidence = None
        self._seen_turns = set()
        self._ttl = ttl_seconds
        self._deadline = 0.0
        self._closed = False

    def begin(self, question, request, context):
        with self._lock:
            g.require(not self._closed, 'SESSION_CLOSED')
            # Invalidate first, including malformed new ingress.
            self._binding = None
            self._evidence = None
            self._deadline = time.monotonic() + self._ttl
            turn = exact_turn(question, request, context)
            g.require(turn.turn_id not in self._seen_turns, 'TURN_ID_REUSE')
            self._seen_turns.add(turn.turn_id)
            self._epoch += 1
            binding = Binding(self.session_id, self.client_id, self._epoch, turn,
                              self._surface.begin(question, request, context))
            binding.validate()
            self._binding = binding
            return binding

    def receive(self, binding, envelope):
        with self._lock:
            if self._closed or self._binding is None or binding != self._binding:
                return g.hold('STALE_HOST_BINDING')
            result = self._surface.receive(binding.challenge, envelope)
            if result.status != g.HOLD:
                self._evidence = envelope
            return result

    def close(self):
        with self._lock:
            self._closed = True
            self._binding = None
            self._evidence = None

    def present(self, raw_request):
        """Sign only a freshly read R2 snapshot, not caller-provided content.

        No bearer authentication: transport must route by authenticated session.
        Signed HOLD or no response cannot grant observed status. Bounded local
        validity is not proof that a remote turn has not since changed.
        """
        try:
            req = wire_request(raw_request)
            with self._lock:
                if self._closed or self._binding is None or req.binding != self._binding:
                    return None
                # R2 has no public typed snapshot API. Use its existing locked
                # snapshot in this additive reference; pin and audit at integration.
                with self._surface._lock:
                    status, rows, branches, ch = self._surface._snapshot()
                if ch != req.binding.challenge:
                    return None
                # Require enough host lifetime to cover a full client request window.
                # Clocks must have ordinary comparable rates; no distributed time proof.
                if self._deadline - time.monotonic() < MAX_TTL:
                    status = g.HOLD
                view = None if status == g.HOLD else _clean_view(rows, branches)
                evidence = None
                if view is not None:
                    r.closed_view(g.DisplayDecision(status, '', g.canonical(view)))
                    evidence = g.strict(self._evidence)
                payload = {'schema':SCHEMA, 'request':asdict(req), 'status':status,
                           'view':view, 'evidence':evidence, 'boundary':BOUNDARY.copy()}
                out = g.canonical({'payload':payload,
                    'signature_hex':self._key.sign(DOMAIN + g.canonical(payload)).hex()})
                g.require(len(out) <= g.MAX_BYTES, 'FRAME_SIZE')
                return out
        except ERRORS:
            return None


class PresentationClient:
    """Final-renderer state for one provisioned session/client identity.

    A trusted local turn-change/disconnect event clears the display synchronously.
    HTTP completion handlers MUST call accept, never insert raw response HTML.
    No methods accept free-form model output. Render is a snapshot, not a live
    browser revocation mechanism. Use a fresh identity after process restart.
    """
    def __init__(self, session_id, client_id, public_key, verifier_key):
        g.require(g.hex64(session_id) and g.hex64(client_id) and
                  isinstance(public_key, Ed25519PublicKey) and
                  isinstance(verifier_key, Ed25519PublicKey), 'CLIENT_PROVISIONING')
        from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
        g.require(public_key.public_bytes(Encoding.Raw, PublicFormat.Raw) !=
                  verifier_key.public_bytes(Encoding.Raw, PublicFormat.Raw), 'SEPARATE_KEYS_REQUIRED')
        # Pure envelope verification; this private R1 method does not admit a
        # new challenge or perform Lean. Integration must pin the R1 source.
        self._evidence_verifier = g.TrustedRenderer(verifier_key)
        self._session, self._client, self._key = session_id, client_id, public_key
        self._lock = threading.Lock()
        self._turn = self._binding = self._pending = None
        self._last_epoch = 0
        self._seen_turns = set()
        self._display = g.hold('NO_LOCAL_TURN')
        self._deadline = 0.0
        self._closed = False

    def _clear(self, reason):
        self._binding = self._pending = None
        self._display = g.hold(reason)
        self._deadline = 0.0

    def select_turn(self, question, request, context):
        with self._lock:
            g.require(not self._closed, 'CLIENT_CLOSED')
            self._clear('AWAITING_TURN_BINDING')
            self._turn = None
            turn = exact_turn(question, request, context)
            g.require(turn.turn_id not in self._seen_turns, 'TURN_ID_REUSE')
            self._seen_turns.add(turn.turn_id)
            self._turn = turn
            return self._turn

    def activate(self, binding):
        """Binding obtained from trusted ingress transport, not response prose."""
        with self._lock:
            try:
                g.require(not self._closed and self._turn is not None and
                          type(binding) is Binding, 'NO_LOCAL_TURN')
                binding.validate()
                g.require(binding.session_id == self._session and binding.client_id == self._client
                          and binding.turn == self._turn and binding.epoch > self._last_epoch,
                          'STALE_OR_FOREIGN_BINDING')
                self._clear('AWAITING_PRESENTATION')
                self._binding = binding
                self._last_epoch = binding.epoch
                return True
            except ERRORS:
                return False  # a stale binding must not mutate a newer turn

    def invalidate(self):
        with self._lock:
            self._turn = None
            self._clear('LOCAL_TURN_INVALIDATED')

    def close(self):
        with self._lock:
            self._closed = True
            self._turn = None
            self._clear('CLIENT_CLOSED')

    def request(self):
        with self._lock:
            if self._closed or self._binding is None:
                return None
            req = PresentationRequest(self._binding, secrets.token_hex(32))
            self._pending = req
            self._deadline = time.monotonic() + MAX_TTL
            self._display = g.hold('AWAITING_PRESENTATION')
            return req, g.canonical(asdict(req))

    def _verify(self, req, raw):
        obj = g.strict(raw)
        g.require(type(obj) is dict and set(obj) == {'payload','signature_hex'}, 'FRAME_SCHEMA')
        sig = obj['signature_hex']
        g.require(type(sig) is str and re.fullmatch('[0-9a-f]{128}',sig), 'SIGNATURE_FORMAT')
        payload = obj['payload']
        self._key.verify(bytes.fromhex(sig), DOMAIN + g.canonical(payload))
        g.require(type(payload) is dict and set(payload) == {'schema','request','status','view','evidence','boundary'}, 'PAYLOAD_SCHEMA')
        g.require(payload['schema'] == SCHEMA and g.canonical(payload['request']) == g.canonical(asdict(req))
                  and g.canonical(payload['boundary']) == g.canonical(BOUNDARY), 'FRAME_BINDING')
        status, view = payload['status'], payload['view']
        if status == g.HOLD:
            g.require(view is None and payload['evidence'] is None, 'HOLD_VIEW')
            return g.hold('HOST_HOLD')
        decision = g.DisplayDecision(status, '', g.canonical(view))
        rows, branches = r.closed_view(decision)
        # Exact projection equality rejects extra prose or metadata even if signed.
        g.require(decision.view_json == g.canonical(_clean_view(rows, branches)), 'NOT_CLOSED_PROJECTION')
        original = self._evidence_verifier._verify_envelope(
            g.canonical(payload['evidence']), req.binding.challenge)
        g.require(original.status == status, 'ORIGINAL_EVIDENCE_NOT_MATCHED')
        original_rows, original_branches = r.closed_view(original)
        g.require(decision.view_json == g.canonical(_clean_view(original_rows, original_branches)),
                  'ORIGINAL_EVIDENCE_VIEW_MISMATCH')
        return decision

    def accept(self, req, raw):
        # Lock across final validation and state update. Old callbacks cannot
        # consume the new request or overwrite a newer display.
        with self._lock:
            if self._closed or self._pending is None or req != self._pending:
                return g.hold('STALE_PRESENTATION_CALLBACK')
            self._pending = None
            if self._binding != req.binding or time.monotonic() >= self._deadline:
                self._display = g.hold('EXPIRED_OR_INACTIVE_REQUEST')
                return self._display
            try:
                decision = self._verify(req, raw)
            except ERRORS:
                decision = g.hold('INVALID_PRESENTATION')
            if time.monotonic() >= self._deadline:
                decision = g.hold('EXPIRED_PRESENTATION')
            self._display = decision
            return decision

    def _current(self):
        if self._closed or self._binding is None or time.monotonic() >= self._deadline:
            return g.hold('NO_CURRENT_PRESENTATION')
        return self._display

    def current(self):
        with self._lock:
            return self._current()

    def render(self):
        """Fixed trusted HTML snapshot at call time. Never use accept's old result."""
        with self._lock:
            d = self._current()
            parts = ['<!doctype html><html lang="en"><meta charset="utf-8"><title>VerifyOS presentation</title>',
                     '<main><h1>VerifyOS presentation</h1>',
                     '<p data-status="'+d.status+'">'+r.STATUS_LABELS[d.status]+'</p>']
            if self._binding is not None:
                parts.append('<p>Turn: <code>'+html.escape(self._binding.turn.turn_id)+'</code></p>')
                parts.append('<p>Question SHA-256: <code>'+html.escape(self._binding.turn.question_sha256)+'</code></p>')
            if d.status != g.HOLD:
                rows, branches = r.closed_view(d)
                parts.append('<table><thead><tr><th>Claim</th><th>Status</th><th>Value</th></tr></thead><tbody>')
                for row in rows:
                    value = '—' if row.status == g.HOLD else str(row.value)
                    parts.append('<tr><th>'+r.LABELS[row.claim_id]+'</th><td>'+row.status+'</td><td>'+html.escape(value)+'</td></tr>')
                parts.append('</tbody></table><h2>Retained interpretation branches</h2><ol>')
                for branch in branches:
                    parts.append('<li><code>'+branch.interpretation_id+'</code> — '+('Active' if branch.active else 'Inactive (retained)')+' — '+branch.status+'<ul>')
                    for ident in branch.required:
                        parts.append('<li>'+r.LABELS[ident]+(' (conditional)' if ident in branch.conditional else ' (common)')+'</li>')
                    parts.append('</ul></li>')
                parts.append('</ol>')
            parts.append('<p>Bounded local snapshot only; no currentness, historical execution, proof/action authority or ChatGPT interception asserted.</p></main></html>')
            return '\n'.join(parts).encode('utf-8')
