#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_planos_finite_gaussian_physical_quantum_qi_homotopy_decoherence_algebra_support_v0_1 import (
    compile_histories,
    exact_gaussian_homotopy_decoherence_observables,
)
from runtime.kuuos_planos_finite_gaussian_physical_quantum_qi_homotopy_decoherence_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    issue_finite_gaussian_physical_quantum_qi_homotopy_decoherence_certificate,
)
from runtime.kuuos_planos_finite_gaussian_physical_quantum_qi_homotopy_decoherence_schema_support_v0_1 import (
    compute_gaussian_homotopy_decoherence_input_digest,
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
    homotopy_class_id: str,
    coherence_block_id: str,
    weight: int,
    phase: int,
    transitions: list[str],
) -> dict:
    return {
        "history_id": history_id,
        "scenario_id": scenario_id,
        "homotopy_class_id": homotopy_class_id,
        "coherence_block_id": coherence_block_id,
        "weight_numerator": weight,
        "phase_mod4": phase,
        "transition_ids": transitions,
        "source_plan_digest": history_id + "-plan-digest",
        "source_homotopy_witness_digest": history_id + "-homotopy-digest",
    }


def reference_input_without_claims() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "source_v121_certificate_digest": "v121-certificate-digest",
        "source_path_homotopy_certificate_digest": "v114-path-homotopy-digest",
        "source_physical_quantum_qi_definition_digest": (
            "physical-quantum-qi-v0-1-digest"
        ),
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
            _transition(
                "transition-a-terminal", "state-a", "state-terminal", [1, 2]
            ),
            _transition(
                "transition-b-terminal", "state-b", "state-terminal", [2, 1]
            ),
            _transition("transition-a-c", "state-a", "state-c", [0, 1]),
            _transition("transition-b-c", "state-b", "state-c", [1, 0]),
            _transition(
                "transition-c-terminal", "state-c", "state-terminal", [1, 1]
            ),
        ],
        "histories": [
            _history(
                "history-alpha-direct",
                "scenario-alpha",
                "homotopy-alpha",
                "block-alpha",
                2,
                0,
                ["transition-root-a", "transition-a-terminal"],
            ),
            _history(
                "history-beta-direct",
                "scenario-beta",
                "homotopy-beta",
                "block-beta",
                2,
                2,
                ["transition-root-b", "transition-b-terminal"],
            ),
            _history(
                "history-alpha-rejoin",
                "scenario-alpha",
                "homotopy-alpha",
                "block-alpha",
                1,
                1,
                ["transition-root-a", "transition-a-c", "transition-c-terminal"],
            ),
            _history(
                "history-beta-rejoin",
                "scenario-beta",
                "homotopy-beta",
                "block-beta",
                1,
                3,
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
    digest = compute_gaussian_homotopy_decoherence_input_digest(
        source_v121_certificate_digest=payload["source_v121_certificate_digest"],
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
        **exact_gaussian_homotopy_decoherence_observables(compiled, 6),
        "all_histories_retained": True,
        "z4_phase_surface_used": True,
        "gaussian_integer_arithmetic_exact": True,
        "homotopy_classes_retained": True,
        "coherence_blocks_retained": True,
        "decoherence_mask_applied_without_pruning": True,
        "argmin_performed": False,
        "representative_history_selected": False,
        "history_ranking_performed": False,
        "history_pruning_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_v121_certificate_mutated": False,
        "source_path_homotopy_certificate_mutated": False,
        "persistent_world_state_mutated": False,
    }
    return payload


def assert_rejects(payload: dict, blocker: str) -> None:
    certificate = issue_finite_gaussian_physical_quantum_qi_homotopy_decoherence_certificate(
        payload
    )
    assert not certificate["accepted"]
    assert blocker in certificate["blockers"], certificate["blockers"]


def main() -> int:
    payload = build_reference_payload()
    certificate = issue_finite_gaussian_physical_quantum_qi_homotopy_decoherence_certificate(
        payload
    )
    assert certificate["accepted"], certificate["blockers"]
    observables = certificate["observables"]
    assert observables["history_count"] == 4
    assert observables["partition_function_polynomial"] == [
        {"action_level": 2, "weight_coefficient_numerator": 4},
        {"action_level": 3, "weight_coefficient_numerator": 2},
    ]

    endpoint = observables["endpoint_gaussian_interference_profile"][0]
    assert endpoint["gaussian_amplitude_real"] == 0
    assert endpoint["gaussian_amplitude_imag"] == 0
    assert endpoint["coherent_intensity_numerator_squared"] == 0
    assert endpoint["incoherent_intensity_numerator_squared"] == 10
    assert endpoint["interference_delta_numerator_squared"] == -10
    assert endpoint["phase_support_mod4"] == [0, 1, 2, 3]

    classes = {
        item["homotopy_class_id"]: item
        for item in observables["homotopy_class_amplitude_profile"]
    }
    assert classes["homotopy-alpha"]["gaussian_amplitude_real"] == 2
    assert classes["homotopy-alpha"]["gaussian_amplitude_imag"] == 1
    assert classes["homotopy-alpha"]["coherent_intensity_numerator_squared"] == 5
    assert classes["homotopy-beta"]["gaussian_amplitude_real"] == -2
    assert classes["homotopy-beta"]["gaussian_amplitude_imag"] == -1
    assert classes["homotopy-beta"]["coherent_intensity_numerator_squared"] == 5

    decoherence = observables["decoherence_profile"][0]
    assert decoherence["pre_decoherence_coherent_intensity_numerator_squared"] == 0
    assert decoherence["post_decoherence_block_intensity_numerator_squared"] == 10
    assert decoherence["fully_incoherent_intensity_numerator_squared"] == 10
    assert decoherence["retained_within_block_interference_numerator_squared"] == 0
    assert decoherence["discarded_cross_block_interference_numerator_squared"] == -10
    assert decoherence["intensity_decomposition_exact"]

    assert [item["state_id"] for item in observables["branch_points"]] == [
        "state-a",
        "state-b",
        "state-root",
    ]
    assert [item["state_id"] for item in observables["reconvergence_points"]] == [
        "state-c",
        "state-terminal",
    ]
    assert certificate["noncollapse"]["all_histories_retained"]
    assert certificate["decoherence"]["homotopy_partition_exact"]

    tampered = copy.deepcopy(payload)
    tampered["histories"][0]["weight_numerator"] = 3
    assert_rejects(tampered, "history_weights_do_not_sum_to_denominator")

    tampered = copy.deepcopy(payload)
    tampered["histories"][0]["phase_mod4"] = 4
    assert_rejects(tampered, "history_phase_mod4_invalid_history-alpha-direct")

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

    tampered = copy.deepcopy(payload)
    tampered["histories"][2]["coherence_block_id"] = "block-alpha-split"
    assert_rejects(
        tampered,
        "homotopy_class_spans_multiple_coherence_blocks_homotopy-alpha",
    )

    tampered = copy.deepcopy(payload)
    tampered["histories"][1]["coherence_block_id"] = "block-alpha"
    assert_rejects(
        tampered,
        "coherence_block_mixes_homotopy_classes_block-alpha",
    )

    tampered = copy.deepcopy(payload)
    tampered["histories"][0]["source_homotopy_witness_digest"] = ""
    assert_rejects(
        tampered,
        "history_homotopy_witness_digest_missing_history-alpha-direct",
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
                "endpoint_gaussian_interference_profile": observables[
                    "endpoint_gaussian_interference_profile"
                ],
                "homotopy_class_amplitude_profile": observables[
                    "homotopy_class_amplitude_profile"
                ],
                "decoherence_profile": observables["decoherence_profile"],
                "all_histories_retained": True,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
