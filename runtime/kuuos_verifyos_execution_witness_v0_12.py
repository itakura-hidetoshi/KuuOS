"""Separate-key execution witness; agreement, not proof of organizational independence."""
from __future__ import annotations
from pathlib import Path
from runtime import kuuos_verifyos_public_receipt_v0_11 as g

b,p = g.b,g.p
SCHEMA = 'kuuos.verifyos.execution-witness.v0.12'
BOUNDARY = {**g.BOUNDARY, 'organizational_independence_verified': False,
            'independent_runtime_isolation_verified': False}
ERRORS = g.ERRORS


def hold(reason, **details):
    return {'schema':SCHEMA,'status':'HOLD','reason':reason,**details,**BOUNDARY}


def policy_check(policy, request, context, anchor, primary_key, witness_key):
    p.context_check(context,request); g.a.tip_check(anchor)
    b.require(type(primary_key) is bytes and type(witness_key) is bytes and len(primary_key)==len(witness_key)==32 and primary_key!=witness_key,'DISTINCT_PINNED_KEYS_REQUIRED')
    b.require(type(policy) is dict and set(policy)=={'nonce','primary_packet_sha256','inventory'},'WITNESS_POLICY_SCHEMA')
    b.require(b.hex64(policy['nonce']) and policy['nonce']!=request['challenge'] and b.hex64(policy['primary_packet_sha256']),'WITNESS_CHALLENGE_REQUIRED')
    inv=policy['inventory']; names={*('base/'+n for n in b.BASE),*('gates/'+n for n in b.GATES),*(f'ledger/{i:012d}.json' for i in range(request['seq']+1))}
    b.require(type(inv) is dict and set(inv)==names and all(map(b.hex64,inv.values())),'FULL_INVENTORY_REQUIRED')
    b.require(all(inv[k]==value for k,value in request['expected_hashes'].items()) and inv[f"ledger/{request['seq']:012d}.json"]==request['tip'],'INVENTORY_PIN_MISMATCH')
    return {**request,'challenge':policy['nonce']}


def witness_payload(raw, policy, request, context, anchor, primary_key, witness_key):
    wr=policy_check(policy,request,context,anchor,primary_key,witness_key)
    bundle=p.strict(raw)
    b.require(type(bundle) is dict and set(bundle)=={'receipt','answer'},'BUNDLE_SCHEMA')
    receipt=bundle['receipt']
    b.require(receipt['request_sha256']==b.sha(b.canonical(wr)),'WITNESS_REQUEST_MISMATCH')
    checked=b.verify(raw,wr,b.sha(raw))
    accepted=(checked.get('status')==p.SUCCESS and receipt.get('before')==policy['inventory'] and receipt.get('after')==policy['inventory'])
    # An unsuccessful run is retained as signed evidence, never mathematical refutation.
    return {'schema':SCHEMA,'role':'separate_execution_witness','primary_key_sha256':b.sha(primary_key),
            'witness_key_sha256':b.sha(witness_key),'policy_sha256':b.sha(b.canonical(policy)),
            'primary_packet_sha256':policy['primary_packet_sha256'],'anchor_tip':anchor,
            'context_sha256':b.sha(b.canonical(context)),'primary_request_sha256':b.sha(b.canonical(request)),
            'witness_request_sha256':b.sha(b.canonical(wr)),'bundle_sha256':b.sha(raw),
            'receipt_sha256':b.sha(b.canonical(receipt)),
            'execution_status':'REEXECUTION_STRUCTURE_MATCHED_ONLY' if accepted else 'HOLD_EXECUTION_NOT_ADMITTED',**BOUNDARY}


def execute_and_issue(snapshot, policy, request, context, anchor, primary_key, witness_key, private_key):
    """Executor-owned path: no incoming receipt or model command is accepted."""
    try:
        wr=policy_check(policy,request,context,anchor,primary_key,witness_key)
        b.require(g.public_key(private_key)==witness_key,'WITNESS_SIGNER_KEY_MISMATCH')
        root=Path(snapshot)
        b.require(not root.is_symlink() and b.inventory(root,wr['seq'])==policy['inventory'],'WITNESS_INPUT_MISMATCH')
        raw=b.canonical(b.run(root,wr))
        payload=witness_payload(raw,policy,request,context,anchor,primary_key,witness_key)
        # Schema and role separate this payload from v0.11, using its established Ed25519 envelope.
        sig=g.sign(payload,private_key,witness_key)
        g.verify_signature(payload,sig,witness_key)
        return {'schema':SCHEMA,'status':'SIGNED_EXECUTION_WITNESS_ONLY','packet':b.canonical({'payload':payload,'signature_hex':sig.hex()}),'raw':raw,**BOUNDARY}
    except ERRORS as exc:
        return hold(str(exc) if type(exc) is ValueError else 'WITNESS_EXECUTION_UNAVAILABLE')


def verify_witness(packet, raw, policy, request, context, anchor, primary_key, witness_key):
    obj=p.strict(packet)
    b.require(type(obj) is dict and set(obj)=={'payload','signature_hex'},'WITNESS_PACKET_SCHEMA')
    sig=obj['signature_hex']; b.require(type(sig) is str and len(sig)==128,'WITNESS_SIGNATURE_ENCODING')
    signature=bytes.fromhex(sig); b.require(signature.hex()==sig,'WITNESS_SIGNATURE_ENCODING')
    g.verify_signature(obj['payload'],signature,witness_key)
    expected=witness_payload(raw,policy,request,context,anchor,primary_key,witness_key)
    b.require(b.canonical(obj['payload'])==b.canonical(expected),'WITNESS_PROJECTION_MISMATCH')
    return expected


def verify_pair(primary_packet, primary_raw, revision_log, seed, witness_packet, witness_raw,
                policy, request, context, anchor, primary_key, witness_key):
    """Verifier-owned policy and keys; both signatures and raw observations retained on disagreement."""
    evidence={}
    try:
        policy_check(policy,request,context,anchor,primary_key,witness_key)
        b.require(b.sha(primary_packet)==policy['primary_packet_sha256'],'PRIMARY_PACKET_BINDING')
        witness=verify_witness(witness_packet,witness_raw,policy,request,context,anchor,primary_key,witness_key)
        evidence['witness']=witness
        primary=g.verify(primary_packet,primary_raw,revision_log,seed,request,context,anchor,primary_key)
        b.require(primary['status']=='PUBLIC_SIGNATURE_AND_REPLAY_MATCHED_ONLY','PRIMARY_NOT_VERIFIED')
        evidence['primary']=primary['payload']
        b.require(witness['execution_status']=='REEXECUTION_STRUCTURE_MATCHED_ONLY','WITNESS_NOT_ADMITTED')
        b.require(b.sha(primary_raw)!=b.sha(witness_raw),'SAME_BUNDLE_REUSE')
        a=p.strict(primary_raw)['receipt']; z=p.strict(witness_raw)['receipt']
        b.require(a['before']==a['after']==z['before']==z['after']==policy['inventory'],'SNAPSHOT_INVENTORY_DISAGREEMENT')
        differences=[]
        for left,right in zip(a['processes'],z['processes']):
            if b.canonical(b.parse(left['stdout']))!=b.canonical(b.parse(right['stdout'])):
                differences.append(left['gate'])
        if differences:
            return hold('GATE_OUTPUT_DISAGREEMENT',disagreeing_gates=differences,**evidence)
        return {'schema':SCHEMA,'status':'SEPARATE_KEY_EXECUTION_REPORTS_AGREE_ONLY',
                'answer_status':primary['payload']['answer_status'],'compared_gate_count':len(b.GATES),
                **evidence,**BOUNDARY}
    except ERRORS as exc:
        return hold(str(exc) if type(exc) is ValueError else 'PAIR_VERIFICATION_UNAVAILABLE',**evidence)
