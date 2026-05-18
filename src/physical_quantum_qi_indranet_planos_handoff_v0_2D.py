#!/usr/bin/env python3
"""PlanOS handoff for Physical Quantum Qi IndraNet transport v0.2D.

This module converts a valid IndraNet gauge-transport runtime result into a
PlanOS transport candidate packet. It is not an audit layer and does not grant
execution or commit authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from physical_quantum_qi_indranet_transport_runtime_v0_2D import (
    IndraNetTransportGateResult,
    IndraNetTransportStatus,
    candidate_from_packet,
    evaluate_indranet_transport,
    result_to_dict,
)

AUTHORITY_FALSE_FIELDS = (
    "execution_authority",
    "commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "proof_authority",
    "ontology_authority",
    "clinical_authority",
    "truth_authority",
    "safety_override_authority",
)


@dataclass(frozen=True)
class PlanOSTransportHandoff:
    handoff_id: str
    source_packet_id: str
    transport_status: str
    accepted_by_planos: bool
    allowed_surface: str = "PlanOS.transport_candidate"
    residue_surface: str = "ReflectionOS.residue_analysis_candidate"
    blockers: List[str] = field(default_factory=list)
    required_next_actions: List[str] = field(default_factory=list)
    transport_runtime_result: Dict[str, Any] = field(default_factory=dict)
    execution_authority: bool = False
    commit_authority: bool = False
    belief_root_commit_authority: bool = False
    memory_overwrite_authority: bool = False
    world_root_rewrite_authority: bool = False
    proof_authority: bool = False
    ontology_authority: bool = False
    clinical_authority: bool = False
    truth_authority: bool = False
    safety_override_authority: bool = False


def build_planos_transport_handoff(packet: Dict[str, Any]) -> PlanOSTransportHandoff:
    result = evaluate_indranet_transport(candidate_from_packet(packet))
    accepted = result.status is IndraNetTransportStatus.VALID_TRANSPORT_CANDIDATE and result.valid
    return PlanOSTransportHandoff(
        handoff_id="physical_quantum_qi_indranet_planos_handoff_v0_2D",
        source_packet_id=str(packet.get("packet_id", "unknown")),
        transport_status=result.status.value,
        accepted_by_planos=accepted,
        blockers=list(result.blockers),
        required_next_actions=list(result.required_next_actions),
        transport_runtime_result=result_to_dict(result),
    )


def handoff_to_dict(handoff: PlanOSTransportHandoff) -> Dict[str, Any]:
    return {
        "handoff_id": handoff.handoff_id,
        "source_packet_id": handoff.source_packet_id,
        "transport_status": handoff.transport_status,
        "accepted_by_planos": handoff.accepted_by_planos,
        "allowed_surface": handoff.allowed_surface,
        "residue_surface": handoff.residue_surface,
        "blockers": handoff.blockers,
        "required_next_actions": handoff.required_next_actions,
        "transport_runtime_result": handoff.transport_runtime_result,
        "execution_authority": handoff.execution_authority,
        "commit_authority": handoff.commit_authority,
        "belief_root_commit_authority": handoff.belief_root_commit_authority,
        "memory_overwrite_authority": handoff.memory_overwrite_authority,
        "world_root_rewrite_authority": handoff.world_root_rewrite_authority,
        "proof_authority": handoff.proof_authority,
        "ontology_authority": handoff.ontology_authority,
        "clinical_authority": handoff.clinical_authority,
        "truth_authority": handoff.truth_authority,
        "safety_override_authority": handoff.safety_override_authority,
    }


def validate_planos_transport_handoff(payload: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if payload.get("handoff_id") != "physical_quantum_qi_indranet_planos_handoff_v0_2D":
        errors.append("handoff_id mismatch")
    if payload.get("allowed_surface") != "PlanOS.transport_candidate":
        errors.append("allowed_surface must be PlanOS.transport_candidate")
    if payload.get("residue_surface") != "ReflectionOS.residue_analysis_candidate":
        errors.append("residue_surface must be ReflectionOS.residue_analysis_candidate")
    for field in AUTHORITY_FALSE_FIELDS:
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    runtime = payload.get("transport_runtime_result", {})
    if not isinstance(runtime, dict):
        errors.append("transport_runtime_result must be object")
    elif payload.get("accepted_by_planos") is True:
        if runtime.get("status") != "valid_transport_candidate":
            errors.append("accepted_by_planos requires valid_transport_candidate")
        if runtime.get("valid") is not True:
            errors.append("accepted_by_planos requires runtime valid true")
    return errors


def build_and_validate_planos_transport_handoff(packet: Dict[str, Any]) -> Dict[str, Any]:
    payload = handoff_to_dict(build_planos_transport_handoff(packet))
    errors = validate_planos_transport_handoff(payload)
    if errors:
        payload["validation_errors"] = errors
    return payload
