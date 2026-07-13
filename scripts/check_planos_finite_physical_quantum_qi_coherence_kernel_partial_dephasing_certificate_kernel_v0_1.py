#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_planos_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_algebra_support_v0_1 import (
    compile_histories,
    exact_partial_dephasing_observables,
)
from runtime.kuuos_planos_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    issue_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_certificate,
)
from runtime.kuuos_planos_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_schema_support_v0_1 import (
    compute_partial_dephasing_input_digest,
    normalize_dephasing_numerators,
    normalize_histories,
)


def _history(
    history_id: str,
    terminal_state_id: str,
    homotopy_class_id: str,
    coherence_block_id: str,
    weight: int,
    phase: int,
) -> dict:
    return {
        "history_id": history_id,
        "terminal_state_id": terminal_state_id,
        "homotopy_class_id": homotopy_class_id,
        "coherence_block_id": coherence_block_id,
        "weight_numerator": weight,
        "phase_mod4": phase,
        "source_v122_history_digest": history_id + "-v122-digest",
        "source_plan_digest": history_id + "-plan-digest",
        "source_homotopy_witness_digest": history_id + "-homotopy-digest",
    }


def reference_input_without_claims() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "source_v122_certificate_digest": "v122-certificate-digest",
        "source_physical_quantum_qi_definition_digest": (
            "physical-quantum-qi-v0-1-digest"
        ),
        "weight_denominator": 6,
        "dephasing_denominator": 2,
        "dephasing_numerators": [2, 1, 0],
        "histories": [
            _history(
                "history-alpha-direct",
                "state-terminal",
                "homotopy-alpha",
                "block-alpha",
                2,
                0,
            ),
            _history(
                "history-beta-direct",
                "state-terminal",
                "homotopy-beta",
                "block-beta",
                2,
                2,
            ),
            _history(
                "history-alpha-rejoin",
                "state-terminal",
                "homotopy-alpha",
                "block-alpha",
                1,
                1,
            ),
            _history(
                "history-beta-rejoin",
                "state-terminal",
                "homotopy-beta",
                "block-beta",
                1,
                3,
            ),
        ],
    }


def build_reference_payload() -> dict:
    payload = reference_input_without_claims()
    history_errors, histories = normalize_histories(
        payload["histories"],
        maximum_history_count=128,
        maximum_weight_numerator=100_000,
    )
    dephasing_errors, numerators = normalize_dephasing_numerators(
        payload["dephasing_numerators"],
        denominator=2,
        maximum_step_count=64,
    )
    assert not history_errors + dephasing_errors
    compiled = compile_histories(histories)
    digest = compute_partial_dephasing_input_digest(
        source_v122_certificate_digest=payload[
            "source_v122_certificate_digest"
        ],
        source_physical_quantum_qi_definition_digest=payload[
            "source_physical_quantum_qi_definition_digest"
        ],
        weight_denominator=6,
        dephasing_denominator=2,
        dephasing_numerators=numerators,
        histories=histories,
    )
    payload["claims"] = {
        "input_digest": digest,
        **exact_partial_dephasing_observables(
            compiled,
            dephasing_denominator=2,
            dephasing_numerators=numerators,
        ),
        "all_histories_retained": True,
        "homotopy_partition_exact": True,
        "exact_rational_partial_dephasing": True,
        "convex_gram_witness_used": True,
        "argmin_performed": False,
        "representative_history_selected": False,
        "history_ranking_performed": False,
        "history_pruning_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_v122_certificate_mutated": False,
        "persistent_world_state_mutated": False,
    }
    return payload


def assert_rejects(payload: dict, blocker: str) -> None:
    certificate = (
        issue_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_certificate(
            payload
        )
    )
    assert not certificate["accepted"]
    assert blocker in certificate["blockers"], certificate["blockers"]


def main() -> int:
    payload = build_reference_payload()
    certificate = (
        issue_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_certificate(
            payload
        )
    )
    assert certificate["accepted"], certificate["blockers"]
    observables = certificate["observables"]

    assert observables["history_count"] == 4
    assert observables["terminal_state_ids"] == ["state-terminal"]
    assert observables["homotopy_class_ids"] == [
        "homotopy-alpha",
        "homotopy-beta",
    ]
    assert observables["coherence_block_ids"] == [
        "block-alpha",
        "block-beta",
    ]
    assert observables["incoherent_mass_numerator_squared"] == 10
    assert (
        observables["endpoint_gram_hilbert_schmidt_numerator_quartic"]
        == 100
    )
    assert (
        observables["block_gram_hilbert_schmidt_numerator_quartic"]
        == 50
    )
    assert (
        observables["cross_block_hilbert_schmidt_numerator_quartic"]
        == 50
    )

    endpoint = observables["endpoint_intensity_profile"][0]
    assert endpoint["gaussian_amplitude_real"] == 0
    assert endpoint["gaussian_amplitude_imag"] == 0
    assert endpoint["fully_coherent_intensity_numerator_squared"] == 0
    assert endpoint["block_dephased_intensity_numerator_squared"] == 10
    assert endpoint["fully_incoherent_intensity_numerator_squared"] == 10

    blocks = {
        item["coherence_block_id"]: item
        for item in observables["block_amplitude_profile"]
    }
    assert blocks["block-alpha"]["gaussian_amplitude_real"] == 2
    assert blocks["block-alpha"]["gaussian_amplitude_imag"] == 1
    assert blocks["block-alpha"]["block_mass_numerator_squared"] == 5
    assert blocks["block-beta"]["gaussian_amplitude_real"] == -2
    assert blocks["block-beta"]["gaussian_amplitude_imag"] == -1
    assert blocks["block-beta"]["block_mass_numerator_squared"] == 5

    trajectory = {
        item["dephasing_numerator"]: item
        for item in observables["partial_dephasing_trajectory"]
    }
    assert trajectory[2]["trace_numerator"] == 20
    assert trajectory[2]["purity_numerator"] == 400
    assert trajectory[2]["purity_reduced"] == {
        "numerator": 1,
        "denominator": 1,
    }
    assert trajectory[2]["quadratic_mixedness_numerator"] == 0
    assert (
        trajectory[2][
            "cross_block_coherence_hilbert_schmidt_numerator_quartic"
        ]
        == 200
    )
    assert trajectory[2]["readout_intensity_numerator"] == 0

    assert trajectory[1]["purity_numerator"] == 250
    assert trajectory[1]["purity_reduced"] == {
        "numerator": 5,
        "denominator": 8,
    }
    assert trajectory[1]["quadratic_mixedness_numerator"] == 150
    assert trajectory[1]["quadratic_mixedness_reduced"] == {
        "numerator": 3,
        "denominator": 8,
    }
    assert (
        trajectory[1][
            "cross_block_coherence_hilbert_schmidt_numerator_quartic"
        ]
        == 50
    )
    assert trajectory[1]["readout_intensity_numerator"] == 10

    assert trajectory[0]["purity_numerator"] == 200
    assert trajectory[0]["purity_reduced"] == {
        "numerator": 1,
        "denominator": 2,
    }
    assert trajectory[0]["quadratic_mixedness_numerator"] == 200
    assert trajectory[0]["quadratic_mixedness_reduced"] == {
        "numerator": 1,
        "denominator": 2,
    }
    assert (
        trajectory[0][
            "cross_block_coherence_hilbert_schmidt_numerator_quartic"
        ]
        == 0
    )
    assert trajectory[0]["readout_intensity_numerator"] == 20

    assert all(
        item["kernel_hermitian"]
        and item["positive_semidefinite_by_convex_gram_construction"]
        for item in trajectory.values()
    )
    assert observables["trajectory_trace_preserved"]
    assert observables["trajectory_cross_coherence_nonincreasing"]
    assert observables["trajectory_purity_nonincreasing"]
    assert observables["trajectory_mixedness_nondecreasing"]
    assert certificate["noncollapse"]["all_histories_retained"]
    assert certificate["partial_dephasing"]["homotopy_partition_exact"]

    tampered = copy.deepcopy(payload)
    tampered["histories"][0]["weight_numerator"] = 3
    assert_rejects(tampered, "history_weights_do_not_sum_to_denominator")

    tampered = copy.deepcopy(payload)
    tampered["histories"][0]["phase_mod4"] = 4
    assert_rejects(
        tampered,
        "history_phase_mod4_invalid_history-alpha-direct",
    )

    tampered = copy.deepcopy(payload)
    tampered["dephasing_numerators"] = [1, 0]
    assert_rejects(
        tampered,
        "dephasing_sequence_must_start_fully_coherent",
    )

    tampered = copy.deepcopy(payload)
    tampered["dephasing_numerators"] = [2, 1, 1, 0]
    assert_rejects(
        tampered,
        "dephasing_numerators_must_strictly_decrease",
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
    tampered["histories"][0]["source_v122_history_digest"] = ""
    assert_rejects(
        tampered,
        "source_v122_history_digest_missing_history-alpha-direct",
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
    tampered["claims"]["partial_dephasing_trajectory"][1][
        "purity_numerator"
    ] = 251
    assert_rejects(
        tampered,
        "claim_mismatch_partial_dephasing_trajectory",
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": SCHEMA_VERSION,
                "history_count": observables["history_count"],
                "endpoint_intensity_profile": observables[
                    "endpoint_intensity_profile"
                ],
                "block_amplitude_profile": observables[
                    "block_amplitude_profile"
                ],
                "partial_dephasing_trajectory_summary": [
                    {
                        key: item[key]
                        for key in (
                            "dephasing_numerator",
                            "dephasing_denominator",
                            "trace_numerator",
                            "purity_numerator",
                            "purity_reduced",
                            "quadratic_mixedness_numerator",
                            "quadratic_mixedness_reduced",
                            "cross_block_coherence_hilbert_schmidt_numerator_quartic",
                            "readout_intensity_numerator",
                            "readout_intensity_denominator",
                        )
                    }
                    for item in observables["partial_dephasing_trajectory"]
                ],
                "all_histories_retained": True,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
