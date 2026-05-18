#!/usr/bin/env python3
"""Validate Physical Quantum Qi non-Markov memory packet v0.2E.

This validator fixes Qi memory as primary non-Markovian semantics.
It rejects Markov reduction, current-state-only identity/recoverability/transport
safety, missing history kernels, hidden finite-window tail residue, erased
holonomy/leak/rollback/recovery history, and authority expansion.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "examples" / "physical_quantum_qi_non_markov_memory_packet_v0_2E.json"

REQUIRED_MEMORY_SEMANTICS_TRUE = [
    "qi_memory_primary",
    "qi_is_non_markovian_by_definition",
    "markov_reduction_forbidden_as_qi_semantics",
    "current_state_only_identity_forbidden",
    "current_state_only_recoverability_forbidden",
    "current_state_only_transport_safety_forbidden",
]

REQUIRED_CANONICAL_CURRENT_TRUE = [
    "J_bare_declared",
    "K_Qi_history_kernel_declared",
    "X_history_vector_declared",
    "H_Qi_holonomy_history_kernel_declared",
    "U_gamma_history_transport_declared",
    "R_Qi_mem_residue_declared",
    "current_depends_on_full_admissible_history",
]

REQUIRED_MEMORY_KERNELS = [
    "K_body",
    "K_boundary",
    "K_leak",
    "K_observation",
    "K_holonomy",
    "K_recovery",
    "K_rollback",
    "K_lockin",
    "K_residue",
]

REQUIRED_FINITE_WINDOW_TRUE = [
    "allowed_only_as_history_preserving_projection",
    "history_window_L_declared",
    "kernel_tail_bound_declared",
    "discarded_tail_residue_declared",
    "holonomy_tail_residue_declared",
    "boundary_leak_tail_residue_declared",
    "observation_tail_burden_declared",
    "recovery_tail_debt_declared",
    "rollback_tail_debt_declared",
    "lockin_tail_residue_declared",
]

REQUIRED_RECOVERABILITY_TRUE = [
    "delta_rec_depends_on_M_Qi_0_t",
    "past_leak_affects_delta_rec",
    "past_observation_burden_affects_delta_rec",
    "past_lockin_affects_delta_rec",
    "past_holonomy_residue_affects_delta_rec",
    "past_failed_repair_affects_delta_rec",
    "past_rollback_affects_delta_rec",
    "positive_local_recovery_does_not_erase_recovery_debt",
]

REQUIRED_TRANSPORT_TRUE = [
    "U_Gamma_0_t_declared",
    "W_C_history_declared",
    "scope_drift_history_declared",
    "holonomy_residue_history_declared",
    "component_transport_residue_history_declared",
    "path_order_history_declared",
    "boundary_crossing_history_declared",
    "fresh_valid_path_cannot_erase_prior_holonomy_history",
]

REQUIRED_COMPRESSION_TRUE = [
    "compression_is_constrained_projection",
    "compression_is_not_deletion",
    "compressed_memory_cannot_replace_source_history",
    "unresolved_conflict_preserved",
    "boundary_leak_history_preserved",
    "holonomy_residue_preserved",
    "scope_drift_preserved",
    "recovery_failure_preserved",
    "rollback_history_preserved",
    "observation_burden_preserved",
    "authority_boundary_preserved",
]

REQUIRED_ALLOWED_SURFACES = {
    "PlanOS.transport_candidate",
    "MemoryOS.recordable_history_candidate",
    "ReflectionOS.residue_analysis_candidate",
    "BeliefOS.observation_candidate",
    "DecisionOS.safety_evaluable_candidate",
}

AUTHORITY_FALSE_FIELDS = [
    "execution_authority",
    "commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "proof_authority",
    "ontology_authority",
    "truth_authority",
    "clinical_authority",
    "safety_override_authority",
]


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def require_object(packet: Dict[str, Any], key: str, errors: List[str]) -> Dict[str, Any]:
    value = packet.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def require_true(section: Dict[str, Any], section_name: str, keys: List[str], errors: List[str]) -> None:
    for key in keys:
        if section.get(key) is not True:
            errors.append(f"{section_name}.{key} must be true")


def validate_shape(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "physical_quantum_qi_non_markov_memory_packet_v0_2E":
        errors.append("packet_id mismatch")
    if packet.get("packet_type") != "qi_non_markov_memory_packet":
        errors.append("packet_type must be qi_non_markov_memory_packet")
    if packet.get("version") != "v0.2E":
        errors.append("version must be v0.2E")
    if packet.get("root_design") != "docs/PHYSICAL_QUANTUM_QI_NON_MARKOV_MEMORY_v0_2E.md":
        errors.append("root_design must point to docs/PHYSICAL_QUANTUM_QI_NON_MARKOV_MEMORY_v0_2E.md")
    return errors


def validate_memory_semantics(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    section = require_object(packet, "memory_semantics", errors)
    require_true(section, "memory_semantics", REQUIRED_MEMORY_SEMANTICS_TRUE, errors)
    return errors


def validate_canonical_current(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    section = require_object(packet, "canonical_current", errors)
    require_true(section, "canonical_current", REQUIRED_CANONICAL_CURRENT_TRUE, errors)
    return errors


def validate_memory_kernel(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    kernel = require_object(packet, "memory_kernel", errors)
    for name in REQUIRED_MEMORY_KERNELS:
        item = kernel.get(name)
        if not isinstance(item, dict):
            errors.append(f"memory_kernel.{name} must be an object")
            continue
        if item.get("declared") is not True:
            errors.append(f"memory_kernel.{name}.declared must be true")
        if not isinstance(item.get("description"), str) or not item.get("description"):
            errors.append(f"memory_kernel.{name}.description must be nonempty")
    return errors


def validate_finite_window(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    section = require_object(packet, "finite_window_projection", errors)
    require_true(section, "finite_window_projection", REQUIRED_FINITE_WINDOW_TRUE, errors)
    if section.get("markov_semantic_substitute") is not False:
        errors.append("finite_window_projection.markov_semantic_substitute must be false")
    return errors


def validate_recoverability(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    section = require_object(packet, "non_markov_recoverability", errors)
    require_true(section, "non_markov_recoverability", REQUIRED_RECOVERABILITY_TRUE, errors)
    return errors


def validate_transport(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    section = require_object(packet, "non_markov_transport", errors)
    require_true(section, "non_markov_transport", REQUIRED_TRANSPORT_TRUE, errors)
    return errors


def validate_compression(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    section = require_object(packet, "compression_rule", errors)
    require_true(section, "compression_rule", REQUIRED_COMPRESSION_TRUE, errors)
    return errors


def validate_surfaces_and_authority(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    surfaces = packet.get("allowed_surfaces")
    if not isinstance(surfaces, list):
        errors.append("allowed_surfaces must be a list")
    else:
        missing = sorted(REQUIRED_ALLOWED_SURFACES - set(str(s) for s in surfaces))
        for surface in missing:
            errors.append(f"allowed_surfaces missing {surface}")
    authority = require_object(packet, "authority_boundary", errors)
    for field in AUTHORITY_FALSE_FIELDS:
        if authority.get(field) is not False:
            errors.append(f"authority_boundary.{field} must be false")
    return errors


def validate_packet(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    errors.extend(validate_shape(packet))
    errors.extend(validate_memory_semantics(packet))
    errors.extend(validate_canonical_current(packet))
    errors.extend(validate_memory_kernel(packet))
    errors.extend(validate_finite_window(packet))
    errors.extend(validate_recoverability(packet))
    errors.extend(validate_transport(packet))
    errors.extend(validate_compression(packet))
    errors.extend(validate_surfaces_and_authority(packet))
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    packet = load_json(path)
    errors = validate_packet(packet)
    if errors:
        print("Physical Quantum Qi non-Markov memory v0.2E validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Physical Quantum Qi non-Markov memory v0.2E validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
