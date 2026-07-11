#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_learning_update_receipt_v0_88 import (
    STATUS_READY,
    build_subsequent_cycle_learning_update_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_learning_update_request_v0_87 import (
    build_subsequent_cycle_learning_update_request,
)
from scripts.check_planos_subsequent_cycle_post_closeout_review_receipt_v0_86 import (
    _source_review_request,
)
from runtime.kuuos_planos_subsequent_cycle_post_closeout_review_receipt_v0_86 import (
    build_subsequent_cycle_post_closeout_review_receipt,
)


def _source_learning_update_request() -> dict:
    review_request = _source_review_request()
    review_receipt = build_subsequent_cycle_post_closeout_review_receipt(review_request).to_dict()
    return build_subsequent_cycle_learning_update_request(review_receipt).to_dict()


def main() -> int:
    source = _source_learning_update_request()
    result = build_subsequent_cycle_learning_update_receipt(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_learning_update_receipt
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["source_learning_update_request_digest"] == source["subsequent_cycle_learning_update_request"]["learning_update_request_digest"]
    assert record["subsequent_cycle_learning_update_requested"] is True
    assert record["subsequent_cycle_learning_update_applied"] is True
    assert record["subsequent_cycle_next_iteration_requested"] is False

    cases: list[dict] = []
    not_requested = deepcopy(source)
    not_requested["boundary"]["subsequent_cycle_learning_update_requested"] = False
    cases.append(not_requested)
    preapplied = deepcopy(source)
    preapplied["boundary"]["subsequent_cycle_learning_update_applied"] = True
    cases.append(preapplied)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_learning_update_request"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_learning_update_receipt(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_learning_update_receipt is None

    assert build_subsequent_cycle_learning_update_receipt(source, learning_update_result={}).status != STATUS_READY
    print("PASS: PlanOS v0.88 subsequent-cycle learning update receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
