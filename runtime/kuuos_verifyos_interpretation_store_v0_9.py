"""Single trusted SQLite file: transactional append/CAS of v0.8 revisions."""
from __future__ import annotations
import os
from pathlib import Path
import sqlite3
from runtime import kuuos_verifyos_interpretation_revision_v0_8 as v

b, p, r = v.b, v.p, v.r
SCHEMA = 'kuuos.verifyos.interpretation-store.v0.9'
ZERO = '0' * 64
TABLE = 'revision_rows'
DDL = ('CREATE TABLE revision_rows (sequence INTEGER PRIMARY KEY CHECK (sequence >= 0), '
       'parent_sha256 TEXT NOT NULL, row_sha256 TEXT NOT NULL UNIQUE, payload BLOB NOT NULL)')
BOUNDARY = {**v.BOUNDARY, 'external_rollback_prevention_verified': False,
            'cross_database_atomicity_verified': False, 'current_at_delivery_verified': False}
ERRORS = (*v.ERRORS, sqlite3.Error)
SEED_FIELDS = {'question','candidate','base_request','base_context','base_log','base_anchor'}


def seed_material(seed):
    b.require(type(seed) is dict and set(seed) == SEED_FIELDS, 'SEED_SCHEMA')
    # Freeze mutable request/context at the API boundary. Host retains original anchors.
    fixed = dict(seed)
    for k in ('base_request','base_context'):
        fixed[k] = p.strict(b.canonical(seed[k]))
    for k in ('question','candidate','base_log'):
        b.require(type(fixed[k]) is bytes and len(fixed[k]) <= p.MAX_BYTES, 'SEED_BYTES')
    prior = r.replay(*(fixed[k] for k in ('question','candidate','base_request','base_context','base_log','base_anchor')))
    b.require(prior['status'] == 'REFINEMENT_CHECKED_BOUNDED_ONLY', 'INVALID_SEED')
    fingerprint = v.digest({'schema':SCHEMA, 'question':b.sha(fixed['question']),
        'candidate':b.sha(fixed['candidate']), 'base_log':b.sha(fixed['base_log']),
        'base_anchor':fixed['base_anchor'], 'request':v.digest(fixed['base_request']),
        'context':v.digest(fixed['base_context'])})
    return fixed, fingerprint, v.empty_log(prior, fixed['base_context'])


def connect(path, mode):
    b.require(isinstance(path, Path) and path.is_absolute() and path.is_file() and not path.is_symlink(), 'TRUSTED_EXISTING_PATH_REQUIRED')
    db = sqlite3.connect(path.as_uri() + '?mode=' + mode, uri=True, timeout=5, isolation_level=None)
    try:
        db.execute('PRAGMA trusted_schema=OFF')
        if mode == 'rw':
            db.execute('PRAGMA synchronous=FULL')
        return db
    except BaseException:
        db.close(); raise


def row_bytes(seed_id, sequence, parent, event):
    return b.canonical({'schema':SCHEMA,'seed_sha256':seed_id,'sequence':sequence,
                        'parent_sha256':parent,'event':event})


def insert(db, seed_id, sequence, parent, event):
    raw = row_bytes(seed_id, sequence, parent, event)
    b.require(len(raw) <= p.MAX_BYTES, 'ROW_SIZE')
    digest = b.sha(raw)
    db.execute('INSERT INTO revision_rows VALUES (?,?,?,?)', (sequence,parent,digest,raw))
    return {'sequence':sequence,'sha256':digest}


def replay_inputs(seed, log, request, context):
    raw = b.canonical(log)
    return {**seed,'revision_log':raw,'revision_anchor':b.sha(raw),
            'current_request':request,'current_context':context}


def load(db, seed, seed_id, log):
    schema = db.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'").fetchall()
    b.require(schema == [('table',TABLE,TABLE,DDL)], 'STORE_SCHEMA_MISMATCH')
    records = db.execute('SELECT sequence,parent_sha256,row_sha256,payload FROM revision_rows ORDER BY sequence LIMIT ?', (v.LIMIT+2,)).fetchall()
    b.require(1 <= len(records) <= v.LIMIT+1, 'STORE_LENGTH')
    parent = ZERO
    request, context = seed['base_request'], seed['base_context']
    for i, (sequence, previous, digest, raw) in enumerate(records):
        b.require(sequence == i and previous == parent and type(raw) is bytes and b.sha(raw) == digest, 'ROW_CHAIN_MISMATCH')
        value = p.strict(raw)
        event = value['event']
        b.require(raw == row_bytes(seed_id,i,parent,event), 'ROW_BINDING_MISMATCH')
        if i == 0:
            b.require(event is None, 'GENESIS_EVENT')
        else:
            b.require(type(event) is dict, 'EVENT_REQUIRED')
            log['events'].append(event)
            request,context = event['next_request'],event['next_context']
        parent = digest
    inputs = replay_inputs(seed,log,request,context)
    checked = v.replay(**inputs)
    b.require(checked['status'] == v.OK, 'STORED_REVISION_INVALID')
    return {'sequence':len(records)-1,'sha256':parent}, inputs, checked


def hold(reason):
    return {'schema':SCHEMA,'status':'HOLD','reason':reason,'tip':None,
            'local_append_commit_confirmed':False,**BOUNDARY}


def observed(tip, inputs, checked, committed=False):
    return {'schema':SCHEMA,'status':'LOCAL_APPEND_COMMITTED' if committed else 'LOCAL_SNAPSHOT_REPLAYED_ONLY',
            'tip':tip,'inputs':inputs,'active_ids':checked['active_ids'],
            'local_append_commit_confirmed':committed,**BOUNDARY}


def stop(db, exc):
    if db is not None:
        try: db.rollback()
        except sqlite3.Error: pass
    return hold(str(exc) if type(exc) is ValueError else 'STORE_ERROR_REOBSERVE_REQUIRED')


def initialize(path, seed):
    """Explicit create-only operation. A failed initialization is not silently deleted."""
    db = None
    try:
        fixed, seed_id, log = seed_material(seed)
        b.require(isinstance(path, Path) and path.is_absolute() and path.parent.is_dir(), 'TRUSTED_PATH_REQUIRED')
        fd = os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600); os.close(fd)
        db = connect(path,'rw'); db.execute('BEGIN IMMEDIATE'); db.execute(DDL)
        insert(db,seed_id,0,ZERO,None)
        tip, inputs, checked = load(db,fixed,seed_id,log)
        result = observed(tip,inputs,checked)
        db.commit(); return result
    except ERRORS as exc:
        return stop(db,exc)
    finally:
        if db is not None: db.close()


def read(path, seed):
    """Read-only transaction; result refers to this snapshot, not delivery time."""
    db = None
    try:
        fixed, seed_id, log = seed_material(seed)
        db = connect(path,'ro'); db.execute('BEGIN')
        result = observed(*load(db,fixed,seed_id,log)); db.commit(); return result
    except ERRORS as exc:
        return stop(db,exc)
    finally:
        if db is not None: db.close()


def same_tip(expected, actual):
    return (type(expected) is dict and set(expected) == {'sequence','sha256'}
            and type(expected['sequence']) is int and expected == actual)


def append(path, seed, expected_tip, event_bytes, trusted_event_sha256, next_request, next_context):
    """Host-captured event and independent expected tip. Never create on append."""
    db = None
    try:
        fixed, seed_id, log = seed_material(seed)
        b.require(type(event_bytes) is bytes and b.hex64(trusted_event_sha256) and b.sha(event_bytes) == trusted_event_sha256, 'EVENT_ANCHOR_MISMATCH')
        event = p.strict(event_bytes)
        b.require(type(event) is dict, 'EVENT_SCHEMA')
        req, ctx = p.strict(b.canonical(next_request)), p.strict(b.canonical(next_context))
        b.require(b.canonical(event['next_request']) == b.canonical(req) and b.canonical(event['next_context']) == b.canonical(ctx), 'NEXT_CONTEXT_MISMATCH')
        db = connect(path,'rw'); db.execute('BEGIN IMMEDIATE')
        tip, inputs, _ = load(db,fixed,seed_id,log)
        b.require(same_tip(expected_tip,tip), 'STALE_EXPECTED_TIP')
        log['events'].append(event)
        inputs = replay_inputs(fixed,log,req,ctx)
        checked = v.replay(**inputs)
        b.require(checked['status'] == v.OK, 'REVISION_INVALID:'+str(checked.get('reason')))
        tip = insert(db,seed_id,tip['sequence']+1,tip['sha256'],event)
        result = observed(tip,inputs,checked,True)
        db.commit(); return result
    except ERRORS as exc:
        return stop(db,exc)
    finally:
        if db is not None: db.close()


def publish_snapshot_at_tip(path, seed, expected_tip, raw, admission, key, prior_packet):
    """Bind v0.8 egress to a read snapshot. A later commit may change the active view."""
    snapshot = read(path,seed)
    if snapshot['status'] != 'LOCAL_SNAPSHOT_REPLAYED_ONLY' or not same_tip(expected_tip,snapshot['tip']):
        return hold('SNAPSHOT_OR_TIP_UNVERIFIED')
    packet = v.publish_question(raw,admission,key,prior_packet,**snapshot['inputs'])
    return {'schema':SCHEMA,'status':'SNAPSHOT_PACKET_ONLY','tip':snapshot['tip'],
            'packet':packet,**BOUNDARY}
