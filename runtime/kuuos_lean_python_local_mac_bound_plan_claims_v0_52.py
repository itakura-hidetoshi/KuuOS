"""v0.52: independently provisioned symmetric-key MAC checks for two claims.

Only HMAC-SHA256 integrity relative to separate verifier-supplied 32+ byte
secrets and exact declared context/sequence is checked. No key is derived
from a claim; no shared secret is returned or logged. A MAC does not prove
that an original PlanOS v1.03 kernel actually produced un-emitted result sets,
nor independently authenticated real-world issuers, nor freshness/replay
exclusion across calls. Caller declarations remain proposal or obstruction.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
import re
from typing import Any

from runtime import kuuos_lean_python_two_declared_plan_result_claims_v0_51 as prior
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA, _plain_copy, _fingerprint,
)

VERSION = "kuuos_lean_python_local_mac_bound_plan_claims_v0_52"
SCHEMA = "kuuos.plan-local-mac-bound-claims.v0.52"
DOMAIN = "KuuOS/PlanOS/TwoDeclaredResultClaims/HMAC-SHA256/v0.52"
MAC_CHECKED_PROPOSAL = "MAC_CHECKED_LOCAL_AGREEMENT_PROPOSAL_ONLY"
MAC_CHECKED_OBSTRUCTION = "MAC_CHECKED_LOCAL_DISAGREEMENT_OBSTRUCTION"
RECEIPT_FIELDS = frozenset((
    "schema_version", "key_id", "context_id", "sequence",
    "nonce_hex", "mac_sha256",
))
SLOTS = ("first", "second")
HEX_32 = re.compile(r"^[a-f0-9]{32}$")
HEX_64 = re.compile(r"^[a-f0-9]{64}$")
LABEL = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{0,127}$")
UNPROVED = (
    "SYMMETRIC_MAC_ONLY_PROVES_POSSESSION_OF_A_VERIFIER_PROVISIONED_KEY",
    "KEY_ID_DOES_NOT_AUTHENTICATE_AN_INDEPENDENT_REAL_WORLD_ISSUER",
    "CALLER_SEQUENCES_DO_NOT_ESTABLISH_A_COMMON_CAUSAL_CLOCK",
    "NO_PERSISTENT_REPLAY_LEDGER_OR_FRESHNESS_CERTIFICATE",
    "ORIGINAL_PLANOS_RESULT_FINSETS_REMAIN_NOT_EMITTED",
    "NO_LEAN_PROOF_OF_HMAC_SECURITY_OR_PYTHON_TO_ORIGINAL_MATCH",
    "NO_GLOBAL_DESCENT_OR_HOST_EXECUTION_AUTHORITY",
)


@dataclass(frozen=True)
class LocalMacBoundPlanClaimsAudit:
    status: str
    issues: tuple[str, ...] = ()
    conflicting_fields: tuple[str, ...] = ()
    declared_key_ids: tuple[str, ...] = ()
    local_mac_verified: bool = False
    source_projection_checked: bool = False
    original_plan_result_state: str = NO_DATA
    bounded_pairwise_agreement: bool = False
    original_result_sets_observed: bool = False
    independent_issuers_authenticated: bool = False
    original_lean_equality_proved: bool = False
    causal_event_identity_proved: bool = False
    persistent_replay_protection_proved: bool = False
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    native_kernel_invocations: int = 0
    read_only: bool = True
    unproved: tuple[str, ...] = UNPROVED


def _stop(status: str, *issues: str, pair=None, keys=()):
    return LocalMacBoundPlanClaimsAudit(
        status=status,
        issues=tuple(dict.fromkeys(issues)),
        conflicting_fields=tuple(getattr(pair, "conflicting_fields", ())),
        declared_key_ids=tuple(keys),
        source_projection_checked=bool(getattr(pair, "original_source_projection_checked", False)),
    )


def _label(value: Any) -> bool:
    return type(value) is str and LABEL.fullmatch(value) is not None


def _mac_message(slot: str, receipt: dict, claim: dict) -> bytes:
    """Canonical domain separated MAC input; never includes the verification key."""
    payload = {
        "domain": DOMAIN,
        "schema_version": SCHEMA,
        "slot": slot,
        "key_id": receipt["key_id"],
        "context_id": receipt["context_id"],
        "sequence": receipt["sequence"],
        "nonce_hex": receipt["nonce_hex"],
        "declared_claim": claim,
    }
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def audit_locally_mac_bound_claims(
    verify_certificate: Any,
    plan_certificate: Any,
    claims: Any = None,
    mac_receipts: Any = None,
    *,
    verification_keys: Any = None,
    expected_context: Any = None,
    expected_sequences: Any = None,
) -> LocalMacBoundPlanClaimsAudit:
    """Require separately provided MAC keys and exact context/sequence bindings.

    Keys and expected values are verifier inputs, NOT trusted just because a
    request contains them. The caller must establish trust out of band.
    """
    pair = prior.audit_two_declared_plan_result_claims(
        verify_certificate, plan_certificate, claims,
    )
    if pair.status not in (prior.PROPOSAL_ONLY, prior.OBSTRUCTION):
        return _stop(pair.status, *pair.issues, pair=pair)
    if mac_receipts is None or verification_keys is None or expected_context is None or expected_sequences is None:
        return _stop(NO_DATA, "independent_mac_verification_inputs_missing", pair=pair)
    if type(mac_receipts) is not dict or set(mac_receipts) != set(SLOTS):
        return _stop(BLOCKED, "exact_two_mac_receipts_required", pair=pair)
    if type(verification_keys) is not dict or not verification_keys:
        return _stop(BLOCKED, "verifier_keyring_required", pair=pair)
    if not _label(expected_context):
        return _stop(BLOCKED, "verifier_context_invalid", pair=pair)
    if type(expected_sequences) is not dict or set(expected_sequences) != set(SLOTS):
        return _stop(BLOCKED, "exact_verifier_sequences_required", pair=pair)
    if any(type(expected_sequences[s]) is not int or expected_sequences[s] <= 0
           for s in SLOTS):
        return _stop(BLOCKED, "verifier_sequences_invalid", pair=pair)
    for key_id, secret in verification_keys.items():
        if not _label(key_id) or type(secret) is not bytes or len(secret) < 32:
            return _stop(BLOCKED, "verifier_keyring_invalid", pair=pair)

    try:
        copied = _plain_copy(mac_receipts, "mac_receipts", dict)
        before = _fingerprint(copied)
        original_claims_digest = _fingerprint(claims)
    except (TypeError, ValueError, RecursionError, OverflowError) as exc:
        return _stop(BLOCKED, "invalid_finite_mac_receipts:" + type(exc).__name__,
                     pair=pair)

    seen_ids: list[str] = []
    seen_nonces: list[str] = []
    for slot in SLOTS:
        item = copied[slot]
        if type(item) is not dict or set(item) != RECEIPT_FIELDS:
            return _stop(BLOCKED, slot + ":mac_receipt_schema_invalid", pair=pair,
                         keys=seen_ids)
        key_id = item.get("key_id")
        if (item.get("schema_version") != SCHEMA or type(item.get("schema_version")) is not str
                or not _label(key_id) or not _label(item.get("context_id"))
                or type(item.get("sequence")) is not int
                or item["sequence"] <= 0
                or type(item.get("nonce_hex")) is not str
                or HEX_32.fullmatch(item["nonce_hex"]) is None
                or type(item.get("mac_sha256")) is not str
                or HEX_64.fullmatch(item["mac_sha256"]) is None):
            return _stop(BLOCKED, slot + ":mac_fields_not_exact", pair=pair,
                         keys=seen_ids)
        if item["context_id"] != expected_context or item["sequence"] != expected_sequences[slot]:
            return _stop(BLOCKED, slot + ":context_or_sequence_not_verifier_bound",
                         pair=pair, keys=seen_ids)
        if key_id not in verification_keys:
            return _stop(NO_DATA, slot + ":verification_key_not_provisioned",
                         pair=pair, keys=seen_ids)
        if key_id in seen_ids:
            return _stop(BLOCKED, "duplicate_verification_key_id", pair=pair,
                         keys=seen_ids)
        if item["nonce_hex"] in seen_nonces:
            return _stop(BLOCKED, "duplicate_nonce_within_pair", pair=pair,
                         keys=seen_ids)
        try:
            expected = hmac.new(
                verification_keys[key_id],
                _mac_message(slot, item, claims[slot]),
                hashlib.sha256,
            ).hexdigest()
        except (TypeError, ValueError, OverflowError, RecursionError):
            return _stop(BLOCKED, slot + ":canonical_mac_message_invalid",
                         pair=pair, keys=seen_ids)
        if not hmac.compare_digest(expected, item["mac_sha256"]):
            return _stop(BLOCKED, slot + ":mac_tag_invalid", pair=pair,
                         keys=seen_ids)
        seen_ids.append(key_id)
        seen_nonces.append(item["nonce_hex"])
    try:
        unchanged = before == _fingerprint(mac_receipts) and (
            original_claims_digest == _fingerprint(claims))
    except (TypeError, ValueError, RecursionError, OverflowError):
        unchanged = False
    if not unchanged:
        return _stop(BLOCKED, "source_changed_during_read_only_mac_check",
                     pair=pair, keys=seen_ids)
    return LocalMacBoundPlanClaimsAudit(
        status=(MAC_CHECKED_OBSTRUCTION if pair.conflicting_fields
                else MAC_CHECKED_PROPOSAL),
        issues=tuple(pair.issues) + UNPROVED,
        conflicting_fields=tuple(pair.conflicting_fields),
        declared_key_ids=tuple(seen_ids),
        local_mac_verified=True,
        source_projection_checked=True,
        original_plan_result_state=NO_DATA,
        bounded_pairwise_agreement=not bool(pair.conflicting_fields),
    )


__all__ = (
    "VERSION", "SCHEMA", "DOMAIN", "MAC_CHECKED_PROPOSAL",
    "MAC_CHECKED_OBSTRUCTION", "RECEIPT_FIELDS", "SLOTS", "UNPROVED",
    "LocalMacBoundPlanClaimsAudit", "audit_locally_mac_bound_claims",
)
