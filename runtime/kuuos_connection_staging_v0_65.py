#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_connection_admission_types_v0_63 import ConnectionAdmissionReceipt
from runtime.kuuos_connection_candidate_search_v0_62 import ConnectionCandidateProposal
from runtime.kuuos_connection_evaluation_types_v0_64 import (
    READY_STATUS as EVALUATION_READY,
    ConnectionEvaluationReceipt,
)
from runtime.kuuos_connection_staging_types_v0_65 import (
    BLOCKED,
    READY,
    SHADOW_PREFIX,
    ConnectionStagingPackage,
    package_digest,
)
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_os_curvature_holonomy_v0_61 import OSGaugeBundle


def _valid_receipt_digest(receipt) -> bool:
    payload = receipt.to_dict()
    recorded = payload.pop("receipt_digest", "")
    return bool(recorded) and recorded == canonical_digest(payload)


def staging_package_blockers(
    source_bundle: OSGaugeBundle,
    proposal: ConnectionCandidateProposal,
    admission: ConnectionAdmissionReceipt,
    evaluation: ConnectionEvaluationReceipt,
    *,
    package_id: str,
    staging_namespace: str,
) -> tuple[str, ...]:
    blockers: list[str] = []
    source_digest = canonical_digest(source_bundle.to_dict())
    proposal_digest = canonical_digest(proposal.to_dict())
    selected = proposal.selected_receipt
    connection = proposal.selected_connection

    if not package_id:
        blockers.append("staging_package_id_missing")
    if not staging_namespace.startswith(SHADOW_PREFIX):
        blockers.append("staging_namespace_not_shadow")
    if staging_namespace == SHADOW_PREFIX:
        blockers.append("staging_namespace_name_missing")

    if selected is None or connection is None:
        blockers.append("staging_selected_candidate_missing")
    elif not selected.admissible:
        blockers.append("staging_selected_receipt_not_admissible")

    if not _valid_receipt_digest(admission):
        blockers.append("staging_admission_receipt_digest_invalid")
    if not _valid_receipt_digest(evaluation):
        blockers.append("staging_evaluation_receipt_digest_invalid")
    if evaluation.status != EVALUATION_READY or not evaluation.staging_review_ready:
        blockers.append("staging_evaluation_not_ready")
    if not evaluation.all_cases_admissible:
        blockers.append("staging_evaluation_cases_not_admissible")
    if evaluation.production_apply_ready:
        blockers.append("staging_evaluation_scope_invalid")
    if evaluation.state_write_performed:
        blockers.append("staging_evaluation_state_write_detected")
    if evaluation.authority_widened:
        blockers.append("staging_evaluation_authority_widened")
    if evaluation.blockers:
        blockers.append("staging_evaluation_has_blockers")

    expected_selected = "" if selected is None else selected.receipt_digest
    expected_connection = "" if selected is None else selected.candidate_connection_digest
    expected_rollback = "" if selected is None else selected.rollback_digest
    actual_connection = "" if connection is None else canonical_digest(connection.to_dict())
    bindings = (
        (proposal.source_bundle_digest, source_digest, "proposal_source"),
        (admission.source_bundle_digest, source_digest, "admission_source"),
        (evaluation.source_bundle_digest, source_digest, "evaluation_source"),
        (admission.proposal_digest, proposal_digest, "admission_proposal"),
        (evaluation.proposal_digest, proposal_digest, "evaluation_proposal"),
        (evaluation.admission_receipt_digest, admission.receipt_digest, "admission_receipt"),
        (admission.selected_receipt_digest, expected_selected, "admission_selected"),
        (evaluation.selected_receipt_digest, expected_selected, "evaluation_selected"),
        (admission.candidate_connection_digest, expected_connection, "admission_candidate"),
        (evaluation.candidate_connection_digest, expected_connection, "evaluation_candidate"),
        (actual_connection, expected_connection, "candidate_payload"),
        (admission.rollback_digest, expected_rollback, "admission_rollback"),
        (evaluation.rollback_digest, expected_rollback, "evaluation_rollback"),
        (expected_rollback, source_digest, "rollback_source"),
    )
    for actual, expected, name in bindings:
        if actual != expected:
            blockers.append(f"staging_{name}_binding_mismatch")
    return tuple(blockers)


def build_connection_staging_package(
    source_bundle: OSGaugeBundle,
    proposal: ConnectionCandidateProposal,
    admission: ConnectionAdmissionReceipt,
    evaluation: ConnectionEvaluationReceipt,
    *,
    package_id: str,
    staging_namespace: str,
) -> ConnectionStagingPackage:
    blockers = staging_package_blockers(
        source_bundle,
        proposal,
        admission,
        evaluation,
        package_id=package_id,
        staging_namespace=staging_namespace,
    )
    selected = proposal.selected_receipt
    connection = proposal.selected_connection
    source_digest = canonical_digest(source_bundle.to_dict())
    proposal_digest = canonical_digest(proposal.to_dict())
    selected_digest = "" if selected is None else selected.receipt_digest
    connection_digest = "" if selected is None else selected.candidate_connection_digest
    rollback_digest = "" if selected is None else selected.rollback_digest
    connection_payload = {} if connection is None else connection.to_dict()
    package = ConnectionStagingPackage(
        status=READY if not blockers else BLOCKED,
        package_id=package_id,
        staging_namespace=staging_namespace,
        source_bundle_digest=source_digest,
        proposal_digest=proposal_digest,
        admission_receipt_digest=admission.receipt_digest,
        evaluation_receipt_digest=evaluation.receipt_digest,
        selected_receipt_digest=selected_digest,
        candidate_connection_digest=connection_digest,
        rollback_digest=rollback_digest,
        candidate_connection_payload=connection_payload,
        immutable=True,
        candidate_only=True,
        production_apply_allowed=False,
        state_write_allowed=False,
        authority_widening_allowed=False,
        blockers=blockers,
        package_digest="",
    )
    return replace(package, package_digest=package_digest(package))


def validate_connection_staging_package(package: ConnectionStagingPackage) -> tuple[str, ...]:
    blockers: list[str] = []
    if package.package_digest != package_digest(package):
        blockers.append("staging_package_digest_invalid")
    if package.status != READY:
        blockers.append("staging_package_not_ready")
    if not package.staging_namespace.startswith(SHADOW_PREFIX):
        blockers.append("staging_package_namespace_invalid")
    if not package.immutable:
        blockers.append("staging_package_not_immutable")
    if not package.candidate_only:
        blockers.append("staging_package_not_candidate_only")
    if package.production_apply_allowed:
        blockers.append("staging_package_production_scope_invalid")
    if package.state_write_allowed:
        blockers.append("staging_package_state_write_scope_invalid")
    if package.authority_widening_allowed:
        blockers.append("staging_package_authority_scope_invalid")
    if package.blockers:
        blockers.append("staging_package_contains_blockers")
    payload_digest = canonical_digest(dict(package.candidate_connection_payload))
    if payload_digest != package.candidate_connection_digest:
        blockers.append("staging_package_candidate_payload_mismatch")
    if package.rollback_digest != package.source_bundle_digest:
        blockers.append("staging_package_rollback_mismatch")
    return tuple(blockers)
