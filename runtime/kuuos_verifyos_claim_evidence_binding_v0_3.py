"""Closed claim projections from a v0.2-admitted execution bundle."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from runtime import kuuos_verifyos_answer_publication_v0_2 as p

b = p.binding
SCHEMA = 'kuuos.verifyos.claim-evidence-binding.v0.3'
# Fixed vocabulary: (gate index, source, field path, type). Never evaluate model paths.
FIELDS = {
    'integrity_status': (0, 'stdout', ('status',), 'status'),
    'scope_status': (1, 'stdout', ('status',), 'status'),
    'integrity_exit_code': (0, 'process', ('exit_code',), 'zero'),
    'scope_exit_code': (1, 'process', ('exit_code',), 'zero'),
    'snapshot_seq': (0, 'stdout', ('seq',), 'nat'),
    'snapshot_tip': (0, 'stdout', ('tip_sha256',), 'digest'),
    'rule_count': (0, 'stdout', ('rule_count',), 'nat'),
    'withdrawn_count': (0, 'stdout', ('withdrawn_count',), 'nat'),
    'obstruction_count': (0, 'stdout', ('obstruction_count',), 'nat'),
    'research_certificate_count': (0, 'stdout', ('research_certificate_count',), 'nat'),
    'scope_candidate_count': (1, 'stdout', ('reviews', 'candidate'), 'nat'),
    'scope_held_count': (1, 'stdout', ('reviews', 'held'), 'nat'),
    'scope_no_use_count': (1, 'stdout', ('reviews', 'no_use'), 'nat'),
}
UNSUPPORTED = frozenset({'current_tip', 'external_truth', 'lean_proof', 'new_context_validity', 'action_permission'})
ERRORS = (ValueError, KeyError, TypeError, AttributeError, OverflowError, UnicodeError, RecursionError, IndexError)


def plan_check(plan):
    b.require(type(plan) is dict and set(plan) == {'claim_ids'}, 'PLAN_SCHEMA')
    ids = plan['claim_ids']
    b.require(type(ids) is list and 0 < len(ids) <= len(FIELDS) + len(UNSUPPORTED), 'PLAN_SIZE')
    b.require(all(type(x) is str and (x in FIELDS or x in UNSUPPORTED) for x in ids), 'UNKNOWN_CLAIM')
    b.require(len(ids) == len(set(ids)), 'DUPLICATE_CLAIM')
    return ids


def held(claim_id, reason):
    return {'claim_id': claim_id, 'status': 'HOLD', 'value': None, 'evidence': None, 'reason': reason}


def project(claim_id, receipt, request, publication):
    if claim_id in UNSUPPORTED:
        return held(claim_id, 'OUTSIDE_CERTIFIED_SCOPE')
    i, source, path, kind = FIELDS[claim_id]
    try:
        record = receipt['processes'][i]
        value = b.parse(record['stdout']) if source == 'stdout' else record
        for field in path:
            value = value[field]
        if kind == 'status':
            good = value == b.EXPECTED[i]
        elif kind == 'digest':
            good = b.hex64(value) and value == request['tip']
        elif kind == 'zero':
            good = type(value) is int and value == 0
        else:
            good = type(value) is int and value >= 0
        b.require(good, 'FIELD_VALUE')
        return {'claim_id': claim_id, 'status': 'OBSERVED_IN_ADMITTED_RECEIPT', 'value': value,
                'scope': 'supplied_snapshot_only', 'reason': None,
                'evidence': {'bundle_sha256': publication['bundle_sha256'],
                             'receipt_sha256': publication['receipt_sha256'],
                             'process_index': i, 'gate': b.GATES[i], 'source': source,
                             'field_path': list(path), 'process_sha256': b.sha(b.canonical(record)),
                             'stdout_sha256': record['stdout_sha256']}}
    except ERRORS:
        return held(claim_id, 'FIELD_MISSING_OR_INVALID')


def hold():
    return b.canonical({'schema': SCHEMA, 'status': 'HOLD', 'reason': 'PUBLICATION_OR_PLAN_INVALID',
                        'claims': [], **b.BOUNDARY})


def publish_claims(raw, admission, request, context, key, prior_packet, plan):
    """The expected plan is a host input, not the answer's self-declared claim list."""
    try:
        ids = plan_check(plan)
        expected = p.publish(raw, admission, request, context, key)
        b.require(prior_packet == expected, 'PRIOR_PACKET_MISMATCH')
        publication = p.strict(expected)['publication']
        b.require(publication['status'] == p.SUCCESS, 'PRIOR_NOT_ADMITTED')
        receipt = p.strict(raw)['receipt']
        rows = [project(x, receipt, request, publication) for x in ids]
        n = sum(row['status'] == 'OBSERVED_IN_ADMITTED_RECEIPT' for row in rows)
        payload = {'schema': SCHEMA, 'status': 'ALL_OBSERVED' if n == len(rows) else 'PARTIAL' if n else 'HOLD',
                   'scope': 'supplied_snapshot_only', 'plan_sha256': b.sha(b.canonical(plan)),
                   'context_sha256': b.sha(b.canonical(context)), 'prior_packet_sha256': b.sha(prior_packet),
                   'claims': rows, **b.BOUNDARY}
        return b.canonical({'publication': payload, 'tag': p.mac(key, b'claim-publication-v0.3', payload)})
    except ERRORS:
        return hold()


def verified_display(packet, raw, admission, request, context, key, prior_packet, plan):
    expected = publish_claims(raw, admission, request, context, key, prior_packet, plan)
    if packet != expected:
        return hold(), 2
    data = p.strict(expected)
    if 'publication' not in data:
        return hold(), 2
    status = data['publication']['status']
    return expected, 0 if status == 'ALL_OBSERVED' else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('publish', 'display'))
    for name in ('request', 'context', 'key-file', 'evidence-dir', 'prior-packet', 'plan'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--packet', type=Path)
    a = parser.parse_args()
    try:
        args = ((a.evidence_dir / 'bundle.json').read_bytes(), (a.evidence_dir / 'admission.json').read_bytes(),
                p.strict(a.request.read_bytes()), p.strict(a.context.read_bytes()), a.key_file.read_bytes(),
                a.prior_packet.read_bytes(), p.strict(a.plan.read_bytes()))
        if a.operation == 'display':
            b.require(a.packet is not None, 'PACKET_REQUIRED')
            out, rc = verified_display(a.packet.read_bytes(), *args)
        else:
            out = publish_claims(*args)
            obj = p.strict(out)
            rc = 0 if obj.get('publication', {}).get('status') == 'ALL_OBSERVED' else 2
        sys.stdout.buffer.write(out)
        return rc
    except (OSError, *ERRORS):
        sys.stdout.buffer.write(hold())
        return 2


if __name__ == '__main__':
    sys.exit(main())
