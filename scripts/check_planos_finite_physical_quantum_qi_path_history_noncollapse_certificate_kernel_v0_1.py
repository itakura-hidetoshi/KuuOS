#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_planos_finite_physical_quantum_qi_path_history_noncollapse_algebra_support_v0_1 import (
    compile_histories,
    exact_path_history_observables,
)
from runtime.kuuos_planos_finite_physical_quantum_qi_path_history_noncollapse_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    issue_finite_physical_quantum_qi_path_history_noncollapse_certificate,
)
from runtime.kuuos_planos_finite_physical_quantum_qi_path_history_noncollapse_schema_support_v0_1 import (
    compute_path_history_input_digest,
    normalize_histories,
    normalize_states,
    normalize_transitions,
)


def _state(state_id: str, coordinate: list[int]) -> dict:
    return {
        "state_id": state_id,
        "source_digest": state_id + "-digest",
        "world_slice_digest": "world-" + state_id + "-digest",
        "qi_coordinate": coordinate,
    }


def _transition(
    transition_id: str,
    source: str,
    target: str,
    flux: list[int],
) -> dict:
    return {
        "transition_id": transition_id,
        "from_state_id": source,
        "to_state_id": target,
        "action_increment": 1,
        "qi_flux_increment": flux,
        "source_digest": transition_id + "-digest",
    }


def _history(
    history_id: str,
    scenario_id: str,
    weight: int,
    phase: int,
    transitions: list[str],
) -> dict:
    return {
        "history_id": history_id,
        "scenario_id": scenario_id,
        "weight_numerator": weight,
        "phase_mod2": phase,
        "transition_ids": transitions,
        "source_plan_digest": history_id + "-plan-digest",
    }


def reference_input_without_claims() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "source_v120_certificate_digest": "v120-certificate-digest",
        "source_path_homotopy_certificate_digest": "v114-path-homotopy-digest",
        "source_physical_quantum_qi_definition_digest": "physical-quantum-qi-v0-1-digest",
        "weight_denominator": 6,
        "qi_dimension": 2,
        "states": [
            _state("state-root", [0, 0]),
            _state("state-a", [1, 0]),
            _state("state-b", [0, 1]),
            _state("state-c", [1, 1]),
            _state("state-terminal", [2, 2]),
        ],
        "transitions": [
            _transition("transition-root-a", "state-root", "state-a", [1, 0]),
            _transition("transition-root-b", "state-root", "state-b", [0, 1]),
            _transition("transition-a-terminal", "state-a", "state-terminal", [1, 2]),
            _transition("transition-b-terminal", "state-b", "state-terminal", [2, 1]),
            _transition("transition-a-c", "state-a", "state-c", [0, 1]),
            _transition("transition-b-c", "state-b", "state-c", [1, 0]),
            _transition("transition-c-terminal", "state-c", "state-terminal", [1, 1]),
        ],
        "histories": [
            _history(
                "history-alpha-direct",
                "scenario-alpha",
                2,
                0,
                ["transition-root-a", "transition-a-terminal"],
            ),
            _history(
                "history-beta-direct",
                "scenario-beta",
                2,
                1,
                ["transition-root-b", "transition-b-terminal"],
            ),
            _history(
                "history-alpha-rejoin",
                "scenario-alpha",
                1,
                0,
                ["transition-root-a", "transition-a-c", "transition-c-terminal"],
            ),
            _history(
                "history-beta-rejoin",
                "scenario-beta",
                1,
                0,
                ["transition-root-b", "transition-b-c", "transition-c-terminal"],
            ),
        ],
    }


def build_reference_payload() -> dict:
    payload = reference_input_without_claims()
    state_errors, states = normalize_states(
        payload["states"],
        qi_dimension=2,
        maximum_state_count=64,
        maximum_absolute_qi_coordinate=10_000,
    )
    transition_errors, transitions = normalize_transitions(
        payload["transitions"],
        qi_dimension=2,
        maximum_transition_count=256,
        maximum_action_increment=10_000,
        maximum_absolute_qi_flux=10_000,
    )
    history_errors, histories = normalize_histories(
        payload["histories"],
        maximum_history_count=128,
        maximum_history_length=32,
    )
    assert not state_errors + transition_errors + history_errors
    compile_errors, compiled = compile_histories(states, transitions, histories, 2)
    assert not compile_errors
    digest = compute_path_history_input_digest(
        source_v120_certificate_digest=payload["source_v120_certificate_digest"],
        source_path_homotopy_certificate_digest=payload[
            "source_path_homotopy_certificate_digest"
        ],
        source_physical_quantum_qi_definition_digest=payload[
            "source_physical_quantum_qi_definition_digest"
        ],
        weight_denominator=6,
        qi_dimension=2,
        states=states,
        transitions=transitions,
        histories=histories,
    )
    payload["claims"] = {
        "input_digest": digest,
        **exact_path_history_observables(compiled, 6),
        "all_histories_retained": True,
        "tree_assumption_required": False,
        "argmin_performed": False,
        "representative_history_selected": False,
        "history_ranking_performed": False,
        "history_pruning_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_v120_certificate_mutated": False,
        "source_path_homotopy_certificate_mutated": False,
        "persistent_world_state_mutated": False,
    }
    return payload


def assert_rejects(payload: dict, blocker: str) -> None:
    certificate = issue_finite_physical_quantum_qi_path_history_noncollapse_certificate(
        payload
    )
    assert not certificate["accepted"]
    assert blocker in certificate["blockers"], certificate["blockers"]


def main() -> int:
    payload = build_reference_payload()
    certificate = issue_finite_physical_quantum_qi_path_history_noncollapse_certificate(
        payload
    )
    assert certificate["accepted"], certificate["blockers"]
    observables = certificate["observables"]
    assert observables["history_count"] == 4
    assert observables["distinct_state_sequence_count"] == 4
    assert observables["partition_function_polynomial"] == [
        {"action_level": 2, "weight_coefficient_numerator": 4},
        {"action_level": 3, "weight_coefficient_numerator": 2},
    ]
    endpoint = observables["endpoint_interference_profile"][0]
    assert endpoint["signed_amplitude_numerator"] == 2
    assert endpoint["phase_cancellation_numerator"] == 4
    assert endpoint["coherent_intensity_numerator_squared"] == 4
    assert endpoint["incoherent_intensity_numerator_squared"] == 10
    assert endpoint["interference_delta_numerator_squared"] == -6
    assert [
        [item["weight_numerator"] for item in marginal["state_weights"]]
        for marginal in observables["depth_state_marginals"]
    ] == [[6], [3, 3], [2, 4], [6]]
    assert [item["state_id"] for item in observables["branch_points"]] == [
        "state-a",
        "state-b",
        "state-root",
    ]
    assert [item["state_id"] for item in observables["reconvergence_points"]] == [
        "state-c",
        "state-terminal",
    ]
    assert observables["loop_history_ids"] == []
    assert certificate["noncollapse"]["all_histories_retained"]
    assert not certificate["noncollapse"]["tree_assumption_required"]

    tampered = copy.deepcopy(payload)
    tampered["histories"][0]["weight_numerator"] = 3
    assert_rejects(tampered, "history_weights_do_not_sum_to_denominator")

    tampered = copy.deepcopy(payload)
    tampered["transitions"][0]["qi_flux_increment"] = [0, 0]
    assert_rejects(tampered, "transition_qi_flux_mismatch_transition-root-a")

    tampered = copy.deepcopy(payload)
    tampered["histories"][0]["transition_ids"] = [
        "transition-root-a",
        "transition-b-terminal",
    ]
    assert_rejects(
        tampered,
        "history_adjacency_invalid_history-alpha-direct_"
        "transition-root-a_transition-b-terminal",
    )

    for field in (
        "argmin_performed",
        "representative_history_selected",
        "history_pruning_performed",
        "execution_permission",
    ):
        tampered = copy.deepcopy(payload)
        tampered["claims"][field] = True
        assert_rejects(tampered, "claim_mismatch_" + field)

    tampered = copy.deepcopy(payload)
    tampered["claims"]["retained_history_ids"] = ["history-alpha-direct"]
    assert_rejects(tampered, "claim_mismatch_retained_history_ids")

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": SCHEMA_VERSION,
                "history_count": observables["history_count"],
                "partition_function_polynomial": observables[
                    "partition_function_polynomial"
                ],
                "endpoint_interference_profile": observables[
                    "endpoint_interference_profile"
                ],
                "branch_points": observables["branch_points"],
                "reconvergence_points": observables["reconvergence_points"],
                "all_histories_retained": True,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
