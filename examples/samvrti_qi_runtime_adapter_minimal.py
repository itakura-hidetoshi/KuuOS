#!/usr/bin/env python3
"""Minimal Samvrti Qi runtime adapter for KuuOS.

Qi is treated as a conventional effective flow state. This adapter never grants
truth authority, theorem authority, standalone diagnosis authority, standalone
treatment authorization, medical act authorization, or execution authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class QiRuntimeInput:
    qi_id: str
    world_id: str
    observer_surface: str
    scale_id: str
    samvrti_scope: bool = True
    paramartha_entity_claim: bool = False
    bridge_authority: str = "reference_only"
    final_theorem_authority: bool = False
    execution_authority: bool = False
    direct_execution_requested: bool = False
    gauge_connection_present: bool = True
    memory_lineage_present: bool = True
    curvature_norm: float = 0.0
    holonomy_defect: float = 0.0
    entropy_production_rate: float = 0.0
    coherence_index: float = 1.0
    recoverability_margin: float = 1.0
    source_trace: Tuple[str, ...] = ()
    unresolved_blockers: Tuple[str, ...] = ()


@dataclass(frozen=True)
class QiRuntimeDecision:
    decision_status: str
    runtime_mode: str
    reason_codes: Tuple[str, ...]
    qi_flow_admissible: bool
    observe_only: bool
    direct_execution_allowed: bool = False
    authority_expansion: bool = False
    standalone_diagnosis_authority: bool = False
    standalone_treatment_authorization: bool = False
    medical_act_authorization: bool = False
    medical_modality_neutral: bool = True
    qi_denied_by_boundary: bool = False
    east_asian_medical_reasoning_denied: bool = False
    biomedicine_privileged_by_wording: bool = False
    professional_judgment_required: bool = True
    patient_context_required: bool = True


MAX_CURVATURE_NORM = 1.0
MAX_HOLONOMY_DEFECT = 0.25
MAX_ENTROPY_PRODUCTION_RATE = 1.0
MIN_COHERENCE_INDEX = 0.10
MIN_RECOVERABILITY_MARGIN = 0.20


def _blocked(*reason_codes: str) -> QiRuntimeDecision:
    return QiRuntimeDecision(
        decision_status="qi_flow_blocked",
        runtime_mode="blocked_for_non_reification",
        reason_codes=tuple(reason_codes),
        qi_flow_admissible=False,
        observe_only=True,
        direct_execution_allowed=False,
        authority_expansion=False,
        standalone_diagnosis_authority=False,
        standalone_treatment_authorization=False,
        medical_act_authorization=False,
        medical_modality_neutral=True,
        qi_denied_by_boundary=False,
        east_asian_medical_reasoning_denied=False,
        biomedicine_privileged_by_wording=False,
        professional_judgment_required=True,
        patient_context_required=True,
    )


def _hold(runtime_mode: str, reason_codes: Tuple[str, ...]) -> QiRuntimeDecision:
    return QiRuntimeDecision(
        decision_status="qi_flow_held",
        runtime_mode=runtime_mode,
        reason_codes=reason_codes,
        qi_flow_admissible=False,
        observe_only=True,
        direct_execution_allowed=False,
        authority_expansion=False,
        standalone_diagnosis_authority=False,
        standalone_treatment_authorization=False,
        medical_act_authorization=False,
        medical_modality_neutral=True,
        qi_denied_by_boundary=False,
        east_asian_medical_reasoning_denied=False,
        biomedicine_privileged_by_wording=False,
        professional_judgment_required=True,
        patient_context_required=True,
    )


def evaluate_samvrti_qi_runtime(runtime_input: QiRuntimeInput) -> QiRuntimeDecision:
    """Evaluate the minimal KuuOS Samvrti Qi runtime gate.

    The output is intentionally non-sovereign. Even an accepted Qi flow only
    authorizes observation and routing inside KuuOS governance; it never directly
    authorizes execution or final belief/proof/medical-act claims.
    """

    if not runtime_input.samvrti_scope:
        return _blocked("QI_BLOCK_NOT_SAMVRTI_SCOPE")

    if runtime_input.paramartha_entity_claim:
        return _blocked("QI_BLOCK_PARAMARTHA_ENTITY_CLAIM")

    if runtime_input.bridge_authority != "reference_only":
        return _blocked("QI_BLOCK_AUTHORITY_EXPANSION")

    if runtime_input.final_theorem_authority:
        return _blocked("QI_BLOCK_FINAL_THEOREM_AUTHORITY")

    if runtime_input.execution_authority or runtime_input.direct_execution_requested:
        return _blocked("QI_BLOCK_EXECUTION_AUTHORITY")

    reasons = []

    if not runtime_input.source_trace:
        reasons.append("QI_HOLD_MISSING_SOURCE_TRACE")

    if not runtime_input.gauge_connection_present:
        reasons.append("QI_HOLD_MISSING_INDRANET_GAUGE_CONNECTION")

    if not runtime_input.memory_lineage_present:
        reasons.append("QI_HOLD_MISSING_MEMORY_LINEAGE")

    if runtime_input.curvature_norm > MAX_CURVATURE_NORM:
        reasons.append("QI_HOLD_CURVATURE_ABOVE_BOUND")

    if runtime_input.holonomy_defect > MAX_HOLONOMY_DEFECT:
        reasons.append("QI_HOLD_HOLONOMY_DEFECT_ABOVE_BOUND")

    if runtime_input.entropy_production_rate > MAX_ENTROPY_PRODUCTION_RATE:
        reasons.append("QI_HOLD_ENTROPY_PRODUCTION_ABOVE_BOUND")

    if runtime_input.coherence_index < MIN_COHERENCE_INDEX:
        reasons.append("QI_HOLD_COHERENCE_BELOW_BOUND")

    if runtime_input.recoverability_margin < MIN_RECOVERABILITY_MARGIN:
        reasons.append("QI_HOLD_RECOVERABILITY_MARGIN_BELOW_BOUND")

    if runtime_input.unresolved_blockers:
        blocker_codes = ",".join(runtime_input.unresolved_blockers)
        reasons.append(f"QI_HOLD_UNRESOLVED_BLOCKERS:{blocker_codes}")

    if reasons:
        mode = (
            "blocked_by_unresolved_obstruction"
            if runtime_input.unresolved_blockers
            else "hold_for_observation"
        )
        return _hold(mode, tuple(reasons))

    return QiRuntimeDecision(
        decision_status="qi_flow_accepted_as_samvrti_reference",
        runtime_mode="observe_and_route",
        reason_codes=("QI_ACCEPT_SAMVRTI_GAUGE_FLOW",),
        qi_flow_admissible=True,
        observe_only=True,
        direct_execution_allowed=False,
        authority_expansion=False,
        standalone_diagnosis_authority=False,
        standalone_treatment_authorization=False,
        medical_act_authorization=False,
        medical_modality_neutral=True,
        qi_denied_by_boundary=False,
        east_asian_medical_reasoning_denied=False,
        biomedicine_privileged_by_wording=False,
        professional_judgment_required=True,
        patient_context_required=True,
    )


def _assert_neutral_boundary(decision: QiRuntimeDecision) -> None:
    assert decision.observe_only is True
    assert decision.direct_execution_allowed is False
    assert decision.authority_expansion is False
    assert decision.standalone_diagnosis_authority is False
    assert decision.standalone_treatment_authorization is False
    assert decision.medical_act_authorization is False
    assert decision.medical_modality_neutral is True
    assert decision.qi_denied_by_boundary is False
    assert decision.east_asian_medical_reasoning_denied is False
    assert decision.biomedicine_privileged_by_wording is False
    assert decision.professional_judgment_required is True
    assert decision.patient_context_required is True


def _self_check() -> None:
    accepted = evaluate_samvrti_qi_runtime(
        QiRuntimeInput(
            qi_id="qi-demo-accepted",
            world_id="public-core-world",
            observer_surface="reviewer-visible",
            scale_id="v0_1",
            source_trace=("README.md#Samvrti-Qi-Layer",),
        )
    )
    assert accepted.decision_status == "qi_flow_accepted_as_samvrti_reference"
    assert accepted.runtime_mode == "observe_and_route"
    assert accepted.qi_flow_admissible is True
    _assert_neutral_boundary(accepted)

    blocked = evaluate_samvrti_qi_runtime(
        QiRuntimeInput(
            qi_id="qi-demo-blocked",
            world_id="public-core-world",
            observer_surface="reviewer-visible",
            scale_id="v0_1",
            paramartha_entity_claim=True,
            source_trace=("negative-case",),
        )
    )
    assert blocked.decision_status == "qi_flow_blocked"
    assert "QI_BLOCK_PARAMARTHA_ENTITY_CLAIM" in blocked.reason_codes
    _assert_neutral_boundary(blocked)

    held = evaluate_samvrti_qi_runtime(
        QiRuntimeInput(
            qi_id="qi-demo-held",
            world_id="public-core-world",
            observer_surface="reviewer-visible",
            scale_id="v0_1",
            gauge_connection_present=False,
            recoverability_margin=0.0,
            source_trace=("negative-case",),
        )
    )
    assert held.decision_status == "qi_flow_held"
    _assert_neutral_boundary(held)


if __name__ == "__main__":
    _self_check()
    print("[samvrti-qi-runtime-adapter] PASS")