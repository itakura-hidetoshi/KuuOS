from __future__ import annotations

from collections import Counter
from typing import Any, Mapping

from runtime.kuuos_codeai_candidate_static_admissibility_preflight_schema_v0_1 import (
    DISPOSITION_ADMISSIBLE,
)
from runtime.kuuos_codeai_independent_test_strengthening_schema_v0_1 import (
    CATEGORY_BASELINE,
    CATEGORY_ERROR_FREE,
    CATEGORY_ERROR_SPECIFIC,
    CATEGORY_NOVELTY,
    CATEGORY_ROUTE,
    DISPOSITION_COMPLETED as STRENGTHENING_DISPOSITION_COMPLETED,
    MODE_PLAN_ONLY,
    OBLIGATION_CATEGORIES,
    OBLIGATION_DIGEST_FIELD,
    PLAN_DIGEST_FIELD as STRENGTHENING_PLAN_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as STRENGTHENING_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import *


def validate_source_pair(plan: Mapping[str, Any], receipt: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    if not digest_ok(plan, STRENGTHENING_PLAN_DIGEST_FIELD):
        issues.append("source_strengthening_plan_digest_mismatch")
    if not digest_ok(receipt, STRENGTHENING_RECEIPT_DIGEST_FIELD):
        issues.append("source_strengthening_receipt_digest_mismatch")
    if issues:
        return issues
    if plan.get("codeai_disposition") != STRENGTHENING_DISPOSITION_COMPLETED:
        issues.append("source_strengthening_disposition_invalid")
    if plan.get("operating_mode") != MODE_PLAN_ONLY:
        issues.append("source_strengthening_mode_invalid")
    pairs = (
        (
            receipt.get("independent_test_strengthening_plan_digest"),
            plan.get(STRENGTHENING_PLAN_DIGEST_FIELD),
            "source_strengthening_receipt_plan_digest_mismatch",
        ),
        (
            receipt.get("repository_full_name"),
            plan.get("repository_full_name"),
            "source_strengthening_receipt_repository_mismatch",
        ),
        (
            receipt.get("source_commit_sha"),
            plan.get("source_commit_sha"),
            "source_strengthening_receipt_commit_mismatch",
        ),
        (
            receipt.get("candidate_count"),
            plan.get("candidate_count"),
            "source_strengthening_receipt_candidate_count_mismatch",
        ),
        (
            receipt.get("obligation_count"),
            plan.get("obligation_count"),
            "source_strengthening_receipt_obligation_count_mismatch",
        ),
    )
    issues.extend(code for left, right, code in pairs if left != right)
    for field in (
        "exact_lineage_verified",
        "all_candidates_preserved",
        "baseline_obligations_present",
        "typed_error_obligations_present",
        "novel_error_falsification_obligations_present",
        "error_free_mutation_probes_present",
        "route_specific_obligations_present",
    ):
        if plan.get(field) is not True or receipt.get(field) is not True:
            issues.append("source_strengthening_required_true:" + field)
    for field in (
        "test_generation_performed",
        "test_execution_performed",
        "ranking_performed",
        "candidate_selected",
        "verification_runner_invoked",
        "repair_executed",
        "repository_mutation_performed",
        "git_effect_performed",
        "selection_authority_granted",
        "verification_authority_granted",
        "repair_authority_granted",
        "execution_authority_granted",
        "git_authority_granted",
        "strengthened_plan_treated_as_test_success",
        "obligation_count_treated_as_candidate_quality",
        "test_coverage_treated_as_correctness_proof",
    ):
        if plan.get(field) is not False or receipt.get(field) is not False:
            issues.append("source_strengthening_forbidden_true:" + field)

    candidates = plan.get("candidate_plans")
    if not isinstance(candidates, list) or not candidates:
        issues.append("source_strengthening_candidates_invalid")
        return sorted(set(issues))
    ids = [candidate.get("candidate_id") for candidate in candidates if isinstance(candidate, Mapping)]
    if ids != plan.get("candidate_ids") or len(ids) != len(set(ids)):
        issues.append("source_strengthening_candidate_ids_invalid")
    if plan.get("candidate_count") != len(candidates):
        issues.append("source_strengthening_candidate_count_invalid")
    total = 0
    for candidate_index, candidate in enumerate(candidates):
        if not isinstance(candidate, Mapping):
            issues.append(f"source_strengthening_candidate_not_mapping:{candidate_index}")
            continue
        obligations = candidate.get("obligations")
        if not isinstance(obligations, list) or not obligations:
            issues.append(f"source_strengthening_obligations_invalid:{candidate_index}")
            continue
        if candidate.get("obligation_count") != len(obligations):
            issues.append(f"source_strengthening_obligation_count_invalid:{candidate_index}")
        total += len(obligations)
        for obligation_index, obligation in enumerate(obligations):
            if not isinstance(obligation, Mapping):
                issues.append(
                    f"source_strengthening_obligation_not_mapping:{candidate_index}:{obligation_index}"
                )
                continue
            if not digest_ok(obligation, OBLIGATION_DIGEST_FIELD):
                issues.append(
                    f"source_strengthening_obligation_digest_mismatch:{candidate_index}:{obligation_index}"
                )
            if obligation.get("candidate_id") != candidate.get("candidate_id"):
                issues.append(
                    f"source_strengthening_obligation_candidate_mismatch:{candidate_index}:{obligation_index}"
                )
            if obligation.get("category") not in OBLIGATION_CATEGORIES:
                issues.append(
                    f"source_strengthening_obligation_category_invalid:{candidate_index}:{obligation_index}"
                )
            for field in ("test_generated", "test_executed", "pass_claimed"):
                if obligation.get(field) is not False:
                    issues.append(
                        f"source_strengthening_obligation_forbidden_true:{candidate_index}:{obligation_index}:{field}"
                    )
    if plan.get("obligation_count") != total:
        issues.append("source_strengthening_obligation_accounting_invalid")
    return sorted(set(issues))


def validate_evidence_packet(packet: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "evidence_packet_id",
        "evidence_packet_revision",
        "repository_full_name",
        "source_commit_sha",
        "strengthening_plan_digest",
        "strengthening_receipt_digest",
        "evidence_created_epoch",
        "candidate_producer_id",
        "independent_runner_id",
        "independent_reviewer_id",
        "candidate_results",
        "candidate_count",
        "evidence_record_count",
        "external_test_execution_reported",
        "independent_runner_verified",
        "independent_reviewer_verified",
        "isolated_execution_verified",
        "source_correspondence_verified",
        "candidate_producer_involved_in_evidence",
        "repository_mutation_performed",
        "git_effect_performed",
        EVIDENCE_PACKET_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(packet)
    extra = set(packet).difference(required)
    if missing:
        issues.append("evidence_packet_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("evidence_packet_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if packet["schema_version"] != SCHEMA_VERSION or packet["profile_version"] != PROFILE_VERSION:
        issues.append("evidence_packet_profile_invalid")
    for field in (
        "evidence_packet_id",
        "evidence_packet_revision",
        "repository_full_name",
        "candidate_producer_id",
        "independent_runner_id",
        "independent_reviewer_id",
    ):
        if not isinstance(packet[field], str) or not packet[field]:
            issues.append("evidence_packet_string_invalid:" + field)
    if not isinstance(packet["source_commit_sha"], str) or SHA40.fullmatch(packet["source_commit_sha"]) is None:
        issues.append("evidence_packet_source_commit_invalid")
    for field in ("strengthening_plan_digest", "strengthening_receipt_digest"):
        if not isinstance(packet[field], str) or SHA256.fullmatch(packet[field]) is None:
            issues.append("evidence_packet_digest_invalid:" + field)
    for field in ("evidence_created_epoch", "candidate_count", "evidence_record_count"):
        if not nonnegative_int(packet[field]):
            issues.append("evidence_packet_integer_invalid:" + field)
    for field in (
        "external_test_execution_reported",
        "independent_runner_verified",
        "independent_reviewer_verified",
        "isolated_execution_verified",
        "source_correspondence_verified",
        "candidate_producer_involved_in_evidence",
        "repository_mutation_performed",
        "git_effect_performed",
    ):
        if not isinstance(packet[field], bool):
            issues.append("evidence_packet_boolean_invalid:" + field)
    if not digest_ok(packet, EVIDENCE_PACKET_DIGEST_FIELD):
        issues.append("evidence_packet_digest_mismatch")
    candidates = packet["candidate_results"]
    if not isinstance(candidates, list) or not candidates:
        issues.append("evidence_packet_candidate_results_invalid")
        return sorted(set(issues))
    if packet["candidate_count"] != len(candidates):
        issues.append("evidence_packet_candidate_count_mismatch")
    record_total = 0
    ids: list[str] = []
    for candidate_index, candidate in enumerate(candidates):
        if not isinstance(candidate, Mapping):
            issues.append(f"evidence_candidate_not_mapping:{candidate_index}")
            continue
        required_candidate = {
            "candidate_id",
            "candidate_sequence",
            "obligation_results",
            "obligation_result_count",
        }
        if set(candidate) != required_candidate:
            issues.append(f"evidence_candidate_fields_invalid:{candidate_index}")
            continue
        ids.append(str(candidate["candidate_id"]))
        if not isinstance(candidate["candidate_id"], str) or not candidate["candidate_id"]:
            issues.append(f"evidence_candidate_id_invalid:{candidate_index}")
        if not positive_int(candidate["candidate_sequence"]):
            issues.append(f"evidence_candidate_sequence_invalid:{candidate_index}")
        results = candidate["obligation_results"]
        if not isinstance(results, list) or not results:
            issues.append(f"evidence_candidate_results_invalid:{candidate_index}")
            continue
        if candidate["obligation_result_count"] != len(results):
            issues.append(f"evidence_candidate_result_count_mismatch:{candidate_index}")
        record_total += len(results)
        for record_index, record in enumerate(results):
            if not isinstance(record, Mapping):
                issues.append(f"evidence_record_not_mapping:{candidate_index}:{record_index}")
                continue
            required_record = {
                "candidate_id",
                "candidate_sequence",
                "obligation_id",
                "obligation_digest",
                "category",
                "check_kind",
                "outcome",
                "evidence_artifact_digest",
                "runner_id",
                "reviewer_id",
                "completed",
                "external_execution",
                "independent_runner",
                "independent_reviewer",
                "isolated_execution",
                "source_correspondence",
                "candidate_producer_involved",
                "repository_mutation_performed",
                "git_effect_performed",
                EVIDENCE_RECORD_DIGEST_FIELD,
            }
            if set(record) != required_record:
                issues.append(f"evidence_record_fields_invalid:{candidate_index}:{record_index}")
                continue
            if not digest_ok(record, EVIDENCE_RECORD_DIGEST_FIELD):
                issues.append(f"evidence_record_digest_mismatch:{candidate_index}:{record_index}")
            if record["candidate_id"] != candidate["candidate_id"]:
                issues.append(f"evidence_record_candidate_mismatch:{candidate_index}:{record_index}")
            if not isinstance(record["obligation_id"], str) or not record["obligation_id"]:
                issues.append(f"evidence_record_obligation_id_invalid:{candidate_index}:{record_index}")
            if not isinstance(record["obligation_digest"], str) or SHA256.fullmatch(record["obligation_digest"]) is None:
                issues.append(f"evidence_record_obligation_digest_invalid:{candidate_index}:{record_index}")
            if record["category"] not in OBLIGATION_CATEGORIES:
                issues.append(f"evidence_record_category_invalid:{candidate_index}:{record_index}")
            if record["outcome"] not in EVIDENCE_OUTCOMES:
                issues.append(f"evidence_record_outcome_invalid:{candidate_index}:{record_index}")
            if not isinstance(record["evidence_artifact_digest"], str) or SHA256.fullmatch(record["evidence_artifact_digest"]) is None:
                issues.append(f"evidence_record_artifact_digest_invalid:{candidate_index}:{record_index}")
            for field in ("runner_id", "reviewer_id", "check_kind"):
                if not isinstance(record[field], str) or not record[field]:
                    issues.append(f"evidence_record_string_invalid:{candidate_index}:{record_index}:{field}")
            for field in (
                "completed",
                "external_execution",
                "independent_runner",
                "independent_reviewer",
                "isolated_execution",
                "source_correspondence",
                "candidate_producer_involved",
                "repository_mutation_performed",
                "git_effect_performed",
            ):
                if not isinstance(record[field], bool):
                    issues.append(f"evidence_record_boolean_invalid:{candidate_index}:{record_index}:{field}")
    if len(ids) != len(set(ids)):
        issues.append("evidence_packet_candidate_ids_duplicate")
    if packet["evidence_record_count"] != record_total:
        issues.append("evidence_packet_record_count_mismatch")
    return sorted(set(issues))


def score_candidate(
    candidate_plan: Mapping[str, Any],
    candidate_evidence: Mapping[str, Any],
    category_weights: Mapping[str, Any],
    require_admissible: bool,
    require_all_passed: bool,
) -> dict[str, Any]:
    obligations = candidate_plan["obligations"]
    records = candidate_evidence["obligation_results"]
    by_id = {record["obligation_id"]: record for record in records}
    outcomes = Counter(record["outcome"] for record in records)
    passed_score = sum(
        int(category_weights[obligation["category"]])
        for obligation in obligations
        if by_id[obligation["obligation_id"]]["outcome"] == OUTCOME_PASSED
    )
    maximum_score = sum(int(category_weights[obligation["category"]]) for obligation in obligations)
    reasons: list[str] = []
    if require_admissible and candidate_plan["source_classification"] != DISPOSITION_ADMISSIBLE:
        reasons.append("source_classification_not_admissible")
    if require_all_passed and outcomes[OUTCOME_PASSED] != len(obligations):
        reasons.append("not_all_obligations_passed")
    eligible = not reasons
    return {
        "candidate_id": candidate_plan["candidate_id"],
        "candidate_sequence": candidate_plan["candidate_sequence"],
        "source_candidate_digest": candidate_plan["source_candidate_digest"],
        "source_classification": candidate_plan["source_classification"],
        "obligation_count": len(obligations),
        "passed_count": outcomes[OUTCOME_PASSED],
        "failed_count": outcomes[OUTCOME_FAILED],
        "inconclusive_count": outcomes[OUTCOME_INCONCLUSIVE],
        "skipped_count": outcomes[OUTCOME_SKIPPED],
        "evidence_score": passed_score,
        "maximum_evidence_score": maximum_score,
        "eligible": eligible,
        "ineligibility_reasons": reasons,
        "score_treated_as_probability": False,
        "score_treated_as_correctness_proof": False,
        "candidate_selected": False,
    }


__all__ = [
    "score_candidate",
    "validate_evidence_packet",
    "validate_source_pair",
]
