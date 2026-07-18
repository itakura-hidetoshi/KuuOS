#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping, Sequence

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD as PATCH_CANDIDATE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CANDIDATE_RECEIPT_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    seal,
)
from runtime.kuuos_codeai_autonomous_isolated_candidate_application_v0_1 import (
    RECEIPT_DIGEST_FIELD as APPLICATION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_verification_execution_v0_1 import (
    CANDIDATE_DIGEST_FIELD as RECEIPT_CANDIDATE_DIGEST_FIELD,
    EVIDENCE_BUNDLE_DIGEST_FIELD,
    INDEPENDENT_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as VERIFICATION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_candidate_regeneration_common_v0_1 import (
    POLICY_DIGEST_FIELD as DOWNSTREAM_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as REGENERATION_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as DOWNSTREAM_REQUEST_DIGEST_FIELD,
    source_digest_field,
)
from runtime.kuuos_codeai_autonomous_candidate_regeneration_v0_1 import (
    STATUS_READY as REGENERATION_STATUS_READY,
    build_codeai_autonomous_candidate_regeneration,
)

VERSION = "kuuos_codeai_verification_guided_candidate_repair_regeneration_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Verification-Guided Candidate Repair and Regeneration v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_BOUNDED_FEEDBACK_REGENERATION = "bounded_verification_feedback_regeneration"
DISPOSITION_REGENERATED = "verification_guided_candidate_repair_regenerated"
DISPOSITION_NO_NOVEL_CANDIDATE = "verification_guided_candidate_repair_exhausted_without_novel_candidate"
REQUEST_DIGEST_FIELD = "codeai_verification_guided_candidate_repair_regeneration_request_digest"
POLICY_DIGEST_FIELD = "codeai_verification_guided_candidate_repair_regeneration_policy_digest"
NORMALIZED_FEEDBACK_DIGEST_FIELD = "codeai_verification_guided_candidate_repair_feedback_digest"
RECEIPT_DIGEST_FIELD = "codeai_verification_guided_candidate_repair_regeneration_receipt_digest"

REQUEST_FIELDS = {
    "request_id", "request_revision",
    "source_verification_execution_receipt_digest",
    "source_evidence_bundle_digest",
    "source_independent_verification_evidence_digest",
    "source_candidate_receipt_digest", "source_application_receipt_digest",
    "source_generation_receipt_digest", "source_observation_receipt_digest",
    "candidate_digest", "patch_artifact_digest", "repository_full_name",
    "source_commit_sha", "repair_intent_text", "target_unique_candidate_count",
    "maximum_repair_rounds_requested", "diversity_axes",
    "requirement_trace_ids", "test_plan_ids", "risk_labels",
    "unresolved_candidate_questions", "request_created_epoch", REQUEST_DIGEST_FIELD,
}
POLICY_FIELDS = {
    "expected_source_verification_execution_receipt_digest",
    "expected_source_evidence_bundle_digest",
    "expected_source_independent_verification_evidence_digest",
    "expected_source_candidate_receipt_digest",
    "expected_source_application_receipt_digest",
    "expected_source_generation_receipt_digest",
    "expected_source_observation_receipt_digest",
    "expected_candidate_digest", "expected_patch_artifact_digest",
    "expected_repository_full_name", "expected_source_commit_sha",
    "allowed_verification_dispositions", "allowed_execution_statuses",
    "allowed_check_ids", "allowed_finding_labels",
    "allowed_failure_reason_prefixes", "allowed_diversity_axes",
    "allowed_provider_ids", "maximum_repair_rounds",
    "maximum_provider_calls_per_round", "maximum_total_provider_calls",
    "maximum_added_candidates", "maximum_total_candidates",
    "maximum_feedback_records", "maximum_failure_reasons_per_record",
    "maximum_excerpt_bytes_per_stream", "maximum_total_feedback_bytes",
    "maximum_raw_output_bytes", "maximum_intent_bytes",
    "maximum_repository_snapshot_bytes", "maximum_existing_candidates",
    "maximum_unique_candidates", "evaluation_epoch", "maximum_response_age",
    "maximum_request_age", "allowed_repository_path_prefixes",
    "forbidden_repository_path_prefixes", "network_access_allowed",
    "secrets_allowed", "live_repository_access_allowed",
    "git_operations_allowed", POLICY_DIGEST_FIELD,
}

@dataclass(frozen=True)
class CodeAIVerificationGuidedCandidateRepairRegenerationResult:
    status: str
    issues: tuple[str, ...]
    normalized_feedback: dict[str, Any] | None
    downstream_regeneration: Any | None
    receipt: dict[str, Any] | None

def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None

def _nat(value: Any, *, positive: bool = False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return None if positive and value == 0 else value

def _strings(value: Any, *, nonempty: bool = False) -> list[str] | None:
    if not isinstance(value, list) or not all(isinstance(x, str) and x for x in value):
        return None
    return None if len(value) != len(set(value)) or (nonempty and not value) else list(value)

def _digest_ok(value: Mapping[str, Any], field: str) -> bool:
    return value.get(field) == canonical_digest({k: v for k, v in value.items() if k != field})

def _exact(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues = []
    missing, extra = fields.difference(value), set(value).difference(fields)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues

def _sealed(value: Any, field: str, prefix: str):
    item = _mapping(value)
    if item is None:
        return None, [prefix + "_not_mapping"]
    return item, [] if _digest_ok(item, field) else [prefix + "_digest_mismatch"]

def _snapshot_bytes(repository: Mapping[str, str]) -> int:
    return sum(len(k.encode()) + len(v.encode()) for k, v in repository.items())

def _bounded(value: str, maximum: int) -> tuple[str, bool]:
    raw = value.encode()
    if len(raw) <= maximum:
        return value, False
    return raw[:maximum].decode(errors="ignore"), True

def _validate_request(value: Any):
    request = _mapping(value)
    if request is None:
        return None, ["repair_request_not_mapping"]
    issues = _exact(request, REQUEST_FIELDS, "repair_request")
    if issues:
        return request, issues
    string_fields = REQUEST_FIELDS - {
        "target_unique_candidate_count", "maximum_repair_rounds_requested",
        "diversity_axes", "requirement_trace_ids", "test_plan_ids",
        "risk_labels", "unresolved_candidate_questions",
        "request_created_epoch", REQUEST_DIGEST_FIELD,
    }
    for field in string_fields:
        if not isinstance(request[field], str) or not request[field]:
            issues.append("repair_request_invalid_string:" + field)
    for field in ("target_unique_candidate_count", "maximum_repair_rounds_requested"):
        if _nat(request[field], positive=True) is None:
            issues.append("repair_request_invalid_positive_nat:" + field)
    for field in ("diversity_axes", "requirement_trace_ids", "test_plan_ids",
                  "risk_labels", "unresolved_candidate_questions"):
        if _strings(request[field], nonempty=field in {"diversity_axes", "requirement_trace_ids"}) is None:
            issues.append("repair_request_invalid_string_list:" + field)
    if _nat(request["request_created_epoch"]) is None:
        issues.append("repair_request_invalid_created_epoch")
    if not _digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("repair_request_digest_mismatch")
    return request, issues

def _validate_policy(value: Any):
    policy = _mapping(value)
    if policy is None:
        return None, ["repair_policy_not_mapping"]
    issues = _exact(policy, POLICY_FIELDS, "repair_policy")
    if issues:
        return policy, issues
    list_fields = {
        "allowed_verification_dispositions", "allowed_execution_statuses",
        "allowed_check_ids", "allowed_finding_labels",
        "allowed_failure_reason_prefixes", "allowed_diversity_axes",
        "allowed_provider_ids", "allowed_repository_path_prefixes",
        "forbidden_repository_path_prefixes",
    }
    bool_fields = {"network_access_allowed", "secrets_allowed",
                   "live_repository_access_allowed", "git_operations_allowed"}
    digest_fields = {POLICY_DIGEST_FIELD}
    nat_fields = {
        "maximum_repair_rounds", "maximum_provider_calls_per_round",
        "maximum_total_provider_calls", "maximum_added_candidates",
        "maximum_total_candidates", "maximum_feedback_records",
        "maximum_failure_reasons_per_record", "maximum_excerpt_bytes_per_stream",
        "maximum_total_feedback_bytes", "maximum_raw_output_bytes",
        "maximum_intent_bytes", "maximum_repository_snapshot_bytes",
        "maximum_existing_candidates", "maximum_unique_candidates",
        "evaluation_epoch", "maximum_response_age", "maximum_request_age",
    }
    for field in POLICY_FIELDS - list_fields - bool_fields - digest_fields - nat_fields:
        if not isinstance(policy[field], str) or not policy[field]:
            issues.append("repair_policy_invalid_string:" + field)
    for field in list_fields:
        if _strings(policy[field], nonempty=field not in {"allowed_finding_labels", "forbidden_repository_path_prefixes"}) is None:
            issues.append("repair_policy_invalid_string_list:" + field)
    for field in nat_fields:
        if _nat(policy[field], positive=field != "evaluation_epoch") is None:
            issues.append("repair_policy_invalid_nat:" + field)
    for field in bool_fields:
        if policy[field] is not False:
            issues.append("repair_policy_required_false:" + field)
    if not _digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("repair_policy_digest_mismatch")
    return policy, issues

def _seed_digests(seed_candidates: Any):
    if not isinstance(seed_candidates, Sequence) or isinstance(seed_candidates, (str, bytes)):
        return [], ["seed_candidates_not_sequence"]
    digests, issues = [], []
    for index, item in enumerate(seed_candidates):
        patch = getattr(item, "patch_candidate", None)
        digest = patch.get(PATCH_CANDIDATE_DIGEST_FIELD) if isinstance(patch, Mapping) else None
        if not isinstance(digest, str) or not digest:
            issues.append(f"seed_candidate[{index}]_digest_invalid")
        else:
            digests.append(digest)
    if len(digests) != len(set(digests)):
        issues.append("seed_candidate_digest_duplicate")
    return digests, issues

def _reason_ids(record: Mapping[str, Any]) -> list[str]:
    values = ["execution_status:" + str(record.get("execution_status", ""))]
    if record.get("timed_out") is True:
        values.append("timed_out")
    if isinstance(record.get("exception_type"), str) and record["exception_type"]:
        values.append("exception_type:" + record["exception_type"])
    if isinstance(record.get("exit_code"), int) and not isinstance(record["exit_code"], bool):
        values.append("exit_code:" + str(record["exit_code"]))
    for field, label in (
        ("network_used", "forbidden_effect:network"),
        ("secret_accessed", "forbidden_effect:secret"),
        ("live_repository_accessed", "forbidden_effect:live_repository"),
        ("git_effect_performed", "forbidden_effect:git"),
    ):
        if record.get(field) is True:
            values.append(label)
    rejected = record.get("runner_result_rejection_reasons")
    if isinstance(rejected, list):
        values.extend("runner_result:" + x for x in rejected if isinstance(x, str) and x)
    return list(dict.fromkeys(values))

def _normalize_feedback(evidence: Mapping[str, Any],
                        independent: Mapping[str, Any],
                        policy: Mapping[str, Any]):
    records = evidence.get("records")
    if not isinstance(records, list):
        return None, ["source_evidence_records_not_list"]
    issues, normalized = [], []
    allowed_checks = set(policy["allowed_check_ids"])
    allowed_statuses = set(policy["allowed_execution_statuses"])
    prefixes = list(policy["allowed_failure_reason_prefixes"])
    max_reasons = int(policy["maximum_failure_reasons_per_record"])
    max_excerpt = int(policy["maximum_excerpt_bytes_per_stream"])
    for record in records:
        if not isinstance(record, Mapping):
            issues.append("source_evidence_record_not_mapping")
            continue
        status = record.get("execution_status")
        if status == "passed":
            continue
        check_id = record.get("check_id")
        if not isinstance(check_id, str) or not check_id:
            issues.append("source_evidence_failed_check_id_invalid")
            continue
        if check_id not in allowed_checks:
            issues.append("repair_feedback_check_not_allowed:" + check_id)
            continue
        if status not in allowed_statuses:
            issues.append("repair_feedback_status_not_allowed:" + str(status))
            continue
        reasons = [x for x in _reason_ids(record)
                   if any(x == p or x.startswith(p) for p in prefixes)]
        if not reasons:
            issues.append("repair_feedback_has_no_allowed_reason:" + check_id)
            continue
        stdout, stdout_cut = _bounded(str(record.get("stdout_excerpt", "")), max_excerpt)
        stderr, stderr_cut = _bounded(str(record.get("stderr_excerpt", "")), max_excerpt)
        normalized.append({
            "check_id": check_id,
            "execution_status": status,
            "failure_reason_ids": reasons[:max_reasons],
            "exit_code": record.get("exit_code"),
            "stdout_digest": record.get("stdout_digest", ""),
            "stderr_digest": record.get("stderr_digest", ""),
            "stdout_excerpt": stdout,
            "stderr_excerpt": stderr,
            "stdout_excerpt_truncated_by_repair_boundary": stdout_cut,
            "stderr_excerpt_truncated_by_repair_boundary": stderr_cut,
            "timed_out": record.get("timed_out") is True,
            "exception_type": record.get("exception_type"),
            "source_record_digest": record.get("record_digest", ""),
        })
    if not normalized:
        issues.append("repair_feedback_has_no_admissible_failed_record")
    if len(normalized) > int(policy["maximum_feedback_records"]):
        issues.append("repair_feedback_record_budget_exceeded")
    labels = independent.get("finding_labels")
    if not isinstance(labels, list) or not all(isinstance(x, str) for x in labels):
        labels, issues = [], issues + ["source_independent_finding_labels_invalid"]
    allowed_labels = set(policy["allowed_finding_labels"])
    rejected = [x for x in labels if x not in allowed_labels]
    if rejected:
        issues.append("repair_feedback_finding_labels_not_allowed:" + ",".join(sorted(set(rejected))))
    value = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_evidence_bundle_digest": evidence[EVIDENCE_BUNDLE_DIGEST_FIELD],
        "source_independent_verification_evidence_digest":
            independent[INDEPENDENT_EVIDENCE_DIGEST_FIELD],
        "failed_check_ids": [x["check_id"] for x in normalized],
        "finding_labels": [x for x in labels if x in allowed_labels],
        "feedback_records": normalized,
        "feedback_record_count": len(normalized),
        "feedback_treated_as_truth": False,
        "failed_check_treated_as_required_edit": False,
        "repair_authority_granted": False,
    }, NORMALIZED_FEEDBACK_DIGEST_FIELD)
    size = len(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())
    if size > int(policy["maximum_total_feedback_bytes"]):
        issues.append("repair_feedback_total_byte_budget_exceeded")
    return value, issues

def _correspondence(*, verification, evidence, independent, generation,
                    observation, candidate, application, repository,
                    seed_digests, request, policy, generation_digest_field):
    issues = []
    vr = verification[VERIFICATION_RECEIPT_DIGEST_FIELD]
    eb = evidence[EVIDENCE_BUNDLE_DIGEST_FIELD]
    iv = independent[INDEPENDENT_EVIDENCE_DIGEST_FIELD]
    gr = generation[generation_digest_field]
    ob = observation[SOURCE_RECEIPT_DIGEST_FIELD]
    cr = candidate[CANDIDATE_RECEIPT_DIGEST_FIELD]
    ar = application[APPLICATION_RECEIPT_DIGEST_FIELD]
    cd = candidate[RECEIPT_CANDIDATE_DIGEST_FIELD]
    pa = candidate["patch_artifact_digest"]
    rs = canonical_digest(repository)
    pairs = (
        (request["source_verification_execution_receipt_digest"], vr, "request_verification"),
        (request["source_evidence_bundle_digest"], eb, "request_evidence"),
        (request["source_independent_verification_evidence_digest"], iv, "request_independent"),
        (request["source_candidate_receipt_digest"], cr, "request_candidate_receipt"),
        (request["source_application_receipt_digest"], ar, "request_application"),
        (request["source_generation_receipt_digest"], gr, "request_generation"),
        (request["source_observation_receipt_digest"], ob, "request_observation"),
        (request["candidate_digest"], cd, "request_candidate"),
        (request["patch_artifact_digest"], pa, "request_artifact"),
        (request["repository_full_name"], candidate["repository_full_name"], "request_repository"),
        (request["source_commit_sha"], candidate["source_commit_sha"], "request_commit"),
        (policy["expected_source_verification_execution_receipt_digest"], vr, "policy_verification"),
        (policy["expected_source_evidence_bundle_digest"], eb, "policy_evidence"),
        (policy["expected_source_independent_verification_evidence_digest"], iv, "policy_independent"),
        (policy["expected_source_candidate_receipt_digest"], cr, "policy_candidate_receipt"),
        (policy["expected_source_application_receipt_digest"], ar, "policy_application"),
        (policy["expected_source_generation_receipt_digest"], gr, "policy_generation"),
        (policy["expected_source_observation_receipt_digest"], ob, "policy_observation"),
        (policy["expected_candidate_digest"], cd, "policy_candidate"),
        (policy["expected_patch_artifact_digest"], pa, "policy_artifact"),
        (policy["expected_repository_full_name"], candidate["repository_full_name"], "policy_repository"),
        (policy["expected_source_commit_sha"], candidate["source_commit_sha"], "policy_commit"),
        (verification.get("source_candidate_receipt_digest"), cr, "verification_candidate_receipt"),
        (verification.get("source_application_receipt_digest"), ar, "verification_application"),
        (verification.get("candidate_digest"), cd, "verification_candidate"),
        (verification.get("patch_artifact_digest"), pa, "verification_artifact"),
        (verification.get("evidence_bundle_digest"), eb, "verification_evidence"),
        (verification.get("independent_verification_evidence_digest"), iv, "verification_independent"),
        (independent.get("source_candidate_receipt_digest"), cr, "independent_candidate_receipt"),
        (independent.get("candidate_patch_digest"), cd, "independent_candidate"),
        (application.get("source_candidate_receipt_digest"), cr, "application_candidate_receipt"),
        (application.get("selected_candidate_digest"), cd, "application_candidate"),
        (application.get("selected_patch_artifact_digest"), pa, "application_artifact"),
        (application.get("source_repository_snapshot_digest"), rs, "application_source_snapshot"),
    )
    for actual, expected, label in pairs:
        if actual != expected:
            issues.append("repair_correspondence_mismatch:" + label)
    if cd not in seed_digests:
        issues.append("selected_candidate_missing_from_seed_lineage")
    disposition = verification.get("codeai_disposition")
    if disposition not in {"verification_execution_completed_with_failures",
                            "verification_execution_aborted_by_runtime_budget"}:
        issues.append("source_verification_not_failed_or_aborted")
    if disposition not in set(policy["allowed_verification_dispositions"]):
        issues.append("source_verification_disposition_not_allowed")
    if int(verification.get("failed_check_count", 0)) <= 0 or int(evidence.get("failed_check_count", 0)) <= 0:
        issues.append("source_verification_has_no_failed_checks")
    if independent.get("declared_verification_outcome") not in {"failed", "inconclusive"}:
        issues.append("source_independent_outcome_not_repairable")
    if independent.get("acceptance_criteria_satisfied") is not False:
        issues.append("source_independent_acceptance_already_satisfied")
    epoch, created = int(policy["evaluation_epoch"]), int(request["request_created_epoch"])
    if not epoch - int(policy["maximum_request_age"]) <= created <= epoch:
        issues.append("repair_request_window_invalid")
    if int(request["maximum_repair_rounds_requested"]) > int(policy["maximum_repair_rounds"]):
        issues.append("repair_round_budget_exceeded")
    if int(request["target_unique_candidate_count"]) > int(policy["maximum_total_candidates"]):
        issues.append("repair_target_candidate_budget_exceeded")
    if not set(request["diversity_axes"]).issubset(set(policy["allowed_diversity_axes"])):
        issues.append("repair_diversity_axis_not_allowed")
    if _snapshot_bytes(repository) > int(policy["maximum_repository_snapshot_bytes"]):
        issues.append("repair_repository_snapshot_budget_exceeded")
    if len(seed_digests) > int(policy["maximum_existing_candidates"]):
        issues.append("repair_existing_candidate_budget_exceeded")
    if len(seed_digests) >= int(policy["maximum_total_candidates"]):
        issues.append("repair_no_candidate_capacity")
    return issues

def _downstream_request(request: Mapping[str, Any], policy: Mapping[str, Any],
                        feedback: Mapping[str, Any], seed_digests: Sequence[str]):
    reasons = ["verification_guided_repair"]
    reasons += ["finding_label:" + x for x in feedback["finding_labels"]]
    for record in feedback["feedback_records"]:
        reasons.extend(record["failure_reason_ids"])
    reasons = list(dict.fromkeys(reasons))
    max_items = int(policy["maximum_feedback_records"]) * int(
        policy["maximum_failure_reasons_per_record"]
    ) + len(policy["allowed_finding_labels"]) + 1
    context = json.dumps(feedback, sort_keys=True, separators=(",", ":"))
    intent, _ = _bounded(
        request["repair_intent_text"]
        + "\n\nBounded verification feedback (context only; not truth or required edits):\n"
        + context,
        int(policy["maximum_intent_bytes"]),
    )
    target = min(
        int(request["target_unique_candidate_count"]),
        len(seed_digests) + int(policy["maximum_added_candidates"]),
        int(policy["maximum_total_candidates"]),
    )
    return seal({
        "request_id": request["request_id"] + ":downstream-regeneration",
        "request_revision": request["request_revision"],
        "intent_text": intent,
        "target_unique_candidate_count": target,
        "maximum_rounds_requested": int(request["maximum_repair_rounds_requested"]),
        "request_created_epoch": int(request["request_created_epoch"]),
        "feedback_reasons": reasons[:max_items],
        "diversity_axes": list(request["diversity_axes"]),
        "requirement_trace_ids": list(request["requirement_trace_ids"]),
        "test_plan_ids": list(request["test_plan_ids"]),
        "risk_labels": list(request["risk_labels"]),
        "unresolved_candidate_questions": list(request["unresolved_candidate_questions"]),
        "prior_candidate_digests": list(seed_digests),
        "prior_producer_session_ids": [],
    }, DOWNSTREAM_REQUEST_DIGEST_FIELD)

def _downstream_policy(policy: Mapping[str, Any]):
    return seal({
        "allowed_provider_ids": list(policy["allowed_provider_ids"]),
        "allowed_diversity_axes": list(policy["allowed_diversity_axes"]),
        "maximum_rounds": int(policy["maximum_repair_rounds"]),
        "maximum_provider_calls_per_round": int(policy["maximum_provider_calls_per_round"]),
        "maximum_total_provider_calls": int(policy["maximum_total_provider_calls"]),
        "maximum_raw_output_bytes": int(policy["maximum_raw_output_bytes"]),
        "maximum_intent_bytes": int(policy["maximum_intent_bytes"]),
        "maximum_repository_snapshot_bytes": int(policy["maximum_repository_snapshot_bytes"]),
        "maximum_feedback_items": int(policy["maximum_feedback_records"])
            * int(policy["maximum_failure_reasons_per_record"])
            + len(policy["allowed_finding_labels"]) + 1,
        "maximum_existing_candidates": int(policy["maximum_existing_candidates"]),
        "maximum_unique_candidates": min(int(policy["maximum_unique_candidates"]),
                                         int(policy["maximum_total_candidates"])),
        "evaluation_epoch": int(policy["evaluation_epoch"]),
        "maximum_response_age": int(policy["maximum_response_age"]),
        "maximum_request_age": int(policy["maximum_request_age"]),
        "allowed_repository_path_prefixes": list(policy["allowed_repository_path_prefixes"]),
        "forbidden_repository_path_prefixes": list(policy["forbidden_repository_path_prefixes"]),
    }, DOWNSTREAM_POLICY_DIGEST_FIELD)

def _receipt(*, verification, evidence, independent, generation, observation,
             candidate, application, request, policy, feedback, downstream,
             generation_digest_field):
    downstream_receipt = downstream.receipt
    regenerated = len(downstream.regenerated_candidates)
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_verification_execution_receipt_digest":
            verification[VERIFICATION_RECEIPT_DIGEST_FIELD],
        "source_evidence_bundle_digest": evidence[EVIDENCE_BUNDLE_DIGEST_FIELD],
        "source_independent_verification_evidence_digest":
            independent[INDEPENDENT_EVIDENCE_DIGEST_FIELD],
        "source_generation_receipt_digest": generation[generation_digest_field],
        "source_observation_receipt_digest": observation[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_candidate_receipt_digest": candidate[CANDIDATE_RECEIPT_DIGEST_FIELD],
        "source_application_receipt_digest": application[APPLICATION_RECEIPT_DIGEST_FIELD],
        "candidate_digest": candidate[RECEIPT_CANDIDATE_DIGEST_FIELD],
        "patch_artifact_digest": candidate["patch_artifact_digest"],
        "repository_full_name": candidate["repository_full_name"],
        "source_commit_sha": candidate["source_commit_sha"],
        "repair_request_digest": request[REQUEST_DIGEST_FIELD],
        "repair_policy_digest": policy[POLICY_DIGEST_FIELD],
        "normalized_feedback_digest": feedback[NORMALIZED_FEEDBACK_DIGEST_FIELD],
        "downstream_regeneration_receipt_digest":
            downstream_receipt[REGENERATION_RECEIPT_DIGEST_FIELD],
        "failed_check_count": int(verification["failed_check_count"]),
        "normalized_feedback_record_count": int(feedback["feedback_record_count"]),
        "seed_candidate_count": int(downstream_receipt["seed_candidate_count"]),
        "regenerated_candidate_count": regenerated,
        "combined_candidate_count": len(downstream.combined_candidates),
        "codeai_disposition": DISPOSITION_REGENERATED if regenerated else DISPOSITION_NO_NOVEL_CANDIDATE,
        "operating_mode": MODE_BOUNDED_FEEDBACK_REGENERATION,
        "route_receipt_recorded": True,
        "verification_lineage_verified": True,
        "candidate_lineage_verified": True,
        "application_lineage_verified": True,
        "generation_lineage_verified": True,
        "feedback_normalized_and_bounded": True,
        "provider_neutral_regeneration_invoked":
            bool(downstream_receipt["provider_calls_performed_by_kernel"]),
        "semantic_patch_deduplication_performed":
            bool(downstream_receipt["semantic_patch_deduplication_performed"]),
        "repository_snapshot_read_only": True,
        "candidate_selected": False,
        "patch_applied": False,
        "repository_mutation_performed": False,
        "git_ref_changed": False,
        "branch_created": False,
        "commit_created": False,
        "push_performed": False,
        "pull_request_created": False,
        "merge_performed": False,
        "deployment_performed": False,
        "secret_access_performed": False,
        "network_access_performed": False,
        "selection_authority_granted": False,
        "verification_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
        "successor_stage_authority_granted": False,
        "verification_failure_treated_as_repair_truth": False,
        "failed_check_treated_as_required_edit": False,
        "repair_feedback_treated_as_authority": False,
        "repair_regeneration_treated_as_correction": False,
        "new_candidate_treated_as_verified_patch": False,
        "tests_passing_after_repair_treated_as_proof": False,
        "repair_ranking_treated_as_selection": False,
        "evidence_guided_novelty_treated_as_requirement_satisfaction": False,
        "repair_loop_mutated_live_repository": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(value, RECEIPT_DIGEST_FIELD)

def build_codeai_verification_guided_candidate_repair_regeneration(
    *, source_verification_execution_receipt: Any,
    source_evidence_bundle: Any,
    source_independent_verification_evidence: Any,
    source_generation_receipt: Any,
    source_observation_receipt: Any,
    source_candidate_receipt: Any,
    source_application_receipt: Any,
    repository_files: Any,
    seed_candidates: Any,
    repair_request: Any,
    provider_adapters: Any,
    repair_policy: Any,
    candidate_policy: Any,
) -> CodeAIVerificationGuidedCandidateRepairRegenerationResult:
    issues = []
    verification, found = _sealed(source_verification_execution_receipt,
                                  VERIFICATION_RECEIPT_DIGEST_FIELD, "source_verification")
    issues += found
    evidence, found = _sealed(source_evidence_bundle,
                              EVIDENCE_BUNDLE_DIGEST_FIELD, "source_evidence")
    issues += found
    independent, found = _sealed(source_independent_verification_evidence,
                                 INDEPENDENT_EVIDENCE_DIGEST_FIELD, "source_independent")
    issues += found
    candidate, found = _sealed(source_candidate_receipt,
                               CANDIDATE_RECEIPT_DIGEST_FIELD, "source_candidate")
    issues += found
    application, found = _sealed(source_application_receipt,
                                 APPLICATION_RECEIPT_DIGEST_FIELD, "source_application")
    issues += found
    observation, found = _sealed(source_observation_receipt,
                                 SOURCE_RECEIPT_DIGEST_FIELD, "source_observation")
    issues += found
    generation = _mapping(source_generation_receipt)
    generation_field = source_digest_field(generation.get("profile_version")) if generation else None
    if generation is None:
        issues.append("source_generation_receipt_not_mapping")
    elif generation_field is None:
        issues.append("source_generation_profile_unsupported")
    elif not _digest_ok(generation, generation_field):
        issues.append("source_generation_receipt_digest_mismatch")
    repository = _mapping(repository_files)
    if repository is None or not all(isinstance(k, str) and isinstance(v, str)
                                     for k, v in (repository or {}).items()):
        issues.append("repository_files_not_text_mapping")
        repository = None
    request, found = _validate_request(repair_request)
    issues += found
    policy, found = _validate_policy(repair_policy)
    issues += found
    seed_digests, found = _seed_digests(seed_candidates)
    issues += found
    required = (verification, evidence, independent, generation, observation,
                candidate, application, repository, request, policy, generation_field)
    if issues or any(x is None for x in required):
        return CodeAIVerificationGuidedCandidateRepairRegenerationResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None, None)

    issues = _correspondence(
        verification=verification, evidence=evidence, independent=independent,
        generation=generation, observation=observation, candidate=candidate,
        application=application, repository=repository, seed_digests=seed_digests,
        request=request, policy=policy, generation_digest_field=generation_field)
    feedback, found = _normalize_feedback(evidence, independent, policy)
    issues += found
    if issues or feedback is None:
        return CodeAIVerificationGuidedCandidateRepairRegenerationResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), feedback, None, None)

    before = canonical_digest(repository)
    downstream = build_codeai_autonomous_candidate_regeneration(
        source_generation_receipt=generation,
        source_observation_receipt=observation,
        repository_files=repository,
        seed_candidates=seed_candidates,
        regeneration_request=_downstream_request(request, policy, feedback, seed_digests),
        provider_adapters=provider_adapters,
        regeneration_policy=_downstream_policy(policy),
        candidate_policy=candidate_policy,
    )
    if canonical_digest(repository) != before:
        return CodeAIVerificationGuidedCandidateRepairRegenerationResult(
            STATUS_BLOCKED, ("repository_snapshot_mutated_during_repair_regeneration",),
            feedback, downstream, None)
    if downstream.status != REGENERATION_STATUS_READY or downstream.receipt is None:
        return CodeAIVerificationGuidedCandidateRepairRegenerationResult(
            STATUS_BLOCKED,
            tuple(sorted(set(["downstream_candidate_regeneration_blocked"] + list(downstream.issues)))),
            feedback, downstream, None)
    if len(downstream.regenerated_candidates) > int(policy["maximum_added_candidates"]):
        return CodeAIVerificationGuidedCandidateRepairRegenerationResult(
            STATUS_BLOCKED, ("repair_added_candidate_budget_exceeded",),
            feedback, downstream, None)
    if len(downstream.combined_candidates) > int(policy["maximum_total_candidates"]):
        return CodeAIVerificationGuidedCandidateRepairRegenerationResult(
            STATUS_BLOCKED, ("repair_total_candidate_budget_exceeded",),
            feedback, downstream, None)
    receipt = _receipt(
        verification=verification, evidence=evidence, independent=independent,
        generation=generation, observation=observation, candidate=candidate,
        application=application, request=request, policy=policy, feedback=feedback,
        downstream=downstream, generation_digest_field=generation_field)
    return CodeAIVerificationGuidedCandidateRepairRegenerationResult(
        STATUS_READY, (), feedback, downstream, receipt)

__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIVerificationGuidedCandidateRepairRegenerationResult",
    "build_codeai_verification_guided_candidate_repair_regeneration",
]
