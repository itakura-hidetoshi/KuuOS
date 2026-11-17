"""Local in-process original receipt capture and independent read-only audit v0.8.

Capture mode is an EXPLICIT, isolated test-fixture builder. It temporarily
wraps the ORIGINAL native v1.3's two receipt constructors to observe their
real return values, restores the original function references, and does not
alter either returned receipt. The original bounded local fixture build has
its original permitted effects; the separate auditor below has NO effects.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
Neither capture nor digest equality certifies an external issuer's signature,
formal Lean descent, Lean/Python refinement, causal truth or any authority.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
from threading import Lock
from typing import Any
from unittest.mock import patch

from runtime import kuuos_qi_world_native_full_cycle_v1_3 as native
from runtime.kuuos_lean_python_native_cycle_ledger_replay_v0_7 import (
    BLOCKED, NO_DATA, SUCCESS as REPLAY_SUCCESS, NativeReplayAudit,
    audit_native_cycle_ledger,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json
from runtime.kuuos_plan_os_kernel_v0_1 import build_plan_phase_activation_receipt
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_replan_wa_activation_receipt,
)
from runtime.kuuos_plan_os_types_v0_1 import (
    plan_activation_receipt_digest,
)
from runtime.kuuos_decision_os_wa_types_v0_3 import (
    wa_activation_receipt_digest,
)
from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_lean_python_native_receipt_return_capture_v0_8"
SOURCE_MAIN = "8ac05b15890abef4a866d09ef97c59d1fb672f7c"
CAPTURE_MODE = "observed_in_process_original_v13_constructor_returns"
SUCCESS = "LOCAL_NATIVE_RECEIPT_RETURNS_MATCHED"

WA_EDGE = "DecisionOSWa->PlanOS"
PLAN_EDGE = "PlanOS->ActOS"
EDGES = (WA_EDGE, PLAN_EDGE)
CAPTURE_KEYS = frozenset((
    "version", "capture_mode", "native_cycle_digest",
    "wa_activation_receipt", "plan_activation_receipt",
    "return_sequence", "capture_sha256",
))
_CAPTURE_LOCK = Lock()


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      allow_nan=False, separators=(",", ":"))


def _hash(value: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def capture_digest(capture: dict[str, Any]) -> str:
    return _hash({key: val for key, val in capture.items()
                  if key != "capture_sha256"})


@dataclass(frozen=True)
class ReturnCaptureAudit:
    status: str
    violations: tuple[str, ...] = ()
    missing: tuple[str, ...] = ()
    native_replay: NativeReplayAudit | None = None
    capture_sha256: str | None = None
    wa_receipt_digest: str | None = None
    plan_receipt_digest: str | None = None
    source_main: str = SOURCE_MAIN
    observation_mode: str = CAPTURE_MODE
    original_constructor_returns_observed: bool = False
    local_fixture_integrity_checked: bool = False
    external_issuer_authenticated: bool = False
    historical_receipt_issuance_proved: bool = False
    formal_descent_certified: bool = False
    lean_python_refinement_proved: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    git_merge_authority_granted: bool = False


def build_captured_native_test_fixture(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Explicit **local test builder**, NOT a read-only audit or production route.

    Original native v1.3 builder runs unchanged except its two globally imported
    receipt constructors are temporarily wrapped by no-op observation shims.
    Their actual return values are copied *after* calling the originals. No
    synthetic, post-hoc reconstructed receipt substitutes for the observed one.
    Refuse preexisting fixture state. Intended for fresh TemporaryDirectory only.
    The lock protects this module's callers; other users of native globals must
    not run concurrently with this in-process instrumentation.
    """
    if not isinstance(root, Path) or not root.is_dir():
        raise ValueError("fresh_temporary_directory_path_required")
    if any((root / name).exists() for name in (
        "belief", "decision", "plural", "wa", "plan", "act", "downstream"
    )):
        raise ValueError("existing_native_fixture_must_not_be_overwritten")

    originals = (
        native.build_replan_wa_activation_receipt,
        native.build_plan_phase_activation_receipt,
    )
    if originals != (build_replan_wa_activation_receipt,
                     build_plan_phase_activation_receipt):
        raise ValueError("native_constructor_binding_drift")

    returned: dict[str, list[dict[str, Any]]] = {key: [] for key in EDGES}
    sequence: list[str] = []

    def observe(edge: str, original: Any):
        def wrapped(*args: Any, **kwargs: Any) -> dict[str, Any]:
            value = original(*args, **kwargs)
            # Snapshot the unmodified return object. The object passed to the
            # original native pipeline remains precisely the original return.
            returned[edge].append(_finite_json(value))
            sequence.append(edge)
            return value
        return wrapped

    with _CAPTURE_LOCK:
        # Test-only, bounded, synchronous instrumentation; automatically
        # restore both global references on success or exception.
        with patch.object(native, "build_replan_wa_activation_receipt",
                          observe(WA_EDGE, originals[0])), \
             patch.object(native, "build_plan_phase_activation_receipt",
                          observe(PLAN_EDGE, originals[1])):
            native_receipt = native.build_native_full_cycle_receipt(root)

    if sequence != list(EDGES) or any(len(returned[edge]) != 1 for edge in EDGES):
        raise ValueError("original_constructor_return_sequence_not_exact")
    receipt = _finite_json(native_receipt)
    capture = {
        "version": VERSION,
        "capture_mode": CAPTURE_MODE,
        "native_cycle_digest": receipt["native_full_cycle_receipt_digest"],
        "wa_activation_receipt": returned[WA_EDGE][0],
        "plan_activation_receipt": returned[PLAN_EDGE][0],
        "return_sequence": list(sequence),
        "capture_sha256": "",
    }
    capture["capture_sha256"] = capture_digest(capture)
    return receipt, capture


def _finish(errors: list[str], missing: list[str], replay: NativeReplayAudit | None,
            *, capture: dict[str, Any] | None = None) -> ReturnCaptureAudit:
    status = BLOCKED if errors else NO_DATA if missing else SUCCESS
    wa = capture.get("wa_activation_receipt") if capture is not None else None
    plan = capture.get("plan_activation_receipt") if capture is not None else None
    return ReturnCaptureAudit(
        status=status, violations=tuple(dict.fromkeys(errors)),
        missing=tuple(dict.fromkeys(missing)), native_replay=replay,
        capture_sha256=(capture.get("capture_sha256") if capture is not None else None),
        wa_receipt_digest=(wa.get("wa_activation_receipt_digest")
                           if type(wa) is dict else None),
        plan_receipt_digest=(plan.get("plan_activation_receipt_digest")
                             if type(plan) is dict else None),
        # Data supplied by an auditor's caller cannot independently prove that
        # it was genuinely observed, even if its full contents reproduce.
        original_constructor_returns_observed=False,
        local_fixture_integrity_checked=(status == SUCCESS),
    )


def audit_captured_native_receipts(
    root: Path,
    native_receipt: Any,
    capture_packet: Any,
) -> ReturnCaptureAudit:
    """Only read supplied snapshots and quiescent local original ActOS ledger.

    Source-bound equality is checked against whole original constructor
    receipt contents, plus the original native source's reference digests.
    The capture packet is NOT independently signed: a caller can fabricate
    its content; success only means local structural compatibility.
    """
    errors: list[str] = []
    missing: list[str] = []
    if capture_packet is None:
        return _finish(errors, ["capture_packet:missing"], None)
    if type(capture_packet) is not dict:
        return _finish(["capture_packet:plain_dict_required"], missing, None)
    try:
        packet = _finite_json(capture_packet)
    except (TypeError, ValueError, UnicodeError, RecursionError, OverflowError):
        return _finish(["capture_packet:invalid_json"], missing, None)

    if set(packet) != CAPTURE_KEYS:
        errors.append("capture_packet:field_inventory_mismatch")
        return _finish(errors, missing, None, capture=packet)
    if packet["version"] != VERSION or packet["capture_mode"] != CAPTURE_MODE:
        errors.append("capture_packet:version_or_mode_mismatch")
    if packet["return_sequence"] != list(EDGES):
        errors.append("capture_packet:return_order_or_count_mismatch")
    if type(packet["capture_sha256"]) is not str or packet["capture_sha256"] != capture_digest(packet):
        errors.append("capture_packet:checksum_mismatch")

    wa = packet["wa_activation_receipt"]
    plan = packet["plan_activation_receipt"]
    if type(wa) is not dict or type(plan) is not dict:
        errors.append("capture_packet:receipt_objects_required")
        return _finish(errors, missing, None, capture=packet)

    # Reuse v0.7's exact original native full-cycle/Act journal verification.
    # A different "real" effect or host authorization can never be invented here.
    replay = audit_native_cycle_ledger(root, native_receipt)
    if replay.status == BLOCKED:
        errors.extend("native_replay:" + e for e in replay.issues or ("blocked",))
        missing.extend("native_replay:" + e for e in replay.missing)
    elif replay.status == NO_DATA:
        missing.extend("native_replay:" + e for e in replay.missing or ("no_data",))
    elif replay.status != REPLAY_SUCCESS:
        errors.append("native_replay:unexpected_status")

    try:
        original = _finite_json(native_receipt)
    except (TypeError, ValueError, UnicodeError, RecursionError, OverflowError):
        errors.append("native_receipt:invalid_json")
        original = None
    artifacts = original.get("native_artifacts") if type(original) is dict else None
    if type(artifacts) is not dict:
        missing.append("native_artifacts:missing")
        return _finish(errors, missing, replay, capture=packet)
    if packet["native_cycle_digest"] != original.get("native_full_cycle_receipt_digest"):
        errors.append("capture_packet:native_cycle_binding_mismatch")

    try:
        if type(wa.get("wa_activation_receipt_digest")) is not str \
                or wa["wa_activation_receipt_digest"] != wa_activation_receipt_digest(wa):
            errors.append("captured_wa_receipt:original_hash_mismatch")
        if type(plan.get("plan_activation_receipt_digest")) is not str \
                or plan["plan_activation_receipt_digest"] != plan_activation_receipt_digest(plan):
            errors.append("captured_plan_receipt:original_hash_mismatch")
    except (TypeError, ValueError, KeyError, AttributeError, OverflowError) as exc:
        errors.append("captured_receipt:hash_exception:" + type(exc).__name__)

    try:
        # Compare full original returns, not only their digests.
        expected_wa = build_replan_wa_activation_receipt(
            state=artifacts["DecisionOSWa"],
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("native-full-cycle-replan-state"),
            replan_receipt_digest=sha("native-full-cycle-replan-receipt"),
            next_plan_basis_digest=sha("native-full-cycle-next-plan-basis"),
            now_ms=50_000,
        )
        expected_plan = build_plan_phase_activation_receipt(
            state=artifacts["PlanOS"],
            mission_cycle_phase="plan",
            mission_cycle_state_digest=sha("native-full-cycle-plan-phase-state"),
            plan_phase_receipt_digest=sha("native-full-cycle-plan-phase-receipt"),
            now_ms=80_000,
        )
        if wa != expected_wa:
            errors.append("captured_wa_receipt:whole_packet_mismatch")
        if plan != expected_plan:
            errors.append("captured_plan_receipt:whole_packet_mismatch")
        if artifacts["PlanOS"]["replan_activation_receipt_digest"] != wa.get("wa_activation_receipt_digest"):
            errors.append("captured_wa_receipt:plan_source_binding_mismatch")
        if artifacts["ActOS"]["plan_activation_receipt_digest"] != plan.get("plan_activation_receipt_digest"):
            errors.append("captured_plan_receipt:final_act_source_binding_mismatch")
        if replay.wa_activation_digest != wa.get("wa_activation_receipt_digest"):
            errors.append("captured_wa_receipt:replayed_source_mismatch")
        if replay.plan_activation_digest != plan.get("plan_activation_receipt_digest"):
            errors.append("captured_plan_receipt:replayed_source_mismatch")
    except (TypeError, KeyError, ValueError, AttributeError, OverflowError) as exc:
        errors.append("captured_receipt:original_builder_exception:" + type(exc).__name__)

    return _finish(errors, missing, replay, capture=packet)


__all__ = (
    "VERSION", "SOURCE_MAIN", "CAPTURE_MODE", "SUCCESS", "NO_DATA", "BLOCKED",
    "WA_EDGE", "PLAN_EDGE", "EDGES", "ReturnCaptureAudit", "capture_digest",
    "build_captured_native_test_fixture", "audit_captured_native_receipts",
)
