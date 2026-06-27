#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_connection_admission_types_v0_63 import (
    ADMIT,
    ALLOWED_DECISIONS,
    BLOCKED,
    DEFER,
    DEFERRED,
    EXTERNAL_SUPERVISOR_CLASS,
    LICENSE_VERSION,
    READY,
    REJECT,
    REJECTED,
    REQUEST_VERSION,
    STAGING_SCOPE,
    VERSION,
    ConnectionAdmissionReceipt,
    ConnectionAdmissionRequest,
    SupervisorAdmissionLicense,
    license_digest,
    request_digest,
)
from runtime.kuuos_connection_candidate_search_v0_62 import ConnectionCandidateProposal
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest


def build_connection_admission_request(
    proposal: ConnectionCandidateProposal,
    *,
    request_id: str,
    requested_by: str,
) -> ConnectionAdmissionRequest:
    if proposal.route != "PROPOSE_CONNECTION_UPDATE":
        raise ValueError("proposal_not_ready_for_admission")
    if proposal.selected_receipt is None or proposal.selected_connection is None:
        raise ValueError("selected_connection_missing")
    receipt = proposal.selected_receipt
    if not receipt.admissible:
        raise ValueError("selected_receipt_not_admissible")
    if not receipt.candidate_only or receipt.state_write_performed:
        raise ValueError("selected_receipt_boundary_invalid")
    if not request_id:
        raise ValueError("admission_request_id_missing")
    if not requested_by:
        raise ValueError("admission_requester_missing")

    request = ConnectionAdmissionRequest(
        request_id=request_id,
        requested_by=requested_by,
        source_bundle_digest=proposal.source_bundle_digest,
        proposal_digest=canonical_digest(proposal.to_dict()),
        selected_receipt_digest=receipt.receipt_digest,
        candidate_connection_digest=receipt.candidate_connection_digest,
        rollback_digest=receipt.rollback_digest,
        requested_scope=STAGING_SCOPE,
        candidate_only=True,
        state_write_requested=False,
        request_digest="",
    )
    return replace(request, request_digest=request_digest(request))


def seal_supervisor_admission_license(
    request: ConnectionAdmissionRequest,
    *,
    license_id: str,
    supervisor_id: str,
    decision: str,
    valid_from_epoch: int,
    valid_through_epoch: int,
    supervisor_class: str = EXTERNAL_SUPERVISOR_CLASS,
    allowed_scopes: tuple[str, ...] = (STAGING_SCOPE,),
    production_apply_allowed: bool = False,
    state_write_allowed: bool = False,
    privilege_escalation_allowed: bool = False,
) -> SupervisorAdmissionLicense:
    if not license_id:
        raise ValueError("admission_license_id_missing")
    if not supervisor_id:
        raise ValueError("admission_supervisor_id_missing")
    license_packet = SupervisorAdmissionLicense(
        license_id=license_id,
        supervisor_id=supervisor_id,
        supervisor_class=supervisor_class,
        decision=decision,
        bound_request_digest=request.request_digest,
        bound_source_bundle_digest=request.source_bundle_digest,
        bound_selected_receipt_digest=request.selected_receipt_digest,
        bound_candidate_connection_digest=request.candidate_connection_digest,
        bound_rollback_digest=request.rollback_digest,
        allowed_scopes=tuple(allowed_scopes),
        valid_from_epoch=valid_from_epoch,
        valid_through_epoch=valid_through_epoch,
        production_apply_allowed=production_apply_allowed,
        state_write_allowed=state_write_allowed,
        privilege_escalation_allowed=privilege_escalation_allowed,
        license_digest="",
    )
    return replace(license_packet, license_digest=license_digest(license_packet))


def _valid_epoch(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def evaluate_connection_admission(
    proposal: ConnectionCandidateProposal,
    request: ConnectionAdmissionRequest,
    license_packet: SupervisorAdmissionLicense,
    *,
    current_epoch: int,
) -> ConnectionAdmissionReceipt:
    blockers: list[str] = []
    warnings: list[str] = []

    selected = proposal.selected_receipt
    if proposal.route != "PROPOSE_CONNECTION_UPDATE":
        blockers.append("proposal_route_not_admissible")
    if selected is None or proposal.selected_connection is None:
        blockers.append("proposal_selected_candidate_missing")
    elif not selected.admissible:
        blockers.append("proposal_selected_receipt_not_admissible")
    elif not selected.candidate_only or selected.state_write_performed:
        blockers.append("proposal_selected_receipt_boundary_invalid")

    proposal_digest = canonical_digest(proposal.to_dict())
    if request.version != REQUEST_VERSION:
        blockers.append("admission_request_version_invalid")
    if request.request_digest != request_digest(request):
        blockers.append("admission_request_digest_invalid")
    if request.proposal_digest != proposal_digest:
        blockers.append("admission_request_proposal_digest_mismatch")
    if request.source_bundle_digest != proposal.source_bundle_digest:
        blockers.append("admission_request_source_bundle_mismatch")
    if request.requested_scope != STAGING_SCOPE:
        blockers.append("admission_request_scope_invalid")
    if not request.candidate_only:
        blockers.append("admission_request_not_candidate_only")
    if request.state_write_requested:
        blockers.append("admission_request_state_write_forbidden")

    expected_receipt_digest = "" if selected is None else selected.receipt_digest
    expected_connection_digest = "" if selected is None else selected.candidate_connection_digest
    expected_rollback_digest = "" if selected is None else selected.rollback_digest
    if request.selected_receipt_digest != expected_receipt_digest:
        blockers.append("admission_request_selected_receipt_mismatch")
    if request.candidate_connection_digest != expected_connection_digest:
        blockers.append("admission_request_candidate_connection_mismatch")
    if request.rollback_digest != expected_rollback_digest:
        blockers.append("admission_request_rollback_mismatch")

    if license_packet.version != LICENSE_VERSION:
        blockers.append("admission_license_version_invalid")
    if license_packet.license_digest != license_digest(license_packet):
        blockers.append("admission_license_digest_invalid")
    if license_packet.decision not in ALLOWED_DECISIONS:
        blockers.append("admission_decision_invalid")
    if license_packet.supervisor_class != EXTERNAL_SUPERVISOR_CLASS:
        blockers.append("admission_external_supervisor_required")
    if not license_packet.supervisor_id:
        blockers.append("admission_supervisor_id_missing")

    bindings = {
        "bound_request_digest": request.request_digest,
        "bound_source_bundle_digest": request.source_bundle_digest,
        "bound_selected_receipt_digest": request.selected_receipt_digest,
        "bound_candidate_connection_digest": request.candidate_connection_digest,
        "bound_rollback_digest": request.rollback_digest,
    }
    for field, expected in bindings.items():
        if getattr(license_packet, field) != expected:
            blockers.append(f"admission_license_{field}_mismatch")

    if license_packet.allowed_scopes != (STAGING_SCOPE,):
        blockers.append("admission_license_scope_widened")
    if license_packet.production_apply_allowed:
        blockers.append("admission_production_apply_forbidden")
    if license_packet.state_write_allowed:
        blockers.append("admission_state_write_forbidden")
    if license_packet.privilege_escalation_allowed:
        blockers.append("admission_privilege_escalation_forbidden")

    if not _valid_epoch(current_epoch):
        blockers.append("admission_current_epoch_invalid")
    if not _valid_epoch(license_packet.valid_from_epoch):
        blockers.append("admission_valid_from_epoch_invalid")
    if not _valid_epoch(license_packet.valid_through_epoch):
        blockers.append("admission_valid_through_epoch_invalid")
    if license_packet.valid_from_epoch > license_packet.valid_through_epoch:
        blockers.append("admission_epoch_window_invalid")
    elif _valid_epoch(current_epoch) and not (
        license_packet.valid_from_epoch <= current_epoch <= license_packet.valid_through_epoch
    ):
        blockers.append("admission_license_outside_validity_window")

    decision = license_packet.decision
    if blockers:
        status = BLOCKED
        staging_ready = False
    elif decision == ADMIT:
        status = READY
        staging_ready = True
    elif decision == REJECT:
        status = REJECTED
        staging_ready = False
        warnings.append("supervisor_rejected_connection_candidate")
    elif decision == DEFER:
        status = DEFERRED
        staging_ready = False
        warnings.append("supervisor_deferred_connection_candidate")
    else:
        status = BLOCKED
        staging_ready = False

    payload = {
        "version": VERSION,
        "status": status,
        "request_digest": request.request_digest,
        "license_digest": license_packet.license_digest,
        "proposal_digest": proposal_digest,
        "selected_receipt_digest": request.selected_receipt_digest,
        "source_bundle_digest": request.source_bundle_digest,
        "candidate_connection_digest": request.candidate_connection_digest,
        "rollback_digest": request.rollback_digest,
        "supervisor_id": license_packet.supervisor_id,
        "decision": decision,
        "staging_scope": STAGING_SCOPE,
        "staging_ready": staging_ready,
        "production_apply_ready": False,
        "candidate_only": True,
        "state_write_performed": False,
        "authority_widened": False,
        "blockers": blockers,
        "warnings": warnings,
    }
    return ConnectionAdmissionReceipt(
        status=status,
        request_digest=request.request_digest,
        license_digest=license_packet.license_digest,
        proposal_digest=proposal_digest,
        selected_receipt_digest=request.selected_receipt_digest,
        source_bundle_digest=request.source_bundle_digest,
        candidate_connection_digest=request.candidate_connection_digest,
        rollback_digest=request.rollback_digest,
        supervisor_id=license_packet.supervisor_id,
        decision=decision,
        staging_scope=STAGING_SCOPE,
        staging_ready=staging_ready,
        production_apply_ready=False,
        candidate_only=True,
        state_write_performed=False,
        authority_widened=False,
        blockers=tuple(blockers),
        warnings=tuple(warnings),
        receipt_digest=canonical_digest(payload),
    )
