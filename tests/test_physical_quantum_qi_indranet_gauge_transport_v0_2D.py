#!/usr/bin/env python3
"""Regression tests for Physical Quantum Qi IndraNet gauge transport v0.2D.

These tests verify that IndraNet transport remains gauge-geometric rather than
collapsing into graph-only relation claims.  They exercise the v0.2D validator
against missing A_mu, hidden curvature/path/scope drift, and scalar-only residue
summaries.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_physical_quantum_qi_indranet_gauge_transport_v0_2D import (  # noqa: E402
    load_json,
    validate_geometry,
    validate_shape,
)

BASE_PACKET = load_json(ROOT / "examples" / "physical_quantum_qi_indranet_gauge_transport_packet_v0_2D.json")


def validate_packet(packet: dict) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_shape(packet))
    errors.extend(validate_geometry(packet))
    return errors


def assert_fails_with(packet: dict, expected_substring: str) -> None:
    errors = validate_packet(packet)
    assert errors, "packet unexpectedly passed"
    joined = " | ".join(errors)
    assert expected_substring in joined, joined


def test_v02d_positive_packet_passes() -> None:
    assert validate_packet(deepcopy(BASE_PACKET)) == []


def test_missing_a_mu_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    del packet["gauge_bundle_connection"]["A_mu_declared"]
    assert_fails_with(packet, "gauge_bundle_connection missing key: A_mu_declared")


def test_graph_only_transport_not_allowed() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["validity_gate"]["graph_only_transport_rejected"] = False
    assert_fails_with(packet, "validity_gate.graph_only_transport_rejected must be true")


def test_missing_path_gamma_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    del packet["path_transport"]["path_gamma_declared"]
    assert_fails_with(packet, "path_transport missing key: path_gamma_declared")


def test_path_order_erasure_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["path_transport"]["path_ordering_declared"] = False
    assert_fails_with(packet, "path_transport.path_ordering_declared must be true")


def test_scope_drift_above_tolerance_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["scope_drift"]["scope_drift_value_or_bound_declared"] = 0.5
    packet["scope_drift"]["scope_drift_tolerance_declared"] = 0.001
    assert_fails_with(packet, "scope_drift exceeds declared tolerance")


def test_holonomy_residue_above_tolerance_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["transport_residue"]["holonomy_residue_declared"] = 0.5
    packet["holonomy_wilson_loop"]["holonomy_tolerance_declared"] = 0.001
    assert_fails_with(packet, "holonomy residue exceeds declared tolerance")


def test_component_residue_visibility_erasure_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["transport_residue"]["component_residue_visibility_declared"] = False
    assert_fails_with(packet, "transport_residue.component_residue_visibility_declared must be true")


def test_scalar_residue_weight_missing_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    del packet["transport_residue"]["scalar_residue_weights_declared_if_scalar_used"]["alpha_s"]
    assert_fails_with(packet, "transport_residue weights missing numeric alpha_s")


def test_negative_component_residue_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["transport_residue"]["scope_residue_declared"] = -0.01
    assert_fails_with(packet, "transport_residue.scope_residue_declared must be nonnegative")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("Physical Quantum Qi IndraNet gauge transport v0.2D regression tests passed.")
