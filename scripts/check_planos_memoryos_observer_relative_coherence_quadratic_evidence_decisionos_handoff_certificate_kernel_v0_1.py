#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    canonical_digest,
    issue_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate,
)
from runtime.kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_certificate_kernel_v0_1 import (
    issue_observer_relative_temporal_window_coherence_cocycle_composition_certificate,
)
from scripts.check_decisionos_world_conditioned_relational_deliberation_v0_6 import (
    build as build_decisionos_v06,
)
from scripts.check_planos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v043_payload,
)

HISTORY_IDS = ["plan-history-a", "plan-history-b"]
CANDIDATE_IDS = ["continue", "hold", "reobserve", "terminate_candidate"]


def couplings() -> list[dict]:
    return [
        {
            "candidate_id": "continue",
            "history_coefficients": {
                "plan-history-a": 1,
                "plan-history-b": 1,
            },
        },
        {
            "candidate_id": "hold",
            "history_coefficients": {
                "plan-history-a": 1,
                "plan-history-b": -1,
            },
        },
        {
            "candidate_id": "reobserve",
            "history_coefficients": {
                "plan-history-a": 1,
                "plan-history-b": 0,
            },
        },
        {
            "candidate_id": "terminate_candidate",
            "history_coefficients": {
                "plan-history-a": 0,
                "plan-history-b": 1,
            },
        },
    ]


def source_memoryos_v043_certificate() -> dict:
    result = issue_observer_relative_temporal_window_coherence_cocycle_composition_certificate(
        build_memoryos_v043_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_decisionos_v06_receipt() -> dict:
    result = build_decisionos_v06()
    assert result.receipt is not None, result.blockers
    return result.receipt


def _trajectory(values: list[int]) -> list[dict]:
    return [
        {
            "step_index": index,
            "dephasing_numerator": numerator,
            "evidence_real_numerator": value,
            "evidence_imag_numerator": 0,
            "evidence_denominator": 2,
            "nonnegative_psd_witness": value >= 0,
            "real_valued_hermitian_witness": True,
        }
        for index, (numerator, value) in enumerate(zip([2, 1, 0], values))
    ]


def expected_claims(memory: dict, decision: dict) -> dict:
    coupling_values = couplings()
    records = {
        item["candidate_id"]: item
        for item in decision["candidate_deliberation_records"]
    }
    evidence_values = {
        "continue": [8, 6, 4],
        "hold": [0, 2, 4],
        "reobserve": [2, 2, 2],
        "terminate_candidate": [2, 2, 2],
    }
    evidence_records: list[dict] = []
    coupling_map = {item["candidate_id"]: item for item in coupling_values}
    for candidate_id in CANDIDATE_IDS:
        values = evidence_values[candidate_id]
        evidence_records.append(
            {
                "candidate_id": candidate_id,
                "source_deliberation_classification": records[candidate_id][
                    "deliberation_classification"
                ],
                "source_relationally_reviewable": bool(
                    records[candidate_id]["relationally_reviewable"]
                ),
                "source_required_review": candidate_id
                in decision["required_review_candidate_ids"],
                "history_coefficients": coupling_map[candidate_id][
                    "history_coefficients"
                ],
                "quadratic_evidence_trajectory": _trajectory(values),
                "full_coherence_evidence_numerator": values[0],
                "fully_dephased_evidence_numerator": values[-1],
                "coherence_contrast_numerator": values[0] - values[-1],
                "candidate_retained": True,
            }
        )
    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v043_certificate_digest": memory[
                "certificate_digest"
            ],
            "source_decisionos_v06_receipt_digest": decision[
                "decisionos_relational_deliberation_receipt_digest"
            ],
            "candidate_history_couplings": coupling_values,
        }
    )
    obs = memory["observables"]
    return {
        "input_digest": input_digest,
        "source_memoryos_v043_certificate_digest": memory["certificate_digest"],
        "source_memoryos_v043_cocycle_digest": obs[
            "temporal_window_cocycle_composition_digest"
        ],
        "source_memoryos_v043_conditioned_kernel_digest": obs[
            "refined_final_kernel_digest"
        ],
        "source_decisionos_v06_receipt_digest": decision[
            "decisionos_relational_deliberation_receipt_digest"
        ],
        "retained_history_ids": HISTORY_IDS,
        "retained_decision_candidate_ids": CANDIDATE_IDS,
        "candidate_history_couplings": coupling_values,
        "candidate_quadratic_evidence_records": evidence_records,
        "positive_coherence_contrast_candidate_ids": ["continue"],
        "zero_coherence_contrast_candidate_ids": [
            "reobserve",
            "terminate_candidate",
        ],
        "negative_coherence_contrast_candidate_ids": ["hold"],
        "all_quadratic_evidence_nonnegative_by_psd": True,
        "all_quadratic_evidence_real_by_hermitian_symmetry": True,
        "all_decision_candidates_retained": True,
        "decisionos_candidate_order_preserved": True,
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
        "coherence_evidence_used_as_advisory_only": True,
        "coherence_contrast_not_used_as_scalar_utility": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v043_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def build_reference_payload() -> dict:
    memory = source_memoryos_v043_certificate()
    decision = source_decisionos_v06_receipt()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v043_certificate": memory,
        "source_decisionos_v06_receipt": decision,
        "candidate_history_couplings": couplings(),
        "claims": expected_claims(memory, decision),
    }


def assert_rejects(payload: dict, blocker: str) -> None:
    result = issue_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    certificate = issue_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate(
        payload
    )
    assert certificate["accepted"], certificate["blockers"]
    obs = certificate["observables"]
    by_id = {
        item["candidate_id"]: item
        for item in obs["candidate_quadratic_evidence_records"]
    }
    assert [
        item["evidence_real_numerator"]
        for item in by_id["continue"]["quadratic_evidence_trajectory"]
    ] == [8, 6, 4]
    assert [
        item["evidence_real_numerator"]
        for item in by_id["hold"]["quadratic_evidence_trajectory"]
    ] == [0, 2, 4]
    assert [
        item["evidence_real_numerator"]
        for item in by_id["reobserve"]["quadratic_evidence_trajectory"]
    ] == [2, 2, 2]
    assert [
        item["evidence_real_numerator"]
        for item in by_id["terminate_candidate"]["quadratic_evidence_trajectory"]
    ] == [2, 2, 2]
    assert obs["positive_coherence_contrast_candidate_ids"] == ["continue"]
    assert obs["zero_coherence_contrast_candidate_ids"] == [
        "reobserve",
        "terminate_candidate",
    ]
    assert obs["negative_coherence_contrast_candidate_ids"] == ["hold"]
    assert obs["source_relational_frontier_candidate_ids"] == ["reobserve"]
    assert obs["source_required_review_candidate_ids"] == [
        "continue",
        "hold",
        "reobserve",
    ]
    assert obs["source_dissent_review_candidate_ids"] == ["continue"]
    assert obs["source_minority_protection_candidate_ids"] == ["hold"]
    assert obs["all_quadratic_evidence_nonnegative_by_psd"]
    assert obs["all_quadratic_evidence_real_by_hermitian_symmetry"]
    assert obs["all_decision_candidates_retained"]
    assert obs["coherence_contrast_not_used_as_scalar_utility"]

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v043_certificate"]["accepted"] = False
    assert_rejects(tampered, "source_memoryos_v043_not_accepted")

    tampered = copy.deepcopy(payload)
    tampered["source_decisionos_v06_receipt"][
        "decisionos_relational_deliberation_receipt_digest"
    ] = "substituted"
    assert_rejects(tampered, "source_decisionos_v06_digest_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["candidate_history_couplings"][0]["history_coefficients"].pop(
        "plan-history-b"
    )
    assert_rejects(tampered, "candidate_history_coefficient_support_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["candidate_history_couplings"][0]["history_coefficients"] = {
        "plan-history-a": 0,
        "plan-history-b": 0,
    }
    assert_rejects(tampered, "candidate_history_coupling_zero_vector_forbidden")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v043_certificate"]["observables"][
        "refined_final_trajectory"
    ][0]["kernel_entries"][1]["real_numerator"] = 999
    assert_rejects(tampered, "source_memoryos_v043_hermitian_entry_mismatch")

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
                "continue_evidence": [8, 6, 4],
                "hold_evidence": [0, 2, 4],
                "certificate_digest": certificate["certificate_digest"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
