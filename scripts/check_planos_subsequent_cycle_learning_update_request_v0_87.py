#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_learning_update_request_v0_87 import (
    STATUS_READY,
    build_subsequent_cycle_learning_update_request,
)
from runtime.kuuos_planos_subsequent_cycle_post_closeout_review_receipt_v0_86 import (
    build_subsequent_cycle_post_closeout_review_receipt,
)
from scripts.check_planos_subsequent_cycle_post_closeout_review_receipt_v0_86 import (
    _source_review_request,
)


def _source_review_receipt() -> dict:
    review_request = _source_review_request()
    return build_subsequent_cycle_post_closeout_review_receipt(review_request).to_dict()


def main() -> int:
    source = _source_review_receipt()
    result = build_subsequent_cycle_learning_update_request(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_learning_update_request
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["source_review_record_digest"] == source["subsequent_cycle_post_closeout_review_receipt"]["post_closeout_review_receipt_digest"]
    assert record["subsequent_cycle_learning_update_requested"] is True
    assert record["subsequent_cycle_learning_update_applied"] is False

    cases: list[dict] = []
    incomplete = deepcopy(source)
    incomplete["boundary"]["subsequent_cycle_post_closeout_review_completed"] = False
    cases.append(incomplete)
    prerequested = deepcopy(source)
    prerequested["boundary"]["subsequent_cycle_learning_update_requested"] = True
    cases.append(prerequested)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_post_closeout_review_receipt"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_learning_update_request(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_learning_update_request is None

    assert build_subsequent_cycle_learning_update_request(source, learning_update_scope="").status != STATUS_READY
    assert build_subsequent_cycle_learning_update_request(source, learning_update_constraints={}).status != STATUS_READY
    print("PASS: PlanOS v0.87 subsequent-cycle learning update request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())