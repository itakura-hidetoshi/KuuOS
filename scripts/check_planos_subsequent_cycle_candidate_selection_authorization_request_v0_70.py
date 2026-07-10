#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_candidate_review_receipt_v0_69 import (
    build_subsequent_cycle_candidate_review_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70 import (
    STATUS_READY,
    build_subsequent_cycle_candidate_selection_authorization_request,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67 import (
    build_subsequent_cycle_candidate_evaluation_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_review_request_v0_68 import (
    build_subsequent_cycle_candidate_review_request,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66 import (
    build_subsequent_cycle_candidate_set_materialization_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_generation_start_receipt_v0_65 import (
    build_subsequent_cycle_candidate_generation_start_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_replan_request_v0_64 import (
    build_subsequent_cycle_replan_request,
)
from runtime.kuuos_planos_next_cycle_closeout_receipt_v0_63 import build_next_cycle_closeout_receipt


def _source_review_receipt():
    closeout = build_next_cycle_closeout_receipt().to_dict()
    replan = build_subsequent_cycle_replan_request(closeout).to_dict()
    generation = build_subsequent_cycle_candidate_generation_start_receipt(replan).to_dict()
    materialized = build_subsequent_cycle_candidate_set_materialization_receipt(generation).to_dict()
    evaluated = build_subsequent_cycle_candidate_evaluation_receipt(materialized).to_dict()
    requested = build_subsequent_cycle_candidate_review_request(evaluated).to_dict()
    specs = [
        {
            "candidate_id": evaluation["candidate_id"],
            "review_disposition": disposition,
            "review_rationale_digest": f"rationale::{evaluation['candidate_id']}",
            "review_constraints_digest": f"constraints::{evaluation['candidate_id']}",
        }
        for evaluation, disposition in zip(
            evaluated["evaluations"],
            ("eligible", "eligible_with_conditions", "deferred"),
            strict=True,
        )
    ]
    return build_subsequent_cycle_candidate_review_receipt(requested, evaluated, specs).to_dict()


def main() -> int:
    source = _source_review_receipt()
    result = build_subsequent_cycle_candidate_selection_authorization_request(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    assert result.selection_eligible_count == 2
    assert len(result.eligible_candidate_ids) == 2
    record = result.subsequent_cycle_candidate_selection_authorization_request
    assert record is not None
    assert record["subsequent_cycle_candidate_selection_authorization_requested"] is True
    assert record["subsequent_cycle_selection_authority_granted"] is False
    assert record["subsequent_cycle_candidate_selection_requested"] is False
    assert record["subsequent_cycle_candidate_selected"] is False
    assert record["subsequent_cycle_admission_requested"] is False

    cases = []
    missing_review = deepcopy(source)
    missing_review["review_outcomes"] = missing_review["review_outcomes"][:-1]
    cases.append(missing_review)

    tampered_digest = deepcopy(source)
    tampered_digest["review_set_digest"] = "tampered"
    cases.append(tampered_digest)

    no_eligible = deepcopy(source)
    for outcome in no_eligible["review_outcomes"]:
        outcome["selection_eligible"] = False
    no_eligible["selection_eligible_count"] = 0
    cases.append(no_eligible)

    pregranted = deepcopy(source)
    pregranted["boundary"]["subsequent_cycle_selection_authority_granted"] = True
    cases.append(pregranted)

    preselected = deepcopy(source)
    preselected["boundary"]["subsequent_cycle_candidate_selected"] = True
    cases.append(preselected)

    for case in cases:
        blocked = build_subsequent_cycle_candidate_selection_authorization_request(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_candidate_selection_authorization_request is None

    print("PASS: PlanOS v0.70 subsequent-cycle candidate selection authorization request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
