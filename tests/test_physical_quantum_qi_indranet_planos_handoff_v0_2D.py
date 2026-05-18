#!/usr/bin/env python3
"""Tests for Physical Quantum Qi IndraNet PlanOS handoff v0.2D."""

from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_indranet_planos_handoff_v0_2D import (  # noqa: E402
    build_planos_transport_handoff,
    build_and_validate_planos_transport_handoff,
    handoff_to_dict,
    validate_planos_transport_handoff,
)

PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_indranet_gauge_transport_packet_v0_2D.json"


def load_packet() -> dict:
    with PACKET_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def assert_authority_false(payload: dict) -> None:
    for key in [
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
    ]:
        assert payload[key] is False, key


def test_valid_packet_builds_planos_transport_candidate() -> None:
    payload = handoff_to_dict(build_planos_transport_handoff(load_packet()))
    assert payload["handoff_id"] == "physical_quantum_qi_indranet_planos_handoff_v0_2D"
    assert payload["source_packet_id"] == "physical_quantum_qi_indranet_gauge_transport_packet_v0_2D"
    assert payload["transport_status"] == "valid_transport_candidate"
    assert payload["accepted_by_planos"] is True
    assert payload["allowed_surface"] == "PlanOS.transport_candidate"
    assert payload["residue_surface"] == "ReflectionOS.residue_analysis_candidate"
    assert validate_planos_transport_handoff(payload) == []
    assert_authority_false(payload)


def test_blocked_packet_does_not_get_planos_acceptance() -> None:
    packet = load_packet()
    packet["validity_gate"]["graph_only_transport_rejected"] = False
    payload = handoff_to_dict(build_planos_transport_handoff(packet))
    assert payload["transport_status"] == "rejected_graph_only"
    assert payload["accepted_by_planos"] is False
    assert "graph_only_transport_not_rejected" in payload["blockers"]
    assert validate_planos_transport_handoff(payload) == []
    assert_authority_false(payload)


def test_handoff_validation_rejects_wrong_surface() -> None:
    payload = handoff_to_dict(build_planos_transport_handoff(load_packet()))
    payload["allowed_surface"] = "DecisionOS.execute"
    errors = validate_planos_transport_handoff(payload)
    assert "allowed_surface must be PlanOS.transport_candidate" in errors


def test_handoff_validation_rejects_authority_expansion() -> None:
    payload = handoff_to_dict(build_planos_transport_handoff(load_packet()))
    payload["execution_authority"] = True
    errors = validate_planos_transport_handoff(payload)
    assert "execution_authority must be false" in errors


def test_build_and_validate_returns_clean_payload() -> None:
    payload = build_and_validate_planos_transport_handoff(load_packet())
    assert "validation_errors" not in payload
    assert payload["accepted_by_planos"] is True
    assert_authority_false(payload)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("Physical Quantum Qi IndraNet PlanOS handoff v0.2D tests passed.")
