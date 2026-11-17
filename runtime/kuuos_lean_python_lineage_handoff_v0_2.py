"""Read-only Lean-aware cross-OS handoff audit for the KuuOS runtime.

This checks exact identity links between *existing* OS state objects. A PASS
only attests to the Python validations actually performed on supplied input;
it is not a Lean proof of this Python module, a truth claim, or authority to
execute. Do not infer a direct DecisionOS -> PlanOS edge: WaOS intermediates.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_lean_python_contract_bridge_v0_1 import (
    BLOCKED, NO_DATA, PASSED, SOURCE_COMMIT, audit_core_state,
)

VERSION = "kuuos_lean_python_lineage_handoff_v0_2"


@dataclass(frozen=True)
class HandoffContract:
    source_os: str
    target_os: str
    lean_source: str
    premise_theorem: str
    lineage_theorem: str
    # source field -> target field, using the *original* Python schema names
    equal_fields: tuple[tuple[str, str], ...]
    source_route: str | None = None
    required_source_flags: tuple[str, ...] = ()


COMMON = (("lineage_id", "lineage_id"), ("mission_contract_digest", "mission_contract_digest"))

HANDOFF_CONTRACTS: dict[tuple[str, str], HandoffContract] = {
    ("ActOS", "ObserveOS"): HandoffContract(
        "ActOS", "ObserveOS",
        "formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean",
        "observation_requires_committed_effect",
        "observation_preserves_effect_identity",
        COMMON + (
            ("act_id", "source_act_id"),
            ("act_state_digest", "source_act_state_digest"),
            ("act_version", "source_act_version"),
            ("updated_at_ms", "source_act_updated_at_ms"),
            ("host_receipt_digest", "host_receipt_digest"),
            ("host_invocation_digest", "host_invocation_digest"),
            ("selected_step_id", "selected_step_id"),
            ("selected_step_digest", "selected_step_digest"),
            ("operation_id", "operation_id"),
            ("expected_observation_digest", "expected_observation_digest"),
            ("verification_criterion_digest", "verification_criterion_digest"),
        ),
        source_route="EFFECT_RECORDED",
        required_source_flags=("effect_recorded", "observation_required", "verification_required"),
    ),
    ("ObserveOS", "VerifyOS"): HandoffContract(
        "ObserveOS", "VerifyOS",
        "formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean",
        "verification_requires_committed_observation",
        "verification_preserves_observation_identity",
        COMMON + (
            ("observe_id", "source_observe_id"),
            ("observe_state_digest", "source_observe_state_digest"),
            ("observe_version", "source_observe_version"),
            ("updated_at_ms", "source_observe_updated_at_ms"),
            ("route", "source_observation_route"),
            ("observation_debt_discharged", "source_observation_debt_discharged"),
            ("reobservation_required", "source_reobservation_required"),
            ("source_act_state_digest", "source_act_state_digest"),
            ("host_receipt_digest", "host_receipt_digest"),
            ("host_invocation_digest", "host_invocation_digest"),
            ("expected_observation_digest", "expected_observation_digest"),
            ("verification_criterion_digest", "verification_criterion_digest"),
            ("evidence_packet_digest", "evidence_packet_digest"),
            ("quality_report_digest", "quality_report_digest"),
            ("comparison_receipt_digest", "comparison_receipt_digest"),
        ),
        required_source_flags=("observation_recorded", "verification_required"),
    ),
    ("VerifyOS", "LearnOS"): HandoffContract(
        "VerifyOS", "LearnOS",
        "formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean",
        "learning_requires_committed_verification",
        "learning_preserves_verification_lineage",
        COMMON + (
            ("verify_id", "source_verify_id"),
            ("verify_state_digest", "source_verify_state_digest"),
            ("verify_version", "source_verify_version"),
            ("updated_at_ms", "source_verify_updated_at_ms"),
            ("route", "source_verification_route"),
            ("verification_evidence_digest", "source_verification_evidence_digest"),
            ("source_observe_state_digest", "source_observe_state_digest"),
            ("source_act_state_digest", "source_act_state_digest"),
            ("verification_criterion_digest", "verification_criterion_digest"),
            ("criterion_packet_digest", "criterion_packet_digest"),
            ("challenge_packet_digest", "source_challenge_packet_digest"),
            ("corroboration_report_digest", "corroboration_report_digest"),
            ("adjudication_receipt_digest", "adjudication_receipt_digest"),
            ("reobservation_required", "source_reobservation_required"),
            ("corrective_action_required", "source_corrective_action_required"),
        ),
        required_source_flags=("verification_recorded", "learning_required"),
    ),
}


@dataclass(frozen=True)
class HandoffAudit:
    source_os: str
    target_os: str
    status: str
    issues: tuple[str, ...]
    lean_source: str | None
    lean_theorems: tuple[str, ...]
    source_commit: str = SOURCE_COMMIT
    scope: str = "source/target Python state and digest comparison only; no Lean/Python refinement proof"

    @property
    def passed_runtime_checks(self) -> bool:
        return self.status == PASSED


def audit_handoff(source_os: str, target_os: str, source_state: Any, target_state: Any) -> HandoffAudit:
    """Check exact source links and the *existing* validators, without effects.

    States are deep-copied before calling the original validators so that
    even a buggy validator cannot mutate the caller's mapping. Missing fields
    lead to NO_DATA; contradictory fields or failed validators to BLOCKED.
    """
    contract = HANDOFF_CONTRACTS.get((source_os, target_os))
    if contract is None:
        return HandoffAudit(source_os, target_os, NO_DATA,
                            ("unsupported_handoff_requires_proof_and_source_mapping",), None, ())

    errors: list[str] = []
    missing: list[str] = []
    if not isinstance(source_state, Mapping):
        missing.append("source_state_missing")
    if not isinstance(target_state, Mapping):
        missing.append("target_state_missing")
    if missing:
        return HandoffAudit(source_os, target_os, NO_DATA, tuple(missing),
                            contract.lean_source, (contract.premise_theorem, contract.lineage_theorem))

    try:
        source_copy = deepcopy(dict(source_state))
        target_copy = deepcopy(dict(target_state))
        source_audit = audit_core_state(source_os, source_copy)
        target_audit = audit_core_state(target_os, target_copy)
    except (TypeError, ValueError, RecursionError) as exc:
        return HandoffAudit(source_os, target_os, NO_DATA, (f"state_copy_unavailable:{type(exc).__name__}",),
                            contract.lean_source, (contract.premise_theorem, contract.lineage_theorem))
    for prefix, result in (("source", source_audit), ("target", target_audit)):
        if result.status == BLOCKED:
            errors.extend(f"{prefix}.{issue}" for issue in result.issues)
        elif result.status == NO_DATA:
            missing.extend(f"{prefix}.{issue}" for issue in result.issues)
    if source_copy != dict(source_state) or target_copy != dict(target_state):
        errors.append("original_validator_mutated_state_copy")

    if source_state.get("current_phase") != "commit":
        if "current_phase" not in source_state:
            missing.append("source.current_phase_missing")
        else:
            errors.append("source_not_committed")
    if contract.source_route:
        route = source_state.get("route")
        if route is None:
            missing.append("source.route_missing")
        elif route != contract.source_route:
            errors.append("source_route_not_effect_recorded")
    elif source_state.get("route") == "PENDING":
        errors.append("source_route_pending")
    elif "route" not in source_state:
        missing.append("source.route_missing")

    for flag in contract.required_source_flags:
        if flag not in source_state:
            missing.append(f"source.{flag}_missing")
        elif source_state[flag] is not True:
            errors.append(f"source.{flag}_not_true")

    for source_key, target_key in contract.equal_fields:
        has_source = source_key in source_state and source_state[source_key] is not None
        has_target = target_key in target_state and target_state[target_key] is not None
        if not has_source:
            missing.append(f"source.{source_key}_missing")
        if not has_target:
            missing.append(f"target.{target_key}_missing")
        if has_source and has_target and source_state[source_key] != target_state[target_key]:
            errors.append(f"binding_mismatch:{source_key}->{target_key}")
    source_time = source_state.get("updated_at_ms")
    target_time = target_state.get("updated_at_ms")
    if type(source_time) is not int or source_time < 0:
        missing.append("source.updated_at_ms_unavailable")
    if type(target_time) is not int or target_time < 0:
        missing.append("target.updated_at_ms_unavailable")
    if (type(source_time) is int and type(target_time) is int
            and source_time >= 0 and target_time >= 0 and target_time < source_time):
        errors.append("target_precedes_source_in_time")
    if source_os == "VerifyOS":
        if target_state.get("active_now") is not False:
            if "active_now" in target_state:
                errors.append("learning_active_without_replan")
            else:
                missing.append("target.active_now_missing")
    return HandoffAudit(
        source_os, target_os,
        BLOCKED if errors else NO_DATA if missing else PASSED,
        tuple(dict.fromkeys(errors + missing)), contract.lean_source,
        (contract.premise_theorem, contract.lineage_theorem),
    )


__all__ = ["VERSION", "HandoffContract", "HANDOFF_CONTRACTS", "HandoffAudit", "audit_handoff"]
