"""Append-only clarification of a bounded interpretation family, not a proof of intent."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from runtime import kuuos_verifyos_interpretation_family_v0_6 as f

b, p, c, q, t = f.b, f.p, f.c, f.q, f.t
SCHEMA = 'kuuos.verifyos.interpretation-refinement.v0.7'
LOG_SCHEMA = SCHEMA + '.log'
EVENT_SCHEMA = SCHEMA + '.confirmation'
LIMIT = 32
BOUNDARY = {**f.BOUNDARY, 'human_identity_authenticated': False,
            'excluded_interpretations_refuted': False, 'general_intent_verified': False}
ERRORS = f.ERRORS


def genesis(family, context):
    return b.sha(b.canonical({'schema': LOG_SCHEMA, 'family_sha256': b.sha(b.canonical(family)),
                              'context_sha256': b.sha(b.canonical(context))}))


def empty_log(family, context):
    return {'schema': LOG_SCHEMA, 'genesis': genesis(family, context), 'events': []}


def replay(question, candidate, request, context, log_bytes, trusted_log_sha256):
    """Anchor and confirmation capture must be supplied by a trusted host, not the model."""
    analysis = f.preflight(question, candidate, request, context)
    family = analysis.get('family')
    original = [] if family is None else family['interpretations']
    active = list(original)
    result = {'schema': SCHEMA, 'status': 'HOLD', 'analysis': analysis,
              'log_sha256': None, 'verified_events': [], 'rejected_event': None,
              'active_ids': [x['interpretation_id'] for x in active], 'excluded': [], **BOUNDARY}
    try:
        b.require(analysis['status'] == f.OK, 'ORIGINAL_FAMILY_NOT_VERIFIED')
        b.require(type(log_bytes) is bytes and b.hex64(trusted_log_sha256), 'LOG_ANCHOR_MISSING')
        b.require(b.sha(log_bytes) == trusted_log_sha256, 'LOG_ANCHOR_MISMATCH')
        log = p.strict(log_bytes)
        b.require(type(log) is dict and set(log) == {'schema', 'genesis', 'events'}, 'LOG_SCHEMA')
        b.require(log['schema'] == LOG_SCHEMA and log['genesis'] == genesis(family, context), 'LOG_CONTEXT_MISMATCH')
        events = log['events']
        b.require(type(events) is list and len(events) <= LIMIT, 'EVENT_LIMIT')
        result['log_sha256'] = trusted_log_sha256
        parent = log['genesis']; seen = set(); spans = set()
        for seq, ev in enumerate(events, 1):
            result['rejected_event'] = {'sequence': seq, 'sha256': b.sha(b.canonical(ev))}
            b.require(type(ev) is dict and set(ev) == {'schema', 'sequence', 'parent_sha256', 'event_id', 'source', 'span_index', 'choice_index', 'span_sha256'}, 'EVENT_SCHEMA')
            b.require(ev['schema'] == EVENT_SCHEMA and type(ev['sequence']) is int and ev['sequence'] == seq and ev['parent_sha256'] == parent, 'EVENT_CHAIN')
            b.require(ev['source'] == 'host_captured_explicit_user_confirmation' and b.hex64(ev['event_id']), 'CONFIRMATION_REQUIRED')
            b.require(ev['event_id'] not in seen, 'EVENT_REPLAY')
            i, j = ev['span_index'], ev['choice_index']
            b.require(type(i) is int and 0 <= i < len(analysis['trace']), 'SPAN_INDEX')
            span = analysis['trace'][i]
            b.require(span['kind'] == 'ambiguous_clause' and ev['span_sha256'] == span['span_sha256'], 'SPAN_BINDING')
            b.require(type(j) is int and 0 <= j < len(span['choices']), 'CHOICE_INDEX')
            b.require(i not in spans, 'REPEATED_OR_CONFLICTING_CONFIRMATION_NEW_CONTEXT_REQUIRED')
            survivors = [x for x in active if x['choices'][i] == j]
            b.require(bool(survivors), 'EMPTY_REFINEMENT')
            digest = b.sha(b.canonical(ev))
            excluded = [{'interpretation_id': x['interpretation_id'], 'event_sha256': digest,
                         'sequence': seq, 'reason': 'EXCLUDED_IN_CONFIRMED_VIEW_ONLY_NOT_REFUTED'}
                        for x in active if x['choices'][i] != j]
            result['excluded'].extend(excluded)
            result['verified_events'].append({'event': ev, 'event_sha256': digest})
            active = survivors; parent = digest; seen.add(ev['event_id']); spans.add(i)
            result['active_ids'] = [x['interpretation_id'] for x in active]
            result['rejected_event'] = None
        sets = [set(x['contract']['plan']['claim_ids']) for x in active]
        result.update(status='REFINEMENT_CHECKED_BOUNDED_ONLY', reason=None,
                      active_common_claim_ids=[x for x in q.ORDER if x in set.intersection(*sets)],
                      active_union_claim_ids=[x for x in q.ORDER if x in set.union(*sets)])
    except ERRORS as exc:
        # A valid prefix is recorded, but never used to publish success for an invalid log.
        result.update(reason=str(exc) if type(exc) is ValueError else 'REFINEMENT_INPUT_INVALID')
    return result


def hold(refinement, reason):
    family = refinement['analysis'].get('family')
    rows = [] if family is None else [c.held(x, reason) for x in family['union_claim_ids']]
    return b.canonical({'schema': SCHEMA, 'status': 'HOLD', 'reason': reason, 'refinement': refinement,
                        'claims': rows, 'branches': [] if family is None else f.branch_rows(family, rows), **BOUNDARY})


def publish_question(question, candidate, request, context, log_bytes, trusted_log_sha256,
                     raw, admission, key, prior_packet):
    refinement = replay(question, candidate, request, context, log_bytes, trusted_log_sha256)
    if refinement['status'] != 'REFINEMENT_CHECKED_BOUNDED_ONLY':
        return hold(refinement, refinement['reason'])
    try:
        packet = f.publish_question(question, candidate, raw, admission, request, context, key, prior_packet)
        source = p.strict(packet).get('publication')
        if source is None:
            return hold(refinement, 'ADMITTED_EVIDENCE_MISSING')
        family = refinement['analysis']['family']
        b.require(source['analysis']['family'] == family, 'ORIGINAL_FAMILY_MISMATCH')
        rows = source['claims']; branches = source['branches']
        b.require([r['claim_id'] for r in rows] == family['union_claim_ids'], 'ORIGINAL_CLAIMS_MISSING')
        b.require([r['interpretation_id'] for r in branches] == [r['interpretation_id'] for r in family['interpretations']], 'ORIGINAL_BRANCHES_MISSING')
        active = set(refinement['active_ids'])
        by_id = {r['claim_id']: r for r in rows}
        required = refinement['active_union_claim_ids']
        n = sum(by_id[x]['status'] == 'OBSERVED_IN_ADMITTED_RECEIPT' for x in required)
        status = 'HOLD' if not n else 'ALL_OBSERVED' if n == len(required) else 'PARTIAL'
        status = ('AMBIGUOUS_' if len(active) > 1 else 'ACTIVE_VIEW_') + status if status != 'HOLD' else status
        payload = {'schema': SCHEMA, 'status': status, 'scope': 'confirmed_bounded_view_only',
                   'original_family_status': source['status'], 'refinement': refinement,
                   'refinement_sha256': b.sha(b.canonical(refinement)), 'original_packet_sha256': b.sha(packet),
                   'claims': rows, 'branches': [{**r, 'active_in_confirmed_view': r['interpretation_id'] in active} for r in branches],
                   'selected_interpretation': None, **BOUNDARY}
        return b.canonical({'publication': payload, 'tag': p.mac(key, b'interpretation-refinement-v0.7', payload)})
    except ERRORS:
        return hold(refinement, 'ADMITTED_EVIDENCE_INVALID')


def verified_display(packet, **kwargs):
    expected = publish_question(**kwargs)
    if packet != expected:
        r = replay(*(kwargs[k] for k in ('question','candidate','request','context','log_bytes','trusted_log_sha256')))
        return hold(r, 'PUBLICATION_MISMATCH'), 2
    return expected, 0 if p.strict(expected).get('publication', {}).get('status') == 'ACTIVE_VIEW_ALL_OBSERVED' else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('replay', 'publish', 'display'))
    for name in ('question', 'candidate', 'request', 'context', 'log'):
        parser.add_argument('--' + name, required=True, type=Path)
    parser.add_argument('--trusted-log-sha256', required=True)
    for name in ('key-file', 'evidence-dir', 'prior-packet', 'packet'):
        parser.add_argument('--' + name, type=Path)
    a = parser.parse_args()
    args = dict(question=t.read_optional(a.question), candidate=t.read_optional(a.candidate),
                request=t.parse_optional(a.request), context=t.parse_optional(a.context),
                log_bytes=t.read_optional(a.log), trusted_log_sha256=a.trusted_log_sha256)
    if a.operation == 'replay':
        result = replay(**args); out = b.canonical(result)
        rc = 0 if result['status'] == 'REFINEMENT_CHECKED_BOUNDED_ONLY' else 2
    else:
        args.update(raw=t.read_optional(a.evidence_dir / 'bundle.json') if a.evidence_dir else None,
                    admission=t.read_optional(a.evidence_dir / 'admission.json') if a.evidence_dir else None,
                    key=t.read_optional(a.key_file), prior_packet=t.read_optional(a.prior_packet))
        if a.operation == 'display': out, rc = verified_display(t.read_optional(a.packet), **args)
        else:
            out = publish_question(**args)
            rc = 0 if p.strict(out).get('publication', {}).get('status') == 'ACTIVE_VIEW_ALL_OBSERVED' else 2
    sys.stdout.buffer.write(out); return rc


if __name__ == '__main__':
    sys.exit(main())
