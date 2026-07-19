#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_codeai_admission_gated_bounded_repair_cycle_execution_v0_1 import (
    DISPOSITION_PASSED,
    STATUS_READY,
    build_codeai_admission_gated_bounded_repair_cycle_execution,
)
from tests.test_kuuos_codeai_admission_gated_bounded_repair_cycle_execution_v0_1 import (
    build_execution_inputs,
)


def main() -> None:
    inputs = build_execution_inputs()
    before = dict(inputs["isolated_repository_files"])
    result = build_codeai_admission_gated_bounded_repair_cycle_execution(**inputs)
    assert result.status == STATUS_READY, result.issues
    assert result.issues == ()
    assert result.receipt is not None
    assert result.next_registry is not None
    assert result.resulting_repository_files is not None
    assert result.evidence_bundle is not None
    assert result.independent_verification_evidence is not None
    receipt = result.receipt
    assert receipt["codeai_disposition"] == DISPOSITION_PASSED
    assert receipt["execution_input_consumed"] is True
    assert receipt["execution_input_replay_excluded"] is True
    assert receipt["cycle_execution_nonce_replay_excluded"] is True
    assert receipt["provider_invoked"] is True
    assert receipt["candidate_generated"] is True
    assert receipt["candidate_selected"] is True
    assert receipt["isolated_patch_application_performed"] is True
    assert receipt["verification_executed"] is True
    assert receipt["cycle_execution_performed"] is True
    assert receipt["cycle_completed"] is True
    assert receipt["cycle_verification_passed"] is True
    assert receipt["used_candidate"] <= receipt["maximum_candidate"]
    assert receipt["used_provider_call"] <= receipt["maximum_provider_call"]
    assert receipt["used_command"] <= receipt["maximum_command"]
    assert receipt["used_timeout_seconds"] <= receipt["maximum_timeout_seconds"]
    assert receipt["used_output_bytes"] <= receipt["maximum_output_bytes"]
    assert result.next_registry["registry_revision"] == 2
    assert result.next_registry["consumed_execution_input_digests"][-1] == receipt["source_execution_input_digest"]
    assert inputs["isolated_repository_files"] == before
    for field in (
        "repository_mutation_performed",
        "git_ref_changed",
        "branch_created",
        "commit_created",
        "push_performed",
        "pull_request_created",
        "network_access_performed",
        "secret_access_performed",
        "merge_performed",
        "deployment_performed",
        "merge_authority_granted",
        "deployment_authority_granted",
        "general_successor_stage_authority_granted",
    ):
        assert receipt[field] is False, field
    print(
        "CodeAI Admission-Gated Bounded Repair Cycle Execution v0.1: "
        "one active non-reusable execution input consumed once, provider adapter and existing "
        "selection/application/verification stages executed inside exact five-dimensional budgets, "
        "execution registry advanced by one, and no live repository, Git, network, secret, merge, "
        "deployment, or successor authority granted."
    )


if __name__ == "__main__":
    main()
