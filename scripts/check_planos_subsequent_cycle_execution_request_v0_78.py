#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_execution_request_v0_78 import (
    STATUS_READY,
    build_subsequent_cycle_execution_request,
)
from scripts.check_planos_subsequent_cycle_start_receipt_v0_77 import _source_start_request
from runtime.kuuos_planos_subsequent_cycle_start_receipt_v0_77 import (
    build_subsequent_cycle_start_receipt,
)


def _source_start_receipt() -> dict:
    source_request = _source_start_request()
    return build_subsequent_cycle_start_receipt(source_request).to_dict()


def main() -> int:
    source = _source_start_receipt()
    result = build_subsequent_cycle_execution_request(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_execution_request
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["selected_candidate_digest"] == source["selected_candidate_digest"]
    assert record["source_start_record_digest"] == source["subsequent_cycle_start_receipt"]["subsequent_cycle_start_receipt_digest"]
    assert record["subsequent_cycle_started"] is True
    assert record["subsequent_cycle_execution_requested"] is True
    assert record["subsequent_cycle_execution_authority_granted"] is False
    assert record["subsequent_cycle_execution_started"] is False

    cases: list[dict] = []
    not_started = deepcopy(source)
    not_started["boundary"]["subsequent_cycle_started"] = False
    cases.append(not_started)
    prerequested = deepcopy(source)
    prerequested["boundary"]["subsequent_cycle_execution_requested"] = True
    cases.append(prerequested)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_start_receipt"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_execution_request(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_execution_request is None

    assert build_subsequent_cycle_execution_request(source, execution_scope="").status != STATUS_READY
    assert build_subsequent_cycle_execution_request(source, execution_constraints={}).status != STATUS_READY
    print("PASS: PlanOS v0.78 subsequent-cycle execution request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
