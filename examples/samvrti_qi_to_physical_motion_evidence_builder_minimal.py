#!/usr/bin/env python3
"""Minimal Samvrti Qi to Physical Motion evidence builder for KuuOS.

This adapter turns an accepted Samvrti Qi flow into a conservative physical Qi
packet candidate. It then delegates classification and motion evaluation to the
Physical Quantum Qi motion pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import sys
from typing import Any, Dict, Mapping

ROOT = Path(__file__).resolve().parents[1]
SAMVRTI_PATH = ROOT / "examples" / "samvrti_qi_runtime_adapter_minimal.py"
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
    observe_only: bool = True
    direct_execution_allowed: bool = False
    authority_expansion: bool = False


def _false_authority() -> Dict[str, bool]:
    return {
        "execution_authority": False,
        "belief_commit_authority": False,
        "memory_overwrite_authority": False,
        "world_root_rewrite_authority": False,
        "safety_override_authority": False,
    }


def build_conservative_evidence(builder_input: QiEvidenceBuilderInput) -> Dict[str, str]:
    evidence: Dict[str, str] = {
        "K_non_reification": "pass",
        "delta_rel_in_K_perp": "pass",
        "gauge_connection_A_mu": "pass",
    }

    if builder_input.structural_support_present:
        evidence.update({
            "string_mode_consistency": "pass",
            "brane_boundary_support": "pass",
        })

    if builder_input.transport_evidence_present and builder_input.structural_support_present:
        evidence.update({
            "curvature_F_munu": "pass",
            "Wilson_loop_residue": "pass",
        })

    if builder_input.current_evidence_present and builder_input.transport_evidence_present:
        evidence["current_J_Qi_mu"] = "pass"

    if builder_input.ward_evidence_present and builder_input.current_evidence_present:
        evidence["Ward_or_leak_identity"] = "pass"

    if builder_input.open_system_evidence_present and builder_input.ward_evidence_present:
        evidence.update({
            "density_state_rho": "pass",
            "Hamiltonian_H": "pass",
            "Lindblad_generator_L": "pass",
            "entropy_production_Sigma": "pass",
            "free_energy_F_beta": "pass",
            "DPI_gap": "pass",
            "recovery_margin": "pass",
            "mass_gap_floor_33_20": "pass",
        })

    if builder_input.full_path_evidence_present and builder_input.open_system_evidence_present:
        evidence.update({
            "SK_plus_branch": "pass",
            "SK_minus_branch": "pass",
            "FV_influence_functional": "pass",
            "memory_kernel": "pass",
            "noise_kernel": "pass",
            "observation_backaction": "pass",
            "noncommutative_operation_history": "pass",
            "path_measure_normalization": "pass",
        })

    return evidence


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
        )

    evidence = build_conservative_evidence(builder_input)
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
        observe_only=True,
        direct_execution_allowed=False,
        authority_expansion=False,
    )


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
    assert full.packet_validated_type == "FullPathQi"
    assert full.pipeline_status == "pipeline_motion_candidate_ready"
    assert "sk_fv_history_flow" in full.active_terms
    assert full.direct_execution_allowed is False

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
    assert proto.packet_validated_type == "ProtoQi"
    assert "memory_kernel_backflow" in proto.ignored_terms

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


if __name__ == "__main__":
    _self_check()
    print("[samvrti-qi-to-physical-motion-evidence-builder] PASS")
