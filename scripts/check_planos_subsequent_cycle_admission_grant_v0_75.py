#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_admission_grant_v0_75 import (
    STATUS_READY,
    build_subsequent_cycle_admission_grant,
)
from runtime.kuuos_planos_subsequent_cycle_admission_request_v0_74 import (
    build_subsequent_cycle_admission_request,
)
from scripts.check_planos_subsequent_cycle_admission_request_v0_74 import (
    _source_selection_receipt,
)


def _source_admission_request() -> dict:
    return build_subsequent_cycle_admission_request(_source_selection_receipt()).to_dict()


def main() -> int:
    source = _source_admission_request()
    result = build_subsequent_cycle_admission_grant(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_admission_grant
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["selected_candidate_digest"] == source["selected_candidate_digest"]
    assert record["subsequent_cycle_admission_requested"] is True
    assert record["subsequent_cycle_admission_granted"] is True
    assert record["subsequent_cycle_started"] is False

    cases: list[dict] = []
    not_requested = deepcopy(source)
    not_requested["boundary"]["subsequent_cycle_admission_requested"] = False
    cases.append(not_requested)
    pregranted = deepcopy(source)
    pregranted["boundary"]["subsequent_cycle_admission_granted"] = True
    cases.append(pregranted)
    prestarted = deepcopy(source)
    prestarted["boundary"]["subsequent_cycle_started"] = True
    cases.append(prestarted)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_admission_request"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_admission_grant(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_admission_grant is None

    assert build_subsequent_cycle_admission_grant(source, grant_rationale={}).status != STATUS_READY
    print("PASS: PlanOS v0.75 subsequent-cycle admission grant")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
