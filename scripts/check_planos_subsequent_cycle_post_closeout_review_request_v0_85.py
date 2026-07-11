#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_post_closeout_review_request_v0_85 import (
    STATUS_READY,
    build_subsequent_cycle_post_closeout_review_request,
)
from runtime.kuuos_planos_subsequent_cycle_closeout_receipt_v0_84 import (
    build_subsequent_cycle_closeout_receipt,
)
from scripts.check_planos_subsequent_cycle_closeout_receipt_v0_84 import (
    _source_closeout_request,
)


def _source_closeout_receipt() -> dict:
    return build_subsequent_cycle_closeout_receipt(_source_closeout_request()).to_dict()


def main() -> int:
    source = _source_closeout_receipt()
    result = build_subsequent_cycle_post_closeout_review_request(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_post_closeout_review_request
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["source_closeout_record_digest"] == source["subsequent_cycle_closeout_receipt"]["closeout_receipt_digest"]
    assert record["subsequent_cycle_closed"] is True
    assert record["subsequent_cycle_post_closeout_review_requested"] is True
    assert record["subsequent_cycle_post_closeout_review_completed"] is False

    cases: list[dict] = []
    not_closed = deepcopy(source)
    not_closed["boundary"]["subsequent_cycle_closed"] = False
    cases.append(not_closed)
    pre_requested = deepcopy(source)
    pre_requested["boundary"]["subsequent_cycle_post_closeout_review_requested"] = True
    cases.append(pre_requested)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_closeout_receipt"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_post_closeout_review_request(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_post_closeout_review_request is None

    assert build_subsequent_cycle_post_closeout_review_request(source, post_closeout_review_scope="").status != STATUS_READY
    assert build_subsequent_cycle_post_closeout_review_request(source, post_closeout_review_criteria={}).status != STATUS_READY
    print("PASS: PlanOS v0.85 subsequent-cycle post-closeout review request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
