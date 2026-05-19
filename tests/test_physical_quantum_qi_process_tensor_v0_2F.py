#!/usr/bin/env python3
"""Regression tests for Physical Quantum Qi Process Tensor v0.2F.

These tests protect the separation:
- Process Tensor is the multi-time non-Markov temporal structure.
- Qi is the history-bearing relational/action flow on that structure.

The tests reject Markov collapse, Qi/process-tensor identity collapse,
current-state-only prediction, erased operation history, erased observation
backaction, erased environment memory, erased temporal correlation, hidden Qi
stagnation/counterflow/deficiency pathology, and authority expansion.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from validate_physical_quantum_qi_process_tensor_v0_2F import load_json  # noqa: E402
from physical_quantum_qi_process_tensor_runtime_v0_2F import (  # noqa: E402
    build_qi_process_tensor_candidate,
    validate_qi_process_tensor_packet,
)

BASE_PACKET = load_json(ROOT / "examples" / "physical_quantum_qi_process_tensor_packet_v0_2F.json")


def assert_fails_with(packet: dict, expected_substring: str) -> None:
    errors = validate_qi_process_tensor_packet(packet)
    assert errors, "packet unexpectedly passed"
    joined = " | ".join(errors)
    assert expected_substring in joined, joined


def test_positive_qi_process_tensor_packet_passes() -> None:
    assert validate_qi_process_tensor_packet(deepcopy(BASE_PACKET)) == []


def test_candidate_payload_is_non_authoritative() -> None:
    result = build_qi_process_tensor_candidate(deepcopy(BASE_PACKET))
    assert result["valid"] is True
    assert result["candidate_payload"]["process_tensor_is_temporal_structure"] is True
    assert result["candidate_payload"]["qi_is_flow_on_temporal_structure"] is True
    assert result["candidate_payload"]["markov_reduction_allowed"] is False
    assert result["candidate_payload"]["current_state_only_prediction_allowed"] is False
    assert result["candidate_payload"]["authority_granted"] is False
    for value in result["authority_boundary"].values():
        assert value is False


def test_process_tensor_collapsed_to_markov_channel_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_reductions"]["process_tensor_collapsed_to_markov_channel"] = True
    assert_fails_with(packet, "forbidden_reductions.process_tensor_collapsed_to_markov_channel must be false")


def test_qi_identified_with_process_tensor_itself_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_reductions"]["qi_identified_with_process_tensor_itself"] = True
    assert_fails_with(packet, "forbidden_reductions.qi_identified_with_process_tensor_itself must be false")


def test_current_state_only_prediction_claimed_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_reductions"]["current_state_only_prediction_claimed"] = True
    assert_fails_with(packet, "forbidden_reductions.current_state_only_prediction_claimed must be false")


def test_operation_history_erased_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_reductions"]["operation_history_erased"] = True
    assert_fails_with(packet, "forbidden_reductions.operation_history_erased must be false")


def test_observation_backaction_erased_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_reductions"]["observation_backaction_erased"] = True
    assert_fails_with(packet, "forbidden_reductions.observation_backaction_erased must be false")


def test_environment_memory_erased_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_reductions"]["environment_memory_erased"] = True
    assert_fails_with(packet, "forbidden_reductions.environment_memory_erased must be false")


def test_temporal_correlation_erased_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_reductions"]["temporal_correlation_erased"] = True
    assert_fails_with(packet, "forbidden_reductions.temporal_correlation_erased must be false")


def test_stagnation_loop_hidden_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_reductions"]["stagnation_loop_hidden"] = True
    assert_fails_with(packet, "forbidden_reductions.stagnation_loop_hidden must be false")


def test_runaway_feedback_hidden_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_reductions"]["runaway_feedback_hidden"] = True
    assert_fails_with(packet, "forbidden_reductions.runaway_feedback_hidden must be false")


def test_coherence_loss_hidden_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_reductions"]["coherence_loss_hidden"] = True
    assert_fails_with(packet, "forbidden_reductions.coherence_loss_hidden must be false")


def test_process_tensor_not_qi_itself_required() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["process_tensor"]["process_tensor_is_temporal_structure_not_qi_itself"] = False
    assert_fails_with(packet, "process_tensor.process_tensor_is_temporal_structure_not_qi_itself must be true")


def test_qi_flow_on_process_tensor_required() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["qi_on_process_tensor"]["qi_flow_on_process_tensor_declared"] = False
    assert_fails_with(packet, "qi_on_process_tensor.qi_flow_on_process_tensor_declared must be true")


def test_operations_sequence_requires_multiple_operations() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["process_tensor"]["operations"] = packet["process_tensor"]["operations"][:1]
    assert_fails_with(packet, "process_tensor.operations must contain at least two time operations")


def test_operation_backaction_visibility_required() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["process_tensor"]["operations"][0]["backaction_visible"] = False
    assert_fails_with(packet, "process_tensor.operations[0].backaction_visible must be true")


def test_memory_link_tail_residue_visibility_required() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["process_tensor"]["memory_links"][0]["tail_residue_visible"] = False
    assert_fails_with(packet, "process_tensor.memory_links[0].tail_residue_visible must be true")


def test_authority_expansion_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["authority_boundary"]["execution_authority"] = True
    assert_fails_with(packet, "authority_boundary.execution_authority must be false")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("Physical Quantum Qi Process Tensor v0.2F regression tests passed.")
