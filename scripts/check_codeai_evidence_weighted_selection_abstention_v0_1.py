#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import (
    STATUS_READY,
)
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_v0_1 import (
    build_codeai_evidence_weighted_selection_abstention,
)
from scripts.build_codeai_evidence_weighted_selection_abstention_fixture_v0_1 import (
    build_fixture,
)

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    spec = load("examples/codeai_evidence_weighted_selection_abstention_v0_1.json")
    fixture = build_fixture(
        spec,
        load("examples/codeai_independent_test_strengthening_v0_1.json"),
        load("examples/codeai_typed_error_classification_v0_1.json"),
        load("examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json"),
        load("examples/codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json"),
    )
    result = build_codeai_evidence_weighted_selection_abstention(
        strengthening_plan=fixture["strengthening_plan"],
        strengthening_receipt=fixture["strengthening_receipt"],
        evidence_packet=fixture["evidence_packet"],
        selection_request=fixture["selection_request"],
        selection_policy=fixture["selection_policy"],
    )
    if result.status != STATUS_READY or result.decision is None or result.receipt is None:
        raise SystemExit("selection blocked: " + ",".join(result.issues))
    decision = result.decision
    expected = {
        "candidate_count": spec["expected_candidate_count"],
        "evidence_record_count": spec["expected_evidence_record_count"],
        "eligible_candidate_count": spec["expected_eligible_candidate_count"],
        "decision": spec["expected_decision"],
        "selected_candidate_id": spec["expected_selected_candidate_id"],
        "selected_evidence_score": spec["expected_selected_evidence_score"],
    }
    actual = {key: decision[key] for key in expected}
    if actual != expected:
        raise SystemExit(f"selection expectation mismatch: expected={expected!r} actual={actual!r}")
    if any(
        decision[field]
        for field in (
            "test_execution_performed_by_kernel",
            "repair_executed",
            "repository_mutation_performed",
            "git_effect_performed",
            "verification_authority_granted",
            "repair_authority_granted",
            "execution_authority_granted",
            "git_authority_granted",
            "score_treated_as_probability",
            "score_treated_as_correctness_proof",
            "selection_treated_as_correctness_proof",
            "abstention_treated_as_rejection",
        )
    ):
        raise SystemExit("selection crossed a downstream effect, authority, or truth boundary")
    print(
        "CodeAI Evidence-Weighted Selection and Abstention v0.1: "
        f"{decision['candidate_count']} candidates, "
        f"{decision['evidence_record_count']} records, "
        f"decision={decision['decision']}, "
        f"selected={decision['selected_candidate_id']}"
    )


if __name__ == "__main__":
    main()
