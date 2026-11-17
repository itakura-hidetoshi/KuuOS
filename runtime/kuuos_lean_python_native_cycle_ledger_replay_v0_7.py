"""Source-pinned native full-cycle replay for Lean/Python OS links (v0.7).

An explicit *fixture* witness, not a Lean descent proof or receipt issuer.
This auditor performs no host call or repository/store write. It reads a
quiescent local native full-cycle fixture, replays the original ActOS ledger,
and compares three genuine contiguous OS segments via the v0.6 auditor.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
from typing import Any

from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    PASS as PATH_PASS,
    PathAudit,
    _finite_json,
    audit_typed_path,
)
from runtime.kuuos_act_os_store_v0_1 import ActStore
from runtime.kuuos_plan_os_kernel_v0_1 import build_plan_phase_activation_receipt
from runtime.kuuos_decision_os_wa_kernel_v0_3 import build_replan_wa_activation_receipt
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    CYCLE_ID,
    RECEIPT_VERSION,
    validate_native_full_cycle_receipt,
)

VERSION = "kuuos_lean_python_native_cycle_ledger_replay_v0_7"
SOURCE_MAIN = "489f7dcc80c892965f36cf0915669283ee14f679"

SUCCESS = "NATIVE_FIXTURE_LINKS_REPLAYED"
NO_DATA = "NO_DATA"
BLOCKED = "BLOCKED"

EXPECTED_OS = (
    "DecisionOS", "DecisionOSPlural", "DecisionOSWa", "PlanOS",
    "ActOS", "ObserveOS", "VerifyOS", "LearnOS",
)
EXPECTED_NATIVE_ARTIFACTS = frozenset(
    EXPECTED_OS + ("BeliefOSState", "BeliefOSReceipt")
)
ACT_STORE_FILES = (
    "act-genesis.json", "act-ledger.jsonl", "act-snapshot.json",
)
MODE = "deterministic_receipt_reconstruction_checked_against_original_state_digests"


@dataclass(frozen=True)
class NativeReplayAudit:
    status: str
    issues: tuple[str, ...] = ()
    missing: tuple[str, ...] = ()
    segments: tuple[tuple[str, PathAudit], ...] = ()
    ledger_commit_count: int | None = None
    receipt_digest: str | None = None
    act_genesis_digest: str | None = None
    act_final_digest: str | None = None
    wa_activation_digest: str | None = None
    plan_activation_digest: str | None = None
    source_main: str = SOURCE_MAIN
    receipt_evidence_mode: str = MODE
    scoped_native_fixture_replay_completed: bool = False
    formal_descent_certified: bool = False
    lean_python_refinement_proved: bool = False
    external_receipt_authenticated: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    merge_authority_granted: bool = False


def _digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                   separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _done(errors: list[str], missing: list[str], segments: list[tuple[str, PathAudit]],
          *, receipt_digest: str | None = None,
          ledger_commit_count: int | None = None,
          act_genesis_digest: str | None = None,
          act_final_digest: str | None = None,
          wa_activation_digest: str | None = None,
          plan_activation_digest: str | None = None) -> NativeReplayAudit:
    status = BLOCKED if errors else NO_DATA if missing else SUCCESS
    return NativeReplayAudit(
        status=status,
        issues=tuple(dict.fromkeys(errors)),
        missing=tuple(dict.fromkeys(missing)),
        segments=tuple(segments),
        receipt_digest=receipt_digest,
        ledger_commit_count=ledger_commit_count,
        act_genesis_digest=act_genesis_digest,
        act_final_digest=act_final_digest,
        wa_activation_digest=wa_activation_digest,
        plan_activation_digest=plan_activation_digest,
        scoped_native_fixture_replay_completed=(status == SUCCESS),
    )


def audit_native_cycle_ledger(root: Any, native_receipt: Any) -> NativeReplayAudit:
    """Verify one existing v1.3 native cycle using its *actual local Act ledger*.

    The v1.3 native artifact records final OS states but not the two intermediate
    raw activation receipts. Reconstruct these with the exact original native
    fixture constants and validate their digests against the stored plan and
    Act genesis. This is reproducible source binding, **not** attestation that
    a distinct issuer actually signed or emitted either original receipt.

    Act genesis and all applied Act events are read from the same local fixture
    store: original _recover_unlocked performs original-kernel event replay
    and original store commit/digest checks without writing a lock/snapshot.
    Do not use on a live concurrently modified store.
    """
    errors: list[str] = []
    missing: list[str] = []
    segments: list[tuple[str, PathAudit]] = []
    digests: dict[str, str | None] = {}

    if native_receipt is None:
        return _done(errors, ["native_receipt:missing"], segments)
    if not isinstance(root, Path):
        return _done(["root:trusted_path_required"], missing, segments)
    if type(native_receipt) is not dict:
        return _done(["native_receipt:plain_object_required"], missing, segments)

    try:
        packet = _finite_json(native_receipt)
        digests["receipt_digest"] = _digest(packet)
    except (TypeError, ValueError, UnicodeError, RecursionError, OverflowError):
        return _done(["native_receipt:invalid_json"], missing, segments)

    if packet.get("version") != RECEIPT_VERSION or packet.get("cycle_id") != CYCLE_ID:
        errors.append("native_receipt:unsupported_version_or_cycle")
    try:
        existing_errors = validate_native_full_cycle_receipt(packet)
    except Exception as exc:
        errors.append("native_receipt:validator_exception:" + type(exc).__name__)
    else:
        if type(existing_errors) is not list or any(type(item) is not str for item in existing_errors):
            errors.append("native_receipt:validator_return_contract_invalid")
        else:
            errors.extend("native_receipt:" + item for item in existing_errors)
    artifacts = packet.get("native_artifacts")
    if type(artifacts) is not dict:
        missing.append("native_artifacts:missing")
        return _done(errors, missing, segments, receipt_digest=digests.get("receipt_digest"))
    if set(artifacts) != EXPECTED_NATIVE_ARTIFACTS:
        errors.append("native_artifacts:inventory_mismatch")
        return _done(errors, missing, segments, receipt_digest=digests.get("receipt_digest"))
    for name in EXPECTED_NATIVE_ARTIFACTS:
        if type(artifacts[name]) is not dict:
            errors.append("native_artifacts:" + name + ":plain_object_required")
    if errors:
        return _done(errors, missing, segments, receipt_digest=digests.get("receipt_digest"))

    wa, plan, final_act = (artifacts[name] for name in
                           ("DecisionOSWa", "PlanOS", "ActOS"))
    wa_activation = None
    plan_activation = None
    try:
        # These are the source-pinned constants of the original _build_plan.
        wa_activation = build_replan_wa_activation_receipt(
            state=wa,
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("native-full-cycle-replan-state"),
            replan_receipt_digest=sha("native-full-cycle-replan-receipt"),
            next_plan_basis_digest=sha("native-full-cycle-next-plan-basis"),
            now_ms=50_000,
        )
        plan_activation = build_plan_phase_activation_receipt(
            state=plan,
            mission_cycle_phase="plan",
            mission_cycle_state_digest=sha("native-full-cycle-plan-phase-state"),
            plan_phase_receipt_digest=sha("native-full-cycle-plan-phase-receipt"),
            now_ms=80_000,
        )
        digests["wa_activation_digest"] = wa_activation["wa_activation_receipt_digest"]
        digests["plan_activation_digest"] = plan_activation["plan_activation_receipt_digest"]
    except (TypeError, ValueError, KeyError, AttributeError) as exc:
        errors.append("native_activation_reconstruction:" + type(exc).__name__)

    if wa_activation is not None and plan.get("replan_activation_receipt_digest") != wa_activation["wa_activation_receipt_digest"]:
        errors.append("plan:wa_receipt_digest_not_reproducible")
    if plan_activation is not None and final_act.get("plan_activation_receipt_digest") != plan_activation["plan_activation_receipt_digest"]:
        errors.append("final_act:plan_receipt_digest_not_reproducible")

    store = ActStore(root / "act")
    if not all((store.root / item).is_file() for item in ACT_STORE_FILES):
        missing.append("actual_act_store:genesis_ledger_snapshot_missing")
        return _done(
            errors, missing, segments, receipt_digest=digests.get("receipt_digest"),
            wa_activation_digest=digests.get("wa_activation_digest"),
            plan_activation_digest=digests.get("plan_activation_digest"),
        )
    try:
        genesis = store._read_json(store.genesis_path)
        final_replay, commits = store._recover_unlocked()
        saved_snapshot = store._read_json(store.snapshot_path)
        digests["act_genesis_digest"] = genesis.get("act_state_digest")
        digests["act_final_digest"] = final_replay.get("act_state_digest")
        if saved_snapshot != final_replay:
            errors.append("act_store:snapshot_not_equal_to_replay")
        if final_replay != final_act:
            errors.append("act_store:replay_not_equal_to_native_artifact")
        if not commits:
            errors.append("act_store:no_transition_witness")
        elif commits[0].get("predecessor_act_state_digest") != genesis.get("act_state_digest"):
            errors.append("act_store:first_event_not_from_actual_genesis")
        if type(final_act.get("event_index")) is not int or final_act["event_index"] != len(commits):
            errors.append("act_store:commit_count_event_index_mismatch")
        if genesis.get("current_phase") != "bind":
            errors.append("act_store:genesis_not_bind")
        if final_act.get("current_phase") != "commit":
            errors.append("act_store:final_not_commit")
        if final_act.get("effect_recorded") is not True or final_act.get("route") != "EFFECT_RECORDED":
            errors.append("act_store:final_effect_route_not_recorded")
        for field in (
            "act_id", "lineage_id", "mission_contract_digest",
            "source_plan_id", "source_plan_state_digest",
            "source_committed_plan_digest", "source_plan_basis_digest",
            "source_wa_basis_digest", "plan_activation_receipt_digest",
        ):
            if genesis.get(field) != final_act.get(field):
                errors.append("act_store:genesis_final_binding_mismatch:" + field)
    except Exception as exc:
        errors.append("act_store:original_replay_exception:" + type(exc).__name__)
        genesis = None
        commits = None
        final_replay = None

    # Preserve the checked checkpoint provenance: a final committed Act is
    # NOT itself an initial bind state for the v0.4 admission contract.
    if wa_activation is not None:
        result = audit_typed_path(
            {name: artifacts[name] for name in EXPECTED_OS[:4]},
            receipts={"DecisionOSWa->PlanOS": wa_activation},
            start="DecisionOS", end="PlanOS",
        )
        segments.append(("DecisionOS->PlanOS", result))
    if genesis is not None and plan_activation is not None:
        result = audit_typed_path(
            {"PlanOS": plan, "ActOS": genesis},
            receipts={"PlanOS->ActOS": plan_activation},
            start="PlanOS", end="ActOS",
        )
        segments.append(("PlanOS->ActOS(initial)", result))
    if final_replay is not None:
        result = audit_typed_path(
            {name: artifacts[name] for name in EXPECTED_OS[4:]},
            start="ActOS", end="LearnOS",
        )
        segments.append(("ActOS(final)->LearnOS", result))

    for label, result in segments:
        if not isinstance(result, PathAudit):
            errors.append("segment:" + label + ":unexpected_auditor_return")
        elif result.status == "BLOCKED":
            errors.extend("segment:" + label + ":" + issue
                          for issue in (result.violations or ("blocked",)))
            missing.extend("segment:" + label + ":" + issue
                           for issue in result.missing)
        elif result.status == "NO_DATA":
            missing.extend("segment:" + label + ":" + issue
                           for issue in (result.missing or ("no_data",)))
        elif result.status != PATH_PASS or result.local_python_checks_completed is not True:
            missing.append("segment:" + label + ":scoped_runtime_validation_unconfirmed")
    if len(segments) != 3:
        missing.append("native_cycle:three_connected_segments_not_complete")

    return _done(
        errors, missing, segments,
        receipt_digest=digests.get("receipt_digest"),
        ledger_commit_count=len(commits) if commits is not None else None,
        act_genesis_digest=digests.get("act_genesis_digest"),
        act_final_digest=digests.get("act_final_digest"),
        wa_activation_digest=digests.get("wa_activation_digest"),
        plan_activation_digest=digests.get("plan_activation_digest"),
    )


__all__ = (
    "VERSION", "SOURCE_MAIN", "SUCCESS", "NO_DATA", "BLOCKED", "NativeReplayAudit",
    "audit_native_cycle_ledger",
)
