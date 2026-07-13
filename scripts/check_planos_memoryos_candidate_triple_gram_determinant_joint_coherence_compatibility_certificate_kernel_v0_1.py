#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from math import gcd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate_kernel_v0_1 import (
    issue_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate,
)
from runtime.kuuos_memoryos_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    canonical_digest,
    issue_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate,
)
from scripts.check_planos_memoryos_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v046_payload,
)

CANDIDATE_IDS = ["continue", "hold", "reobserve", "terminate_candidate"]
DEPHASING_NUMERATORS = [2, 1, 0]


def source_memoryos_v046_certificate() -> dict:
    result = issue_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate(
        build_memoryos_v046_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def _complex_mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _abs_square(value: tuple[int, int]) -> int:
    return value[0] * value[0] + value[1] * value[1]


def _pair_map(step: dict) -> dict[tuple[str, str], dict]:
    return {
        (item["left_candidate_id"], item["right_candidate_id"]): item
        for item in step["candidate_pair_envelopes"]
    }


def expected_triple_trajectory(source: dict) -> list[dict]:
    trajectory: list[dict] = []
    for source_step in source["observables"][
        "candidate_pair_cauchy_schwarz_envelope_trajectory"
    ]:
        pairs = _pair_map(source_step)
        denominator = source_step["source_kernel_entry_denominator"]
        records: list[dict] = []
        for first_id in CANDIDATE_IDS:
            for second_id in CANDIDATE_IDS:
                for third_id in CANDIDATE_IDS:
                    first_diagonal = pairs[(first_id, first_id)][
                        "source_real_numerator"
                    ]
                    second_diagonal = pairs[(second_id, second_id)][
                        "source_real_numerator"
                    ]
                    third_diagonal = pairs[(third_id, third_id)][
                        "source_real_numerator"
                    ]
                    first_second = (
                        pairs[(first_id, second_id)]["source_real_numerator"],
                        pairs[(first_id, second_id)]["source_imag_numerator"],
                    )
                    second_third = (
                        pairs[(second_id, third_id)]["source_real_numerator"],
                        pairs[(second_id, third_id)]["source_imag_numerator"],
                    )
                    third_first = (
                        pairs[(third_id, first_id)]["source_real_numerator"],
                        pairs[(third_id, first_id)]["source_imag_numerator"],
                    )
                    cyclic = _complex_mul(
                        _complex_mul(first_second, second_third),
                        third_first,
                    )
                    diagonal_cubic = (
                        first_diagonal * second_diagonal * third_diagonal
                    )
                    first_subtraction = (
                        first_diagonal * _abs_square(second_third)
                    )
                    second_subtraction = (
                        second_diagonal * _abs_square(third_first)
                    )
                    third_subtraction = (
                        third_diagonal * _abs_square(first_second)
                    )
                    determinant = (
                        diagonal_cubic
                        + 2 * cyclic[0]
                        - first_subtraction
                        - second_subtraction
                        - third_subtraction
                    )
                    distinct = len({first_id, second_id, third_id}) == 3
                    records.append(
                        {
                            "first_candidate_id": first_id,
                            "second_candidate_id": second_id,
                            "third_candidate_id": third_id,
                            "candidate_ids_distinct": distinct,
                            "first_diagonal_numerator": first_diagonal,
                            "second_diagonal_numerator": second_diagonal,
                            "third_diagonal_numerator": third_diagonal,
                            "first_second_real_numerator": first_second[0],
                            "first_second_imag_numerator": first_second[1],
                            "second_third_real_numerator": second_third[0],
                            "second_third_imag_numerator": second_third[1],
                            "third_first_real_numerator": third_first[0],
                            "third_first_imag_numerator": third_first[1],
                            "cyclic_product_real_numerator": cyclic[0],
                            "cyclic_product_imag_numerator": cyclic[1],
                            "twice_cyclic_product_real_numerator": 2 * cyclic[0],
                            "diagonal_cubic_numerator": diagonal_cubic,
                            "first_diagonal_times_second_third_magnitude_square_numerator": (
                                first_subtraction
                            ),
                            "second_diagonal_times_third_first_magnitude_square_numerator": (
                                second_subtraction
                            ),
                            "third_diagonal_times_first_second_magnitude_square_numerator": (
                                third_subtraction
                            ),
                            "candidate_triple_gram_determinant_numerator": determinant,
                            "candidate_triple_gram_determinant_denominator": denominator**3,
                            "candidate_triple_principal_minor_nonnegative": determinant >= 0,
                            "candidate_triple_rank_two_determinant_zero": determinant == 0,
                            "pairwise_envelopes_jointly_compatible": determinant >= 0,
                            "triple_retained": True,
                        }
                    )
        trajectory.append(
            {
                "step_index": source_step["step_index"],
                "dephasing_numerator": source_step["dephasing_numerator"],
                "source_kernel_entry_denominator": denominator,
                "candidate_triple_gram_determinant_records": records,
                "ordered_candidate_triple_support_complete": True,
                "all_step_candidate_triple_principal_minors_nonnegative": all(
                    item["candidate_triple_principal_minor_nonnegative"]
                    for item in records
                ),
                "all_step_candidate_triple_determinants_zero": all(
                    item["candidate_triple_rank_two_determinant_zero"]
                    for item in records
                ),
                "all_step_pairwise_envelopes_jointly_compatible": all(
                    item["pairwise_envelopes_jointly_compatible"]
                    for item in records
                ),
            }
        )
    return trajectory


def expected_claims(source: dict) -> dict:
    source_obs = source["observables"]
    trajectory = expected_triple_trajectory(source)
    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v046_certificate_digest": source[
                "certificate_digest"
            ],
            "source_candidate_pair_envelope_digest": source_obs[
                "candidate_pair_cauchy_schwarz_envelope_digest"
            ],
            "candidate_ids": CANDIDATE_IDS,
        }
    )
    return {
        "input_digest": input_digest,
        "source_memoryos_v046_certificate_digest": source["certificate_digest"],
        "source_memoryos_v046_candidate_pair_envelope_digest": source_obs[
            "candidate_pair_cauchy_schwarz_envelope_digest"
        ],
        "source_memoryos_v045_certificate_digest": source_obs[
            "source_memoryos_v045_certificate_digest"
        ],
        "source_memoryos_v045_candidate_gram_kernel_digest": source_obs[
            "source_memoryos_v045_candidate_gram_kernel_digest"
        ],
        "source_memoryos_v043_certificate_digest": source_obs[
            "source_memoryos_v043_certificate_digest"
        ],
        "source_memoryos_v044_certificate_digest": source_obs[
            "source_memoryos_v044_certificate_digest"
        ],
        "retained_decision_candidate_ids": CANDIDATE_IDS,
        "candidate_triple_gram_determinant_trajectory": trajectory,
        "candidate_triple_gram_determinant_digest": canonical_digest(trajectory),
        "ordered_candidate_triple_count_per_step": 64,
        "distinct_ordered_candidate_triple_count_per_step": 24,
        "all_ordered_candidate_triple_support_retained": True,
        "all_candidate_triple_principal_minors_nonnegative": True,
        "all_candidate_triple_determinants_zero": True,
        "all_pairwise_envelopes_jointly_compatible": True,
        "candidate_gram_rank_at_most_two_witness": True,
        "all_repeated_candidate_triples_degenerate": True,
        "all_distinct_candidate_triples_rank_two_saturated": True,
        "source_candidate_pair_envelope_exact": True,
        "source_relational_frontier_candidate_ids": ["reobserve"],
        "source_required_review_candidate_ids": [
            "continue",
            "hold",
            "reobserve",
        ],
        "source_dissent_review_candidate_ids": ["continue"],
        "source_minority_protection_candidate_ids": ["hold"],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "joint_coherence_compatibility_advisory_only": True,
        "triple_cyclic_product_not_group_preference": True,
        "rank_two_saturation_not_candidate_consensus": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v046_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def build_reference_payload() -> dict:
    source = source_memoryos_v046_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v046_certificate": source,
        "claims": expected_claims(source),
    }


def _resign_v046(certificate: dict) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def _fraction(numerator: int, denominator: int) -> tuple[int, int]:
    common = gcd(numerator, denominator)
    return numerator // common, denominator // common


def _set_pair_real(
    certificate: dict,
    *,
    step_index: int,
    left_id: str,
    right_id: str,
    real_numerator: int,
) -> None:
    trajectory = certificate["observables"][
        "candidate_pair_cauchy_schwarz_envelope_trajectory"
    ]
    step = trajectory[step_index]
    records = step["candidate_pair_envelopes"]
    for item in records:
        pair = item["left_candidate_id"], item["right_candidate_id"]
        if pair not in {
            (left_id, right_id),
            (right_id, left_id),
        }:
            continue
        item["source_real_numerator"] = real_numerator
        item["source_imag_numerator"] = 0
        magnitude = real_numerator * real_numerator
        product = (
            item["left_diagonal_numerator"]
            * item["right_diagonal_numerator"]
        )
        margin = product - magnitude
        zero_pair = (
            item["left_diagonal_numerator"] == 0
            or item["right_diagonal_numerator"] == 0
        )
        if zero_pair:
            normalized = (0, 1)
        else:
            normalized = _fraction(magnitude, product)
        item["coherence_magnitude_square_numerator"] = magnitude
        item["diagonal_product_numerator"] = product
        item["determinant_margin_numerator"] = margin
        item["cauchy_schwarz_bound_holds"] = margin >= 0
        item["zero_diagonal_pair"] = zero_pair
        item["zero_diagonal_forces_zero_coherence"] = (
            not zero_pair or magnitude == 0
        )
        item["normalized_coherence_square_numerator"] = normalized[0]
        item["normalized_coherence_square_denominator"] = normalized[1]
        item["normalized_coherence_square_at_most_one"] = (
            normalized[0] <= normalized[1]
        )
    step["all_step_cauchy_schwarz_bounds_hold"] = all(
        item["cauchy_schwarz_bound_holds"] for item in records
    )
    step["all_step_normalized_coherence_squares_at_most_one"] = all(
        item["normalized_coherence_square_at_most_one"] for item in records
    )
    step["all_step_zero_diagonal_pairs_have_zero_coherence"] = all(
        item["zero_diagonal_forces_zero_coherence"] for item in records
    )
    observables = certificate["observables"]
    observables["all_cauchy_schwarz_bounds_hold"] = all(
        item["all_step_cauchy_schwarz_bounds_hold"] for item in trajectory
    )
    observables["all_normalized_coherence_squares_bounded_by_one"] = all(
        item["all_step_normalized_coherence_squares_at_most_one"]
        for item in trajectory
    )
    observables["all_zero_diagonal_pairs_have_zero_coherence"] = all(
        item["all_step_zero_diagonal_pairs_have_zero_coherence"]
        for item in trajectory
    )
    observables["candidate_pair_cauchy_schwarz_envelope_digest"] = (
        canonical_digest(trajectory)
    )
    _resign_v046(certificate)


def assert_rejects(payload: dict, blocker: str) -> None:
    result = issue_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def _record(step: dict, first_id: str, second_id: str, third_id: str) -> dict:
    return next(
        item
        for item in step["candidate_triple_gram_determinant_records"]
        if item["first_candidate_id"] == first_id
        and item["second_candidate_id"] == second_id
        and item["third_candidate_id"] == third_id
    )


def _trajectory_values(
    steps: list[dict],
    first_id: str,
    second_id: str,
    third_id: str,
    field: str,
) -> list:
    return [
        _record(step, first_id, second_id, third_id)[field]
        for step in steps
    ]


def main() -> int:
    payload = build_reference_payload()
    certificate = issue_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate(
        payload
    )
    assert certificate["accepted"], certificate["blockers"]
    obs = certificate["observables"]
    steps = obs["candidate_triple_gram_determinant_trajectory"]
    assert len(steps) == 3
    assert all(
        len(step["candidate_triple_gram_determinant_records"]) == 64
        for step in steps
    )
    assert obs["ordered_candidate_triple_count_per_step"] == 64
    assert obs["distinct_ordered_candidate_triple_count_per_step"] == 24

    triple = ("continue", "reobserve", "terminate_candidate")
    assert _trajectory_values(
        steps, *triple, "cyclic_product_real_numerator"
    ) == [32, 9, 0]
    assert _trajectory_values(
        steps, *triple, "twice_cyclic_product_real_numerator"
    ) == [64, 18, 0]
    assert _trajectory_values(
        steps, *triple, "diagonal_cubic_numerator"
    ) == [32, 24, 16]
    assert _trajectory_values(
        steps,
        *triple,
        "first_diagonal_times_second_third_magnitude_square_numerator",
    ) == [32, 6, 0]
    assert _trajectory_values(
        steps,
        *triple,
        "second_diagonal_times_third_first_magnitude_square_numerator",
    ) == [32, 18, 8]
    assert _trajectory_values(
        steps,
        *triple,
        "third_diagonal_times_first_second_magnitude_square_numerator",
    ) == [32, 18, 8]
    assert _trajectory_values(
        steps, *triple, "candidate_triple_gram_determinant_numerator"
    ) == [0, 0, 0]

    signed_triple = ("hold", "reobserve", "terminate_candidate")
    assert _trajectory_values(
        steps, *signed_triple, "cyclic_product_real_numerator"
    ) == [0, -1, 0]
    assert _trajectory_values(
        steps, *signed_triple, "twice_cyclic_product_real_numerator"
    ) == [0, -2, 0]
    assert _trajectory_values(
        steps, *signed_triple, "candidate_triple_gram_determinant_numerator"
    ) == [0, 0, 0]

    assert obs["all_ordered_candidate_triple_support_retained"]
    assert obs["all_candidate_triple_principal_minors_nonnegative"]
    assert obs["all_candidate_triple_determinants_zero"]
    assert obs["all_pairwise_envelopes_jointly_compatible"]
    assert obs["candidate_gram_rank_at_most_two_witness"]
    assert obs["all_distinct_candidate_triples_rank_two_saturated"]
    assert obs["source_relational_frontier_candidate_ids"] == ["reobserve"]
    assert obs["source_dissent_review_candidate_ids"] == ["continue"]
    assert obs["source_minority_protection_candidate_ids"] == ["hold"]

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v046_certificate"]["accepted"] = False
    assert_rejects(tampered, "source_memoryos_v046_not_accepted")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v046_certificate"][
        "certificate_digest"
    ] = "substituted"
    assert_rejects(
        tampered,
        "source_memoryos_v046_certificate_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v046_certificate"]["observables"][
        "candidate_pair_cauchy_schwarz_envelope_digest"
    ] = "substituted"
    _resign_v046(tampered["source_memoryos_v046_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v046_envelope_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    _set_pair_real(
        tampered["source_memoryos_v046_certificate"],
        step_index=1,
        left_id="reobserve",
        right_id="terminate_candidate",
        real_numerator=0,
    )
    assert_rejects(
        tampered,
        "observable_required_all_candidate_triple_principal_minors_nonnegative",
    )

    tampered = copy.deepcopy(payload)
    _set_pair_real(
        tampered["source_memoryos_v046_certificate"],
        step_index=1,
        left_id="continue",
        right_id="reobserve",
        real_numerator=2,
    )
    assert_rejects(
        tampered,
        "observable_required_all_candidate_triple_determinants_zero",
    )

    for field in (
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v046_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        tampered = copy.deepcopy(payload)
        tampered["claims"][field] = True
        assert_rejects(tampered, "claim_mismatch_" + field)

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": SCHEMA_VERSION,
                "candidate_count": len(CANDIDATE_IDS),
                "ordered_candidate_triple_count": len(CANDIDATE_IDS) ** 3,
                "distinct_ordered_candidate_triple_count": (
                    len(CANDIDATE_IDS)
                    * (len(CANDIDATE_IDS) - 1)
                    * (len(CANDIDATE_IDS) - 2)
                ),
                "dephasing_step_count": len(steps),
                "triple_determinant_digest": obs[
                    "candidate_triple_gram_determinant_digest"
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
