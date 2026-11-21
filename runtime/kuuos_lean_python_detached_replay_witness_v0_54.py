"""v0.54 detached, independently *recomputable* v0.53 local replay evidence.

This exports a non-secret snapshot of the local SQLite hash chain and
validates a detached JSON-shaped object WITHOUT a database or original
VerifyOS/PlanOS runtime. A separately supplied SHA-256 checkpoint VALUE
may be compared with the canonical snapshot; the provenance, custody,
time and independence of that checkpoint are deliberately not verified.

Recomputation is not authentication; self-consistency does not prevent a
database owner from rewriting all rows and recomputing the entire chain.
The original three PlanOS result Finsets remain NO_DATA.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import hmac
import json
from pathlib import Path
import sqlite3
from typing import Any
from urllib.parse import quote

from runtime import kuuos_lean_python_local_replay_reservation_v0_53 as replay
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA,
)

VERSION = "kuuos_lean_python_detached_replay_witness_v0_54"
MANIFEST_SCHEMA = "kuuos.planos.detached-replay-witness.v0.54"
DETACHED_UNANCHORED = "DETACHED_REPLAY_SELF_CONSISTENT_UNANCHORED_PROPOSAL_ONLY"
DETACHED_EXPORTED = "DETACHED_REPLAY_READ_ONLY_EXPORT_PROPOSAL_ONLY"
CHECKPOINT_MATCH = "CALLER_SUPPLIED_CHECKPOINT_VALUE_MATCH_PROPOSAL_ONLY"
CHECKPOINT_MISMATCH = "CALLER_SUPPLIED_CHECKPOINT_MISMATCH_OBSTRUCTION"
MAX_MANIFEST_BYTES = 16 * 1024 * 1024

ENTRY_KEYS = frozenset((
    "entry_id", "key_id", "context_id", "sequence", "nonce_hex",
    "message_sha256", "previous_row_sha256", "row_sha256",
))
MANIFEST_KEYS = frozenset((
    "schema", "source_boundary", "chain_domain", "genesis",
    "entries", "declared_chain_head",
))
UNPROVED = (
    "RECOMPUTED_CHAIN_IS_NOT_EXTERNAL_AUTHENTICATION",
    "CALLER_CHECKPOINT_VALUE_HAS_NO_VERIFIED_INDEPENDENT_CUSTODY",
    "NO_EXTERNAL_SIGNATURE_OR_ISSUER_PROVENANCE_PROOF",
    "NO_CROSS_HOST_REPLAY_OR_CAUSAL_TIME_PROOF",
    "NO_SHA256_SECURITY_OR_SQLITE_REFINEMENT_THEOREM_IN_LEAN",
    "ORIGINAL_PLANOS_THREE_RESULT_FINSETS_STILL_NO_DATA",
    "NO_GLOBAL_DESCENT_OR_HOST_EXECUTION_AUTHORITY",
)


@dataclass(frozen=True)
class DetachedReplayAudit:
    status: str
    issues: tuple[str, ...] = ()
    manifest: dict[str, Any] | None = None
    manifest_sha256: str | None = None
    chain_head: str | None = None
    entry_count: int = 0
    local_chain_recomputed: bool = False
    caller_checkpoint_value_matches: bool = False
    independent_checkpoint_custody_authenticated: bool = False
    original_plan_result_state: str = NO_DATA
    external_issuers_authenticated: bool = False
    cross_host_replay_protected: bool = False
    original_lean_match_proved: bool = False
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    native_kernel_invocations: int = 0
    unresolved: tuple[str, ...] = UNPROVED


def _sha256_shape(value: Any) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(ch in "0123456789abcdef" for ch in value)
    )


def _canonical(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def verify_detached_replay_witness(
    manifest: Any, *, separately_supplied_checkpoint_sha256: Any = None,
) -> DetachedReplayAudit:
    """Pure offline verification: no DB, keys, network or original OS calls.

    A matching caller-provided checkpoint is a value equality ONLY.
    The caller must establish any independent custody through other means.
    """
    if manifest is None:
        return DetachedReplayAudit(NO_DATA, ("detached_manifest_missing",))
    try:
        raw = _canonical(manifest)
        if len(raw) > MAX_MANIFEST_BYTES:
            return DetachedReplayAudit(BLOCKED, ("manifest_size_limit",))
        copied = json.loads(raw)
    except (TypeError, ValueError, OverflowError, RecursionError, UnicodeError):
        return DetachedReplayAudit(BLOCKED, ("invalid_detached_manifest_json",))

    if type(copied) is not dict or frozenset(copied) != MANIFEST_KEYS:
        return DetachedReplayAudit(BLOCKED, ("invalid_manifest_schema_keys",))
    if (copied["schema"] != MANIFEST_SCHEMA
            or copied["source_boundary"] != replay.VERSION
            or copied["chain_domain"] != replay.CHAIN_DOMAIN
            or copied["genesis"] != replay.GENESIS):
        return DetachedReplayAudit(BLOCKED, ("detached_manifest_domain_mismatch",))
    entries = copied["entries"]
    if (type(entries) is not list or len(entries) == 0
            or len(entries) > replay.MAX_AUDIT_ROWS
            or len(entries) % 2 != 0):
        return DetachedReplayAudit(BLOCKED, ("invalid_pairwise_entry_count",))
    if not _sha256_shape(copied["declared_chain_head"]):
        return DetachedReplayAudit(BLOCKED, ("invalid_declared_chain_head",))

    prev = replay.GENESIS
    seen_sequence = set()
    seen_nonce = set()
    for expected_id, entry in enumerate(entries, start=1):
        if type(entry) is not dict or frozenset(entry) != ENTRY_KEYS:
            return DetachedReplayAudit(BLOCKED, ("invalid_entry_fields",))
        if type(entry["entry_id"]) is not int or entry["entry_id"] != expected_id:
            return DetachedReplayAudit(BLOCKED, ("discontinuous_entry_identity",))
        for key in ("key_id", "context_id", "nonce_hex"):
            if (type(entry[key]) is not str or not entry[key]
                    or len(entry[key]) > 1024):
                return DetachedReplayAudit(BLOCKED, ("invalid_entry_identifier",))
        if type(entry["sequence"]) is not int or entry["sequence"] <= 0:
            return DetachedReplayAudit(BLOCKED, ("invalid_entry_sequence",))
        if (not _sha256_shape(entry["message_sha256"])
                or not _sha256_shape(entry["row_sha256"])
                or not _sha256_shape(entry["previous_row_sha256"])):
            return DetachedReplayAudit(BLOCKED, ("invalid_entry_digest_shape",))
        seq_key = (entry["key_id"], entry["context_id"], entry["sequence"])
        nonce_key = (entry["key_id"], entry["nonce_hex"])
        if seq_key in seen_sequence or nonce_key in seen_nonce:
            return DetachedReplayAudit(BLOCKED, ("duplicate_local_reservation_key",))
        seen_sequence.add(seq_key)
        seen_nonce.add(nonce_key)
        actual = replay._hash_row(
            prev, entry["key_id"], entry["context_id"],
            entry["sequence"], entry["nonce_hex"], entry["message_sha256"],
        )
        if (not hmac.compare_digest(entry["previous_row_sha256"], prev)
                or not hmac.compare_digest(entry["row_sha256"], actual)):
            return DetachedReplayAudit(BLOCKED, ("detached_replay_chain_inconsistent",))
        prev = actual
    if not hmac.compare_digest(prev, copied["declared_chain_head"]):
        return DetachedReplayAudit(BLOCKED, ("declared_chain_head_inconsistent",))

    manifest_sha = hashlib.sha256(raw).hexdigest()
    baseline = DetachedReplayAudit(
        DETACHED_UNANCHORED, manifest_sha256=manifest_sha,
        chain_head=prev, entry_count=len(entries), local_chain_recomputed=True,
    )
    if separately_supplied_checkpoint_sha256 is None:
        return baseline
    if not _sha256_shape(separately_supplied_checkpoint_sha256):
        return replace(baseline, status=BLOCKED,
                       issues=("invalid_separate_checkpoint_sha256",))
    if not hmac.compare_digest(
            manifest_sha, separately_supplied_checkpoint_sha256):
        return replace(baseline, status=CHECKPOINT_MISMATCH,
                       issues=("separately_supplied_checkpoint_disagrees",))
    return replace(baseline, status=CHECKPOINT_MATCH,
                   caller_checkpoint_value_matches=True)


def export_detached_local_replay_witness(ledger_path: Any) -> DetachedReplayAudit:
    """Read-only snapshot of a verifier-selected, pre-existing v0.53 DB.

    Never creates a DB or exports raw HMAC keys, MAC tags or original claims.
    Use verify_detached_replay_witness elsewhere, without the DB.
    """
    if ledger_path is None:
        return DetachedReplayAudit(NO_DATA, ("local_ledger_path_missing",))
    if type(ledger_path) is not type(Path()) or not ledger_path.is_absolute():
        return DetachedReplayAudit(BLOCKED, ("trusted_absolute_path_required",))
    if ledger_path.is_symlink() or not ledger_path.is_file():
        return DetachedReplayAudit(BLOCKED, ("preexisting_regular_ledger_required",))
    db = None
    try:
        uri = "file:" + quote(str(ledger_path), safe="/") + "?mode=ro"
        db = sqlite3.connect(uri, uri=True, isolation_level=None, timeout=5)
        db.execute("PRAGMA query_only=ON")
        db.execute("BEGIN")
        head = replay._validate_local_chain(db)
        rows = db.execute(
            "SELECT entry_id,key_id,context_id,sequence,nonce_hex,"
            "message_sha256,previous_row_sha256,row_sha256 "
            "FROM kuuos_plan_mac_seen_v053 ORDER BY entry_id LIMIT ?",
            (replay.MAX_AUDIT_ROWS + 1,),
        ).fetchall()
        manifest = {
            "schema": MANIFEST_SCHEMA,
            "source_boundary": replay.VERSION,
            "chain_domain": replay.CHAIN_DOMAIN,
            "genesis": replay.GENESIS,
            "entries": [dict(zip((
                "entry_id", "key_id", "context_id", "sequence", "nonce_hex",
                "message_sha256", "previous_row_sha256", "row_sha256",
            ), row)) for row in rows],
            "declared_chain_head": head,
        }
        checked = verify_detached_replay_witness(manifest)
        if checked.status != DETACHED_UNANCHORED:
            return replace(checked, status=BLOCKED,
                           issues=checked.issues + ("export_not_verified",))
        return replace(checked, status=DETACHED_EXPORTED, manifest=manifest)
    except (sqlite3.DatabaseError, ValueError, OSError, TypeError) as exc:
        return DetachedReplayAudit(
            BLOCKED, ("local_detached_export_failed:" + type(exc).__name__,),
        )
    finally:
        if db is not None:
            db.close()


__all__ = (
    "VERSION", "MANIFEST_SCHEMA", "DETACHED_UNANCHORED", "DETACHED_EXPORTED",
    "CHECKPOINT_MATCH", "CHECKPOINT_MISMATCH", "DetachedReplayAudit",
    "verify_detached_replay_witness", "export_detached_local_replay_witness",
)
