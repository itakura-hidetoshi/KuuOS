#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_algebra_support_v0_1 import (
    influence_conditioned_coherence_observables,
)
from runtime.kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate_kernel_v0_1 import (
    issue_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate,
)
from runtime.kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate_support_v0_1 import (
    expected_governance_claims,
)
from runtime.kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_schema_support_v0_1 import (
    SCHEMA_VERSION,
    SOURCE_MEMORYOS_V041_SCHEMA_VERSION,
    SOURCE_PLANOS_V123_SCHEMA_VERSION,
    compute_input_digest,
    normalize_source_memoryos_v041_receipt,
    normalize_source_planos_v123_kernel_receipt,
)

HISTORY_IDS = ["plan-history-a", "plan-history-b"]
PLANOS_INPUT_DIGEST = "planos-v1.23-partial-dephasing-input-digest"


def source_memoryos_v041_receipt() -> dict:
    return {
        "accepted": True,
        "schema_version": SOURCE_MEMORYOS_V041_SCHEMA_VERSION,
        "certificate_digest": "memoryos-v0.41-certificate-digest",
        "input_digest": "memoryos-v0.41-input-digest",
        "influence_handoff_digest": "memoryos-v0.41-influence-handoff-digest",
        "source_planos_v123_input_digest": PLANOS_INPUT_DIGEST,
        "retained_history_ids": HISTORY_IDS,
        "candidate_influence_profile": [
            {
                "history_id": "plan-history-a",
                "base_action_numerator": 11,
                "window_influence_numerator": 34,
                "tail_influence_numerator": 9,
                "total_history_influence_numerator": 43,
                "conditioned_action_numerator": 54,
                "window_only_action_numerator": 45,
                "action_denominator": 4,
                "support_retained": True,
            },
            {
                "history_id": "plan-history-b",
                "base_action_numerator": 20,
                "window_influence_numerator": 7,
                "tail_influence_numerator": 2,
                "total_history_influence_numerator": 9,
                "conditioned_action_numerator": 29,
                "window_only_action_numerator": 27,
                "action_denominator": 4,
                "support_retained": True,
            },
        ],
        "all_planos_histories_retained": True,
        "history_pruning_performed": False,
        "history_ranking_performed": False,
        "representative_history_selected": False,
        "plan_selection_performed": False,
        "activation_performed": False,
        "execution_permission": False,
    }


def _kernel_entries(cross_scale: int) -> list[dict]:
    return [
        {
            "row_history_id": "plan-history-a",
            "column_history_id": "plan-history-a",
            "real_numerator": 2,
            "imag_numerator": 0,
        },
        {
            "row_history_id": "plan-history-a",
            "column_history_id": "plan-history-b",
            "real_numerator": 0,
            "imag_numerator": -cross_scale,
        },
        {
            "row_history_id": "plan-history-b",
            "column_history_id": "plan-history-a",
            "real_numerator": 0,
            "imag_numerator": cross_scale,
        },
        {
            "row_history_id": "plan-history-b",
            "column_history_id": "plan-history-b",
            "real_numerator": 2,
            "imag_numerator": 0,
        },
    ]


def source_planos_v123_kernel_receipt() -> dict:
    return {
        "accepted": True,
        "schema_version": SOURCE_PLANOS_V123_SCHEMA_VERSION,
        "input_digest": PLANOS_INPUT_DIGEST,
        "retained_history_ids": HISTORY_IDS,
        "dephasing_denominator": 2,
        "dephasing_numerators": [2, 1, 0],
        "partial_dephasing_trajectory": [
            {
                "dephasing_numerator": numerator,
                "kernel_entry_denominator": 2,
                "kernel_hermitian": True,
                "positive_semidefinite_by_convex_gram_construction": True,
                "kernel_entries": _kernel_entries(numerator),
            }
            for numerator in [2, 1, 0]
        ],
        "all_histories_retained": True,
        "history_pruning_performed": False,
        "history_ranking_performed": False,
        "representative_history_selected": False,
    }


def reference_input_without_claims() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v041_receipt": source_memoryos_v041_receipt(),
        "source_planos_v123_kernel_receipt": source_planos_v123_kernel_receipt(),
    }


def build_reference_payload() -> dict:
    payload = reference_input_without_claims()
    source_memory = normalize_source_memoryos_v041_receipt(
        payload["source_memoryos_v041_receipt"]
    )
    source_planos = normalize_source_planos_v123_kernel_receipt(
        payload["source_planos_v123_kernel_receipt"]
    )
    input_digest = compute_input_digest(
        source_memoryos_v041_receipt=source_memory,
        source_planos_v123_kernel_receipt=source_planos,
    )
    observables = influence_conditioned_coherence_observables(
        source_memoryos_v041_receipt=source_memory,
        source_planos_v123_kernel_receipt=source_planos,
        input_digest=input_digest,
    )
    payload["claims"] = {**observables, **expected_governance_claims()}
    return payload


def assert_rejects(payload: dict, blocker: str) -> None:
    result = issue_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def _entry(step: dict, row_id: str, column_id: str) -> dict:
    return next(
        item
        for item in step["kernel_entries"]
        if item["row_history_id"] == row_id
        and item["column_history_id"] == column_id
    )


def main() -> int:
    payload = build_reference_payload()
    certificate = issue_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate(
        payload
    )
    assert certificate["accepted"], certificate["blockers"]
    obs = certificate["observables"]

    assert obs["retained_history_ids"] == HISTORY_IDS
    phase_a, phase_b = obs["memory_phase_profile"]
    assert phase_a["conditioned_phase_mod4"] == 2
    assert phase_a["window_only_phase_mod4"] == 1
    assert phase_a["tail_phase_shift_mod4"] == 1
    assert phase_b["conditioned_phase_mod4"] == 1
    assert phase_b["window_only_phase_mod4"] == 3
    assert phase_b["tail_phase_shift_mod4"] == 2

    full_step_2 = obs["full_memory_conditioned_trajectory"][0]
    window_step_2 = obs["window_only_conditioned_trajectory"][0]
    full_ab = _entry(full_step_2, "plan-history-a", "plan-history-b")
    window_ab = _entry(window_step_2, "plan-history-a", "plan-history-b")
    assert (full_ab["real_numerator"], full_ab["imag_numerator"]) == (2, 0)
    assert (window_ab["real_numerator"], window_ab["imag_numerator"]) == (0, 2)
    assert _entry(full_step_2, "plan-history-a", "plan-history-a")[
        "real_numerator"
    ] == 2

    assert obs["tail_sensitive_kernel_entry_count"] == 4
    assert obs["tail_sensitive_dephasing_numerators"] == [2, 1]
    assert obs["discarded_tail_changes_coherence_kernel"]
    assert obs["all_conditioned_steps_hermitian"]
    assert obs["all_window_only_steps_hermitian"]
    assert obs["all_diagonals_preserved"]
    assert obs["all_steps_psd_by_diagonal_phase_congruence"]
    assert obs["all_history_pair_support_retained"]
    assert not obs["amplitude_reweighting_performed"]
    assert not obs["kernel_entry_deletion_performed"]
    assert certificate["certificate_digest"]

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v041_receipt"]["source_planos_v123_input_digest"] = "substituted"
    assert_rejects(tampered, "source_planos_v123_input_digest_binding_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v041_receipt"]["retained_history_ids"][0] = "substituted"
    assert_rejects(tampered, "source_memoryos_v041_candidate_profile_support_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v041_receipt"]["candidate_influence_profile"][0][
        "conditioned_action_numerator"
    ] = 53
    assert_rejects(
        tampered,
        "source_memoryos_v041_conditioned_action_identity_invalid_plan-history-a",
    )

    tampered = copy.deepcopy(payload)
    tampered["source_planos_v123_kernel_receipt"]["partial_dephasing_trajectory"][0][
        "kernel_entries"
    ][1]["imag_numerator"] = -1
    assert_rejects(
        tampered,
        "source_planos_v123_kernel_not_hermitian_0_plan-history-a_plan-history-b",
    )

    tampered = copy.deepcopy(payload)
    tampered["source_planos_v123_kernel_receipt"]["partial_dephasing_trajectory"][0][
        "kernel_entries"
    ].pop()
    assert_rejects(tampered, "source_planos_v123_kernel_support_count_invalid_0")

    tampered = copy.deepcopy(payload)
    tampered["source_planos_v123_kernel_receipt"]["partial_dephasing_trajectory"][1][
        "positive_semidefinite_by_convex_gram_construction"
    ] = False
    assert_rejects(tampered, "source_planos_v123_psd_witness_required_1")

    for field in (
        "history_pruning_performed",
        "history_ranking_performed",
        "representative_history_selected",
        "plan_selection_performed",
        "decision_commit_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v041_mutated",
        "source_planos_v123_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        tampered = copy.deepcopy(payload)
        tampered["claims"][field] = True
        assert_rejects(tampered, "claim_mismatch_" + field)

    tampered = copy.deepcopy(payload)
    tampered["claims"]["full_memory_conditioned_trajectory"][0]["kernel_entries"][1][
        "real_numerator"
    ] = 999
    assert_rejects(tampered, "claim_mismatch_full_memory_conditioned_trajectory")

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": SCHEMA_VERSION,
                "history_count": obs["history_count"],
                "tail_sensitive_kernel_entry_count": obs[
                    "tail_sensitive_kernel_entry_count"
                ],
                "tail_sensitive_dephasing_numerators": obs[
                    "tail_sensitive_dephasing_numerators"
                ],
                "conditioned_kernel_digest": obs["conditioned_kernel_digest"],
                "certificate_digest": certificate["certificate_digest"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
