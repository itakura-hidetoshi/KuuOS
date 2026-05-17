#!/usr/bin/env python3
"""Physical Quantum Qi -> KuuOS OS bridge packet v0.2.

This module turns a phase handoff into concrete, OS-readable payloads.
It is intentionally non-executing: no bridge packet grants execution, commit,
belief-root commit, memory overwrite, world-root rewrite, proof, ontology,
truth, clinical, or safety-override authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Mapping, MutableMapping, Sequence

from physical_quantum_qi_phase_runtime_v0_2 import QiHandoff, QiPhase

AUTHORITY_FALSE_KEYS = [
    "execution_authority",
    "commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "clinical_authority",
    "proof_authority",
    "ontology_authority",
    "truth_authority",
    "safety_override_authority",
]

OS_SURFACE_TO_PAYLOAD = {
    "BeliefOS.observation_candidate": "BeliefOS",
    "PlanOS.preparation_surface": "PlanOS",
    "PlanOS.boundary_candidate": "PlanOS",
    "PlanOS.transport_candidate": "PlanOS",
    "DecisionOS.safety_evaluable_candidate": "DecisionOS",
    "MemoryOS.recordable_history_candidate": "MemoryOS",
    "ReflectionOS.residue_analysis_candidate": "ReflectionOS",
}


@dataclass(frozen=True)
class QiOSBridgePacket:
    """OS-readable packet generated from a Qi phase handoff."""

    packet_id: str
    source: str
    phase: QiPhase
    handoff_status: str
    allowed_surfaces: List[str]
    os_payloads: Dict[str, Dict[str, object]]
    required_next_actions: List[str]
    blockers: List[str]
    authority: Dict[str, bool] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)



def _authority_false_map() -> Dict[str, bool]:
    return {key: False for key in AUTHORITY_FALSE_KEYS}



def _empty_os_payloads() -> Dict[str, Dict[str, object]]:
    return {
        "BeliefOS": {
            "surface": None,
            "observation_candidate": False,
            "belief_root_commit_authority": False,
            "status": "inactive",
        },
        "PlanOS": {
            "surfaces": [],
            "transport_candidate": False,
            "execution_authority": False,
            "status": "inactive",
        },
        "DecisionOS": {
            "safety_evaluable_candidate": False,
            "safety_override_authority": False,
            "execution_authority": False,
            "status": "inactive",
        },
        "MemoryOS": {
            "recordable_history_candidate": False,
            "memory_overwrite_authority": False,
            "status": "inactive",
        },
        "ReflectionOS": {
            "residue_analysis_candidate": False,
            "world_root_rewrite_authority": False,
            "status": "inactive",
        },
    }



def build_qi_os_bridge_packet(
    handoff: QiHandoff,
    *,
    packet_id: str = "physical_quantum_qi_os_bridge_packet_v0_2",
    source: str = "physical_quantum_qi_phase_runtime_v0_2",
) -> QiOSBridgePacket:
    """Build a concrete bridge packet from a phase handoff.

    The packet is a dispatchable data structure for KuuOS internals, but it
    remains candidate-only.  The bridge only tells each OS which surface may
    receive the Qi phase record; it does not perform the receiving OS action.
    """

    payloads = _empty_os_payloads()

    for surface in handoff.allowed_surfaces:
        target = OS_SURFACE_TO_PAYLOAD.get(surface)
        if target is None:
            continue

        if target == "BeliefOS":
            payloads[target].update(
                {
                    "surface": surface,
                    "observation_candidate": True,
                    "phase": handoff.phase.value,
                    "handoff_status": handoff.status,
                    "status": "candidate",
                }
            )
        elif target == "PlanOS":
            surfaces = list(payloads[target].get("surfaces", []))
            surfaces.append(surface)
            payloads[target].update(
                {
                    "surfaces": surfaces,
                    "transport_candidate": "PlanOS.transport_candidate" in surfaces,
                    "phase": handoff.phase.value,
                    "handoff_status": handoff.status,
                    "status": "candidate",
                }
            )
        elif target == "DecisionOS":
            payloads[target].update(
                {
                    "safety_evaluable_candidate": True,
                    "phase": handoff.phase.value,
                    "handoff_status": handoff.status,
                    "status": "candidate",
                }
            )
        elif target == "MemoryOS":
            payloads[target].update(
                {
                    "recordable_history_candidate": True,
                    "phase": handoff.phase.value,
                    "handoff_status": handoff.status,
                    "status": "candidate",
                }
            )
        elif target == "ReflectionOS":
            payloads[target].update(
                {
                    "residue_analysis_candidate": True,
                    "phase": handoff.phase.value,
                    "handoff_status": handoff.status,
                    "status": "candidate",
                }
            )

    return QiOSBridgePacket(
        packet_id=packet_id,
        source=source,
        phase=handoff.phase,
        handoff_status=handoff.status,
        allowed_surfaces=list(handoff.allowed_surfaces),
        os_payloads=payloads,
        required_next_actions=list(handoff.required_next_actions),
        blockers=list(handoff.blockers),
        authority=_authority_false_map(),
        notes=[
            "routing_surface_only",
            "candidate_only",
            "no_execution_or_commit_authority",
        ],
    )



def bridge_packet_to_dict(packet: QiOSBridgePacket) -> Dict[str, object]:
    return {
        "packet_id": packet.packet_id,
        "source": packet.source,
        "phase": packet.phase.value,
        "handoff_status": packet.handoff_status,
        "allowed_surfaces": packet.allowed_surfaces,
        "os_payloads": packet.os_payloads,
        "required_next_actions": packet.required_next_actions,
        "blockers": packet.blockers,
        "authority": packet.authority,
        "notes": packet.notes,
    }



def validate_qi_os_bridge_packet(packet: Mapping[str, object]) -> List[str]:
    """Return validation errors for a bridge packet dictionary."""

    errors: List[str] = []
    authority = packet.get("authority", {})
    if not isinstance(authority, Mapping):
        errors.append("authority must be an object")
    else:
        for key in AUTHORITY_FALSE_KEYS:
            if authority.get(key) is not False:
                errors.append(f"authority.{key} must be false")

    payloads = packet.get("os_payloads", {})
    if not isinstance(payloads, Mapping):
        errors.append("os_payloads must be an object")
        return errors

    allowed_surfaces = packet.get("allowed_surfaces", [])
    if not isinstance(allowed_surfaces, Sequence) or isinstance(allowed_surfaces, (str, bytes)):
        errors.append("allowed_surfaces must be a list")
        return errors

    surfaces = set(str(x) for x in allowed_surfaces)

    if "DecisionOS.safety_evaluable_candidate" in surfaces:
        decision = payloads.get("DecisionOS", {})
        if not isinstance(decision, Mapping) or decision.get("safety_evaluable_candidate") is not True:
            errors.append("DecisionOS payload must expose safety_evaluable_candidate")

    if "MemoryOS.recordable_history_candidate" in surfaces:
        memory = payloads.get("MemoryOS", {})
        if not isinstance(memory, Mapping) or memory.get("recordable_history_candidate") is not True:
            errors.append("MemoryOS payload must expose recordable_history_candidate")

    if "ReflectionOS.residue_analysis_candidate" in surfaces:
        reflection = payloads.get("ReflectionOS", {})
        if not isinstance(reflection, Mapping) or reflection.get("residue_analysis_candidate") is not True:
            errors.append("ReflectionOS payload must expose residue_analysis_candidate")

    for os_name, payload in payloads.items():
        if not isinstance(payload, Mapping):
            errors.append(f"{os_name} payload must be an object")
            continue
        for forbidden_key in [
            "execution_authority",
            "belief_root_commit_authority",
            "memory_overwrite_authority",
            "world_root_rewrite_authority",
            "safety_override_authority",
        ]:
            if forbidden_key in payload and payload.get(forbidden_key) is not False:
                errors.append(f"{os_name}.{forbidden_key} must be false")

    return errors
