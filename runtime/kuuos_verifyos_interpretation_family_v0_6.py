"""Bounded interpretation families; ambiguity is not evidence or permission."""
from __future__ import annotations
import argparse
from itertools import product
from math import prod
from pathlib import Path
import sys
from runtime import kuuos_verifyos_question_translation_v0_5 as t

b, p, c, q = t.b, t.p, t.c, t.q
SCHEMA = 'kuuos.verifyos.interpretation-family.v0.6'
FAMILY_SCHEMA = SCHEMA + '.candidate'
OK = 'FAMILY_CHECKED_BOUNDED_ONLY'
LIMIT = 32
AMBIGUOUS = {
    '検査結果': ('snapshot_integrity', 'full_audit'),
    '認証状況': ('scope_reviews', 'authority_limits'),
    '記録状況': ('rule_inventory', 'scope_reviews'),
    'tip': ('snapshot_integrity', 'current_state'),
}
BOUNDARY = {**t.BOUNDARY, 'open_language_interpretation_completeness_verified': False,
            'interpretation_selection_authorized': False}
ERRORS = t.ERRORS


def policy_digest():
    return b.sha(b.canonical({'schema': SCHEMA, 'ambiguities': AMBIGUOUS,
                              'predecessor_policy': t.policy_digest(), 'limit': LIMIT}))


def analyze(question):
    out = {'schema': SCHEMA, 'status': 'HOLD', 'question_sha256': b.sha(question) if type(question) is bytes else None,
           'policy_sha256': policy_digest(), 'trace': [], 'unresolved': [], 'family': None, **BOUNDARY}
    try:
        b.require(type(question) is bytes and 0 < len(question) <= 8192, 'QUESTION_BYTES')
        text = question.decode('utf-8')
        def span(start, end, kind, choices):
            row = {'start_byte': start, 'end_byte': end, 'kind': kind,
                   'span_sha256': b.sha(question[start:end]), 'choices': [list(x) for x in choices]}
            out['trace'].append(row)
            if not choices:
                out['unresolved'].append(row)
        prior = t.analyze(question)
        if prior['status'] == 'TRANSLATION_CANDIDATE':
            for row in prior['trace']:
                span(row['start_byte'], row['end_byte'], row['kind'], (row['topics'],))
        else:
            prefix = next((s for s in t.PREFIXES if text.startswith(s)), None)
            b.require(prefix is not None, 'UNREGISTERED_PREFIX')
            fresh = text.endswith(t.FRESH)
            core = text[:-len(t.FRESH)] if fresh else text
            suffix = next((s for s in t.SUFFIXES if core.endswith(s)), None)
            b.require(suffix is not None, 'UNREGISTERED_SUFFIX_OR_CONDITION')
            pos = len(prefix.encode()); span(0, pos, 'prefix', (t.PREFIXES[prefix],))
            seen, ambiguous = set(), False
            for i, word in enumerate(core[len(prefix):-len(suffix)].split('、')):
                if i:
                    end = pos + len('、'.encode()); span(pos, end, 'separator', ((),)); pos = end
                end = pos + len(word.encode())
                if word in seen:
                    span(pos, end, 'duplicate_clause', ())
                elif word in AMBIGUOUS:
                    ambiguous = True
                    span(pos, end, 'ambiguous_clause', tuple((x,) for x in AMBIGUOUS[word]))
                elif word in t.CLAUSES:
                    span(pos, end, 'clause', ((t.CLAUSES[word],),))
                else:
                    span(pos, end, 'unresolved', ())
                seen.add(word); pos = end
            end = pos + len(suffix.encode()); span(pos, end, 'request_suffix', ((),)); pos = end
            if fresh:
                span(pos, len(question), 'freshness_condition', (('current_state',),))
            if out['unresolved']:
                out['reason'] = 'UNRESOLVED_OR_DUPLICATE_CLAUSE'; return out
            b.require(ambiguous, 'NO_SUPPORTED_AMBIGUOUS_GRAMMAR')
        cursor = 0
        for row in out['trace']:
            b.require(row['start_byte'] == cursor and row['end_byte'] >= cursor, 'SPAN_COVERAGE')
            cursor = row['end_byte']
        b.require(cursor == len(question), 'SPAN_COVERAGE')
        dimensions = [range(len(row['choices'])) for row in out['trace']]
        if prod(map(len, dimensions)) > LIMIT:
            out['reason'] = 'FAMILY_LIMIT_EXCEEDED_NO_TRUNCATION'; return out
        branches = []
        for indices in product(*dimensions):
            topics = {topic for row, index in zip(out['trace'], indices) for topic in row['choices'][index]}
            typed = {'schema': q.QUESTION_SCHEMA, 'topics': [x for x in q.TOPICS if x in topics]}
            contract = q.compile_question(b.canonical(typed))
            witness = {'choices': list(indices), 'typed_question': typed, 'contract': contract}
            branches.append({'interpretation_id': b.sha(b.canonical(witness)), **witness})
        sets = [set(x['contract']['plan']['claim_ids']) for x in branches]
        common = set.intersection(*sets); union = set.union(*sets)
        family = {'schema': FAMILY_SCHEMA, 'question_sha256': out['question_sha256'],
                  'policy_sha256': out['policy_sha256'], 'trace_sha256': b.sha(b.canonical(out['trace'])),
                  'interpretations': branches, 'common_claim_ids': [x for x in q.ORDER if x in common],
                  'union_claim_ids': [x for x in q.ORDER if x in union]}
        out.update(status='FAMILY_CANDIDATE', reason=None, family=family)
    except ERRORS:
        out.update(reason='UNSUPPORTED_OR_MALFORMED_QUESTION', trace=[], unresolved=[])
        if type(question) is bytes and question:
            out['unresolved'] = [{'start_byte': 0, 'end_byte': len(question), 'kind': 'unresolved',
                                  'span_sha256': b.sha(question), 'choices': []}]
    return out


def check_family(question, candidate):
    result = analyze(question)
    if result['status'] == 'FAMILY_CANDIDATE':
        if type(candidate) is bytes and candidate == b.canonical(result['family']):
            result['status'] = OK
        else:
            result.update(status='HOLD', reason='INTERPRETATION_FAMILY_MISMATCH')
    return result


def preflight(question, candidate, request, context):
    result = check_family(question, candidate)
    if result['status'] == OK:
        try:
            p.context_check(context, request)
            b.require(context['question_sha256'] == result['question_sha256'], 'ORIGINAL_QUESTION_MISMATCH')
        except ERRORS:
            result.update(status='HOLD', reason='ORIGINAL_CONTEXT_MISMATCH')
    return result


def execute_question(snapshot, question, candidate, request, context, key):
    result = preflight(question, candidate, request, context)
    if result['status'] != OK:
        return None, None, result
    try:
        raw, admission = p.execute_and_admit(snapshot, request, context, key)
        return raw, admission, result
    except ERRORS:
        result.update(status='HOLD', reason='EXECUTION_UNAVAILABLE')
        return None, None, result


def branch_rows(family, rows):
    by_id = {r['claim_id']: r for r in rows}
    common = set(family['common_claim_ids'])
    result = []
    for branch in family['interpretations']:
        ids = branch['contract']['plan']['claim_ids']
        n = sum(by_id[x]['status'] == 'OBSERVED_IN_ADMITTED_RECEIPT' for x in ids)
        result.append({'interpretation_id': branch['interpretation_id'],
                       'status': 'ALL_OBSERVED' if n == len(ids) else 'PARTIAL' if n else 'HOLD',
                       'required_claim_ids': ids, 'conditional_claim_ids': [x for x in ids if x not in common]})
    return result


def hold(analysis, reason):
    family = analysis.get('family')
    rows = [] if family is None else [c.held(x, reason) for x in family['union_claim_ids']]
    return b.canonical({'schema': SCHEMA, 'status': 'HOLD', 'reason': reason, 'analysis': analysis,
                        'claims': rows, 'branches': [] if family is None else branch_rows(family, rows),
                        'selected_interpretation': None, **BOUNDARY})


def publish_question(question, candidate, raw, admission, request, context, key, prior_packet):
    analysis = preflight(question, candidate, request, context)
    if analysis['status'] != OK:
        return hold(analysis, analysis['reason'])
    try:
        family = analysis['family']
        plan = {'claim_ids': family['union_claim_ids']}
        packet = c.publish_claims(raw, admission, request, context, key, prior_packet, plan)
        source = p.strict(packet).get('publication')
        if source is None:
            return hold(analysis, 'ADMITTED_EVIDENCE_MISSING')
        rows = source['claims']
        b.require([r['claim_id'] for r in rows] == plan['claim_ids'], 'REQUIRED_CLAIM_COVERAGE')
        b.require(source['plan_sha256'] == b.sha(b.canonical(plan)), 'PLAN_BINDING')
        multiple = len(family['interpretations']) > 1
        status = source['status']
        if multiple and status != 'HOLD':
            status = 'AMBIGUOUS_' + status
        payload = {'schema': SCHEMA, 'status': status, 'scope': 'bounded_interpretation_family_only',
                   'analysis': analysis, 'analysis_sha256': b.sha(b.canonical(analysis)),
                   'context_sha256': b.sha(b.canonical(context)), 'claim_packet_sha256': b.sha(packet),
                   'claims': rows, 'branches': branch_rows(family, rows), 'ambiguity_unresolved': multiple,
                   'selected_interpretation': None, **BOUNDARY}
        return b.canonical({'publication': payload, 'tag': p.mac(key, b'interpretation-family-v0.6', payload)})
    except ERRORS:
        return hold(analysis, 'ADMITTED_EVIDENCE_INVALID')


def verified_display(packet, **kwargs):
    expected = publish_question(**kwargs)
    if packet != expected:
        return hold(check_family(kwargs.get('question'), kwargs.get('candidate')), 'PUBLICATION_MISMATCH'), 2
    return expected, 0 if p.strict(expected).get('publication', {}).get('status') == 'ALL_OBSERVED' else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('compile', 'check', 'issue', 'publish', 'display'))
    parser.add_argument('--question', required=True, type=Path)
    for name in ('candidate', 'request', 'context', 'key-file', 'evidence-dir', 'snapshot', 'prior-packet', 'packet'):
        parser.add_argument('--' + name, type=Path)
    a = parser.parse_args()
    question, candidate = t.read_optional(a.question), t.read_optional(a.candidate)
    analysis = analyze(question)
    try:
        if a.operation == 'compile':
            out, rc = b.canonical(analysis), 0 if analysis['status'] == 'FAMILY_CANDIDATE' else 2
        elif a.operation == 'check':
            analysis = check_family(question, candidate)
            out, rc = b.canonical(analysis), 0 if analysis['status'] == OK else 2
        else:
            request, context, key = t.parse_optional(a.request), t.parse_optional(a.context), t.read_optional(a.key_file)
            if a.operation == 'issue':
                analysis = preflight(question, candidate, request, context)
                if analysis['status'] != OK:
                    out, rc = hold(analysis, analysis['reason']), 2
                else:
                    b.require(a.snapshot is not None and a.evidence_dir is not None, 'PRIVATE_PATHS_REQUIRED')
                    a.evidence_dir.mkdir(mode=0o700, parents=False, exist_ok=False)
                    raw, admission, analysis = execute_question(a.snapshot, question, candidate, request, context, key)
                    if raw is not None: p.write_new(a.evidence_dir / 'bundle.json', raw)
                    if admission is not None:
                        p.write_new(a.evidence_dir / 'admission.json', admission)
                        out, rc = b.canonical({'schema': SCHEMA, 'status': 'ADMISSION_CREATED_NOT_PUBLISHED',
                                               'analysis_sha256': b.sha(b.canonical(analysis)), **BOUNDARY}), 0
                    else:
                        out, rc = hold(analysis, 'ADMISSION_UNAVAILABLE'), 2
            else:
                raw = t.read_optional(a.evidence_dir / 'bundle.json') if a.evidence_dir else None
                admission = t.read_optional(a.evidence_dir / 'admission.json') if a.evidence_dir else None
                args = dict(question=question, candidate=candidate, raw=raw, admission=admission, request=request,
                            context=context, key=key, prior_packet=t.read_optional(a.prior_packet))
                if a.operation == 'display':
                    out, rc = verified_display(t.read_optional(a.packet), **args)
                else:
                    out = publish_question(**args)
                    rc = 0 if p.strict(out).get('publication', {}).get('status') == 'ALL_OBSERVED' else 2
        sys.stdout.buffer.write(out)
        return rc
    except ERRORS:
        sys.stdout.buffer.write(hold(analysis, 'PRIVATE_INPUT_OR_EXECUTION_UNAVAILABLE'))
        return 2


if __name__ == '__main__':
    sys.exit(main())
