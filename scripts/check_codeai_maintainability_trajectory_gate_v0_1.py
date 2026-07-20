#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_maintainability_trajectory_gate_schema_v0_1 import (
    DECISION_DIGEST_FIELD,
    GATE_ADMITTED,
    RECEIPT_DIGEST_FIELD,
    STATUS_READY,
    seal,
)
from runtime.kuuos_codeai_maintainability_trajectory_gate_v0_1 import (
    build_codeai_maintainability_trajectory_gate,
)
from scripts.build_codeai_maintainability_trajectory_gate_fixture_v0_1 import (
    build_fixture,
)

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    spec = load("examples/codeai_maintainability_trajectory_gate_v0_1.json")
    fixture = build_fixture(
        spec,
        load("examples/codeai_evidence_weighted_selection_abstention_v0_1.json"),
        load("examples/codeai_independent_test_strengthening_v0_1.json"),
        load("examples/codeai_version_bound_repair_memory_v0_1.json"),
        load("examples/codeai_typed_error_classification_v0_1.json"),
        load("examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json"),
        load(
            "examples/codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json"
        ),
    )
    result = build_codeai_maintainability_trajectory_gate(**fixture)
    if result.status != STATUS_READY or result.decision is None or result.receipt is None:
        raise SystemExit(
            "maintainability trajectory gate blocked: " + ",".join(result.issues)
        )
    decision = result.decision
    receipt = result.receipt
    expected = {
        "axis_count": spec["expected_axis_count"],
        "improved_axis_count": spec["expected_improved_axis_count"],
        "total_regression": spec["expected_total_regression"],
        "gate_decision": spec["expected_gate_decision"],
    }
    actual = {key: decision[key] for key in expected}
    if actual != expected:
        raise SystemExit(
            "maintainability trajectory fixture mismatch: "
            + json.dumps({"expected": expected, "actual": actual}, sort_keys=True)
        )
    if decision["gate_decision"] != GATE_ADMITTED:
        raise SystemExit("reference candidate was not admitted")
    if decision["exceeded_axis_count"] != 0:
        raise SystemExit("reference candidate unexpectedly exceeded an axis limit")
    if decision[DECISION_DIGEST_FIELD] != seal(
        decision, DECISION_DIGEST_FIELD
    )[DECISION_DIGEST_FIELD]:
        raise SystemExit("maintainability decision seal is not deterministic")
    if receipt[RECEIPT_DIGEST_FIELD] != seal(
        receipt, RECEIPT_DIGEST_FIELD
    )[RECEIPT_DIGEST_FIELD]:
        raise SystemExit("maintainability receipt seal is not deterministic")
    for field in (
        "memory_hint_used_as_threshold_waiver",
        "historical_repair_outcome_used_as_probability",
        "test_execution_performed_by_kernel",
        "repair_executed",
        "repository_mutation_performed",
        "git_effect_performed",
        "selection_authority_granted",
        "verification_authority_granted",
        "repair_authority_granted",
        "execution_authority_granted",
        "git_authority_granted",
        "bounded_measurement_treated_as_future_proof",
        "maintainability_gate_treated_as_correctness_proof",
        "maintainability_gate_treated_as_probability",
        "held_treated_as_rejection",
    ):
        if decision[field] is not False:
            raise SystemExit("maintainability boundary violated: " + field)
    print(
        json.dumps(
            {
                "status": result.status,
                "gate_decision": decision["gate_decision"],
                "selected_candidate_id": decision["selected_candidate_id"],
                "axis_count": decision["axis_count"],
                "improved_axis_count": decision["improved_axis_count"],
                "total_regression": decision["total_regression"],
                "memory_hint_available": decision["memory_hint_available"],
                "decision_digest": decision[DECISION_DIGEST_FIELD],
                "receipt_digest": receipt[RECEIPT_DIGEST_FIELD],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
