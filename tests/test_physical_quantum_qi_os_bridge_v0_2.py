#!/usr/bin/env python3
"""Tests for Physical Quantum Qi -> KuuOS OS bridge packet v0.2."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_phase_runtime_v0_2 import (  # noqa: E402
    QiPhase,
    PhaseResult,
    qi_phase_handoff,
)
from physical_quantum_qi_os_bridge_v0_2 import (  # noqa: E402
    AUTHORITY_FALSE_KEYS,
    bridge_packet_to_dict,
    build_qi_os_bridge_packet,
    validate_qi_os_bridge_packet,
)


def make_handoff(phase: QiPhase):
    return qi_phase_handoff(
        PhaseResult(
            phase=phase,
            reasons=["test"],
            blockers=[],
            missing_for_next_phase=[],
        )
    )


def test_fullpathqi_bridge_exposes_candidate_payloads() -> None:
    packet = build_qi_os_bridge_packet(make_handoff(QiPhase.FULL_PATH_QI))
    data = bridge_packet_to_dict(packet)

    assert data["phase"] == "FullPathQi"
    assert data["handoff_status"] == "memory_recordable_reflection_analyzable_candidate"

    payloads = data["os_payloads"]
    assert payloads["BeliefOS"]["observation_candidate"] is True
    assert payloads["PlanOS"]["transport_candidate"] is True
    assert payloads["DecisionOS"]["safety_evaluable_candidate"] is True
    assert payloads["MemoryOS"]["recordable_history_candidate"] is True
    assert payloads["ReflectionOS"]["residue_analysis_candidate"] is True

    assert validate_qi_os_bridge_packet(data) == []


def test_bridge_authority_never_opens() -> None:
    packet = build_qi_os_bridge_packet(make_handoff(QiPhase.FULL_PATH_QI))
    data = bridge_packet_to_dict(packet)

    for key in AUTHORITY_FALSE_KEYS:
        assert data["authority"][key] is False, key

    for os_name, payload in data["os_payloads"].items():
        for key in [
            "execution_authority",
            "belief_root_commit_authority",
            "memory_overwrite_authority",
            "world_root_rewrite_authority",
            "safety_override_authority",
        ]:
            if key in payload:
                assert payload[key] is False, f"{os_name}.{key} must be false"


def test_physicalqi_bridge_stops_before_memory_and_reflection() -> None:
    packet = build_qi_os_bridge_packet(make_handoff(QiPhase.PHYSICAL_QI))
    data = bridge_packet_to_dict(packet)
    payloads = data["os_payloads"]

    assert payloads["DecisionOS"]["safety_evaluable_candidate"] is True
    assert payloads["MemoryOS"]["recordable_history_candidate"] is False
    assert payloads["ReflectionOS"]["residue_analysis_candidate"] is False
    assert validate_qi_os_bridge_packet(data) == []


def test_nonqi_bridge_has_blocker_and_no_os_candidate() -> None:
    handoff = make_handoff(QiPhase.NON_QI)
    packet = build_qi_os_bridge_packet(handoff)
    data = bridge_packet_to_dict(packet)

    assert data["phase"] == "NonQi"
    assert data["allowed_surfaces"] == []
    assert "not_a_constructive_Qi_phase" in data["blockers"]
    assert all(payload["status"] == "inactive" for payload in data["os_payloads"].values())
    assert validate_qi_os_bridge_packet(data) == []


def test_validator_rejects_authority_escalation() -> None:
    packet = build_qi_os_bridge_packet(make_handoff(QiPhase.FULL_PATH_QI))
    data = bridge_packet_to_dict(packet)
    data["authority"]["execution_authority"] = True

    errors = validate_qi_os_bridge_packet(data)
    assert "authority.execution_authority must be false" in errors


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("Physical Quantum Qi OS bridge tests passed.")
