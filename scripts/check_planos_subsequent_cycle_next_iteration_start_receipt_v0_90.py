#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_next_iteration_start_receipt_v0_90 import (
    STATUS_READY,
    build_subsequent_cycle_next_iteration_start_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_next_iteration_request_v0_89 import (
    build_subsequent_cycle_next_iteration_request,
)
from scripts.check_planos_subsequent_cycle_learning_update_receipt_v0_88 import (
    _source_learning_update_request,
)
from runtime.kuuos_planos_subsequent_cycle_learning_update_receipt_v0_88 import (
    build_subsequent_cycle_learning_update_receipt,
)


def _source_next_iteration_request() -> dict:
    learning_update_request = _source_learning_update_request()
    learning_update_receipt = build_subsequent_cycle_learning_update_receipt(
        learning_update_request
    ).to_dict()
    return build_subsequent_cycle_next_iteration_request(learning_update_receipt).to_dict()


def main() -> int:
    source = _source_next_iteration_request()
    result = build_subsequent_cycle_next_iteration_start_receipt(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_next_iteration_start_receipt
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["source_next_iteration_request_digest"] == source[
        "subsequent_cycle_next_iteration_request"
    ]["next_iteration_request_digest"]
    assert record["subsequent_cycle_next_iteration_requested"] is True
    assert record["subsequent_cycle_next_iteration_started"] is True
    assert record["subsequent_cycle_next_iteration_planning_requested"] is False

    cases: list[dict] = []
    not_requested = deepcopy(source)
    not_requested["boundary"]["subsequent_cycle_next_iteration_requested"] = False
    cases.append(not_requested)
    prestarted = deepcopy(source)
    prestarted["boundary"]["subsequent_cycle_next_iteration_started"] = True
    cases.append(prestarted)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_next_iteration_request"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_next_iteration_start_receipt(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_next_iteration_start_receipt is None

    assert build_subsequent_cycle_next_iteration_start_receipt(
        source, start_rationale={}
    ).status != STATUS_READY
    print("PASS: PlanOS v0.90 subsequent-cycle next iteration start receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
