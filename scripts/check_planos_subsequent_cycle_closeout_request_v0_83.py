#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_closeout_request_v0_83 import (
    STATUS_READY,
    build_subsequent_cycle_closeout_request,
)
from scripts.check_planos_subsequent_cycle_execution_completion_request_v0_81 import _source_execution_start_receipt
from runtime.kuuos_planos_subsequent_cycle_execution_completion_request_v0_81 import build_subsequent_cycle_execution_completion_request
from runtime.kuuos_planos_subsequent_cycle_execution_completion_receipt_v0_82 import build_subsequent_cycle_execution_completion_receipt


def _source_completion_receipt() -> dict:
    start_receipt = _source_execution_start_receipt()
    request = build_subsequent_cycle_execution_completion_request(start_receipt).to_dict()
    return build_subsequent_cycle_execution_completion_receipt(request).to_dict()


def main() -> int:
    source = _source_completion_receipt()
    result = build_subsequent_cycle_closeout_request(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_closeout_request
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["source_execution_completion_record_digest"] == source["subsequent_cycle_execution_completion_receipt"]["execution_completion_receipt_digest"]
    assert record["subsequent_cycle_execution_completed"] is True
    assert record["subsequent_cycle_closeout_requested"] is True
    assert record["subsequent_cycle_closed"] is False

    cases: list[dict] = []
    not_completed = deepcopy(source)
    not_completed["boundary"]["subsequent_cycle_execution_completed"] = False
    cases.append(not_completed)
    precloseout = deepcopy(source)
    precloseout["boundary"]["subsequent_cycle_closeout_requested"] = True
    cases.append(precloseout)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_execution_completion_receipt"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_closeout_request(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_closeout_request is None

    assert build_subsequent_cycle_closeout_request(source, closeout_scope="").status != STATUS_READY
    assert build_subsequent_cycle_closeout_request(source, closeout_constraints={}).status != STATUS_READY
    print("PASS: PlanOS v0.83 subsequent-cycle closeout request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
