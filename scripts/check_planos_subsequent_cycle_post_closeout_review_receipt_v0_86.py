#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_post_closeout_review_receipt_v0_86 import (
    STATUS_READY,
    build_subsequent_cycle_post_closeout_review_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_post_closeout_review_request_v0_85 import (
    build_subsequent_cycle_post_closeout_review_request,
)
from scripts.check_planos_subsequent_cycle_closeout_receipt_v0_84 import _source_closeout_request
from runtime.kuuos_planos_subsequent_cycle_closeout_receipt_v0_84 import (
    build_subsequent_cycle_closeout_receipt,
)


def _source_review_request() -> dict:
    closeout_request = _source_closeout_request()
    closeout_receipt = build_subsequent_cycle_closeout_receipt(closeout_request).to_dict()
    return build_subsequent_cycle_post_closeout_review_request(closeout_receipt).to_dict()


def main() -> int:
    source = _source_review_request()
    result = build_subsequent_cycle_post_closeout_review_receipt(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_post_closeout_review_receipt
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["source_review_request_digest"] == source["subsequent_cycle_post_closeout_review_request"]["post_closeout_review_request_digest"]
    assert record["subsequent_cycle_post_closeout_review_requested"] is True
    assert record["subsequent_cycle_post_closeout_review_completed"] is True
    assert record["subsequent_cycle_learning_update_requested"] is False

    cases: list[dict] = []
    not_requested = deepcopy(source)
    not_requested["boundary"]["subsequent_cycle_post_closeout_review_requested"] = False
    cases.append(not_requested)
    precompleted = deepcopy(source)
    precompleted["boundary"]["subsequent_cycle_post_closeout_review_completed"] = True
    cases.append(precompleted)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_post_closeout_review_request"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_post_closeout_review_receipt(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_post_closeout_review_receipt is None

    assert build_subsequent_cycle_post_closeout_review_receipt(source, review_outcome={}).status != STATUS_READY
    print("PASS: PlanOS v0.86 subsequent-cycle post-closeout review receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
