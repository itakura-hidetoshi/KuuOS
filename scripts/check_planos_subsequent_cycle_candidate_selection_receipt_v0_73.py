#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_candidate_selection_receipt_v0_73 import (
    STATUS_READY,
    build_subsequent_cycle_candidate_selection_receipt,
)


def _source() -> dict:
    ids = ["repair-route::continuity", "repair-route::refinement"]
    digests = ["candidate-digest-continuity", "candidate-digest-refinement"]
    record = {
        "selection_request_digest": "selection-request-digest-v0-72",
        "candidate_set_digest": "candidate-set-digest",
        "evaluation_set_digest": "evaluation-set-digest",
        "review_set_digest": "review-set-digest",
        "selection_scope": "subsequent_cycle_candidate_selection_only",
        "selection_criteria_digest": "selection-criteria-digest",
    }
    return {
        "version": "kuuos_planos_subsequent_cycle_candidate_selection_request_v0_72",
        "status": "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_REQUEST_READY",
        "receipt_digest": "selection-request-receipt-digest-v0-72",
        "candidate_set_digest": record["candidate_set_digest"],
        "evaluation_set_digest": record["evaluation_set_digest"],
        "review_set_digest": record["review_set_digest"],
        "eligible_candidate_ids": ids,
        "eligible_candidate_digests": digests,
        "selection_scope": record["selection_scope"],
        "selection_criteria_digest": record["selection_criteria_digest"],
        "subsequent_cycle_candidate_selection_request": record,
        "boundary": {
            "subsequent_cycle_selection_authority_granted": True,
            "subsequent_cycle_candidate_selection_requested": True,
            "subsequent_cycle_candidate_selected": False,
            "subsequent_cycle_admission_requested": False,
        },
    }


def main() -> int:
    source = _source()
    result = build_subsequent_cycle_candidate_selection_receipt(
        source,
        selected_candidate_id="repair-route::continuity",
    )
    assert result.status == STATUS_READY, result.blockers
    assert result.selected_candidate_id == "repair-route::continuity"
    assert result.selected_candidate_digest == "candidate-digest-continuity"
    record = result.subsequent_cycle_candidate_selection_receipt
    assert record is not None
    assert record["subsequent_cycle_candidate_selected"] is True
    assert record["subsequent_cycle_admission_requested"] is False

    unknown = build_subsequent_cycle_candidate_selection_receipt(source, selected_candidate_id="unknown")
    assert unknown.status != STATUS_READY
    assert "selected_candidate_not_eligible" in unknown.blockers

    preselected = deepcopy(source)
    preselected["boundary"]["subsequent_cycle_candidate_selected"] = True
    blocked = build_subsequent_cycle_candidate_selection_receipt(
        preselected, selected_candidate_id="repair-route::continuity"
    )
    assert blocked.status != STATUS_READY

    no_rationale = build_subsequent_cycle_candidate_selection_receipt(
        source,
        selected_candidate_id="repair-route::continuity",
        selection_rationale={},
    )
    assert no_rationale.status != STATUS_READY
    assert "selection_rationale_missing" in no_rationale.blockers

    print("PASS: PlanOS v0.73 subsequent-cycle candidate selection receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
