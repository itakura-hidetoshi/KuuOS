#!/usr/bin/env python3
"""Tests for the Physical Quantum Qi IndraNet transport runtime adapter v0.2D."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_indranet_transport_runtime_v0_2D import (  # noqa: E402
    IndraNetTransportStatus,
    candidate_from_packet,
    evaluate_indranet_transport,
    result_to_dict,
)

PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_indranet_gauge_transport_packet_v0_2D.json"


def load_packet() -> dict:
    with PACKET_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def eval_packet(packet: dict):
    return evaluate_indranet_transport(candidate_from_packet(packet))


def test_valid_transport_candidate_routes_to_planos_and_reflectionos() -> None:
    result = eval_packet(load_packet())
    assert result.status is IndraNetTransportStatus.VALID_TRANSPORT_CANDIDATE
    assert result.valid is True
    assert "PlanOS.transport_candidate" in result.allowed_surfaces
    assert "ReflectionOS.residue_analysis_candidate" in result.allowed_surfaces
    payload = result_to_dict(result)
    assert payload["execution_authority"] is False
    assert payload["commit_authority"] is False
    assert payload["belief_root_commit_authority"] is False
    assert payload["memory_overwrite_authority"] is False
    assert payload["world_root_rewrite_authority"] is False
    assert payload["truth_authority"] is False


def test_graph_only_transport_is_rejected() -> None:
    packet = load_packet()
    packet["validity_gate"]["graph_only_transport_rejected"] = False
    result = eval_packet(packet)
    assert result.status is IndraNetTransportStatus.REJECTED_GRAPH_ONLY
    assert result.valid is False
    assert "graph_only_transport_not_rejected" in result.blockers


def test_missing_a_mu_blocks_incomplete_geometry() -> None:
    packet = load_packet()
    del packet["gauge_bundle_connection"]["A_mu_declared"]
    result = eval_packet(packet)
    assert result.status is IndraNetTransportStatus.BLOCKED_INCOMPLETE_GEOMETRY
    assert "A_mu" in result.blockers


def test_missing_path_ordering_blocks_geometry() -> None:
    packet = load_packet()
    packet["path_transport"]["path_ordering_declared"] = False
    result = eval_packet(packet)
    assert result.status is IndraNetTransportStatus.BLOCKED_INCOMPLETE_GEOMETRY
    assert "path_ordering" in result.blockers


def test_scope_drift_above_tolerance_blocks_transport() -> None:
    packet = load_packet()
    packet["scope_drift"]["scope_drift_value_or_bound_declared"] = 0.5
    packet["scope_drift"]["scope_drift_tolerance_declared"] = 0.001
    result = eval_packet(packet)
    assert result.status is IndraNetTransportStatus.BLOCKED_SCOPE_DRIFT
    assert "scope_drift_missing_or_above_tolerance" in result.blockers


def test_holonomy_residue_above_tolerance_blocks_transport() -> None:
    packet = load_packet()
    packet["transport_residue"]["holonomy_residue_declared"] = 0.5
    packet["holonomy_wilson_loop"]["holonomy_tolerance_declared"] = 0.001
    result = eval_packet(packet)
    assert result.status is IndraNetTransportStatus.BLOCKED_HOLONOMY_RESIDUE
    assert "holonomy_residue_missing_or_above_tolerance" in result.blockers


def test_hidden_component_residue_blocks_transport() -> None:
    packet = load_packet()
    packet["transport_residue"]["component_residue_visibility_declared"] = False
    result = eval_packet(packet)
    assert result.status is IndraNetTransportStatus.BLOCKED_HIDDEN_RESIDUE
    assert "component_residue_visibility_missing" in result.blockers


def test_scalar_summary_without_weights_blocks_transport() -> None:
    packet = load_packet()
    del packet["transport_residue"]["scalar_residue_weights_declared_if_scalar_used"]
    result = eval_packet(packet)
    assert result.status is IndraNetTransportStatus.BLOCKED_HIDDEN_RESIDUE
    assert "scalar_residue_weights_missing" in result.blockers


def test_authority_boundary_must_remain_false() -> None:
    packet = load_packet()
    packet["authority_boundary"]["execution_authority"] = True
    result = eval_packet(packet)
    assert result.status is IndraNetTransportStatus.BLOCKED_INCOMPLETE_GEOMETRY
    assert "authority_boundary_not_false" in result.blockers


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("Physical Quantum Qi IndraNet transport runtime v0.2D tests passed.")
