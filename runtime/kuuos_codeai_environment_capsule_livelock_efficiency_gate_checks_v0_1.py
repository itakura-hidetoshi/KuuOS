from __future__ import annotations

from collections import Counter
from typing import Any, Mapping

from runtime.kuuos_codeai_environment_capsule_livelock_efficiency_gate_schema_v0_1 import *
from runtime.kuuos_codeai_environment_capsule_livelock_efficiency_gate_schema_v0_1 import _validate_binding


ROUTER_MANIFEST_FIELDS = {
    "schema_version",
    "profile_version",
    "repository_full_name",
    "source_commit_sha",
    "queried_subtask_kind",
    "exploration_turns",
    "observation_count",
    "execution_signal_count",
    "grounding_source_count",
    "observable_artifact_count",
    "eligible_specialist_count",
    "excluded_specialist_count",
    "route_decision",
    "selected_specialist_id",
    "selected_specialist_kind",
    "selected_utility_score",
    "measurement_grounded",
    "exact_binding_verified",
    "memory_pack_binding_verified",
    "specialist_alignment_verified",
    "independent_measurement_verified",
    "route_hint_only",
    "specialist_dispatched",
    "candidate_selected",
    "execution_authority_granted",
    "repository_mutation_performed",
    "git_authority_granted",
    "correctness_claimed",
    "memory_pack_digest",
    "memory_receipt_digest",
    "request_digest",
    "policy_digest",
    "trajectory_digest",
    "admission_pack_digest",
    "receipt_digest",
}


def binding_mismatches(value: Mapping[str, Any], query: Mapping[str, Any]) -> list[str]:
    return [field for field in BINDING_FIELDS if value.get(field) != query.get(field)]


def validate_router_admission(router: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    missing = ROUTER_MANIFEST_FIELDS.difference(router)
    extra = set(router).difference(ROUTER_MANIFEST_FIELDS)
    if missing:
        issues.append("router_manifest_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("router_manifest_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if router["schema_version"] != SCHEMA_VERSION:
        issues.append("router_manifest_schema_invalid")
    if router["profile_version"] != PREDECESSOR_PROFILE_VERSION:
        issues.append("router_manifest_profile_invalid")
    if not isinstance(router["repository_full_name"], str) or not router["repository_full_name"]:
        issues.append("router_manifest_repository_invalid")
    if not isinstance(router["source_commit_sha"], str) or SHA40.fullmatch(router["source_commit_sha"]) is None:
        issues.append("router_manifest_source_commit_invalid")
    if router["queried_subtask_kind"] not in SUBTASK_KINDS:
        issues.append("router_manifest_subtask_invalid")
    if router["selected_specialist_kind"] not in SPECIALIST_KINDS:
        issues.append("router_manifest_specialist_kind_invalid")
    if not isinstance(router["selected_specialist_id"], str) or IDENTIFIER.fullmatch(router["selected_specialist_id"]) is None:
        issues.append("router_manifest_specialist_id_invalid")
    for field in (
        "exploration_turns",
        "observation_count",
        "execution_signal_count",
        "grounding_source_count",
        "observable_artifact_count",
        "eligible_specialist_count",
        "excluded_specialist_count",
        "selected_utility_score",
    ):
        if not nonnegative_int(router[field]):
            issues.append("router_manifest_integer_invalid:" + field)
    for field in (
        "memory_pack_digest",
        "memory_receipt_digest",
        "request_digest",
        "policy_digest",
        "trajectory_digest",
        "admission_pack_digest",
        "receipt_digest",
    ):
        if not isinstance(router[field], str) or SHA256.fullmatch(router[field]) is None:
            issues.append("router_manifest_digest_invalid:" + field)
    for field in (
        "measurement_grounded",
        "exact_binding_verified",
        "memory_pack_binding_verified",
        "specialist_alignment_verified",
        "independent_measurement_verified",
        "route_hint_only",
        "specialist_dispatched",
        "candidate_selected",
        "execution_authority_granted",
        "repository_mutation_performed",
        "git_authority_granted",
        "correctness_claimed",
    ):
        if not isinstance(router[field], bool):
            issues.append("router_manifest_boolean_invalid:" + field)
    return sorted(set(issues))


def validate_environment_capsule(capsule: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "capsule_id",
        "capsule_revision",
        *BINDING_FIELDS,
        "runner_image_digest",
        "operating_system_digest",
        "architecture",
        "python_version",
        "lean_toolchain",
        "dependency_manifest_digest",
        "workflow_definition_digest",
        "environment_variables_digest",
        "locale",
        "timezone",
        "network_access_allowed",
        "root_filesystem_immutable",
        "dependency_lock_verified",
        "capsule_complete",
        "capsule_observed",
        "self_report_only",
        "capsule_created_epoch",
        "continuation_authority_granted",
        "execution_authority_granted",
        "repository_mutation_performed",
        "git_authority_granted",
        "correctness_claimed",
        CAPSULE_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(capsule)
    extra = set(capsule).difference(required)
    if missing:
        issues.append("capsule_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("capsule_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if capsule["schema_version"] != SCHEMA_VERSION or capsule["profile_version"] != PROFILE_VERSION:
        issues.append("capsule_profile_invalid")
    for field in ("capsule_id", "capsule_revision"):
        if not isinstance(capsule[field], str) or IDENTIFIER.fullmatch(capsule[field]) is None:
            issues.append("capsule_identifier_invalid:" + field)
    issues.extend(_validate_binding(capsule, "capsule_binding"))
    for field in (
        "runner_image_digest",
        "operating_system_digest",
        "dependency_manifest_digest",
        "workflow_definition_digest",
        "environment_variables_digest",
    ):
        if not isinstance(capsule[field], str) or SHA256.fullmatch(capsule[field]) is None:
            issues.append("capsule_digest_invalid:" + field)
    for field in ("architecture", "python_version", "lean_toolchain", "locale", "timezone"):
        if not isinstance(capsule[field], str) or VERSION_TEXT.fullmatch(capsule[field]) is None:
            issues.append("capsule_text_invalid:" + field)
    if not nonnegative_int(capsule["capsule_created_epoch"]):
        issues.append("capsule_epoch_invalid")
    for field in (
        "network_access_allowed",
        "root_filesystem_immutable",
        "dependency_lock_verified",
        "capsule_complete",
        "capsule_observed",
        "self_report_only",
        "continuation_authority_granted",
        "execution_authority_granted",
        "repository_mutation_performed",
        "git_authority_granted",
        "correctness_claimed",
    ):
        if not isinstance(capsule[field], bool):
            issues.append("capsule_boolean_invalid:" + field)
    if not digest_ok(capsule, CAPSULE_DIGEST_FIELD):
        issues.append("capsule_digest_mismatch")
    return sorted(set(issues))


def validate_checkpoint(checkpoint: Mapping[str, Any], index: int) -> list[str]:
    required = {
        "step_index",
        "phase",
        "state_before_digest",
        "action_digest",
        "observation_digest",
        "state_after_digest",
        "observable_artifact_digest",
        "progress_units",
        "tool_calls",
        "model_calls",
       "input_tokens",
        "output_tokens",
       "wall_clock_ms",
        "failed_action",
    }
    issues: list[str] = []
    missing = required.difference(checkpoint)
    extra = set(checkpoint).difference(required)
    prefix = f"checkpoint:{index}:"
    if missing:
        issues.append(prefix + "missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if not nonnegative_int(checkpoint["step_index"]):
        issues.append(prefix + "step_index_invalid")
    if checkpoint["phase"] not in CHECKPOINT_PHASES:
        issues.append(prefix + "phase_invalid")
    for field in (
        "state_before_digest",
        "action_digest",
        "observation_digest",
        "state_after_digest",
        "observable_artifact_digest",
    ):
        if not isinstance(checkpoint[field], str) or SHA256.fullmatch(checkpoint[field]) is None:
            issues.append(prefix + "digest_invalid:" + field)
    for field in (
        "progress_units",
        "tool_calls",
        "model_calls",
        "input_tokens",
        "output_tokens",
       "wall_clock_ms",
    ):
        if not nonnegative_int(checkpoint[field]):
            issues.append(prefix + "integer_invalid:" + field)
    if not isinstance(checkpoint["failed_action"], bool):
        issues.append(prefix + "failed_action_invalid")
    return sorted(set(issues))


def validate_progress_trace(trace: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "trace_id",
        "trace_revision",
        *BINDING_FIELDS,
        "environment_capsule_digest",
        "checkpoints",
        "trace_observable",
        "trace_complete",
        "self_report_only",
        "trace_created_epoch",
        "continuation_authority_granted",
        "execution_authority_granted",
        "repository_mutation_performed",
        "git_authority_granted",
        "correctness_claimed",
        TRACE_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(trace)
    extra = set(trace).difference(required)
    if missing:
        issues.append("trace_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("trace_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if trace["schema_version"] != SCHEMA_VERSION or trace["profile_version"] != PROFILE_VERSION:
        issues.append("trace_profile_invalid")
    for field in ("trace_id", "trace_revision"):
        if not isinstance(trace[field], str) or IDENTIFIER.fullmatch(trace[field]) is None:
            issues.append("trace_identifier_invalid:" + field)
    issues.extend(_validate_binding(trace, "trace_binding"))
    if not isinstance(trace["environment_capsule_digest"], str) or SHA256.fullmatch(trace["environment_capsule_digest"]) is None:
        issues.append("trace_capsule_digest_invalid")
    checkpoints = trace["checkpoints"]
    if not isinstance(checkpoints, list) or not checkpoints:
        issues.append("trace_checkpoints_invalid")
    else:
        for index, checkpoint in enumerate(checkpoints):
            if not isinstance(checkpoint, Mapping):
                issues.append(f"checkpoint:{index}:not_mapping")
                continue
            issues.extend(validate_checkpoint(checkpoint, index))
        indices = [item.get("step_index") for item in checkpoints if isinstance(item, Mapping)]
        if indices != list(range(len(checkpoints))):
            issues.append("trace_checkpoint_indices_nonconsecutive")
        artifacts = [item.get("observable_artifact_digest") for item in checkpoints if isinstance(item, Mapping)]
        if len(artifacts) != len(set(artifacts)):
            issues.append("trace_checkpoint_artifacts_not_unique")
    if not nonnegative_int(trace["trace_created_epoch"]):
        issues.append("trace_epoch_invalid")
    for field in (
        "trace_observable",
        "trace_complete",
        "self_report_only",
        "continuation_authority_granted",
        "execution_authority_granted",
        "repository_mutation_performed",
        "git_authority_granted",
        "correctness_claimed",
    ):
        if not isinstance(trace[field], bool):
            issues.append("trace_boolean_invalid:" + field)
    if not digest_ok(trace, TRACE_DIGEST_FIELD):
        issues.append("trace_digest_mismatch")
    return sorted(set(issues))


def derive_progress_metrics(checkpoints: list[Mapping[str, Any]]) -> dict[str, Any]:
    total_tool_calls = sum(int(item["tool_calls"]) for item in checkpoints)
    total_model_calls = sum(int(item["model_calls"]) for item in checkpoints)
    total_token_units = sum(int(item["input_tokens"]) + int(item["output_tokens"]) for item in checkpoints)
    total_wall_clock_ms = sum(int(item["wall_clock_ms"]) for item in checkpoints)
    failed_action_count = sum(1 for item in checkpoints if item["failed_action"] is True)
    total_progress_units = sum(int(item["progress_units"]) for item in checkpoints)

    no_progress_streak = 0
    maximum_no_progress_streak = 0
    seen_states: set[str] = set()
    cycle_count = 0
    transitions: Counter[tuple[str, str, str]] = Counter()
    all_states: set[str] = set()
    for item in checkpoints:
        before = str(item["state_before_digest"])
        after = str(item["state_after_digest"])
        progress = int(item["progress_units"])
        all_states.update((before, after))
        seen_states.add(before)
        if progress == 0:
            no_progress_streak += 1
            maximum_no_progress_streak = max(maximum_no_progress_streak, no_progress_streak)
            transitions[(before, str(item["action_digest"]), after)] += 1
            if after in seen_states:
                cycle_count += 1
        else:
            no_progress_streak = 0
        seen_states.add(after)

    repeated_zero_progress_transitions = sum(max(count - 1, 0) for count in transitions.values())
    return {
        "step_count": len(checkpoints),
        "tool_call_count": total_tool_calls,
        "model_call_count": total_model_calls,
        "token_units": total_token_units,
        "wall_clock_ms": total_wall_clock_ms,
        "failed_action_count": failed_action_count,
        "total_progress_units": total_progress_units,
        "distinct_state_count": len(all_states),
        "maximum_no_progress_streak": maximum_no_progress_streak,
        "repeated_zero_progress_transitions": repeated_zero_progress_transitions,
        "cycle_count": cycle_count,
        "cycle_detected": cycle_count > 0,
    }


__all__ = [
    "ROUTER_MANIFEST_FIELDS",
    "binding_mismatches",
    "derive_progress_metrics",
    "validate_checkpoint",
    "validate_environment_capsule",
    "validate_progress_trace",
    "validate_router_admission",
]
