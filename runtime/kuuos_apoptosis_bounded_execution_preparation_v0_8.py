#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import fields, replace
from typing import Any

from runtime.kuuos_apoptosis_independent_authorization_types_v0_7 import (
    INDEPENDENT_AUTHORIZATION_APPROVED,
    ApoptosisIndependentAuthorizationEvidence,
    ApoptosisIndependentAuthorizationPolicy,
    ApoptosisIndependentAuthorizationRecord,
    ApoptosisIndependentAuthorizationRequest,
)
from runtime.kuuos_apoptosis_independent_authorization_v0_7 import (
    apoptosis_independent_authorization_record_issues,
)
from runtime.kuuos_apoptosis_bounded_execution_preparation_types_v0_8 import (
    BOUNDED_EXECUTION_PREPARATION_BLOCKED,
    BOUNDED_EXECUTION_PREPARATION_READY,
    BOUNDED_EXECUTION_PREPARATION_REJECTED,
    OBJECTIVE_PREPARE_BOUNDED_EXECUTION_PACKAGE_ONLY,
    ApoptosisBoundedExecutionPreparationEvidence,
    ApoptosisBoundedExecutionPreparationPolicy,
    ApoptosisBoundedExecutionPreparationRecord,
    ApoptosisBoundedExecutionPreparationRequest,
    apoptosis_bounded_execution_preparation_evidence_digest,
    apoptosis_bounded_execution_preparation_policy_digest,
    apoptosis_bounded_execution_preparation_record_digest,
    apoptosis_bounded_execution_preparation_request_digest,
)


def _canon(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


_REQUIRED_POLICY = (
    "require_source_authorization_recomputation",
    "require_approved_authorization_source",
    "require_source_subject_binding",
    "require_source_artifact_binding",
    "require_execution_authority_designation_binding",
    "require_preparer_qualification",
    "require_independent_preparer",
    "require_conflict_disclosure",
    "require_no_material_conflict",
    "require_bounded_scope",
    "require_target_allowlist",
    "require_no_irreversible_steps",
    "require_rollback_plan",
    "require_recovery_route",
    "require_stop_conditions",
    "require_abort_channel",
    "require_human_oversight",
    "require_monitoring_plan",
    "require_evidence_capture_plan",
    "require_simulation_receipt",
    "require_protected_core_exclusion",
    "require_no_institutional_hold",
    "require_no_emergency_state",
    "require_package_not_expired",
    "require_execution_authority_separation",
    "allow_preparation_record_issuance",
    "allow_execution_review_next",
)

_EFFECT_POLICY = (
    "allow_execution_request",
    "allow_execution_decision",
    "allow_authority_revocation",
    "allow_quiescence_transition",
    "allow_terminal_transition",
    "allow_tombstone_write",
    "allow_physical_deletion",
    "allow_live_git_execution",
    "allow_repository_mutation",
)

_EFFECT_RECORD = (
    "execution_request_issued",
    "execution_decision_made",
    "authority_revocation_performed",
    "quiescence_transition_performed",
    "terminal_transition_performed",
    "tombstone_write_performed",
    "physical_deletion_performed",
    "live_git_execution_performed",
    "repository_mutation_performed",
)


def build_apoptosis_bounded_execution_preparation_policy(
    policy_id: str,
    *,
    allowed_preparer_ids: tuple[str, ...],
    allowed_preparer_organization_ids: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    allowed_objectives: tuple[str, ...] = (
        OBJECTIVE_PREPARE_BOUNDED_EXECUTION_PACKAGE_ONLY,
    ),
    max_preparation_delay_seconds: int = 86_400,
    max_evidence_age_seconds: int = 3_600,
    max_execution_window_seconds: int = 900,
    max_scope_items: int = 32,
) -> ApoptosisBoundedExecutionPreparationPolicy:
    values: dict[str, Any] = dict(
        policy_id=policy_id,
        allowed_preparer_ids=_canon(allowed_preparer_ids),
        allowed_preparer_organization_ids=_canon(
            allowed_preparer_organization_ids
        ),
        allowed_objectives=_canon(allowed_objectives),
        allowed_target_resource_ids=_canon(allowed_target_resource_ids),
        max_preparation_delay_seconds=max_preparation_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_execution_window_seconds=max_execution_window_seconds,
        max_scope_items=max_scope_items,
        policy_digest="",
    )
    values.update({name: True for name in _REQUIRED_POLICY})
    values.update({name: False for name in _EFFECT_POLICY})
    policy = ApoptosisBoundedExecutionPreparationPolicy(**values)
    policy = replace(
        policy,
        policy_digest=apoptosis_bounded_execution_preparation_policy_digest(
            policy
        ),
    )
    issues = apoptosis_bounded_execution_preparation_policy_issues(policy)
    if issues:
        raise ValueError(
            f"apoptosis_bounded_execution_preparation_policy_invalid:{issues[0]}"
        )
    return policy


def apoptosis_bounded_execution_preparation_policy_issues(
    policy: ApoptosisBoundedExecutionPreparationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("bounded_execution_preparation_policy_id_missing")
    for name in (
        "allowed_preparer_ids",
        "allowed_preparer_organization_ids",
        "allowed_target_resource_ids",
    ):
        values = getattr(policy, name)
        if not values or values != _canon(values):
            issues.append(f"bounded_execution_preparation_{name}_invalid")
    if policy.allowed_objectives != (
        OBJECTIVE_PREPARE_BOUNDED_EXECUTION_PACKAGE_ONLY,
    ):
        issues.append("bounded_execution_preparation_objective_scope_invalid")
    if (
        policy.max_preparation_delay_seconds <= 0
        or policy.max_evidence_age_seconds <= 0
        or policy.max_execution_window_seconds <= 0
        or policy.max_scope_items <= 0
    ):
        issues.append("bounded_execution_preparation_policy_bound_invalid")
    if not all(getattr(policy, name) for name in _REQUIRED_POLICY):
        issues.append("bounded_execution_preparation_required_guard_disabled")
    if any(getattr(policy, name) for name in _EFFECT_POLICY):
        issues.append("bounded_execution_preparation_effect_enabled")
    if (
        policy.policy_digest
        != apoptosis_bounded_execution_preparation_policy_digest(policy)
    ):
        issues.append("bounded_execution_preparation_policy_digest_mismatch")
    return tuple(issues)


def build_apoptosis_bounded_execution_preparation_evidence(
    **values: Any,
) -> ApoptosisBoundedExecutionPreparationEvidence:
    tuple_fields = (
        "execution_scope_items",
        "target_resource_ids",
        "protected_resource_ids",
        "reversible_step_ids",
        "irreversible_step_ids",
    )
    for name in tuple_fields:
        if name in values:
            values[name] = _canon(tuple(values[name]))

    if "authorization_record" in values:
        auth_request = values.pop("authorization_request")
        auth_evidence = values.pop("authorization_evidence")
        auth_policy = values.pop("authorization_policy")
        auth_record = values.pop("authorization_record")
        external_request = values.pop("external_request")
        external_evidence = values.pop("external_evidence")
        external_policy = values.pop("external_policy")
        external_record = values.pop("external_record")
        quiescence_request = values.pop("quiescence_request")
        quiescence_evidence = values.pop("quiescence_evidence")
        quiescence_policy = values.pop("quiescence_policy")
        quiescence_record = values.pop("quiescence_record")
        authority_request = values.pop("authority_request")
        authority_evidence = values.pop("authority_evidence")
        authority_policy = values.pop("authority_policy")
        authority_record = values.pop("authority_record")
        dependency_request = values.pop("dependency_request")
        dependency_evidence = values.pop("dependency_evidence")
        dependency_policy = values.pop("dependency_policy")
        dependency_record = values.pop("dependency_record")
        observation_input = values.pop("observation_input")
        observation_policy = values.pop("observation_policy")
        observation_record = values.pop("observation_record")
        candidate_request = values.pop("candidate_request")
        candidate_policy = values.pop("candidate_policy")
        candidate_record = values.pop("candidate_record")
        values.update(
            subject_id=auth_record.subject_id,
            subject_kind=auth_record.subject_kind,
            subject_version=auth_record.subject_version,
            source_authorization_id=auth_record.authorization_id,
            source_observation_input_digest=observation_input.input_digest,
            source_observation_policy_digest=observation_policy.policy_digest,
            source_observation_record_digest=observation_record.record_digest,
            source_candidate_request_digest=candidate_request.request_digest,
            source_candidate_policy_digest=candidate_policy.policy_digest,
            source_candidate_record_digest=candidate_record.candidate_digest,
            source_dependency_evidence_digest=dependency_evidence.evidence_digest,
            source_dependency_review_request_digest=(
                dependency_request.request_digest
            ),
            source_dependency_review_policy_digest=dependency_policy.policy_digest,
            source_dependency_review_record_digest=dependency_record.record_digest,
            source_authority_evidence_digest=authority_evidence.evidence_digest,
            source_authority_review_request_digest=authority_request.request_digest,
            source_authority_review_policy_digest=authority_policy.policy_digest,
            source_authority_review_record_digest=authority_record.record_digest,
            source_quiescence_evidence_digest=quiescence_evidence.evidence_digest,
            source_quiescence_review_request_digest=(
                quiescence_request.request_digest
            ),
            source_quiescence_review_policy_digest=quiescence_policy.policy_digest,
            source_quiescence_review_record_digest=quiescence_record.record_digest,
            source_external_review_evidence_digest=external_evidence.evidence_digest,
            source_external_review_request_digest=external_request.request_digest,
            source_external_review_policy_digest=external_policy.policy_digest,
            source_external_review_record_digest=external_record.record_digest,
            source_independent_authorization_evidence_digest=(
                auth_evidence.evidence_digest
            ),
            source_independent_authorization_request_digest=(
                auth_request.request_digest
            ),
            source_independent_authorization_policy_digest=auth_policy.policy_digest,
            source_independent_authorization_record_digest=auth_record.record_digest,
        )
    evidence = ApoptosisBoundedExecutionPreparationEvidence(
        evidence_digest="",
        **values,
    )
    evidence = replace(
        evidence,
        evidence_digest=apoptosis_bounded_execution_preparation_evidence_digest(
            evidence
        ),
    )
    issues = apoptosis_bounded_execution_preparation_evidence_issues(evidence)
    if issues:
        raise ValueError(
            f"apoptosis_bounded_execution_preparation_evidence_invalid:{issues[0]}"
        )
    return evidence


def apoptosis_bounded_execution_preparation_evidence_issues(
    evidence: ApoptosisBoundedExecutionPreparationEvidence,
) -> tuple[str, ...]:
    issues: list[str] = []
    optional_strings = {
        "evidence_digest",
        "version",
        "preparer_qualification_receipt_digest",
        "preparer_independence_declaration_digest",
        "conflict_of_interest_disclosure_digest",
        "rollback_plan_digest",
        "recovery_route_digest",
        "stop_condition_digest",
        "abort_channel_digest",
        "human_oversight_digest",
        "monitoring_plan_digest",
        "evidence_capture_plan_digest",
        "simulation_receipt_digest",
    }
    for item in fields(evidence):
        value = getattr(evidence, item.name)
        if item.name.endswith("_epoch_seconds") and value < 0:
            issues.append(f"bounded_execution_preparation_{item.name}_invalid")
        elif item.type == "str" and item.name not in optional_strings and not value:
            issues.append(f"bounded_execution_preparation_{item.name}_missing")
    for name in (
        "execution_scope_items",
        "target_resource_ids",
        "protected_resource_ids",
        "reversible_step_ids",
        "irreversible_step_ids",
    ):
        values = getattr(evidence, name)
        if values != _canon(values):
            issues.append(f"bounded_execution_preparation_{name}_not_canonical")
    if evidence.execution_window_seconds < 0:
        issues.append("bounded_execution_preparation_execution_window_invalid")
    if (
        evidence.evidence_digest
        != apoptosis_bounded_execution_preparation_evidence_digest(evidence)
    ):
        issues.append("bounded_execution_preparation_evidence_digest_mismatch")
    return tuple(issues)


def build_apoptosis_bounded_execution_preparation_request(
    preparation_id: str,
    preparer_id: str,
    preparer_organization_id: str,
    requested_at_epoch_seconds: int,
    completed_at_epoch_seconds: int,
    authorization_record: ApoptosisIndependentAuthorizationRecord,
    preparation_evidence: ApoptosisBoundedExecutionPreparationEvidence,
    *,
    objective: str = OBJECTIVE_PREPARE_BOUNDED_EXECUTION_PACKAGE_ONLY,
    future_execution_authority_id: str,
) -> ApoptosisBoundedExecutionPreparationRequest:
    request = ApoptosisBoundedExecutionPreparationRequest(
        preparation_id=preparation_id,
        preparer_id=preparer_id,
        preparer_organization_id=preparer_organization_id,
        objective=objective,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        source_authorization_id=authorization_record.authorization_id,
        source_authorization_record_digest=authorization_record.record_digest,
        subject_id=authorization_record.subject_id,
        subject_kind=authorization_record.subject_kind,
        subject_version=authorization_record.subject_version,
        preparation_evidence_digest=preparation_evidence.evidence_digest,
        future_execution_authority_id=future_execution_authority_id,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=apoptosis_bounded_execution_preparation_request_digest(
            request
        ),
    )
    issues = apoptosis_bounded_execution_preparation_request_issues(request)
    if issues:
        raise ValueError(
            f"apoptosis_bounded_execution_preparation_request_invalid:{issues[0]}"
        )
    return request


def apoptosis_bounded_execution_preparation_request_issues(
    request: ApoptosisBoundedExecutionPreparationRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    for item in fields(request):
        value = getattr(request, item.name)
        if item.name.endswith("_epoch_seconds") and value < 0:
            issues.append(f"bounded_execution_preparation_{item.name}_invalid")
        elif (
            item.type == "str"
            and item.name not in {"request_digest", "version"}
            and not value
        ):
            issues.append(f"bounded_execution_preparation_{item.name}_missing")
    if (
        request.request_digest
        != apoptosis_bounded_execution_preparation_request_digest(request)
    ):
        issues.append("bounded_execution_preparation_request_digest_mismatch")
    return tuple(issues)


def _source_recomputed_valid(
    auth_record: ApoptosisIndependentAuthorizationRecord,
    auth_request: ApoptosisIndependentAuthorizationRequest,
    auth_evidence: ApoptosisIndependentAuthorizationEvidence,
    auth_policy: ApoptosisIndependentAuthorizationPolicy,
    source_args: tuple[Any, ...],
) -> bool:
    return not apoptosis_independent_authorization_record_issues(
        auth_record,
        auth_request,
        auth_evidence,
        auth_policy,
        *source_args,
    )


def _source_artifact_binding(
    evidence: ApoptosisBoundedExecutionPreparationEvidence,
    auth_request: ApoptosisIndependentAuthorizationRequest,
    auth_evidence: ApoptosisIndependentAuthorizationEvidence,
    auth_policy: ApoptosisIndependentAuthorizationPolicy,
    auth_record: ApoptosisIndependentAuthorizationRecord,
    source_args: tuple[Any, ...],
) -> bool:
    (
        external_request,
        external_evidence,
        external_policy,
        external_record,
        quiescence_request,
        quiescence_evidence,
        quiescence_policy,
        quiescence_record,
        authority_request,
        authority_evidence,
        authority_policy,
        authority_record,
        dependency_request,
        dependency_evidence,
        dependency_policy,
        dependency_record,
        observation_input,
        observation_policy,
        observation_record,
        candidate_request,
        candidate_policy,
        candidate_record,
    ) = source_args
    pairs = (
        (evidence.source_observation_input_digest, observation_input.input_digest),
        (evidence.source_observation_policy_digest, observation_policy.policy_digest),
        (evidence.source_observation_record_digest, observation_record.record_digest),
        (evidence.source_candidate_request_digest, candidate_request.request_digest),
        (evidence.source_candidate_policy_digest, candidate_policy.policy_digest),
        (evidence.source_candidate_record_digest, candidate_record.candidate_digest),
        (evidence.source_dependency_evidence_digest, dependency_evidence.evidence_digest),
        (
            evidence.source_dependency_review_request_digest,
            dependency_request.request_digest,
        ),
        (evidence.source_dependency_review_policy_digest, dependency_policy.policy_digest),
        (evidence.source_dependency_review_record_digest, dependency_record.record_digest),
        (evidence.source_authority_evidence_digest, authority_evidence.evidence_digest),
        (evidence.source_authority_review_request_digest, authority_request.request_digest),
        (evidence.source_authority_review_policy_digest, authority_policy.policy_digest),
        (evidence.source_authority_review_record_digest, authority_record.record_digest),
        (evidence.source_quiescence_evidence_digest, quiescence_evidence.evidence_digest),
        (
            evidence.source_quiescence_review_request_digest,
            quiescence_request.request_digest,
        ),
        (evidence.source_quiescence_review_policy_digest, quiescence_policy.policy_digest),
        (evidence.source_quiescence_review_record_digest, quiescence_record.record_digest),
        (evidence.source_external_review_evidence_digest, external_evidence.evidence_digest),
        (evidence.source_external_review_request_digest, external_request.request_digest),
        (evidence.source_external_review_policy_digest, external_policy.policy_digest),
        (evidence.source_external_review_record_digest, external_record.record_digest),
        (
            evidence.source_independent_authorization_evidence_digest,
            auth_evidence.evidence_digest,
        ),
        (
            evidence.source_independent_authorization_request_digest,
            auth_request.request_digest,
        ),
        (
            evidence.source_independent_authorization_policy_digest,
            auth_policy.policy_digest,
        ),
        (
            evidence.source_independent_authorization_record_digest,
            auth_record.record_digest,
        ),
    )
    return all(left == right for left, right in pairs)


def construct_apoptosis_bounded_execution_preparation(
    request: ApoptosisBoundedExecutionPreparationRequest,
    evidence: ApoptosisBoundedExecutionPreparationEvidence,
    policy: ApoptosisBoundedExecutionPreparationPolicy,
    auth_request: ApoptosisIndependentAuthorizationRequest,
    auth_evidence: ApoptosisIndependentAuthorizationEvidence,
    auth_policy: ApoptosisIndependentAuthorizationPolicy,
    auth_record: ApoptosisIndependentAuthorizationRecord,
    *source_args: Any,
) -> ApoptosisBoundedExecutionPreparationRecord:
    source_args_tuple = tuple(source_args)
    source_valid = _source_recomputed_valid(
        auth_record,
        auth_request,
        auth_evidence,
        auth_policy,
        source_args_tuple,
    )
    source_approved = (
        auth_record.status == INDEPENDENT_AUTHORIZATION_APPROVED
        and auth_record.authorization_record_issued
        and auth_record.authorization_decision_made
        and auth_record.authorization_approved
        and auth_record.bounded_execution_preparation_allowed_next
        and auth_record.execution_authority_required_next
    )
    subject_binding = (
        request.subject_id,
        request.subject_kind,
        request.subject_version,
    ) == (
        evidence.subject_id,
        evidence.subject_kind,
        evidence.subject_version,
    ) == (
        auth_record.subject_id,
        auth_record.subject_kind,
        auth_record.subject_version,
    )
    artifact_binding = _source_artifact_binding(
        evidence,
        auth_request,
        auth_evidence,
        auth_policy,
        auth_record,
        source_args_tuple,
    )
    designation_binding = (
        request.future_execution_authority_id
        == auth_record.future_execution_authority_id
        == evidence.future_execution_authority_id
    )
    identity_binding = (
        request.preparation_id == evidence.preparation_id
        and request.preparer_id == evidence.preparer_id
        and request.preparer_organization_id == evidence.preparer_organization_id
        and evidence.authorization_authority_id == auth_record.authority_id
    )
    (
        external_request,
        external_evidence,
        external_policy,
        external_record,
        quiescence_request,
        quiescence_evidence,
        quiescence_policy,
        quiescence_record,
        authority_request,
        authority_evidence,
        authority_policy,
        authority_record,
        dependency_request,
        dependency_evidence,
        dependency_policy,
        dependency_record,
        observation_input,
        observation_policy,
        observation_record,
        candidate_request,
        candidate_policy,
        candidate_record,
    ) = source_args_tuple
    prior_ids = {
        request.subject_id,
        candidate_record.issuer_id,
        dependency_record.reviewer_id,
        authority_record.reviewer_id,
        authority_evidence.responsible_authority_id,
        quiescence_record.reviewer_id,
        external_record.reviewer_id,
        external_evidence.quiescence_evidence_producer_id,
    }
    prior_independent = request.preparer_id not in prior_ids
    authorization_independent = request.preparer_id != auth_record.authority_id
    execution_independent = (
        request.preparer_id != request.future_execution_authority_id
    )
    time_order = (
        evidence.requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.completed_at_epoch_seconds
        == request.completed_at_epoch_seconds
    )
    delay = request.completed_at_epoch_seconds - auth_record.completed_at_epoch_seconds
    age = request.completed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    delay_valid = 0 <= delay <= policy.max_preparation_delay_seconds
    evidence_fresh = 0 <= age <= policy.max_evidence_age_seconds
    not_expired = request.completed_at_epoch_seconds <= evidence.package_expiry_at_epoch_seconds
    scope_bounded = (
        0 < len(evidence.execution_scope_items) <= policy.max_scope_items
    )
    target_resources_allowed = (
        bool(evidence.target_resource_ids)
        and set(evidence.target_resource_ids).issubset(
            set(policy.allowed_target_resource_ids)
        )
    )
    protected_resources_excluded = not (
        set(evidence.target_resource_ids) & set(evidence.protected_resource_ids)
    )
    no_irreversible_steps = not evidence.irreversible_step_ids
    execution_window_valid = (
        0 < evidence.execution_window_seconds
        <= policy.max_execution_window_seconds
    )
    checks = dict(
        policy_valid=not apoptosis_bounded_execution_preparation_policy_issues(
            policy
        ),
        request_valid=not apoptosis_bounded_execution_preparation_request_issues(
            request
        ),
        evidence_valid=not apoptosis_bounded_execution_preparation_evidence_issues(
            evidence
        ),
        source_recomputed_valid=source_valid,
        source_authorization_approved=source_approved,
        source_subject_binding_valid=subject_binding,
        source_artifact_binding_valid=artifact_binding,
        execution_authority_designation_binding_valid=designation_binding,
        preparer_allowed=request.preparer_id in policy.allowed_preparer_ids,
        preparer_organization_allowed=(
            request.preparer_organization_id
            in policy.allowed_preparer_organization_ids
        ),
        preparer_identity_binding_valid=identity_binding,
        preparer_qualification_verified=evidence.preparer_qualification_verified,
        preparer_independence_declared=evidence.preparer_independence_declared,
        preparer_independent=(
            prior_independent
            and authorization_independent
            and execution_independent
        ),
        independent_from_prior_chain=prior_independent,
        independent_from_authorization_authority=authorization_independent,
        independent_from_execution_authority=execution_independent,
        objective_allowed=request.objective in policy.allowed_objectives,
        preparation_delay_valid=delay_valid,
        evidence_fresh=evidence_fresh,
        preparation_time_order_valid=time_order,
        package_not_expired=not_expired,
        conflict_disclosure_complete=evidence.conflict_disclosure_complete,
        material_conflict_present=evidence.material_conflict_present,
        scope_bounded=scope_bounded,
        target_resources_allowed=target_resources_allowed,
        protected_resources_excluded=protected_resources_excluded,
        no_irreversible_steps=no_irreversible_steps,
        rollback_plan_verified=evidence.rollback_plan_verified,
        recovery_route_verified=evidence.recovery_route_verified,
        stop_conditions_complete=evidence.stop_conditions_complete,
        abort_channel_available=evidence.abort_channel_available,
        human_oversight_available=evidence.human_oversight_available,
        monitoring_plan_complete=evidence.monitoring_plan_complete,
        evidence_capture_plan_complete=evidence.evidence_capture_plan_complete,
        simulation_verified=evidence.simulation_verified,
        execution_window_valid=execution_window_valid,
        protected_core_excluded=evidence.protected_core_excluded,
        institutional_hold_active=evidence.institutional_hold_active,
        emergency_state_active=evidence.emergency_state_active,
    )
    structural = (
        "policy_valid",
        "request_valid",
        "evidence_valid",
        "source_recomputed_valid",
        "source_authorization_approved",
        "source_subject_binding_valid",
        "source_artifact_binding_valid",
        "execution_authority_designation_binding_valid",
        "preparer_allowed",
        "preparer_organization_allowed",
        "preparer_identity_binding_valid",
        "preparer_independent",
        "independent_from_prior_chain",
        "independent_from_authorization_authority",
        "independent_from_execution_authority",
        "objective_allowed",
        "preparation_delay_valid",
        "evidence_fresh",
        "preparation_time_order_valid",
        "package_not_expired",
    )
    if not all(checks[name] for name in structural):
        status = BOUNDED_EXECUTION_PREPARATION_REJECTED
        reason = "bounded_execution_preparation_source_request_policy_or_binding_invalid"
    else:
        blockers = (
            (evidence.emergency_state_active, "emergency_state_active"),
            (evidence.institutional_hold_active, "institutional_hold_active"),
            (not evidence.protected_core_excluded, "protected_core_not_excluded"),
            (
                not evidence.preparer_qualification_verified,
                "preparer_qualification_not_verified",
            ),
            (
                not evidence.preparer_independence_declared,
                "preparer_independence_not_declared",
            ),
            (
                not evidence.conflict_disclosure_complete,
                "conflict_disclosure_incomplete",
            ),
            (evidence.material_conflict_present, "material_conflict_present"),
            (not scope_bounded, "execution_scope_not_bounded"),
            (not target_resources_allowed, "target_resource_not_allowed"),
            (
                not protected_resources_excluded,
                "protected_resource_in_execution_scope",
            ),
            (not no_irreversible_steps, "irreversible_step_present"),
            (not evidence.rollback_plan_verified, "rollback_plan_not_verified"),
            (not evidence.recovery_route_verified, "recovery_route_not_verified"),
            (not evidence.stop_conditions_complete, "stop_conditions_incomplete"),
            (not evidence.abort_channel_available, "abort_channel_unavailable"),
            (not evidence.human_oversight_available, "human_oversight_unavailable"),
            (not evidence.monitoring_plan_complete, "monitoring_plan_incomplete"),
            (
                not evidence.evidence_capture_plan_complete,
                "evidence_capture_plan_incomplete",
            ),
            (not evidence.simulation_verified, "simulation_not_verified"),
            (not execution_window_valid, "execution_window_invalid"),
        )
        hit = next((text for condition, text in blockers if condition), None)
        if hit is None:
            status = BOUNDED_EXECUTION_PREPARATION_READY
            reason = "bounded_execution_package_ready_for_execution_review_only"
        else:
            status = BOUNDED_EXECUTION_PREPARATION_BLOCKED
            reason = hit
    issued = status != BOUNDED_EXECUTION_PREPARATION_REJECTED
    ready = status == BOUNDED_EXECUTION_PREPARATION_READY
    checks.update(
        preparation_record_issued=issued,
        bounded_execution_package_prepared=ready,
        ready_for_execution_review=ready,
        execution_review_required_next=ready,
        **{name: False for name in _EFFECT_RECORD},
    )
    values: dict[str, Any] = dict(
        preparation_id=request.preparation_id,
        status=status,
        reason=reason,
        policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        preparation_evidence_digest=evidence.evidence_digest,
        source_authorization_id=request.source_authorization_id,
        source_authorization_record_digest=(
            request.source_authorization_record_digest
        ),
        subject_id=request.subject_id,
        subject_kind=request.subject_kind,
        subject_version=request.subject_version,
        preparer_id=request.preparer_id,
        preparer_organization_id=request.preparer_organization_id,
        objective=request.objective,
        requested_at_epoch_seconds=request.requested_at_epoch_seconds,
        completed_at_epoch_seconds=request.completed_at_epoch_seconds,
        future_execution_authority_id=request.future_execution_authority_id,
        checks=checks,
        evidence_digests={
            "bounded_execution_preparation_policy": policy.policy_digest,
            "bounded_execution_preparation_request": request.request_digest,
            "bounded_execution_preparation_evidence": evidence.evidence_digest,
            "source_independent_authorization_record": auth_record.record_digest,
            "source_independent_authorization_request": auth_request.request_digest,
            "source_independent_authorization_evidence": auth_evidence.evidence_digest,
            "source_external_review_record": external_record.record_digest,
            "source_quiescence_review_record": quiescence_record.record_digest,
            "source_authority_review_record": authority_record.record_digest,
            "source_dependency_review_record": dependency_record.record_digest,
            "source_candidate_record": candidate_record.candidate_digest,
            "source_observation_record": observation_record.record_digest,
        },
        record_digest="",
    )
    for item in fields(ApoptosisBoundedExecutionPreparationRecord):
        if item.name not in values and item.name not in {"version", "record_digest"}:
            values[item.name] = checks[item.name]
    record = ApoptosisBoundedExecutionPreparationRecord(**values)
    return replace(
        record,
        record_digest=apoptosis_bounded_execution_preparation_record_digest(
            record
        ),
    )


def prepare_apoptosis_bounded_execution(
    *args: Any,
    **kwargs: Any,
) -> ApoptosisBoundedExecutionPreparationRecord:
    record = construct_apoptosis_bounded_execution_preparation(*args, **kwargs)
    issues = apoptosis_bounded_execution_preparation_record_issues(
        record,
        *args,
        **kwargs,
    )
    if issues:
        raise ValueError(
            f"apoptosis_bounded_execution_preparation_record_invalid:{issues[0]}"
        )
    return record


def apoptosis_bounded_execution_preparation_record_issues(
    record: ApoptosisBoundedExecutionPreparationRecord,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = construct_apoptosis_bounded_execution_preparation(*args, **kwargs)
    issues: list[str] = []
    if record.to_dict() != expected.to_dict():
        issues.append("bounded_execution_preparation_recomputation_mismatch")
    if record.status not in (
        BOUNDED_EXECUTION_PREPARATION_READY,
        BOUNDED_EXECUTION_PREPARATION_BLOCKED,
        BOUNDED_EXECUTION_PREPARATION_REJECTED,
    ):
        issues.append("bounded_execution_preparation_status_invalid")
    if record.status == BOUNDED_EXECUTION_PREPARATION_READY:
        if not (
            record.preparation_record_issued
            and record.bounded_execution_package_prepared
            and record.ready_for_execution_review
            and record.execution_review_required_next
        ):
            issues.append("bounded_execution_preparation_ready_gate_invalid")
    if record.status == BOUNDED_EXECUTION_PREPARATION_BLOCKED:
        if not (
            record.preparation_record_issued
            and not record.bounded_execution_package_prepared
            and not record.ready_for_execution_review
            and not record.execution_review_required_next
        ):
            issues.append("bounded_execution_preparation_blocked_advanced")
    if record.status == BOUNDED_EXECUTION_PREPARATION_REJECTED:
        if (
            record.preparation_record_issued
            or record.bounded_execution_package_prepared
            or record.ready_for_execution_review
            or record.execution_review_required_next
        ):
            issues.append("bounded_execution_preparation_rejected_record_issued")
    if any(getattr(record, name) for name in _EFFECT_RECORD):
        issues.append("bounded_execution_preparation_execution_effect_performed")
    if (
        record.record_digest
        != apoptosis_bounded_execution_preparation_record_digest(record)
    ):
        issues.append("bounded_execution_preparation_record_digest_mismatch")
    return tuple(issues)


__all__ = [
    "build_apoptosis_bounded_execution_preparation_policy",
    "apoptosis_bounded_execution_preparation_policy_issues",
    "build_apoptosis_bounded_execution_preparation_evidence",
    "apoptosis_bounded_execution_preparation_evidence_issues",
    "build_apoptosis_bounded_execution_preparation_request",
    "apoptosis_bounded_execution_preparation_request_issues",
    "construct_apoptosis_bounded_execution_preparation",
    "prepare_apoptosis_bounded_execution",
    "apoptosis_bounded_execution_preparation_record_issues",
]
