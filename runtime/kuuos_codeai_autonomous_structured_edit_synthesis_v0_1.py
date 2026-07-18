#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict
import json
from typing import Any, Mapping, Sequence

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as CANDIDATE_POLICY_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    seal,
)
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import (
    RECEIPT_DIGEST_FIELD as UNIFIED_DIFF_RECEIPT_DIGEST_FIELD,
    STATUS_READY as UNIFIED_DIFF_STATUS_READY,
    GeneratedUnifiedDiffCandidate,
    build_codeai_autonomous_unified_diff_candidates,
)
from runtime.kuuos_codeai_autonomous_structured_edit_types_v0_1 import *
from runtime.kuuos_codeai_autonomous_structured_edit_provider_v0_1 import (
    attempt,
    parse_provider_response,
    provider_boundary_status,
)


def _receipt(
    source: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    candidate_policy: Mapping[str, Any],
    repository: Mapping[str, str],
    adapters: Sequence[ProviderAdapter],
    attempts: Sequence[ProviderAttemptReceipt],
    proposals: Sequence[Mapping[str, Any]],
    downstream_receipt: Mapping[str, Any] | None,
    candidates: Sequence[GeneratedUnifiedDiffCandidate],
    issues: Sequence[str],
) -> dict[str, Any]:
    statuses = (
        BOUNDARY_CANDIDATE,
        BOUNDARY_HOLD,
        BOUNDARY_REPAIR,
        BOUNDARY_REJECT,
        BOUNDARY_QUARANTINE,
    )
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_observation_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "synthesis_request_digest": request[REQUEST_DIGEST_FIELD],
        "synthesis_policy_digest": policy[POLICY_DIGEST_FIELD],
        "candidate_policy_digest": candidate_policy[CANDIDATE_POLICY_DIGEST_FIELD],
        "repository_snapshot_digest": canonical_digest(repository),
        "provider_adapter_set_digest": canonical_digest([
            {"adapter_id": item.adapter_id, "provider_id": item.provider_id, "model_id": item.model_id}
            for item in adapters
        ]),
        "provider_call_count": len(attempts),
        "provider_boundary_status_counts": {
            status: sum(item.boundary_status == status for item in attempts)
            for status in statuses
        },
        "provider_attempt_receipts": [asdict(item) for item in attempts],
        "structured_proposal_count": len(proposals),
        "structured_proposal_ids": [item["proposal_id"] for item in proposals],
        "downstream_unified_diff_receipt_digest": (
            downstream_receipt.get(UNIFIED_DIFF_RECEIPT_DIGEST_FIELD, "")
            if downstream_receipt else ""
        ),
        "generated_candidate_count": len(candidates),
        "generated_candidate_ids": [item.proposal_id for item in candidates],
        "generated_candidate_digests": [
            item.patch_candidate[CANDIDATE_DIGEST_FIELD] for item in candidates
        ],
        "issues": list(issues),
        "codeai_disposition": DISPOSITION_SYNTHESIZED if candidates else DISPOSITION_NO_CANDIDATE,
        "operating_mode": MODE_PROPOSAL_ONLY,
        "route_receipt_recorded": True,
        "provider_calls_performed_by_kernel": bool(attempts),
        "provider_output_boundary_evaluated": bool(attempts),
        "repository_snapshot_read_only": True,
        "raw_provider_output_treated_as_authority": False,
        "provider_name_treated_as_authority": False,
        "structured_proposals_generated_by_kernel": bool(proposals),
        "unified_diff_candidates_generated": bool(candidates),
        "candidate_selected": False,
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
        "selection_authority_granted": False,
        "verification_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
        "provider_output_treated_as_correct": False,
        "generated_candidate_treated_as_correct": False,
        "validation_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(value, RECEIPT_DIGEST_FIELD)


def build_codeai_autonomous_structured_edit_synthesis(
    *,
    source_observation_receipt: Any,
    repository_files: Any,
    synthesis_request: Any,
    provider_adapters: Any,
    synthesis_policy: Any,
    candidate_policy: Any,
) -> CodeAIAutonomousStructuredEditSynthesisResult:
    source = mapping(source_observation_receipt)
    candidate = mapping(candidate_policy)
    repository, repository_issues = validate_repository(repository_files)
    request, request_issues = validate_request(synthesis_request)
    policy, policy_issues = validate_policy(synthesis_policy)
    adapters, adapter_issues = validate_adapters(provider_adapters)
    issues = repository_issues + request_issues + policy_issues + adapter_issues
    if source is None:
        issues.append("source_observation_receipt_not_mapping")
    else:
        if not isinstance(source.get(SOURCE_RECEIPT_DIGEST_FIELD), str):
            issues.append("source_observation_receipt_digest_missing")
        elif not digest_ok(source, SOURCE_RECEIPT_DIGEST_FIELD):
            issues.append("source_observation_receipt_digest_mismatch")
        if source.get("codeai_disposition") != "intent_repository_observation_supported":
            issues.append("source_observation_receipt_not_supported")
        if (
            source.get("operating_mode") != "read_only"
            or source.get("repository_observation_read_only") is not True
        ):
            issues.append("source_observation_receipt_not_read_only")
    if candidate is None:
        issues.append("candidate_policy_not_mapping")
    elif not isinstance(candidate.get(CANDIDATE_POLICY_DIGEST_FIELD), str):
        issues.append("candidate_policy_digest_missing")
    elif not digest_ok(candidate, CANDIDATE_POLICY_DIGEST_FIELD):
        issues.append("candidate_policy_digest_mismatch")
    if issues or None in (source, candidate, repository, request, policy, adapters):
        return CodeAIAutonomousStructuredEditSynthesisResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), (), (), None
        )

    assert source is not None and candidate is not None and repository is not None
    assert request is not None and policy is not None and adapters is not None
    correspondence = (
        (
            "candidate_policy_source_receipt_mismatch",
            candidate.get("expected_source_observation_receipt_digest"),
            source.get(SOURCE_RECEIPT_DIGEST_FIELD),
        ),
        (
            "candidate_policy_repository_mismatch",
            candidate.get("expected_repository_full_name"),
            source.get("repository_full_name"),
        ),
        (
            "candidate_policy_source_commit_mismatch",
            candidate.get("expected_source_commit_sha"),
            source.get("source_commit_sha"),
        ),
    )
    for issue, expected, observed in correspondence:
        if expected != observed:
            return CodeAIAutonomousStructuredEditSynthesisResult(
                STATUS_BLOCKED, (issue,), (), (), None
            )
    evaluation = int(policy["evaluation_epoch"])
    created = int(request["request_created_epoch"])
    if not evaluation - int(policy["maximum_request_age"]) <= created <= evaluation:
        return CodeAIAutonomousStructuredEditSynthesisResult(
            STATUS_BLOCKED, ("synthesis_request_window_invalid",), (), (), None
        )
    scope_issues = repository_scope_issues(repository, policy)
    if scope_issues:
        return CodeAIAutonomousStructuredEditSynthesisResult(
            STATUS_BLOCKED, tuple(sorted(set(scope_issues))), (), (), None
        )
    if len(request["intent_text"].encode("utf-8")) > int(policy["maximum_intent_bytes"]):
        return CodeAIAutonomousStructuredEditSynthesisResult(
            STATUS_BLOCKED, ("intent_budget_exceeded",), (), (), None
        )
    snapshot_bytes = len(json.dumps(
        repository,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8"))
    if snapshot_bytes > int(policy["maximum_repository_snapshot_bytes"]):
        return CodeAIAutonomousStructuredEditSynthesisResult(
            STATUS_BLOCKED, ("repository_snapshot_budget_exceeded",), (), (), None
        )
    if int(request["candidate_count"]) > int(policy["maximum_proposals"]):
        return CodeAIAutonomousStructuredEditSynthesisResult(
            STATUS_BLOCKED, ("requested_candidate_count_exceeds_policy",), (), (), None
        )

    ordered = sorted(adapters, key=lambda item: item.adapter_id)
    disallowed = sorted(
        {item.provider_id for item in ordered}.difference(policy["allowed_provider_ids"])
    )
    if disallowed:
        return CodeAIAutonomousStructuredEditSynthesisResult(
            STATUS_BLOCKED,
            tuple("provider_not_allowed:" + item for item in disallowed),
            (),
            (),
            None,
        )
    limit = min(
        int(request["candidate_count"]),
        int(policy["maximum_provider_calls"]),
        len(ordered),
    )
    attempts: list[ProviderAttemptReceipt] = []
    proposals: list[dict[str, Any]] = []
    route_issues: list[str] = []
    response_ids: set[str] = set()
    session_ids: set[str] = set()
    for index, adapter in enumerate(ordered[:limit], start=1):
        prompt = prompt_packet(request, repository, adapter, index)
        prompt_digest = canonical_digest(prompt)
        try:
            raw_response = adapter.generate(prompt)
        except Exception as exc:
            attempts.append(attempt(
                adapter,
                prompt_digest,
                route_reason="provider_exception:" + type(exc).__name__,
            ))
            route_issues.append(
                adapter.adapter_id + ":provider_exception:" + type(exc).__name__
            )
            continue
        proposal, attempt_receipt, attempt_issues = parse_provider_response(
            adapter, prompt_digest, raw_response, request, policy
        )
        duplicate = ""
        if (
            attempt_receipt.provider_response_id
            and attempt_receipt.provider_response_id in response_ids
        ):
            duplicate = "duplicate_provider_response_id"
        elif (
            attempt_receipt.producer_session_id
            and attempt_receipt.producer_session_id in session_ids
        ):
            duplicate = "duplicate_producer_session_id"
        if attempt_receipt.provider_response_id:
            response_ids.add(attempt_receipt.provider_response_id)
        if attempt_receipt.producer_session_id:
            session_ids.add(attempt_receipt.producer_session_id)
        if duplicate:
            proposal = None
            attempt_receipt = attempt(
                adapter,
                prompt_digest,
                response_digest=attempt_receipt.response_digest,
                provider_response_id=attempt_receipt.provider_response_id,
                producer_session_id=attempt_receipt.producer_session_id,
                route_reason=duplicate,
                raw_output_size_bytes=attempt_receipt.raw_output_size_bytes,
            )
            attempt_issues.append(adapter.adapter_id + ":" + duplicate)
        attempts.append(attempt_receipt)
        route_issues.extend(attempt_issues)
        if proposal is not None:
            proposals.append(proposal)

    downstream = None
    candidates: tuple[GeneratedUnifiedDiffCandidate, ...] = ()
    if proposals:
        downstream = build_codeai_autonomous_unified_diff_candidates(
            source_observation_receipt=source,
            repository_files=repository,
            proposals=proposals,
            candidate_policy=candidate,
        )
        route_issues.extend(downstream.issues)
        if downstream.status == UNIFIED_DIFF_STATUS_READY:
            candidates = downstream.candidates
    receipt = _receipt(
        source,
        request,
        policy,
        candidate,
        repository,
        ordered[:limit],
        attempts,
        proposals,
        downstream.receipt if downstream else None,
        candidates,
        route_issues,
    )
    return CodeAIAutonomousStructuredEditSynthesisResult(
        STATUS_READY if candidates else STATUS_BLOCKED,
        tuple(route_issues),
        tuple(attempts),
        candidates,
        receipt,
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIAutonomousStructuredEditSynthesisResult",
    "ProviderAdapter",
    "ProviderAttemptReceipt",
    "build_codeai_autonomous_structured_edit_synthesis",
    "provider_boundary_status",
]
