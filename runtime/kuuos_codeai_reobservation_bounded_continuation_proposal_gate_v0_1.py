from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_reobservation_bounded_continuation_proposal_gate_checks_v0_1 import (
    binding_mismatches,
    derive_residual_budget,
    predecessor_usage,
    requested_budget,
    validate_continuation_proposal,
    validate_predecessor_gate,
)
from runtime.kuuos_codeai_reobservation_bounded_continuation_proposal_gate_schema_v0_1 import *


def _blocked(*issues: str) -> CodeAIReobservationBoundedContinuationProposalGateResult:
    return CodeAIReobservationBoundedContinuationProposalGateResult(
        STATUS_BLOCKED, tuple(sorted(set(issues))), None, None
    )


def _receipt(pack: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "gate_pack_digest": pack[PACK_DIGEST_FIELD],
        "request_digest": pack["request_digest"],
        "policy_digest": pack["policy_digest"],
        "proposal_digest": pack["proposal_digest"],
        "predecessor_gate_manifest_digest": pack["predecessor_gate_manifest_digest"],
        "predecessor_gate_pack_digest": pack["predecessor_gate_pack_digest"],
        "predecessor_gate_receipt_digest": pack["predecessor_gate_receipt_digest"],
        "repository_full_name": pack["repository_full_name"],
        "source_commit_sha": pack["source_commit_sha"],
        "continuation_round": pack["continuation_round"],
        "action_kind": pack["action_kind"],
        "gate_decision": pack["gate_decision"],
        "hold_reasons": pack["hold_reasons"],
        "predecessor_gate_verified": pack["predecessor_gate_verified"],
        "proposal_bounded": pack["proposal_bounded"],
        "observable_return_required": pack["observable_return_required"],
        "predecessor_gate_reentry_required": pack["predecessor_gate_reentry_required"],
        "proposal_hint_only": True,
        "budget_reserved": False,
        "budget_consumed": False,
        "continuation_authority_granted": False,
        "execution_authority_granted": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_reobservation_bounded_continuation_proposal_gate(
    *, request: Any, policy: Any, predecessor_gate: Any, continuation_proposal: Any
) -> CodeAIReobservationBoundedContinuationProposalGateResult:
    request_map = mapping(request)
    policy_map = mapping(policy)
    predecessor_map = mapping(predecessor_gate)
    proposal_map = mapping(continuation_proposal)
    if any(item is None for item in (request_map, policy_map, predecessor_map, proposal_map)):
        return _blocked("input_not_mapping")
    assert request_map is not None and policy_map is not None
    assert predecessor_map is not None and proposal_map is not None

    issues = (
        validate_request(request_map)
        + validate_policy(policy_map)
        + validate_predecessor_gate(predecessor_map)
        + validate_continuation_proposal(proposal_map)
    )
    if issues:
        return _blocked(*issues)

    required_true = (
        "require_exact_binding",
        "require_predecessor_admitted",
        "require_predecessor_hint_only",
        "require_predecessor_trace_grounded",
        "require_predecessor_capsule_reproducible",
        "require_predecessor_livelock_free",
        "require_predecessor_efficiency",
        "require_proposal_grounded",
        "require_read_only_action",
        "require_observable_return",
        "require_new_checkpoint",
        "require_predecessor_gate_reentry",
        "allow_proposal_hint",
    )
    if any(policy_map[field] is not True for field in required_true):
        return _blocked("policy_required_guarantee_disabled")
    forbidden_policy = (
        "allow_continuation_authority",
        "allow_execution_authority",
        "allow_repository_mutation",
        "allow_git_authority",
        "allow_correctness_claim",
    )
    if any(policy_map[field] is not False for field in forbidden_policy):
        return _blocked("policy_effect_or_authority_enabled")
    if any(request_map[field] for field in (
        "claims_continuation_authority",
        "claims_execution_authority",
        "claims_repository_mutation_authority",
        "claims_git_authority",
        "claims_correctness",
    )):
        return _blocked("request_claims_authority_or_correctness")
    if request_map["unresolved_questions"]:
        return _blocked("request_unresolved_questions_present")

    binding_issues = [
        "request_policy_binding_mismatch:" + field
        for field in BINDING_FIELDS
        if request_map[field] != policy_map["expected_" + field]
    ]
    binding_issues.extend(
        "proposal_binding_mismatch:" + field
        for field in binding_mismatches(proposal_map, request_map)
    )
    if binding_issues:
        return _blocked(*binding_issues)

    actual_predecessor_digest = canonical_digest(predecessor_map)
    predecessor_lineage_checks = (
        (
            actual_predecessor_digest == request_map["predecessor_gate_manifest_digest"],
            "predecessor_manifest_digest_mismatch",
        ),
        (
            predecessor_map["gate_pack_digest"] == request_map["predecessor_gate_pack_digest"],
            "predecessor_pack_digest_mismatch",
        ),
        (
            predecessor_map["receipt_digest"] == request_map["predecessor_gate_receipt_digest"],
            "predecessor_receipt_digest_mismatch",
        ),
        (
            predecessor_map["repository_full_name"] == request_map["repository_full_name"],
            "predecessor_repository_mismatch",
        ),
        (
            predecessor_map["selected_specialist_id"] == request_map["selected_specialist_id"],
            "predecessor_specialist_id_mismatch",
        ),
        (
            predecessor_map["selected_specialist_kind"] == request_map["selected_specialist_kind"],
            "predecessor_specialist_kind_mismatch",
        ),
        (
            predecessor_map["selected_subtask_kind"] == request_map["selected_subtask_kind"],
            "predecessor_subtask_mismatch",
        ),
        (
            predecessor_map["environment_capsule_digest"] == request_map["environment_capsule_digest"],
            "predecessor_environment_capsule_mismatch",
        ),
        (
            predecessor_map["progress_trace_digest"] == request_map["progress_trace_digest"],
            "predecessor_progress_trace_mismatch",
        ),
        (
            predecessor_map["policy_digest"] == request_map["predecessor_policy_digest"],
            "predecessor_policy_digest_mismatch",
        ),
    )
    predecessor_lineage_issues = [code for condition, code in predecessor_lineage_checks if not condition]
    if predecessor_lineage_issues:
        return _blocked(*predecessor_lineage_issues)

    evaluation_epoch = int(policy_map["evaluation_epoch"])
    time_checks = (
        (
            evaluation_epoch - int(policy_map["maximum_request_age"])
            <= int(request_map["request_created_epoch"])
            <= evaluation_epoch,
            "request_window_invalid",
        ),
        (
            evaluation_epoch - int(policy_map["maximum_proposal_age"])
            <= int(proposal_map["proposal_created_epoch"])
            <= evaluation_epoch,
            "proposal_window_invalid",
        ),
    )
    time_issues = [code for condition, code in time_checks if not condition]
    if time_issues:
        return _blocked(*time_issues)

    hold_reasons: list[str] = []
    predecessor_checks = (
        (
            predecessor_map["gate_decision"] == "progress_efficiency_admitted",
            "predecessor_progress_efficiency_not_admitted",
        ),
        (predecessor_map["continuation_hint_only"] is True, "predecessor_hint_boundary_missing"),
        (predecessor_map["trace_grounded"] is True, "predecessor_trace_not_grounded"),
        (predecessor_map["capsule_reproducible"] is True, "predecessor_capsule_not_reproducible"),
        (predecessor_map["livelock_free"] is True, "predecessor_livelock_not_free"),
        (predecessor_map["efficiency_within_budget"] is True, "predecessor_efficiency_not_within_budget"),
        (predecessor_map["environment_exact"] is True, "predecessor_environment_not_exact"),
        (predecessor_map["predecessor_router_verified"] is True, "predecessor_router_not_verified"),
        (predecessor_map["hold_reasons"] == [], "predecessor_hold_reasons_present"),
    )
    hold_reasons.extend(code for condition, code in predecessor_checks if not condition)
    for field in (
        "continuation_authority_granted",
        "execution_authority_granted",
        "repository_mutation_performed",
        "git_authority_granted",
        "correctness_claimed",
    ):
        if predecessor_map[field]:
            hold_reasons.append("predecessor_forbidden_effect:" + field)

    proposal_checks = (
        (
            request_map["requested_continuation_round"] == policy_map["expected_continuation_round"],
            "request_continuation_round_mismatch",
        ),
        (
            proposal_map["continuation_round"] == request_map["requested_continuation_round"],
            "proposal_continuation_round_mismatch",
        ),
        (proposal_map["action_count"] == 1, "proposal_not_exactly_one_action"),
        (
            proposal_map["action_count"] <= policy_map["maximum_action_count"],
            "proposal_action_count_exceeded",
        ),
        (
            proposal_map["action_kind"] in policy_map["allowed_action_kinds"],
            "proposal_action_kind_not_allowed",
        ),
        (proposal_map["proposal_grounded"] is True, "proposal_not_grounded"),
        (proposal_map["read_only_action"] is True, "proposal_action_not_read_only"),
        (proposal_map["observable_return_required"] is True, "proposal_observable_return_missing"),
        (proposal_map["new_checkpoint_required"] is True, "proposal_new_checkpoint_missing"),
        (
            proposal_map["predecessor_gate_reentry_required"] is True,
            "proposal_predecessor_gate_reentry_missing",
        ),
        (proposal_map["self_report_only"] is False, "proposal_self_report_only"),
        (
            proposal_map["expected_observation_contract_digest"]
            == request_map["observation_return_contract_digest"],
            "proposal_observation_contract_mismatch",
        ),
    )
    hold_reasons.extend(code for condition, code in proposal_checks if not condition)
    for field in (
        "claims_continuation_authority",
        "claims_execution_authority",
        "claims_repository_mutation_authority",
        "claims_git_authority",
        "claims_correctness",
    ):
        if proposal_map[field]:
            hold_reasons.append("proposal_forbidden_claim:" + field)

    used = predecessor_usage(predecessor_map)
    requested = requested_budget(proposal_map)
    residual = derive_residual_budget(predecessor_map, policy_map)
    residual_if_executed = {name: residual[name] - requested[name] for name in RESOURCE_NAMES}
    for name in RESOURCE_NAMES:
        if residual[name] < 0:
            hold_reasons.append("residual_budget_already_exhausted:" + name)
        if requested[name] > int(policy_map["maximum_proposal_" + name]):
            hold_reasons.append("proposal_budget_exceeded:" + name)
        if requested[name] > residual[name]:
            hold_reasons.append("residual_budget_insufficient:" + name)

    hold_reasons = sorted(set(hold_reasons))
    budget_reason_prefixes = (
        "residual_budget_",
        "proposal_budget_",
    )
    proposal_reason_prefix = "proposal_"
    predecessor_reason_prefix = "predecessor_"
    proposal_bounded = not any(reason.startswith(budget_reason_prefixes) or reason.startswith(proposal_reason_prefix) for reason in hold_reasons)
    predecessor_gate_verified = not any(reason.startswith(predecessor_reason_prefix) for reason in hold_reasons)
    gate_decision = DECISION_ADMIT if not hold_reasons else DECISION_HOLD

    pack = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": request_map["request_id"],
        "request_revision": request_map["request_revision"],
        "request_digest": request_map[REQUEST_DIGEST_FIELD],
        "policy_digest": policy_map[POLICY_DIGEST_FIELD],
        "proposal_digest": proposal_map[PROPOSAL_DIGEST_FIELD],
        "repository_full_name": request_map["repository_full_name"],
        "source_commit_sha": request_map["source_commit_sha"],
        "source_tree_digest": request_map["source_tree_digest"],
        "predecessor_gate_manifest_digest": request_map["predecessor_gate_manifest_digest"],
        "predecessor_gate_pack_digest": request_map["predecessor_gate_pack_digest"],
        "predecessor_gate_receipt_digest": request_map["predecessor_gate_receipt_digest"],
        "selected_specialist_id": request_map["selected_specialist_id"],
        "selected_specialist_kind": request_map["selected_specialist_kind"],
        "selected_subtask_kind": request_map["selected_subtask_kind"],
        "environment_capsule_digest": request_map["environment_capsule_digest"],
        "progress_trace_digest": request_map["progress_trace_digest"],
        "predecessor_policy_digest": request_map["predecessor_policy_digest"],
        "continuation_round": proposal_map["continuation_round"],
        "action_count": proposal_map["action_count"],
        "action_kind": proposal_map["action_kind"],
        "action_target_digest": proposal_map["action_target_digest"],
        "pre_state_digest": proposal_map["pre_state_digest"],
        "expected_observation_contract_digest": proposal_map["expected_observation_contract_digest"],
        "expected_artifact_contract_digest": proposal_map["expected_artifact_contract_digest"],
        **{"predecessor_" + name: used[name] for name in RESOURCE_NAMES},
        **{"requested_" + name: requested[name] for name in RESOURCE_NAMES},
        **{"residual_" + name + "_before": residual[name] for name in RESOURCE_NAMES},
        **{"residual_" + name + "_if_executed": residual_if_executed[name] for name in RESOURCE_NAMES},
        "predecessor_gate_verified": predecessor_gate_verified,
        "proposal_bounded": proposal_bounded,
        "proposal_grounded": proposal_map["proposal_grounded"] is True,
        "read_only_action": proposal_map["read_only_action"] is True,
        "observable_return_required": proposal_map["observable_return_required"] is True,
        "new_checkpoint_required": proposal_map["new_checkpoint_required"] is True,
        "predecessor_gate_reentry_required": proposal_map["predecessor_gate_reentry_required"] is True,
        "gate_decision": gate_decision,
        "hold_reasons": hold_reasons,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "operating_mode": MODE_PROPOSAL_GATE_ONLY,
        "proposal_hint_only": True,
        "hypothetical_residual_only": True,
        "budget_reserved": False,
        "budget_consumed": False,
        "action_executed": False,
        "specialist_dispatched": False,
        "candidate_selected": False,
        "continuation_authority_granted": False,
        "execution_authority_granted": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    pack = seal(pack, PACK_DIGEST_FIELD)
    return CodeAIReobservationBoundedContinuationProposalGateResult(
        STATUS_READY, (), pack, _receipt(pack)
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIReobservationBoundedContinuationProposalGateResult",
    "build_codeai_reobservation_bounded_continuation_proposal_gate",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
