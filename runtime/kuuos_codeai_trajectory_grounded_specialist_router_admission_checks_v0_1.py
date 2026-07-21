from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_trajectory_grounded_specialist_router_admission_schema_v0_1 import *
from runtime.kuuos_codeai_trajectory_grounded_specialist_router_admission_schema_v0_1 import _validate_binding


def binding_mismatches(value: Mapping[str, Any], query: Mapping[str, Any]) -> list[str]:
    return [field for field in BINDING_FIELDS if value.get(field) != query.get(field)]


def validate_trajectory(trajectory: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version", "profile_version", "trajectory_id", "trajectory_revision",
        *BINDING_FIELDS, "exploration_turns", "observation_count", "execution_signal_count",
        "grounding_sources", "observable_artifact_digests", "self_report_only",
        "measurement_complete", "repository_state_observed", "tests_observed",
        "trajectory_created_epoch", "repository_mutation_performed", "specialist_dispatched",
        "candidate_selected", "execution_authority_granted", "git_authority_granted",
        TRAJECTORY_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(trajectory)
    extra = set(trajectory).difference(required)
    if missing:
        issues.append("trajectory_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("trajectory_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if trajectory["schema_version"] != SCHEMA_VERSION or trajectory["profile_version"] != PROFILE_VERSION:
        issues.append("trajectory_profile_invalid")
    for field in ("trajectory_id", "trajectory_revision"):
        if not isinstance(trajectory[field], str) or IDENTIFIER.fullmatch(trajectory[field]) is None:
            issues.append("trajectory_identifier_invalid:" + field)
    issues.extend(_validate_binding(trajectory, "trajectory_binding"))
    for field in ("exploration_turns", "observation_count", "execution_signal_count", "trajectory_created_epoch"):
        if not nonnegative_int(trajectory[field]):
            issues.append("trajectory_integer_invalid:" + field)
    if not unique_strings(trajectory["grounding_sources"], nonempty=True):
        issues.append("trajectory_grounding_sources_invalid")
    if not unique_strings(trajectory["observable_artifact_digests"], nonempty=True):
        issues.append("trajectory_artifacts_invalid")
    elif any(SHA256.fullmatch(item) is None for item in trajectory["observable_artifact_digests"]):
        issues.append("trajectory_artifact_digest_invalid")
    for field in (
        "self_report_only", "measurement_complete", "repository_state_observed", "tests_observed",
        "repository_mutation_performed", "specialist_dispatched", "candidate_selected",
        "execution_authority_granted", "git_authority_granted",
    ):
        if not isinstance(trajectory[field], bool):
            issues.append("trajectory_boolean_invalid:" + field)
    if not digest_ok(trajectory, TRAJECTORY_DIGEST_FIELD):
        issues.append("trajectory_digest_mismatch")
    return sorted(set(issues))


def validate_specialist_evidence(evidence: Mapping[str, Any], index: int) -> list[str]:
    required = {
        "schema_version", "profile_version", "specialist_id", "specialist_revision",
        "specialist_kind", "supported_subtask_kind", *BINDING_FIELDS,
        "measurement_packet_digest", "fit_score", "reliability_score",
        "estimated_cost_units", "utility_score", "independent_measurement",
        "evidence_created_epoch", "route_hint_only", "repository_mutation_performed",
        "specialist_dispatched", "candidate_selected", "execution_authority_granted",
        "git_authority_granted", "correctness_claimed", SPECIALIST_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(evidence)
    extra = set(evidence).difference(required)
    prefix = f"specialist:{index}:"
    if missing:
        issues.append(prefix + "missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if evidence["schema_version"] != SCHEMA_VERSION or evidence["profile_version"] != PROFILE_VERSION:
        issues.append(prefix + "profile_invalid")
    for field in ("specialist_id", "specialist_revision"):
        if not isinstance(evidence[field], str) or IDENTIFIER.fullmatch(evidence[field]) is None:
            issues.append(prefix + "identifier_invalid:" + field)
    if evidence["specialist_kind"] not in SPECIALIST_KINDS:
        issues.append(prefix + "specialist_kind_invalid")
    if evidence["supported_subtask_kind"] not in SUBTASK_KINDS:
        issues.append(prefix + "supported_subtask_invalid")
    issues.extend(prefix + item for item in _validate_binding(evidence, "binding"))
    if not isinstance(evidence["measurement_packet_digest"], str) or SHA256.fullmatch(evidence["measurement_packet_digest"]) is None:
        issues.append(prefix + "measurement_digest_invalid")
    for field in ("fit_score", "reliability_score", "estimated_cost_units", "utility_score", "evidence_created_epoch"):
        if not nonnegative_int(evidence[field]):
            issues.append(prefix + "integer_invalid:" + field)
    expected_utility = evidence["fit_score"] + evidence["reliability_score"] - evidence["estimated_cost_units"]
    if evidence["fit_score"] + evidence["reliability_score"] < evidence["estimated_cost_units"] or evidence["utility_score"] != expected_utility:
        issues.append(prefix + "utility_score_invalid")
    for field in (
        "independent_measurement", "route_hint_only", "repository_mutation_performed",
        "specialist_dispatched", "candidate_selected", "execution_authority_granted",
        "git_authority_granted", "correctness_claimed",
    ):
        if not isinstance(evidence[field], bool):
            issues.append(prefix + "boolean_invalid:" + field)
    if not digest_ok(evidence, SPECIALIST_DIGEST_FIELD):
        issues.append(prefix + "digest_mismatch")
    return sorted(set(issues))


def validate_specialists(specialists: Any) -> list[str]:
    if not isinstance(specialists, list):
        return ["specialists_not_list"]
    issues: list[str] = []
    ids: list[str] = []
    digests: list[str] = []
    for index, item in enumerate(specialists):
        if not isinstance(item, Mapping):
            issues.append(f"specialist:{index}:not_mapping")
            continue
        issues.extend(validate_specialist_evidence(item, index))
        ids.append(str(item.get("specialist_id", "")))
        digests.append(str(item.get(SPECIALIST_DIGEST_FIELD, "")))
    if len(ids) != len(set(ids)):
        issues.append("specialist_ids_not_unique")
    if len(digests) != len(set(digests)):
        issues.append("specialist_digests_not_unique")
    return sorted(set(issues))


__all__ = [
    "binding_mismatches", "validate_specialist_evidence", "validate_specialists",
    "validate_trajectory",
]
