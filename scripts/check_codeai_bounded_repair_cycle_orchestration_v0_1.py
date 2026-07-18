#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_codeai_bounded_repair_cycle_orchestration_v0_1 import (
    DISPOSITION_PASSED,
    STATUS_READY,
    build_codeai_bounded_repair_cycle_orchestration,
)
from tests.test_kuuos_codeai_bounded_repair_cycle_orchestration_v0_1 import (
    build_cycle_inputs,
)


def main() -> int:
    inputs = build_cycle_inputs()
    repository_before = dict(inputs["repository_files"])
    result = build_codeai_bounded_repair_cycle_orchestration(**inputs)
    assert result.status == STATUS_READY, result.issues
    assert result.receipt is not None
    assert result.selected_candidate is not None
    assert result.resulting_repository_files is not None
    assert result.evidence_bundle is not None
    assert result.independent_verification_evidence is not None
    assert result.receipt["codeai_disposition"] == DISPOSITION_PASSED
    assert result.receipt["failed_candidate_excluded_from_reselection"] is True
    assert result.receipt["least_change_reselection_performed"] is True
    assert result.receipt["isolated_application_performed"] is True
    assert result.receipt["bounded_verification_execution_performed"] is True
    assert result.receipt["cycle_verification_passed"] is True
    assert result.receipt["next_cycle_eligible"] is False
    assert result.receipt["repository_mutation_performed"] is False
    assert result.receipt["git_ref_changed"] is False
    assert result.receipt["successor_stage_authority_granted"] is False
    assert inputs["repository_files"] == repository_before
    print(
        "PASS: failed verification -> bounded repair regeneration -> "
        "failed-candidate exclusion -> least-change reselection -> isolated "
        "application -> bounded verification execution"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
