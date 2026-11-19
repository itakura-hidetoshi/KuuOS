"""v0.33: exact original Wa -> PlanOS native source compatibility.

Join the existing original Plural->Wa and PlanOS source-bound Lean-data
auditors only through the registered Wa->Plan edge and its separately
supplied original replan activation receipt. This does not prove global
descent, complete Python refinement, external issuer authenticity, or
give any execution, host, truth or repository authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint
from runtime.kuuos_lean_python_decision_mediator_source_v0_29 import (
    PASS, BLOCKED, NO_DATA,
)
from runtime.kuuos_lean_python_wa_native_binding_v0_29 import audit_native_wa_endorsement
from runtime.kuuos_lean_python_plan_native_binding_v0_28 import audit_native_plan_effect_guards
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import (
    audit_decision_plan_edge, EDGE_SPECS, _same,
)
from runtime.kuuos_lean_python_contract_bridge_v0_1 import PASSED as ORIGINAL_EDGE_PASS

VERSION = "kuuos_lean_python_wa_plan_local_compat_v0_33"
SOURCE_PARENT = "cc5093e37adf01f7eec583b0a7ac4c99517d9368"
SCOPED_COMPATIBLE = "SCOPED_WA_PLAN_SOURCE_COMPATIBLE"
EDGE = ("DecisionOSWa", "PlanOS")


@dataclass(frozen=True)
class NativeWaPlanLocalAudit:
    status: str
    issues: tuple[str, ...] = ()
    observed_wa_digest: str | None = None
    observed_plan_digest: str | None = None
    observed_replan_receipt_digest: str | None = None
    checked_field_paths: tuple[str, ...] = ()
    original_wa_conditions_checked: bool = False
    original_plan_guards_checked: bool = False
    original_replan_edge_checked: bool = False
    selected_lean_data_conditions_checked: bool = False
    # Source compatibility is not a Lean-to-Python compiler/refinement proof.
    formal_descent_certified: bool = False
    global_gluing_proved: bool = False
    complete_lean_python_refinement_proved: bool = False
    lean_proof_term_constructed: bool = False
    external_issuer_authenticated: bool = False
    external_replan_receipt_authenticated: bool = False
    host_license_granted: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    git_authority_granted: bool = False
    original_state_mutated: bool = False


def _hold(status: str, reason: str) -> NativeWaPlanLocalAudit:
    return NativeWaPlanLocalAudit(status=status, issues=(reason,))


def _snapshot(value: Any, name: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise TypeError(name + ":plain_native_dict_required")
    try:
        copy = _finite_json(value)
    except (TypeError, ValueError, RecursionError, UnicodeError, OverflowError) as exc:
        raise ValueError(name + ":invalid_finite_json:" + type(exc).__name__) from exc
    if type(copy) is not dict:
        raise ValueError(name + ":finite_json_not_dict")
    return copy


def audit_native_wa_plan_local_compatibility(
    plural_state: Any,
    wa_state: Any,
    plan_state: Any,
    replan_activation_receipt: Any,
) -> NativeWaPlanLocalAudit:
    """Read-only original record compatibility, NEVER a synthetic direct shortcut."""
    values = (plural_state, wa_state, plan_state, replan_activation_receipt)
    names = ("Plural", "Wa", "PlanOS", "replan_receipt")
    for name, value in zip(names, values):
        if value is None:
            return _hold(NO_DATA, name + ":original_source_missing")
    try:
        plural, wa, plan, receipt = tuple(
            _snapshot(value, name) for name, value in zip(names, values)
        )
    except (TypeError, ValueError) as exc:
        return _hold(BLOCKED, str(exc))

    # These existing auditors run the ORIGINAL native validators and
    # selectively project already-proved Lean structure data conditions.
    wa_local = audit_native_wa_endorsement(plural, wa)
    plan_local = audit_native_plan_effect_guards(plan)
    # A separately SUPPLIED receipt is required, never reconstructed here.
    edge = audit_decision_plan_edge(
        *EDGE, wa, plan, replan_activation_receipt=receipt
    )
    for name, result, expected in (
        ("wa_native", wa_local, PASS),
        ("plan_native", plan_local, PASS),
        ("original_wa_plan_edge", edge, ORIGINAL_EDGE_PASS),
    ):
        if result.status == BLOCKED:
            return _hold(BLOCKED, name + ":" + ";".join(result.issues))
    for name, result, expected in (
        ("wa_native", wa_local, PASS),
        ("plan_native", plan_local, PASS),
        ("original_wa_plan_edge", edge, ORIGINAL_EDGE_PASS),
    ):
        if result.status != expected:
            return _hold(NO_DATA, name + ":" + ";".join(result.issues))

    # Exactly the registered original typed fields; no Decision->Plan shortcut.
    spec = EDGE_SPECS.get(EDGE)
    if spec is None:
        return _hold(NO_DATA, "registered_Wa_to_Plan_edge_missing")
    for source_key, target_key in spec.equal_fields:
        if source_key not in wa or target_key not in plan:
            return _hold(NO_DATA, "registered_edge_field_missing:" + target_key)
        if not _same(wa[source_key], plan[target_key]):
            return _hold(BLOCKED, "registered_edge_field_mismatch:" + target_key)

    # Verify each auditor saw these EXACT copies, not unrelated validated states.
    if (wa_local.source_digest != _fingerprint(wa)
            or plan_local.source_digest != _fingerprint(plan)):
        return _hold(BLOCKED, "audited_source_digest_mismatch")
    digest = receipt.get("wa_activation_receipt_digest")
    if type(digest) is not str or not digest:
        return _hold(NO_DATA, "original_replan_receipt_digest_missing")
    if not _same(plan.get("replan_activation_receipt_digest"), digest):
        return _hold(BLOCKED, "plan_replan_receipt_identity_mismatch")

    paths = (
        "DecisionOSPlural.plural_state_digest",
        "DecisionOSWa.wa_state_digest",
        "DecisionOSWa.pending_replan_activation",
        "replan_receipt.wa_activation_receipt_digest",
        "replan_receipt.future_only",
        "replan_receipt.memory_overwrite",
        "replan_receipt.host_license_granted",
        "PlanOS.replan_activation_receipt_digest",
        "PlanOS.plan_state_digest",
        "PlanOS.guard_summary.all_effects_guarded",
        "PlanOS.checkpoint_summary.all_effects_have_checkpoint",
    ) + tuple(
        "DecisionOSWa." + src + "=PlanOS." + dst
        for src, dst in spec.equal_fields
    )
    return NativeWaPlanLocalAudit(
        status=SCOPED_COMPATIBLE,
        observed_wa_digest=_fingerprint(wa),
        observed_plan_digest=_fingerprint(plan),
        observed_replan_receipt_digest=digest,
        checked_field_paths=paths,
        original_wa_conditions_checked=True,
        original_plan_guards_checked=True,
        original_replan_edge_checked=True,
        selected_lean_data_conditions_checked=True,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "PASS", "BLOCKED", "NO_DATA",
    "SCOPED_COMPATIBLE", "EDGE", "NativeWaPlanLocalAudit",
    "audit_native_wa_plan_local_compatibility",
)
