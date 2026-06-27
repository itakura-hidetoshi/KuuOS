#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_connection_evidence_types_v0_68 import (
    BLOCKED,
    READY,
    REVIEW_SCOPE,
    ConnectionEvidenceCapsule,
    capsule_digest,
)
from runtime.kuuos_connection_orbit_types_v0_67 import (
    READY as GAUGE_READY,
    ConnectionOrbitValidationReceipt,
)
from runtime.kuuos_connection_shadow_types_v0_66 import (
    READY as SHADOW_READY,
    ConnectionShadowReceipt,
)
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_os_curvature_holonomy_v0_61 import OSGaugeBundle


def _valid_receipt_digest(receipt: Any) -> bool:
    payload = receipt.to_dict()
    recorded = payload.pop("receipt_digest", "")
    return bool(recorded) and recorded == canonical_digest(payload)


def _valid_epoch(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def evidence_capsule_blockers(
    source_bundle: OSGaugeBundle,
    shadow_bundle: OSGaugeBundle,
    shadow_receipt: ConnectionShadowReceipt,
    gauge_validation: ConnectionOrbitValidationReceipt,
    *,
    capsule_id: str,
    valid_from_epoch: int,
    valid_through_epoch: int,
) -> tuple[str, ...]:
    blockers: list[str] = []
    source_digest = canonical_digest(source_bundle.to_dict())
    shadow_digest = canonical_digest(shadow_bundle.to_dict())

    if not capsule_id:
        blockers.append("evidence_capsule_id_missing")
    if not _valid_epoch(valid_from_epoch):
        blockers.append("evidence_valid_from_epoch_invalid")
    if not _valid_epoch(valid_through_epoch):
        blockers.append("evidence_valid_through_epoch_invalid")
    if _valid_epoch(valid_from_epoch) and _valid_epoch(valid_through_epoch):
        if valid_from_epoch > valid_through_epoch:
            blockers.append("evidence_validity_window_invalid")

    if not _valid_receipt_digest(shadow_receipt):
        blockers.append("evidence_shadow_receipt_digest_invalid")
    if not _valid_receipt_digest(gauge_validation):
        blockers.append("evidence_gauge_validation_digest_invalid")
    if shadow_receipt.status != SHADOW_READY:
        blockers.append("evidence_shadow_receipt_not_ready")
    if gauge_validation.status != GAUGE_READY:
        blockers.append("evidence_gauge_validation_not_ready")
    if shadow_receipt.blockers:
        blockers.append("evidence_shadow_receipt_has_blockers")
    if gauge_validation.blockers:
        blockers.append("evidence_gauge_validation_has_blockers")
    if not gauge_validation.all_samples_admissible:
        blockers.append("evidence_samples_not_all_admissible")
    if not gauge_validation.rollback_reconstruction_exact:
        blockers.append("evidence_rollback_reconstruction_not_exact")
    if not gauge_validation.source_unchanged:
        blockers.append("evidence_source_not_preserved")
    if not gauge_validation.orbit_only:
        blockers.append("evidence_gauge_scope_invalid")
    if gauge_validation.production_apply_ready:
        blockers.append("evidence_live_scope_invalid")
    if gauge_validation.state_write_performed:
        blockers.append("evidence_state_write_detected")
    if gauge_validation.authority_widened:
        blockers.append("evidence_authority_widened")

    bindings = (
        (shadow_receipt.source_bundle_digest_before, source_digest, "shadow_source_before"),
        (shadow_receipt.source_bundle_digest_after, source_digest, "shadow_source_after"),
        (shadow_receipt.shadow_bundle_digest, shadow_digest, "shadow_bundle"),
        (gauge_validation.source_bundle_digest_before, source_digest, "gauge_source_before"),
        (gauge_validation.source_bundle_digest_after, source_digest, "gauge_source_after"),
        (gauge_validation.shadow_bundle_digest, shadow_digest, "gauge_shadow_bundle"),
        (gauge_validation.shadow_receipt_digest, shadow_receipt.receipt_digest, "shadow_receipt"),
        (gauge_validation.rollback_bundle_digest, source_digest, "rollback_bundle"),
    )
    for actual, expected, name in bindings:
        if actual != expected:
            blockers.append(f"evidence_{name}_binding_mismatch")
    return tuple(blockers)


def build_connection_evidence_capsule(
    source_bundle: OSGaugeBundle,
    shadow_bundle: OSGaugeBundle,
    shadow_receipt: ConnectionShadowReceipt,
    gauge_validation: ConnectionOrbitValidationReceipt,
    *,
    capsule_id: str,
    valid_from_epoch: int,
    valid_through_epoch: int,
) -> ConnectionEvidenceCapsule:
    blockers = evidence_capsule_blockers(
        source_bundle,
        shadow_bundle,
        shadow_receipt,
        gauge_validation,
        capsule_id=capsule_id,
        valid_from_epoch=valid_from_epoch,
        valid_through_epoch=valid_through_epoch,
    )
    capsule = ConnectionEvidenceCapsule(
        status=READY if not blockers else BLOCKED,
        capsule_id=capsule_id,
        review_scope=REVIEW_SCOPE,
        source_bundle_digest=canonical_digest(source_bundle.to_dict()),
        shadow_bundle_digest=canonical_digest(shadow_bundle.to_dict()),
        staging_package_digest=shadow_receipt.staging_package_digest,
        shadow_receipt_digest=shadow_receipt.receipt_digest,
        gauge_validation_digest=gauge_validation.receipt_digest,
        candidate_connection_digest=shadow_receipt.candidate_connection_digest,
        rollback_bundle_digest=gauge_validation.rollback_bundle_digest,
        sample_count=gauge_validation.sample_count,
        valid_from_epoch=valid_from_epoch,
        valid_through_epoch=valid_through_epoch,
        evidence_only=True,
        candidate_only=True,
        live_effect_allowed=False,
        state_write_allowed=False,
        authority_widening_allowed=False,
        blockers=blockers,
        capsule_digest="",
    )
    return replace(capsule, capsule_digest=capsule_digest(capsule))


def validate_connection_evidence_capsule(
    capsule: ConnectionEvidenceCapsule,
    source_bundle: OSGaugeBundle,
    shadow_bundle: OSGaugeBundle,
    shadow_receipt: ConnectionShadowReceipt,
    gauge_validation: ConnectionOrbitValidationReceipt,
    *,
    current_epoch: int,
) -> tuple[str, ...]:
    blockers: list[str] = []
    source_digest = canonical_digest(source_bundle.to_dict())
    shadow_digest = canonical_digest(shadow_bundle.to_dict())

    if capsule.capsule_digest != capsule_digest(capsule):
        blockers.append("evidence_capsule_digest_invalid")
    if capsule.status != READY:
        blockers.append("evidence_capsule_not_ready")
    if capsule.review_scope != REVIEW_SCOPE:
        blockers.append("evidence_capsule_scope_invalid")
    if not capsule.evidence_only:
        blockers.append("evidence_capsule_not_evidence_only")
    if not capsule.candidate_only:
        blockers.append("evidence_capsule_not_candidate_only")
    if capsule.live_effect_allowed:
        blockers.append("evidence_capsule_live_effect_scope_invalid")
    if capsule.state_write_allowed:
        blockers.append("evidence_capsule_state_write_scope_invalid")
    if capsule.authority_widening_allowed:
        blockers.append("evidence_capsule_authority_scope_invalid")
    if capsule.blockers:
        blockers.append("evidence_capsule_contains_blockers")
    if not _valid_epoch(current_epoch):
        blockers.append("evidence_current_epoch_invalid")
    elif not capsule.valid_from_epoch <= current_epoch <= capsule.valid_through_epoch:
        blockers.append("evidence_capsule_outside_validity_window")

    bindings = (
        (capsule.source_bundle_digest, source_digest, "source_bundle"),
        (capsule.shadow_bundle_digest, shadow_digest, "shadow_bundle"),
        (capsule.staging_package_digest, shadow_receipt.staging_package_digest, "staging_package"),
        (capsule.shadow_receipt_digest, shadow_receipt.receipt_digest, "shadow_receipt"),
        (capsule.gauge_validation_digest, gauge_validation.receipt_digest, "gauge_validation"),
        (capsule.candidate_connection_digest, shadow_receipt.candidate_connection_digest, "candidate"),
        (capsule.rollback_bundle_digest, source_digest, "rollback"),
        (capsule.sample_count, gauge_validation.sample_count, "sample_count"),
    )
    for actual, expected, name in bindings:
        if actual != expected:
            blockers.append(f"evidence_capsule_{name}_binding_mismatch")
    blockers.extend(
        evidence_capsule_blockers(
            source_bundle,
            shadow_bundle,
            shadow_receipt,
            gauge_validation,
            capsule_id=capsule.capsule_id,
            valid_from_epoch=capsule.valid_from_epoch,
            valid_through_epoch=capsule.valid_through_epoch,
        )
    )
    return tuple(dict.fromkeys(blockers))
