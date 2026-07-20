#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace
from typing import Any

from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_types_v0_1 import (
    RESUME_INPUT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1 import (
    DISPOSITION_CONSUMED,
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    EXECUTION_INPUT_DIGEST_FIELD,
    EXECUTION_INPUT_PROFILE_VERSION,
    PROFILE_VERSION as SOURCE_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as SOURCE_REGISTRY_DIGEST_FIELD,
    canonical_digest,
)
from runtime.kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1 import (
    EVIDENCE_DIGEST_FIELD as INNER_EVIDENCE_DIGEST_FIELD,
    LIFECYCLE_RECEIPT_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as INNER_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as INNER_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as INNER_REQUEST_DIGEST_FIELD,
    STATUS_READY as INNER_STATUS_READY,
)
from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_execution_v0_1 import (
    DISPOSITION_EXECUTED,
    EVIDENCE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_READY,
    build_codeai_durable_git_lifecycle_loop_resumption_execution,
)

HEX_A = "a" * 64
HEX_B = "b" * 64
HEX_C = "c" * 64
HEX_D = "d" * 64


def seal(value: dict[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(value)
    result.pop(field, None)
    result[field] = canonical_digest(result)
    return result


def stub_orchestrator(**kwargs: Any) -> Any:
    del kwargs
    evidence = seal(
        {"schema_version": "v0.1", "codeai_disposition": "bounded_loop_evidence"},
        INNER_EVIDENCE_DIGEST_FIELD,
    )
    receipt = seal(
        {
            "schema_version": "v0.1",
            "codeai_disposition": "bounded_autonomous_git_lifecycle_loop_completed",
            "total_effect_count": 2,
        },
        INNER_RECEIPT_DIGEST_FIELD,
    )
    return SimpleNamespace(
        status=INNER_STATUS_READY,
        issues=(),
        evidence=evidence,
        receipt=receipt,
        next_loop_registry={"registry": "loop"},
        next_execution_registry={"registry": "execution"},
        next_reobservation_registry={"registry": "reobservation"},
        next_continuation_registry={"registry": "continuation"},
        final_lifecycle_receipt={"receipt": "final"},
        final_lifecycle_state={"state": "final"},
    )


def build_example_bundle() -> dict[str, Any]:
    final_lifecycle_receipt = seal(
        {
            "schema_version": "v0.1",
            "lifecycle_id": "git-loop-lifecycle-001",
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "execution_lease_issued": True,
            "next_effect_phase": "local_commit",
        },
        LIFECYCLE_RECEIPT_DIGEST_FIELD,
    )
    resume_input = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Durable Git Lifecycle Loop Resume Input v0.1",
            "resume_input_id": "git-loop-resume-input-001",
            "checkpoint_id": "git-loop-checkpoint-001",
            "checkpoint_envelope_digest": HEX_A,
            "source_persistence_receipt_digest": HEX_B,
            "source_persistence_registry_digest": HEX_C,
            "source_store_state_digest": HEX_D,
            "loop_id": "git-loop-001",
            "lifecycle_id": "git-loop-lifecycle-001",
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "loop_disposition": "bounded_autonomous_git_lifecycle_effect_budget_exhausted",
            "prior_effect_count": 2,
            "prior_maximum_effect_count": 4,
            "final_lifecycle_receipt_digest": final_lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
            "final_lifecycle_state_digest": HEX_B,
            "final_lifecycle_completed": False,
            "final_execution_lease_issued": True,
            "resume_effect_budget": 2,
            "resume_execution_command_budget": 8,
            "resume_execution_output_bytes": 8000,
            "issued_epoch": 500,
            "future_only": True,
            "active_now": False,
            "loop_execution_authorized": False,
            "git_effect_authorized": False,
            "automatic_resumption_authorized": False,
            "general_successor_stage_authority_granted": False,
        },
        RESUME_INPUT_DIGEST_FIELD,
    )
    execution_input = seal(
        {
            "schema_version": "v0.1",
            "profile_version": EXECUTION_INPUT_PROFILE_VERSION,
            "execution_input_id": "git-loop-execution-session-001:loop-execution-input",
            "source_resumption_receipt_digest": HEX_A,
            "source_resumption_evidence_digest": HEX_B,
            "source_resumption_registry_digest": HEX_C,
            "source_resume_input_digest": resume_input[RESUME_INPUT_DIGEST_FIELD],
            "checkpoint_id": resume_input["checkpoint_id"],
            "checkpoint_envelope_digest": resume_input["checkpoint_envelope_digest"],
            "loop_id": resume_input["loop_id"],
            "lifecycle_id": resume_input["lifecycle_id"],
            "repository_full_name": resume_input["repository_full_name"],
            "prior_loop_disposition": resume_input["loop_disposition"],
            "prior_effect_count": resume_input["prior_effect_count"],
            "prior_maximum_effect_count": resume_input["prior_maximum_effect_count"],
            "resume_effect_budget": resume_input["resume_effect_budget"],
            "resume_execution_command_budget": resume_input["resume_execution_command_budget"],
            "resume_execution_output_bytes": resume_input["resume_execution_output_bytes"],
            "issued_epoch": 510,
            "one_shot": True,
            "reusable": False,
            "active_now": True,
            "loop_execution_authorized": True,
            "direct_git_effect_authorized": False,
            "automatic_execution_authorized": False,
            "network_access_authorized": False,
            "secret_material_read_authorized": False,
            "general_git_authority_granted": False,
            "general_successor_stage_authority_granted": False,
        },
        EXECUTION_INPUT_DIGEST_FIELD,
    )
    source_registry = seal(
        {
            "registry_id": "git-loop-resumption-consumption-registry",
            "registry_revision": 1,
            "consumed_consumption_nonce_digests": [HEX_A],
            "consumed_resumption_receipt_digests": [HEX_B],
            "consumed_resume_input_digests": [resume_input[RESUME_INPUT_DIGEST_FIELD]],
            "issued_execution_input_digests": [execution_input[EXECUTION_INPUT_DIGEST_FIELD]],
            "successful_consumption_count": 1,
            "last_consumption_epoch": 510,
        },
        SOURCE_REGISTRY_DIGEST_FIELD,
    )
    source_evidence = seal(
        {
            "schema_version": "v0.1",
            "profile_version": SOURCE_PROFILE_VERSION,
            "source_resume_input_digest": resume_input[RESUME_INPUT_DIGEST_FIELD],
            "next_consumption_registry_digest": source_registry[SOURCE_REGISTRY_DIGEST_FIELD],
            "execution_input_digest": execution_input[EXECUTION_INPUT_DIGEST_FIELD],
            "source_correspondence_verified": True,
            "resume_input_consumed": True,
            "execution_input_issued": True,
            "execution_input_active": True,
            "loop_execution_performed": False,
            "git_effect_performed": False,
            "automatic_resumption_performed": False,
            "network_accessed": False,
            "secret_material_read": False,
        },
        SOURCE_EVIDENCE_DIGEST_FIELD,
    )
    source_receipt = seal(
        {
            "schema_version": "v0.1",
            "profile_version": SOURCE_PROFILE_VERSION,
            "source_resume_input_digest": resume_input[RESUME_INPUT_DIGEST_FIELD],
            "next_consumption_registry_digest": source_registry[SOURCE_REGISTRY_DIGEST_FIELD],
            "consumption_evidence_digest": source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD],
            "execution_input_digest": execution_input[EXECUTION_INPUT_DIGEST_FIELD],
            "checkpoint_id": resume_input["checkpoint_id"],
            "checkpoint_envelope_digest": resume_input["checkpoint_envelope_digest"],
            "loop_id": resume_input["loop_id"],
            "lifecycle_id": resume_input["lifecycle_id"],
            "repository_full_name": resume_input["repository_full_name"],
            "codeai_disposition": DISPOSITION_CONSUMED,
            "operating_mode": "durable_git_lifecycle_loop_resumption_consumption",
            "route_receipt_recorded": True,
            "source_resumption_bundle_verified": True,
            "source_resume_input_verified": True,
            "consumption_nonce_consumed": True,
            "consumption_registry_advanced_once": True,
            "resume_input_consumed": True,
            "execution_input_issued": True,
            "execution_input_one_shot": True,
            "execution_input_reusable": False,
            "execution_input_active": True,
            "loop_execution_authorized_for_successor": True,
            "direct_git_effect_authorized": False,
            "automatic_execution_authorized": False,
            "loop_execution_performed": False,
            "git_effect_performed": False,
            "automatic_resumption_performed": False,
            "network_accessed": False,
            "secret_material_read": False,
            "general_git_authority_granted": False,
            "general_successor_stage_authority_granted": False,
        },
        SOURCE_RECEIPT_DIGEST_FIELD,
    )
    loop_request = seal(
        {
            "loop_id": execution_input["loop_id"],
            "lifecycle_id": execution_input["lifecycle_id"],
            "repository_full_name": execution_input["repository_full_name"],
            "requested_max_effect_count": 2,
        },
        INNER_REQUEST_DIGEST_FIELD,
    )
    loop_policy = seal(
        {
            "maximum_effect_count": 2,
            "maximum_total_execution_command_count": 4,
            "maximum_total_reobservation_command_count": 4,
            "maximum_total_execution_output_bytes": 4000,
            "maximum_total_reobservation_output_bytes": 4000,
        },
        INNER_POLICY_DIGEST_FIELD,
    )
    request = seal(
        {
            "execution_session_id": "git-loop-resumption-execution-001",
            "invocation_nonce_digest": HEX_D,
            "source_consumption_receipt_digest": source_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
            "source_consumption_evidence_digest": source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD],
            "source_consumption_registry_digest": source_registry[SOURCE_REGISTRY_DIGEST_FIELD],
            "source_execution_input_digest": execution_input[EXECUTION_INPUT_DIGEST_FIELD],
            "source_resume_input_digest": resume_input[RESUME_INPUT_DIGEST_FIELD],
            "loop_id": execution_input["loop_id"],
            "lifecycle_id": execution_input["lifecycle_id"],
            "repository_full_name": execution_input["repository_full_name"],
            "executor_id": "codeai-loop-resumption-executor",
            "request_created_epoch": 520,
            "consume_execution_input": True,
            "invoke_bounded_loop": True,
            "source_correspondence_confirmed": True,
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "expected_source_consumption_receipt_digest": source_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
            "expected_source_consumption_evidence_digest": source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD],
            "expected_source_consumption_registry_digest": source_registry[SOURCE_REGISTRY_DIGEST_FIELD],
            "expected_source_execution_input_digest": execution_input[EXECUTION_INPUT_DIGEST_FIELD],
            "expected_source_resume_input_digest": resume_input[RESUME_INPUT_DIGEST_FIELD],
            "expected_repository_full_name": execution_input["repository_full_name"],
            "authorized_executor_ids": ["codeai-loop-resumption-executor"],
            "maximum_request_age": 100,
            "maximum_registry_entries": 16,
            "maximum_effect_count": 2,
            "maximum_total_command_count": 8,
            "maximum_total_output_bytes": 8000,
            "evaluation_epoch": 520,
            "allow_execution_input_consumption": True,
            "allow_bounded_loop_invocation": True,
            "require_one_shot": True,
            "require_active_input": True,
            "require_existing_lifecycle_effect_chain": True,
            "allow_direct_git_effect": False,
            "allow_automatic_execution": False,
            "allow_unbounded_execution": False,
            "allow_network_access_outside_orchestrator": False,
            "allow_secret_material_read": False,
            "allow_general_successor_authority": False,
        },
        POLICY_DIGEST_FIELD,
    )
    registry = seal(
        {
            "registry_id": "git-loop-resumption-execution-registry",
            "registry_revision": 0,
            "consumed_invocation_nonce_digests": [],
            "consumed_execution_input_digests": [],
            "emitted_loop_receipt_digests": [],
            "successful_execution_count": 0,
            "last_execution_epoch": 0,
        },
        REGISTRY_DIGEST_FIELD,
    )
    return {
        "consumption_receipt": source_receipt,
        "consumption_evidence": source_evidence,
        "consumption_registry": source_registry,
        "source_resume_input": resume_input,
        "execution_input": execution_input,
        "execution_request": request,
        "execution_policy": policy,
        "execution_registry": registry,
        "source_trajectory_receipt": {"trajectory": "source"},
        "initial_lifecycle_receipt": final_lifecycle_receipt,
        "loop_request": loop_request,
        "loop_policy": loop_policy,
        "loop_registry": {"registry": "loop"},
        "inner_execution_registry": {"registry": "inner-execution"},
        "reobservation_registry": {"registry": "reobservation"},
        "continuation_registry": {"registry": "continuation"},
        "execution_adapter": object(),
        "reobservation_adapter": object(),
        "orchestrator": stub_orchestrator,
    }


def main() -> int:
    bundle = build_example_bundle()
    result = build_codeai_durable_git_lifecycle_loop_resumption_execution(**bundle)
    assert result.status == STATUS_READY, result.issues
    assert result.receipt is not None
    assert result.evidence is not None
    assert result.next_registry is not None
    assert result.receipt["codeai_disposition"] == DISPOSITION_EXECUTED
    assert result.receipt["execution_input_consumed"] is True
    assert result.receipt["bounded_loop_invoked_once"] is True
    assert result.receipt["existing_lifecycle_effect_chain_enforced"] is True
    assert result.receipt["direct_git_effect_performed"] is False
    assert result.receipt["delegated_git_effect_count"] == 2
    assert result.next_registry["registry_revision"] == 1
    assert result.next_registry["successful_execution_count"] == 1
    assert result.receipt[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {k: v for k, v in result.receipt.items() if k != RECEIPT_DIGEST_FIELD}
    )
    assert result.evidence[EVIDENCE_DIGEST_FIELD] == canonical_digest(
        {k: v for k, v in result.evidence.items() if k != EVIDENCE_DIGEST_FIELD}
    )
    print("CodeAI Durable Git Lifecycle Loop Resumption Execution v0.1: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
