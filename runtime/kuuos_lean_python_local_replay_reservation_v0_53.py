"""v0.53: explicit, durable LOCAL replay ledger for two MAC-verified claims.

A separately chosen SQLite file records a pair as one BEGIN IMMEDIATE/
COMMIT transaction. Unique constraints reject old (key,context,sequence)
or (key,nonce) entries across reopened local connections. SQL uses INSERT
only for observations: this is *logical* append-only, not immutable storage.
The finite hash chain is not externally anchored and does not prevent an
attacker with DB write access from replacing the whole history.

Original PlanOS has not emitted three resulting Finsets. HMAC verification
does not authenticate independent human issuers, establish a common clock,
or license host actions. This module is the first explicitly state-writing
LOCAL observation layer; v0.52 and all original kernels stay read-only.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any

from runtime import kuuos_lean_python_local_mac_bound_plan_claims_v0_52 as mac
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA, _plain_copy, _fingerprint,
)

VERSION = "kuuos_lean_python_local_replay_reservation_v0_53"
LOCAL_RECORDED_PROPOSAL = "LOCAL_ATOMIC_REPLAY_LEDGER_RECORDED_PROPOSAL_ONLY"
LOCAL_RECORDED_OBSTRUCTION = "LOCAL_ATOMIC_REPLAY_LEDGER_RECORDED_OBSTRUCTION"
LOCAL_REPLAY_OBSTRUCTION = "LOCAL_ATOMIC_REPLAY_COLLISION_OBSTRUCTION"
SCHEMA_NAME = "kuuos_plan_mac_seen_v053"
CHAIN_DOMAIN = "KuuOS/PlanOS/LocalReplayLedger/sha256/v0.53"
GENESIS = "0" * 64
MAX_AUDIT_ROWS = 100000

# sqlite_master normalizes away IF NOT EXISTS; check the entire table schema
# before every write so an existing attacker-modified table cannot silently
# omit the unique constraints. The directory/file must be verifier-controlled.
_SCHEMA = """CREATE TABLE kuuos_plan_mac_seen_v053 (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_id TEXT NOT NULL,
    context_id TEXT NOT NULL,
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    nonce_hex TEXT NOT NULL,
    message_sha256 TEXT NOT NULL,
    previous_row_sha256 TEXT NOT NULL,
    row_sha256 TEXT NOT NULL,
    UNIQUE(key_id, context_id, sequence),
    UNIQUE(key_id, nonce_hex),
    UNIQUE(row_sha256)
)"""
_CREATE = _SCHEMA.replace("CREATE TABLE ", "CREATE TABLE IF NOT EXISTS ", 1)

UNPROVED = (
    "LOCAL_SQLITE_LOGICAL_APPEND_IS_NOT_IMMUTABLE_OR_EXTERNALLY_ANCHORED",
    "MAC_CHECKED_WITH_SEPARATELY_SUPPLIED_SYMMETRIC_VERIFIER_KEYS_ONLY",
    "LOCAL_KEY_NONCE_RESERVATION_IS_NOT_GLOBAL_CROSS_HOST_REPLAY_PROTECTION",
    "SEQUENCES_AND_NONCES_DO_NOT_PROVE_REAL_WORLD_CAUSAL_CLOCK",
    "DISTINCT_KEY_IDS_DO_NOT_PROVE_INDEPENDENT_REAL_WORLD_ISSUERS",
    "ORIGINAL_PLANOS_RESULT_SETS_NOT_EMITTED_AND_REMAIN_NO_DATA",
    "NO_LEAN_PROOF_OF_SQLITE_TRANSACTION_OR_HMAC_SECURITY",
    "NO_ORIGINAL_LEAN_TO_CPYTHON_REFINEMENT_OR_EXECUTION_AUTHORITY",
)


@dataclass(frozen=True)
class LocalReplayReservationAudit:
    status: str
    issues: tuple[str, ...] = ()
    conflicting_fields: tuple[str, ...] = ()
    original_plan_result_state: str = NO_DATA
    local_mac_verified: bool = False
    local_reservation_committed: bool = False
    local_rows_added: int = 0
    local_chain_head: str | None = None
    pairwise_agreement_proposal_only: bool = False
    original_results_observed: bool = False
    external_issuers_authenticated: bool = False
    cross_host_replay_protected: bool = False
    original_lean_match_proved: bool = False
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    native_kernel_invocations: int = 0
    unresolved: tuple[str, ...] = UNPROVED


def _halt(status: str, issues: tuple[str, ...],
          mac_result: Any = None) -> LocalReplayReservationAudit:
    return LocalReplayReservationAudit(
        status=status,
        issues=issues,
        conflicting_fields=tuple(getattr(mac_result, "conflicting_fields", ())),
        local_mac_verified=bool(getattr(mac_result, "local_mac_verified", False)),
    )


def _canonical_bytes(obj: dict) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def _hash_row(prev: str, key_id: str, context_id: str,
              sequence: int, nonce_hex: str, message_sha256: str) -> str:
    return hashlib.sha256(_canonical_bytes({
        "domain": CHAIN_DOMAIN,
        "previous_row_sha256": prev,
        "key_id": key_id,
        "context_id": context_id,
        "sequence": sequence,
        "nonce_hex": nonce_hex,
        "message_sha256": message_sha256,
    })).hexdigest()


def _validate_local_chain(db: sqlite3.Connection) -> str:
    schema = db.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
        (SCHEMA_NAME,),
    ).fetchone()
    triggers = db.execute(
        "SELECT name FROM sqlite_master WHERE type='trigger' AND tbl_name=?",
        (SCHEMA_NAME,),
    ).fetchone()
    if schema is None or schema[0] != _SCHEMA or triggers is not None:
        raise ValueError("untrusted_or_changed_local_ledger_schema")
    rows = db.execute(
        "SELECT key_id, context_id, sequence, nonce_hex, message_sha256, "
        "previous_row_sha256, row_sha256 "
        "FROM kuuos_plan_mac_seen_v053 ORDER BY entry_id LIMIT ?",
        (MAX_AUDIT_ROWS + 1,),
    ).fetchall()
    if len(rows) > MAX_AUDIT_ROWS:
        raise ValueError("local_ledger_audit_limit")
    prev = GENESIS
    for key_id, context_id, sequence, nonce_hex, msg, old_prev, row_hash in rows:
        actual = _hash_row(prev, key_id, context_id, sequence, nonce_hex, msg)
        if old_prev != prev or row_hash != actual:
            raise ValueError("local_ledger_chain_inconsistent")
        prev = actual
    return prev


def reserve_verified_mac_pair_locally(
    verify_certificate: Any,
    plan_certificate: Any,
    claims: Any = None,
    receipts: Any = None,
    *,
    verification_keys: Any = None,
    expected_context: Any = None,
    expected_sequences: Any = None,
    ledger_path: Any = None,
) -> LocalReplayReservationAudit:
    """Reserve both already-checked claims in ONE local SQLite transaction.

    Explicitly side-effecting only if a verifier supplies an absolute path.
    This function never creates/derives secrets or calls original kernels.
    """
    if type(claims) is not dict or type(receipts) is not dict:
        prior = mac.audit_locally_mac_bound_claims(
            verify_certificate, plan_certificate, claims, receipts,
            verification_keys=verification_keys,
            expected_context=expected_context,
            expected_sequences=expected_sequences,
        )
        return _halt(prior.status, tuple(prior.issues), prior)

    try:
        before = (_fingerprint(claims), _fingerprint(receipts))
        claims_copy = _plain_copy(claims, "claims", dict)
        receipts_copy = _plain_copy(receipts, "mac_receipts", dict)
        if before != (_fingerprint(claims), _fingerprint(receipts)):
            return _halt(BLOCKED, ("caller_inputs_changed_during_snapshot",))
    except (TypeError, ValueError, RecursionError, OverflowError):
        return _halt(BLOCKED, ("invalid_plain_claim_or_receipt_snapshot",))

    checked = mac.audit_locally_mac_bound_claims(
        verify_certificate, plan_certificate, claims_copy, receipts_copy,
        verification_keys=verification_keys,
        expected_context=expected_context,
        expected_sequences=expected_sequences,
    )
    if not checked.local_mac_verified:
        return _halt(checked.status, tuple(checked.issues), checked)
    if ledger_path is None:
        return _halt(NO_DATA, ("separately_selected_local_ledger_path_missing",), checked)
    if type(ledger_path) is not type(Path()) or not ledger_path.is_absolute():
        return _halt(BLOCKED, ("trusted_absolute_path_object_required",), checked)
    if (ledger_path.is_symlink() or not ledger_path.parent.is_dir()
            or (ledger_path.exists() and not ledger_path.is_file())):
        return _halt(BLOCKED, ("local_ledger_path_not_regular_or_parent_unavailable",),
                     checked)

    db: sqlite3.Connection | None = None
    try:
        db = sqlite3.connect(str(ledger_path), timeout=5, isolation_level=None)
        db.execute("PRAGMA synchronous=FULL")
        db.execute("BEGIN IMMEDIATE")
        db.execute(_CREATE)
        previous = _validate_local_chain(db)
        for slot in mac.SLOTS:
            receipt = receipts_copy[slot]
            message_sha = hashlib.sha256(
                mac._mac_message(slot, receipt, claims_copy[slot])
            ).hexdigest()
            values = (
                receipt["key_id"], receipt["context_id"], receipt["sequence"],
                receipt["nonce_hex"], message_sha,
            )
            new_digest = _hash_row(previous, *values)
            db.execute(
                "INSERT INTO kuuos_plan_mac_seen_v053 "
                "(key_id,context_id,sequence,nonce_hex,message_sha256,"
                "previous_row_sha256,row_sha256) VALUES (?,?,?,?,?,?,?)",
                (*values, previous, new_digest),
            )
            previous = new_digest
        db.commit()
        return LocalReplayReservationAudit(
            status=(LOCAL_RECORDED_OBSTRUCTION if checked.conflicting_fields
                    else LOCAL_RECORDED_PROPOSAL),
            issues=tuple(checked.issues) + UNPROVED,
            conflicting_fields=tuple(checked.conflicting_fields),
            local_mac_verified=True,
            local_reservation_committed=True,
            local_rows_added=2,
            local_chain_head=previous,
            pairwise_agreement_proposal_only=not bool(checked.conflicting_fields),
        )
    except sqlite3.IntegrityError:
        if db is not None:
            db.rollback()
        return _halt(
            LOCAL_REPLAY_OBSTRUCTION,
            ("seen_local_key_context_sequence_or_key_nonce",), checked,
        )
    except (sqlite3.DatabaseError, ValueError, OSError, TypeError) as exc:
        if db is not None:
            db.rollback()
        return _halt(BLOCKED, ("local_ledger_unverified:" + type(exc).__name__,),
                     checked)
    finally:
        if db is not None:
            db.close()


__all__ = (
    "VERSION", "LOCAL_RECORDED_PROPOSAL", "LOCAL_RECORDED_OBSTRUCTION",
    "LOCAL_REPLAY_OBSTRUCTION", "LocalReplayReservationAudit",
    "reserve_verified_mac_pair_locally",
)
