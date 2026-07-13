#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    canonical_digest,
    issue_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate,
)
from runtime.kuuos_memoryos_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate_kernel_v0_1 import (
    issue_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate,
)
from scripts.check_planos_memoryos_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v044_payload,
    source_memoryos_v043_certificate,
)

HISTORY_IDS = ["plan-history-a", "plan-history-b"]
CANDIDATE_IDS = ["continue", "hold", "reobserve", "terminate_candidate"]
DEPHASING_NUMERATORS = [2, 1, 0]


def source_memoryos_v044_certificate() -> dict:
    result = issue_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate(
        build_memoryos_v044_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def _matrix_entries(matrix: list[list[int]]) -> list[dict]:
    return [
        {
            "left_candidate_id": left_id,
            "right_candidate_id": right_id,
            "real_numerator": matrix[left_index][right_index],
            "imag_numerator": 0,
        }
        for left_index, left_id in enumerate(CANDIDATE_IDS)
        for right_index, right_id in enumerate(CANDIDATE_IDS)
    ]


def reference_matrices() -> list[list[list[int]]]:
    return [
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


def expected_candidate_kernel_trajectory() -> list[dict]:
    return [
        {
            "step_index": index,
            "dephasing_numerator": numerator,
            "kernel_entry_denominator": 2,
            "candidate_kernel_entries": _matrix_entries(matrix),
            "candidate_pair_support_complete": True,
            "candidate_kernel_hermitian": True,
            "candidate_kernel_positive_semidefinite_by_gram_lift": True,
            "candidate_kernel_diagonal_matches_v044_quadratic_evidence": True,
        }
        for index, (numerator, matrix) in enumerate(
            zip(DEPHASING_NUMERATORS, reference_matrices())
        )
    ]


def expected_pair_records() -> list[dict]:
    matrices = reference_matrices()
    output: list[dict] = []
    for left_index, left_id in enumerate(CANDIDATE_IDS):
        for right_index in range(left_index + 1, len(CANDIDATE_IDS)):
            right_id = CANDIDATE_IDS[right_index]
            values = [matrix[left_index][right_index] for matrix in matrices]
            trajectory = [
                {
                    "step_index": index,
                    "dephasing_numerator": numerator,
                    "real_numerator": value,
                    "imag_numerator": 0,
                    "denominator": 2,
                }
                for index, (numerator, value) in enumerate(
                    zip(DEPHASING_NUMERATORS, values)
                )
            ]
            output.append(
                {
                    "left_candidate_id": left_id,
                    "right_candidate_id": right_id,
                    "pair_coherence_trajectory": trajectory,
                    "full_coherence_real_numerator": values[0],
                    "fully_dephased_real_numerator": values[-1],
                    "pair_coherence_contrast_numerator": values[0] - values[-1],
                    "pair_retained": True,
                }
            )
    return output


def expected_claims(source_v043: dict, source_v044: dict) -> dict:
    v043 = source_v043["observables"]
    v044 = source_v044["observables"]
    trajectory = expected_candidate_kernel_trajectory()
    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v043_certificate_digest": source_v043[
                "certificate_digest"
            ],
            "source_memoryos_v044_certificate_digest": source_v044[
                "certificate_digest"
            ],
            "candidate_ids": CANDIDATE_IDS,
            "history_ids": HISTORY_IDS,
            "candidate_history_couplings": v044["candidate_history_couplings"],
        }
    )
    return {
        "input_digest": input_digest,
        "source_memoryos_v043_certificate_digest": source_v043[
            "certificate_digest"
        ],
        "source_memoryos_v043_conditioned_kernel_digest": v043[
            "refined_final_kernel_digest"
        ],
        "source_memoryos_v044_certificate_digest": source_v044[
            "certificate_digest"
        ],
        "source_memoryos_v044_quadratic_evidence_input_digest": v044[
            "input_digest"
        ],
        "retained_history_ids": HISTORY_IDS,
        "retained_decision_candidate_ids": CANDIDATE_IDS,
        "candidate_history_couplings": v044["candidate_history_couplings"],
        "candidate_gram_kernel_trajectory": trajectory,
        "candidate_pair_coherence_records": expected_pair_records(),
        "candidate_gram_kernel_digest": canonical_digest(trajectory),
        "all_candidate_pair_support_retained": True,
        "all_candidate_kernels_hermitian": True,
        "all_candidate_kernels_psd_by_gram_lift": True,
        "all_candidate_diagonals_match_v044_quadratic_evidence": True,
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "source_relational_frontier_candidate_ids": ["reobserve"],
        "source_required_review_candidate_ids": ["continue", "hold", "reobserve"],
        "source_dissent_review_candidate_ids": ["continue"],
        "source_minority_protection_candidate_ids": ["hold"],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "candidate_pair_coherence_advisory_only": True,
        "candidate_gram_kernel_not_relational_order": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v043_mutated": False,
        "source_memoryos_v044_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def build_reference_payload() -> dict:
    source_v043 = source_memoryos_v043_certificate()
    source_v044 = source_memoryos_v044_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v043_certificate": source_v043,
        "source_memoryos_v044_certificate": source_v044,
        "claims": expected_claims(source_v043, source_v044),
    }


def _resign_v044(certificate: dict) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def assert_rejects(payload: dict, blocker: str) -> None:
    result = issue_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def _entry(step: dict, left_id: str, right_id: str) -> dict:
    return next(
        item
        for item in step["candidate_kernel_entries"]
        if item["left_candidate_id"] == left_id
        and item["right_candidate_id"] == right_id
    )


def main() -> int:
    payload = build_reference_payload()
    certificate = issue_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate(
        payload
    )
    assert certificate["accepted"], certificate["blockers"]
    obs = certificate["observables"]
    steps = obs["candidate_gram_kernel_trajectory"]
    assert len(steps) == 3
    assert len(steps[0]["candidate_kernel_entries"]) == 16

    assert [_entry(step, "continue", "continue")["real_numerator"] for step in steps] == [8, 6, 4]
    assert [_entry(step, "hold", "hold")["real_numerator"] for step in steps] == [0, 2, 4]
    assert [_entry(step, "reobserve", "reobserve")["real_numerator"] for step in steps] == [2, 2, 2]
    assert [_entry(step, "terminate_candidate", "terminate_candidate")["real_numerator"] for step in steps] == [2, 2, 2]
    assert [_entry(step, "continue", "hold")["real_numerator"] for step in steps] == [0, 0, 0]
    assert [_entry(step, "continue", "reobserve")["real_numerator"] for step in steps] == [4, 3, 2]
    assert [_entry(step, "hold", "reobserve")["real_numerator"] for step in steps] == [0, 1, 2]
    assert [_entry(step, "hold", "terminate_candidate")["real_numerator"] for step in steps] == [0, -1, -2]
    assert [_entry(step, "reobserve", "terminate_candidate")["real_numerator"] for step in steps] == [2, 1, 0]
    assert obs["all_candidate_pair_support_retained"]
    assert obs["all_candidate_kernels_hermitian"]
    assert obs["all_candidate_kernels_psd_by_gram_lift"]
    assert obs["all_candidate_diagonals_match_v044_quadratic_evidence"]
    assert obs["source_relational_frontier_candidate_ids"] == ["reobserve"]
    assert obs["source_dissent_review_candidate_ids"] == ["continue"]
    assert obs["source_minority_protection_candidate_ids"] == ["hold"]

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v043_certificate"]["accepted"] = False
    assert_rejects(tampered, "source_memoryos_v043_not_accepted")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v044_certificate"]["certificate_digest"] = "substituted"
    assert_rejects(tampered, "source_memoryos_v044_certificate_digest_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v044_certificate"]["observables"][
        "source_memoryos_v043_certificate_digest"
    ] = "substituted"
    _resign_v044(tampered["source_memoryos_v044_certificate"])
    assert_rejects(tampered, "source_v044_v043_certificate_binding_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v044_certificate"]["observables"][
        "candidate_history_couplings"
    ][0]["history_coefficients"].pop("plan-history-b")
    _resign_v044(tampered["source_memoryos_v044_certificate"])
    assert_rejects(tampered, "source_memoryos_v044_coupling_history_support_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v044_certificate"]["observables"][
        "candidate_quadratic_evidence_records"
    ][0]["quadratic_evidence_trajectory"][0]["evidence_real_numerator"] = 7
    _resign_v044(tampered["source_memoryos_v044_certificate"])
    assert_rejects(
        tampered,
        "observable_required_all_candidate_diagonals_match_v044_quadratic_evidence",
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
        "source_memoryos_v043_mutated",
        "source_memoryos_v044_mutated",
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
                "candidate_pair_count": len(CANDIDATE_IDS) ** 2,
                "candidate_gram_kernel_digest": obs["candidate_gram_kernel_digest"],
                "certificate_digest": certificate["certificate_digest"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
