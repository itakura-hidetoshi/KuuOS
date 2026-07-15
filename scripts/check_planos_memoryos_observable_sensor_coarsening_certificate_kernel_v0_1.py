#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_global_observable_kernel_quotient_certificate_kernel_v0_1 import (
    issue_global_observable_kernel_quotient_certificate,
)
from runtime.kuuos_memoryos_observable_sensor_coarsening_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_observable_sensor_coarsening_certificate,
)
from scripts.check_planos_memoryos_global_observable_kernel_quotient_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v084_payload,
)


def source_memoryos_v084_certificate() -> dict[str, Any]:
    result = issue_global_observable_kernel_quotient_certificate(
        build_memoryos_v084_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v084 = source_memoryos_v084_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v084_certificate": source_v084,
        "claims": _derive_observables(source_v084),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_observable_sensor_coarsening_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_observable_sensor_coarsening_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_observable_sensor_coarsening_record_count": 6,
        "sensor_profile_record_count": 3,
        "sensor_kernel_inclusion_record_count": 12,
        "sensor_root_independence_record_count": 48,
        "sensor_composition_record_count": 16,
        "sensor_quotient_functoriality_record_count": 12,
        "injective_sensor_equivalence_record_count": 4,
        "sensor_wilson_pullback_record_count": 12,
        "canonical_sensor_visibility_record_count": 12,
        "source_confidence_preservation_record_count": 4,
        "observable_sensor_coarsening_memory_fusion_record_count": 4,
        "full_rank_transport_observable_sensor_coarsening_record_count": 8,
        "singular_atomic_observable_sensor_coarsening_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    profiles = obs["sensor_profile_records"]
    assert [record["sensor_id"] for record in profiles] == [
        "identity-s3",
        "parity-c2",
        "terminal-group",
    ]
    assert profiles[0]["injective"] is True
    assert profiles[1]["injective"] is False
    assert profiles[2]["injective"] is False

    assert all(
        record["global_kernel_subset_sensor_kernel"]
        and record["kernel_information_can_only_be_lost"]
        for record in obs["sensor_kernel_inclusion_records"]
    )
    identity_kernel = [
        record
        for record in obs["sensor_kernel_inclusion_records"]
        if record["sensor_id"] == "identity-s3"
    ]
    assert len(identity_kernel) == 4
    assert all(record["sensor_kernel_equals_global_kernel"] for record in identity_kernel)

    assert all(
        record["sensor_evaluation_hom_equal"]
        and record["sensor_kernel_equal"]
        and record["sensor_range_equal"]
        for record in obs["sensor_root_independence_records"]
    )
    assert all(
        record["evaluation_composition_exact"]
        and record["source_sensor_kernel_subset_composite_kernel"]
        and record["quotient_coarsening_composes"]
        for record in obs["sensor_composition_records"]
    )
    assert all(
        record["source_quotient_maps_to_sensor_quotient"]
        and record["representative_class_preserved"]
        and record["sensor_first_isomorphism_exact"]
        for record in obs["sensor_quotient_functoriality_records"]
    )
    assert all(
        record["sensor_injective"]
        and record["sensor_kernel_equals_global_kernel"]
        and record["observable_quotient_mul_equivalence_exact"]
        and record["canonical_separator_preserved"]
        for record in obs["injective_sensor_equivalence_records"]
    )
    assert all(
        record["class_function_pulled_back_along_sensor"]
        and record["sensor_wilson_equals_pullback_wilson"]
        and record["sensor_wilson_root_independent"]
        for record in obs["sensor_wilson_pullback_records"]
    )

    visibility = obs["canonical_sensor_visibility_records"]
    identity_visibility = [r for r in visibility if r["sensor_id"] == "identity-s3"]
    parity_visibility = [r for r in visibility if r["sensor_id"] == "parity-c2"]
    terminal_visibility = [r for r in visibility if r["sensor_id"] == "terminal-group"]
    assert len(identity_visibility) == len(parity_visibility) == len(terminal_visibility) == 4
    assert all(record["ordered_ab_in_sensor_kernel"] for record in visibility)
    assert all(record["ordered_ba_visible_after_sensor"] for record in identity_visibility)
    assert all(record["canonical_separator_preserved"] for record in identity_visibility)
    assert all(not record["ordered_ba_in_sensor_kernel"] for record in identity_visibility)
    assert all(record["ordered_ba_in_sensor_kernel"] for record in parity_visibility)
    assert all(not record["canonical_separator_preserved"] for record in parity_visibility)
    assert all(record["ordered_ba_in_sensor_kernel"] for record in terminal_visibility)
    assert all(not record["canonical_separator_preserved"] for record in terminal_visibility)

    expected_confidence = {
        "flat_four_route_atlas": {"numerator": 1, "denominator": 3},
        "single_support_atlas": {"numerator": 5, "denominator": 18},
        "ordered_ab_atlas": {"numerator": 11, "denominator": 54},
        "ordered_ba_atlas": {"numerator": 11, "denominator": 54},
    }
    for record in obs["source_confidence_preservation_records"]:
        expected = expected_confidence[record["profile_id"]]
        assert record["source_global_observable_quotient_adjusted_confidence"] == expected
        assert record["observable_sensor_coarsening_adjusted_confidence"] == expected
        assert record["new_sensor_coarsening_penalty"] == {
            "numerator": 0,
            "denominator": 1,
        }
        assert record["confidence_preserved_exactly"]

    required_true = (
        "source_memoryos_v084_exact",
        "finite_observable_sensor_coarsening_exact",
        "sensor_evaluation_homomorphism_exact",
        "global_kernel_included_in_every_sensor_kernel_exact",
        "sensor_kernel_root_independent_exact",
        "sensor_range_root_independent_exact",
        "sensor_composition_kernel_monotone_exact",
        "observable_quotient_functorial_map_exact",
        "sensor_first_isomorphism_exact",
        "injective_sensor_quotient_equivalence_exact",
        "sensor_wilson_pullback_exact",
        "sensor_wilson_root_independent_exact",
        "identity_sensor_separator_preserved_exact",
        "noninjective_sensor_information_loss_recorded",
        "parity_sensor_collapses_canonical_ab_ba_separator",
        "terminal_sensor_collapses_all_canonical_values",
        "source_confidence_preserved_exact",
        "no_new_confidence_penalty_introduced",
        "all_full_rank_transport_observable_sensor_coarsening_layer_commutes",
        "singular_atomic_observable_sensor_coarsening_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "sensor_coarsening_not_truth_authority",
        "sensor_kernel_not_candidate_pruning",
        "sensor_resolution_not_candidate_ranking",
        "sensor_postprocessing_not_source_mutation",
        "future_only",
        "read_only",
    )
    for field in required_true:
        assert obs[field] is True, field

    required_false = (
        "universal_sensor_classification_claimed",
        "universal_information_order_claimed",
        "continuum_observation_stack_claimed",
        "physical_measurement_inference_claimed",
        "sensor_kernel_used_as_truth",
        "sensor_kernel_used_as_candidate_pruning",
        "sensor_resolution_used_as_candidate_ranking",
        "source_confidence_mutated",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v084_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_false:
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["claims"]["sensor_kernel_inclusion_records"][0][
        "global_kernel_subset_sensor_kernel"
    ] = False
    assert_rejects(tampered, "claim_mismatch_sensor_kernel_inclusion_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["sensor_root_independence_records"][17][
        "sensor_kernel_equal"
    ] = False
    assert_rejects(tampered, "claim_mismatch_sensor_root_independence_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["sensor_composition_records"][6][
        "source_sensor_kernel_subset_composite_kernel"
    ] = False
    assert_rejects(tampered, "claim_mismatch_sensor_composition_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["injective_sensor_equivalence_records"][2][
        "observable_quotient_mul_equivalence_exact"
    ] = False
    assert_rejects(tampered, "claim_mismatch_injective_sensor_equivalence_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["canonical_sensor_visibility_records"][0][
        "canonical_separator_preserved"
    ] = False
    assert_rejects(tampered, "claim_mismatch_canonical_sensor_visibility_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["source_confidence_preservation_records"][0][
        "observable_sensor_coarsening_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 2}
    assert_rejects(tampered, "claim_mismatch_source_confidence_preservation_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["sensor_coarsening_not_truth_authority"] = False
    assert_rejects(tampered, "claim_mismatch_sensor_coarsening_not_truth_authority")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v084_certificate"]["observables"][
        "canonical_kernel_visibility_records"
    ][0]["ordered_ab_value"] = [1, 0, 2]
    assert_rejects(tampered, "source_memoryos_v084_certificate_digest_mismatch")

    print("MemoryOS v0.85 observable sensor coarsening checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
