#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_independent_test_strengthening_v0_1 import (
    build_codeai_independent_test_strengthening,
)
from scripts.build_codeai_independent_test_strengthening_fixture_v0_1 import (
    build_fixture,
)

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    spec = load("examples/codeai_independent_test_strengthening_v0_1.json")
    inputs = build_fixture(
        spec,
        load("examples/codeai_typed_error_classification_v0_1.json"),
        load("examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json"),
        load("examples/codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json"),
    )
    result = build_codeai_independent_test_strengthening(**inputs)
    if result.plan is None or result.receipt is None:
        raise SystemExit("blocked: " + ",".join(result.issues))
    repeat = build_codeai_independent_test_strengthening(**inputs)
    if repeat.plan != result.plan or repeat.receipt != result.receipt:
        raise SystemExit("non-deterministic strengthening output")
    plan = result.plan
    expected = {
        "candidate_count": spec["expected_candidate_count"],
        "typed_error_count": spec["expected_typed_error_count"],
        "obligation_count": spec["expected_obligation_count"],
        "check_kind_counts": spec["expected_check_kind_counts"],
        "category_counts": spec["expected_category_counts"],
    }
    for field, value in expected.items():
        if plan[field] != value:
            raise SystemExit(f"{field} mismatch: {plan[field]!r} != {value!r}")
    forbidden = (
        "test_generation_performed",
        "test_execution_performed",
        "ranking_performed",
        "candidate_selected",
        "verification_runner_invoked",
        "repair_executed",
        "repository_mutation_performed",
        "git_effect_performed",
        "selection_authority_granted",
        "verification_authority_granted",
        "repair_authority_granted",
        "execution_authority_granted",
        "git_authority_granted",
        "strengthened_plan_treated_as_test_success",
        "obligation_count_treated_as_candidate_quality",
        "test_coverage_treated_as_correctness_proof",
    )
    if any(plan[field] for field in forbidden):
        raise SystemExit("effect, authority, or proof inference present")
    print(
        json.dumps(
            {
                "status": result.status,
                "candidate_count": plan["candidate_count"],
                "typed_error_count": plan["typed_error_count"],
                "obligation_count": plan["obligation_count"],
                "category_counts": plan["category_counts"],
                "plan_digest": plan["codeai_independent_test_strengthening_plan_digest"],
                "receipt_digest": result.receipt[
                    "codeai_independent_test_strengthening_receipt_digest"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
