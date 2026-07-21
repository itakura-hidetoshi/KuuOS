from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_reobservation_bounded_continuation_proposal_gate_schema_v0_1 import *
from runtime.kuuos_codeai_reobservation_bounded_continuation_proposal_gate_schema_v0_1 import _validate_binding

PREDECESSOR_MANIFEST_FIELDS = {
    "capsule_reproducible",
    "continuation_authority_granted",
    "continuation_hint_only",
    "correctness_claimed",
    "cycle_count",
    "cycle_detected",
    "distinct_state_count",
    "efficiency_within_budget",
    "environment_capsule_digest",
    "environment_exact",
    "execution_authority_granted",
    "failed_action_count",
    "gate_decision",
    "gate_pack_digest",
    "git_authority_granted",
    "hold_reasons",
    "livelock_free",
    "maximum_no_progress_streak",
    "model_call_count",
    "policy_digest",
    "predecessor_router_verified",
    "profile_version",
    "progress_trace_digest",
    "receipt_digest",
    "repeated_zero_progress_transitions",
    "repository_full_name",
    "repository_mutation_performed",
    "request_digest",
    "router_admission_manifest_digest",
    "router_admission_pack_digest",
    "router_admission_receipt_digest",
    "schema_version",
    "selected_specialist_id",
    "selected_specialist_kind",
    "selected_subtask_kind",
    "source_commit_sha",
    "step_count",
    "token_units",
    "tool_call_count",
    "total_progress_units",
    "trace_grounded",
    "wall_clock_ms",
}


def binding_mismatches(value: Mapping[str, Any], query: Mapping[str, Any]) -> list[str]:
    return [field for field in BINDING_FIELDS if value.get(field) != query.get(field)]


def validate_predecessor_gate(manifest: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    missing = PREDECESSOR_MANIFEST_FIELDS.difference(manifest)
    extra = set(manifest).difference(PREDECESSOR_MANIFEST_FIELDS)
    if missing:
        issues.append("predecessor_manifest_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("predecessor_manifest_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if manifest["schema_version"] != SCHEMA_VERSION:
        issues.append("predecessor_manifest_schema_invalid")
    if manifest["profile_version"] != PREDECESSOR_PROFILE_VERSION:
        issues.append("predecessor_manifest_profile_invalid")
    if not isinstance(manifest["repository_full_name"], str) or not manifest["repository_full_name"]:
        issues.append("predecessor_repository_invalid")
    if not isinstance(manifest["source_commit_sha"], str) or SHA40.fullmatch(manifest["source_commit_sha"]) is None:
        issues.append("predecessor_source_commit_invalid")
    if manifest["selected_specialist_kind"] not in SPECIALIST_KINDS:
        issues.append("predecessor_specialist_kind_invalid")
    if manifest["selected_subtask_kind"] not in SUBTASK_KINDS:
        issues.append("predecessor_subtask_kind_invalid")
    if not isinstance(manifest["selected_specialist_id"], str) or IDENTIFIER.fullmatch(manifest["selected_specialist_id"]) is None:
        issues.append("predecessor_specialist_id_invalid")
    for field in (
        "step_count",
        "tool_call_count",
        "model_call_count",
        "token_units",
        "wall_clock_ms",
        "failed_action_count",
        "total_progress_units",
        "distinct_state_count",
        "maximum_no_progress_streak",
        "repeated_zero_progress_transitions",
        "cycle_count",
    ):
        if not nonnegative_int(manifest[field]):
            issues.append("predecessor_integer_invalid:" + field)
    for field in (
        "request_digest",
        "policy_digest",
        "router_admission_manifest_digest",
        "router_admission_pack_digest",
        "router_admission_receipt_digest",
        "environment_capsule_digest",
        "progress_trace_digest",
        "gate_pack_digest",
        "receipt_digest",
    ):
        if not isinstance(manifest[field], str) or SHA256.fullmatch(manifest[field]) is None:
            issues.append("predecessor_digest_invalid:" + field)
    if not unique_strings(manifest["hold_reasons"]):
        issues.append("predecessor_hold_reasons_invalid")
    for field in (
        "capsule_reproducible",
        "continuation_authority_granted",
        "continuation_hint_only",
        "correctness_claimed",
        "cycle_detected",
        "efficiency_within_budget",
        "environment_exact",
        "execution_authority_granted",
        "git_authority_granted",
        "livelock_free",
        "predecessor_router_verified",
        "repository_mutation_performed",
        "trace_grounded",
    ):
        if not isinstance(manifest[field], bool):
            issues.append("predecessor_boolean_invalid:" + field)
    if not isinstance(manifest["gate_decision"], str) or not manifest["gate_decision"]:
        issues.append("predecessor_decision_invalid")
    return sorted(set(issues))


def validate_continuation_proposal(proposal: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "proposal_id",
        "proposal_revision",
        *BINDING_FIELDS,
        "continuation_round",
        "action_count",
        "action_kind",
        "action_target_digest",
        "pre_state_digest",
        "expected_observation_contract_digest",
        "expected_artifact_contract_digest",
        *{"requested_" + name for name in RESOURCE_NAMES},
        "proposal_grounded",
        "read_only_action",
        "observable_return_required",
        "new_checkpoint_required",
        "predecessor_gate_reentry_required",
        "self_report_only",
        "proposal_created_epoch",
        "claims_continuation_authority",
        "claims_execution_authority",
        "claims_repository_mutation_authority",
        "claims_git_authority",
        "claims_correctness",
        PROPOSAL_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(proposal)
    extra = set(proposal).difference(required)
    if missing:
        issues.append("proposal_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("proposal_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if proposal["schema_version"] != SCHEMA_VERSION or proposal["profile_version"] != PROFILE_VERSION:
        issues.append("proposal_profile_invalid")
    for field in ("proposal_id", "proposal_revision"):
        if not isinstance(proposal[field], str) or IDENTIFIER.fullmatch(proposal[field]) is None:
            issues.append("proposal_identifier_invalid:" + field)
    issues.extend(_validate_binding(proposal, "proposal_binding"))
    if not positive_int(proposal["continuation_round"]):
        issues.append("proposal_continuation_round_invalid")
    if not positive_int(proposal["action_count"]):
        issues.append("proposal_action_count_invalid")
    if proposal["action_kind"] not in ACTION_KINDS:
        issues.append("proposal_action_kind_invalid")
    for field in (
        "action_target_digest",
        "pre_state_digest",
        "expected_observation_contract_digest",
        "expected_artifact_contract_digest",
    ):
        if not isinstance(proposal[field], str) or SHA256.fullmatch(proposal[field]) is None:
            issues.append("proposal_digest_invalid:" + field)
    for resource in RESOURCE_NAMES:
        if not nonnegative_int(proposal["requested_" + resource]):
            issues.append("proposal_integer_invalid:requested_" + resource)
    for field in (
        "requested_steps",
        "requested_tool_calls",
        "requested_model_calls",
        "requested_token_units",
        "requested_wall_clock_ms",
    ):
        if not positive_int(proposal[field]):
            issues.append("proposal_positive_integer_invalid:" + field)
    for field in (
        "proposal_grounded",
        "read_only_action",
        "observable_return_required",
        "new_checkpoint_required",
        "predecessor_gate_reentry_required",
        "self_report_only",
        "claims_continuation_authority",
        "claims_execution_authority",
        "claims_repository_mutation_authority",
        "claims_git_authority",
        "claims_correctness",
    ):
        if not isinstance(proposal[field], bool):
            issues.append("proposal_boolean_invalid:" + field)
    if not nonnegative_int(proposal["proposal_created_epoch"]):
        issues.append("proposal_epoch_invalid")
    if not digest_ok(proposal, PROPOSAL_DIGEST_FIELD):
        issues.append("proposal_digest_mismatch")
    return sorted(set(issues))


def predecessor_usage(manifest: Mapping[str, Any]) -> dict[str, int]:
    return {
        "steps": int(manifest["step_count"]),
        "tool_calls": int(manifest["tool_call_count"]),
        "model_calls": int(manifest["model_call_count"]),
        "token_units": int(manifest["token_units"]),
        "wall_clock_ms": int(manifest["wall_clock_ms"]),
        "failed_actions": int(manifest["failed_action_count"]),
    }


def requested_budget(proposal: Mapping[str, Any]) -> dict[str, int]:
    return {name: int(proposal["requested_" + name]) for name in RESOURCE_NAMES}


def derive_residual_budget(manifest: Mapping[str, Any], policy: Mapping[str, Any]) -> dict[str, int]:
    used = predecessor_usage(manifest)
    return {name: int(policy["maximum_total_" + name]) - used[name] for name in RESOURCE_NAMES}


__all__ = [
    "PREDECESSOR_MANIFEST_FIELDS",
    "binding_mismatches",
    "derive_residual_budget",
    "predecessor_usage",
    "requested_budget",
    "validate_continuation_proposal",
    "validate_predecessor_gate",
]
