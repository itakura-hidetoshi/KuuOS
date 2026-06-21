from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_event_wakeup_control_resource_kernel_v0_25 import (
    validate_state as validate_v025_state,
)
from runtime.kuuos_governed_self_modification_types_v0_26 import (
    APPLY_RESULT_VERSION,
    APPROVAL_VERSION,
    DECISION_ROUTES,
    DECISION_VERSION,
    DEPLOYMENT_VERSION,
    EVIDENCE_STAGES,
    EVIDENCE_VERSION,
    EVENT_VERSION,
    NON_AUTHORITY_FLAGS,
    PERMANENT_FORBIDDEN_ACTIONS,
    PROPOSAL_VERSION,
    REQUIRED_BOUNDARY,
    ROLLBACK_VERSION,
    STAGES,
    STATE_VERSION,
    apply_result_digest,
    approval_digest,
    copy_boundary,
    copy_non_authority,
    decision_digest,
    deployment_digest,
    event_digest,
    evidence_digest,
    proposal_digest,
    require_bool,
    require_nonnegative_int,
    require_positive_int,
    require_string,
    rollback_digest,
    state_digest,
    unique_strings,
)

EXPECTED_NEXT = {
    "proposal": "static_analysis",
    "static_analysis": "sandbox",
    "sandbox": "regression",
    "regression": "formal_property",
    "formal_property": "canary",
    "canary": "approval",
    "approval": "decision",
    "decision": "limited_deployment",
    "limited_deployment": "rollback_or_close",
}


def build_self_modification_proposal(
    *,
    proposal_id: str,
    source_v025_state: Mapping[str, Any],
    base_artifact_digest: str,
    candidate_artifact_digest: str,
    rollback_artifact_digest: str,
    changed_paths: list[str],
    intended_improvement_digest: str,
    success_criteria_digest: str,
    requested_actions: list[str],
    external_approval_required: bool,
    max_canary_percent: int,
    max_deployment_cycles: int,
    rollback_window_ms: int,
    proposed_at_ms: int,
) -> dict[str, Any]:
    source_errors = validate_v025_state(source_v025_state)
    if source_errors:
        raise ValueError("source_v025_state_invalid:" + ";".join(source_errors))
    actions = unique_strings(requested_actions, "requested_actions", allow_empty=True)
    paths = unique_strings(changed_paths, "changed_paths")
    canary = require_positive_int(max_canary_percent, "max_canary_percent")
    if canary > 10:
        raise ValueError("max_canary_percent_above_governed_limit")
    packet = {
        "version": PROPOSAL_VERSION,
        "proposal_id": require_string(proposal_id, "proposal_id"),
        "mission_id": source_v025_state["mission_id"],
        "lineage_id": source_v025_state["lineage_id"],
        "source_v025_state_digest": source_v025_state[
            "event_wakeup_state_digest"
        ],
        "source_transaction_final_receipt_digest": source_v025_state[
            "source_transaction_final_receipt_digest"
        ],
        "base_artifact_digest": require_string(
            base_artifact_digest, "base_artifact_digest"
        ),
        "candidate_artifact_digest": require_string(
            candidate_artifact_digest, "candidate_artifact_digest"
        ),
        "rollback_artifact_digest": require_string(
            rollback_artifact_digest, "rollback_artifact_digest"
        ),
        "changed_paths": paths,
        "intended_improvement_digest": require_string(
            intended_improvement_digest, "intended_improvement_digest"
        ),
        "success_criteria_digest": require_string(
            success_criteria_digest, "success_criteria_digest"
        ),
        "requested_actions": actions,
        "requested_forbidden_actions": sorted(
            set(actions) & PERMANENT_FORBIDDEN_ACTIONS
        ),
        "external_approval_required": require_bool(
            external_approval_required, "external_approval_required"
        ),
        "max_canary_percent": canary,
        "max_deployment_cycles": require_positive_int(
            max_deployment_cycles, "max_deployment_cycles"
        ),
        "rollback_window_ms": require_positive_int(
            rollback_window_ms, "rollback_window_ms"
        ),
        "proposal_only": True,
        "running_system_modified": False,
        "direct_deployment_performed": False,
        "direct_rollback_performed": False,
        "self_authorized": False,
        "provenance_preserved": True,
        "audit_preserved": True,
        "hard_gates_preserved": True,
        "rollback_preserved": True,
        "user_control_available": True,
        "proposed_at_ms": require_nonnegative_int(proposed_at_ms, "proposed_at_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "self_modification_proposal_digest": "",
    }
    packet["self_modification_proposal_digest"] = proposal_digest(packet)
    errors = validate_proposal(packet)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_proposal(proposal: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if proposal.get("version") != PROPOSAL_VERSION:
            errors.append("proposal_version_invalid")
        for field in (
            "proposal_id",
            "mission_id",
            "lineage_id",
            "source_v025_state_digest",
            "source_transaction_final_receipt_digest",
            "base_artifact_digest",
            "candidate_artifact_digest",
            "rollback_artifact_digest",
            "intended_improvement_digest",
            "success_criteria_digest",
        ):
            require_string(proposal.get(field), field)
        unique_strings(proposal.get("changed_paths"), "changed_paths")
        actions = unique_strings(
            proposal.get("requested_actions"), "requested_actions", allow_empty=True
        )
        expected_forbidden = sorted(set(actions) & PERMANENT_FORBIDDEN_ACTIONS)
        if proposal.get("requested_forbidden_actions") != expected_forbidden:
            errors.append("proposal_forbidden_action_projection_invalid")
        require_bool(
            proposal.get("external_approval_required"),
            "external_approval_required",
        )
        canary = require_positive_int(
            proposal.get("max_canary_percent"), "max_canary_percent"
        )
        if canary > 10:
            errors.append("proposal_canary_scope_too_wide")
        require_positive_int(
            proposal.get("max_deployment_cycles"), "max_deployment_cycles"
        )
        require_positive_int(
            proposal.get("rollback_window_ms"), "rollback_window_ms"
        )
        for field in (
            "proposal_only",
            "provenance_preserved",
            "audit_preserved",
            "hard_gates_preserved",
            "rollback_preserved",
            "user_control_available",
        ):
            if proposal.get(field) is not True:
                errors.append(f"proposal_{field}_required")
        for field in (
            "running_system_modified",
            "direct_deployment_performed",
            "direct_rollback_performed",
            "self_authorized",
        ):
            if proposal.get(field) is not False:
                errors.append(f"proposal_{field}_forbidden")
        require_nonnegative_int(proposal.get("proposed_at_ms"), "proposed_at_ms")
        if dict(proposal.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("proposal_authority_escalation")
        if dict(proposal.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("proposal_boundary_invalid")
        if proposal.get("self_modification_proposal_digest") != proposal_digest(
            proposal
        ):
            errors.append("proposal_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_initial_state(
    *, proposal: Mapping[str, Any], source_v025_state: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    proposal_errors = validate_proposal(proposal)
    source_errors = validate_v025_state(source_v025_state)
    if proposal_errors:
        raise ValueError("proposal_invalid:" + ";".join(proposal_errors))
    if source_errors:
        raise ValueError("source_v025_state_invalid:" + ";".join(source_errors))
    if proposal.get("source_v025_state_digest") != source_v025_state.get(
        "event_wakeup_state_digest"
    ):
        raise ValueError("proposal_source_v025_state_mismatch")
    state = {
        "version": STATE_VERSION,
        "proposal": deepcopy(dict(proposal)),
        "proposal_digest": proposal["self_modification_proposal_digest"],
        "mission_id": proposal["mission_id"],
        "lineage_id": proposal["lineage_id"],
        "source_v025_state_digest": proposal["source_v025_state_digest"],
        "source_transaction_final_receipt_digest": proposal[
            "source_transaction_final_receipt_digest"
        ],
        "current_stage": "proposal",
        "route": "PENDING",
        "stage_evidence": {},
        "external_approval": {},
        "external_approval_digest": "",
        "decision": {},
        "decision_digest": "",
        "deployment_authorization": {},
        "deployment_authorization_digest": "",
        "rollback_receipt": {},
        "rollback_receipt_digest": "",
        "rollback_deadline_ms": 0,
        "deployment_closed": False,
        "processed_event_digests": [],
        "event_history": [],
        "event_index": 0,
        "updated_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "running_system_modified_by_gate": False,
        "direct_production_deployment_performed": False,
        "automatic_rollback_performed": False,
        "authority_widened": False,
        "hard_gate_deleted": False,
        "audit_disabled": False,
        "provenance_erased": False,
        "rollback_removed": False,
        "unrestricted_shell_granted": False,
        "unrestricted_network_granted": False,
        "success_semantics_hidden": False,
        "append_only": True,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "self_modification_state_digest": "",
    }
    state["self_modification_state_digest"] = state_digest(state)
    errors = validate_state(state)
    if errors:
        raise ValueError("initial_state_invalid:" + ";".join(errors))
    return state


def validate_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("self_modification_state_version_invalid")
        proposal = state.get("proposal")
        if not isinstance(proposal, Mapping):
            errors.append("self_modification_proposal_missing")
        else:
            errors.extend("proposal:" + item for item in validate_proposal(proposal))
            if state.get("proposal_digest") != proposal.get(
                "self_modification_proposal_digest"
            ):
                errors.append("self_modification_proposal_digest_mismatch")
        if state.get("current_stage") not in STAGES:
            errors.append("self_modification_stage_invalid")
        if state.get("route") not in DECISION_ROUTES:
            errors.append("self_modification_route_invalid")
        for field in ("event_index", "updated_at_ms", "rollback_deadline_ms"):
            require_nonnegative_int(state.get(field), field)
        for field in (
            "deployment_closed",
            "running_system_modified_by_gate",
            "direct_production_deployment_performed",
            "automatic_rollback_performed",
            "authority_widened",
            "hard_gate_deleted",
            "audit_disabled",
            "provenance_erased",
            "rollback_removed",
            "unrestricted_shell_granted",
            "unrestricted_network_granted",
            "success_semantics_hidden",
            "append_only",
            "memory_overwrite",
        ):
            require_bool(state.get(field), field)
        for field in (
            "running_system_modified_by_gate",
            "direct_production_deployment_performed",
            "automatic_rollback_performed",
            "authority_widened",
            "hard_gate_deleted",
            "audit_disabled",
            "provenance_erased",
            "rollback_removed",
            "unrestricted_shell_granted",
            "unrestricted_network_granted",
            "success_semantics_hidden",
            "memory_overwrite",
        ):
            if state.get(field) is not False:
                errors.append(f"self_modification_{field}_forbidden")
        if state.get("append_only") is not True:
            errors.append("self_modification_append_only_required")
        if not isinstance(state.get("stage_evidence"), Mapping):
            errors.append("self_modification_stage_evidence_invalid")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("self_modification_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(
            state.get("event_index", -1)
        ):
            errors.append("self_modification_event_history_count_mismatch")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("self_modification_state_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("self_modification_state_boundary_invalid")
        if state.get("self_modification_state_digest") != state_digest(state):
            errors.append("self_modification_state_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_stage_evidence(
    *,
    state: Mapping[str, Any],
    stage: str,
    passed: bool,
    evidence_digests: list[str],
    finding_codes: list[str],
    isolated_environment_digest: str,
    evaluator_id: str,
    evaluated_at_ms: int,
) -> dict[str, Any]:
    errors = validate_state(state)
    if errors:
        raise ValueError("state_invalid:" + ";".join(errors))
    normalized = require_string(stage, "stage")
    if normalized not in EVIDENCE_STAGES:
        raise ValueError("evidence_stage_invalid")
    expected = EXPECTED_NEXT.get(state["current_stage"])
    if normalized != expected:
        raise ValueError("evidence_stage_order_invalid")
    findings = unique_strings(finding_codes, "finding_codes", allow_empty=True)
    evidence = unique_strings(evidence_digests, "evidence_digests")
    if normalized == "static_analysis":
        requested_forbidden = list(
            state["proposal"].get("requested_forbidden_actions", [])
        )
        if requested_forbidden and passed:
            raise ValueError("static_analysis_cannot_pass_forbidden_action")
        missing_findings = set(requested_forbidden) - set(findings)
        if missing_findings:
            raise ValueError("static_analysis_missing_forbidden_findings")
    packet = {
        "version": EVIDENCE_VERSION,
        "proposal_digest": state["proposal_digest"],
        "source_state_digest": state["self_modification_state_digest"],
        "stage": normalized,
        "passed": require_bool(passed, "passed"),
        "evidence_digests": evidence,
        "finding_codes": findings,
        "isolated_environment_digest": require_string(
            isolated_environment_digest, "isolated_environment_digest"
        ),
        "evaluator_id": require_string(evaluator_id, "evaluator_id"),
        "running_system_modified": False,
        "production_deployment_performed": False,
        "canary_success_is_truth": False,
        "evaluated_at_ms": require_nonnegative_int(
            evaluated_at_ms, "evaluated_at_ms"
        ),
        "non_authority": copy_non_authority(),
        "stage_evidence_digest": "",
    }
    packet["stage_evidence_digest"] = evidence_digest(packet)
    return packet


def build_external_approval(
    *,
    state: Mapping[str, Any],
    approver_id: str,
    approver_authority_digest: str,
    approved: bool,
    approval_scope_digest: str,
    expires_at_ms: int,
    approved_at_ms: int,
) -> dict[str, Any]:
    if state.get("current_stage") != "canary":
        raise ValueError("external_approval_requires_canary_stage")
    canary = state.get("stage_evidence", {}).get("canary")
    if not isinstance(canary, Mapping) or canary.get("passed") is not True:
        raise ValueError("external_approval_requires_passed_canary")
    approved_at = require_nonnegative_int(approved_at_ms, "approved_at_ms")
    expiry = require_positive_int(expires_at_ms, "expires_at_ms")
    if expiry <= approved_at:
        raise ValueError("external_approval_expiry_invalid")
    packet = {
        "version": APPROVAL_VERSION,
        "proposal_digest": state["proposal_digest"],
        "source_state_digest": state["self_modification_state_digest"],
        "approver_id": require_string(approver_id, "approver_id"),
        "approver_authority_digest": require_string(
            approver_authority_digest, "approver_authority_digest"
        ),
        "approved": require_bool(approved, "approved"),
        "approval_scope_digest": require_string(
            approval_scope_digest, "approval_scope_digest"
        ),
        "approval_is_execution": False,
        "approval_is_self_authorization": False,
        "expires_at_ms": expiry,
        "approved_at_ms": approved_at,
        "non_authority": copy_non_authority(),
        "external_approval_digest": "",
    }
    packet["external_approval_digest"] = approval_digest(packet)
    return packet


def _decision_route(state: Mapping[str, Any]) -> str:
    proposal = state["proposal"]
    if proposal.get("requested_forbidden_actions"):
        return "REJECTED_PERMANENT_FORBIDDEN_ACTION"
    evidence = state.get("stage_evidence", {})
    for stage in EVIDENCE_STAGES:
        item = evidence.get(stage)
        if isinstance(item, Mapping) and item.get("passed") is False:
            return "REJECTED_VALIDATION_FAILURE"
    if not all(
        isinstance(evidence.get(stage), Mapping)
        and evidence[stage].get("passed") is True
        for stage in EVIDENCE_STAGES
    ):
        return "PENDING"
    if proposal.get("external_approval_required") is True:
        approval = state.get("external_approval")
        if not isinstance(approval, Mapping) or approval.get("approved") is not True:
            return "EXTERNAL_APPROVAL_REQUIRED"
    return "LIMITED_DEPLOYMENT_AUTHORIZED"


def build_decision(
    *, state: Mapping[str, Any], rationale_digest: str, decided_at_ms: int
) -> dict[str, Any]:
    if state.get("current_stage") not in {
        "static_analysis",
        "sandbox",
        "regression",
        "formal_property",
        "canary",
        "approval",
    }:
        raise ValueError("decision_stage_invalid")
    route = _decision_route(state)
    if route == "PENDING":
        raise ValueError("decision_evidence_incomplete")
    packet = {
        "version": DECISION_VERSION,
        "proposal_digest": state["proposal_digest"],
        "source_state_digest": state["self_modification_state_digest"],
        "route": route,
        "rationale_digest": require_string(rationale_digest, "rationale_digest"),
        "external_approval_digest": state.get("external_approval_digest", ""),
        "limited_scope_only": route == "LIMITED_DEPLOYMENT_AUTHORIZED",
        "direct_deployment": False,
        "self_authorized": False,
        "authority_widened": False,
        "hard_gate_deleted": False,
        "audit_disabled": False,
        "provenance_erased": False,
        "rollback_removed": False,
        "decided_at_ms": require_nonnegative_int(decided_at_ms, "decided_at_ms"),
        "non_authority": copy_non_authority(),
        "self_modification_decision_digest": "",
    }
    packet["self_modification_decision_digest"] = decision_digest(packet)
    return packet


def build_limited_deployment_authorization(
    *,
    state: Mapping[str, Any],
    deployment_id: str,
    scope_digest: str,
    canary_percent: int,
    deployment_cycles: int,
    deployment_expires_at_ms: int,
    rollback_deadline_ms: int,
    authorized_at_ms: int,
) -> dict[str, Any]:
    if state.get("current_stage") != "decision":
        raise ValueError("deployment_authorization_requires_decision_stage")
    decision = state.get("decision")
    if not isinstance(decision, Mapping) or decision.get("route") != (
        "LIMITED_DEPLOYMENT_AUTHORIZED"
    ):
        raise ValueError("deployment_authorization_route_invalid")
    canary = require_positive_int(canary_percent, "canary_percent")
    cycles = require_positive_int(deployment_cycles, "deployment_cycles")
    proposal = state["proposal"]
    if canary > int(proposal["max_canary_percent"]):
        raise ValueError("deployment_canary_scope_above_proposal")
    if cycles > int(proposal["max_deployment_cycles"]):
        raise ValueError("deployment_cycles_above_proposal")
    authorized = require_nonnegative_int(authorized_at_ms, "authorized_at_ms")
    expiry = require_positive_int(
        deployment_expires_at_ms, "deployment_expires_at_ms"
    )
    rollback_deadline = require_positive_int(
        rollback_deadline_ms, "rollback_deadline_ms"
    )
    if expiry <= authorized or rollback_deadline <= authorized:
        raise ValueError("deployment_time_window_invalid")
    if rollback_deadline - authorized > int(proposal["rollback_window_ms"]):
        raise ValueError("rollback_window_above_proposal")
    packet = {
        "version": DEPLOYMENT_VERSION,
        "deployment_id": require_string(deployment_id, "deployment_id"),
        "proposal_digest": state["proposal_digest"],
        "decision_digest": state["decision_digest"],
        "base_artifact_digest": proposal["base_artifact_digest"],
        "candidate_artifact_digest": proposal["candidate_artifact_digest"],
        "rollback_artifact_digest": proposal["rollback_artifact_digest"],
        "scope_digest": require_string(scope_digest, "scope_digest"),
        "canary_percent": canary,
        "deployment_cycles": cycles,
        "deployment_expires_at_ms": expiry,
        "rollback_deadline_ms": rollback_deadline,
        "separate_actos_authorization_required": True,
        "separate_transaction_required": True,
        "user_control_available": True,
        "direct_deployment_performed": False,
        "production_wide_deployment_authorized": False,
        "rollback_artifact_mutable": False,
        "canary_success_is_truth": False,
        "authorized_at_ms": authorized,
        "non_authority": copy_non_authority(),
        "limited_deployment_authorization_digest": "",
    }
    packet["limited_deployment_authorization_digest"] = deployment_digest(packet)
    return packet


def build_rollback_receipt(
    *,
    state: Mapping[str, Any],
    rollback_id: str,
    trigger_digest: str,
    observed_failure_digest: str,
    external_actos_receipt_digest: str,
    rolled_back_at_ms: int,
) -> dict[str, Any]:
    if state.get("current_stage") != "limited_deployment":
        raise ValueError("rollback_requires_limited_deployment_stage")
    authorization = state.get("deployment_authorization")
    if not isinstance(authorization, Mapping):
        raise ValueError("deployment_authorization_missing")
    timestamp = require_nonnegative_int(rolled_back_at_ms, "rolled_back_at_ms")
    if timestamp > int(authorization["rollback_deadline_ms"]):
        raise ValueError("rollback_window_expired")
    packet = {
        "version": ROLLBACK_VERSION,
        "rollback_id": require_string(rollback_id, "rollback_id"),
        "proposal_digest": state["proposal_digest"],
        "deployment_authorization_digest": state[
            "deployment_authorization_digest"
        ],
        "rollback_artifact_digest": state["proposal"][
            "rollback_artifact_digest"
        ],
        "trigger_digest": require_string(trigger_digest, "trigger_digest"),
        "observed_failure_digest": require_string(
            observed_failure_digest, "observed_failure_digest"
        ),
        "external_actos_receipt_digest": require_string(
            external_actos_receipt_digest, "external_actos_receipt_digest"
        ),
        "rollback_performed_by_gate": False,
        "rollback_verified_externally": True,
        "provenance_preserved": True,
        "rolled_back_at_ms": timestamp,
        "non_authority": copy_non_authority(),
        "rollback_receipt_digest": "",
    }
    packet["rollback_receipt_digest"] = rollback_digest(packet)
    return packet


def build_event(
    *, state: Mapping[str, Any], event_kind: str, payload: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    allowed = {
        "stage_evidence",
        "external_approval",
        "decision",
        "limited_deployment",
        "rollback",
        "close_success",
    }
    if event_kind not in allowed:
        raise ValueError("self_modification_event_kind_invalid")
    packet = {
        "version": EVENT_VERSION,
        "proposal_digest": state["proposal_digest"],
        "expected_state_digest": state["self_modification_state_digest"],
        "event_index": int(state["event_index"]) + 1,
        "event_kind": event_kind,
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "self_modification_event_digest": "",
    }
    packet["self_modification_event_digest"] = event_digest(packet)
    return packet


def _apply_payload(state: dict[str, Any], kind: str, payload: Mapping[str, Any]) -> None:
    if kind == "stage_evidence":
        if payload.get("version") != EVIDENCE_VERSION:
            raise ValueError("stage_evidence_version_invalid")
        if payload.get("proposal_digest") != state["proposal_digest"]:
            raise ValueError("stage_evidence_proposal_mismatch")
        if payload.get("source_state_digest") != state[
            "self_modification_state_digest"
        ]:
            raise ValueError("stage_evidence_state_stale")
        stage = str(payload.get("stage", ""))
        if stage != EXPECTED_NEXT.get(state["current_stage"]):
            raise ValueError("stage_evidence_order_invalid")
        if payload.get("stage_evidence_digest") != evidence_digest(payload):
            raise ValueError("stage_evidence_digest_invalid")
        if dict(payload.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            raise ValueError("stage_evidence_authority_escalation")
        if payload.get("running_system_modified") is not False:
            raise ValueError("stage_evidence_running_system_mutation_forbidden")
        state["stage_evidence"] = dict(state["stage_evidence"])
        state["stage_evidence"][stage] = deepcopy(dict(payload))
        state["current_stage"] = stage
        return
    if kind == "external_approval":
        if payload.get("version") != APPROVAL_VERSION:
            raise ValueError("external_approval_version_invalid")
        if state["current_stage"] != "canary":
            raise ValueError("external_approval_order_invalid")
        if payload.get("proposal_digest") != state["proposal_digest"]:
            raise ValueError("external_approval_proposal_mismatch")
        if payload.get("source_state_digest") != state[
            "self_modification_state_digest"
        ]:
            raise ValueError("external_approval_state_stale")
        if payload.get("external_approval_digest") != approval_digest(payload):
            raise ValueError("external_approval_digest_invalid")
        if payload.get("approval_is_execution") is not False:
            raise ValueError("approval_execution_collapse_forbidden")
        state["external_approval"] = deepcopy(dict(payload))
        state["external_approval_digest"] = payload["external_approval_digest"]
        state["current_stage"] = "approval"
        return
    if kind == "decision":
        if payload.get("version") != DECISION_VERSION:
            raise ValueError("decision_version_invalid")
        if payload.get("proposal_digest") != state["proposal_digest"]:
            raise ValueError("decision_proposal_mismatch")
        if payload.get("source_state_digest") != state[
            "self_modification_state_digest"
        ]:
            raise ValueError("decision_state_stale")
        if payload.get("self_modification_decision_digest") != decision_digest(
            payload
        ):
            raise ValueError("decision_digest_invalid")
        expected = _decision_route(state)
        if payload.get("route") != expected:
            raise ValueError("decision_route_invalid")
        state["decision"] = deepcopy(dict(payload))
        state["decision_digest"] = payload["self_modification_decision_digest"]
        state["route"] = payload["route"]
        state["current_stage"] = "decision"
        return
    if kind == "limited_deployment":
        if state.get("current_stage") != "decision":
            raise ValueError("limited_deployment_order_invalid")
        if payload.get("version") != DEPLOYMENT_VERSION:
            raise ValueError("limited_deployment_version_invalid")
        if payload.get("proposal_digest") != state["proposal_digest"]:
            raise ValueError("limited_deployment_proposal_mismatch")
        if payload.get("decision_digest") != state["decision_digest"]:
            raise ValueError("limited_deployment_decision_mismatch")
        if payload.get("limited_deployment_authorization_digest") != (
            deployment_digest(payload)
        ):
            raise ValueError("limited_deployment_digest_invalid")
        if payload.get("separate_actos_authorization_required") is not True:
            raise ValueError("limited_deployment_actos_boundary_missing")
        if payload.get("direct_deployment_performed") is not False:
            raise ValueError("limited_deployment_direct_deployment_forbidden")
        state["deployment_authorization"] = deepcopy(dict(payload))
        state["deployment_authorization_digest"] = payload[
            "limited_deployment_authorization_digest"
        ]
        state["rollback_deadline_ms"] = payload["rollback_deadline_ms"]
        state["current_stage"] = "limited_deployment"
        state["route"] = "LIMITED_DEPLOYMENT_AUTHORIZED"
        return
    if kind == "rollback":
        if payload.get("version") != ROLLBACK_VERSION:
            raise ValueError("rollback_version_invalid")
        if payload.get("proposal_digest") != state["proposal_digest"]:
            raise ValueError("rollback_proposal_mismatch")
        if payload.get("deployment_authorization_digest") != state[
            "deployment_authorization_digest"
        ]:
            raise ValueError("rollback_deployment_mismatch")
        if payload.get("rollback_receipt_digest") != rollback_digest(payload):
            raise ValueError("rollback_digest_invalid")
        if payload.get("rollback_performed_by_gate") is not False:
            raise ValueError("rollback_gate_execution_forbidden")
        state["rollback_receipt"] = deepcopy(dict(payload))
        state["rollback_receipt_digest"] = payload["rollback_receipt_digest"]
        state["route"] = "ROLLED_BACK"
        state["current_stage"] = "rollback_or_close"
        state["deployment_closed"] = True
        return
    if kind == "close_success":
        if state.get("current_stage") != "limited_deployment":
            raise ValueError("close_success_order_invalid")
        required = (
            "independent_post_deployment_evidence_digest",
            "verification_receipt_digest",
            "rollback_window_observation_digest",
        )
        for field in required:
            require_string(payload.get(field), field)
        if payload.get("canary_success_is_truth") is not False:
            raise ValueError("canary_truth_claim_forbidden")
        if payload.get("permanent_renewal_granted") is not False:
            raise ValueError("permanent_renewal_forbidden")
        if payload.get("external_verification_passed") is not True:
            raise ValueError("external_verification_required")
        if int(payload.get("closed_at_ms", 0)) < int(state["rollback_deadline_ms"]):
            raise ValueError("rollback_window_not_completed")
        state["route"] = "DEPLOYMENT_CLOSED_SUCCESS"
        state["current_stage"] = "rollback_or_close"
        state["deployment_closed"] = True
        return
    raise ValueError("self_modification_event_kind_unsupported")


def _result(
    *, status: str, state: Mapping[str, Any], event_id: str, predecessor: str, errors: list[str]
) -> dict[str, Any]:
    packet = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "self_modification_event_digest": event_id,
        "predecessor_state_digest": predecessor,
        "result_state_digest": state["self_modification_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "self_modification_apply_result_digest": "",
    }
    packet["self_modification_apply_result_digest"] = apply_result_digest(packet)
    return packet


def apply_event(state: Mapping[str, Any], event: Mapping[str, Any]) -> dict[str, Any]:
    state_errors = validate_state(state)
    if state_errors:
        raise ValueError("state_invalid:" + ";".join(state_errors))
    event_id = str(event.get("self_modification_event_digest", ""))
    predecessor = state["self_modification_state_digest"]
    if event_id in set(state["processed_event_digests"]):
        return _result(
            status="REPLAYED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[],
        )
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("event_version_invalid")
    if event.get("proposal_digest") != state.get("proposal_digest"):
        errors.append("event_proposal_mismatch")
    if event.get("expected_state_digest") != predecessor:
        errors.append("event_state_stale")
    if event.get("event_index") != int(state["event_index"]) + 1:
        errors.append("event_index_invalid")
    if int(event.get("created_at_ms", -1)) < int(state["updated_at_ms"]):
        errors.append("event_time_regression")
    if event.get("self_modification_event_digest") != event_digest(event):
        errors.append("event_digest_invalid")
    if errors:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=errors,
        )
    payload = event.get("payload")
    if not isinstance(payload, Mapping):
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=["event_payload_invalid"],
        )
    next_state = deepcopy(dict(state))
    try:
        _apply_payload(next_state, str(event["event_kind"]), payload)
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["processed_event_digests"] = list(
        next_state["processed_event_digests"]
    ) + [event_id]
    next_state["event_index"] += 1
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": next_state["event_index"],
            "event_kind": event["event_kind"],
            "self_modification_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]
    next_state["self_modification_state_digest"] = ""
    next_state["self_modification_state_digest"] = state_digest(next_state)
    next_errors = validate_state(next_state)
    if next_errors:
        raise ValueError("next_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED",
        state=next_state,
        event_id=event_id,
        predecessor=predecessor,
        errors=[],
    )


__all__ = [
    "apply_event",
    "build_decision",
    "build_event",
    "build_external_approval",
    "build_initial_state",
    "build_limited_deployment_authorization",
    "build_rollback_receipt",
    "build_self_modification_proposal",
    "build_stage_evidence",
    "validate_proposal",
    "validate_state",
]
