#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_execution_completion_request_v0_81 import (
    STATUS_READY,
    build_subsequent_cycle_execution_completion_request,
)
from scripts.check_planos_subsequent_cycle_execution_start_receipt_v0_80 import _source_authorization_grant
from runtime.kuuos_planos_subsequent_cycle_execution_start_receipt_v0_80 import (
    build_subsequent_cycle_execution_start_receipt,
)


def _source_execution_start_receipt() -> dict:
    source_grant = _source_authorization_grant()
    return build_subsequent_cycle_execution_start_receipt(source_grant).to_dict()


def main() -> int:
    source = _source_execution_start_receipt()
    result = build_subsequent_cycle_execution_completion_request(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_execution_completion_request
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["selected_candidate_digest"] == source["selected_candidate_digest"]
    assert record["source_execution_start_record_digest"] == source["subsequent_cycle_execution_start_receipt"]["execution_start_receipt_digest"]
    assert record["subsequent_cycle_execution_started"] is True
    assert record["subsequent_cycle_execution_completion_requested"] is True
    assert record["subsequent_cycle_execution_completed"] is False

    cases: list[dict] = []
    not_started = deepcopy(source)
    not_started["boundary"]["subsequent_cycle_execution_started"] = False
    cases.append(not_started)
    precompleted = deepcopy(source)
    precompleted["boundary"]["subsequent_cycle_execution_completed"] = True
    cases.append(precompleted)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_execution_start_receipt"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_execution_completion_request(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_execution_completion_request is None

    assert build_subsequent_cycle_execution_completion_request(source, completion_scope="").status != STATUS_READY
    assert build_subsequent_cycle_execution_completion_request(source, completion_constraints={}).status != STATUS_READY
    print("PASS: PlanOS v0.81 subsequent-cycle execution completion request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
