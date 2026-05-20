#!/usr/bin/env python3
"""Minimal Samvrti Qi to Physical Motion evidence builder for KuuOS.

This adapter turns an accepted Samvrti Qi flow into a conservative physical Qi
packet candidate through KuStringQiBridge. It then delegates classification and
motion evaluation to the Physical Quantum Qi motion pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import sys
from typing import Any, Dict, Mapping

ROOT = Path(__file__).resolve().parents[1]
SAMVRTI_PATH = ROOT / "examples" / "samvrti_qi_runtime_adapter_minimal.py"
BRIDGE_PATH = ROOT / "examples" / "kustring_qi_bridge_minimal.py"
PIPELINE_PATH = ROOT / "examples" / "physical_quantum_qi_motion_pipeline_minimal.py"


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


samvrti = _load_module("samvrti_qi_runtime_adapter_minimal", SAMVRTI_PATH)
bridge = _load_module("kustring_qi_bridge_minimal", BRIDGE_PATH)
pipeline = _load_module("physical_quantum_qi_motion_pipeline_minimal", PIPELINE_PATH)


@dataclass(frozen=True)
class QiEvidenceBuilderInput:
    qi_id: str
    world_id: str
    observer_surface: str
    scale_id: str
    source_trace: tuple[str, ...]
    numeric_terms: Mapping[str, float]
    structural_support_present: bool = False
    transport_evidence_present: bool = False
    current_evidence_present: bool = False
    ward_evidence_present: bool = False
    open_system_evidence_present: bool = False
    full_path_evidence_present: bool = False
    direct_execution_requested: bool = False


@dataclass(frozen=True)
class QiEvidenceBuilderDecision:
    builder_status: str
    samvrti_status: str
    packet_validated_type: str
    pipeline_status: str
    motion_status: str
    motion_score: float
    evidence_status: Mapping[str, str]
    active_terms: tuple[str, ...]
    ignored_terms: tuple[str, ...]
    reason_codes: tuple[str, ...]
    bridge_status: str = "bridge_not_run"
    bridge_projected_level_hint: str = "Reject"
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


def _false_authority() -> Dict[str, bool]:
    return {
        "execution_authority": False,
        "belief_commit_authority": False,
        "memory_overwrite_authority": False,
        "world_root_rewrite_authority": False,
        "safety_override_authority": False,
    }


def build_conservative_evidence(builder_input: QiEvidenceBuilderInput) -> Dict[str, str]:
    """Backward-compatible wrapper around KuStringQiBridge evidence projection."""
    bridge_decision = bridge.project_samvrti_qi_to_kustring_evidence(
        bridge.KuStringQiBridgeInput(
            qi_id=builder_input.qi_id,
            samvrti_status="qi_flow_accepted_as_samvrti_reference",
            source_trace=builder_input.source_trace,
            string_mode_visible=builder_input.structural_support_present,
            brane_boundary_visible=builder_input.structural_support_present,
            gauge_connection_visible=True,
            curvature_visible=builder_input.transport_evidence_present,
            wilson_residue_visible=builder_input.transport_evidence_present,
            current_visible=builder_input.current_evidence_present,
            ward_leak_visible=builder_input.ward_evidence_present,
            open_state_visible=builder_input.open_system_evidence_present,
            sk_fv_history_visible=builder_input.full_path_evidence_present,
            memory_kernel_visible=builder_input.full_path_evidence_present,
            noncommutative_history_visible=builder_input.full_path_evidence_present,
            path_measure_normalized=builder_input.full_path_evidence_present,
            direct_execution_requested=builder_input.direct_execution_requested,
        )
    )
    return dict(bridge_decision.evidence_status)


def _bridge_from_builder_input(
    builder_input: QiEvidenceBuilderInput,
    samvrti_status: str,
):
    return bridge.project_samvrti_qi_to_kustring_evidence(
        bridge.KuStringQiBridgeInput(
            qi_id=builder_input.qi_id,
            samvrti_status=samvrti_status,
            source_trace=builder_input.source_trace,
            string_mode_visible=builder_input.structural_support_present,
            brane_boundary_visible=builder_input.structural_support_present,
            gauge_connection_visible=True,
            curvature_visible=builder_input.transport_evidence_present,
            wilson_residue_visible=builder_input.transport_evidence_present,
            current_visible=builder_input.current_evidence_present,
            ward_leak_visible=builder_input.ward_evidence_present,
            open_state_visible=builder_input.open_system_evidence_present,
            sk_fv_history_visible=builder_input.full_path_evidence_present,
            memory_kernel_visible=builder_input.full_path_evidence_present,
            noncommutative_history_visible=builder_input.full_path_evidence_present,
            path_measure_normalized=builder_input.full_path_evidence_present,
            direct_execution_requested=builder_input.direct_execution_requested,
        )
    )


def _builder_boundary_kwargs() -> Dict[str, bool]:
    return {
        "observe_only": True,
        "direct_execution_allowed": False,
        "authority_expansion": False,
        "standalone_diagnosis_authority": False,
        "standalone_treatment_authorization": False,
        "medical_act_authorization": False,
        "medical_modality_neutral": True,
        "qi_denied_by_boundary": False,
        "east_asian_medical_reasoning_denied": False,
        "biomedicine_privileged_by_wording": False,
        "professional_judgment_required": True,
        "patient_context_required": True,
    }


def run_samvrti_to_physical_motion_builder(builder_input: QiEvidenceBuilderInput) -> QiEvidenceBuilderDecision:
    samvrti_decision = samvrti.evaluate_samvrti_qi_runtime(
        samvrti.QiRuntimeInput(
            qi_id=builder_input.qi_id,
            world_id=builder_input.world_id,
            observer_surface=builder_input.observer_surface,
            scale_id=builder_input.scale_id,
            source_trace=builder_input.source_trace,
            direct_execution_requested=builder_input.direct_execution_requested,
        )
    )

    bridge_decision = _bridge_from_builder_input(builder_input, samvrti_decision.decision_status)

    if samvrti_decision.decision_status != "qi_flow_accepted_as_samvrti_reference":
        return QiEvidenceBuilderDecision(
            builder_status="builder_not_opened_by_samvrti",
            samvrti_status=samvrti_decision.decision_status,
            packet_validated_type="Reject",
            pipeline_status="pipeline_not_run",
            motion_status="qi_motion_blocked",
            motion_score=0.0,
            evidence_status={},
            active_terms=(),
            ignored_terms=tuple(sorted(builder_input.numeric_terms.keys())),
            reason_codes=samvrti_decision.reason_codes,
            bridge_status=bridge_decision.bridge_status,
            bridge_projected_level_hint=bridge_decision.projected_level_hint,
            **_builder_boundary_kwargs(),
        )

    if bridge_decision.bridge_status != "bridge_evidence_projected":
        return QiEvidenceBuilderDecision(
            builder_status="builder_blocked_by_kustring_bridge",
            samvrti_status=samvrti_decision.decision_status,
            packet_validated_type="Reject",
            pipeline_status="pipeline_not_run",
            motion_status="qi_motion_blocked",
            motion_score=0.0,
            evidence_status={},
            active_terms=(),
            ignored_terms=tuple(sorted(builder_input.numeric_terms.keys())),
            reason_codes=(bridge_decision.bridge_reason,),
            bridge_status=bridge_decision.bridge_status,
            bridge_projected_level_hint=bridge_decision.projected_level_hint,
            **_builder_boundary_kwargs(),
        )

    evidence = dict(bridge_decision.evidence_status)
    packet: Dict[str, Any] = {
        "packet_id": f"physical-motion-candidate-{builder_input.qi_id}",
        "claimed_type": "untrusted_samvrti_projection",
        "evidence_status": evidence,
        "mass_gap_floor": {"not_source_of_qi": True},
        "authority": _false_authority(),
    }

    motion = pipeline.run_physical_quantum_qi_motion_pipeline(
        pipeline.QiMotionPipelineInput(
            packet_id=packet["packet_id"],
            packet=packet,
            numeric_terms=builder_input.numeric_terms,
            direct_execution_requested=builder_input.direct_execution_requested,
        )
    )

    return QiEvidenceBuilderDecision(
        builder_status="builder_packet_routed_to_motion_pipeline",
        samvrti_status=samvrti_decision.decision_status,
        packet_validated_type=motion.validated_type,
        pipeline_status=motion.pipeline_status,
        motion_status=motion.motion_status,
        motion_score=motion.motion_score,
        evidence_status=evidence,
        active_terms=motion.active_terms,
        ignored_terms=motion.ignored_terms,
        reason_codes=motion.reason_codes,
        bridge_status=bridge_decision.bridge_status,
        bridge_projected_level_hint=bridge_decision.projected_level_hint,
        **_builder_boundary_kwargs(),
    )


def _assert_boundary(decision: QiEvidenceBuilderDecision) -> None:
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
    full = run_samvrti_to_physical_motion_builder(
        QiEvidenceBuilderInput(
            qi_id="builder-fullpath-demo",
            world_id="public-core-world",
            observer_surface="reviewer-visible",
            scale_id="v0_1",
            source_trace=("samvrti-builder-demo",),
            structural_support_present=True,
            transport_evidence_present=True,
            current_evidence_present=True,
            ward_evidence_present=True,
            open_system_evidence_present=True,
            full_path_evidence_present=True,
            numeric_terms={"sk_fv_history_flow": 1.0, "memory_kernel_backflow": 0.5},
        )
    )
    assert full.bridge_status == "bridge_evidence_projected"
    assert full.bridge_projected_level_hint == "FullPathQi"
    assert full.packet_validated_type == "FullPathQi"
    assert full.pipeline_status == "pipeline_motion_candidate_ready"
    assert "sk_fv_history_flow" in full.active_terms
    assert full.direct_execution_allowed is False
    _assert_boundary(full)

    proto = run_samvrti_to_physical_motion_builder(
        QiEvidenceBuilderInput(
            qi_id="builder-proto-demo",
            world_id="public-core-world",
            observer_surface="reviewer-visible",
            scale_id="v0_1",
            source_trace=("samvrti-builder-demo",),
            structural_support_present=True,
            numeric_terms={"gauge_connection_tendency": 0.2, "memory_kernel_backflow": 99.0},
        )
    )
    assert proto.bridge_status == "bridge_evidence_projected"
    assert proto.bridge_projected_level_hint == "ProtoQi"
    assert proto.packet_validated_type == "ProtoQi"
    assert "memory_kernel_backflow" in proto.ignored_terms
    _assert_boundary(proto)

    blocked = run_samvrti_to_physical_motion_builder(
        QiEvidenceBuilderInput(
            qi_id="builder-blocked-demo",
            world_id="public-core-world",
            observer_surface="reviewer-visible",
            scale_id="v0_1",
            source_trace=("samvrti-builder-demo",),
            numeric_terms={"sk_fv_history_flow": 1.0},
            direct_execution_requested=True,
        )
    )
    assert blocked.builder_status == "builder_not_opened_by_samvrti"
    assert blocked.bridge_status == "bridge_blocked"
    _assert_boundary(blocked)


if __name__ == "__main__":
    _self_check()
    print("[samvrti-qi-to-physical-motion-evidence-builder] PASS")