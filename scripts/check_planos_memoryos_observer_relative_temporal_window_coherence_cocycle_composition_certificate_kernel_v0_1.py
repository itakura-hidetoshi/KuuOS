#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_algebra_support_v0_1 import (
    deform_trajectory,
    temporal_window_coherence_cocycle_observables,
)
from runtime.kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_certificate_kernel_v0_1 import (
    issue_observer_relative_temporal_window_coherence_cocycle_composition_certificate,
)
from runtime.kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_certificate_support_v0_1 import (
    expected_governance_claims,
)
from runtime.kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_schema_support_v0_1 import (
    COMPONENTS,
    SCHEMA_VERSION,
    SOURCE_MEMORYOS_V041_SCHEMA_VERSION,
    SOURCE_MEMORYOS_V042_SCHEMA_VERSION,
    SOURCE_PLANOS_V123_SCHEMA_VERSION,
    compute_input_digest,
    digest_object,
    normalize_source_memoryos_v041_receipt,
    normalize_source_memoryos_v042_receipt,
    normalize_source_planos_v123_kernel_receipt,
    normalize_temporal_segments,
)

RECORD_IDS = ["record-tail", "record-window-a", "record-window-b"]
RECORD_DIGESTS = [
    "record-tail-digest",
    "record-window-a-digest",
    "record-window-b-digest",
]
OBSERVER_IDS = ["observer-alpha", "observer-beta"]
TRANSLATION_IDS = ["translation-alpha-beta"]
HISTORY_IDS = ["plan-history-a", "plan-history-b"]
PLANOS_INPUT_DIGEST = "planos-v1.23-partial-dephasing-input-digest"


def _effects(**overrides: int) -> dict[str, int]:
    values = {component: 0 for component in COMPONENTS}
    values.update(overrides)
    return values


def projection_records() -> list[dict]:
    return [
        {
            "record_id": RECORD_IDS[0],
            "record_digest": RECORD_DIGESTS[0],
            "observer_id": "observer-alpha",
            "event_digest": "event-tail-digest",
            "sequence_index": 0,
            "component_effects": _effects(holonomy=1, rollback=1, residue=2),
            "translation_residue_visible": True,
            "observation_backaction_visible": True,
        },
        {
            "record_id": RECORD_IDS[1],
            "record_digest": RECORD_DIGESTS[1],
            "observer_id": "observer-alpha",
            "event_digest": "event-window-a-digest",
            "sequence_index": 1,
            "component_effects": _effects(body=1, observation=2, residue=1),
            "translation_residue_visible": False,
            "observation_backaction_visible": True,
        },
        {
            "record_id": RECORD_IDS[2],
            "record_digest": RECORD_DIGESTS[2],
            "observer_id": "observer-beta",
            "event_digest": "event-window-b-digest",
            "sequence_index": 2,
            "component_effects": _effects(boundary=1, leak=-1, holonomy=1, residue=2),
            "translation_residue_visible": True,
            "observation_backaction_visible": True,
        },
    ]


def candidate_couplings() -> list[dict]:
    return [
        {
            "history_id": "plan-history-a",
            "base_action_numerator": 11,
            "component_couplings": {
                "body": 1,
                "boundary": 2,
                "leak": 1,
                "observation": 1,
                "holonomy": 1,
                "recovery": -1,
                "rollback": 2,
                "lockin": 1,
                "residue": 3,
            },
        },
        {
            "history_id": "plan-history-b",
            "base_action_numerator": 20,
            "component_couplings": {
                "body": 0,
                "boundary": 1,
                "leak": 2,
                "observation": 0,
                "holonomy": 1,
                "recovery": 1,
                "rollback": -1,
                "lockin": 2,
                "residue": 1,
            },
        },
    ]


def source_memoryos_v041_receipt() -> dict:
    return {
        "accepted": True,
        "schema_version": SOURCE_MEMORYOS_V041_SCHEMA_VERSION,
        "certificate_digest": "memoryos-v0.41-certificate-digest",
        "input_digest": "memoryos-v0.41-input-digest",
        "influence_handoff_digest": "memoryos-v0.41-influence-handoff-digest",
        "source_memoryos_v040_record_ledger_digest": digest_object(
            {
                "record_digests": RECORD_DIGESTS,
                "observer_ids": OBSERVER_IDS,
                "translation_ids": TRANSLATION_IDS,
            }
        ),
        "source_memoryos_v040_temporal_cycle_digest": "memoryos-v0.40-temporal-cycle-digest",
        "source_planos_v123_input_digest": PLANOS_INPUT_DIGEST,
        "retained_record_ids": RECORD_IDS,
        "retained_record_digests": RECORD_DIGESTS,
        "retained_observer_ids": OBSERVER_IDS,
        "retained_translation_ids": TRANSLATION_IDS,
        "retained_history_ids": HISTORY_IDS,
        "history_projection_records": projection_records(),
        "window_length": 2,
        "lag_weights": [3, 2],
        "candidate_couplings": candidate_couplings(),
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
        "action_denominator": 4,
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


def source_memoryos_v042_receipt() -> dict:
    source_planos = normalize_source_planos_v123_kernel_receipt(
        source_planos_v123_kernel_receipt()
    )
    conditioned = deform_trajectory(
        source_planos["partial_dephasing_trajectory"],
        phase_by_id={"plan-history-a": 2, "plan-history-b": 1},
        history_ids=HISTORY_IDS,
    )
    return {
        "accepted": True,
        "schema_version": SOURCE_MEMORYOS_V042_SCHEMA_VERSION,
        "certificate_digest": "memoryos-v0.42-certificate-digest",
        "input_digest": "memoryos-v0.42-input-digest",
        "source_memoryos_v041_certificate_digest": "memoryos-v0.41-certificate-digest",
        "source_memoryos_v041_influence_handoff_digest": "memoryos-v0.41-influence-handoff-digest",
        "source_planos_v123_input_digest": PLANOS_INPUT_DIGEST,
        "retained_history_ids": HISTORY_IDS,
        "source_kernel_digest": digest_object(
            source_planos["partial_dephasing_trajectory"]
        ),
        "conditioned_kernel_digest": digest_object(conditioned),
        "full_memory_conditioned_trajectory": conditioned,
        "all_conditioned_steps_hermitian": True,
        "all_diagonals_preserved": True,
        "all_steps_psd_by_diagonal_phase_congruence": True,
        "all_history_pair_support_retained": True,
        "amplitude_reweighting_performed": False,
        "kernel_entry_deletion_performed": False,
    }


def temporal_segments() -> list[dict]:
    return [
        {
            "segment_id": "tail-segment",
            "segment_kind": "discarded-tail",
            "record_ids": ["record-tail"],
            "observer_id": "observer-alpha",
            "lag_weight": 1,
            "source_sequence_start": 0,
            "source_sequence_end": 0,
            "translation_from_previous_id": None,
            "translation_residue_visible": True,
        },
        {
            "segment_id": "window-segment-a",
            "segment_kind": "retained-window",
            "record_ids": ["record-window-a"],
            "observer_id": "observer-alpha",
            "lag_weight": 3,
            "source_sequence_start": 1,
            "source_sequence_end": 1,
            "translation_from_previous_id": None,
            "translation_residue_visible": False,
        },
        {
            "segment_id": "window-segment-b",
            "segment_kind": "retained-window",
            "record_ids": ["record-window-b"],
            "observer_id": "observer-beta",
            "lag_weight": 2,
            "source_sequence_start": 2,
            "source_sequence_end": 2,
            "translation_from_previous_id": "translation-alpha-beta",
            "translation_residue_visible": True,
        },
    ]


def reference_input_without_claims() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v041_receipt": source_memoryos_v041_receipt(),
        "source_memoryos_v042_receipt": source_memoryos_v042_receipt(),
        "source_planos_v123_kernel_receipt": source_planos_v123_kernel_receipt(),
        "temporal_segments": temporal_segments(),
    }


def build_reference_payload() -> dict:
    payload = reference_input_without_claims()
    source_v041 = normalize_source_memoryos_v041_receipt(
        payload["source_memoryos_v041_receipt"]
    )
    source_v042 = normalize_source_memoryos_v042_receipt(
        payload["source_memoryos_v042_receipt"]
    )
    source_planos = normalize_source_planos_v123_kernel_receipt(
        payload["source_planos_v123_kernel_receipt"]
    )
    segments = normalize_temporal_segments(
        payload["temporal_segments"],
        source_record_ids=source_v041["retained_record_ids"],
        source_observer_ids=source_v041["retained_observer_ids"],
        source_translation_ids=source_v041["retained_translation_ids"],
    )
    input_digest = compute_input_digest(
        source_memoryos_v041_receipt=source_v041,
        source_memoryos_v042_receipt=source_v042,
        source_planos_v123_kernel_receipt=source_planos,
        temporal_segments=segments,
    )
    observables = temporal_window_coherence_cocycle_observables(
        source_memoryos_v041_receipt=source_v041,
        source_memoryos_v042_receipt=source_v042,
        source_planos_v123_kernel_receipt=source_planos,
        temporal_segments=segments,
        input_digest=input_digest,
    )
    payload["claims"] = {**observables, **expected_governance_claims()}
    return payload


def assert_rejects(payload: dict, blocker: str) -> None:
    result = issue_observer_relative_temporal_window_coherence_cocycle_composition_certificate(
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
    certificate = issue_observer_relative_temporal_window_coherence_cocycle_composition_certificate(
        payload
    )
    assert certificate["accepted"], certificate["blockers"]
    obs = certificate["observables"]

    assert obs["temporal_segment_ids"] == [
        "tail-segment",
        "window-segment-a",
        "window-segment-b",
    ]
    components = obs["temporal_segment_components"]
    assert components[0]["weighted_components"] == _effects(
        holonomy=1, rollback=1, residue=2
    )
    assert components[1]["weighted_components"] == _effects(
        body=3, observation=6, residue=3
    )
    assert components[2]["weighted_components"] == _effects(
        boundary=2, leak=-2, holonomy=2, residue=4
    )

    profile_a, profile_b = obs["candidate_segment_influence_profile"]
    assert [item["influence_numerator"] for item in profile_a["segments"]] == [9, 18, 16]
    assert [item["phase_mod4"] for item in profile_a["segments"]] == [1, 2, 0]
    assert [item["influence_numerator"] for item in profile_b["segments"]] == [2, 3, 4]
    assert [item["phase_mod4"] for item in profile_b["segments"]] == [2, 3, 0]
    assert [item["phase_mod4"] for item in profile_a["cumulative_phase_profile"]] == [3, 0, 2, 2]
    assert [item["phase_mod4"] for item in profile_b["cumulative_phase_profile"]] == [0, 2, 1, 1]
    assert profile_a["conditioned_action_numerator"] == 54
    assert profile_b["conditioned_action_numerator"] == 29

    stages = obs["refined_stage_trajectories"]
    source_ab_after_base = _entry(
        stages[0]["trajectory"][0], "plan-history-a", "plan-history-b"
    )
    source_ab_after_tail = _entry(
        stages[1]["trajectory"][0], "plan-history-a", "plan-history-b"
    )
    source_ab_after_window_a = _entry(
        stages[2]["trajectory"][0], "plan-history-a", "plan-history-b"
    )
    source_ab_after_window_b = _entry(
        stages[3]["trajectory"][0], "plan-history-a", "plan-history-b"
    )
    assert (source_ab_after_base["real_numerator"], source_ab_after_base["imag_numerator"]) == (-2, 0)
    assert (source_ab_after_tail["real_numerator"], source_ab_after_tail["imag_numerator"]) == (0, 2)
    assert (source_ab_after_window_a["real_numerator"], source_ab_after_window_a["imag_numerator"]) == (2, 0)
    assert (source_ab_after_window_b["real_numerator"], source_ab_after_window_b["imag_numerator"]) == (2, 0)

    assert obs["phase_neutral_segment_ids"] == ["window-segment-b"]
    assert obs["nonzero_phase_neutral_influence_visible"]
    assert obs["observer_translation_compatible"]
    assert obs["v041_candidate_influence_profile_exact"]
    assert obs["refinement_coarsening_consistent"]
    assert obs["cocycle_direct_composition_consistent"]
    assert obs["source_v042_trajectory_exact"]
    assert obs["composition_associative"]
    assert obs["all_composed_steps_hermitian"]
    assert obs["all_composed_diagonals_preserved"]
    assert obs["all_composed_steps_psd_by_diagonal_phase_congruence"]
    assert obs["all_history_pair_support_retained"]
    assert certificate["certificate_digest"]

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v042_receipt"]["source_memoryos_v041_certificate_digest"] = "substituted-digest"
    assert_rejects(tampered, "source_memoryos_v042_v041_certificate_binding_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v041_receipt"]["candidate_influence_profile"][0][
        "window_influence_numerator"
    ] = 33
    assert_rejects(tampered, "source_memoryos_v041_candidate_influence_profile_not_exact")

    tampered = copy.deepcopy(payload)
    tampered["temporal_segments"][1]["record_ids"] = ["record-window-b"]
    assert_rejects(tampered, "temporal_segment_record_coverage_or_order_invalid")

    tampered = copy.deepcopy(payload)
    tampered["temporal_segments"][1]["lag_weight"] = 2
    assert_rejects(tampered, "temporal_segment_lag_weight_binding_invalid_window-segment-a")

    tampered = copy.deepcopy(payload)
    tampered["temporal_segments"][2]["observer_id"] = "observer-alpha"
    assert_rejects(tampered, "temporal_segment_observer_binding_invalid_window-segment-b")

    tampered = copy.deepcopy(payload)
    tampered["temporal_segments"][2]["translation_from_previous_id"] = None
    assert_rejects(tampered, "observer_transition_translation_required_window-segment-b")

    tampered = copy.deepcopy(payload)
    tampered["temporal_segments"][2]["translation_residue_visible"] = False
    assert_rejects(tampered, "temporal_segment_hides_source_translation_residue_window-segment-b")

    tampered = copy.deepcopy(payload)
    source_v042 = tampered["source_memoryos_v042_receipt"]
    source_v042["full_memory_conditioned_trajectory"][0]["kernel_entries"][1][
        "real_numerator"
    ] = 999
    source_v042["conditioned_kernel_digest"] = digest_object(
        source_v042["full_memory_conditioned_trajectory"]
    )
    assert_rejects(tampered, "observable_required_source_v042_trajectory_exact")

    tampered = copy.deepcopy(payload)
    tampered["source_planos_v123_kernel_receipt"]["partial_dephasing_trajectory"][0][
        "kernel_entries"
    ][1]["imag_numerator"] = -1
    assert_rejects(tampered, "source_planos_v123_kernel_not_hermitian")

    for field in (
        "history_pruning_performed",
        "history_ranking_performed",
        "representative_history_selected",
        "plan_selection_performed",
        "decision_commit_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v041_mutated",
        "source_memoryos_v042_mutated",
        "source_planos_v123_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        tampered = copy.deepcopy(payload)
        tampered["claims"][field] = True
        assert_rejects(tampered, "claim_mismatch_" + field)

    tampered = copy.deepcopy(payload)
    tampered["claims"]["refinement_coarsening_consistent"] = False
    assert_rejects(tampered, "claim_mismatch_refinement_coarsening_consistent")

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": SCHEMA_VERSION,
                "temporal_segment_count": obs["temporal_segment_count"],
                "phase_neutral_segment_ids": obs["phase_neutral_segment_ids"],
                "refined_final_kernel_digest": obs["refined_final_kernel_digest"],
                "temporal_window_cocycle_composition_digest": obs[
                    "temporal_window_cocycle_composition_digest"
                ],
                "certificate_digest": certificate["certificate_digest"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
