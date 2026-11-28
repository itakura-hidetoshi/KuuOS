"""Append-only corrections across contexts; no retroactive change of evidence."""
from __future__ import annotations
from runtime import kuuos_verifyos_interpretation_refinement_v0_7 as r

b, p, c, q, f = r.b, r.p, r.c, r.q, r.f
SCHEMA = 'kuuos.verifyos.interpretation-revision.v0.8'
LOG = SCHEMA + '.log'
EVENT = SCHEMA + '.event'
OK = 'REVISION_CHECKED_BOUNDED_ONLY'
BOUNDARY = {**r.BOUNDARY, 'historical_evidence_rebound': False,
            'persistent_append_atomicity_verified': False}
ERRORS = r.ERRORS
LIMIT = 32


def digest(value):
    return b.sha(b.canonical(value))


def genesis(seed, context):
    return digest({'schema': LOG, 'family_sha256': digest(seed['analysis']['family']),
                   'confirmation_log_sha256': seed['log_sha256'], 'context_sha256': digest(context)})


def empty_log(seed, context):
    b.require(seed['status'] == 'REFINEMENT_CHECKED_BOUNDED_ONLY', 'INVALID_SEED')
    return {'schema': LOG, 'genesis': genesis(seed, context), 'events': []}


def matching(family, effective):
    return [x for x in family['interpretations']
            if all(x['choices'][i] == item['choice'] for i, item in effective.items())]


def replay(question, candidate, base_request, base_context, base_log, base_anchor,
           revision_log, revision_anchor, current_request, current_context):
    seed = r.replay(question, candidate, base_request, base_context, base_log, base_anchor)
    family = seed['analysis'].get('family')
    original = [] if family is None else family['interpretations']
    out = {'schema': SCHEMA, 'status': 'HOLD', 'seed': seed, 'verified_revisions': [],
           'rejected_event': None, 'active_ids': [x['interpretation_id'] for x in original],
           'effective_confirmations': [], 'revision_log_sha256': None, **BOUNDARY}
    try:
        b.require(seed['status'] == 'REFINEMENT_CHECKED_BOUNDED_ONLY', 'INVALID_SEED')
        b.require(type(revision_log) is bytes and b.hex64(revision_anchor) and b.sha(revision_log) == revision_anchor, 'REVISION_ANCHOR_MISMATCH')
        log = p.strict(revision_log)
        b.require(type(log) is dict and set(log) == {'schema','genesis','events'}, 'LOG_SCHEMA')
        b.require(log['schema'] == LOG and log['genesis'] == genesis(seed, base_context), 'LOG_GENESIS')
        events = log['events']
        b.require(type(events) is list and len(events) <= LIMIT, 'REVISION_LIMIT')
        out['revision_log_sha256'] = revision_anchor
        effective = {v['event']['span_index']: {'choice':v['event']['choice_index'], 'event_sha256':v['event_sha256']}
                     for v in seed['verified_events']}
        seen_ids = {v['event']['event_id'] for v in seed['verified_events']}
        turns, challenges = {base_context['turn_id']}, {base_context['challenge']}
        last_request, last_context = base_request, base_context
        parent = log['genesis']

        def refresh():
            active = matching(family, effective)
            out['active_ids'] = [x['interpretation_id'] for x in active]
            out['effective_confirmations'] = [{'span_index':i, **effective[i]} for i in sorted(effective)]
            return active

        refresh()
        for seq, ev in enumerate(events, 1):
            out['rejected_event'] = {'sequence':seq, 'sha256':digest(ev)}
            b.require(type(ev) is dict and set(ev) == {'schema','sequence','parent_sha256','event_id','source','operation',
                      'span_index','span_sha256','choice_index','target_event_sha256','next_request','next_context'}, 'EVENT_SCHEMA')
            b.require(ev['schema'] == EVENT and type(ev['sequence']) is int and ev['sequence'] == seq and ev['parent_sha256'] == parent, 'EVENT_CHAIN')
            b.require(ev['source'] == 'host_captured_explicit_user_revision' and b.hex64(ev['event_id']) and ev['event_id'] not in seen_ids, 'REVISION_CAPTURE_REQUIRED')
            request, context = ev['next_request'], ev['next_context']
            p.context_check(context, request)
            b.require(context['question_sha256'] == b.sha(question), 'QUESTION_CHANGED')
            b.require(context['turn_id'] not in turns and context['challenge'] not in challenges, 'FRESH_CONTEXT_REQUIRED')
            i, j, op = ev['span_index'], ev['choice_index'], ev['operation']
            trace = seed['analysis']['trace']
            b.require(type(i) is int and 0 <= i < len(trace), 'SPAN_INDEX')
            span = trace[i]
            b.require(span['kind'] == 'ambiguous_clause' and ev['span_sha256'] == span['span_sha256'], 'SPAN_BINDING')
            previous = effective.get(i)
            target = ev['target_event_sha256']
            b.require(op in ('confirm','replace','retract'), 'OPERATION')
            if op == 'confirm':
                b.require(previous is None and target is None, 'CONFIRM_REQUIRES_OPEN_SPAN')
            else:
                b.require(previous is not None and target == previous['event_sha256'], 'STALE_REVISION_TARGET')
            if op == 'retract':
                b.require(j is None, 'RETRACTION_HAS_CHOICE')
            else:
                b.require(type(j) is int and 0 <= j < len(span['choices']), 'CHOICE_INDEX')
                b.require(op != 'replace' or j != previous['choice'], 'REPLACEMENT_NO_CHANGE')
            before = set(out['active_ids']); event_digest = digest(ev)
            if op == 'retract':
                del effective[i]
            else:
                effective[i] = {'choice':j,'event_sha256':event_digest}
            active = refresh(); after = set(out['active_ids'])
            b.require(bool(active), 'EMPTY_ACTIVE_VIEW')
            ids = [x['interpretation_id'] for x in original]
            out['verified_revisions'].append({'event':ev, 'event_sha256':event_digest,
                'prior_confirmation':previous, 'removed_ids':[x for x in ids if x in before-after],
                'restored_ids':[x for x in ids if x in after-before], 'reason':'VIEW_REVISION_NOT_REFUTATION'})
            seen_ids.add(ev['event_id']); turns.add(context['turn_id']); challenges.add(context['challenge'])
            parent = event_digest; last_request, last_context = request, context
            out['rejected_event'] = None
        p.context_check(current_context, current_request)
        b.require(b.canonical(current_request) == b.canonical(last_request) and b.canonical(current_context) == b.canonical(last_context), 'CURRENT_CONTEXT_MISMATCH')
        sets = [set(x['contract']['plan']['claim_ids']) for x in matching(family,effective)]
        out.update(status=OK, reason=None, current_context_sha256=digest(current_context),
                   active_union_claim_ids=[x for x in q.ORDER if x in set.union(*sets)],
                   active_common_claim_ids=[x for x in q.ORDER if x in set.intersection(*sets)])
    except ERRORS as exc:
        out['reason'] = str(exc) if type(exc) is ValueError else 'REVISION_INPUT_INVALID'
    return out


def hold(result, reason):
    family = result['seed']['analysis'].get('family')
    rows = [] if family is None else [c.held(x,reason) for x in family['union_claim_ids']]
    return b.canonical({'schema':SCHEMA,'status':'HOLD','reason':reason,'revision':result,
                        'claims':rows,'branches':[] if family is None else f.branch_rows(family,rows), **BOUNDARY})


def publish_question(raw, admission, key, prior_packet, **inputs):
    result = replay(**inputs)
    if result['status'] != OK:
        return hold(result,result['reason'])
    try:
        packet = f.publish_question(inputs['question'],inputs['candidate'],raw,admission,
                                    inputs['current_request'],inputs['current_context'],key,prior_packet)
        source = p.strict(packet).get('publication')
        if source is None:
            return hold(result,'CURRENT_CONTEXT_EVIDENCE_MISSING')
        family = result['seed']['analysis']['family']
        b.require(source['analysis']['family'] == family, 'FAMILY_MISMATCH')
        rows = source['claims']; branches = source['branches']
        b.require([x['claim_id'] for x in rows] == family['union_claim_ids'], 'ORIGINAL_CLAIMS_MISSING')
        b.require([x['interpretation_id'] for x in branches] == [x['interpretation_id'] for x in family['interpretations']], 'ORIGINAL_BRANCHES_MISSING')
        active = set(result['active_ids']); required = result['active_union_claim_ids']
        by_id = {x['claim_id']:x for x in rows}
        n = sum(by_id[x]['status'] == 'OBSERVED_IN_ADMITTED_RECEIPT' for x in required)
        status = 'HOLD' if not n else ('AMBIGUOUS_' if len(active)>1 else 'ACTIVE_VIEW_') + ('ALL_OBSERVED' if n==len(required) else 'PARTIAL')
        payload = {'schema':SCHEMA,'status':status,'scope':'revised_bounded_view_only',
                   'revision':result,'revision_sha256':digest(result),'current_packet_sha256':b.sha(packet),
                   'original_family_status':source['status'],'claims':rows,
                   'branches':[{**x,'active_in_revised_view':x['interpretation_id'] in active} for x in branches],
                   'selected_interpretation':None, **BOUNDARY}
        return b.canonical({'publication':payload,'tag':p.mac(key,b'interpretation-revision-v0.8',payload)})
    except ERRORS:
        return hold(result,'CURRENT_CONTEXT_EVIDENCE_INVALID')


def verified_display(packet, raw, admission, key, prior_packet, **inputs):
    expected = publish_question(raw,admission,key,prior_packet,**inputs)
    if packet != expected:
        return hold(replay(**inputs),'PUBLICATION_MISMATCH'),2
    return expected, 0 if p.strict(expected).get('publication',{}).get('status') == 'ACTIVE_VIEW_ALL_OBSERVED' else 2
