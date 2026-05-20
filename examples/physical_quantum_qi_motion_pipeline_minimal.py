#!/usr/bin/env python3
"""Minimal Physical Quantum Qi motion pipeline for KuuOS.

This pipeline connects evidence-bound classification to dynamics licensing:
packet -> validated_type -> licensed motion terms -> observe-only motion candidate.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import sys
from typing import Any, Dict, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[1]
DYNAMICS_KERNEL_PATH = ROOT / "examples" / "physical_quantum_qi_dynamics_kernel_minimal.py"


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


dynamics = _load_module("physical_quantum_qi_dynamics_kernel_minimal", DYNAMICS_KERNEL_PATH)


@dataclass(frozen=True)
class QiMotionPipelineInput:
    packet_id: str
    packet: Mapping[str, Any]
    numeric_terms: Mapping[str, float]
    direct_execution_requested: bool = False
    unresolved_blockers: Tuple[str, ...] = ()


@dataclass(frozen=True)
class QiMotionPipelineDecision:
    pipeline_status: str
    validated_type: str
    classification_reason: str
    motion_status: str
    licensed_terms: Tuple[str, ...]
    active_terms: Tuple[str, ...]
    ignored_terms: Tuple[str, ...]
    motion_score: float
    reason_codes: Tuple[str, ...]
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


QI_LADDER: Tuple[str, ...] = (
    "NonQi",
    "PreQi",
    "ProtoQi",
    "TransportableQi",
    "CurvedQi",
    "CurrentQi",
    "PhysicalQi",
    "FullPathQi",
)


def _all_pass(evidence_status: Mapping[str, str], keys: Tuple[str, ...]) -> bool:
    return all(evidence_status.get(key) == "pass" for key in keys)


def classify_by_dynamics_evidence(packet: Mapping[str, Any]) -> Tuple[str, str]:
    """Classify by available evidence without trusting claimed_type."""
    evidence = packet.get("evidence_status", {})
    if not isinstance(evidence, Mapping):
        return "Reject", "evidence_status is not a mapping"
    authority = packet.get("authority", {})
    if not isinstance(authority, Mapping):
        return "Reject", "authority is not a mapping"

    for key in (
        "execution_authority",
        "belief_commit_authority",
        "memory_overwrite_authority",
        "world_root_rewrite_authority",
        "safety_override_authority",
    ):
        if authority.get(key) is not False:
            return "Reject", "forbidden authority flag is not false"

    if packet.get("mass_gap_floor", {}).get("not_source_of_qi") is False:
        return "Reject", "mass-gap floor is incorrectly treated as source"

    for qi_type in reversed(QI_LADDER):
        required = dynamics.REQUIRED_EVIDENCE_BY_TYPE[qi_type]
        if _all_pass(evidence, required):
            return qi_type, f"validated as {qi_type} by evidence"
    return "Reject", "no evidence-bound Qi level available"


def run_physical_quantum_qi_motion_pipeline(
    pipeline_input: QiMotionPipelineInput,
) -> QiMotionPipelineDecision:
    validated_type, classification_reason = classify_by_dynamics_evidence(pipeline_input.packet)

    if validated_type == "Reject":
        return QiMotionPipelineDecision(
            pipeline_status="pipeline_blocked_by_classification",
            validated_type=validated_type,
            classification_reason=classification_reason,
            motion_status="qi_motion_blocked",
            licensed_terms=(),
            active_terms=(),
            ignored_terms=tuple(sorted(pipeline_input.numeric_terms.keys())),
            motion_score=0.0,
            reason_codes=("QI_PIPELINE_BLOCKED_BY_CLASSIFICATION",),
        )

    motion = dynamics.evaluate_physical_quantum_qi_dynamics(
        dynamics.QiDynamicsInput(
            packet_id=pipeline_input.packet_id,
            validated_type=validated_type,
            evidence_status=pipeline_input.packet.get("evidence_status", {}),
            numeric_terms=pipeline_input.numeric_terms,
            authority=pipeline_input.packet.get("authority", {}),
            direct_execution_requested=pipeline_input.direct_execution_requested,
            unresolved_blockers=pipeline_input.unresolved_blockers,
        )
    )

    if motion.motion_status == "qi_motion_candidate_ready":
        pipeline_status = "pipeline_motion_candidate_ready"
    elif motion.motion_status == "qi_motion_not_licensed":
        pipeline_status = "pipeline_no_qi_motion_licensed"
    elif motion.motion_status == "qi_motion_held":
        pipeline_status = "pipeline_motion_held"
    else:
        pipeline_status = "pipeline_motion_blocked"

    return QiMotionPipelineDecision(
        pipeline_status=pipeline_status,
        validated_type=validated_type,
        classification_reason=classification_reason,
        motion_status=motion.motion_status,
        licensed_terms=motion.licensed_terms,
        active_terms=motion.active_terms,
        ignored_terms=motion.ignored_terms,
        motion_score=motion.motion_score,
        reason_codes=motion.reason_codes,
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


def _false_authority() -> Dict[str, bool]:
    return {
        "execution_authority": False,
        "belief_commit_authority": False,
        "memory_overwrite_authority": False,
        "world_root_rewrite_authority": False,
        "safety_override_authority": False,
    }


def _packet_for(qi_type: str) -> Dict[str, Any]:
    return {
        "packet_id": f"motion-pipeline-{qi_type}",
        "claimed_type": "untrusted_claim",
        "evidence_status": {key: "pass" for key in dynamics.REQUIRED_EVIDENCE_BY_TYPE[qi_type]},
        "mass_gap_floor": {"not_source_of_qi": True},
        "authority": _false_authority(),
    }


def _assert_medical_modality_neutral(decision: QiMotionPipelineDecision) -> None:
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
    full = run_physical_quantum_qi_motion_pipeline(
        QiMotionPipelineInput(
            packet_id="motion-pipeline-fullpath-demo",
            packet=_packet_for("FullPathQi"),
            numeric_terms={
                "sk_fv_history_flow": 1.0,
                "memory_kernel_backflow": 0.5,
                "noise_kernel_diffusion": 0.1,
            },
        )
    )
    assert full.pipeline_status == "pipeline_motion_candidate_ready"
    assert full.validated_type == "FullPathQi"
    assert "sk_fv_history_flow" in full.active_terms
    assert full.direct_execution_allowed is False
    _assert_medical_modality_neutral(full)

    proto = run_physical_quantum_qi_motion_pipeline(
        QiMotionPipelineInput(
            packet_id="motion-pipeline-proto-demo",
            packet=_packet_for("ProtoQi"),
            numeric_terms={"gauge_connection_tendency": 0.2, "memory_kernel_backflow": 99.0},
        )
    )
    assert proto.validated_type == "ProtoQi"
    assert "memory_kernel_backflow" in proto.ignored_terms
    _assert_medical_modality_neutral(proto)

    blocked_packet = _packet_for("FullPathQi")
    blocked_packet["authority"] = dict(blocked_packet["authority"])
    blocked_packet["authority"]["execution_authority"] = True
    blocked = run_physical_quantum_qi_motion_pipeline(
        QiMotionPipelineInput(
            packet_id="motion-pipeline-block-demo",
            packet=blocked_packet,
            numeric_terms={"sk_fv_history_flow": 1.0},
        )
    )
    assert blocked.pipeline_status == "pipeline_blocked_by_classification"
    _assert_medical_modality_neutral(blocked)


if __name__ == "__main__":
    _self_check()
    print("[physical-quantum-qi-motion-pipeline] PASS")