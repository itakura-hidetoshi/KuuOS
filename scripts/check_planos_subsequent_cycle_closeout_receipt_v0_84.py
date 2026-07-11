#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_closeout_receipt_v0_84 import (
    STATUS_READY,
    build_subsequent_cycle_closeout_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_closeout_request_v0_83 import (
    build_subsequent_cycle_closeout_request,
)
from scripts.check_planos_subsequent_cycle_execution_completion_receipt_v0_82 import (
    _source_completion_request,
)
from runtime.kuuos_planos_subsequent_cycle_execution_completion_receipt_v0_82 import (
    build_subsequent_cycle_execution_completion_receipt,
)


def _source_closeout_request() -> dict:
    completion_request = _source_completion_request()
    completion_receipt = build_subsequent_cycle_execution_completion_receipt(completion_request).to_dict()
    return build_subsequent_cycle_closeout_request(completion_receipt).to_dict()


def main() -> int:
    source = _source_closeout_request()
    result = build_subsequent_cycle_closeout_receipt(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_closeout_receipt
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["selected_candidate_digest"] == source["selected_candidate_digest"]
    assert record["source_closeout_request_digest"] == source["subsequent_cycle_closeout_request"]["closeout_request_digest"]
    assert record["subsequent_cycle_closeout_requested"] is True
    assert record["subsequent_cycle_closed"] is True
    assert record["subsequent_cycle_post_closeout_review_requested"] is False

    cases: list[dict] = []
    not_requested = deepcopy(source)
    not_requested["boundary"]["subsequent_cycle_closeout_requested"] = False
    cases.append(not_requested)
    preclosed = deepcopy(source)
    preclosed["boundary"]["subsequent_cycle_closed"] = True
    cases.append(preclosed)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_closeout_request"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_closeout_receipt(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_closeout_receipt is None

    assert build_subsequent_cycle_closeout_receipt(source, closeout_rationale={}).status != STATUS_READY
    print("PASS: PlanOS v0.84 subsequent-cycle closeout receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
