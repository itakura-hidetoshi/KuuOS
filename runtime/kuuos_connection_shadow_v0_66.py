#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_connection_candidate_search_v0_62 import ConnectionCandidateProposal
from runtime.kuuos_connection_case_evaluation_v0_64 import (
    connection_domain,
    field_signature,
    memory_observables_preserved,
    source_signature,
)
from runtime.kuuos_connection_shadow_types_v0_66 import (
    BLOCKED,
    READY,
    VERSION,
    ConnectionShadowReceipt,
)
from runtime.kuuos_connection_staging_types_v0_65 import (
    READY as PACKAGE_READY,
    ConnectionStagingPackage,
)
from runtime.kuuos_connection_staging_v0_65 import validate_connection_staging_package
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_os_curvature_holonomy_v0_61 import (
    OSGaugeBundle,
    decompose_os_curvature,
    memory_holonomy,
)


def materialize_connection_shadow(
    source_bundle: OSGaugeBundle,
    proposal: ConnectionCandidateProposal,
    package: ConnectionStagingPackage,
    *,
    tolerance: float = 1e-12,
) -> tuple[OSGaugeBundle | None, ConnectionShadowReceipt]:
    blockers = list(validate_connection_staging_package(package))
    source_before = canonical_digest(source_bundle.to_dict())
    proposal_digest = canonical_digest(proposal.to_dict())
    selected = proposal.selected_receipt
    candidate = proposal.selected_connection

    if package.status != PACKAGE_READY:
        blockers.append("shadow_package_not_ready")
    if proposal.source_bundle_digest != source_before:
        blockers.append("shadow_proposal_source_mismatch")
    if package.source_bundle_digest != source_before:
        blockers.append("shadow_package_source_mismatch")
    if package.proposal_digest != proposal_digest:
        blockers.append("shadow_package_proposal_mismatch")
    if selected is None or candidate is None:
        blockers.append("shadow_candidate_missing")
    else:
        if package.selected_receipt_digest != selected.receipt_digest:
            blockers.append("shadow_selected_receipt_mismatch")
        if package.candidate_connection_digest != selected.candidate_connection_digest:
            blockers.append("shadow_candidate_digest_mismatch")
        if canonical_digest(candidate.to_dict()) != package.candidate_connection_digest:
            blockers.append("shadow_candidate_payload_mismatch")
    if package.rollback_digest != source_before:
        blockers.append("shadow_rollback_source_mismatch")

    shadow_bundle: OSGaugeBundle | None = None
    source_curvature_value: float | None = None
    shadow_curvature_value: float | None = None
    curvature_ok = False
    holonomy_ok = False
    fields_ok = False
    bindings_ok = False

    if candidate is not None:
        if candidate.group != source_bundle.group:
            blockers.append("shadow_group_mismatch")
        if tuple(sorted(candidate.transports)) != connection_domain(source_bundle):
            blockers.append("shadow_connection_domain_mismatch")

    if not blockers and candidate is not None:
        shadow_bundle = OSGaugeBundle(
            source_bundle.group,
            candidate,
            source_bundle.fields,
        )
        source_curvature = decompose_os_curvature(source_bundle)
        shadow_curvature = decompose_os_curvature(shadow_bundle)
        source_memory = memory_holonomy(source_bundle)
        shadow_memory = memory_holonomy(shadow_bundle)
        source_curvature_value = source_curvature.total_curvature
        shadow_curvature_value = shadow_curvature.total_curvature
        curvature_ok = shadow_curvature_value <= source_curvature_value + tolerance
        holonomy_ok = memory_observables_preserved(
            source_memory,
            shadow_memory,
            tolerance,
        )
        fields_ok = field_signature(shadow_bundle) == field_signature(source_bundle)
        bindings_ok = source_signature(shadow_bundle) == source_signature(source_bundle)
        if not curvature_ok:
            blockers.append("shadow_curvature_increased")
        if not holonomy_ok:
            blockers.append("shadow_memory_holonomy_changed")
        if not fields_ok:
            blockers.append("shadow_fields_changed")
        if not bindings_ok:
            blockers.append("shadow_source_bindings_changed")

    source_after = canonical_digest(source_bundle.to_dict())
    source_unchanged = source_before == source_after
    if not source_unchanged:
        blockers.append("shadow_source_mutated")
    rollback_ready = package.rollback_digest == source_before and source_unchanged
    if not rollback_ready:
        blockers.append("shadow_rollback_witness_invalid")

    ready = not blockers and shadow_bundle is not None
    shadow_digest = "" if shadow_bundle is None else canonical_digest(shadow_bundle.to_dict())
    source_connection_digest = canonical_digest(source_bundle.connection.to_dict())
    payload = {
        "version": VERSION,
        "status": READY if ready else BLOCKED,
        "source_bundle_digest_before": source_before,
        "source_bundle_digest_after": source_after,
        "source_connection_digest": source_connection_digest,
        "staging_package_digest": package.package_digest,
        "staging_namespace": package.staging_namespace,
        "candidate_connection_digest": package.candidate_connection_digest,
        "rollback_bundle_digest": package.rollback_digest,
        "shadow_bundle_digest": shadow_digest,
        "source_curvature": source_curvature_value,
        "shadow_curvature": shadow_curvature_value,
        "curvature_nonincreasing": curvature_ok,
        "memory_holonomy_preserved": holonomy_ok,
        "fields_preserved": fields_ok,
        "source_bindings_preserved": bindings_ok,
        "source_unchanged": source_unchanged,
        "rollback_witness_ready": rollback_ready,
        "shadow_only": True,
        "production_apply_ready": False,
        "state_write_performed": False,
        "authority_widened": False,
        "blockers": blockers,
    }
    receipt = ConnectionShadowReceipt(
        status=payload["status"],
        source_bundle_digest_before=source_before,
        source_bundle_digest_after=source_after,
        source_connection_digest=source_connection_digest,
        staging_package_digest=package.package_digest,
        staging_namespace=package.staging_namespace,
        candidate_connection_digest=package.candidate_connection_digest,
        rollback_bundle_digest=package.rollback_digest,
        shadow_bundle_digest=shadow_digest,
        source_curvature=source_curvature_value,
        shadow_curvature=shadow_curvature_value,
        curvature_nonincreasing=curvature_ok,
        memory_holonomy_preserved=holonomy_ok,
        fields_preserved=fields_ok,
        source_bindings_preserved=bindings_ok,
        source_unchanged=source_unchanged,
        rollback_witness_ready=rollback_ready,
        shadow_only=True,
        production_apply_ready=False,
        state_write_performed=False,
        authority_widened=False,
        blockers=tuple(blockers),
        receipt_digest=canonical_digest(payload),
    )
    return shadow_bundle, receipt
