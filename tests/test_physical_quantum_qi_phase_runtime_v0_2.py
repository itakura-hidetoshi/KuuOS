#!/usr/bin/env python3
"""Tests for Physical Quantum Qi phase runtime v0.2."""

from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_phase_runtime_v0_2 import (  # noqa: E402
    PhysicalQuantumQiState,
    QiPhase,
    SKFVHistory,
    WardLeakAccounting,
    classify_qi_phase,
    state_from_packet,
)


def assert_phase(state: PhysicalQuantumQiState, expected: QiPhase) -> None:
    result = classify_qi_phase(state)
    assert result.phase == expected, f"expected {expected}, got {result.phase}: {result}"


def base_state() -> PhysicalQuantumQiState:
    return PhysicalQuantumQiState(
        delta_rel_in_K_perp=True,
        delta_rel_nonzero=True,
        string_mode_worldsheet=True,
        brane_boundary=True,
        boundary_coupling=True,
        chi_delta_rel_defined=True,
        boundary_kernel_defined=True,
        A_mu_defined=True,
        F_munu_defined=True,
        gauge_projection_defined=True,
        holonomy_or_wilson_residue_defined=True,
        S_eff_defined=True,
        J_Qi_from_variation=True,
        current_decomposition_declared=True,
        ward_leak=WardLeakAccounting(
            open_identity_holds=True,
            leak_declared=True,
            anomaly_declared=True,
        ),
        sk_fv=SKFVHistory(
            plus_branch=True,
            minus_branch=True,
            influence_functional=True,
            memory_kernel=True,
            noise_kernel=True,
            observation_backaction=True,
            noncommutative_operation_history=True,
            path_measure_normalization=True,
            boundary_conditions=True,
            leak_identity_on_paths=True,
        ),
    )


def test_nonqi_without_delta_rel() -> None:
    assert_phase(PhysicalQuantumQiState(), QiPhase.NON_QI)


def test_preqi_with_delta_rel_only() -> None:
    assert_phase(
        PhysicalQuantumQiState(delta_rel_in_K_perp=True, delta_rel_nonzero=True),
        QiPhase.PRE_QI,
    )


def test_protoqi_with_stringmode_only() -> None:
    assert_phase(
        PhysicalQuantumQiState(
            delta_rel_in_K_perp=True,
            delta_rel_nonzero=True,
            string_mode_worldsheet=True,
        ),
        QiPhase.PROTO_QI,
    )


def test_boundaryqi_with_boundary_coupling_only() -> None:
    assert_phase(
        PhysicalQuantumQiState(
            delta_rel_in_K_perp=True,
            delta_rel_nonzero=True,
            string_mode_worldsheet=True,
            brane_boundary=True,
            boundary_coupling=True,
            chi_delta_rel_defined=True,
            boundary_kernel_defined=True,
        ),
        QiPhase.BOUNDARY_QI,
    )


def test_transportqi_with_gauge_but_no_current_variation() -> None:
    assert_phase(
        PhysicalQuantumQiState(
            delta_rel_in_K_perp=True,
            delta_rel_nonzero=True,
            string_mode_worldsheet=True,
            brane_boundary=True,
            boundary_coupling=True,
            chi_delta_rel_defined=True,
            boundary_kernel_defined=True,
            A_mu_defined=True,
            F_munu_defined=True,
            gauge_projection_defined=True,
            holonomy_or_wilson_residue_defined=True,
        ),
        QiPhase.TRANSPORT_QI,
    )


def test_transportqi_with_current_but_unclosed_ward_leak() -> None:
    state = PhysicalQuantumQiState(
        delta_rel_in_K_perp=True,
        delta_rel_nonzero=True,
        string_mode_worldsheet=True,
        brane_boundary=True,
        boundary_coupling=True,
        chi_delta_rel_defined=True,
        boundary_kernel_defined=True,
        A_mu_defined=True,
        F_munu_defined=True,
        gauge_projection_defined=True,
        holonomy_or_wilson_residue_defined=True,
        S_eff_defined=True,
        J_Qi_from_variation=True,
        current_decomposition_declared=True,
    )
    assert_phase(state, QiPhase.TRANSPORT_QI)


def test_physicalqi_without_complete_sk_fv() -> None:
    state = PhysicalQuantumQiState(
        delta_rel_in_K_perp=True,
        delta_rel_nonzero=True,
        string_mode_worldsheet=True,
        brane_boundary=True,
        boundary_coupling=True,
        chi_delta_rel_defined=True,
        boundary_kernel_defined=True,
        A_mu_defined=True,
        F_munu_defined=True,
        gauge_projection_defined=True,
        holonomy_or_wilson_residue_defined=True,
        S_eff_defined=True,
        J_Qi_from_variation=True,
        current_decomposition_declared=True,
        ward_leak=WardLeakAccounting(closed_identity_holds=True),
    )
    assert_phase(state, QiPhase.PHYSICAL_QI)


def test_fullpathqi_with_all_conditions() -> None:
    assert_phase(base_state(), QiPhase.FULL_PATH_QI)


def test_forbidden_collapse_blocks_to_nonqi() -> None:
    state = PhysicalQuantumQiState(
        delta_rel_in_K_perp=True,
        delta_rel_nonzero=True,
        K_identified_as_Qi=True,
    )
    result = classify_qi_phase(state)
    assert result.phase == QiPhase.NON_QI
    assert "K_identified_as_Qi" in result.blockers


def test_equation_packet_classifies_as_fullpathqi() -> None:
    packet_path = ROOT / "examples" / "physical_quantum_qi_equation_packet_v0_2.json"
    with packet_path.open("r", encoding="utf-8") as f:
        packet = json.load(f)
    state = state_from_packet(packet)
    result = classify_qi_phase(state)
    assert result.phase == QiPhase.FULL_PATH_QI, result


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("Physical Quantum Qi phase runtime tests passed.")
