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

from runtime.kuuos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1 import (
    issue_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate,
)
from runtime.kuuos_memoryos_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    canonical_digest,
    issue_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate,
)
from scripts.check_planos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v045_payload,
)

CANDIDATE_IDS = ["continue", "hold", "reobserve", "terminate_candidate"]
DEPHASING_NUMERATORS = [2, 1, 0]
REFERENCE_MATRICES = [
    [
        [8, 0, 4, 4],
        [0, 0, 0, 0],
        [4, 0, 2, 2],
        [4, 0, 2, 2],
    ],
    [
        [6, 0, 3, 3],
        [0, 2, 1, -1],
        [3, 1, 2, 1],
        [3, -1, 1, 2],
    ],
    [
        [4, 0, 2, 2],
        [0, 4, 2, -2],
        [2, 2, 2, 0],
        [2, -2, 0, 2],
    ],
]


def source_memoryos_v045_certificate() -> dict:
    result = issue_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate(
        build_memoryos_v045_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def _fraction(numerator: int, denominator: int) -> tuple[int, int]:
    common = gcd(numerator, denominator)
    return numerator // common, denominator // common


def expected_envelope_trajectory() -> list[dict]:
    trajectory: list[dict] = []
    for step_index, (dephasing_numerator, matrix) in enumerate(
        zip(DEPHASING_NUMERATORS, REFERENCE_MATRICES)
    ):
        records: list[dict] = []
        for left_index, left_id in enumerate(CANDIDATE_IDS):
            for right_index, right_id in enumerate(CANDIDATE_IDS):
                real_numerator = matrix[left_index][right_index]
                imag_numerator = 0
                left_diagonal = matrix[left_index][left_index]
                right_diagonal = matrix[right_index][right_index]
                magnitude_square = real_numerator * real_numerator
                diagonal_product = left_diagonal * right_diagonal
                margin = diagonal_product - magnitude_square
                zero_diagonal_pair = left_diagonal == 0 or right_diagonal == 0
                if zero_diagonal_pair:
                    normalized_numerator, normalized_denominator = 0, 1
                else:
                    normalized_numerator, normalized_denominator = _fraction(
                        magnitude_square,
                        diagonal_product,
                    )
                records.append(
                    {
                        "left_candidate_id": left_id,
                        "right_candidate_id": right_id,
                        "source_real_numerator": real_numerator,
                        "source_imag_numerator": imag_numerator,
                        "source_kernel_entry_denominator": 2,
                        "left_diagonal_numerator": left_diagonal,
                        "right_diagonal_numerator": right_diagonal,
                        "coherence_magnitude_square_numerator": magnitude_square,
                        "coherence_magnitude_square_denominator": 4,
                        "diagonal_product_numerator": diagonal_product,
                        "diagonal_product_denominator": 4,
                        "determinant_margin_numerator": margin,
                        "determinant_margin_denominator": 4,
                        "cauchy_schwarz_bound_holds": True,
                        "zero_diagonal_pair": zero_diagonal_pair,
                        "zero_diagonal_forces_zero_coherence": True,
                        "normalized_coherence_square_numerator": normalized_numerator,
                        "normalized_coherence_square_denominator": normalized_denominator,
                        "normalized_coherence_square_at_most_one": True,
                        "pair_retained": True,
                    }
                )
        trajectory.append(
            {
                "step_index": step_index,
                "dephasing_numerator": dephasing_numerator,
                "source_kernel_entry_denominator": 2,
                "candidate_pair_envelopes": records,
                "ordered_candidate_pair_support_complete": True,
                "all_step_cauchy_schwarz_bounds_hold": True,
                "all_step_normalized_coherence_squares_at_most_one": True,
                "all_step_zero_diagonal_pairs_have_zero_coherence": True,
            }
        )
    return trajectory


def expected_claims(source: dict) -> dict:
    source_obs = source["observables"]
    trajectory = expected_envelope_trajectory()
    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v045_certificate_digest": source[
                "certificate_digest"
            ],
            "source_candidate_gram_kernel_digest": source_obs[
                "candidate_gram_kernel_digest"
            ],
            "candidate_ids": CANDIDATE_IDS,
        }
    )
    return {
        "input_digest": input_digest,
        "source_memoryos_v045_certificate_digest": source["certificate_digest"],
        "source_memoryos_v045_candidate_gram_kernel_digest": source_obs[
            "candidate_gram_kernel_digest"
        ],
        "source_memoryos_v043_certificate_digest": source_obs[
            "source_memoryos_v043_certificate_digest"
        ],
        "source_memoryos_v044_certificate_digest": source_obs[
            "source_memoryos_v044_certificate_digest"
        ],
        "retained_decision_candidate_ids": CANDIDATE_IDS,
        "candidate_pair_cauchy_schwarz_envelope_trajectory": trajectory,
        "candidate_pair_cauchy_schwarz_envelope_digest": canonical_digest(
            trajectory
        ),
        "all_ordered_candidate_pair_support_retained": True,
        "all_cauchy_schwarz_bounds_hold": True,
        "all_normalized_coherence_squares_bounded_by_one": True,
        "all_zero_diagonal_pairs_have_zero_coherence": True,
        "all_candidate_diagonals_nonnegative": True,
        "source_candidate_gram_kernel_exact": True,
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
        "normalized_coherence_advisory_only": True,
        "normalized_coherence_not_scalar_utility": True,
        "off_diagonal_sign_not_preference": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v045_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def build_reference_payload() -> dict:
    source = source_memoryos_v045_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v045_certificate": source,
        "claims": expected_claims(source),
    }


def _resign_v045(certificate: dict) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def _refresh_v045_kernel_digest_and_resign(certificate: dict) -> None:
    observables = certificate["observables"]
    observables["candidate_gram_kernel_digest"] = canonical_digest(
        observables["candidate_gram_kernel_trajectory"]
    )
    _resign_v045(certificate)


def assert_rejects(payload: dict, blocker: str) -> None:
    result = issue_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def _record(step: dict, left_id: str, right_id: str) -> dict:
    return next(
        item
        for item in step["candidate_pair_envelopes"]
        if item["left_candidate_id"] == left_id
        and item["right_candidate_id"] == right_id
    )


def _trajectory_values(
    steps: list[dict], left_id: str, right_id: str, field: str
) -> list:
    return [_record(step, left_id, right_id)[field] for step in steps]


def main() -> int:
    payload = build_reference_payload()
    certificate = issue_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate(
        payload
    )
    assert certificate["accepted"], certificate["blockers"]
    obs = certificate["observables"]
    steps = obs["candidate_pair_cauchy_schwarz_envelope_trajectory"]
    assert len(steps) == 3
    assert all(len(step["candidate_pair_envelopes"]) == 16 for step in steps)

    assert list(
        zip(
            _trajectory_values(
                steps,
                "continue",
                "reobserve",
                "normalized_coherence_square_numerator",
            ),
            _trajectory_values(
                steps,
                "continue",
                "reobserve",
                "normalized_coherence_square_denominator",
            ),
        )
    ) == [(1, 1), (3, 4), (1, 2)]
    assert _trajectory_values(
        steps,
        "continue",
        "reobserve",
        "determinant_margin_numerator",
    ) == [0, 3, 4]

    assert list(
        zip(
            _trajectory_values(
                steps,
                "hold",
                "terminate_candidate",
                "normalized_coherence_square_numerator",
            ),
            _trajectory_values(
                steps,
                "hold",
                "terminate_candidate",
                "normalized_coherence_square_denominator",
            ),
        )
    ) == [(0, 1), (1, 4), (1, 2)]
    assert _trajectory_values(
        steps,
        "hold",
        "terminate_candidate",
        "source_real_numerator",
    ) == [0, -1, -2]
    assert _trajectory_values(
        steps,
        "hold",
        "terminate_candidate",
        "determinant_margin_numerator",
    ) == [0, 3, 4]

    assert list(
        zip(
            _trajectory_values(
                steps,
                "reobserve",
                "terminate_candidate",
                "normalized_coherence_square_numerator",
            ),
            _trajectory_values(
                steps,
                "reobserve",
                "terminate_candidate",
                "normalized_coherence_square_denominator",
            ),
        )
    ) == [(1, 1), (1, 4), (0, 1)]
    assert _trajectory_values(
        steps,
        "continue",
        "hold",
        "determinant_margin_numerator",
    ) == [0, 12, 16]
    assert _trajectory_values(
        steps,
        "continue",
        "hold",
        "zero_diagonal_pair",
    ) == [True, False, False]

    assert obs["all_ordered_candidate_pair_support_retained"]
    assert obs["all_cauchy_schwarz_bounds_hold"]
    assert obs["all_normalized_coherence_squares_bounded_by_one"]
    assert obs["all_zero_diagonal_pairs_have_zero_coherence"]
    assert obs["source_relational_frontier_candidate_ids"] == ["reobserve"]
    assert obs["source_dissent_review_candidate_ids"] == ["continue"]
    assert obs["source_minority_protection_candidate_ids"] == ["hold"]

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v045_certificate"]["accepted"] = False
    assert_rejects(tampered, "source_memoryos_v045_not_accepted")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v045_certificate"]["certificate_digest"] = "substituted"
    assert_rejects(tampered, "source_memoryos_v045_certificate_digest_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v045_certificate"]["observables"][
        "candidate_gram_kernel_digest"
    ] = "substituted"
    _resign_v045(tampered["source_memoryos_v045_certificate"])
    assert_rejects(tampered, "source_memoryos_v045_kernel_digest_mismatch")

    tampered = copy.deepcopy(payload)
    trajectory = tampered["source_memoryos_v045_certificate"]["observables"][
        "candidate_gram_kernel_trajectory"
    ]
    for item in trajectory[1]["candidate_kernel_entries"]:
        pair = item["left_candidate_id"], item["right_candidate_id"]
        if pair in {
            ("continue", "reobserve"),
            ("reobserve", "continue"),
        }:
            item["real_numerator"] = 99
    _refresh_v045_kernel_digest_and_resign(
        tampered["source_memoryos_v045_certificate"]
    )
    assert_rejects(
        tampered,
        "observable_required_all_cauchy_schwarz_bounds_hold",
    )

    tampered = copy.deepcopy(payload)
    trajectory = tampered["source_memoryos_v045_certificate"]["observables"][
        "candidate_gram_kernel_trajectory"
    ]
    for item in trajectory[0]["candidate_kernel_entries"]:
        pair = item["left_candidate_id"], item["right_candidate_id"]
        if pair in {
            ("hold", "reobserve"),
            ("reobserve", "hold"),
        }:
            item["real_numerator"] = 1
    _refresh_v045_kernel_digest_and_resign(
        tampered["source_memoryos_v045_certificate"]
    )
    assert_rejects(
        tampered,
        "observable_required_all_zero_diagonal_pairs_have_zero_coherence",
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
        "source_memoryos_v045_mutated",
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
                "ordered_candidate_pair_count": len(CANDIDATE_IDS) ** 2,
                "dephasing_step_count": len(steps),
                "envelope_digest": obs[
                    "candidate_pair_cauchy_schwarz_envelope_digest"
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
