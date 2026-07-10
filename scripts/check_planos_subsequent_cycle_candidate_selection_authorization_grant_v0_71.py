#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from scripts.check_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70 import _source_review_receipt
from runtime.kuuos_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70 import build_subsequent_cycle_candidate_selection_authorization_request
from runtime.kuuos_planos_subsequent_cycle_candidate_selection_authorization_grant_v0_71 import (
    STATUS_READY,
    build_subsequent_cycle_candidate_selection_authorization_grant,
)


def _source_request() -> dict:
    return build_subsequent_cycle_candidate_selection_authorization_request(_source_review_receipt()).to_dict()


def main() -> int:
    source = _source_request()
    result = build_subsequent_cycle_candidate_selection_authorization_grant(source)
    assert result.status == STATUS_READY, result.blockers
    assert result.blockers == []
    assert result.selection_eligible_count == 2
    assert len(result.eligible_candidate_ids) == 2
    record = result.subsequent_cycle_candidate_selection_authorization_grant
    assert record is not None
    assert record["source_authorization_request_receipt_digest"] == source["receipt_digest"]
    assert record["source_authorization_request_digest"] == source["subsequent_cycle_candidate_selection_authorization_request"]["authorization_request_digest"]
    assert record["subsequent_cycle_candidate_selection_authorization_requested"] is True
    assert record["subsequent_cycle_selection_authority_granted"] is True
    assert record["subsequent_cycle_candidate_selection_requested"] is False
    assert record["subsequent_cycle_candidate_selected"] is False
    assert record["subsequent_cycle_admission_requested"] is False

    cases = []
    pregranted = deepcopy(source)
    pregranted["boundary"]["subsequent_cycle_selection_authority_granted"] = True
    cases.append(pregranted)
    prerequested = deepcopy(source)
    prerequested["boundary"]["subsequent_cycle_candidate_selection_requested"] = True
    cases.append(prerequested)
    tampered = deepcopy(source)
    tampered["authorization_constraints_digest"] = "tampered"
    cases.append(tampered)
    empty = deepcopy(source)
    empty["selection_eligible_count"] = 0
    empty["eligible_candidate_ids"] = []
    empty["eligible_candidate_digests"] = []
    cases.append(empty)
    missing_digest = deepcopy(source)
    missing_digest["subsequent_cycle_candidate_selection_authorization_request"]["authorization_request_digest"] = ""
    cases.append(missing_digest)

    for case in cases:
        blocked = build_subsequent_cycle_candidate_selection_authorization_grant(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_candidate_selection_authorization_grant is None

    print("PASS: PlanOS v0.71 subsequent-cycle candidate selection authorization grant")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
