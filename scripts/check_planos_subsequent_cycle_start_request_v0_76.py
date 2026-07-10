#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_start_request_v0_76 import (
    STATUS_READY,
    build_subsequent_cycle_start_request,
)
from runtime.kuuos_planos_subsequent_cycle_admission_grant_v0_75 import (
    build_subsequent_cycle_admission_grant,
)
from scripts.check_planos_subsequent_cycle_admission_request_v0_74 import (
    _source_selection_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_admission_request_v0_74 import (
    build_subsequent_cycle_admission_request,
)


def _source_admission_grant() -> dict:
    request = build_subsequent_cycle_admission_request(_source_selection_receipt()).to_dict()
    return build_subsequent_cycle_admission_grant(request).to_dict()


def main() -> int:
    source = _source_admission_grant()
    result = build_subsequent_cycle_start_request(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_start_request
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["selected_candidate_digest"] == source["selected_candidate_digest"]
    assert record["subsequent_cycle_admission_granted"] is True
    assert record["subsequent_cycle_start_requested"] is True
    assert record["subsequent_cycle_started"] is False

    cases: list[dict] = []
    not_granted = deepcopy(source)
    not_granted["boundary"]["subsequent_cycle_admission_granted"] = False
    cases.append(not_granted)
    prestarted = deepcopy(source)
    prestarted["boundary"]["subsequent_cycle_started"] = True
    cases.append(prestarted)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_admission_grant"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_start_request(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_start_request is None

    assert build_subsequent_cycle_start_request(source, start_scope="").status != STATUS_READY
    assert build_subsequent_cycle_start_request(source, start_constraints={}).status != STATUS_READY
    print("PASS: PlanOS v0.76 subsequent-cycle start request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
