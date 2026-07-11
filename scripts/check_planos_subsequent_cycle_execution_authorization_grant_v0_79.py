#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_execution_authorization_grant_v0_79 import (
    STATUS_READY,
    build_subsequent_cycle_execution_authorization_grant,
)
from scripts.check_planos_subsequent_cycle_execution_request_v0_78 import _source_start_receipt
from runtime.kuuos_planos_subsequent_cycle_execution_request_v0_78 import (
    build_subsequent_cycle_execution_request,
)


def _source_execution_request() -> dict:
    return build_subsequent_cycle_execution_request(_source_start_receipt()).to_dict()


def main() -> int:
    source = _source_execution_request()
    result = build_subsequent_cycle_execution_authorization_grant(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_execution_authorization_grant
    assert record is not None
    assert record["source_execution_request_digest"] == source["subsequent_cycle_execution_request"]["execution_request_digest"]
    assert record["subsequent_cycle_execution_requested"] is True
    assert record["subsequent_cycle_execution_authority_granted"] is True
    assert record["subsequent_cycle_execution_started"] is False

    cases: list[dict] = []
    not_requested = deepcopy(source)
    not_requested["boundary"]["subsequent_cycle_execution_requested"] = False
    cases.append(not_requested)
    pregranted = deepcopy(source)
    pregranted["boundary"]["subsequent_cycle_execution_authority_granted"] = True
    cases.append(pregranted)
    prestarted = deepcopy(source)
    prestarted["boundary"]["subsequent_cycle_execution_started"] = True
    cases.append(prestarted)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_execution_request"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_execution_authorization_grant(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_execution_authorization_grant is None

    assert build_subsequent_cycle_execution_authorization_grant(source, grant_rationale={}).status != STATUS_READY
    print("PASS: PlanOS v0.79 subsequent-cycle execution authorization grant")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
