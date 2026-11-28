"""VerifyOS controlled answer egress; trusted-host interface, not a ChatGPT hook."""
from __future__ import annotations

import argparse
import hashlib
import hmac
import sys
from pathlib import Path

from runtime import kuuos_verifyos_execution_answer_binding_v0_1 as binding

SCHEMA = 'kuuos.verifyos.answer-publication.v0.2'
AUDIENCE = 'private_verification_channel'
SUCCESS = 'PASS_LOCAL_EXECUTION_STRUCTURE_ONLY'
HOLD_TEXT = 'HOLD: 実行証拠または公開条件を確認できません。検証合格は未認証です。'
PASS_TEXT = '指定されたスナップショットの記録整合性検査と適用条件記録の構造検査が合格しました。外部証拠の真正性・現行状態・新文脈への適用・証明・行為権限は認証していません。'
MAX_BYTES = 8 * 1024 * 1024
canonical, sha, require = binding.canonical, binding.sha, binding.require


def strict(raw):
    require(isinstance(raw, bytes) and len(raw) <= MAX_BYTES, 'INPUT_SIZE')
    obj = binding.parse(raw)
    require(canonical(obj) == raw, 'NONCANONICAL_INPUT')
    return obj


def context_check(context, request):
    binding.request_check(request)
    require(set(context) == {'turn_id', 'question_sha256', 'challenge', 'request_sha256', 'audience'}, 'CONTEXT_SCHEMA')
    require(all(binding.hex64(context[k]) for k in ('turn_id', 'question_sha256', 'challenge', 'request_sha256')), 'CONTEXT_BINDING')
    require(context['audience'] == AUDIENCE, 'AUDIENCE_MISMATCH')
    require(context['challenge'] == request['challenge'], 'CHALLENGE_MISMATCH')
    require(context['request_sha256'] == sha(canonical(request)), 'REQUEST_MISMATCH')


def mac(key, domain, payload):
    require(isinstance(key, bytes) and len(key) == 32, 'HOST_KEY_REQUIRED')
    return hmac.new(key, SCHEMA.encode() + b'\x00' + domain + b'\x00' + canonical(payload), hashlib.sha256).hexdigest()


def accepted(raw, request, digest):
    strict(raw)
    result = binding.verify(raw, request, digest)
    require(result.get('status') == SUCCESS, 'BINDING_NOT_ACCEPTED')
    require(result.get('gate_results') == list(binding.EXPECTED), 'GATE_RESULTS')
    require(result.get('scope') == 'supplied_snapshot_only', 'SCOPE_MISMATCH')
    require(all(result.get(k) is False for k in binding.BOUNDARY), 'AUTHORITY_ESCALATION')
    return result


def execute_and_admit(snapshot, request, context, key):
    """Issuer path: execute pinned gates; never sign an incoming model receipt."""
    context_check(context, request)
    mac(key, b'key-check', {})
    raw = canonical(binding.run(snapshot, request))
    try:
        result = accepted(raw, request, sha(raw))
    except (ValueError, KeyError, TypeError, AttributeError, OverflowError, UnicodeError):
        return raw, None
    payload = {'schema': SCHEMA, 'context_sha256': sha(canonical(context)),
               'bundle_sha256': sha(raw), 'receipt_sha256': result['receipt_sha256'],
               'request_sha256': result['request_sha256']}
    return raw, canonical({'payload': payload, 'tag': mac(key, b'admission', payload)})


def hold():
    return canonical({'schema': SCHEMA, 'status': 'HOLD', 'message': HOLD_TEXT,
                      'scope': 'unverified', **binding.BOUNDARY})


def publish(raw, admission, request, context, key):
    """Only the trusted egress supplies request, context and key. No prose input."""
    try:
        context_check(context, request)
        token = strict(admission)
        require(set(token) == {'payload', 'tag'}, 'ADMISSION_SCHEMA')
        payload = token['payload']
        require(set(payload) == {'schema', 'context_sha256', 'bundle_sha256', 'receipt_sha256', 'request_sha256'}, 'ADMISSION_PAYLOAD')
        require(binding.hex64(token['tag']) and hmac.compare_digest(token['tag'], mac(key, b'admission', payload)), 'ADMISSION_AUTHENTICATION')
        require(payload['schema'] == SCHEMA and payload['context_sha256'] == sha(canonical(context)), 'ADMISSION_CONTEXT')
        require(payload['request_sha256'] == sha(canonical(request)) and payload['bundle_sha256'] == sha(raw), 'ADMISSION_BINDING')
        result = accepted(raw, request, payload['bundle_sha256'])
        require(payload['receipt_sha256'] == result['receipt_sha256'], 'RECEIPT_MISMATCH')
        output = {'schema': SCHEMA, 'status': SUCCESS, 'message': PASS_TEXT,
                  'scope': 'supplied_snapshot_only', 'turn_id': context['turn_id'],
                  'question_sha256': context['question_sha256'],
                  'request_sha256': result['request_sha256'], 'context_sha256': payload['context_sha256'],
                  'bundle_sha256': payload['bundle_sha256'], 'receipt_sha256': result['receipt_sha256'],
                  'gate_results': result['gate_results'], **binding.BOUNDARY}
        return canonical({'publication': output, 'tag': mac(key, b'publication', output)})
    except (ValueError, KeyError, TypeError, AttributeError, OverflowError, UnicodeError):
        return hold()


def verified_display(packet, raw, admission, request, context, key):
    """Entire packet must match recomputation; never echo caller-supplied text."""
    expected = publish(raw, admission, request, context, key)
    if packet != expected:
        return HOLD_TEXT, 2
    data = strict(expected)
    if 'publication' not in data:
        return HOLD_TEXT, 2
    return data['publication']['message'], 0


def write_new(path, raw):
    # Host supplies a private, new directory; preserve evidence on failure.
    import os
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as out:
        out.write(raw)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='op', required=True)
    for name in ('issue', 'publish', 'display'):
        s = sub.add_parser(name)
        for arg in ('request', 'context', 'key-file', 'evidence-dir'):
            s.add_argument('--' + arg, required=True, type=Path)
        if name == 'issue':
            s.add_argument('--snapshot', required=True, type=Path)
        if name == 'display':
            s.add_argument('--packet', required=True, type=Path)
    a = p.parse_args()
    try:
        request, context = strict(a.request.read_bytes()), strict(a.context.read_bytes())
        key = a.key_file.read_bytes()
        if a.op == 'issue':
            raw, admission = execute_and_admit(a.snapshot, request, context, key)
            a.evidence_dir.mkdir(mode=0o700, parents=False, exist_ok=False)
            write_new(a.evidence_dir / 'bundle.json', raw)
            if admission is None:
                sys.stdout.buffer.write(hold()); return 2
            write_new(a.evidence_dir / 'admission.json', admission)
            # Admission is not publication. Do not emit a success claim here.
            return 0
        raw = (a.evidence_dir / 'bundle.json').read_bytes()
        admission = (a.evidence_dir / 'admission.json').read_bytes()
        if a.op == 'publish':
            packet = publish(raw, admission, request, context, key)
            sys.stdout.buffer.write(packet)
            return 0 if 'publication' in strict(packet) else 2
        message, rc = verified_display(a.packet.read_bytes(), raw, admission, request, context, key)
        print(message)
        return rc
    except (OSError, ValueError, KeyError, TypeError, AttributeError, OverflowError, UnicodeError):
        if a.op == 'display':
            print(HOLD_TEXT)
        else:
            sys.stdout.buffer.write(hold())
        return 2


if __name__ == '__main__':
    sys.exit(main())
