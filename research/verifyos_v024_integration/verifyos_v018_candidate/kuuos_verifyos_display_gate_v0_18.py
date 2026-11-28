"""v0.18 candidate: trusted display gate, not a ChatGPT interception mechanism.

The verifier host and renderer must be outside the model's authority. The host
selects v0.17 inputs and owns the private key; the renderer owns the challenge,
trusted public key, clock, and status UI. No general certification is implied.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
from pathlib import Path
import re
import secrets
import threading
import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey,
)

SCHEMA = 'kuuos.verifyos.display-gate.v0.18.candidate'
DOMAIN = b'KuuOS/VerifyOS/display-gate/v0.18/candidate\0'
PREDECESSOR_HEAD = 'd1df31cba81423868a21bda9a952b89586b8b87d'
PREDECESSOR_BLOB = '0ad46d751c7096e0efb550f47c3bbc99d917eff0'
MATCH = 'LEAN_EXECUTED_EGRESS_MATCHED_ONLY'
OBSERVED = 'OBSERVED_IN_ADMITTED_RECEIPT'
ALL = 'MATCHED_ALL_OBSERVED_ONLY'
LIMITED = 'MATCHED_LIMITED_ONLY'
HOLD = 'HOLD'
MAX_BYTES = 1_048_576
BOUNDARY = {'proof_authority': False, 'action_authority': False,
            'external_truth_verified': False, 'external_currentness_verified': False,
            'chatgpt_interception_verified': False}


def sha(data: bytes) -> str:
    if type(data) is not bytes:
        raise ValueError('bytes required')
    return hashlib.sha256(data).hexdigest()


def canonical(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=True, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('ascii')


def require(condition, reason='INVALID'):
    if not condition:
        raise ValueError(reason)


def strict(raw: bytes):
    require(type(raw) is bytes and len(raw) <= MAX_BYTES, 'SIZE_OR_TYPE')
    def pairs(items):
        result = {}
        for k, v in items:
            require(k not in result, 'DUPLICATE_KEY')
            result[k] = v
        return result
    def bad(_):
        raise ValueError('NONFINITE_NUMBER')
    obj = json.loads(raw.decode('utf-8', errors='strict'), object_pairs_hook=pairs,
                     parse_constant=bad)
    require(canonical(obj) == raw, 'NONCANONICAL')
    return obj


def hex64(value):
    return type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None


@dataclass(frozen=True)
class Challenge:
    nonce: str
    question_sha256: str
    request_sha256: str
    context_sha256: str

    def validate(self):
        require(all(hex64(x) for x in asdict(self).values()), 'CHALLENGE_FORMAT')


@dataclass(frozen=True)
class DisplayDecision:
    # The UI uses this trusted status field only, never the model's prose.
    status: str
    reason: str
    view_json: bytes | None = None


def hold(reason):
    return DisplayDecision(HOLD, reason)


def _classify(view):
    require(type(view) is dict and set(view) == {
        'answer_status', 'original_family_status', 'claims', 'branches',
        'selected_interpretation'}, 'VIEW_SCHEMA')
    rows = view['claims']
    require(type(rows) is list and bool(rows), 'EMPTY_CLAIMS')
    require(type(view['branches']) is list and bool(view['branches']), 'BRANCHES')
    require(view['selected_interpretation'] is None, 'UNEXPECTED_SELECTION')
    ids = set()
    for row in rows:
        require(type(row) is dict and type(row.get('claim_id')) is str
                and row['claim_id'] not in ids, 'CLAIM_ID')
        ids.add(row['claim_id'])
        require('value' in row and row.get('status') in (OBSERVED, HOLD), 'CLAIM_STATUS')
        require(row['value'] is None if row['status'] == HOLD else row['value'] is not None,
                'CLAIM_VALUE')
    if view['answer_status'] == HOLD or not any(row['status'] == OBSERVED for row in rows):
        return HOLD
    require(view['answer_status'] in ('ACTIVE_VIEW_ALL_OBSERVED', 'ACTIVE_VIEW_PARTIAL',
                                     'AMBIGUOUS_ALL_OBSERVED', 'AMBIGUOUS_PARTIAL'), 'ANSWER_STATUS')
    # Tighten-only: do not promote even a single active view if any retained
    # row (including inactive branches) is HOLD. No ambiguous view gets ALL.
    if view['answer_status'] == 'ACTIVE_VIEW_ALL_OBSERVED' and all(
        row['status'] == OBSERVED for row in rows
    ):
        require(sum(type(x) is dict and x.get('active_in_revised_view') is True
                    for x in view['branches']) == 1, 'ACTIVE_VIEW_COUNT')
        return ALL
    return LIMITED


def _run_v017(snapshot, lean, question_bytes, challenge, pair_inputs):
    # Fixed host-selected module, no model-supplied verifier/packet/callback.
    from runtime import kuuos_verifyos_lean_egress_v0_17 as g
    source = Path(g.__file__).read_bytes()
    git_blob = hashlib.sha1(b'blob ' + str(len(source)).encode() + b'\0' + source).hexdigest()
    require(git_blob == PREDECESSOR_BLOB, 'PREDECESSOR_SOURCE_MISMATCH')
    require(sha(question_bytes) == challenge.question_sha256, 'QUESTION_MISMATCH')
    require(sha(g.b.canonical(pair_inputs['request'])) == challenge.request_sha256
            and sha(g.b.canonical(pair_inputs['context'])) == challenge.context_sha256,
            'HOST_CONTEXT_MISMATCH')
    require(pair_inputs['context']['question_sha256'] == challenge.question_sha256
            and pair_inputs['context']['request_sha256'] == challenge.request_sha256
            and pair_inputs['seed']['question'] == question_bytes, 'QUESTION_CONTRACT_MISMATCH')
    # The trusted transport must select the actual user question and associated context.
    # This wrapper does not prove natural-language contract completeness.
    packet = g.publication(snapshot, lean, **pair_inputs)
    result = g.p.strict(packet)
    require(result.get('status') == g.MATCH == MATCH, 'V017_NOT_MATCHED')
    displayed, rc = g.verified_display(packet, snapshot, lean, **pair_inputs)
    require(type(displayed) is bytes and displayed == packet, 'V017_REPLAY_MISMATCH')
    require(rc == (0 if result['answer_status'] == 'ACTIVE_VIEW_ALL_OBSERVED' else 2),
            'V017_REPLAY_EXIT')
    execution = result['execution']
    require(type(execution['exit_code']) is int and execution['exit_code'] == 0,
            'V017_EXECUTION_EXIT')
    require(result['context_sha256'] == execution['context_sha256'] == challenge.context_sha256
            and execution['request_sha256'] == challenge.request_sha256,
            'V017_EXECUTION_BINDING')
    require(all(result.get(k) is False for k in g.BOUNDARY), 'V017_BOUNDARY')
    return packet, {k: result[k] for k in ('answer_status', 'original_family_status',
                                           'claims', 'branches', 'selected_interpretation')}


class TrustedSigner:
    """Run only in the host process, not as a model-callable arbitrary signing service."""
    def __init__(self, private_key: Ed25519PrivateKey):
        require(isinstance(private_key, Ed25519PrivateKey), 'SIGNER_KEY')
        self._key = private_key

    def issue(self, challenge: Challenge, *, snapshot, lean: Path, question_bytes: bytes,
              pair_inputs: dict) -> bytes | None:
        # The production caller must resolve inputs from authenticated host state;
        # pair_inputs is NOT an untrusted request body or model-controlled argument.
        try:
            require(type(challenge) is Challenge, 'CHALLENGE_TYPE')
            challenge.validate()
            packet, view = _run_v017(snapshot, lean, question_bytes, challenge, pair_inputs)
            status = _classify(view)
            require(status != HOLD, 'V017_HOLD')
            payload = {'schema': SCHEMA, 'challenge': asdict(challenge),
                       'predecessor_head': PREDECESSOR_HEAD, 'packet_sha256': sha(packet),
                       'view': view, 'status': status, 'boundary': BOUNDARY.copy()}
            sig = self._key.sign(DOMAIN + canonical(payload))
            envelope = canonical({'payload': payload, 'signature_hex': sig.hex()})
            require(len(envelope) <= MAX_BYTES, 'SIZE')
            return envelope
        except Exception:
            # Do not publish exception messages, raw receipt, private key or a cached pass.
            return None


class TrustedRenderer:
    """One outstanding challenge per renderer; process-local, not a durable replay log."""
    def __init__(self, public_key: Ed25519PublicKey, *, ttl_seconds=1800):
        require(isinstance(public_key, Ed25519PublicKey), 'PINNED_PUBLIC_KEY')
        require(type(ttl_seconds) is int and 1 <= ttl_seconds <= 1800, 'TTL')
        self._key = public_key
        self._ttl = ttl_seconds
        self._lock = threading.Lock()
        self._pending: tuple[Challenge, float] | None = None
        self._active: tuple[Challenge, float] | None = None
        self._display = hold('NO_PENDING_CHALLENGE')

    def begin(self, question_bytes: bytes, request_bytes: bytes, context_bytes: bytes) -> Challenge:
        # request/context bytes must be canonical v0.17 inputs from trusted host state.
        ch = Challenge(secrets.token_hex(32), sha(question_bytes), sha(request_bytes), sha(context_bytes))
        with self._lock:
            self._active = self._pending = (ch, time.monotonic() + self._ttl)
            self._display = hold('AWAITING_EVIDENCE')
        return ch

    def current(self, challenge: Challenge) -> DisplayDecision:
        # UI must read this state for the active turn, not cache consume's return.
        with self._lock:
            if self._active is None or self._active[0] != challenge:
                return hold('STALE_TURN')
            if time.monotonic() >= self._active[1]:
                return hold('EXPIRED_CHALLENGE')
            return self._display

    def consume(self, envelope: bytes | None) -> DisplayDecision:
        # Consume first, atomically. Invalid attempts also consume the challenge.
        # A caller must not forward arbitrary untrusted network traffic here.
        with self._lock:
            pending, self._pending = self._pending, None
            now = time.monotonic()
        if pending is None:
            return hold('NO_PENDING_CHALLENGE')
        challenge, expires = pending
        if now >= expires:
            return hold('EXPIRED_CHALLENGE')
        decision = self._verify_envelope(envelope, challenge)
        with self._lock:
            if self._active is None or self._active[0] != challenge:
                return hold('STALE_TURN')
            if time.monotonic() >= expires:
                self._display = hold('EXPIRED_CHALLENGE')
            else:
                self._display = decision
            return self._display

    def _verify_envelope(self, envelope, challenge):
        try:
            obj = strict(envelope)
            require(type(obj) is dict and set(obj) == {'payload', 'signature_hex'}, 'ENVELOPE_SCHEMA')
            sig = obj['signature_hex']
            require(type(sig) is str and re.fullmatch('[0-9a-f]{128}', sig), 'SIGNATURE_FORMAT')
            payload = obj['payload']
            self._key.verify(bytes.fromhex(sig), DOMAIN + canonical(payload))
            require(type(payload) is dict and set(payload) == {'schema', 'challenge', 'predecessor_head',
                       'packet_sha256', 'view', 'status', 'boundary'}, 'PAYLOAD_SCHEMA')
            require(payload['schema'] == SCHEMA and payload['predecessor_head'] == PREDECESSOR_HEAD,
                    'PROFILE_MISMATCH')
            require(payload['challenge'] == asdict(challenge), 'CHALLENGE_MISMATCH')
            require(hex64(payload['packet_sha256']), 'PACKET_DIGEST')
            require(canonical(payload['boundary']) == canonical(BOUNDARY), 'AUTHORITY_BOUNDARY')
            status = _classify(payload['view'])
            require(status == payload['status'] and status != HOLD, 'STATUS_MISMATCH')
            # Data only. The host UI must use safe text rendering (no HTML/Markdown interpretation)
            # and keep its status indicator outside all model-controlled output.
            return DisplayDecision(status, '', canonical(payload['view']))
        except (ValueError, TypeError, KeyError, AttributeError, UnicodeError,
                OverflowError, RecursionError, InvalidSignature):
            return hold('INVALID_OR_UNMATCHED_ENVELOPE')

    def untrusted_model_output(self, text: str) -> DisplayDecision:
        # Model text can never promote certification. This method does not
        # render the text; the trusted UI may show it in an explicitly unverified area.
        return hold('MODEL_TEXT_NOT_EVIDENCE')
