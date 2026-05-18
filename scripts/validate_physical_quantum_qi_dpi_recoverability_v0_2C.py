#!/usr/bin/env python3
"""Validate Physical Quantum Qi DPI recoverability theoremization v0.2C."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_dpi_recoverability_packet_v0_2C.json"

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
    "states_and_channel",
    "DPI_gap",
    "Qi_recoverability_score",
    "irreversibility_burden",
    "recovery_margin",
    "repair_rollback_gate",
    "theorem_targets",
    "authority_boundary",
    "rejected_claims",
}

REQUIRED_STATES = {
    "rho_declared",
    "sigma_declared",
    "channel_E_declared",
    "CPTP_channel_declared",
    "relative_entropy_declared",
    "support_condition_declared",
}

REQUIRED_DPI = {
    "Delta_DPI_defined",
    "Delta_DPI_value_declared",
    "DPI_nonnegative_declared",
    "DPI_channel_loss_interpretation_declared",
    "DPI_equality_recovery_condition_declared",
}

REQUIRED_RQI = {
    "R_Qi_defined",
    "R_Qi_value_declared",
    "R_Qi_range_declared",
    "R_Qi_monotone_in_Delta_DPI_declared",
    "optional_recovery_fidelity_witness_declared_if_used",
}

REQUIRED_ETA = {
    "eta_Qi_defined",
    "Sigma_declared",
    "C_lockin_declared",
    "C_mem_declared",
    "C_obs_declared",
    "eta_Qi_value_declared",
    "nonnegative_burden_terms_declared",
}

REQUIRED_DELTA_REC = {
    "delta_rec_defined",
    "delta_rec_value_declared",
    "delta_rec_sign_declared",
    "delta_rec_positive_opens_evaluation_declared",
    "delta_rec_nonpositive_blocks_recovery_declared",
    "nonauthority_boundary_declared",
}

REQUIRED_GATE = {
    "repair_rollback_gate_declared",
    "recovery_evaluation_open_when_delta_rec_positive",
    "recovery_blocked_when_delta_rec_nonpositive",
    "positive_delta_rec_is_not_execution_authority",
    "positive_delta_rec_is_not_automatic_rollback",
    "positive_delta_rec_is_not_memory_overwrite",
    "positive_delta_rec_is_not_world_root_rewrite",
}

REQUIRED_THEOREMS = {
    "DPI_nonnegativity_gate",
    "Recoverability_range",
    "Nonnegative_burden",
    "Recovery_gate_positive",
    "Recovery_gate_nonpositive",
    "NonAuthority_theorem",
}

REQUIRED_REJECTIONS = {
    "DPI_claim_without_states",
    "DPI_claim_without_channel",
    "relative_entropy_without_support_condition",
    "negative_Delta_DPI_without_diagnostic",
    "DPI_loss_erasure",
    "R_Qi_without_Delta_DPI",
    "recoverability_score_grants_authority",
    "eta_Qi_without_entropy_production",
    "lockin_ignored",
    "nonMarkov_memory_burden_ignored",
    "observation_burden_ignored",
    "repair_claim_without_delta_rec",
    "rollback_claim_without_delta_rec",
    "positive_delta_rec_claimed_as_execution_authority",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def missing(required: Iterable[str], actual: Iterable[str]) -> List[str]:
    return sorted(set(required) - set(actual))


def section(packet: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = packet.get(key)
    return value if isinstance(value, dict) else {}


def require_bool_true(obj: Dict[str, Any], keys: Iterable[str], prefix: str) -> List[str]:
    return [f"{prefix}.{key} must be true" for key in sorted(keys) if obj.get(key) is not True]


def validate_shape(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    errors.extend([f"missing top-level key: {x}" for x in missing(REQUIRED_TOP_LEVEL, packet.keys())])
    if packet.get("packet_id") != "physical_quantum_qi_dpi_recoverability_packet_v0_2C":
        errors.append("packet_id mismatch")
    if packet.get("packet_type") != "dpi_recoverability_equation_packet":
        errors.append("packet_type must be dpi_recoverability_equation_packet")

    section_requirements = [
        ("states_and_channel", REQUIRED_STATES),
        ("DPI_gap", REQUIRED_DPI),
        ("Qi_recoverability_score", REQUIRED_RQI),
        ("irreversibility_burden", REQUIRED_ETA),
        ("recovery_margin", REQUIRED_DELTA_REC),
        ("repair_rollback_gate", REQUIRED_GATE),
        ("theorem_targets", REQUIRED_THEOREMS),
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


def validate_numeric_theorems(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    states = section(packet, "states_and_channel")
    dpi = section(packet, "DPI_gap")
    rqi = section(packet, "Qi_recoverability_score")
    eta = section(packet, "irreversibility_burden")
    delta = section(packet, "recovery_margin")
    gate = section(packet, "repair_rollback_gate")

    errors.extend(require_bool_true(states, ["rho_declared", "sigma_declared", "channel_E_declared", "CPTP_channel_declared"], "states_and_channel"))
    errors.extend(require_bool_true(dpi, ["DPI_nonnegative_declared"], "DPI_gap"))
    errors.extend(require_bool_true(rqi, ["R_Qi_monotone_in_Delta_DPI_declared"], "Qi_recoverability_score"))
    errors.extend(require_bool_true(eta, ["nonnegative_burden_terms_declared"], "irreversibility_burden"))
    errors.extend(require_bool_true(delta, ["delta_rec_positive_opens_evaluation_declared", "delta_rec_nonpositive_blocks_recovery_declared", "nonauthority_boundary_declared"], "recovery_margin"))
    errors.extend(require_bool_true(gate, REQUIRED_GATE, "repair_rollback_gate"))

    delta_dpi = dpi.get("Delta_DPI_value_declared")
    rqi_value = rqi.get("R_Qi_value_declared")
    sigma = eta.get("Sigma_declared")
    c_lockin = eta.get("C_lockin_declared")
    c_mem = eta.get("C_mem_declared")
    c_obs = eta.get("C_obs_declared")
    eta_value = eta.get("eta_Qi_value_declared")
    delta_rec = delta.get("delta_rec_value_declared")

    numeric_values = {
        "Delta_DPI_value_declared": delta_dpi,
        "R_Qi_value_declared": rqi_value,
        "Sigma_declared": sigma,
        "C_lockin_declared": c_lockin,
        "C_mem_declared": c_mem,
        "C_obs_declared": c_obs,
        "eta_Qi_value_declared": eta_value,
        "delta_rec_value_declared": delta_rec,
    }
    for key, value in numeric_values.items():
        if not isinstance(value, (int, float)):
            errors.append(f"{key} must be numeric")

    if errors:
        return errors

    if delta_dpi < 0 and not dpi.get("numerical_diagnostic_error_declared"):
        errors.append("Delta_DPI must be nonnegative unless numerical_diagnostic_error_declared is true")

    expected_rqi = math.exp(-float(delta_dpi))
    if abs(float(rqi_value) - expected_rqi) > 1e-6:
        errors.append(f"R_Qi_value_declared must equal exp(-Delta_DPI), expected {expected_rqi}")
    if not (0 < float(rqi_value) <= 1):
        errors.append("R_Qi_value_declared must satisfy 0 < R_Qi <= 1")

    for key, value in [("Sigma", sigma), ("C_lockin", c_lockin), ("C_mem", c_mem), ("C_obs", c_obs)]:
        if float(value) < 0:
            errors.append(f"{key} must be nonnegative under default convention")

    expected_eta = float(delta_dpi) + float(sigma) + float(c_lockin) + float(c_mem) + float(c_obs)
    if abs(float(eta_value) - expected_eta) > 1e-6:
        errors.append(f"eta_Qi_value_declared must equal Delta_DPI + Sigma + C_lockin + C_mem + C_obs, expected {expected_eta}")

    expected_delta_rec = float(rqi_value) - float(eta_value)
    if abs(float(delta_rec) - expected_delta_rec) > 1e-6:
        errors.append(f"delta_rec_value_declared must equal R_Qi - eta_Qi, expected {expected_delta_rec}")

    sign = delta.get("delta_rec_sign_declared")
    if float(delta_rec) > 0 and sign != "positive":
        errors.append("delta_rec_sign_declared must be positive when delta_rec > 0")
    if float(delta_rec) <= 0 and sign != "nonpositive":
        errors.append("delta_rec_sign_declared must be nonpositive when delta_rec <= 0")

    return errors


def validate_theorem_text(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    theorem_targets = section(packet, "theorem_targets")
    required_tokens = {
        "DPI_nonnegativity_gate": ["Delta_DPI", ">= 0"],
        "Recoverability_range": ["R_Qi", "<= 1"],
        "Nonnegative_burden": ["eta_Qi", ">= 0"],
        "Recovery_gate_positive": ["delta_rec > 0", "RecoveryEvaluationOpen"],
        "Recovery_gate_nonpositive": ["delta_rec <= 0", "RecoveryBlocked"],
        "NonAuthority_theorem": ["does not imply ExecutionAuthority"],
    }
    for key, tokens in required_tokens.items():
        text = str(theorem_targets.get(key, ""))
        for token in tokens:
            if token not in text:
                errors.append(f"theorem_targets.{key} missing token: {token}")
    return errors


def main() -> int:
    packet = load_json(PACKET_PATH)
    errors: List[str] = []
    errors.extend(validate_shape(packet))
    errors.extend(validate_numeric_theorems(packet))
    errors.extend(validate_theorem_text(packet))

    if errors:
        print("Physical Quantum Qi DPI recoverability v0.2C validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Physical Quantum Qi DPI recoverability v0.2C validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
