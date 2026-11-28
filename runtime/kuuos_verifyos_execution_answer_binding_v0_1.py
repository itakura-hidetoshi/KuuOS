"""Bound local execution reports for the GPT inheritance gates (VerifyOS).
Only a trusted host may invoke the runner and admit its digest. No text from
an LLM can substitute for that observation. No external truth or authority.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

SCHEMA = 'kuuos.verifyos.execution-answer-binding.v0.1'
BASE = ('KuuOS_native_GPT_continuity_v15.md', 'initial_checks_20261128_v15.json',
        'kuuos_continuation_20261128_v15.json', 'kuuos_inheritance_gate_v15.py')
GATES = ('kuuos_inheritance_gate_v16.py', 'kuuos_scope_guard_v16_1.py')
EXPECTED = ('PASS_INTEGRITY_ONLY', 'PASS_SCOPE_RECORDS_ONLY')
BOUNDARY = {'proof_authority': False, 'action_authority': False,
            'external_truth_verified': False, 'new_context_verified': False,
            'external_anchor_freshness_verified': False}


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def hex64(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def parse(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('NONFINITE_JSON')))


def request_check(request):
    require(set(request) == {'challenge', 'seq', 'tip', 'expected_hashes'}, 'REQUEST_SCHEMA')
    require(hex64(request['challenge']) and hex64(request['tip']), 'REQUEST_BINDING')
    require(type(request['seq']) is int and 0 <= request['seq'] <= 100000, 'REQUEST_SEQ')
    keys = {'base/' + BASE[2], *('gates/' + name for name in GATES)}
    h = request['expected_hashes']
    require(isinstance(h, dict) and set(h) == keys and all(map(hex64, h.values())), 'EXPECTED_HASHES')


def inventory(root, seq):
    expected = {'base': set(BASE), 'gates': set(GATES),
                'ledger': {f'{i:012d}.json' for i in range(seq + 1)}}
    result = {}
    for group, names in expected.items():
        folder = root / group
        require(folder.is_dir() and not folder.is_symlink(), 'UNSAFE_DIRECTORY')
        require({p.name for p in folder.iterdir()} == names, 'FILE_SET_MISMATCH')
        for name in sorted(names):
            path = folder / name
            require(path.is_file() and not path.is_symlink(), 'UNSAFE_FILE')
            result[f'{group}/{name}'] = sha(path.read_bytes())
    return result


def command(root, gate, request, python):
    return [python, '-B', '-E', '-s', str(root / 'gates' / gate),
            '--base', str(root / 'base'), '--ledger', str(root / 'ledger'),
            '--tip-seq', str(request['seq']), '--tip-sha256', request['tip']]


def process_pass(record, root, gate, expected, request, python):
    require(record['gate'] == gate and record['argv'] == command(root, gate, request, python), 'COMMAND_MISMATCH')
    require(type(record['exit_code']) is int and record['exit_code'] == 0, 'EXIT_NOT_ZERO')
    require(record['stderr'] == '', 'STDERR_NOT_EMPTY')
    for stream in ('stdout', 'stderr'):
        require(sha(record[stream].encode('utf-8')) == record[stream + '_sha256'], 'OUTPUT_DIGEST_MISMATCH')
    start, end = (datetime.fromisoformat(record[k]) for k in ('started_at', 'completed_at'))
    require(start.tzinfo is not None and end.tzinfo is not None and start <= end, 'TIME_BINDING')
    data = parse(record['stdout'])
    require(data['status'] == expected, 'STATUS_MISMATCH')
    require(type(data['seq']) is int and data['seq'] == request['seq'] and data['tip_sha256'] == request['tip'], 'ANCHOR_MISMATCH')
    require(data['proof_authority'] is False and data['action_authority'] is False, 'AUTHORITY_ESCALATION')
    return expected


def render(receipt, request):
    """Closed answer language; no caller-supplied prose or claims."""
    try:
        request_check(request)
        require(receipt['schema'] == SCHEMA and receipt['request_sha256'] == sha(canonical(request)), 'REQUEST_MISMATCH')
        require(receipt['boundary'] == BOUNDARY, 'BOUNDARY_MISMATCH')
        require(receipt['run_status'] == 'COMPLETED', 'RUN_INCOMPLETE')
        before, after = receipt['before'], receipt['after']
        require(before == after, 'INPUT_DRIFT')
        names = {*('base/' + n for n in BASE), *('gates/' + n for n in GATES),
                 *(f'ledger/{i:012d}.json' for i in range(request['seq'] + 1))}
        require(set(before) == names and all(map(hex64, before.values())), 'INPUT_INVENTORY')
        require(all(before[k] == v for k, v in request['expected_hashes'].items()), 'PIN_MISMATCH')
        require(before[f"ledger/{request['seq']:012d}.json"] == request['tip'], 'TIP_BYTES_MISMATCH')
        require(len(receipt['processes']) == len(GATES), 'MISSING_PROCESS')
        outcomes = [process_pass(row, Path(receipt['root']), gate, expected, request, receipt['python'])
                    for row, gate, expected in zip(receipt['processes'], GATES, EXPECTED)]
        status, reason = 'PASS_LOCAL_EXECUTION_STRUCTURE_ONLY', None
    except (ValueError, KeyError, TypeError, AttributeError, UnicodeError, OverflowError):
        outcomes, status, reason = [], 'HOLD', 'EXECUTION_EVIDENCE_INCOMPLETE_OR_INVALID'
    return {'schema': SCHEMA, 'request_sha256': sha(canonical(request)),
            'receipt_sha256': sha(canonical(receipt)), 'status': status,
            'gate_results': outcomes, 'reason': reason,
            'scope': 'supplied_snapshot_only', **BOUNDARY}


def run(root, request, timeout=60):
    """Call from a trusted host, not with arbitrary model-supplied commands."""
    root = Path(root)
    receipt = {'schema': SCHEMA, 'request_sha256': sha(canonical(request)),
               'root': str(root.absolute()), 'python': sys.executable,
               'boundary': dict(BOUNDARY), 'processes': [], 'run_status': 'HOLD'}
    try:
        request_check(request)
        require(not root.is_symlink(), 'ROOT_SYMLINK')
        root = root.resolve()
        receipt['root'] = str(root)
        receipt['before'] = inventory(root, request['seq'])
        require(all(receipt['before'][k] == v for k, v in request['expected_hashes'].items()), 'PIN_MISMATCH')
        for gate, expected in zip(GATES, EXPECTED):
            argv = command(root, gate, request, sys.executable)
            row = {'gate': gate, 'argv': argv, 'started_at': datetime.now(timezone.utc).isoformat()}
            receipt['processes'].append(row)
            proc = subprocess.run(argv, cwd=root, capture_output=True, timeout=timeout, check=False)
            row.update(exit_code=proc.returncode, stdout=proc.stdout.decode('utf-8'),
                       stderr=proc.stderr.decode('utf-8'), stdout_sha256=sha(proc.stdout),
                       stderr_sha256=sha(proc.stderr), completed_at=datetime.now(timezone.utc).isoformat())
            process_pass(row, root, gate, expected, request, sys.executable)
        receipt['after'] = inventory(root, request['seq'])
        receipt['run_status'] = 'COMPLETED'
    except (ValueError, KeyError, TypeError, OSError, subprocess.TimeoutExpired, UnicodeError) as exc:
        receipt['obstruction'] = type(exc).__name__ + ': ' + str(exc)
    return {'receipt': receipt, 'answer': render(receipt, request)}


def verify(raw, request, trusted_bundle_sha256):
    """Digest must be admitted from the actual host response, independently
    of the untrusted answer. Recomputing the candidate's own hash is not admission.
    This verifies correspondence, not authenticity of an untrusted host.
    """
    try:
        request_check(request)
        require(hex64(trusted_bundle_sha256) and sha(raw) == trusted_bundle_sha256, 'UNADMITTED_BUNDLE')
        bundle = parse(raw)
        require(raw == canonical(bundle) and set(bundle) == {'receipt', 'answer'}, 'BUNDLE_SCHEMA')
        expected = render(bundle['receipt'], request)
        require(canonical(bundle['answer']) == canonical(expected), 'ANSWER_MISMATCH')
        return expected
    except (ValueError, KeyError, TypeError, AttributeError, UnicodeError, OverflowError):
        return {'schema': SCHEMA, 'status': 'HOLD', 'reason': 'UNADMITTED_OR_MISMATCHED_BUNDLE', **BOUNDARY}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='operation', required=True)
    for op in ('run', 'verify'):
        p = sub.add_parser(op)
        p.add_argument('--request', type=Path, required=True)
        p.add_argument('--bundle', type=Path, required=True)
        if op == 'run':
            p.add_argument('--snapshot', type=Path, required=True)
        else:
            p.add_argument('--trusted-bundle-sha256', required=True)
    a = parser.parse_args()
    try:
        request = parse(a.request.read_bytes())
        request_check(request)
        if a.operation == 'run':
            bundle = run(a.snapshot, request)
            raw = canonical(bundle)
            with a.bundle.open('xb') as handle:
                handle.write(raw)
            answer = bundle['answer']
            output = {'bundle_sha256': sha(raw), 'answer': answer}
        else:
            answer = verify(a.bundle.read_bytes(), request, a.trusted_bundle_sha256)
            output = {'answer': answer}
        print(canonical(output).decode(), end='')
        return 0 if answer['status'] == 'PASS_LOCAL_EXECUTION_STRUCTURE_ONLY' else 2
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(canonical({'status': 'HOLD', 'reason': type(exc).__name__, **BOUNDARY}).decode(), end='')
        return 2


if __name__ == '__main__':
    sys.exit(main())
