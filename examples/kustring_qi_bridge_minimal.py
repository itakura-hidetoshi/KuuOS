#!/usr/bin/env python3
"""Minimal KuString Qi Bridge v0.1 for KuuOS."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Tuple


@dataclass(frozen=True)
class KuStringQiBridgeInput:
    qi_id: str
    samvrti_status: str
    source_trace: Tuple[str, ...]
    string_mode_visible: bool = False
    brane_boundary_visible: bool = False
    gauge_connection_visible: bool = True
    curvature_visible: bool = False
    wilson_residue_visible: bool = False
    current_visible: bool = False
    ward_leak_visible: bool = False
    open_state_visible: bool = False
    sk_fv_history_visible: bool = False
    memory_kernel_visible: bool = False
    noncommutative_history_visible: bool = False
    path_measure_normalized: bool = False
    direct_execution_requested: bool = False


@dataclass(frozen=True)
class KuStringQiBridgeDecision:
    bridge_status: str
    bridge_reason: str
    evidence_status: Mapping[str, str]
    projected_level_hint: str
    observe_only: bool = True
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


def _blocked(reason: str) -> KuStringQiBridgeDecision:
    return KuStringQiBridgeDecision("bridge_blocked", reason, {}, "Reject")


def project_samvrti_qi_to_kustring_evidence(i: KuStringQiBridgeInput) -> KuStringQiBridgeDecision:
    if i.samvrti_status != "qi_flow_accepted_as_samvrti_reference":
        return _blocked("samvrti_qi_not_accepted")
    if i.direct_execution_requested:
        return _blocked("direct_execution_requested")
    if not i.source_trace:
        return _blocked("missing_source_trace")

    e: Dict[str, str] = {"K_non_reification": "pass", "delta_rel_in_K_perp": "pass"}
    if i.gauge_connection_visible:
        e["gauge_connection_A_mu"] = "pass"
    if i.string_mode_visible and i.brane_boundary_visible:
        e.update({"string_mode_consistency": "pass", "brane_boundary_support": "pass"})
    if i.curvature_visible and i.wilson_residue_visible:
        e.update({"curvature_F_munu": "pass", "Wilson_loop_residue": "pass"})
    if i.current_visible:
        e["current_J_Qi_mu"] = "pass"
    if i.ward_leak_visible:
        e["Ward_or_leak_identity"] = "pass"
    if i.open_state_visible:
        e.update({
            "density_state_rho": "pass", "Hamiltonian_H": "pass", "Lindblad_generator_L": "pass",
            "entropy_production_Sigma": "pass", "free_energy_F_beta": "pass", "DPI_gap": "pass",
            "recovery_margin": "pass", "mass_gap_floor_33_20": "pass",
        })
    if i.sk_fv_history_visible and i.memory_kernel_visible and i.noncommutative_history_visible and i.path_measure_normalized:
        e.update({
            "SK_plus_branch": "pass", "SK_minus_branch": "pass", "FV_influence_functional": "pass",
            "memory_kernel": "pass", "noise_kernel": "pass", "observation_backaction": "pass",
            "noncommutative_operation_history": "pass", "path_measure_normalization": "pass",
        })

    if "path_measure_normalization" in e:
        level = "FullPathQi"
    elif "density_state_rho" in e:
        level = "PhysicalQi"
    elif "Ward_or_leak_identity" in e:
        level = "CurrentQi"
    elif "current_J_Qi_mu" in e:
        level = "CurvedQi"
    elif "curvature_F_munu" in e:
        level = "TransportableQi"
    elif "gauge_connection_A_mu" in e:
        level = "ProtoQi"
    else:
        level = "PreQi"

    return KuStringQiBridgeDecision(
        "bridge_evidence_projected",
        "samvrti_qi_projected_through_kustring_coordinates",
        e,
        level,
    )


def _assert_boundary(d: KuStringQiBridgeDecision) -> None:
    assert d.observe_only is True
    assert d.direct_execution_allowed is False
    assert d.authority_expansion is False
    assert d.standalone_diagnosis_authority is False
    assert d.standalone_treatment_authorization is False
    assert d.medical_act_authorization is False
    assert d.medical_modality_neutral is True
    assert d.qi_denied_by_boundary is False
    assert d.east_asian_medical_reasoning_denied is False
    assert d.biomedicine_privileged_by_wording is False
    assert d.professional_judgment_required is True
    assert d.patient_context_required is True


def _self_check() -> None:
    full = project_samvrti_qi_to_kustring_evidence(KuStringQiBridgeInput(
        qi_id="bridge-fullpath-demo",
        samvrti_status="qi_flow_accepted_as_samvrti_reference",
        source_trace=("samvrti-demo",),
        string_mode_visible=True, brane_boundary_visible=True, curvature_visible=True,
        wilson_residue_visible=True, current_visible=True, ward_leak_visible=True,
        open_state_visible=True, sk_fv_history_visible=True, memory_kernel_visible=True,
        noncommutative_history_visible=True, path_measure_normalized=True,
    ))
    assert full.bridge_status == "bridge_evidence_projected"
    assert full.projected_level_hint == "FullPathQi"
    assert full.evidence_status["FV_influence_functional"] == "pass"
    _assert_boundary(full)

    blocked = project_samvrti_qi_to_kustring_evidence(KuStringQiBridgeInput(
        qi_id="bridge-blocked-demo", samvrti_status="qi_flow_blocked", source_trace=("samvrti-demo",)
    ))
    assert blocked.bridge_status == "bridge_blocked"
    _assert_boundary(blocked)


if __name__ == "__main__":
    _self_check()
    print("[kustring-qi-bridge] PASS")