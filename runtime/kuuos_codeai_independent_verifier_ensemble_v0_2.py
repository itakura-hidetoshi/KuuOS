from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from runtime.kuuos_codeai_independent_verifier_ensemble_checks_v0_2 import (
    canonical_digest,
    digest_without,
    exact_fields,
    exact_partition,
    mapping,
    nat,
    seal,
    strings,
    valid_sha40,
    valid_sha256,
)
from runtime.kuuos_codeai_independent_verifier_ensemble_schema_v0_2 import (
    ALLOWED_FAMILIES,
    ALLOWED_OUTCOMES,
    ALLOWED_SEVERITIES,
    DISPOSITION_ACCEPTED,
    DISPOSITION_DISAGREEMENT,
    DISPOSITION_FAILED,
    DISPOSITION_INCONCLUSIVE,
    ENSEMBLE_DIGEST_FIELD,
    EVIDENCE_DIGEST_FIELD,
    EVIDENCE_FIELDS,
    MODE_CONSENSUS_FAIL,
    MODE_CONSENSUS_PASS,
    MODE_DISAGREEMENT_HOLD,
    MODE_INCONCLUSIVE_HOLD,
    POLICY_DIGEST_FIELD,
    POLICY_FIELDS,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    REQUEST_FIELDS,
    STATUS_BLOCKED,
    STATUS_READY,
)


@dataclass(frozen=True)
class CodeAIIndependentVerifierEnsembleResult:
    status: str
    issues: tuple[str, ...]
    ensemble: dict[str, Any] | None
    receipt: dict[str, Any] | None


def _validate_request(value: Mapping[str, Any]) -> list[str]:
    issues = exact_fields(value, REQUEST_FIELDS, "ensemble_request")
    if issues:
        return issues
    for field in ("request_id", "request_revision", "repository_full_name"):
        if not isinstance(value[field], str) or not value[field]:
            issues.append("ensemble_request_invalid_string:" + field)
    if not valid_sha40(value["source_commit_sha"]):
        issues.append("ensemble_request_invalid_source_commit")
    for field in ("candidate_digest", "context_pack_digest"):
        if not valid_sha256(value[field]):
            issues.append("ensemble_request_invalid_digest:" + field)
    families = strings(value["required_check_families"], nonempty=True, sorted_unique=True)
    if families is None or any(item not in ALLOWED_FAMILIES for item in value["required_check_families"]):
        issues.append("ensemble_request_invalid_required_families")
    if nat(value["request_created_epoch"]) is None:
        issues.append("ensemble_request_invalid_created_epoch")
    if value[REQUEST_DIGEST_FIELD] != digest_without(value, REQUEST_DIGEST_FIELD):
        issues.append("ensemble_request_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = exact_fields(value, POLICY_FIELDS, "ensemble_policy")
    if issues:
        return issues
    if not isinstance(value["expected_repository_full_name"], str) or not value["expected_repository_full_name"]:
        issues.append("ensemble_policy_repository_invalid")
    if not valid_sha40(value["expected_source_commit_sha"]):
        issues.append("ensemble_policy_source_commit_invalid")
    for field in ("expected_candidate_digest", "expected_context_pack_digest"):
        if not valid_sha256(value[field]):
            issues.append("ensemble_policy_invalid_digest:" + field)
    for field in (
        "allowed_verifier_ids",
        "allowed_reviewer_ids",
        "allowed_runner_ids",
        "required_check_families",
    ):
        parsed = strings(value[field], nonempty=True, sorted_unique=True)
        if parsed is None:
            issues.append("ensemble_policy_invalid_string_list:" + field)
    if any(item not in ALLOWED_FAMILIES for item in value["required_check_families"]):
        issues.append("ensemble_policy_invalid_required_family")
    for field in (
        "minimum_verifier_count",
        "minimum_organization_count",
        "minimum_method_count",
        "minimum_pass_quorum",
        "minimum_fail_quorum",
        "maximum_evidence_age",
        "maximum_verification_duration",
    ):
        if nat(value[field], positive=True) is None:
            issues.append("ensemble_policy_invalid_positive_nat:" + field)
    if nat(value["maximum_skipped_checks"]) is None or nat(value["evaluation_epoch"]) is None:
        issues.append("ensemble_policy_invalid_nat")
    bool_fields = [field for field in POLICY_FIELDS if field.startswith("require_") or field.startswith("allow_")]
    bool_fields.extend(("critical_failure_overrides_quorum", "conflict_requires_hold"))
    for field in bool_fields:
        if not isinstance(value[field], bool):
            issues.append("ensemble_policy_invalid_bool:" + field)
    if value[POLICY_DIGEST_FIELD] != digest_without(value, POLICY_DIGEST_FIELD):
        issues.append("ensemble_policy_digest_mismatch")
    return issues


def _validate_evidence(value: Mapping[str, Any]) -> list[str]:
    issues = exact_fields(value, EVIDENCE_FIELDS, "verifier_evidence")
    if issues:
        return issues
    for field in (
        "evidence_id",
        "verifier_id",
        "reviewer_id",
        "runner_id",
        "organization_id",
        "verification_session_id",
        "nonce",
        "repository_full_name",
        "check_family",
        "highest_severity",
        "declared_outcome",
    ):
        if not isinstance(value[field], str) or not value[field]:
            issues.append("verifier_evidence_invalid_string:" + field)
    if value["check_family"] not in ALLOWED_FAMILIES:
        issues.append("verifier_evidence_invalid_family")
    if value["declared_outcome"] not in ALLOWED_OUTCOMES:
        issues.append("verifier_evidence_invalid_outcome")
    if value["highest_severity"] not in ALLOWED_SEVERITIES:
        issues.append("verifier_evidence_invalid_severity")
    if not valid_sha40(value["source_commit_sha"]):
        issues.append("verifier_evidence_invalid_source_commit")
    for field in (
        "candidate_digest",
        "context_pack_digest",
        "verification_method_digest",
        "environment_digest",
        "toolchain_digest",
        "protocol_digest",
        "evidence_artifact_digest",
    ):
        if not valid_sha256(value[field]):
            issues.append("verifier_evidence_invalid_digest:" + field)
    partitions: dict[str, tuple[str, ...]] = {}
    for field in ("check_ids", "passed_check_ids", "failed_check_ids", "skipped_check_ids", "finding_labels"):
        parsed = strings(value[field], nonempty=(field == "check_ids"), sorted_unique=True)
        if parsed is None:
            issues.append("verifier_evidence_invalid_string_list:" + field)
        else:
            partitions[field] = parsed
    if all(field in partitions for field in ("check_ids", "passed_check_ids", "failed_check_ids", "skipped_check_ids")):
        if not exact_partition(
            partitions["check_ids"],
            partitions["passed_check_ids"],
            partitions["failed_check_ids"],
            partitions["skipped_check_ids"],
        ):
            issues.append("verifier_evidence_check_partition_invalid")
    for field in (
        "falsification_executed",
        "falsification_passed",
        "acceptance_criteria_satisfied",
        "independent_from_candidate_producer",
        "independent_from_other_verifiers",
        "prompt_lineage_independent",
        "repair_memory_independent",
        "test_generation_independent",
        "isolated_execution_reported",
        "kernel_executed_verification",
        "repository_mutation_performed",
        "candidate_selection_performed",
        "execution_authority_granted",
        "git_authority_granted",
        "correctness_proof_claimed",
    ):
        if not isinstance(value[field], bool):
            issues.append("verifier_evidence_invalid_bool:" + field)
    started = nat(value["verification_started_epoch"])
    completed = nat(value["verification_completed_epoch"])
    if started is None or completed is None or (started is not None and completed is not None and completed < started):
        issues.append("verifier_evidence_window_invalid")
    failed = value.get("failed_check_ids", [])
    skipped = value.get("skipped_check_ids", [])
    if value["declared_outcome"] == "passed":
        if failed or skipped or not value["acceptance_criteria_satisfied"]:
            issues.append("verifier_evidence_pass_inconsistent")
        if value["falsification_executed"] and not value["falsification_passed"]:
            issues.append("verifier_evidence_pass_falsification_inconsistent")
    elif value["declared_outcome"] == "failed":
        if not failed and value["acceptance_criteria_satisfied"] and (
            not value["falsification_executed"] or value["falsification_passed"]
        ):
            issues.append("verifier_evidence_fail_inconsistent")
    elif value["declared_outcome"] == "inconclusive":
        if not skipped:
            issues.append("verifier_evidence_inconclusive_without_skipped_check")
    if value[EVIDENCE_DIGEST_FIELD] != digest_without(value, EVIDENCE_DIGEST_FIELD):
        issues.append("verifier_evidence_digest_mismatch")
    return issues


def _blocked(issues: Sequence[str]) -> CodeAIIndependentVerifierEnsembleResult:
    return CodeAIIndependentVerifierEnsembleResult(STATUS_BLOCKED, tuple(issues), None, None)


def evaluate_independent_verifier_ensemble(
    request: Mapping[str, Any], policy: Mapping[str, Any], evidence_packets: Sequence[Mapping[str, Any]]
) -> CodeAIIndependentVerifierEnsembleResult:
    issues: list[str] = []
    request_map = mapping(request)
    policy_map = mapping(policy)
    if request_map is None:
        issues.append("ensemble_request_not_object")
    else:
        issues.extend(_validate_request(request_map))
    if policy_map is None:
        issues.append("ensemble_policy_not_object")
    else:
        issues.extend(_validate_policy(policy_map))
    if not isinstance(evidence_packets, list) or not evidence_packets:
        issues.append("verifier_evidence_packets_invalid")
        evidence_maps: list[Mapping[str, Any]] = []
    else:
        evidence_maps = []
        for index, packet in enumerate(evidence_packets):
            packet_map = mapping(packet)
            if packet_map is None:
                issues.append(f"verifier_evidence_not_object:{index}")
            else:
                evidence_maps.append(packet_map)
                issues.extend(f"evidence[{index}]:{issue}" for issue in _validate_evidence(packet_map))
    if issues:
        return _blocked(issues)
    assert request_map is not None and policy_map is not None

    bindings = (
        ("repository_full_name", "expected_repository_full_name"),
        ("source_commit_sha", "expected_source_commit_sha"),
        ("candidate_digest", "expected_candidate_digest"),
        ("context_pack_digest", "expected_context_pack_digest"),
    )
    for request_field, policy_field in bindings:
        if request_map[request_field] != policy_map[policy_field]:
            issues.append("ensemble_request_policy_binding_mismatch:" + request_field)
    if request_map["required_check_families"] != policy_map["required_check_families"]:
        issues.append("ensemble_required_family_binding_mismatch")
    evaluation_epoch = policy_map["evaluation_epoch"]
    if request_map["request_created_epoch"] > evaluation_epoch:
        issues.append("ensemble_request_from_future")
    elif evaluation_epoch - request_map["request_created_epoch"] > policy_map["maximum_evidence_age"]:
        issues.append("ensemble_request_stale")

    verifier_ids = [item["verifier_id"] for item in evidence_maps]
    organizations = [item["organization_id"] for item in evidence_maps]
    sessions = [item["verification_session_id"] for item in evidence_maps]
    methods = [item["verification_method_digest"] for item in evidence_maps]
    evidence_ids = [item["evidence_id"] for item in evidence_maps]
    families = [item["check_family"] for item in evidence_maps]

    if len(evidence_maps) < policy_map["minimum_verifier_count"]:
        issues.append("ensemble_insufficient_verifier_count")
    if len(set(organizations)) < policy_map["minimum_organization_count"]:
        issues.append("ensemble_insufficient_organization_count")
    if len(set(methods)) < policy_map["minimum_method_count"]:
        issues.append("ensemble_insufficient_method_count")
    if policy_map["require_distinct_verifiers"] and len(verifier_ids) != len(set(verifier_ids)):
        issues.append("ensemble_duplicate_verifier")
    if policy_map["require_distinct_sessions"] and len(sessions) != len(set(sessions)):
        issues.append("ensemble_duplicate_session")
    if policy_map["require_distinct_organizations"] and len(organizations) != len(set(organizations)):
        issues.append("ensemble_duplicate_organization")
    if len(evidence_ids) != len(set(evidence_ids)):
        issues.append("ensemble_duplicate_evidence_id")
    if not set(policy_map["required_check_families"]).issubset(set(families)):
        issues.append("ensemble_required_family_missing")
    for index, item in enumerate(evidence_maps):
        for field in ("repository_full_name", "source_commit_sha", "candidate_digest", "context_pack_digest"):
            if item[field] != request_map[field]:
                issues.append(f"evidence[{index}]:binding_mismatch:{field}")
        if item["verifier_id"] not in policy_map["allowed_verifier_ids"]:
            issues.append(f"evidence[{index}]:verifier_not_allowed")
        if item["reviewer_id"] not in policy_map["allowed_reviewer_ids"]:
            issues.append(f"evidence[{index}]:reviewer_not_allowed")
        if item["runner_id"] not in policy_map["allowed_runner_ids"]:
            issues.append(f"evidence[{index}]:runner_not_allowed")
        if item["verification_completed_epoch"] > evaluation_epoch:
            issues.append(f"evidence[{index}]:verification_from_future")
        elif evaluation_epoch - item["verification_completed_epoch"] > policy_map["maximum_evidence_age"]:
            issues.append(f"evidence[{index}]:verification_stale")
        if item["verification_completed_epoch"] - item["verification_started_epoch"] > policy_map["maximum_verification_duration"]:
            issues.append(f"evidence[{index}]:verification_duration_exceeded")
        if len(item["skipped_check_ids"]) > policy_map["maximum_skipped_checks"]:
            issues.append(f"evidence[{index}]:too_many_skipped_checks")
        independence_requirements = (
            ("require_producer_independence", "independent_from_candidate_producer"),
            ("require_peer_independence", "independent_from_other_verifiers"),
            ("require_prompt_independence", "prompt_lineage_independent"),
            ("require_memory_independence", "repair_memory_independent"),
            ("require_test_generation_independence", "test_generation_independent"),
        )
        for policy_field, evidence_field in independence_requirements:
            if policy_map[policy_field] and not item[evidence_field]:
                issues.append(f"evidence[{index}]:independence_requirement_failed:{evidence_field}")
        if item["kernel_executed_verification"]:
            issues.append(f"evidence[{index}]:kernel_execution_forbidden")
        if item["repository_mutation_performed"] or policy_map["allow_repository_mutation"]:
            issues.append(f"evidence[{index}]:repository_mutation_forbidden")
        if item["candidate_selection_performed"] or policy_map["allow_candidate_selection_authority"]:
            issues.append(f"evidence[{index}]:candidate_selection_forbidden")
        if item["execution_authority_granted"] or policy_map["allow_execution_authority"]:
            issues.append(f"evidence[{index}]:execution_authority_forbidden")
        if item["git_authority_granted"] or policy_map["allow_git_authority"]:
            issues.append(f"evidence[{index}]:git_authority_forbidden")
        if item["correctness_proof_claimed"]:
            issues.append(f"evidence[{index}]:correctness_proof_claim_forbidden")
    if policy_map["allow_network_access"] or policy_map["allow_secret_access"]:
        issues.append("ensemble_policy_forbidden_access")
    if issues:
        return _blocked(issues)

    pass_count = sum(item["declared_outcome"] == "passed" for item in evidence_maps)
    fail_count = sum(item["declared_outcome"] == "failed" for item in evidence_maps)
    inconclusive_count = sum(item["declared_outcome"] == "inconclusive" for item in evidence_maps)
    skipped_count = sum(len(item["skipped_check_ids"]) for item in evidence_maps)
    critical_failure_count = sum(
        item["declared_outcome"] == "failed" and item["highest_severity"] == "critical"
        for item in evidence_maps
    )
    conflict = pass_count > 0 and fail_count > 0

    if policy_map["critical_failure_overrides_quorum"] and critical_failure_count > 0:
        disposition = DISPOSITION_FAILED
        mode = MODE_CONSENSUS_FAIL
        consensus_outcome = "failed"
    elif policy_map["conflict_requires_hold"] and conflict:
        disposition = DISPOSITION_DISAGREEMENT
        mode = MODE_DISAGREEMENT_HOLD
        consensus_outcome = "disagreement"
    elif fail_count >= policy_map["minimum_fail_quorum"]:
        disposition = DISPOSITION_FAILED
        mode = MODE_CONSENSUS_FAIL
        consensus_outcome = "failed"
    elif pass_count >= policy_map["minimum_pass_quorum"] and inconclusive_count == 0:
        disposition = DISPOSITION_ACCEPTED
        mode = MODE_CONSENSUS_PASS
        consensus_outcome = "passed"
    else:
        disposition = DISPOSITION_INCONCLUSIVE
        mode = MODE_INCONCLUSIVE_HOLD
        consensus_outcome = "inconclusive"

    evidence_digests = sorted(item[EVIDENCE_DIGEST_FIELD] for item in evidence_maps)
    ensemble = seal(
        {
            "ensemble_id": request_map["request_id"],
            "repository_full_name": request_map["repository_full_name"],
            "source_commit_sha": request_map["source_commit_sha"],
            "candidate_digest": request_map["candidate_digest"],
            "context_pack_digest": request_map["context_pack_digest"],
            "request_digest": request_map[REQUEST_DIGEST_FIELD],
            "policy_digest": policy_map[POLICY_DIGEST_FIELD],
            "evidence_digests": evidence_digests,
            "verifier_count": len(evidence_maps),
            "organization_count": len(set(organizations)),
            "method_count": len(set(methods)),
            "covered_check_families": sorted(set(families)),
            "pass_count": pass_count,
            "fail_count": fail_count,
            "inconclusive_count": inconclusive_count,
            "skipped_check_count": skipped_count,
            "critical_failure_count": critical_failure_count,
            "conflict_detected": conflict,
            "consensus_outcome": consensus_outcome,
            "producer_independence_verified": all(item["independent_from_candidate_producer"] for item in evidence_maps),
            "peer_independence_verified": all(item["independent_from_other_verifiers"] for item in evidence_maps),
            "prompt_independence_verified": all(item["prompt_lineage_independent"] for item in evidence_maps),
            "memory_independence_verified": all(item["repair_memory_independent"] for item in evidence_maps),
            "test_generation_independence_verified": all(item["test_generation_independent"] for item in evidence_maps),
            "repository_mutation_performed": False,
            "candidate_selection_performed": False,
            "execution_authority_granted": False,
            "git_authority_granted": False,
            "correctness_proof_claimed": False,
        },
        ENSEMBLE_DIGEST_FIELD,
    )
    receipt = seal(
        {
            "codeai_disposition": disposition,
            "operating_mode": mode,
            "repository_full_name": request_map["repository_full_name"],
            "source_commit_sha": request_map["source_commit_sha"],
            "candidate_digest": request_map["candidate_digest"],
            "context_pack_digest": request_map["context_pack_digest"],
            "ensemble_digest": ensemble[ENSEMBLE_DIGEST_FIELD],
            "consensus_outcome": consensus_outcome,
            "verification_debt_open": mode in {MODE_DISAGREEMENT_HOLD, MODE_INCONCLUSIVE_HOLD},
            "reverification_required": mode in {MODE_DISAGREEMENT_HOLD, MODE_INCONCLUSIVE_HOLD},
            "candidate_accepted": False,
            "candidate_rejected": False,
            "repository_mutation_performed": False,
            "candidate_selection_authority": False,
            "execution_authority": False,
            "git_authority": False,
            "truth_authority": False,
            "correctness_proof": False,
        },
        RECEIPT_DIGEST_FIELD,
    )
    return CodeAIIndependentVerifierEnsembleResult(STATUS_READY, (), ensemble, receipt)


__all__ = [
    "CodeAIIndependentVerifierEnsembleResult",
    "evaluate_independent_verifier_ensemble",
    "canonical_digest",
    "seal",
]
