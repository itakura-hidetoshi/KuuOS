#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD,
    canonical_digest,
    patch_artifact_digest,
    seal,
)
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import (
    DISPOSITION_SYNTHESIZED as UNIFIED_DIFF_DISPOSITION_SYNTHESIZED,
    RECEIPT_DIGEST_FIELD as UNIFIED_DIFF_RECEIPT_DIGEST_FIELD,
    GeneratedUnifiedDiffCandidate,
)
from runtime.kuuos_codeai_autonomous_structured_edit_types_v0_1 import (
    DISPOSITION_SYNTHESIZED as STRUCTURED_EDIT_DISPOSITION_SYNTHESIZED,
    RECEIPT_DIGEST_FIELD as STRUCTURED_EDIT_RECEIPT_DIGEST_FIELD,
)

VERSION = "kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Autonomous Candidate Portfolio Selection v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_SELECTION_ONLY = "selection_only"
DISPOSITION_SELECTED = "candidate_selected_for_independent_verification"
DISPOSITION_NO_ADMISSIBLE = "no_admissible_candidate_for_independent_verification"
SELECTION_PURPOSE = "independent_verification"
SELECTION_STRATEGY = "least_change_admissible"

REQUEST_DIGEST_FIELD = "codeai_autonomous_candidate_selection_request_digest"
POLICY_DIGEST_FIELD = "codeai_autonomous_candidate_selection_policy_digest"
RECEIPT_DIGEST_FIELD = "codeai_autonomous_candidate_selection_receipt_digest"

_REQUEST_FIELDS = {
    "selection_request_id",
    "selection_request_revision",
    "source_portfolio_receipt_digest",
    "selection_purpose",
    "requested_by_actor_id",
    "request_created_epoch",
    REQUEST_DIGEST_FIELD,
}
_POLICY_FIELDS = {
    "expected_source_portfolio_receipt_digest",
    "maximum_candidate_count",
    "maximum_patch_bytes",
    "maximum_changed_paths",
    "allowed_risk_labels",
    "forbidden_risk_labels",
    "require_no_unresolved_questions",
    "allowed_path_prefixes",
    "forbidden_path_prefixes",
    "selection_strategy",
    "evaluation_epoch",
    "maximum_request_age",
    POLICY_DIGEST_FIELD,
}
_PORTFOLIO_DIGEST_FIELDS = (
    UNIFIED_DIFF_RECEIPT_DIGEST_FIELD,
    STRUCTURED_EDIT_RECEIPT_DIGEST_FIELD,
)
_ALLOWED_SOURCE_DISPOSITIONS = {
    UNIFIED_DIFF_DISPOSITION_SYNTHESIZED,
    STRUCTURED_EDIT_DISPOSITION_SYNTHESIZED,
}


@dataclass(frozen=True)
class SelectedVerificationCandidate:
    candidate_id: str
    upstream_rank: int
    patch_candidate: dict[str, Any]
    patch_artifact: str
    candidate_receipt: dict[str, Any]


@dataclass(frozen=True)
class CodeAIAutonomousCandidatePortfolioSelectionResult:
    status: str
    issues: tuple[str, ...]
    selected_candidate: SelectedVerificationCandidate | None
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any, *, positive: bool = False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    if positive and value == 0:
        return None
    return value


def _unique_strings(value: Any, *, nonempty: bool = False) -> list[str] | None:
    if not isinstance(value, list):
        return None
    if not all(isinstance(item, str) and item for item in value):
        return None
    if len(value) != len(set(value)) or (nonempty and not value):
        return None
    return list(value)


def _exact_fields(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = fields.difference(value)
    extra = set(value).difference(fields)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def _digest_ok(value: Mapping[str, Any], field: str) -> bool:
    return value.get(field) == canonical_digest({k: v for k, v in value.items() if k != field})


def _path_has_prefix(path: str, prefix: str) -> bool:
    normalized = prefix.rstrip("/")
    return path == normalized or path.startswith(normalized + "/")


def _portfolio_digest_field(receipt: Mapping[str, Any]) -> str | None:
    present = [field for field in _PORTFOLIO_DIGEST_FIELDS if field in receipt]
    return present[0] if len(present) == 1 else None


def _validate_portfolio_receipt(value: Any) -> tuple[Mapping[str, Any] | None, str | None, list[str]]:
    receipt = _mapping(value)
    if receipt is None:
        return None, None, ["source_portfolio_receipt_not_mapping"]
    issues: list[str] = []
    digest_field = _portfolio_digest_field(receipt)
    if digest_field is None:
        issues.append("source_portfolio_receipt_digest_field_invalid")
    elif not _digest_ok(receipt, digest_field):
        issues.append("source_portfolio_receipt_digest_mismatch")
    if receipt.get("codeai_disposition") not in _ALLOWED_SOURCE_DISPOSITIONS:
        issues.append("source_portfolio_receipt_not_synthesized")
    if receipt.get("operating_mode") != "proposal_only":
        issues.append("source_portfolio_receipt_not_proposal_only")
    if receipt.get("route_receipt_recorded") is not True:
        issues.append("source_portfolio_route_not_recorded")
    if receipt.get("candidate_selected") is not False:
        issues.append("source_portfolio_already_selected")
    if _nat(receipt.get("generated_candidate_count"), positive=True) is None:
        issues.append("source_portfolio_candidate_count_invalid")
    if _unique_strings(receipt.get("generated_candidate_ids"), nonempty=True) is None:
        issues.append("source_portfolio_candidate_ids_invalid")
    if _unique_strings(receipt.get("generated_candidate_digests"), nonempty=True) is None:
        issues.append("source_portfolio_candidate_digests_invalid")
    return receipt, digest_field, issues


def _validate_request(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    request = _mapping(value)
    if request is None:
        return None, ["selection_request_not_mapping"]
    issues = _exact_fields(request, _REQUEST_FIELDS, "selection_request")
    if issues:
        return request, issues
    for field in (
        "selection_request_id",
        "selection_request_revision",
        "source_portfolio_receipt_digest",
        "requested_by_actor_id",
    ):
        if not isinstance(request[field], str) or not request[field]:
            issues.append("selection_request_invalid_string:" + field)
    if request["selection_purpose"] != SELECTION_PURPOSE:
        issues.append("selection_request_purpose_invalid")
    if _nat(request["request_created_epoch"]) is None:
        issues.append("selection_request_created_epoch_invalid")
    if not _digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("selection_request_digest_mismatch")
    return request, issues


def _validate_policy(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    policy = _mapping(value)
    if policy is None:
        return None, ["selection_policy_not_mapping"]
    issues = _exact_fields(policy, _POLICY_FIELDS, "selection_policy")
    if issues:
        return policy, issues
    if not isinstance(policy["expected_source_portfolio_receipt_digest"], str) or not policy[
        "expected_source_portfolio_receipt_digest"
    ]:
        issues.append("selection_policy_expected_source_digest_invalid")
    for field in (
        "maximum_candidate_count",
        "maximum_patch_bytes",
        "maximum_changed_paths",
        "maximum_request_age",
    ):
        if _nat(policy[field], positive=True) is None:
            issues.append("selection_policy_invalid_positive_nat:" + field)
    if _nat(policy["evaluation_epoch"]) is None:
        issues.append("selection_policy_evaluation_epoch_invalid")
    for field in ("allowed_risk_labels", "forbidden_risk_labels"):
        if _unique_strings(policy[field], nonempty=(field == "allowed_risk_labels")) is None:
            issues.append("selection_policy_invalid_string_list:" + field)
    for field in ("allowed_path_prefixes", "forbidden_path_prefixes"):
        if _unique_strings(policy[field], nonempty=(field == "allowed_path_prefixes")) is None:
            issues.append("selection_policy_invalid_string_list:" + field)
    if not isinstance(policy["require_no_unresolved_questions"], bool):
        issues.append("selection_policy_require_no_unresolved_questions_invalid")
    if policy["selection_strategy"] != SELECTION_STRATEGY:
        issues.append("selection_policy_strategy_invalid")
    if not _digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("selection_policy_digest_mismatch")
    return policy, issues


def _validate_candidates(value: Any) -> tuple[list[GeneratedUnifiedDiffCandidate] | None, list[str]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or not value:
        return None, ["candidate_portfolio_not_nonempty_sequence"]
    issues: list[str] = []
    candidates: list[GeneratedUnifiedDiffCandidate] = []
    ranks: set[int] = set()
    ids: set[str] = set()
    digests: set[str] = set()
    for index, item in enumerate(value):
        prefix = f"candidate[{index}]"
        if not isinstance(item, GeneratedUnifiedDiffCandidate):
            issues.append(prefix + ":invalid_type")
            continue
        candidates.append(item)
        if _nat(item.rank, positive=True) is None:
            issues.append(prefix + ":rank_invalid")
        elif item.rank in ranks:
            issues.append(prefix + ":rank_duplicate")
        ranks.add(item.rank)
        candidate = _mapping(item.patch_candidate)
        receipt = _mapping(item.candidate_receipt)
        if candidate is None:
            issues.append(prefix + ":patch_candidate_not_mapping")
            continue
        candidate_id = candidate.get("candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id:
            issues.append(prefix + ":candidate_id_invalid")
        elif candidate_id != item.proposal_id:
            issues.append(prefix + ":proposal_candidate_id_mismatch")
        elif candidate_id in ids:
            issues.append(prefix + ":candidate_id_duplicate")
        ids.add(str(candidate_id))
        digest = candidate.get(CANDIDATE_DIGEST_FIELD)
        if not isinstance(digest, str) or not digest:
            issues.append(prefix + ":candidate_digest_missing")
        elif not _digest_ok(candidate, CANDIDATE_DIGEST_FIELD):
            issues.append(prefix + ":candidate_digest_mismatch")
        elif digest in digests:
            issues.append(prefix + ":candidate_digest_duplicate")
        digests.add(str(digest))
        if candidate.get("patch_artifact_digest") != patch_artifact_digest(item.patch_artifact):
            issues.append(prefix + ":patch_artifact_digest_mismatch")
        if _nat(candidate.get("patch_size_bytes"), positive=True) is None:
            issues.append(prefix + ":patch_size_invalid")
        if _nat(candidate.get("declared_change_count"), positive=True) is None:
            issues.append(prefix + ":change_count_invalid")
        changed_paths = _unique_strings(candidate.get("changed_paths"), nonempty=True)
        if changed_paths is None:
            issues.append(prefix + ":changed_paths_invalid")
        elif len(changed_paths) != candidate.get("declared_change_count"):
            issues.append(prefix + ":change_count_mismatch")
        if _unique_strings(candidate.get("risk_labels"), nonempty=True) is None:
            issues.append(prefix + ":risk_labels_invalid")
        if _unique_strings(candidate.get("unresolved_candidate_questions")) is None:
            issues.append(prefix + ":unresolved_questions_invalid")
        if receipt is None:
            issues.append(prefix + ":candidate_receipt_not_mapping")
        else:
            if receipt.get("candidate_patch_ready") is not True:
                issues.append(prefix + ":candidate_receipt_not_ready")
            if receipt.get("codeai_disposition") != "candidate_patch_supported":
                issues.append(prefix + ":candidate_receipt_not_supported")
    if candidates and ranks != set(range(1, len(candidates) + 1)):
        issues.append("candidate_ranks_not_contiguous")
    return candidates, issues


def _candidate_rejection_reasons(
    item: GeneratedUnifiedDiffCandidate,
    policy: Mapping[str, Any],
) -> list[str]:
    candidate = item.patch_candidate
    reasons: list[str] = []
    if candidate["patch_size_bytes"] > policy["maximum_patch_bytes"]:
        reasons.append("patch_byte_budget_exceeded")
    if candidate["declared_change_count"] > policy["maximum_changed_paths"]:
        reasons.append("changed_path_budget_exceeded")
    allowed_risks = set(policy["allowed_risk_labels"])
    forbidden_risks = set(policy["forbidden_risk_labels"])
    risk_labels = set(candidate["risk_labels"])
    unknown_risks = sorted(risk_labels.difference(allowed_risks))
    if unknown_risks:
        reasons.append("risk_label_not_allowed:" + ",".join(unknown_risks))
    blocked_risks = sorted(risk_labels.intersection(forbidden_risks))
    if blocked_risks:
        reasons.append("risk_label_forbidden:" + ",".join(blocked_risks))
    if policy["require_no_unresolved_questions"] and candidate[
        "unresolved_candidate_questions"
    ]:
        reasons.append("unresolved_candidate_questions_present")
    for path in candidate["changed_paths"]:
        if not any(_path_has_prefix(path, prefix) for prefix in policy["allowed_path_prefixes"]):
            reasons.append("changed_path_not_allowed:" + path)
        if any(_path_has_prefix(path, prefix) for prefix in policy["forbidden_path_prefixes"]):
            reasons.append("changed_path_forbidden:" + path)
    return sorted(set(reasons))


def _selection_key(item: GeneratedUnifiedDiffCandidate) -> tuple[int, int, int, int, str]:
    candidate = item.patch_candidate
    return (
        int(candidate["declared_change_count"]),
        int(candidate["patch_size_bytes"]),
        len(candidate["risk_labels"]),
        item.rank,
        str(candidate["candidate_id"]),
    )


def _receipt(
    *,
    source_receipt_digest: str,
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    candidates: Sequence[GeneratedUnifiedDiffCandidate],
    admissible: Sequence[GeneratedUnifiedDiffCandidate],
    rejected: Sequence[Mapping[str, Any]],
    selected: GeneratedUnifiedDiffCandidate | None,
) -> dict[str, Any]:
    selected_candidate = selected.patch_candidate if selected else None
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_portfolio_receipt_digest": source_receipt_digest,
        "selection_request_digest": request[REQUEST_DIGEST_FIELD],
        "selection_policy_digest": policy[POLICY_DIGEST_FIELD],
        "evaluated_candidate_count": len(candidates),
        "evaluated_candidate_ids": [item.patch_candidate["candidate_id"] for item in candidates],
        "evaluated_candidate_digests": [
            item.patch_candidate[CANDIDATE_DIGEST_FIELD] for item in candidates
        ],
        "admissible_candidate_count": len(admissible),
        "admissible_candidate_ids": [item.patch_candidate["candidate_id"] for item in admissible],
        "rejected_candidate_count": len(rejected),
        "rejected_candidates": list(rejected),
        "selected_candidate_id": selected_candidate["candidate_id"] if selected_candidate else "",
        "selected_candidate_digest": selected_candidate[CANDIDATE_DIGEST_FIELD] if selected_candidate else "",
        "selected_patch_artifact_digest": selected_candidate["patch_artifact_digest"] if selected_candidate else "",
        "selected_upstream_rank": selected.rank if selected else 0,
        "selection_key": list(_selection_key(selected)) if selected else [],
        "selection_strategy": SELECTION_STRATEGY,
        "selection_purpose": SELECTION_PURPOSE,
        "codeai_disposition": DISPOSITION_SELECTED if selected else DISPOSITION_NO_ADMISSIBLE,
        "operating_mode": MODE_SELECTION_ONLY,
        "route_receipt_recorded": True,
        "selection_policy_evaluated": True,
        "candidate_selected": selected is not None,
        "selected_for_independent_verification": selected is not None,
        "selection_performed_by_kernel": selected is not None,
        "selection_authority_consumed_by_kernel": selected is not None,
        "successor_selection_authority_granted": False,
        "verification_lease_issued": False,
        "execution_lease_issued": False,
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
        "verification_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
        "selected_candidate_treated_as_correct": False,
        "ranking_treated_as_correctness_proof": False,
        "selection_treated_as_verification": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(value, RECEIPT_DIGEST_FIELD)


def build_codeai_autonomous_candidate_portfolio_selection(
    *,
    source_portfolio_receipt: Any,
    candidates: Any,
    selection_request: Any,
    selection_policy: Any,
) -> CodeAIAutonomousCandidatePortfolioSelectionResult:
    source, source_digest_field, source_issues = _validate_portfolio_receipt(source_portfolio_receipt)
    parsed_candidates, candidate_issues = _validate_candidates(candidates)
    request, request_issues = _validate_request(selection_request)
    policy, policy_issues = _validate_policy(selection_policy)
    issues = source_issues + candidate_issues + request_issues + policy_issues
    if (
        issues
        or source is None
        or source_digest_field is None
        or parsed_candidates is None
        or request is None
        or policy is None
    ):
        return CodeAIAutonomousCandidatePortfolioSelectionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None
        )

    source_digest = str(source[source_digest_field])
    if request["source_portfolio_receipt_digest"] != source_digest:
        issues.append("selection_request_source_portfolio_mismatch")
    if policy["expected_source_portfolio_receipt_digest"] != source_digest:
        issues.append("selection_policy_source_portfolio_mismatch")
    if len(parsed_candidates) > policy["maximum_candidate_count"]:
        issues.append("candidate_count_budget_exceeded")
    if source["generated_candidate_count"] != len(parsed_candidates):
        issues.append("source_portfolio_candidate_count_mismatch")
    candidate_ids = [item.patch_candidate["candidate_id"] for item in parsed_candidates]
    candidate_digests = [item.patch_candidate[CANDIDATE_DIGEST_FIELD] for item in parsed_candidates]
    if source["generated_candidate_ids"] != candidate_ids:
        issues.append("source_portfolio_candidate_ids_mismatch")
    if source["generated_candidate_digests"] != candidate_digests:
        issues.append("source_portfolio_candidate_digests_mismatch")
    evaluation_epoch = int(policy["evaluation_epoch"])
    created_epoch = int(request["request_created_epoch"])
    if not evaluation_epoch - int(policy["maximum_request_age"]) <= created_epoch <= evaluation_epoch:
        issues.append("selection_request_window_invalid")
    if issues:
        return CodeAIAutonomousCandidatePortfolioSelectionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None
        )

    admissible: list[GeneratedUnifiedDiffCandidate] = []
    rejected: list[dict[str, Any]] = []
    route_issues: list[str] = []
    for item in parsed_candidates:
        reasons = _candidate_rejection_reasons(item, policy)
        if reasons:
            rejected.append({"candidate_id": item.patch_candidate["candidate_id"], "reasons": reasons})
            route_issues.extend(item.patch_candidate["candidate_id"] + ":" + reason for reason in reasons)
        else:
            admissible.append(item)
    admissible.sort(key=_selection_key)
    selected = admissible[0] if admissible else None
    receipt = _receipt(
        source_receipt_digest=source_digest,
        request=request,
        policy=policy,
        candidates=parsed_candidates,
        admissible=admissible,
        rejected=rejected,
        selected=selected,
    )
    selected_candidate = (
        SelectedVerificationCandidate(
            candidate_id=selected.patch_candidate["candidate_id"],
            upstream_rank=selected.rank,
            patch_candidate=selected.patch_candidate,
            patch_artifact=selected.patch_artifact,
            candidate_receipt=selected.candidate_receipt,
        )
        if selected
        else None
    )
    return CodeAIAutonomousCandidatePortfolioSelectionResult(
        STATUS_READY if selected else STATUS_BLOCKED,
        tuple(route_issues),
        selected_candidate,
        receipt,
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "SelectedVerificationCandidate",
    "CodeAIAutonomousCandidatePortfolioSelectionResult",
    "build_codeai_autonomous_candidate_portfolio_selection",
]
