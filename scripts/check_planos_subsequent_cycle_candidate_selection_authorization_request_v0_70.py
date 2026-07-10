#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from scripts.check_planos_subsequent_cycle_candidate_review_receipt_v0_69 import (
    _build,
    _ready_candidate_review_sources,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70 import (
    STATUS_READY,
    build_subsequent_cycle_candidate_selection_authorization_request,
)


def _source_review_receipt() -> dict:
    request, evaluation = _ready_candidate_review_sources()
    return _build(request, evaluation)


def main() -> int:
    source = _source_review_receipt()
    result = build_subsequent_cycle_candidate_selection_authorization_request(source)
    assert result.status == STATUS_READY, result.blockers
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
