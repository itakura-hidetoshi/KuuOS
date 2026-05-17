#!/usr/bin/env python3
"""Tests for Physical Quantum Qi MemoryOS record candidate v0.2."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_phase_runtime_v0_2 import QiPhase, PhaseResult, qi_phase_handoff  # noqa: E402
from physical_quantum_qi_os_bridge_v0_2 import bridge_packet_to_dict, build_qi_os_bridge_packet  # noqa: E402
from physical_quantum_qi_memory_record_v0_2 import (  # noqa: E402
    MEMORY_AUTHORITY_FALSE_KEYS,
    build_qi_memory_record_candidate,
    memory_record_to_dict,
    validate_qi_memory_record_candidate,
)


def make_bridge(phase: QiPhase):
    handoff = qi_phase_handoff(
        PhaseResult(
            phase=phase,
            reasons=["test"],
            blockers=[],
            missing_for_next_phase=[],
        )
    )
    return bridge_packet_to_dict(build_qi_os_bridge_packet(handoff))


def test_fullpathqi_builds_memory_record_candidate() -> None:
    bridge = make_bridge(QiPhase.FULL_PATH_QI)
    record = memory_record_to_dict(build_qi_memory_record_candidate(bridge))

    assert record["record_type"] == "physical_quantum_qi_memory_record_candidate_v0_2"
    assert record["source_phase"] == "FullPathQi"
    assert record["memory_surface"] == "MemoryOS.recordable_history_candidate"
    assert record["record_status"] == "append_only_candidate"
    assert record["append_only"] is True
    assert record["overwrite_forbidden"] is True
    assert record["same_root_required"] is True
    assert "MemoryOS.recordable_history_candidate" in record["observed_surfaces"]
    assert validate_qi_memory_record_candidate(record) == []


def test_memory_record_authority_never_opens() -> None:
    bridge = make_bridge(QiPhase.FULL_PATH_QI)
    record = memory_record_to_dict(build_qi_memory_record_candidate(bridge))

    for key in MEMORY_AUTHORITY_FALSE_KEYS:
        assert record["authority"][key] is False, key


def test_physicalqi_cannot_build_memory_record_candidate() -> None:
    bridge = make_bridge(QiPhase.PHYSICAL_QI)
    try:
        build_qi_memory_record_candidate(bridge)
    except ValueError as exc:
        assert "MemoryOS.recordable_history_candidate is required" in str(exc)
    else:
        raise AssertionError("PhysicalQi must not build a MemoryOS record candidate")


def test_memory_record_validator_rejects_overwrite_authority() -> None:
    bridge = make_bridge(QiPhase.FULL_PATH_QI)
    record = memory_record_to_dict(build_qi_memory_record_candidate(bridge))
    record["authority"]["memory_overwrite_authority"] = True

    errors = validate_qi_memory_record_candidate(record)
    assert "authority.memory_overwrite_authority must be false" in errors


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("Physical Quantum Qi MemoryOS record candidate tests passed.")
