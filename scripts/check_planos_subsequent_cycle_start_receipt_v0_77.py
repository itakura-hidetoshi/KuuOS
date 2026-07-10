#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_start_receipt_v0_77 import (
    STATUS_READY,
    build_subsequent_cycle_start_receipt,
)
from scripts.check_planos_subsequent_cycle_start_request_v0_76 import _source_admission_grant
from runtime.kuuos_planos_subsequent_cycle_start_request_v0_76 import (
    build_subsequent_cycle_start_request,
)


def _source_start_request() -> dict:
    source_grant = _source_admission_grant()
    return build_subsequent_cycle_start_request(source_grant).to_dict()


def main() -> int:
    source = _source_start_request()
    result = build_subsequent_cycle_start_receipt(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_start_receipt
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["selected_candidate_digest"] == source["selected_candidate_digest"]
    assert record["source_start_request_digest"] == source["subsequent_cycle_start_request"]["start_request_digest"]
    assert record["subsequent_cycle_start_requested"] is True
    assert record["subsequent_cycle_started"] is True
    assert record["subsequent_cycle_execution_requested"] is False

    cases: list[dict] = []
    not_requested = deepcopy(source)
    not_requested["boundary"]["subsequent_cycle_start_requested"] = False
    cases.append(not_requested)
    prestarted = deepcopy(source)
    prestarted["boundary"]["subsequent_cycle_started"] = True
    cases.append(prestarted)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_start_request"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_start_receipt(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_start_receipt is None

    assert build_subsequent_cycle_start_receipt(source, start_rationale={}).status != STATUS_READY
    print("PASS: PlanOS v0.77 subsequent-cycle start receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
