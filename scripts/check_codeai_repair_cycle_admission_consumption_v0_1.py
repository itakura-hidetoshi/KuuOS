#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_repair_cycle_admission_consumption_v0_1 import (
    STATUS_READY,
    build_codeai_repair_cycle_admission_consumption,
)


EXAMPLE = Path("examples/codeai_repair_cycle_admission_consumption_v0_1.json")


def main() -> None:
    payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    result = build_codeai_repair_cycle_admission_consumption(
        admission_receipt=payload["admission_receipt"],
        consumption_request=payload["consumption_request"],
        consumption_policy=payload["consumption_policy"],
        consumption_registry=payload["consumption_registry"],
    )
    assert result.status == STATUS_READY, result.issues
    assert result.issues == ()
    assert result.execution_input is not None
    assert result.next_registry is not None
    assert result.receipt is not None

    execution_input = result.execution_input
    next_registry = result.next_registry
    receipt = result.receipt
    admission = payload["admission_receipt"]

    assert receipt["source_admission_consumed"] is True
    assert receipt["admission_replay_excluded"] is True
    assert receipt["execution_nonce_replay_excluded"] is True
    assert receipt["registry_transition_verified"] is True
    assert receipt["exactly_one_execution_input_issued"] is True
    assert execution_input["execution_input_active"] is True
    assert execution_input["execution_input_reusable"] is False
    assert execution_input["execution_input_consumed"] is False
    assert execution_input["bounded_cycle_execution_authority_granted"] is True
    assert execution_input["automatic_execution_authority_granted"] is False
    assert execution_input["general_successor_stage_authority_granted"] is False

    budget_pairs = (
        ("reserved_candidate", "maximum_candidate_count"),
        ("reserved_provider_call", "maximum_provider_call_count"),
        ("reserved_command", "maximum_command_count"),
        ("reserved_timeout_seconds", "maximum_total_timeout_seconds"),
        ("reserved_output_bytes", "maximum_total_output_bytes"),
    )
    for source_field, execution_field in budget_pairs:
        assert execution_input[execution_field] == admission[source_field]

    assert next_registry["registry_revision"] == (
        payload["consumption_registry"]["registry_revision"] + 1
    )
    assert next_registry["consumed_admission_receipt_digests"][-1] == (
        admission["codeai_repair_cycle_continuation_admission_receipt_digest"]
    )
    assert next_registry["consumed_execution_nonce_digests"][-1] == (
        payload["consumption_request"]["execution_nonce_digest"]
    )
    assert next_registry["last_consumed_cycle_index"] == admission["admitted_cycle_index"]

    for surface in (execution_input, receipt):
        for field in (
            "cycle_execution_performed",
            "provider_invoked",
            "runner_invoked",
            "candidate_generated",
            "candidate_selected",
            "patch_applied",
            "verification_executed",
            "repository_mutation_performed",
            "git_ref_changed",
            "network_access_performed",
            "secret_access_performed",
            "merge_performed",
            "deployment_performed",
        ):
            assert surface[field] is False

    print(
        "CodeAI Repair Cycle Admission Consumption v0.1: "
        "sealed non-reusable admission consumed once, replay registry advanced, "
        "reserved five-dimensional budget mapped to one active bounded execution input, "
        "and no cycle, provider, runner, repository, Git, network, secret, merge, "
        "or deployment action performed."
    )


if __name__ == "__main__":
    main()
