"""Bounded Japanese question translation; retain every byte or HOLD before execution."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from runtime import kuuos_verifyos_question_claim_contract_v0_4 as q

b, p, c = q.b, q.p, q.claims
SCHEMA = 'kuuos.verifyos.question-translation.v0.5'
BOUNDARY = {**q.BOUNDARY, 'general_semantic_equivalence_verified': False}
PREFIXES = {'取得済み台帳について、': (), '空OSの現行継承台帳について、': ('current_state',)}
CLAUSES = {
    '整合性検査結果': 'snapshot_integrity',
    '規則数・撤回数・障害数・研究認証記録数': 'rule_inventory',
    '適用条件審査結果': 'scope_reviews',
    '信頼済みtipの最新性': 'current_state',
    '証明・行為権限・外部証拠・新文脈の認証範囲': 'authority_limits',
    '全検査結果・認証範囲': 'full_audit',
}
SUFFIXES = ('を教えて。', 'を示して。')
FRESH = '過去の値を今の値と取り違えないで。'
OK = 'TRANSLATION_CHECKED_BOUNDED_ONLY'
ERRORS = (*c.ERRORS, OSError)


def policy_digest():
    return b.sha(b.canonical({'schema': SCHEMA, 'prefixes': PREFIXES, 'clauses': CLAUSES,
                              'suffixes': SUFFIXES, 'fresh': FRESH, 'separator': '、',
                              'predecessor_policy': q.policy_digest()}))


def analyze(question):
    """Reparse the original bytes independently of any proposed translation."""
    out = {'schema': SCHEMA, 'status': 'HOLD', 'policy_sha256': policy_digest(),
           'question_sha256': b.sha(question) if type(question) is bytes else None,
           'trace': [], 'unresolved': [], 'typed_question': None, 'contract': None, **BOUNDARY}
    try:
        b.require(type(question) is bytes and 0 < len(question) <= 8192, 'QUESTION_BYTES')
        text = question.decode('utf-8')
        def piece(start, end, kind, topics=()):
            row = {'start_byte': start, 'end_byte': end, 'kind': kind,
                   'span_sha256': b.sha(question[start:end]), 'topics': list(topics)}
            out['trace'].append(row)
            if kind == 'unresolved':
                out['unresolved'].append(dict(row))
        topics = set()
        if text in q.QUESTIONS or question.startswith(b'{'):
            prior = q.compile_question(question)
            topics.update(prior['topics'])
            piece(0, len(question), 'registered_or_typed', prior['topics'])
        else:
            prefix = next((s for s in PREFIXES if text.startswith(s)), None)
            b.require(prefix is not None, 'UNREGISTERED_PREFIX')
            fresh = text.endswith(FRESH)
            core = text[:-len(FRESH)] if fresh else text
            suffix = next((s for s in SUFFIXES if core.endswith(s)), None)
            b.require(suffix is not None, 'UNREGISTERED_SUFFIX_OR_CONDITION')
            pos = len(prefix.encode()); piece(0, pos, 'prefix', PREFIXES[prefix]); topics.update(PREFIXES[prefix])
            body = core[len(prefix):-len(suffix)]
            seen = set()
            for i, word in enumerate(body.split('、')):
                if i:
                    end = pos + len('、'.encode()); piece(pos, end, 'separator'); pos = end
                end = pos + len(word.encode())
                topic = CLAUSES.get(word)
                if topic is None or topic in seen:
                    piece(pos, end, 'unresolved')
                else:
                    seen.add(topic); topics.add(topic); piece(pos, end, 'clause', (topic,))
                pos = end
            end = pos + len(suffix.encode()); piece(pos, end, 'request_suffix'); pos = end
            if fresh:
                topics.add('current_state'); piece(pos, len(question), 'freshness_condition', ('current_state',))
        cursor = 0
        for row in out['trace']:
            b.require(row['start_byte'] == cursor and row['end_byte'] >= cursor, 'SPAN_COVERAGE')
            cursor = row['end_byte']
        b.require(cursor == len(question), 'SPAN_COVERAGE')
        if out['unresolved']:
            out['reason'] = 'UNRESOLVED_OR_DUPLICATE_CLAUSE'
            return out
        typed = {'schema': q.QUESTION_SCHEMA, 'topics': [t for t in q.TOPICS if t in topics]}
        contract = q.compile_question(b.canonical(typed))
        out.update(status='TRANSLATION_CANDIDATE', typed_question=typed, contract=contract, reason=None)
    except ERRORS:
        # A malformed or out-of-grammar request is not silently shortened.
        out.update(reason='UNSUPPORTED_OR_MALFORMED_QUESTION', trace=[], unresolved=[])
        if type(question) is bytes and question:
            out['unresolved'] = [{'start_byte': 0, 'end_byte': len(question), 'kind': 'unresolved',
                                  'span_sha256': b.sha(question), 'topics': []}]
    return out


def check_translation(question, candidate):
    out = analyze(question)
    if out['status'] != 'TRANSLATION_CANDIDATE':
        return out
    if type(candidate) is not bytes or candidate != b.canonical(out['typed_question']):
        out.update(status='HOLD', reason='TYPED_TRANSLATION_MISMATCH')
    else:
        out['status'] = OK
    return out


def hold(translation, reason):
    contract = translation.get('contract')
    rows = [] if contract is None else [c.held(x, reason) for x in contract['plan']['claim_ids']]
    return b.canonical({'schema': SCHEMA, 'status': 'HOLD', 'reason': reason,
                        'translation': translation, 'claims': rows, **BOUNDARY})


def preflight(question, candidate, request, context):
    translation = check_translation(question, candidate)
    if translation['status'] != OK:
        return translation
    try:
        p.context_check(context, request)
        b.require(context['question_sha256'] == translation['question_sha256'], 'ORIGINAL_QUESTION_MISMATCH')
    except ERRORS:
        translation.update(status='HOLD', reason='ORIGINAL_CONTEXT_MISMATCH')
    return translation


def execute_question(snapshot, question, candidate, request, context, key):
    """Unsupported question/condition or wrong candidate stops before any gate subprocess."""
    translation = preflight(question, candidate, request, context)
    if translation['status'] != OK:
        return None, None, translation
    try:
        raw, admission = p.execute_and_admit(snapshot, request, context, key)
        return raw, admission, translation
    except ERRORS:
        translation.update(status='HOLD', reason='PRIVATE_INPUT_OR_EXECUTION_UNAVAILABLE')
        return None, None, translation


def publish_question(question, candidate, raw, admission, request, context, key, prior_packet):
    translation = preflight(question, candidate, request, context)
    if translation['status'] != OK:
        return hold(translation, translation['reason'])
    try:
        plan = translation['contract']['plan']
        packet = c.publish_claims(raw, admission, request, context, key, prior_packet, plan)
        source = p.strict(packet).get('publication')
        if source is None:
            return hold(translation, 'ADMITTED_CLAIM_EVIDENCE_MISSING')
        b.require([r['claim_id'] for r in source['claims']] == plan['claim_ids'], 'REQUIRED_CLAIM_COVERAGE')
        b.require(source['plan_sha256'] == b.sha(b.canonical(plan)), 'PLAN_BINDING')
        payload = {'schema': SCHEMA, 'status': source['status'], 'scope': 'bounded_original_question_only',
                   'translation': translation, 'translation_sha256': b.sha(b.canonical(translation)),
                   'context_sha256': b.sha(b.canonical(context)), 'claim_packet_sha256': b.sha(packet),
                   'claims': source['claims'], **BOUNDARY}
        return b.canonical({'publication': payload, 'tag': p.mac(key, b'question-translation-v0.5', payload)})
    except ERRORS:
        return hold(translation, 'ADMITTED_CLAIM_EVIDENCE_INVALID')


def verified_display(packet, **kwargs):
    expected = publish_question(**kwargs)
    if packet != expected:
        return hold(check_translation(kwargs.get('question'), kwargs.get('candidate')), 'PUBLICATION_MISMATCH'), 2
    data = p.strict(expected)
    return expected, 0 if data.get('publication', {}).get('status') == 'ALL_OBSERVED' else 2


def read_optional(path):
    try:
        return path.read_bytes() if path is not None else None
    except OSError:
        return None


def parse_optional(path):
    try:
        return p.strict(read_optional(path))
    except ERRORS:
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('compile', 'check', 'issue', 'publish', 'display'))
    parser.add_argument('--question', required=True, type=Path)
    for name in ('candidate', 'request', 'context', 'key-file', 'evidence-dir', 'snapshot', 'prior-packet', 'packet'):
        parser.add_argument('--' + name, type=Path)
    a = parser.parse_args()
    question, candidate = read_optional(a.question), read_optional(a.candidate)
    translation = analyze(question)
    try:
        if a.operation == 'compile':
            out, rc = b.canonical(translation), 0 if translation['status'] == 'TRANSLATION_CANDIDATE' else 2
        elif a.operation == 'check':
            translation = check_translation(question, candidate)
            out, rc = b.canonical(translation), 0 if translation['status'] == OK else 2
        else:
            request, context, key = parse_optional(a.request), parse_optional(a.context), read_optional(a.key_file)
            if a.operation == 'issue':
                translation = preflight(question, candidate, request, context)
                if translation['status'] != OK:
                    out, rc = hold(translation, translation['reason']), 2
                else:
                    b.require(a.snapshot is not None and a.evidence_dir is not None, 'PRIVATE_PATHS_REQUIRED')
                    a.evidence_dir.mkdir(mode=0o700, parents=False, exist_ok=False)
                    raw, admission, translation = execute_question(a.snapshot, question, candidate, request, context, key)
                    if raw is not None:
                        p.write_new(a.evidence_dir / 'bundle.json', raw)
                    if admission is not None:
                        p.write_new(a.evidence_dir / 'admission.json', admission)
                        out, rc = b.canonical({'schema': SCHEMA, 'status': 'ADMISSION_CREATED_NOT_PUBLISHED',
                                               'translation_sha256': b.sha(b.canonical(translation)), **BOUNDARY}), 0
                    else:
                        out, rc = hold(translation, 'ADMISSION_UNAVAILABLE'), 2
            else:
                raw = read_optional(a.evidence_dir / 'bundle.json') if a.evidence_dir else None
                admission = read_optional(a.evidence_dir / 'admission.json') if a.evidence_dir else None
                args = dict(question=question, candidate=candidate, raw=raw, admission=admission,
                            request=request, context=context, key=key, prior_packet=read_optional(a.prior_packet))
                if a.operation == 'display':
                    out, rc = verified_display(read_optional(a.packet), **args)
                else:
                    out = publish_question(**args)
                    rc = 0 if p.strict(out).get('publication', {}).get('status') == 'ALL_OBSERVED' else 2
        sys.stdout.buffer.write(out)
        return rc
    except ERRORS:
        sys.stdout.buffer.write(hold(translation, 'PRIVATE_INPUT_OR_EXECUTION_UNAVAILABLE'))
        return 2


if __name__ == '__main__':
    sys.exit(main())
