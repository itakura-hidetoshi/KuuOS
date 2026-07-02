#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_apoptosis_bounded_execution_preparation_v0_8"

BOUNDED_EXECUTION_PREPARATION_READY = (
    "APOPTOSIS_BOUNDED_EXECUTION_PREPARATION_READY_FOR_EXECUTION_REVIEW"
)
BOUNDED_EXECUTION_PREPARATION_BLOCKED = (
    "APOPTOSIS_BOUNDED_EXECUTION_PREPARATION_BLOCKED"
)
BOUNDED_EXECUTION_PREPARATION_REJECTED = (
    "APOPTOSIS_BOUNDED_EXECUTION_PREPARATION_REJECTED"
)

OBJECTIVE_PREPARE_BOUNDED_EXECUTION_PACKAGE_ONLY = (
    "PREPARE_BOUNDED_EXECUTION_PACKAGE_ONLY"
)


@dataclass(frozen=True)
class ApoptosisBoundedExecutionPreparationPolicy:
    policy_id: str
    allowed_preparer_ids: tuple[str, ...]
    allowed_preparer_organization_ids: tuple[str, ...]
    allowed_objectives: tuple[str, ...]
    allowed_target_resource_ids: tuple[str, ...]
    max_preparation_delay_seconds: int
    max_evidence_age_seconds: int
    max_execution_window_seconds: int
    max_scope_items: int
    require_source_authorization_recomputation: bool
    require_approved_authorization_source: bool
    require_source_subject_binding: bool
    require_source_artifact_binding: bool
    require_execution_authority_designation_binding: bool
    require_preparer_qualification: bool
    require_independent_preparer: bool
    require_conflict_disclosure: bool
    require_no_material_conflict: bool
    require_bounded_scope: bool
    require_target_allowlist: bool
    require_no_irreversible_steps: bool
    require_rollback_plan: bool
    require_recovery_route: bool
    require_stop_conditions: bool
    require_abort_channel: bool
    require_human_oversight: bool
    require_monitoring_plan: bool
    require_evidence_capture_plan: bool
    require_simulation_receipt: bool
    require_protected_core_exclusion: bool
    require_no_institutional_hold: bool
    require_no_emergency_state: bool
    require_package_not_expired: bool
    require_execution_authority_separation: bool
    allow_preparation_record_issuance: bool
    allow_execution_review_next: bool
    allow_execution_request: bool
    allow_execution_decision: bool
    allow_authority_revocation: bool
    allow_quiescence_transition: bool
    allow_terminal_transition: bool
    allow_tombstone_write: bool
    allow_physical_deletion: bool
    allow_live_git_execution: bool
    allow_repository_mutation: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_preparer_ids",
            "allowed_preparer_organization_ids",
            "allowed_objectives",
            "allowed_target_resource_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


def apoptosis_bounded_execution_preparation_policy_digest(
    policy: ApoptosisBoundedExecutionPreparationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisBoundedExecutionPreparationEvidence:
    evidence_id: str
    preparation_id: str
    preparer_id: str
    preparer_organization_id: str
    authorization_authority_id: str
    future_execution_authority_id: str
    preparer_qualification_receipt_digest: str
    preparer_qualification_verified: bool
    preparer_independence_declaration_digest: str
    preparer_independence_declared: bool
    conflict_of_interest_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    subject_id: str
    subject_kind: str
    subject_version: str
    source_authorization_id: str
    source_observation_input_digest: str
    source_observation_policy_digest: str
    source_observation_record_digest: str
    source_candidate_request_digest: str
    source_candidate_policy_digest: str
    source_candidate_record_digest: str
    source_dependency_evidence_digest: str
    source_dependency_review_request_digest: str
    source_dependency_review_policy_digest: str
    source_dependency_review_record_digest: str
    source_authority_evidence_digest: str
    source_authority_review_request_digest: str
    source_authority_review_policy_digest: str
    source_authority_review_record_digest: str
    source_quiescence_evidence_digest: str
    source_quiescence_review_request_digest: str
    source_quiescence_review_policy_digest: str
    source_quiescence_review_record_digest: str
    source_external_review_evidence_digest: str
    source_external_review_request_digest: str
    source_external_review_policy_digest: str
    source_external_review_record_digest: str
    source_independent_authorization_evidence_digest: str
    source_independent_authorization_request_digest: str
    source_independent_authorization_policy_digest: str
    source_independent_authorization_record_digest: str
    execution_scope_digest: str
    execution_scope_items: tuple[str, ...]
    target_resource_ids: tuple[str, ...]
    protected_resource_ids: tuple[str, ...]
    reversible_step_ids: tuple[str, ...]
    irreversible_step_ids: tuple[str, ...]
    rollback_plan_digest: str
    rollback_plan_verified: bool
    recovery_route_digest: str
    recovery_route_verified: bool
    stop_condition_digest: str
    stop_conditions_complete: bool
    abort_channel_digest: str
    abort_channel_available: bool
    human_oversight_digest: str
    human_oversight_available: bool
    monitoring_plan_digest: str
    monitoring_plan_complete: bool
    evidence_capture_plan_digest: str
    evidence_capture_plan_complete: bool
    simulation_receipt_digest: str
    simulation_verified: bool
    requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    package_expiry_at_epoch_seconds: int
    execution_window_seconds: int
    protected_core_excluded: bool
    institutional_hold_active: bool
    emergency_state_active: bool
    evidence_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "execution_scope_items",
            "target_resource_ids",
            "protected_resource_ids",
            "reversible_step_ids",
            "irreversible_step_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


def apoptosis_bounded_execution_preparation_evidence_digest(
    evidence: ApoptosisBoundedExecutionPreparationEvidence,
) -> str:
    payload = evidence.to_dict()
    payload.pop("evidence_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisBoundedExecutionPreparationRequest:
    preparation_id: str
    preparer_id: str
    preparer_organization_id: str
    objective: str
    requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    source_authorization_id: str
    source_authorization_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    preparation_evidence_digest: str
    future_execution_authority_id: str
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_bounded_execution_preparation_request_digest(
    request: ApoptosisBoundedExecutionPreparationRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisBoundedExecutionPreparationRecord:
    preparation_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    preparation_evidence_digest: str
    source_authorization_id: str
    source_authorization_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    preparer_id: str
    preparer_organization_id: str
    objective: str
    requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    future_execution_authority_id: str
    source_recomputed_valid: bool
    source_authorization_approved: bool
    source_subject_binding_valid: bool
    source_artifact_binding_valid: bool
    execution_authority_designation_binding_valid: bool
    preparer_allowed: bool
    preparer_organization_allowed: bool
    preparer_identity_binding_valid: bool
    preparer_qualification_verified: bool
    preparer_independence_declared: bool
    preparer_independent: bool
    independent_from_prior_chain: bool
    independent_from_authorization_authority: bool
    independent_from_execution_authority: bool
    objective_allowed: bool
    preparation_delay_valid: bool
    evidence_valid: bool
    evidence_fresh: bool
    preparation_time_order_valid: bool
    package_not_expired: bool
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    scope_bounded: bool
    target_resources_allowed: bool
    protected_resources_excluded: bool
    no_irreversible_steps: bool
    rollback_plan_verified: bool
    recovery_route_verified: bool
    stop_conditions_complete: bool
    abort_channel_available: bool
    human_oversight_available: bool
    monitoring_plan_complete: bool
    evidence_capture_plan_complete: bool
    simulation_verified: bool
    execution_window_valid: bool
    protected_core_excluded: bool
    institutional_hold_active: bool
    emergency_state_active: bool
    preparation_record_issued: bool
    bounded_execution_package_prepared: bool
    ready_for_execution_review: bool
    execution_review_required_next: bool
    execution_request_issued: bool
    execution_decision_made: bool
    authority_revocation_performed: bool
    quiescence_transition_performed: bool
    terminal_transition_performed: bool
    tombstone_write_performed: bool
    physical_deletion_performed: bool
    live_git_execution_performed: bool
    repository_mutation_performed: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    record_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_bounded_execution_preparation_record_digest(
    record: ApoptosisBoundedExecutionPreparationRecord,
) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
