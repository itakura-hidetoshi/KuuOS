"""Ed25519 receipt binding and public replay; not independent execution attestation."""
from __future__ import annotations
import subprocess
import tempfile
from pathlib import Path
from runtime import kuuos_verifyos_interpretation_anchor_v0_10 as a

s, v, b, p, f = a.s, a.v, a.b, a.p, a.v.f
c, q = v.c, v.q
SCHEMA = 'kuuos.verifyos.public-receipt.v0.11'
DOMAIN = b'KuuOS/VerifyOS/Ed25519/public-receipt/v0.11\x00'
SPKI = bytes.fromhex('302a300506032b6570032100')
BOUNDARY = {**a.BOUNDARY, 'independent_execution_attested': False,
            'signer_identity_authenticated': False, 'global_replay_prevented': False}
ERRORS = (*a.ERRORS, subprocess.SubprocessError)


def openssl(*args):
    proc = subprocess.run(['openssl', *args], stdin=subprocess.DEVNULL,
                          capture_output=True, timeout=15, check=False)
    b.require(proc.returncode == 0, 'OPENSSL_OPERATION_FAILED')
    return proc.stdout


def public_key(private_key):
    der = openssl('pkey', '-in', str(private_key), '-pubout', '-outform', 'DER')
    b.require(len(der) == len(SPKI)+32 and der.startswith(SPKI), 'ED25519_KEY_REQUIRED')
    return der[len(SPKI):]


def message(payload):
    return DOMAIN + b.canonical(payload)


def sign(payload, private_key, expected_key):
    b.require(type(expected_key) is bytes and len(expected_key)==32 and public_key(private_key)==expected_key, 'SIGNER_KEY_MISMATCH')
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)/'message'; path.write_bytes(message(payload))
        sig = openssl('pkeyutl','-sign','-rawin','-inkey',str(private_key),'-in',str(path))
    b.require(len(sig)==64, 'SIGNATURE_LENGTH')
    return sig


def verify_signature(payload, signature, expected_key):
    b.require(type(expected_key) is bytes and len(expected_key)==32 and type(signature) is bytes and len(signature)==64, 'ED25519_INPUT')
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp); msg = root/'message'; sig = root/'signature'; pub = root/'public.der'
        msg.write_bytes(message(payload)); sig.write_bytes(signature); pub.write_bytes(SPKI+expected_key)
        openssl('pkeyutl','-verify','-rawin','-pubin','-keyform','DER','-inkey',str(pub),'-in',str(msg),'-sigfile',str(sig))


def reconstruct_tips(seed_id, events):
    """Recreate the sealed v0.10 journal from exact v0.8 events, without DB access."""
    store = a.genesis_tip(seed_id)
    anchor = {'sequence':0,'sha256':b.sha(a.row(seed_id,0,s.ZERO,'GENESIS',store))}
    for event in events:
        seq = store['sequence']+1
        target = {'sequence':seq,'sha256':b.sha(s.row_bytes(seed_id,seq,store['sha256'],event))}
        material = {'previous':store,'target':target,'event_sha256':v.digest(event)}
        for operation in ('PREPARE','SEAL'):
            n = anchor['sequence']+1
            anchor = {'sequence':n,'sha256':b.sha(a.row(seed_id,n,anchor['sha256'],operation,material))}
        store = target
    return anchor, store


def derive(raw, revision_log, seed, current_request, current_context, expected_anchor, expected_key):
    """Public structural replay. Expected key, anchor, seed and context are verifier inputs."""
    b.require(type(expected_key) is bytes and len(expected_key)==32, 'ED25519_KEY_REQUIRED')
    fixed, seed_id, _ = s.seed_material(seed)
    log = p.strict(revision_log)
    inputs = s.replay_inputs(fixed,log,current_request,current_context)
    checked = v.replay(**inputs)
    b.require(checked['status']==v.OK, 'REVISION_REPLAY_FAILED')
    anchor, store = reconstruct_tips(seed_id,log['events'])
    a.tip_check(expected_anchor)
    b.require(s.same_tip(expected_anchor,anchor), 'SEALED_ANCHOR_MISMATCH')
    p.strict(raw)
    result = b.verify(raw,current_request,b.sha(raw))
    b.require(result.get('status')==p.SUCCESS and result.get('gate_results')==list(b.EXPECTED), 'EXECUTION_RECEIPT_INVALID')
    receipt = p.strict(raw)['receipt']
    family = checked['seed']['analysis']['family']
    rows = [c.project(x,receipt,current_request,{'bundle_sha256':b.sha(raw),'receipt_sha256':result['receipt_sha256']}) for x in family['union_claim_ids']]
    active = set(checked['active_ids']); observed = {x['claim_id'] for x in rows if x['status']=='OBSERVED_IN_ADMITTED_RECEIPT'}
    required = set(checked['active_union_claim_ids'])
    def status(ids):
        n = len(observed & set(ids))
        return 'ALL_OBSERVED' if n==len(ids) else 'PARTIAL' if n else 'HOLD'
    original = status(family['union_claim_ids'])
    if len(family['interpretations'])>1 and original!='HOLD': original='AMBIGUOUS_'+original
    answer = status(required)
    if answer!='HOLD': answer=('AMBIGUOUS_' if len(active)>1 else 'ACTIVE_VIEW_')+answer
    branches = [{**row,'active_in_revised_view':row['interpretation_id'] in active} for row in f.branch_rows(family,rows)]
    return {'schema':SCHEMA,'algorithm':'Ed25519','key_sha256':b.sha(expected_key),
            'seed_sha256':seed_id,'anchor_tip':anchor,'committed_tip':store,
            'context_sha256':v.digest(current_context),'request_sha256':v.digest(current_request),
            'revision_log_sha256':b.sha(revision_log),'revision_sha256':v.digest(checked),
            'bundle_sha256':b.sha(raw),'receipt_sha256':result['receipt_sha256'],
            'answer_status':answer,'original_family_status':original,'claims':rows,'branches':branches,
            'selected_interpretation':None,'scope':'signed_replayed_snapshot_only',**BOUNDARY}


def hold(reason):
    return {'schema':SCHEMA,'status':'HOLD','reason':reason,**BOUNDARY}


def issue(store, anchor, seed, expected_anchor, raw, admission, host_key, prior_packet,
          private_key, expected_key, current_request, current_context):
    """Trusted issuer reads actual sealed snapshot and verifies v0.2 admission before signing."""
    try:
        snap=a.read(store,anchor,seed,expected_anchor)
        b.require(snap['status']=='ANCHOR_MATCHED_SNAPSHOT_ONLY', 'ANCHOR_NOT_MATCHED')
        inputs=snap['inputs']; log=inputs['revision_log']
        b.require(b.canonical(inputs['current_request'])==b.canonical(current_request) and b.canonical(inputs['current_context'])==b.canonical(current_context), 'CURRENT_CONTEXT_MISMATCH')
        source=p.strict(v.publish_question(raw,admission,host_key,prior_packet,**inputs)).get('publication')
        b.require(source is not None, 'HOST_ADMISSION_INVALID')
        payload=derive(raw,log,seed,current_request,current_context,expected_anchor,expected_key)
        b.require(s.same_tip(payload['committed_tip'],snap['committed_tip']), 'STORE_TIP_MISMATCH')
        for name in ('claims','branches','original_family_status','revision_sha256'):
            b.require(payload[name]==source[name], 'HOST_PUBLIC_PROJECTION_MISMATCH')
        b.require(payload['answer_status']==source['status'], 'HOST_ANSWER_MISMATCH')
        signature=sign(payload,private_key,expected_key)
        verify_signature(payload,signature,expected_key)
        return {'schema':SCHEMA,'status':'SIGNED_SNAPSHOT_ONLY','packet':b.canonical({'payload':payload,'signature_hex':signature.hex()}),'revision_log':log,**BOUNDARY}
    except ERRORS as exc:
        return hold(str(exc) if type(exc) is ValueError else 'ISSUER_UNAVAILABLE')


def verify(packet, raw, revision_log, seed, current_request, current_context, expected_anchor, expected_key):
    """No private signing key, host MAC key, DB or model supplied trust anchor needed."""
    try:
        obj=p.strict(packet)
        b.require(type(obj) is dict and set(obj)=={'payload','signature_hex'}, 'PACKET_SCHEMA')
        sig=obj['signature_hex']; b.require(type(sig) is str and len(sig)==128, 'SIGNATURE_ENCODING')
        signature=bytes.fromhex(sig); b.require(sig==signature.hex(), 'SIGNATURE_ENCODING')
        verify_signature(obj['payload'],signature,expected_key)
        expected=derive(raw,revision_log,seed,current_request,current_context,expected_anchor,expected_key)
        b.require(b.canonical(obj['payload'])==b.canonical(expected), 'SIGNED_PROJECTION_MISMATCH')
        return {'schema':SCHEMA,'status':'PUBLIC_SIGNATURE_AND_REPLAY_MATCHED_ONLY','payload':expected,**BOUNDARY}
    except ERRORS as exc:
        return hold(str(exc) if type(exc) is ValueError else 'PUBLIC_VERIFIER_UNAVAILABLE')
