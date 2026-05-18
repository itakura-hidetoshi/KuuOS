#!/usr/bin/env python3
"""Regression tests for Physical Quantum Qi non-Markov memory v0.2E.

These tests protect the v0.2E design decision that Qi memory is primary
non-Markovian semantics.  Markov reduction, current-state-only judgment,
finite-window tail erasure, holonomy erasure, rollback erasure, compression as
deletion, and authority expansion must fail.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_physical_quantum_qi_non_markov_memory_v0_2E import (  # noqa: E402
    load_json,
    validate_packet,
)

BASE_PACKET = load_json(ROOT / "examples" / "physical_quantum_qi_non_markov_memory_packet_v0_2E.json")


def assert_fails_with(packet: dict, expected_substring: str) -> None:
    errors = validate_packet(packet)
    assert errors, "packet unexpectedly passed"
    joined = " | ".join(errors)
    assert expected_substring in joined, joined


def test_positive_non_markov_memory_packet_passes() -> None:
    assert validate_packet(deepcopy(BASE_PACKET)) == []


def test_markov_reduction_as_semantics_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["memory_semantics"]["markov_reduction_forbidden_as_qi_semantics"] = False
    assert_fails_with(packet, "memory_semantics.markov_reduction_forbidden_as_qi_semantics must be true")


def test_current_state_only_identity_not_allowed() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["memory_semantics"]["current_state_only_identity_forbidden"] = False
    assert_fails_with(packet, "memory_semantics.current_state_only_identity_forbidden must be true")


def test_current_state_only_recoverability_not_allowed() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["memory_semantics"]["current_state_only_recoverability_forbidden"] = False
    assert_fails_with(packet, "memory_semantics.current_state_only_recoverability_forbidden must be true")


def test_current_state_only_transport_safety_not_allowed() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["memory_semantics"]["current_state_only_transport_safety_forbidden"] = False
    assert_fails_with(packet, "memory_semantics.current_state_only_transport_safety_forbidden must be true")


def test_missing_holonomy_history_kernel_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["memory_kernel"]["K_holonomy"]["declared"] = False
    assert_fails_with(packet, "memory_kernel.K_holonomy.declared must be true")


def test_missing_rollback_history_kernel_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["memory_kernel"]["K_rollback"]["declared"] = False
    assert_fails_with(packet, "memory_kernel.K_rollback.declared must be true")


def test_finite_window_as_markov_substitute_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["finite_window_projection"]["markov_semantic_substitute"] = True
    assert_fails_with(packet, "finite_window_projection.markov_semantic_substitute must be false")


def test_discarded_tail_residue_hidden_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["finite_window_projection"]["discarded_tail_residue_declared"] = False
    assert_fails_with(packet, "finite_window_projection.discarded_tail_residue_declared must be true")


def test_holonomy_tail_residue_hidden_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["finite_window_projection"]["holonomy_tail_residue_declared"] = False
    assert_fails_with(packet, "finite_window_projection.holonomy_tail_residue_declared must be true")


def test_boundary_leak_tail_residue_hidden_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["finite_window_projection"]["boundary_leak_tail_residue_declared"] = False
    assert_fails_with(packet, "finite_window_projection.boundary_leak_tail_residue_declared must be true")


def test_recovery_tail_debt_hidden_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["finite_window_projection"]["recovery_tail_debt_declared"] = False
    assert_fails_with(packet, "finite_window_projection.recovery_tail_debt_declared must be true")


def test_rollback_tail_debt_hidden_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["finite_window_projection"]["rollback_tail_debt_declared"] = False
    assert_fails_with(packet, "finite_window_projection.rollback_tail_debt_declared must be true")


def test_positive_local_recovery_erasing_debt_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["non_markov_recoverability"]["positive_local_recovery_does_not_erase_recovery_debt"] = False
    assert_fails_with(packet, "non_markov_recoverability.positive_local_recovery_does_not_erase_recovery_debt must be true")


def test_fresh_valid_path_erasing_holonomy_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["non_markov_transport"]["fresh_valid_path_cannot_erase_prior_holonomy_history"] = False
    assert_fails_with(packet, "non_markov_transport.fresh_valid_path_cannot_erase_prior_holonomy_history must be true")


def test_compression_as_deletion_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["compression_rule"]["compression_is_not_deletion"] = False
    assert_fails_with(packet, "compression_rule.compression_is_not_deletion must be true")


def test_compressed_memory_replacing_source_history_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["compression_rule"]["compressed_memory_cannot_replace_source_history"] = False
    assert_fails_with(packet, "compression_rule.compressed_memory_cannot_replace_source_history must be true")


def test_authority_expansion_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["authority_boundary"]["execution_authority"] = True
    assert_fails_with(packet, "authority_boundary.execution_authority must be false")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("Physical Quantum Qi non-Markov memory v0.2E regression tests passed.")
