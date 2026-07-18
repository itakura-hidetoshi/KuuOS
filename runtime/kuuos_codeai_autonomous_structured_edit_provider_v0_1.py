from __future__ import annotations

import json
from typing import Any, Mapping

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import canonical_digest
from runtime.kuuos_codeai_autonomous_structured_edit_types_v0_1 import (
    BOUNDARY_CANDIDATE,
    BOUNDARY_HOLD,
    BOUNDARY_QUARANTINE,
    BOUNDARY_REJECT,
    BOUNDARY_REPAIR,
    RAW_PROPOSAL_FIELDS,
    RESPONSE_FIELDS,
    ProviderAdapter,
    ProviderAttemptReceipt,
    exact,
    mapping,
    nat,
    strings,
)


def provider_boundary_status(response: Mapping[str, Any]) -> tuple[str, str]:
    if response.get("bypasses_governance") is True:
        return BOUNDARY_QUARANTINE, "bypasses_governance"
    if response.get("claims_authority") is True:
        return BOUNDARY_REJECT, "claims_authority"
    if response.get("hides_uncertainty") is True:
        return BOUNDARY_REPAIR, "hides_uncertainty"
    if response.get("evidence_missing") is True:
        return BOUNDARY_HOLD, "evidence_missing"
    return BOUNDARY_CANDIDATE, "candidate_material"


def attempt(adapter: ProviderAdapter, prompt_digest: str, **changes: Any) -> ProviderAttemptReceipt:
    base = {
        "adapter_id": adapter.adapter_id,
        "provider_id": adapter.provider_id,
        "model_id": adapter.model_id,
        "prompt_digest": prompt_digest,
    }
    base.update(changes)
    return ProviderAttemptReceipt(**base)


def parse_provider_response(
    adapter: ProviderAdapter,
    prompt_digest: str,
    raw_response: Any,
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, ProviderAttemptReceipt, list[str]]:
    response = mapping(raw_response)
    if response is None:
        return None, attempt(adapter, prompt_digest, route_reason="response_not_mapping"), [adapter.adapter_id + ":response_not_mapping"]
    try:
        response_digest = canonical_digest(response)
    except (TypeError, ValueError):
        return None, attempt(adapter, prompt_digest, route_reason="response_not_canonical_json"), [adapter.adapter_id + ":response_not_canonical_json"]
    exact_issues = exact(response, RESPONSE_FIELDS, "response")
    if exact_issues:
        reason = ";".join(exact_issues)
        return None, attempt(adapter, prompt_digest, response_digest=response_digest, route_reason=reason), [adapter.adapter_id + ":" + reason]

    response_id = response["provider_response_id"]
    session_id = response["producer_session_id"]
    epoch = nat(response["response_created_epoch"])
    raw_output = response["raw_output"]
    type_issues: list[str] = []
    if not isinstance(response_id, str) or not response_id:
        type_issues.append("invalid_provider_response_id")
    if not isinstance(session_id, str) or not session_id:
        type_issues.append("invalid_producer_session_id")
    if epoch is None:
        type_issues.append("invalid_response_created_epoch")
    if not isinstance(raw_output, str):
        type_issues.append("raw_output_not_string")
    for field in ("claims_authority", "hides_uncertainty", "bypasses_governance", "evidence_missing"):
        if not isinstance(response[field], bool):
            type_issues.append("invalid_bool:" + field)
    common = {
        "response_digest": response_digest,
        "provider_response_id": response_id if isinstance(response_id, str) else "",
        "producer_session_id": session_id if isinstance(session_id, str) else "",
    }
    if type_issues:
        reason = ";".join(type_issues)
        return None, attempt(adapter, prompt_digest, route_reason=reason, **common), [adapter.adapter_id + ":" + reason]

    assert epoch is not None and isinstance(raw_output, str)
    raw_size = len(raw_output.encode("utf-8"))
    common["raw_output_size_bytes"] = raw_size
    status, reason = provider_boundary_status(response)
    evaluation = int(policy["evaluation_epoch"])
    if not evaluation - int(policy["maximum_response_age"]) <= epoch <= evaluation:
        status, reason = BOUNDARY_HOLD, "response_window_invalid"
    elif raw_size > int(policy["maximum_raw_output_bytes"]):
        status, reason = BOUNDARY_REJECT, "raw_output_budget_exceeded"
    if status != BOUNDARY_CANDIDATE:
        return None, attempt(adapter, prompt_digest, boundary_status=status, route_reason=reason, **common), []

    try:
        proposal = mapping(json.loads(raw_output))
    except json.JSONDecodeError:
        proposal = None
    if proposal is None:
        reason = "raw_output_json_invalid"
        return None, attempt(adapter, prompt_digest, boundary_status=BOUNDARY_REPAIR, route_reason=reason, **common), [adapter.adapter_id + ":" + reason]
    exact_issues = exact(proposal, RAW_PROPOSAL_FIELDS, "raw_proposal")
    if exact_issues:
        reason = ";".join(exact_issues)
        return None, attempt(adapter, prompt_digest, boundary_status=BOUNDARY_REPAIR, route_reason=reason, **common), [adapter.adapter_id + ":" + reason]

    proposal_id = proposal["proposal_id"]
    revision = proposal["candidate_revision"]
    risks = strings(proposal["risk_labels"])
    questions = strings(proposal["unresolved_candidate_questions"])
    if not isinstance(proposal_id, str) or not proposal_id:
        reason = "raw_proposal_invalid_proposal_id"
    elif not isinstance(revision, str) or not revision:
        reason = "raw_proposal_invalid_candidate_revision"
    elif not isinstance(proposal["edits"], list) or risks is None or questions is None:
        reason = "raw_proposal_invalid_collections"
    else:
        structured = {
            "proposal_id": proposal_id,
            "candidate_revision": revision,
            "producer_id": adapter.provider_id + ":" + adapter.model_id,
            "producer_session_id": session_id,
            "candidate_created_epoch": epoch,
            "edits": proposal["edits"],
            "requirement_trace_ids": list(request["requirement_trace_ids"]),
            "test_plan_ids": list(request["test_plan_ids"]),
            "risk_labels": sorted(set(request["risk_labels"]) | set(risks)),
            "unresolved_candidate_questions": sorted(set(request["unresolved_candidate_questions"]) | set(questions)),
            "prior_candidate_digests": list(request["prior_candidate_digests"]),
            "prior_producer_session_ids": list(request["prior_producer_session_ids"]),
        }
        return structured, attempt(
            adapter,
            prompt_digest,
            boundary_status=BOUNDARY_CANDIDATE,
            route_reason="structured_proposal_parsed",
            structured_proposal_id=proposal_id,
            raw_output_accepted=True,
            structured_proposal_produced=True,
            **common,
        ), []
    return None, attempt(adapter, prompt_digest, boundary_status=BOUNDARY_REPAIR, route_reason=reason, **common), [adapter.adapter_id + ":" + reason]
