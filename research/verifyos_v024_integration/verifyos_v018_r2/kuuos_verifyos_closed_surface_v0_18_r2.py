"""Additive trusted display surface candidate; no ChatGPT interception.
Only the host can begin/receive evidence. WSGI exposes a read-only snapshot.
The model is not a Python caller or a principal with host process privileges.
"""
from __future__ import annotations

from dataclasses import dataclass
import html
import threading

if __package__:
    from . import kuuos_verifyos_display_gate_v0_18 as gate
else:
    import kuuos_verifyos_display_gate_v0_18 as gate

# From fixed v0.3 source blob 001d89ed1d9395c9d7a72595fe7e1a60716c4ecd.
CLAIM_PROFILE_BLOB = '001d89ed1d9395c9d7a72595fe7e1a60716c4ecd'
FIELDS = {
    'integrity_status': ('literal', 'PASS_INTEGRITY_ONLY'),
    'scope_status': ('literal', 'PASS_SCOPE_RECORDS_ONLY'),
    'integrity_exit_code': ('zero', None), 'scope_exit_code': ('zero', None),
    'snapshot_seq': ('nat', None), 'snapshot_tip': ('digest', None),
    'rule_count': ('nat', None), 'withdrawn_count': ('nat', None),
    'obstruction_count': ('nat', None), 'research_certificate_count': ('nat', None),
    'scope_candidate_count': ('nat', None), 'scope_held_count': ('nat', None),
    'scope_no_use_count': ('nat', None),
}
UNSUPPORTED = frozenset({'current_tip', 'external_truth', 'lean_proof',
                         'new_context_validity', 'action_permission'})
LABELS = {
    'integrity_status': 'Snapshot integrity gate', 'scope_status': 'Scope-record gate',
    'integrity_exit_code': 'Integrity exit code', 'scope_exit_code': 'Scope exit code',
    'snapshot_seq': 'Observed snapshot sequence', 'snapshot_tip': 'Observed snapshot tip',
    'rule_count': 'Rule count', 'withdrawn_count': 'Withdrawn count',
    'obstruction_count': 'Obstruction count', 'research_certificate_count': 'Research record count',
    'scope_candidate_count': 'Scope candidate count', 'scope_held_count': 'Scope held count',
    'scope_no_use_count': 'Scope no-use count', 'current_tip': 'Current tip',
    'external_truth': 'External truth', 'lean_proof': 'Lean proof authority',
    'new_context_validity': 'New-context validity', 'action_permission': 'Action permission',
}
STATUS_LABELS = {
    gate.HOLD: 'HOLD — no admitted display',
    gate.LIMITED: 'LIMITED — matched snapshot claims only',
    gate.ALL: 'ALL OBSERVED — matched active-view snapshot claims only',
}


@dataclass(frozen=True)
class Row:
    claim_id: str
    status: str
    value: int | str | None


@dataclass(frozen=True)
class Branch:
    interpretation_id: str
    active: bool
    status: str
    required: tuple[str, ...]
    conditional: tuple[str, ...]


def closed_view(decision):
    """Re-check display vocabulary and value types, not external truth."""
    gate.require(decision.status in (gate.ALL, gate.LIMITED), 'DISPLAY_STATUS')
    view = gate.strict(decision.view_json)
    gate.require(gate._classify(view) == decision.status, 'VIEW_STATUS')
    branches = view['branches']
    gate.require(all(type(x) is dict and type(x.get('active_in_revised_view')) is bool
                     for x in branches), 'BRANCH_TYPE')
    active = sum(x['active_in_revised_view'] for x in branches)
    gate.require(active > 0, 'NO_ACTIVE_BRANCH')
    gate.require(view['answer_status'].startswith('AMBIGUOUS_' if active > 1 else 'ACTIVE_VIEW_'),
                 'BRANCH_STATUS_MISMATCH')
    result = []
    for row in view['claims']:
        ident, status, value = row['claim_id'], row['status'], row['value']
        gate.require(ident in LABELS, 'UNKNOWN_CLAIM')
        if status == gate.HOLD:
            gate.require(value is None, 'HOLD_VALUE')
        else:
            gate.require(status == gate.OBSERVED and ident in FIELDS, 'UNSUPPORTED_OBSERVED')
            kind, literal = FIELDS[ident]
            ok = ((kind == 'literal' and type(value) is str and value == literal)
                  or (kind == 'zero' and type(value) is int and value == 0)
                  or (kind == 'nat' and type(value) is int and value >= 0)
                  or (kind == 'digest' and gate.hex64(value)))
            gate.require(ok, 'CLAIM_VALUE_TYPE')
        result.append(Row(ident, status, value))
    # From fixed v0.6 branch_rows, blob 523954c2105b251d02e2742dc48e243ba1227c15,
    # and v0.11 derive. Retain branch membership; recompute statuses from rows.
    by_id = {x.claim_id: x for x in result}
    def aggregate(ids):
        n = sum(by_id[x].status == gate.OBSERVED for x in ids)
        return 'ALL_OBSERVED' if n == len(ids) else 'PARTIAL' if n else 'HOLD'
    parsed, seen = [], set()
    for branch in branches:
        ident = branch.get('interpretation_id')
        ids, conditional = branch.get('required_claim_ids'), branch.get('conditional_claim_ids')
        gate.require(gate.hex64(ident) and ident not in seen, 'BRANCH_ID')
        seen.add(ident)
        gate.require(type(ids) is list and bool(ids) and all(type(x) is str and x in by_id for x in ids)
                     and len(set(ids)) == len(ids), 'BRANCH_REQUIRED')
        gate.require(type(conditional) is list and all(type(x) is str and x in ids for x in conditional)
                     and len(set(conditional)) == len(conditional), 'BRANCH_CONDITIONAL')
        status = aggregate(ids)
        gate.require(branch.get('status') == status, 'BRANCH_VALUE_STATUS')
        parsed.append(Branch(ident, branch['active_in_revised_view'], status, tuple(ids), tuple(conditional)))
    union = set().union(*(set(x.required) for x in parsed))
    common = set.intersection(*(set(x.required) for x in parsed))
    gate.require(union == set(by_id), 'BRANCH_UNION_COVERAGE')
    for branch in parsed:
        gate.require(branch.conditional == tuple(x for x in branch.required if x not in common), 'CONDITIONAL_MEMBERSHIP')
    active_union = set().union(*(set(x.required) for x in parsed if x.active))
    answer = aggregate(active_union)
    expected = answer if answer == gate.HOLD else ('AMBIGUOUS_' if active > 1 else 'ACTIVE_VIEW_') + answer
    original = aggregate(union)
    if len(parsed) > 1 and original != gate.HOLD:
        original = 'AMBIGUOUS_' + original
    gate.require(view['answer_status'] == expected and view['original_family_status'] == original, 'AGGREGATE_STATUS')
    return tuple(result), tuple(parsed)


class ClosedSurface:
    """One host-owned session. No model text, arbitrary markup or signing endpoint.

    Outer lock serializes begin, correlated receipt arrival and snapshot creation.
    A late callback must supply the host-retained challenge; it cannot consume the
    new challenge. It is not an authentication credential for an untrusted caller.
    """
    def __init__(self, public_key, *, ttl_seconds=1800):
        self._lock = threading.Lock()
        self._renderer = gate.TrustedRenderer(public_key, ttl_seconds=ttl_seconds)
        self._active = None

    def begin(self, question_bytes, request_bytes, context_bytes):
        with self._lock:
            self._active = self._renderer.begin(question_bytes, request_bytes, context_bytes)
            return self._active

    def receive(self, challenge, envelope):
        with self._lock:
            if self._active is None or challenge != self._active:
                return gate.hold('STALE_CALLBACK')
            result = self._renderer.consume(envelope)
            if result.status != gate.HOLD:
                try:
                    closed_view(result)
                except Exception:
                    # Clear old admitted state; do not leave a signed but invalid view.
                    self._active = None
                    return gate.hold('CLOSED_VOCABULARY_REJECTED')
            return result

    def _snapshot(self):
        # Caller holds outer lock. Return no model-origin text or arbitrary status.
        if self._active is None:
            return gate.HOLD, (), (), None
        decision = self._renderer.current(self._active)
        if decision.status == gate.HOLD:
            return gate.HOLD, (), (), self._active
        try:
            rows, branches = closed_view(decision)
            return decision.status, rows, branches, self._active
        except Exception:
            return gate.HOLD, (), (), self._active

    def render(self):
        with self._lock:
            status, rows, branches, challenge = self._snapshot()
            # Fixed HTML shell, fixed labels, typed values. No model prose even when
            # a valid envelope exists. HTML escapes text as defense in depth.
            lines = ['<!doctype html><html lang="en"><head><meta charset="utf-8">',
                     '<title>VerifyOS snapshot display</title></head><body>',
                     '<main><h1>VerifyOS snapshot display</h1>',
                     '<p id="verified-status" data-status="'+status+'">'+STATUS_LABELS[status]+'</p>',
                     '<p>Snapshot at response generation, not a current-state or historical-execution guarantee.</p>']
            if challenge is not None:
                lines.append('<p>Display challenge: <code>'+html.escape(challenge.nonce)+'</code></p>')
                lines.append('<p>Question SHA-256: <code>'+html.escape(challenge.question_sha256)+'</code></p>')
            if rows:
                lines.append('<table><thead><tr><th>Claim</th><th>Status</th><th>Value</th></tr></thead><tbody>')
                for row in rows:
                    val = '—' if row.status == gate.HOLD else str(row.value)
                    lines.append('<tr><th>'+LABELS[row.claim_id]+'</th><td>'+row.status+'</td><td>'+html.escape(val)+'</td></tr>')
                lines.append('</tbody></table>')
            if branches:
                lines.append('<h2>Retained interpretation branches</h2><ol>')
                for branch in branches:
                    lines.append('<li><code>'+html.escape(branch.interpretation_id)+'</code> — '+
                                 ('Active' if branch.active else 'Inactive (retained)')+' — '+branch.status+'<ul>')
                    for ident in branch.required:
                        lines.append('<li>'+LABELS[ident]+(' (conditional)' if ident in branch.conditional else ' (common)')+'</li>')
                    lines.append('</ul></li>')
                lines.append('</ol>')
            lines.append('<p>No proof authority, action authority, external truth, currentness, or ChatGPT interception asserted.</p></main></body></html>')
            return '\n'.join(lines).encode('utf-8')

    def __call__(self, environ, start_response):
        # Mount behind trusted per-user transport; this reference route provides
        # neither authentication nor an externally accessible mutation operation.
        if environ.get('REQUEST_METHOD') != 'GET':
            status, body = '405 Method Not Allowed', b'Method not allowed'
        elif environ.get('PATH_INFO') != '/verifyos' or environ.get('QUERY_STRING'):
            status, body = '404 Not Found', b'Not found'
        else:
            status, body = '200 OK', self.render()
        start_response(status, [('Content-Type','text/html; charset=utf-8'),
            ('Content-Length',str(len(body))), ('Cache-Control','no-store'),
            ('Content-Security-Policy',"default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'"),
            ('X-Content-Type-Options','nosniff'), ('X-Frame-Options','DENY')])
        return [body]
