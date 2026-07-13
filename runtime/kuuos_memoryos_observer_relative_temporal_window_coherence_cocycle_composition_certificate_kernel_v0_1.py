from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_algebra_support_v0_1 import (
    recompute_v041_candidate_profile,
    temporal_window_coherence_cocycle_observables,
)
from runtime.kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_certificate_support_v0_1 import (
    expected_governance_claims,
)
from runtime.kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_schema_support_v0_1 import (
    SCHEMA_VERSION,
    compute_input_digest,
    digest_object,
    normalize_source_memoryos_v041_receipt,
    normalize_source_memoryos_v042_receipt,
    normalize_source_planos_v123_kernel_receipt,
    normalize_temporal_segments,
)


def _kernel_trajectory_is_hermitian(
    trajectory: list[dict[str, Any]], history_ids: list[str]
) -> bool:
    for step in trajectory:
        by_pair = {
            (entry["row_history_id"], entry["column_history_id"]): entry
            for entry in step["kernel_entries"]
        }
        for row_id in history_ids:
            for column_id in history_ids:
                left = by_pair[(row_id, column_id)]
                right = by_pair[(column_id, row_id)]
                if left["real_numerator"] != right["real_numerator"]:
                    return False
                if left["imag_numerator"] != -right["imag_numerator"]:
                    return False
    return True


def _append_source_boundary_blockers(
    blockers: list[str],
    source_memoryos_v041: dict[str, Any],
    source_memoryos_v042: dict[str, Any],
    source_planos_v123: dict[str, Any],
) -> None:
    if not source_memoryos_v041["all_planos_histories_retained"]:
        blockers.append("source_memoryos_v041_history_support_not_retained")
    for field in (
        "history_pruning_performed",
        "history_ranking_performed",
        "representative_history_selected",
        "plan_selection_performed",
        "activation_performed",
        "execution_permission",
    ):
        if source_memoryos_v041[field]:
            blockers.append("source_memoryos_v041_forbidden_" + field)
    if not source_planos_v123["all_histories_retained"]:
        blockers.append("source_planos_v123_history_support_not_retained")
    for field in (
        "history_pruning_performed",
        "history_ranking_performed",
        "representative_history_selected",
    ):
        if source_planos_v123[field]:
            blockers.append("source_planos_v123_forbidden_" + field)
    for field in (
        "all_conditioned_steps_hermitian",
        "all_diagonals_preserved",
        "all_steps_psd_by_diagonal_phase_congruence",
        "all_history_pair_support_retained",
    ):
        if not source_memoryos_v042[field]:
            blockers.append("source_memoryos_v042_required_" + field)
    for field in (
        "amplitude_reweighting_performed",
        "kernel_entry_deletion_performed",
    ):
        if source_memoryos_v042[field]:
            blockers.append("source_memoryos_v042_forbidden_" + field)


def _append_binding_blockers(
    blockers: list[str],
    source_memoryos_v041: dict[str, Any],
    source_memoryos_v042: dict[str, Any],
    source_planos_v123: dict[str, Any],
) -> None:
    if (
        source_memoryos_v041["source_planos_v123_input_digest"]
        != source_planos_v123["input_digest"]
    ):
        blockers.append("source_memoryos_v041_planos_input_digest_binding_mismatch")
    if (
        source_memoryos_v042["source_planos_v123_input_digest"]
        != source_planos_v123["input_digest"]
    ):
        blockers.append("source_memoryos_v042_planos_input_digest_binding_mismatch")
    if (
        source_memoryos_v042["source_memoryos_v041_certificate_digest"]
        != source_memoryos_v041["certificate_digest"]
    ):
        blockers.append("source_memoryos_v042_v041_certificate_binding_mismatch")
    if (
        source_memoryos_v042["source_memoryos_v041_influence_handoff_digest"]
        != source_memoryos_v041["influence_handoff_digest"]
    ):
        blockers.append("source_memoryos_v042_v041_handoff_binding_mismatch")
    histories = source_planos_v123["retained_history_ids"]
    if source_memoryos_v041["retained_history_ids"] != histories:
        blockers.append("source_memoryos_v041_history_support_mismatch")
    if source_memoryos_v042["retained_history_ids"] != histories:
        blockers.append("source_memoryos_v042_history_support_mismatch")
    source_kernel_digest = digest_object(
        source_planos_v123["partial_dephasing_trajectory"]
    )
    if source_memoryos_v042["source_kernel_digest"] != source_kernel_digest:
        blockers.append("source_memoryos_v042_source_kernel_digest_mismatch")
    if not _kernel_trajectory_is_hermitian(
        source_planos_v123["partial_dephasing_trajectory"], histories
    ):
        blockers.append("source_planos_v123_kernel_not_hermitian")
    if not all(
        step["kernel_hermitian"]
        and step["positive_semidefinite_by_diagonal_phase_congruence"]
        for step in source_planos_v123["partial_dephasing_trajectory"]
    ):
        blockers.append("source_planos_v123_kernel_witness_invalid")


def _append_v041_arithmetic_blockers(
    blockers: list[str], source_memoryos_v041: dict[str, Any]
) -> None:
    recomputed = recompute_v041_candidate_profile(source_memoryos_v041)
    if recomputed != source_memoryos_v041["candidate_influence_profile"]:
        blockers.append("source_memoryos_v041_candidate_influence_profile_not_exact")
    for item in source_memoryos_v041["candidate_influence_profile"]:
        history_id = item["history_id"]
        if (
            item["total_history_influence_numerator"]
            != item["window_influence_numerator"] + item["tail_influence_numerator"]
        ):
            blockers.append(
                "source_memoryos_v041_total_influence_identity_invalid_" + history_id
            )
        if (
            item["conditioned_action_numerator"]
            != item["base_action_numerator"]
            + item["total_history_influence_numerator"]
        ):
            blockers.append(
                "source_memoryos_v041_conditioned_action_identity_invalid_" + history_id
            )
        if item["action_denominator"] != source_memoryos_v041["action_denominator"]:
            blockers.append("source_memoryos_v041_action_denominator_mismatch_" + history_id)
        if not item["support_retained"]:
            blockers.append("source_memoryos_v041_candidate_support_not_retained_" + history_id)


def _append_segment_blockers(
    blockers: list[str],
    source_memoryos_v041: dict[str, Any],
    temporal_segments: list[dict[str, Any]],
) -> None:
    records = source_memoryos_v041["history_projection_records"]
    records_by_id = {record["record_id"]: record for record in records}
    flattened = [record_id for segment in temporal_segments for record_id in segment["record_ids"]]
    if flattened != source_memoryos_v041["retained_record_ids"]:
        blockers.append("temporal_segment_record_coverage_or_order_invalid")
    if any(len(segment["record_ids"]) != 1 for segment in temporal_segments):
        blockers.append("temporal_segment_must_bind_exactly_one_source_record")
    if len(temporal_segments) != len(records):
        blockers.append("temporal_segment_count_must_equal_source_record_count")
    window_start = len(records) - source_memoryos_v041["window_length"]
    window_weight_by_record = {
        record["record_id"]: weight
        for record, weight in zip(
            records[window_start:], source_memoryos_v041["lag_weights"]
        )
    }
    for index, segment in enumerate(temporal_segments):
        if len(segment["record_ids"]) != 1:
            continue
        record_id = segment["record_ids"][0]
        record = records_by_id[record_id]
        if segment["source_sequence_start"] != index or segment["source_sequence_end"] != index:
            blockers.append("temporal_segment_sequence_binding_invalid_" + segment["segment_id"])
        if record["sequence_index"] != index:
            blockers.append("source_record_sequence_binding_invalid_" + record_id)
        if segment["observer_id"] != record["observer_id"]:
            blockers.append("temporal_segment_observer_binding_invalid_" + segment["segment_id"])
        expected_kind = "discarded-tail" if index < window_start else "retained-window"
        if segment["segment_kind"] != expected_kind:
            blockers.append("temporal_segment_kind_binding_invalid_" + segment["segment_id"])
        expected_weight = 1 if expected_kind == "discarded-tail" else window_weight_by_record[record_id]
        if segment["lag_weight"] != expected_weight:
            blockers.append("temporal_segment_lag_weight_binding_invalid_" + segment["segment_id"])
        if not record["observation_backaction_visible"]:
            blockers.append("source_observation_backaction_hidden_" + record_id)
        if record["translation_residue_visible"] and not segment["translation_residue_visible"]:
            blockers.append("temporal_segment_hides_source_translation_residue_" + segment["segment_id"])
        if index == 0:
            if segment["translation_from_previous_id"] is not None:
                blockers.append("first_temporal_segment_translation_must_be_none")
            continue
        previous = temporal_segments[index - 1]
        observer_changed = previous["observer_id"] != segment["observer_id"]
        if observer_changed:
            if segment["translation_from_previous_id"] is None:
                blockers.append("observer_transition_translation_required_" + segment["segment_id"])
            if not segment["translation_residue_visible"]:
                blockers.append("observer_transition_translation_residue_hidden_" + segment["segment_id"])
        elif segment["translation_from_previous_id"] is not None:
            blockers.append("same_observer_transition_must_not_invent_translation_" + segment["segment_id"])


def issue_observer_relative_temporal_window_coherence_cocycle_composition_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    blockers: list[str] = []
    if not isinstance(payload, Mapping):
        return {
            "accepted": False,
            "schema_version": SCHEMA_VERSION,
            "blockers": ["payload_invalid"],
            "observables": {},
            "certificate_digest": None,
        }
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        source_memoryos_v041 = normalize_source_memoryos_v041_receipt(
            payload.get("source_memoryos_v041_receipt")
        )
        source_memoryos_v042 = normalize_source_memoryos_v042_receipt(
            payload.get("source_memoryos_v042_receipt")
        )
        source_planos_v123 = normalize_source_planos_v123_kernel_receipt(
            payload.get("source_planos_v123_kernel_receipt")
        )
        temporal_segments = normalize_temporal_segments(
            payload.get("temporal_segments"),
            source_record_ids=source_memoryos_v041["retained_record_ids"],
            source_observer_ids=source_memoryos_v041["retained_observer_ids"],
            source_translation_ids=source_memoryos_v041["retained_translation_ids"],
        )
    except ValueError as exc:
        blockers.append(str(exc))
        return {
            "accepted": False,
            "schema_version": SCHEMA_VERSION,
            "blockers": blockers,
            "observables": {},
            "certificate_digest": None,
        }

    _append_source_boundary_blockers(
        blockers, source_memoryos_v041, source_memoryos_v042, source_planos_v123
    )
    _append_binding_blockers(
        blockers, source_memoryos_v041, source_memoryos_v042, source_planos_v123
    )
    _append_v041_arithmetic_blockers(blockers, source_memoryos_v041)
    _append_segment_blockers(blockers, source_memoryos_v041, temporal_segments)

    input_digest = compute_input_digest(
        source_memoryos_v041_receipt=source_memoryos_v041,
        source_memoryos_v042_receipt=source_memoryos_v042,
        source_planos_v123_kernel_receipt=source_planos_v123,
        temporal_segments=temporal_segments,
    )
    observables = temporal_window_coherence_cocycle_observables(
        source_memoryos_v041_receipt=source_memoryos_v041,
        source_memoryos_v042_receipt=source_memoryos_v042,
        source_planos_v123_kernel_receipt=source_planos_v123,
        temporal_segments=temporal_segments,
        input_digest=input_digest,
    )
    required_true = (
        "observer_translation_compatible",
        "v041_candidate_influence_profile_exact",
        "refinement_coarsening_consistent",
        "cocycle_direct_composition_consistent",
        "source_v042_trajectory_exact",
        "composition_associative",
        "all_composed_steps_hermitian",
        "all_composed_diagonals_preserved",
        "all_composed_steps_psd_by_diagonal_phase_congruence",
        "all_history_pair_support_retained",
    )
    for field in required_true:
        if not observables[field]:
            blockers.append("observable_required_" + field)
    if observables["source_kernel_digest"] != source_memoryos_v042["source_kernel_digest"]:
        blockers.append("observable_source_kernel_digest_mismatch")
    if (
        observables["refined_final_kernel_digest"]
        != source_memoryos_v042["conditioned_kernel_digest"]
    ):
        blockers.append("observable_conditioned_kernel_digest_mismatch")

    expected_claims = {**observables, **expected_governance_claims()}
    claims = payload.get("claims")
    if not isinstance(claims, Mapping):
        blockers.append("claims_invalid")
    else:
        for field, expected in expected_claims.items():
            if claims.get(field) != expected:
                blockers.append("claim_mismatch_" + field)
        extra = sorted(set(claims) - set(expected_claims))
        if extra:
            blockers.append("claim_extra_field_" + extra[0])

    accepted = not blockers
    certificate_digest = (
        digest_object(
            {
                "schema_version": SCHEMA_VERSION,
                "input_digest": input_digest,
                "observables": observables,
                "governance_claims": expected_governance_claims(),
            }
        )
        if accepted
        else None
    )
    return {
        "accepted": accepted,
        "schema_version": SCHEMA_VERSION,
        "blockers": blockers,
        "observables": observables,
        "governance_claims": expected_governance_claims(),
        "certificate_digest": certificate_digest,
    }


__all__ = [
    "issue_observer_relative_temporal_window_coherence_cocycle_composition_certificate"
]
