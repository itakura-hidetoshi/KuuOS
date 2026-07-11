#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_execution_completion_receipt_v0_82 import (
    STATUS_READY,
    build_subsequent_cycle_execution_completion_receipt,
)
from scripts.check_planos_subsequent_cycle_execution_start_receipt_v0_80 import _source_authorization_grant
from runtime.kuuos_planos_subsequent_cycle_execution_start_receipt_v0_80 import (
    build_subsequent_cycle_execution_start_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_execution_completion_request_v0_81 import (
    build_subsequent_cycle_execution_completion_request,
)


def _source_completion_request() -> dict:
    source_grant = _source_authorization_grant()
    start_receipt = build_subsequent_cycle_execution_start_receipt(source_grant).to_dict()
    return build_subsequent_cycle_execution_completion_request(start_receipt).to_dict()


def main() -> int:
    source = _source_completion_request()
    result = build_subsequent_cycle_execution_completion_receipt(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_execution_completion_receipt
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["selected_candidate_digest"] == source["selected_candidate_digest"]
    assert record["source_completion_request_digest"] == source["subsequent_cycle_execution_completion_request"]["execution_completion_request_digest"]
    assert record["subsequent_cycle_execution_completion_requested"] is True
    assert record["subsequent_cycle_execution_completed"] is True
    assert record["subsequent_cycle_closeout_requested"] is False

    cases: list[dict] = []
    not_requested = deepcopy(source)
    not_requested["boundary"]["subsequent_cycle_execution_completion_requested"] = False
    cases.append(not_requested)
    precompleted = deepcopy(source)
    precompleted["boundary"]["subsequent_cycle_execution_completed"] = True
    cases.append(precompleted)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_execution_completion_request"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_execution_completion_receipt(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_execution_completion_receipt is None

    assert build_subsequent_cycle_execution_completion_receipt(source, completion_rationale={}).status != STATUS_READY
    print("PASS: PlanOS v0.82 subsequent-cycle execution completion receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
