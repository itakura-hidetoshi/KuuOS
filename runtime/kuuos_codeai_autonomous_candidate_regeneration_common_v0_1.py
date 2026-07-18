from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Any, Mapping, Sequence

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as CANDIDATE_POLICY_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    patch_artifact_digest,
    seal,
)
from runtime.kuuos_codeai_autonomous_structured_edit_types_v0_1 import (
    BOUNDARY_REJECT,
    MODE_PROPOSAL_ONLY,
    RAW_PROPOSAL_FIELDS,
    ProviderAdapter,
    ProviderAttemptReceipt,
    canonical_path,
    digest_ok,
    exact,
    mapping,
    nat,
    path_has_prefix,
    strings,
    validate_adapters,
    validate_repository,
)
from runtime.kuuos_codeai_autonomous_structured_edit_provider_v0_1 import (
    attempt,
    parse_provider_response,
)
from runtime.kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 import (
    RECEIPT_DIGEST_FIELD as STRUCTURED_SYNTHESIS_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import (
    RECEIPT_DIGEST_FIELD as UNIFIED_DIFF_RECEIPT_DIGEST_FIELD,
    STATUS_READY as UNIFIED_DIFF_STATUS_READY,
    GeneratedUnifiedDiffCandidate,
    build_codeai_autonomous_unified_diff_candidates,
)

VERSION = "kuuos_codeai_autonomous_candidate_regeneration_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Autonomous Candidate Regeneration v0.1"
SOURCE_STRUCTURED_PROFILE = "CodeAI Autonomous Structured Edit Synthesis v0.1"
SOURCE_STRUCTURED_DISPOSITION = "autonomous_structured_edit_candidates_synthesized"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
DISPOSITION_REGENERATED = "autonomous_candidate_portfolio_regenerated"
DISPOSITION_NO_NOVEL_CANDIDATE = "candidate_regeneration_exhausted_without_novel_candidate"
REQUEST_DIGEST_FIELD = "codeai_autonomous_candidate_regeneration_request_digest"
POLICY_DIGEST_FIELD = "codeai_autonomous_candidate_regeneration_policy_digest"
RECEIPT_DIGEST_FIELD = "codeai_autonomous_candidate_regeneration_receipt_digest"

REQUEST_FIELDS = {
    "request_id", "request_revision", "intent_text",
    "target_unique_candidate_count", "maximum_rounds_requested",
    "request_created_epoch", "feedback_reasons", "diversity_axes",
    "requirement_trace_ids", "test_plan_ids", "risk_labels",
    "unresolved_candidate_questions", "prior_candidate_digests",
    "prior_producer_session_ids", REQUEST_DIGEST_FIELD,
}
POLICY_FIELDS = {
    "allowed_provider_ids", "allowed_diversity_axes", "maximum_rounds",
    "maximum_provider_calls_per_round", "maximum_total_provider_calls",
    "maximum_raw_output_bytes", "maximum_intent_bytes",
    "maximum_repository_snapshot_bytes", "maximum_feedback_items",
    "maximum_existing_candidates", "maximum_unique_candidates",
    "evaluation_epoch", "maximum_response_age", "maximum_request_age",
    "allowed_repository_path_prefixes", "forbidden_repository_path_prefixes",
    POLICY_DIGEST_FIELD,
}

@dataclass(frozen=True)
class CandidateRegenerationAttemptReceipt:
    round_index: int
    attempt_index: int
    diversity_axis: str
    provider_attempt: ProviderAttemptReceipt
    downstream_unified_diff_receipt_digest: str = ""
    candidate_id: str = ""
    candidate_digest: str = ""
    patch_artifact_digest: str = ""
    accepted_novel_candidate: bool = False
    novelty_rejection_reason: str = ""

@dataclass(frozen=True)
class CodeAIAutonomousCandidateRegenerationResult:
    status: str
    issues: tuple[str, ...]
    attempts: tuple[CandidateRegenerationAttemptReceipt, ...]
    regenerated_candidates: tuple[GeneratedUnifiedDiffCandidate, ...]
    combined_candidates: tuple[GeneratedUnifiedDiffCandidate, ...]
    receipt: dict[str, Any] | None

def validate_request(value: Any):
    request = mapping(value)
    if request is None:
        return None, ["regeneration_request_not_mapping"]
    issues = exact(request, REQUEST_FIELDS, "regeneration_request")
    if issues:
        return request, issues
    for field in ("request_id", "request_revision", "intent_text"):
        if not isinstance(request[field], str) or not request[field]:
            issues.append("regeneration_request_invalid_string:" + field)
    list_fields = (
        "feedback_reasons", "diversity_axes", "requirement_trace_ids",
        "test_plan_ids", "risk_labels", "unresolved_candidate_questions",
        "prior_candidate_digests", "prior_producer_session_ids",
    )
    for field in list_fields:
        required = field in {"feedback_reasons", "diversity_axes"}
        if strings(request[field], nonempty=required) is None:
            issues.append("regeneration_request_invalid_string_list:" + field)
    for field in ("target_unique_candidate_count", "maximum_rounds_requested"):
        if nat(request[field], positive=True) is None:
            issues.append("regeneration_request_invalid_positive_nat:" + field)
    if nat(request["request_created_epoch"]) is None:
        issues.append("regeneration_request_invalid_created_epoch")
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("regeneration_request_digest_mismatch")
    return request, issues

def validate_policy(value: Any):
    policy = mapping(value)
    if policy is None:
        return None, ["regeneration_policy_not_mapping"]
    issues = exact(policy, POLICY_FIELDS, "regeneration_policy")
    if issues:
        return policy, issues
    nats = (
        "maximum_rounds", "maximum_provider_calls_per_round",
        "maximum_total_provider_calls", "maximum_raw_output_bytes",
        "maximum_intent_bytes", "maximum_repository_snapshot_bytes",
        "maximum_feedback_items", "maximum_existing_candidates",
        "maximum_unique_candidates", "maximum_response_age",
        "maximum_request_age",
    )
    for field in nats:
        if nat(policy[field], positive=True) is None:
            issues.append("regeneration_policy_invalid_positive_nat:" + field)
    if nat(policy["evaluation_epoch"]) is None:
        issues.append("regeneration_policy_invalid_evaluation_epoch")
    required_lists = (
        "allowed_provider_ids", "allowed_diversity_axes",
        "allowed_repository_path_prefixes",
    )
    for field in required_lists:
        if strings(policy[field], nonempty=True) is None:
            issues.append("regeneration_policy_invalid_string_list:" + field)
    if strings(policy["forbidden_repository_path_prefixes"]) is None:
        issues.append("regeneration_policy_invalid_string_list:forbidden_repository_path_prefixes")
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("regeneration_policy_digest_mismatch")
    return policy, issues

def source_digest_field(profile: Any):
    if profile == SOURCE_STRUCTURED_PROFILE:
        return STRUCTURED_SYNTHESIS_RECEIPT_DIGEST_FIELD
    if profile == PROFILE_VERSION:
        return RECEIPT_DIGEST_FIELD
    return None

def source_route_issues(receipt: Mapping[str, Any], profile: str):
    allowed = ({SOURCE_STRUCTURED_DISPOSITION} if profile == SOURCE_STRUCTURED_PROFILE
               else {DISPOSITION_REGENERATED, DISPOSITION_NO_NOVEL_CANDIDATE})
    issues: list[str] = []
    if receipt.get("codeai_disposition") not in allowed:
        issues.append("source_generation_receipt_disposition_invalid")
    if receipt.get("operating_mode") != MODE_PROPOSAL_ONLY:
        issues.append("source_generation_receipt_not_proposal_only")
    if receipt.get("route_receipt_recorded") is not True:
        issues.append("source_generation_route_not_recorded")
    if receipt.get("repository_snapshot_read_only") is not True:
        issues.append("source_generation_repository_snapshot_not_read_only")
    if receipt.get("candidate_selected") is not False:
        issues.append("source_generation_candidate_already_selected")
    for field in (
        "patch_applied", "repository_mutation_performed", "git_ref_changed",
        "selection_authority_granted", "verification_authority_granted",
        "execution_authority_granted",
    ):
        if receipt.get(field) is not False:
            issues.append("source_generation_effect_or_authority_invalid:" + field)
    return issues

__all__ = [name for name in globals() if not name.startswith("__")]
