#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_admission_request_v0_74 import (
    STATUS_READY,
    build_subsequent_cycle_admission_request,
)
from scripts.check_planos_subsequent_cycle_candidate_selection_receipt_v0_73 import _source_selection_request
from runtime.kuuos_planos_subsequent_cycle_candidate_selection_receipt_v0_73 import (
    build_subsequent_cycle_candidate_selection_receipt,
)


def _source_selection_receipt() -> dict:
    source_request = _source_selection_request()
    return build_subsequent_cycle_candidate_selection_receipt(
        source_request,
        selected_candidate_id=source_request["eligible_candidate_ids"][0],
    ).to_dict()


def main() -> int:
    source = _source_selection_receipt()
    result = build_subsequent_cycle_admission_request(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_admission_request
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["selected_candidate_digest"] == source["selected_candidate_digest"]
    assert record["subsequent_cycle_admission_requested"] is True
    assert record["subsequent_cycle_admission_granted"] is False
    assert record["subsequent_cycle_started"] is False

    cases: list[dict] = []
    not_selected = deepcopy(source)
    not_selected["boundary"]["subsequent_cycle_candidate_selected"] = False
    cases.append(not_selected)
    preadmitted = deepcopy(source)
    preadmitted["boundary"]["subsequent_cycle_admission_requested"] = True
    cases.append(preadmitted)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_candidate_selection_receipt"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_admission_request(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_admission_request is None

    assert build_subsequent_cycle_admission_request(source, admission_scope="").status != STATUS_READY
    assert build_subsequent_cycle_admission_request(source, admission_constraints={}).status != STATUS_READY
    print("PASS: PlanOS v0.74 subsequent-cycle admission request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
