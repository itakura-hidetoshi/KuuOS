"""Exact question contracts for receipt-bound claims; no open-language completeness claim."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from runtime import kuuos_verifyos_claim_evidence_binding_v0_3 as claims

b, p = claims.b, claims.p
SCHEMA = 'kuuos.verifyos.question-claim-contract.v0.4'
QUESTION_SCHEMA = 'kuuos.verifyos.typed-question.v0.4'
BASELINE = ('integrity_status', 'scope_status', 'integrity_exit_code', 'scope_exit_code', 'snapshot_seq', 'snapshot_tip')
TOPICS = {
    'snapshot_integrity': (),
    'rule_inventory': ('rule_count', 'withdrawn_count', 'obstruction_count', 'research_certificate_count'),
    'scope_reviews': ('scope_candidate_count', 'scope_held_count', 'scope_no_use_count'),
    'current_state': ('current_tip',),
    'authority_limits': ('external_truth', 'lean_proof', 'new_context_validity', 'action_permission'),
    'full_audit': tuple(claims.FIELDS) + tuple(sorted(claims.UNSUPPORTED)),
}
QUESTIONS = {
    '取得済み台帳スナップショットの整合性検査結果を教えて。': ('snapshot_integrity',),
    '取得済み台帳の適用条件審査結果を教えて。': ('scope_reviews',),
    '取得済み台帳の規則数・障害数・研究認証記録数を教えて。': ('rule_inventory',),
    '空OSの現行継承台帳の信頼済みtipと、台帳の整合性が成立しているかを教えて。過去の値を今の値と取り違えないで。': ('current_state',),
    '取得済み台帳の全検査結果と、証明・行為権限・外部証拠・新文脈・現行性の認証範囲を教えて。': ('full_audit',),
}
ORDER = tuple(claims.FIELDS) + tuple(sorted(claims.UNSUPPORTED))
BOUNDARY = {**b.BOUNDARY, 'open_language_completeness_verified': False}


def policy_digest():
    return b.sha(b.canonical({'schema': SCHEMA, 'question_schema': QUESTION_SCHEMA,
                              'baseline': BASELINE, 'topics': TOPICS, 'questions': QUESTIONS, 'order': ORDER}))


def compile_question(question):
    """Only exact original bytes: registered text or a closed typed question."""
    b.require(type(question) is bytes and 0 < len(question) <= 8192, 'QUESTION_BYTES')
    text = question.decode('utf-8')
    if text in QUESTIONS:
        topics = QUESTIONS[text]
        kind = 'exact_registered_text'
    else:
        value = p.strict(question)
        b.require(type(value) is dict and set(value) == {'schema', 'topics'}, 'QUESTION_SCHEMA')
        b.require(value['schema'] == QUESTION_SCHEMA, 'QUESTION_VERSION')
        topics = value['topics']
        b.require(type(topics) is list and 0 < len(topics) <= len(TOPICS), 'TOPIC_COUNT')
        b.require(all(type(t) is str and t in TOPICS for t in topics), 'UNKNOWN_TOPIC')
        b.require(len(topics) == len(set(topics)), 'DUPLICATE_TOPIC')
        kind = 'typed_question'
    required = set(BASELINE)
    for topic in topics:
        required.update(TOPICS[topic])
    ids = [x for x in ORDER if x in required]
    b.require(set(ids) == required, 'POLICY_COVERAGE')
    plan = {'claim_ids': ids}
    claims.plan_check(plan)
    return {'schema': SCHEMA, 'question_sha256': b.sha(question), 'policy_sha256': policy_digest(),
            'kind': kind, 'topics': list(topics), 'plan': plan}


def hold(reason='QUESTION_OR_EVIDENCE_INVALID', contract=None):
    rows = [] if contract is None else [claims.held(x, reason) for x in contract['plan']['claim_ids']]
    return b.canonical({'schema': SCHEMA, 'status': 'HOLD', 'reason': reason, 'contract': contract,
                        'claims': rows, **BOUNDARY})


def publish_question(question, raw, admission, request, context, key, prior_packet):
    contract = None
    try:
        p.context_check(context, request)
        b.require(b.sha(question) == context['question_sha256'], 'ORIGINAL_QUESTION_MISMATCH')
        contract = compile_question(question)
        packet = claims.publish_claims(raw, admission, request, context, key, prior_packet, contract['plan'])
        parsed = p.strict(packet)
        if 'publication' not in parsed:
            return hold('ADMITTED_CLAIM_EVIDENCE_MISSING', contract)
        source = parsed['publication']
        rows = source['claims']
        b.require([r['claim_id'] for r in rows] == contract['plan']['claim_ids'], 'REQUIRED_CLAIM_COVERAGE')
        b.require(source['plan_sha256'] == b.sha(b.canonical(contract['plan'])), 'PLAN_BINDING')
        payload = {'schema': SCHEMA, 'status': source['status'], 'scope': 'registered_question_contract_only',
                   'contract': contract, 'contract_sha256': b.sha(b.canonical(contract)),
                   'context_sha256': b.sha(b.canonical(context)), 'claim_packet_sha256': b.sha(packet),
                   'claims': rows, **BOUNDARY}
        return b.canonical({'publication': payload, 'tag': p.mac(key, b'question-publication-v0.4', payload)})
    except claims.ERRORS:
        return hold(contract=contract)


def verified_display(packet, **kwargs):
    expected = publish_question(**kwargs)
    if packet != expected:
        return hold('PUBLICATION_MISMATCH'), 2
    data = p.strict(expected)
    return expected, 0 if data.get('publication', {}).get('status') == 'ALL_OBSERVED' else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('compile', 'publish', 'display'))
    parser.add_argument('--question', required=True, type=Path)
    for name in ('request', 'context', 'key-file', 'evidence-dir', 'prior-packet', 'packet'):
        parser.add_argument('--' + name, type=Path)
    a = parser.parse_args()
    try:
        question = a.question.read_bytes()
        if a.operation == 'compile':
            sys.stdout.buffer.write(b.canonical(compile_question(question)))
            return 0  # Plan compilation only, not a verification result.
        kwargs = dict(question=question, raw=(a.evidence_dir / 'bundle.json').read_bytes(),
                      admission=(a.evidence_dir / 'admission.json').read_bytes(), request=p.strict(a.request.read_bytes()),
                      context=p.strict(a.context.read_bytes()), key=a.key_file.read_bytes(), prior_packet=a.prior_packet.read_bytes())
        if a.operation == 'display':
            out, rc = verified_display(a.packet.read_bytes(), **kwargs)
        else:
            out = publish_question(**kwargs)
            rc = 0 if p.strict(out).get('publication', {}).get('status') == 'ALL_OBSERVED' else 2
        sys.stdout.buffer.write(out)
        return rc
    except (OSError, *claims.ERRORS):
        sys.stdout.buffer.write(hold())
        return 2


if __name__ == '__main__':
    sys.exit(main())
