#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from scripts.check_planos_subsequent_cycle_candidate_selection_authorization_grant_v0_71 import _source_authorization_request
from runtime.kuuos_planos_subsequent_cycle_candidate_selection_authorization_grant_v0_71 import build_subsequent_cycle_candidate_selection_authorization_grant
from runtime.kuuos_planos_subsequent_cycle_candidate_selection_request_v0_72 import STATUS_READY, build_subsequent_cycle_candidate_selection_request


def _source_grant() -> dict:
    return build_subsequent_cycle_candidate_selection_authorization_grant(_source_authorization_request()).to_dict()


def main() -> int:
    source = _source_grant()
    result = build_subsequent_cycle_candidate_selection_request(source)
    assert result.status == STATUS_READY, result.blockers
    assert result.blockers == []
    assert result.selection_eligible_count == 2
    assert len(result.eligible_candidate_ids) == 2
    record = result.subsequent_cycle_candidate_selection_request
    assert record is not None
    assert record["subsequent_cycle_selection_authority_granted"] is True
    assert record["subsequent_cycle_candidate_selection_requested"] is True
    assert record["subsequent_cycle_candidate_selected"] is False
    assert record["subsequent_cycle_admission_requested"] is False
    assert record["selection_request_digest"]

    cases = []
    preselected = deepcopy(source)
    preselected["boundary"]["subsequent_cycle_candidate_selected"] = True
    cases.append(preselected)
    missing_grant = deepcopy(source)
    missing_grant["subsequent_cycle_candidate_selection_authorization_grant"] = None
    cases.append(missing_grant)
    tampered_ids = deepcopy(source)
    tampered_ids["eligible_candidate_ids"] = tampered_ids["eligible_candidate_ids"][:-1]
    cases.append(tampered_ids)
    empty_criteria = build_subsequent_cycle_candidate_selection_request(source, selection_criteria={})
    assert empty_criteria.status != STATUS_READY
    for case in cases:
        blocked = build_subsequent_cycle_candidate_selection_request(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_candidate_selection_request is None

    print("PASS: PlanOS v0.72 subsequent-cycle candidate selection request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
