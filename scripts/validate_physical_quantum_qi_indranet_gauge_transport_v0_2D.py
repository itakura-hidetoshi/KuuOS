#!/usr/bin/env python3
"""Validate Physical Quantum Qi IndraNet gauge transport geometry v0.2D."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_indranet_gauge_transport_packet_v0_2D.json"

AUTHORITY_FALSE_FIELDS = {
    "proof_authority",
    "ontology_authority",
    "clinical_authority",
    "execution_authority",
    "commit_authority",
    "belief_commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "truth_authority",
    "safety_override_authority",
}

REQUIRED_TOP_LEVEL = {
    "packet_id",
    "packet_type",
    "scope",
    "gauge_bundle_connection",
    "curvature",
    "path_transport",
    "holonomy_wilson_loop",
    "scope_drift",
    "transport_residue",
    "validity_gate",
    "authority_boundary",
    "rejected_claims",
}

REQUIRED_GAUGE = {
    "scope_manifold_or_site_declared",
    "bundle_E_declared",
    "gauge_group_or_algebra_declared",
    "A_mu_declared",
    "covariant_derivative_declared",
    "current_representation_declared",
}

REQUIRED_CURVATURE = {
    "F_munu_defined",
    "curvature_domain_declared",
    "noncommutative_term_declared",
    "flatness_status_declared",
    "curvature_visibility_declared",
}

REQUIRED_PATH = {
    "path_gamma_declared",
    "path_ordering_declared",
    "U_gamma_defined",
    "transport_representation_declared",
    "path_family_or_single_path_declared",
}

REQUIRED_HOLONOMY = {
    "closed_loop_C_declared",
    "U_C_defined",
    "W_C_defined",
    "holonomy_residue_declared",
    "wilson_residue_declared",
    "holonomy_tolerance_declared",
}

REQUIRED_SCOPE = {
    "source_scope_declared",
    "target_scope_declared",
    "scope_map_declared",
    "scope_metric_or_mismatch_declared",
    "scope_drift_value_or_bound_declared",
    "scope_drift_tolerance_declared",
    "sheaf_local_drift_declared",
}

REQUIRED_RESIDUE = {
    "transport_residue_vector_declared",
    "holonomy_residue_declared",
    "curvature_residue_declared",
    "scope_residue_declared",
    "path_residue_declared",
    "representation_residue_declared",
    "boundary_residue_declared",
    "scalar_residue_weights_declared_if_scalar_used",
    "component_residue_visibility_declared",
    "scalar_residue_summary",
}

REQUIRED_GATE = {
    "A_mu_required",
    "F_munu_required",
    "path_gamma_required",
    "U_gamma_required",
    "source_target_scope_required",
    "holonomy_or_Wilson_residue_required",
    "scope_drift_required",
    "transport_residue_visibility_required",
    "graph_only_transport_rejected",
    "nonauthority_boundary_declared",
}

REQUIRED_REJECTIONS = {
    "graph_edge_claimed_as_gauge_transport",
    "transport_without_connection",
    "current_transport_without_representation",
    "path_independence_claim_with_nonzero_curvature",
    "curvature_erasure",
    "flat_transport_claim_without_flatness_status",
    "transport_without_path",
    "path_order_erasure",
    "path_independence_without_flatness_or_holonomy_bound",
    "cycle_consistency_without_holonomy",
    "Wilson_loop_erasure",
    "holonomy_residue_hidden",
    "scope_free_transport_claim",
    "scope_drift_erasure",
    "transport_to_target_without_scope_compatibility",
    "residue_scalar_hides_component_failure",
    "holonomy_residue_erasure",
    "scope_residue_erasure",
    "representation_residue_erasure",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def section(packet: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = packet.get(key)
    return value if isinstance(value, dict) else {}


def missing(required: Iterable[str], actual: Iterable[str]) -> List[str]:
    return sorted(set(required) - set(actual))


def require_true(obj: Dict[str, Any], keys: Iterable[str], prefix: str) -> List[str]:
    return [f"{prefix}.{key} must be true" for key in sorted(keys) if obj.get(key) is not True]


def validate_shape(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    errors.extend([f"missing top-level key: {x}" for x in missing(REQUIRED_TOP_LEVEL, packet.keys())])
    if packet.get("packet_id") != "physical_quantum_qi_indranet_gauge_transport_packet_v0_2D":
        errors.append("packet_id mismatch")
    if packet.get("packet_type") != "indranet_gauge_transport_geometry_packet":
        errors.append("packet_type must be indranet_gauge_transport_geometry_packet")

    section_requirements = [
        ("gauge_bundle_connection", REQUIRED_GAUGE),
        ("curvature", REQUIRED_CURVATURE),
        ("path_transport", REQUIRED_PATH),
        ("holonomy_wilson_loop", REQUIRED_HOLONOMY),
        ("scope_drift", REQUIRED_SCOPE),
        ("transport_residue", REQUIRED_RESIDUE),
        ("validity_gate", REQUIRED_GATE),
    ]
    for sec, required in section_requirements:
        obj = section(packet, sec)
        errors.extend([f"{sec} missing key: {x}" for x in missing(required, obj.keys())])

    authority = section(packet, "authority_boundary")
    for key in sorted(AUTHORITY_FALSE_FIELDS):
        if authority.get(key) is not False:
            errors.append(f"authority_boundary.{key} must be false")

    rejected = packet.get("rejected_claims", [])
    if not isinstance(rejected, list):
        errors.append("rejected_claims must be a list")
    else:
        errors.extend([f"rejected_claims missing: {x}" for x in missing(REQUIRED_REJECTIONS, rejected)])
    return errors


def validate_geometry(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    gauge = section(packet, "gauge_bundle_connection")
    curvature = section(packet, "curvature")
    path = section(packet, "path_transport")
    hol = section(packet, "holonomy_wilson_loop")
    scope = section(packet, "scope_drift")
    residue = section(packet, "transport_residue")
    gate = section(packet, "validity_gate")

    errors.extend(require_true(gauge, ["scope_manifold_or_site_declared", "bundle_E_declared"], "gauge_bundle_connection"))
    errors.extend(require_true(curvature, ["curvature_visibility_declared"], "curvature"))
    errors.extend(require_true(path, ["path_ordering_declared"], "path_transport"))
    errors.extend(require_true(hol, ["closed_loop_C_declared"], "holonomy_wilson_loop"))
    errors.extend(require_true(residue, ["transport_residue_vector_declared", "component_residue_visibility_declared"], "transport_residue"))
    errors.extend(require_true(gate, REQUIRED_GATE, "validity_gate"))

    text_tokens = {
        ("gauge_bundle_connection", "A_mu_declared"): ["A_mu", "dx^mu"],
        ("gauge_bundle_connection", "covariant_derivative_declared"): ["D_mu", "A_mu"],
        ("curvature", "F_munu_defined"): ["partial_mu A_nu", "[A_mu,A_nu]"],
        ("path_transport", "U_gamma_defined"): ["P exp", "integral_gamma"],
        ("holonomy_wilson_loop", "W_C_defined"): ["W(C)", "Tr", "P exp"],
        ("scope_drift", "scope_metric_or_mismatch_declared"): ["d_scope"],
        ("scope_drift", "sheaf_local_drift_declared"): ["rho_i^j", "s_i"],
    }
    for (sec, key), tokens in text_tokens.items():
        value = str(section(packet, sec).get(key, ""))
        for token in tokens:
            if token not in value:
                errors.append(f"{sec}.{key} missing token: {token}")

    for key in ["holonomy_residue_declared", "curvature_residue_declared", "scope_residue_declared", "path_residue_declared", "representation_residue_declared", "boundary_residue_declared", "scalar_residue_summary"]:
        value = residue.get(key)
        if not isinstance(value, (int, float)):
            errors.append(f"transport_residue.{key} must be numeric")
        elif value < 0:
            errors.append(f"transport_residue.{key} must be nonnegative")

    scope_value = scope.get("scope_drift_value_or_bound_declared")
    scope_tol = scope.get("scope_drift_tolerance_declared")
    if isinstance(scope_value, (int, float)) and isinstance(scope_tol, (int, float)):
        if scope_value > scope_tol:
            errors.append("scope_drift exceeds declared tolerance")
    else:
        errors.append("scope_drift value and tolerance must be numeric")

    hol_tol = hol.get("holonomy_tolerance_declared")
    hol_value = residue.get("holonomy_residue_declared")
    if isinstance(hol_value, (int, float)) and isinstance(hol_tol, (int, float)):
        if hol_value > hol_tol:
            errors.append("holonomy residue exceeds declared tolerance")
    else:
        errors.append("holonomy residue and tolerance must be numeric")

    weights = residue.get("scalar_residue_weights_declared_if_scalar_used", {})
    if not isinstance(weights, dict):
        errors.append("transport_residue.scalar_residue_weights_declared_if_scalar_used must be object")
    else:
        for key in ["alpha_h", "alpha_c", "alpha_s", "alpha_p", "alpha_r", "alpha_b"]:
            if not isinstance(weights.get(key), (int, float)):
                errors.append(f"transport_residue weights missing numeric {key}")

    return errors


def main() -> int:
    packet = load_json(PACKET_PATH)
    errors: List[str] = []
    errors.extend(validate_shape(packet))
    errors.extend(validate_geometry(packet))

    if errors:
        print("Physical Quantum Qi IndraNet gauge transport v0.2D validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Physical Quantum Qi IndraNet gauge transport v0.2D validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
