#!/usr/bin/env python3
from __future__ import annotations

from tests.test_kuuos_codeai_verification_guided_candidate_repair_regeneration_v0_1 import (
    build_fixture,
    execute_fixture,
)
from runtime.kuuos_codeai_verification_guided_candidate_repair_regeneration_v0_1 import (
    STATUS_READY,
)


def main() -> int:
    inputs = build_fixture()
    result = execute_fixture(inputs)
    assert result.status == STATUS_READY, result.issues
    assert result.normalized_feedback is not None
    assert result.downstream_regeneration is not None
    assert result.receipt is not None
    assert result.normalized_feedback["feedback_record_count"] == 1
    assert result.normalized_feedback["feedback_treated_as_truth"] is False
    assert len(result.downstream_regeneration.regenerated_candidates) == 1
    assert len(result.downstream_regeneration.combined_candidates) == 2
    assert result.receipt["verification_lineage_verified"] is True
    assert result.receipt["feedback_normalized_and_bounded"] is True
    assert result.receipt["candidate_selected"] is False
    assert result.receipt["patch_applied"] is False
    assert result.receipt["repository_mutation_performed"] is False
    assert result.receipt["git_ref_changed"] is False
    assert result.receipt["network_access_performed"] is False
    assert result.receipt["secret_access_performed"] is False
    assert result.receipt["successor_stage_authority_granted"] is False
    assert result.receipt["verification_failure_treated_as_repair_truth"] is False
    assert result.receipt["failed_check_treated_as_required_edit"] is False
    assert result.receipt["repair_regeneration_treated_as_correction"] is False
    assert result.receipt["new_candidate_treated_as_verified_patch"] is False
    print(
        "PASS: failed verification evidence -> bounded feedback -> "
        "provider-neutral repair regeneration -> unselected candidate"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
