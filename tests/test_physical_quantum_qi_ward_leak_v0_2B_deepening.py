#!/usr/bin/env python3
"""Regression tests for Physical Quantum Qi Ward/leak identity v0.2B.

These tests verify that the deepening validator rejects nonphysical Ward/leak
claims: current without action variation, open trace without leak accounting,
nonzero W_leak residual, closed conservation claimed for an open trace, and
anomaly hidden as ordinary leak.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_physical_quantum_qi_deepening_v0_2 import load_json, validate_packet  # noqa: E402

SPEC = load_json(ROOT / "specs" / "physical_quantum_qi_deepening_contract_v0_2.json")

AUTHORITY_FALSE = {
    "proof_authority": False,
    "ontology_authority": False,
    "clinical_authority": False,
    "execution_authority": False,
    "commit_authority": False,
    "belief_commit_authority": False,
    "belief_root_commit_authority": False,
    "memory_overwrite_authority": False,
    "world_root_rewrite_authority": False,
    "truth_authority": False,
    "safety_override_authority": False,
}


def base_b_payload() -> dict[str, object]:
    return {
        "S_eff_declared": "pass",
        "A_mu_variation_declared": "pass",
        "metric_density_factor_declared": "pass",
        "CTP_branch_current_declared": "pass",
        "current_domain_declared": "pass",
        "J_boundary_declared": "pass",
        "J_rel_declared": "pass",
        "J_IF_declared": "pass",
        "open_system_current_component_declared": "pass",
        "D_mu_J_declared": "pass",
        "open_or_closed_case_declared": "pass",
        "L_leak_declared": "pass",
        "A_anom_declared_or_zero": "pass",
        "R_res_declared_or_zero": "pass",
        "W_leak_residual_declared": "pass",
        "W_leak_tolerance_declared": "pass",
        "leak_term_decomposition_declared": "pass",
        "anomaly_origin_declared_or_zero": "pass",
        "residue_origin_declared_or_zero": "pass",
        "W_leak_residual_value": 0.0,
        "closed_conservation_claimed": False,
        "open_system_trace_declared": True,
        "anomaly_hidden_as_leak": False,
        "leak_residual_hidden": False,
    }


def packet(payload: dict[str, object]) -> dict[str, object]:
    return {
        "modules": {"Ward_leak_identity_v0_2B": payload},
        "authority": dict(AUTHORITY_FALSE),
    }


def assert_fails_with(payload: dict[str, object], expected_substring: str) -> None:
    ok, errors = validate_packet(packet(payload), SPEC)
    assert not ok, "packet unexpectedly passed"
    joined = " | ".join(errors)
    assert expected_substring in joined, joined


def test_ward_leak_v02b_positive_minimal_passes() -> None:
    ok, errors = validate_packet(packet(base_b_payload()), SPEC)
    assert ok, errors


def test_j_qi_without_action_variation_fails() -> None:
    payload = base_b_payload()
    payload["A_mu_variation_declared"] = "missing"
    assert_fails_with(payload, "requires J_Qi as action variation")


def test_open_trace_without_leak_term_fails() -> None:
    payload = base_b_payload()
    payload["L_leak_declared"] = "missing"
    payload["open_system_trace_declared"] = True
    assert_fails_with(payload, "open system requires L_leak")


def test_nonzero_w_leak_blocks_fullpathqi() -> None:
    payload = base_b_payload()
    payload["W_leak_residual_value"] = 0.01
    assert_fails_with(payload, "nonzero W_leak residual blocks")


def test_closed_conservation_with_open_trace_fails() -> None:
    payload = base_b_payload()
    payload["closed_conservation_claimed"] = True
    payload["open_system_trace_declared"] = True
    assert_fails_with(payload, "closed conservation claim with open trace")


def test_anomaly_hidden_as_leak_fails() -> None:
    payload = base_b_payload()
    payload["anomaly_hidden_as_leak"] = True
    assert_fails_with(payload, "anomaly hidden as leak")


def test_hidden_leak_residual_fails() -> None:
    payload = base_b_payload()
    payload["leak_residual_hidden"] = True
    assert_fails_with(payload, "hidden leak residual")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("Physical Quantum Qi Ward/leak v0.2B regression tests passed.")
