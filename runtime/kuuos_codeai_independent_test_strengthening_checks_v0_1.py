from __future__ import annotations

from collections import Counter
from typing import Any, Mapping

from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    CLASSIFICATION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CLASSIFICATION_RECEIPT_DIGEST_FIELD,
    NOVELTY_NOVEL,
    digest_ok as source_digest_ok,
)
from runtime.kuuos_codeai_independent_test_strengthening_schema_v0_1 import *


def validate_source_pair(
    classification: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> list[str]:
    issues: list[str] = []
    if not source_digest_ok(classification, CLASSIFICATION_DIGEST_FIELD):
        issues.append("source_classification_digest_mismatch")
    if not source_digest_ok(receipt, CLASSIFICATION_RECEIPT_DIGEST_FIELD):
        issues.append("source_classification_receipt_digest_mismatch")
    if issues:
        return issues
    pairs = (
        (
            receipt.get("typed_error_classification_digest"),
            classification.get(CLASSIFICATION_DIGEST_FIELD),
            "source_receipt_classification_digest_mismatch",
        ),
        (
            receipt.get("repository_full_name"),
            classification.get("repository_full_name"),
            "source_receipt_repository_mismatch",
        ),
        (
            receipt.get("source_commit_sha"),
            classification.get("source_commit_sha"),
            "source_receipt_commit_mismatch",
        ),
        (
            receipt.get("candidate_count"),
            classification.get("candidate_count"),
            "source_receipt_candidate_count_mismatch",
        ),
        (
            receipt.get("typed_error_count"),
            classification.get("typed_error_count"),
            "source_receipt_typed_error_count_mismatch",
        ),
    )
    issues.extend(code for left, right, code in pairs if left != right)
    candidates = classification.get("typed_candidates")
    if not isinstance(candidates, list):
        issues.append("source_classification_candidates_invalid")
        candidates = []
    if classification.get("candidate_count") != len(candidates):
        issues.append("source_classification_candidate_count_invalid")
    candidate_ids = [candidate.get("candidate_id") for candidate in candidates if isinstance(candidate, Mapping)]
    if candidate_ids != classification.get("candidate_ids"):
        issues.append("source_classification_candidate_ids_invalid")
    if len(candidate_ids) != len(set(candidate_ids)):
        issues.append("source_classification_candidate_ids_duplicate")
    typed_error_total = 0
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, Mapping):
            issues.append(f"source_candidate_not_mapping:{index}")
            continue
        errors = candidate.get("typed_errors")
        if not isinstance(errors, list):
            issues.append(f"source_candidate_errors_invalid:{index}")
            continue
        typed_error_total += len(errors)
        if candidate.get("typed_error_count") != len(errors):
            issues.append(f"source_candidate_error_count_invalid:{index}")
        if candidate.get("no_static_error_observed") != (len(errors) == 0):
            issues.append(f"source_candidate_zero_error_flag_invalid:{index}")
    if classification.get("typed_error_count") != typed_error_total:
        issues.append("source_classification_typed_error_accounting_invalid")
    forbidden_true = (
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
        "typed_error_treated_as_cause_proof",
        "historical_frequency_treated_as_probability",
        "zero_static_error_treated_as_correctness_proof",
    )
    for field in forbidden_true:
        if classification.get(field) is not False:
            issues.append("source_classification_effect_or_authority_present:" + field)
        if receipt.get(field) is not False:
            issues.append("source_receipt_effect_or_authority_present:" + field)
    return sorted(set(issues))


def capability_map(catalog: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(capability["check_kind"]): capability
        for capability in catalog["check_capabilities"]
    }


def required_check_kinds(candidate: Mapping[str, Any]) -> dict[str, set[str]]:
    requirements: dict[str, set[str]] = {kind: set() for kind in BASELINE_CHECKS}
    errors = candidate["typed_errors"]
    for error in errors:
        fingerprint = str(error["error_fingerprint"])
        requirements.setdefault(FAMILY_CHECK_KIND[error["error_family"]], set()).add(fingerprint)
        requirements.setdefault(ROUTE_CHECK_KIND[error["repair_route"]], set()).add(fingerprint)
        if error["baseline_novelty"] == NOVELTY_NOVEL:
            requirements.setdefault(CHECK_NOVELTY_FALSIFICATION, set()).add(fingerprint)
    if not errors:
        requirements.setdefault(CHECK_ERROR_FREE_MUTATION_PROBE, set())
    return requirements


def build_obligations(
    candidate: Mapping[str, Any],
    capabilities: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    requirements = required_check_kinds(candidate)
    obligations: list[dict[str, Any]] = []
    sequence = 0
    for kind in CHECK_KINDS:
        if kind not in requirements:
            continue
        sequence += 1
        capability = capabilities[kind]
        linked = sorted(requirements[kind])
        obligation = {
            "candidate_id": candidate["candidate_id"],
            "candidate_sequence": candidate["candidate_sequence"],
            "obligation_sequence": sequence,
            "obligation_id": f"{candidate['candidate_id']}:{sequence:03d}:{kind}",
            "category": CHECK_CATEGORY[kind],
            "check_kind": kind,
            "source_error_fingerprints": linked,
            "source_error_count": len(linked),
            "expected_evidence": list(EXPECTED_EVIDENCE[kind]),
            "runner_profile": capability["runner_profile"],
            "evidence_format": capability["evidence_format"],
            "independent_runner_required": True,
            "isolated_execution_required": True,
            "mutation_capability_required": kind == CHECK_ERROR_FREE_MUTATION_PROBE,
            "falsification_capability_required": kind == CHECK_NOVELTY_FALSIFICATION,
            "test_generated": False,
            "test_executed": False,
            "pass_claimed": False,
        }
        obligations.append(seal(obligation, OBLIGATION_DIGEST_FIELD))
    return obligations


def summarize_obligations(candidate_plans: list[dict[str, Any]]) -> dict[str, Any]:
    obligations = [
        obligation
        for candidate in candidate_plans
        for obligation in candidate["obligations"]
    ]
    return {
        "obligation_count": len(obligations),
        "check_kind_counts": {
            kind: sum(obligation["check_kind"] == kind for obligation in obligations)
            for kind in CHECK_KINDS
        },
        "category_counts": {
            category: sum(obligation["category"] == category for obligation in obligations)
            for category in OBLIGATION_CATEGORIES
        },
        "candidate_obligation_counts": {
            candidate["candidate_id"]: candidate["obligation_count"]
            for candidate in candidate_plans
        },
    }


def required_capability_issues(
    candidate_plans: list[dict[str, Any]],
    capabilities: Mapping[str, Mapping[str, Any]],
    policy: Mapping[str, Any],
) -> list[str]:
    issues: list[str] = []
    required_kinds = sorted(
        {
            obligation["check_kind"]
            for candidate in candidate_plans
            for obligation in candidate["obligations"]
        }
    )
    for kind in required_kinds:
        capability = capabilities.get(kind)
        if capability is None:
            issues.append("strengthening_required_check_kind_unsupported:" + kind)
            continue
        if policy["require_independent_runner"] and capability["independent_runner"] is not True:
            issues.append("strengthening_independent_runner_unavailable:" + kind)
        if policy["require_isolated_execution"] and capability["isolated_execution"] is not True:
            issues.append("strengthening_isolated_execution_unavailable:" + kind)
        if kind == CHECK_NOVELTY_FALSIFICATION and policy["require_falsification_for_novel_errors"]:
            if capability["falsification_capable"] is not True:
                issues.append("strengthening_falsification_capability_unavailable")
        if kind == CHECK_ERROR_FREE_MUTATION_PROBE and policy["require_error_free_mutation_probe"]:
            if capability["mutation_capable"] is not True:
                issues.append("strengthening_mutation_capability_unavailable")
    return sorted(set(issues))


__all__ = [
    "build_obligations",
    "capability_map",
    "required_capability_issues",
    "required_check_kinds",
    "summarize_obligations",
    "validate_source_pair",
]
