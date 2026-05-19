#!/usr/bin/env python3
"""Regression tests for KuuOS Qi Process Tensor Conventional Autonomy v0.2G.

These tests protect the design decision that Qi Process Tensor can be a
conventional-truth temporal substrate for autonomous AI without becoming
ultimate truth, fixed ontology, execution authority, or ungated agent loop.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_kuuos_qi_process_tensor_conventional_autonomy_v0_2G import (  # noqa: E402
    load_json,
    validate_packet,
)

BASE_PACKET = load_json(ROOT / "examples" / "kuuos_qi_process_tensor_conventional_autonomy_packet_v0_2G.json")


def assert_fails_with(packet: dict, expected_substring: str) -> None:
    errors = validate_packet(packet)
    assert errors, "packet unexpectedly passed"
    joined = " | ".join(errors)
    assert expected_substring in joined, joined


def test_positive_conventional_autonomy_packet_passes() -> None:
    assert validate_packet(deepcopy(BASE_PACKET)) == []


def test_conventional_substrate_as_ultimate_truth_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["conventional_truth_substrate_claimed_as_ultimate_truth"] = True
    assert_fails_with(packet, "forbidden_collapses.conventional_truth_substrate_claimed_as_ultimate_truth must be false")


def test_process_tensor_reified_as_fixed_ontology_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["process_tensor_reified_as_fixed_ontology"] = True
    assert_fails_with(packet, "forbidden_collapses.process_tensor_reified_as_fixed_ontology must be false")


def test_qi_process_tensor_execution_authority_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["qi_process_tensor_grants_execution_authority"] = True
    assert_fails_with(packet, "forbidden_collapses.qi_process_tensor_grants_execution_authority must be false")


def test_state_snapshot_replaces_process_history_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["state_snapshot_replaces_process_history"] = True
    assert_fails_with(packet, "forbidden_collapses.state_snapshot_replaces_process_history must be false")


def test_reward_loop_replaces_recoverability_gate_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["reward_loop_replaces_recoverability_gate"] = True
    assert_fails_with(packet, "forbidden_collapses.reward_loop_replaces_recoverability_gate must be false")


def test_agent_loop_skips_decision_gate_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["agent_loop_skips_decision_gate"] = True
    assert_fails_with(packet, "forbidden_collapses.agent_loop_skips_decision_gate must be false")


def test_observation_backaction_erased_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["observation_backaction_erased"] = True
    assert_fails_with(packet, "forbidden_collapses.observation_backaction_erased must be false")


def test_environment_memory_erased_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["environment_memory_erased"] = True
    assert_fails_with(packet, "forbidden_collapses.environment_memory_erased must be false")


def test_temporal_correlation_erased_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["temporal_correlation_erased"] = True
    assert_fails_with(packet, "forbidden_collapses.temporal_correlation_erased must be false")


def test_residue_hidden_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["residue_hidden"] = True
    assert_fails_with(packet, "forbidden_collapses.residue_hidden must be false")


def test_reflection_result_claimed_as_truth_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["reflection_result_claimed_as_truth"] = True
    assert_fails_with(packet, "forbidden_collapses.reflection_result_claimed_as_truth must be false")


def test_memory_candidate_claimed_as_source_history_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["memory_candidate_claimed_as_source_history"] = True
    assert_fails_with(packet, "forbidden_collapses.memory_candidate_claimed_as_source_history must be false")


def test_plan_candidate_claimed_as_execution_license_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["forbidden_collapses"]["plan_candidate_claimed_as_execution_license"] = True
    assert_fails_with(packet, "forbidden_collapses.plan_candidate_claimed_as_execution_license must be false")


def test_two_truth_non_reification_required() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["two_truths_placement"]["qi_process_tensor_not_ultimate_truth"] = False
    assert_fails_with(packet, "two_truths_placement.qi_process_tensor_not_ultimate_truth must be true")


def test_state_snapshot_replacement_forbidden_required() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["conventional_temporal_substrate"]["state_snapshot_replacement_forbidden"] = False
    assert_fails_with(packet, "conventional_temporal_substrate.state_snapshot_replacement_forbidden must be true")


def test_gate_declared_required() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["autonomous_loop"]["gate_declared"] = False
    assert_fails_with(packet, "autonomous_loop.gate_declared must be true")


def test_execution_requires_gate_license_required() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["autonomous_loop"]["execution_requires_gate_license"] = False
    assert_fails_with(packet, "autonomous_loop.execution_requires_gate_license must be true")


def test_decision_gate_required() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["safety_gates"]["DecisionOS_safety_gate_required"] = False
    assert_fails_with(packet, "safety_gates.DecisionOS_safety_gate_required must be true")


def test_qi_flow_cannot_skip_gate_required() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["safety_gates"]["no_gate_may_be_skipped_by_qi_flow_claim"] = False
    assert_fails_with(packet, "safety_gates.no_gate_may_be_skipped_by_qi_flow_claim must be true")


def test_authority_expansion_fails() -> None:
    packet = deepcopy(BASE_PACKET)
    packet["authority_boundary"]["execution_authority"] = True
    assert_fails_with(packet, "authority_boundary.execution_authority must be false")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("KuuOS Qi Process Tensor Conventional Autonomy v0.2G regression tests passed.")
