#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_subsequent_cycle_next_iteration_request_v0_89 import (
    STATUS_READY,
    build_subsequent_cycle_next_iteration_request,
)
from runtime.kuuos_planos_subsequent_cycle_learning_update_receipt_v0_88 import (
    build_subsequent_cycle_learning_update_receipt,
)
from scripts.check_planos_subsequent_cycle_learning_update_receipt_v0_88 import (
    _source_learning_update_request,
)


def _source_learning_update_receipt() -> dict:
    request = _source_learning_update_request()
    return build_subsequent_cycle_learning_update_receipt(request).to_dict()


def main() -> int:
    source = _source_learning_update_receipt()
    result = build_subsequent_cycle_next_iteration_request(source)
    assert result.status == STATUS_READY
    assert result.blockers == []
    record = result.subsequent_cycle_next_iteration_request
    assert record is not None
    assert record["selected_candidate_id"] == source["selected_candidate_id"]
    assert record["source_learning_update_record_digest"] == source["subsequent_cycle_learning_update_receipt"]["learning_update_receipt_digest"]
    assert record["subsequent_cycle_next_iteration_requested"] is True
    assert record["subsequent_cycle_next_iteration_started"] is False

    cases: list[dict] = []
    not_applied = deepcopy(source)
    not_applied["boundary"]["subsequent_cycle_learning_update_applied"] = False
    cases.append(not_applied)
    pre_requested = deepcopy(source)
    pre_requested["boundary"]["subsequent_cycle_next_iteration_requested"] = True
    cases.append(pre_requested)
    tampered = deepcopy(source)
    tampered["selected_candidate_digest"] = "tampered"
    cases.append(tampered)
    missing_record = deepcopy(source)
    missing_record["subsequent_cycle_learning_update_receipt"] = None
    cases.append(missing_record)

    for case in cases:
        blocked = build_subsequent_cycle_next_iteration_request(case)
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.subsequent_cycle_next_iteration_request is None

    assert build_subsequent_cycle_next_iteration_request(source, next_iteration_scope="").status != STATUS_READY
    assert build_subsequent_cycle_next_iteration_request(source, next_iteration_constraints={}).status != STATUS_READY
    print("PASS: PlanOS v0.89 subsequent-cycle next iteration request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
