"""Separate trusted anchor journal; interrupted two-file commits fail closed."""
from __future__ import annotations
import os
from pathlib import Path
from runtime import kuuos_verifyos_interpretation_store_v0_9 as s

b, p, v = s.b, s.p, s.v
SCHEMA = 'kuuos.verifyos.interpretation-anchor.v0.10'
DDL = ('CREATE TABLE anchor_rows (sequence INTEGER PRIMARY KEY CHECK (sequence >= 0), '
       'parent_sha256 TEXT NOT NULL, row_sha256 TEXT NOT NULL UNIQUE, payload BLOB NOT NULL)')
BOUNDARY = {**s.BOUNDARY, 'independent_storage_authenticity_verified': False,
            'power_loss_recovery_verified': False}
ERRORS = s.ERRORS


def hold(reason):
    return {'schema': SCHEMA, 'status': 'HOLD', 'reason': reason,
            'anchor_snapshot_matched': False, **BOUNDARY}


def tip_check(tip):
    b.require(type(tip) is dict and set(tip) == {'sequence', 'sha256'} and
              type(tip['sequence']) is int and tip['sequence'] >= 0 and
              b.hex64(tip['sha256']), 'TIP_SCHEMA')


def separate(store, anchor):
    b.require(isinstance(store, Path) and isinstance(anchor, Path) and
              store.is_absolute() and anchor.is_absolute() and
              store.resolve() != anchor.resolve(), 'SEPARATE_PATHS_REQUIRED')
    if store.exists() and anchor.exists():
        b.require(not os.path.samefile(store, anchor), 'SEPARATE_FILES_REQUIRED')


def genesis_tip(seed_id):
    return {'sequence': 0, 'sha256': b.sha(s.row_bytes(seed_id, 0, s.ZERO, None))}


def row(seed_id, sequence, parent, operation, material):
    return b.canonical({'schema': SCHEMA, 'seed_sha256': seed_id,
                        'sequence': sequence, 'parent_sha256': parent,
                        'operation': operation, 'material': material})


def insert(db, seed_id, sequence, parent, operation, material):
    raw = row(seed_id, sequence, parent, operation, material)
    tip = {'sequence': sequence, 'sha256': b.sha(raw)}
    db.execute('INSERT INTO anchor_rows VALUES (?,?,?,?)',
               (sequence, parent, tip['sha256'], raw))
    return tip


def load(db, seed_id):
    schema = db.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'").fetchall()
    b.require(schema == [('table', 'anchor_rows', 'anchor_rows', DDL)], 'ANCHOR_SCHEMA')
    records = db.execute('SELECT sequence,parent_sha256,row_sha256,payload FROM anchor_rows ORDER BY sequence LIMIT ?',
                         (2*v.LIMIT+2,)).fetchall()
    b.require(1 <= len(records) <= 2*v.LIMIT+1, 'ANCHOR_LENGTH')
    parent = s.ZERO
    committed, pending = None, None
    for i, (seq, prev, digest, raw) in enumerate(records):
        b.require(seq == i and prev == parent and type(raw) is bytes and b.sha(raw) == digest, 'ANCHOR_CHAIN')
        obj = p.strict(raw); op, mat = obj['operation'], obj['material']
        b.require(raw == row(seed_id, i, parent, op, mat), 'ANCHOR_ROW_BINDING')
        if i == 0:
            b.require(op == 'GENESIS' and mat == genesis_tip(seed_id), 'ANCHOR_GENESIS')
            committed = mat
        elif op == 'PREPARE':
            b.require(pending is None and type(mat) is dict and set(mat) == {'previous', 'target', 'event_sha256'}, 'ANCHOR_PREPARE')
            tip_check(mat['previous']); tip_check(mat['target'])
            b.require(s.same_tip(mat['previous'], committed) and
                      mat['target']['sequence'] == committed['sequence']+1 and
                      mat['target']['sequence'] <= v.LIMIT and b.hex64(mat['event_sha256']), 'ANCHOR_TRANSITION')
            pending = mat
        else:
            b.require(op == 'SEAL' and pending is not None and mat == pending, 'ANCHOR_SEAL')
            committed, pending = pending['target'], None
        parent = digest
    return {'anchor_tip': {'sequence': len(records)-1, 'sha256': parent},
            'committed_tip': committed, 'pending': pending}


def checked_state(db, seed_id, expected):
    tip_check(expected)
    state = load(db, seed_id)
    b.require(s.same_tip(expected, state['anchor_tip']), 'ANCHOR_EXPECTATION_MISMATCH')
    return state


def store_snapshot(store, seed):
    snap = s.read(store, seed)
    b.require(snap['status'] == 'LOCAL_SNAPSHOT_REPLAYED_ONLY', 'STORE_REPLAY_FAILED')
    return snap


def match_store(actual, expected):
    tip_check(actual); tip_check(expected)
    if actual['sequence'] < expected['sequence']:
        raise ValueError('STORE_ROLLBACK_RELATIVE_TO_ANCHOR')
    if actual['sequence'] > expected['sequence']:
        raise ValueError('STORE_UNANCHORED_AHEAD')
    b.require(s.same_tip(expected, actual), 'STORE_DIVERGED_AT_ANCHORED_SEQUENCE')


def result(state, status, matched=False, **extra):
    return {'schema': SCHEMA, 'status': status, **state,
            'anchor_snapshot_matched': matched, **extra, **BOUNDARY}


def stop(db, exc):
    if db is not None:
        try: db.rollback()
        except s.sqlite3.Error: pass
    return hold(str(exc) if type(exc) is ValueError else 'STORAGE_UNCERTAIN_REOBSERVE_REQUIRED')


def initialize(store, anchor, seed, expected_genesis):
    db = None
    try:
        separate(store, anchor)
        fixed, seed_id, _ = s.seed_material(seed)
        tip_check(expected_genesis)
        b.require(s.same_tip(expected_genesis, genesis_tip(seed_id)), 'INDEPENDENT_GENESIS_REQUIRED')
        match_store(store_snapshot(store, fixed)['tip'], expected_genesis)
        b.require(anchor.parent.is_dir(), 'ANCHOR_PARENT_REQUIRED')
        fd = os.open(anchor, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600); os.close(fd)
        db = s.connect(anchor, 'rw'); db.execute('BEGIN IMMEDIATE'); db.execute(DDL)
        insert(db, seed_id, 0, s.ZERO, 'GENESIS', expected_genesis)
        state = load(db, seed_id); db.commit()
        return result(state, 'ANCHOR_GENESIS_RECORDED')
    except ERRORS as exc:
        return stop(db, exc)
    finally:
        if db is not None: db.close()


def read(store, anchor, seed, expected_anchor):
    db = None
    try:
        separate(store, anchor); fixed, seed_id, _ = s.seed_material(seed)
        db = s.connect(anchor, 'ro'); db.execute('BEGIN')
        state = checked_state(db, seed_id, expected_anchor)
        b.require(state['pending'] is None, 'PENDING_INTENT_REQUIRES_EXPLICIT_RECOVERY')
        snap = store_snapshot(store, fixed)
        match_store(snap['tip'], state['committed_tip'])
        db.commit(); return result(state, 'ANCHOR_MATCHED_SNAPSHOT_ONLY', True, inputs=snap['inputs'])
    except ERRORS as exc:
        return stop(db, exc)
    finally:
        if db is not None: db.close()


def intent(seed_id, previous, event_bytes, trusted_event_sha256, next_request, next_context):
    b.require(type(event_bytes) is bytes and b.hex64(trusted_event_sha256) and
              b.sha(event_bytes) == trusted_event_sha256, 'EVENT_ANCHOR_MISMATCH')
    event = p.strict(event_bytes)
    b.require(type(event) is dict and b.canonical(event['next_request']) == b.canonical(next_request) and
              b.canonical(event['next_context']) == b.canonical(next_context), 'NEXT_CONTEXT_MISMATCH')
    seq = previous['sequence']+1
    target = {'sequence': seq, 'sha256': b.sha(s.row_bytes(seed_id, seq, previous['sha256'], event))}
    return event, {'previous': previous, 'target': target, 'event_sha256': trusted_event_sha256}


def prepare(store, anchor, seed, expected_anchor, event_bytes, trusted_event_sha256, next_request, next_context):
    db = None
    try:
        separate(store, anchor); fixed, seed_id, _ = s.seed_material(seed)
        db = s.connect(anchor, 'rw'); db.execute('BEGIN IMMEDIATE')
        state = checked_state(db, seed_id, expected_anchor)
        b.require(state['pending'] is None, 'PENDING_INTENT_REQUIRES_EXPLICIT_RECOVERY')
        snap = store_snapshot(store, fixed); match_store(snap['tip'], state['committed_tip'])
        event, mat = intent(seed_id, snap['tip'], event_bytes, trusted_event_sha256, next_request, next_context)
        log = p.strict(snap['inputs']['revision_log']); log['events'].append(event)
        checked = v.replay(**s.replay_inputs(fixed, log, next_request, next_context))
        b.require(checked['status'] == v.OK, 'REVISION_INVALID')
        parent = state['anchor_tip']; insert(db, seed_id, parent['sequence']+1, parent['sha256'], 'PREPARE', mat)
        state = load(db, seed_id); db.commit()
        return result(state, 'INTENT_PREPARED_NOT_COMMITTED')
    except ERRORS as exc:
        return stop(db, exc)
    finally:
        if db is not None: db.close()


def resume(store, anchor, seed, expected_anchor, event_bytes, trusted_event_sha256, next_request, next_context):
    """Explicit recovery only for the exact durable intent; never accept an arbitrary tail."""
    db = None
    try:
        separate(store, anchor); fixed, seed_id, _ = s.seed_material(seed)
        db = s.connect(anchor, 'rw'); db.execute('BEGIN IMMEDIATE')
        state = checked_state(db, seed_id, expected_anchor)
        mat = state['pending']; b.require(mat is not None, 'NO_PREPARED_INTENT')
        _, wanted = intent(seed_id, state['committed_tip'], event_bytes, trusted_event_sha256, next_request, next_context)
        b.require(mat == wanted, 'PREPARED_INTENT_MISMATCH')
        snap = store_snapshot(store, fixed)
        if s.same_tip(mat['previous'], snap['tip']):
            appended = s.append(store, fixed, mat['previous'], event_bytes, trusted_event_sha256, next_request, next_context)
            b.require(appended['status'] == 'LOCAL_APPEND_COMMITTED' and
                      s.same_tip(mat['target'], appended['tip']), 'STORE_APPEND_UNCERTAIN_REOBSERVE_REQUIRED')
        else:
            match_store(snap['tip'], mat['target'])
        match_store(store_snapshot(store, fixed)['tip'], mat['target'])
        parent = state['anchor_tip']; insert(db, seed_id, parent['sequence']+1, parent['sha256'], 'SEAL', mat)
        state = load(db, seed_id); db.commit()
        return result(state, 'ANCHOR_SEALED')
    except ERRORS as exc:
        return stop(db, exc)
    finally:
        if db is not None: db.close()


def publish_snapshot(store, anchor, seed, expected_anchor, raw, admission, key, prior_packet):
    snap = read(store, anchor, seed, expected_anchor)
    if snap['status'] != 'ANCHOR_MATCHED_SNAPSHOT_ONLY':
        return snap
    packet = v.publish_question(raw, admission, key, prior_packet, **snap['inputs'])
    return result({k: snap[k] for k in ('anchor_tip', 'committed_tip', 'pending')},
                  'ANCHORED_SNAPSHOT_PACKET_ONLY', True, packet=packet)
