#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_execution_start_receipt_v0_80 import (
    STATUS_READY,
    build_subsequent_cycle_execution_start_receipt,
)
from scripts.check_planos_subsequent_cycle_execution_authorization_grant_v0_79 import (
    _source_execution_request,
)
from runtime.kuuos_planos_subsequent_cycle_execution_authorization_grant_v0_79 import (
    build_subsequent_cycle_execution_authorization_grant,
)


def _source_execution_authorization_grant() -> dict:
    source_request = _source_execution_request()
    return build_subsequent_cycle_execution_authorization_grant(source_request).to_dict()


def main() -> int:
    source = _source_execution_authorization_grant()
    result = build_subsequent_cycle_execution_start_receipt(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_execution_start_receipt
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["selected_candidate_digest"] == source["selected_candidate_digest"]
    assert record["subsequent_cycle_execution_requested"] is True
    assert record["subsequent_cycle_execution_authority_granted"] is True
    assert record["subsequent_cycle_execution_started"] is True
    assert record["subsequent_cycle_execution_completed"] is False

    cases: list[dict] = []
    no_authority = deepcopy(source)
    no_authority["boundary"]["subsequent_cycle_execution_authority_granted"] = False
    cases.append(no_authority)
    prestarted = deepcopy(source)
    prestarted["boundary"]["subsequent_cycle_execution_started"] = True
    cases.append(prestarted)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_execution_authorization_grant"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_execution_start_receipt(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_execution_start_receipt is None

    assert build_subsequent_cycle_execution_start_receipt(
        source, execution_start_rationale={}
    ).status != STATUS_READY
    print("PASS: PlanOS v0.80 subsequent-cycle execution start receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
