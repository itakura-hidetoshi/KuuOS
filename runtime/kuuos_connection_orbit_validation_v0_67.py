#!/usr/bin/env python3
from __future__ import annotations

from typing import Mapping

from runtime.kuuos_connection_case_evaluation_v0_64 import (
    field_signature,
    memory_observables_preserved,
    source_signature,
)
from runtime.kuuos_connection_orbit_types_v0_67 import (
    BLOCKED,
    READY,
    VERSION,
    ConnectionOrbitValidationReceipt,
    OrbitSampleReceipt,
)
from runtime.kuuos_connection_shadow_types_v0_66 import (
    READY as SHADOW_READY,
    ConnectionShadowReceipt,
)
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)
from runtime.kuuos_os_curvature_holonomy_v0_61 import (
    OSGaugeBundle,
    decompose_os_curvature,
    memory_holonomy,
)


def _valid_receipt_digest(receipt: ConnectionShadowReceipt) -> bool:
    payload = receipt.to_dict()
    recorded = payload.pop("receipt_digest", "")
    return bool(recorded) and recorded == canonical_digest(payload)


def _curvature_residual(left, right) -> float:
    return max(
        abs(left.epistemic_curvature - right.epistemic_curvature),
        abs(left.verification_curvature - right.verification_curvature),
        abs(left.memory_return_curvature - right.memory_return_curvature),
        abs(left.total_curvature - right.total_curvature),
    )


def _holonomy_residual(left, right) -> float:
    return max(
        abs(left.wilson_observable - right.wilson_observable),
        abs(left.holonomy_defect - right.holonomy_defect),
        abs(left.memory_channel_return_energy - right.memory_channel_return_energy),
    )


def _sample_receipt(
    sample_id: str,
    source_bundle: OSGaugeBundle,
    shadow_bundle: OSGaugeBundle,
    local_gauges: Mapping[str, SignedPermutation],
    *,
    tolerance: float,
) -> OrbitSampleReceipt:
    blockers: list[str] = []
    try:
        source_transformed = source_bundle.gauge_transform(local_gauges)
        shadow_transformed = shadow_bundle.gauge_transform(local_gauges)
    except (TypeError, ValueError) as error:
        blockers.append(f"orbit_gauge_transform_invalid:{type(error).__name__}")
        payload = {
            "sample_id": sample_id,
            "source_curvature_residual": 0.0,
            "shadow_curvature_residual": 0.0,
            "source_holonomy_residual": 0.0,
            "shadow_holonomy_residual": 0.0,
            "relative_curvature_nonincreasing": False,
            "relative_memory_holonomy_preserved": False,
            "fields_synchronized": False,
            "source_bindings_synchronized": False,
            "admissible": False,
            "blockers": blockers,
        }
        return OrbitSampleReceipt(
            sample_id=sample_id,
            source_curvature_residual=0.0,
            shadow_curvature_residual=0.0,
            source_holonomy_residual=0.0,
            shadow_holonomy_residual=0.0,
            relative_curvature_nonincreasing=False,
            relative_memory_holonomy_preserved=False,
            fields_synchronized=False,
            source_bindings_synchronized=False,
            admissible=False,
            blockers=tuple(blockers),
            receipt_digest=canonical_digest(payload),
        )

    source_curvature = decompose_os_curvature(source_bundle)
    source_transformed_curvature = decompose_os_curvature(source_transformed)
    shadow_curvature = decompose_os_curvature(shadow_bundle)
    shadow_transformed_curvature = decompose_os_curvature(shadow_transformed)
    source_memory = memory_holonomy(source_bundle)
    source_transformed_memory = memory_holonomy(source_transformed)
    shadow_memory = memory_holonomy(shadow_bundle)
    shadow_transformed_memory = memory_holonomy(shadow_transformed)

    source_curvature_residual = _curvature_residual(
        source_curvature,
        source_transformed_curvature,
    )
    shadow_curvature_residual = _curvature_residual(
        shadow_curvature,
        shadow_transformed_curvature,
    )
    source_holonomy_residual = _holonomy_residual(
        source_memory,
        source_transformed_memory,
    )
    shadow_holonomy_residual = _holonomy_residual(
        shadow_memory,
        shadow_transformed_memory,
    )
    relative_curvature_ok = (
        shadow_transformed_curvature.total_curvature
        <= source_transformed_curvature.total_curvature + tolerance
    )
    relative_holonomy_ok = memory_observables_preserved(
        source_transformed_memory,
        shadow_transformed_memory,
        tolerance,
    )
    fields_ok = field_signature(source_transformed) == field_signature(shadow_transformed)
    bindings_ok = source_signature(source_transformed) == source_signature(shadow_transformed)

    if source_curvature_residual > tolerance:
        blockers.append("orbit_source_curvature_not_invariant")
    if shadow_curvature_residual > tolerance:
        blockers.append("orbit_shadow_curvature_not_invariant")
    if source_holonomy_residual > tolerance:
        blockers.append("orbit_source_holonomy_not_invariant")
    if shadow_holonomy_residual > tolerance:
        blockers.append("orbit_shadow_holonomy_not_invariant")
    if not relative_curvature_ok:
        blockers.append("orbit_relative_curvature_increased")
    if not relative_holonomy_ok:
        blockers.append("orbit_relative_holonomy_changed")
    if not fields_ok:
        blockers.append("orbit_fields_desynchronized")
    if not bindings_ok:
        blockers.append("orbit_source_bindings_desynchronized")

    payload = {
        "sample_id": sample_id,
        "source_curvature_residual": source_curvature_residual,
        "shadow_curvature_residual": shadow_curvature_residual,
        "source_holonomy_residual": source_holonomy_residual,
        "shadow_holonomy_residual": shadow_holonomy_residual,
        "relative_curvature_nonincreasing": relative_curvature_ok,
        "relative_memory_holonomy_preserved": relative_holonomy_ok,
        "fields_synchronized": fields_ok,
        "source_bindings_synchronized": bindings_ok,
        "admissible": not blockers,
        "blockers": blockers,
    }
    return OrbitSampleReceipt(
        sample_id=sample_id,
        source_curvature_residual=source_curvature_residual,
        shadow_curvature_residual=shadow_curvature_residual,
        source_holonomy_residual=source_holonomy_residual,
        shadow_holonomy_residual=shadow_holonomy_residual,
        relative_curvature_nonincreasing=relative_curvature_ok,
        relative_memory_holonomy_preserved=relative_holonomy_ok,
        fields_synchronized=fields_ok,
        source_bindings_synchronized=bindings_ok,
        admissible=not blockers,
        blockers=tuple(blockers),
        receipt_digest=canonical_digest(payload),
    )


def validate_connection_orbit(
    source_bundle: OSGaugeBundle,
    shadow_bundle: OSGaugeBundle,
    shadow_receipt: ConnectionShadowReceipt,
    gauge_samples: Mapping[str, Mapping[str, SignedPermutation]],
    *,
    tolerance: float = 1e-12,
    max_samples: int = 64,
) -> ConnectionOrbitValidationReceipt:
    blockers: list[str] = []
    source_before = canonical_digest(source_bundle.to_dict())
    shadow_digest = canonical_digest(shadow_bundle.to_dict())

    if tolerance < 0.0:
        blockers.append("orbit_tolerance_invalid")
    if not 1 <= max_samples <= 256:
        blockers.append("orbit_max_samples_invalid")
    if not _valid_receipt_digest(shadow_receipt):
        blockers.append("orbit_shadow_receipt_digest_invalid")
    if shadow_receipt.status != SHADOW_READY:
        blockers.append("orbit_shadow_receipt_not_ready")
    if shadow_receipt.source_bundle_digest_before != source_before:
        blockers.append("orbit_source_binding_mismatch")
    if shadow_receipt.source_bundle_digest_after != source_before:
        blockers.append("orbit_source_after_binding_mismatch")
    if shadow_receipt.shadow_bundle_digest != shadow_digest:
        blockers.append("orbit_shadow_binding_mismatch")
    if not shadow_receipt.source_unchanged:
        blockers.append("orbit_source_not_preserved")
    if not shadow_receipt.rollback_witness_ready:
        blockers.append("orbit_rollback_witness_missing")
    if not shadow_receipt.shadow_only:
        blockers.append("orbit_shadow_scope_invalid")
    if shadow_receipt.production_apply_ready:
        blockers.append("orbit_production_scope_invalid")
    if shadow_receipt.state_write_performed:
        blockers.append("orbit_state_write_detected")
    if shadow_receipt.authority_widened:
        blockers.append("orbit_authority_widened")

    normalized = tuple(sorted((str(key), value) for key, value in gauge_samples.items()))
    if not normalized:
        blockers.append("orbit_samples_empty")
    if len(normalized) > max_samples:
        blockers.append("orbit_sample_limit_exceeded")
    if any(not sample_id for sample_id, _ in normalized):
        blockers.append("orbit_sample_id_missing")

    samples = tuple(
        _sample_receipt(
            sample_id,
            source_bundle,
            shadow_bundle,
            gauges,
            tolerance=tolerance,
        )
        for sample_id, gauges in normalized[:max_samples]
    )
    all_samples = bool(samples) and all(sample.admissible for sample in samples)
    if not all_samples:
        blockers.append("orbit_samples_not_all_admissible")

    rollback_bundle = OSGaugeBundle(
        source_bundle.group,
        source_bundle.connection,
        shadow_bundle.fields,
    )
    rollback_digest = canonical_digest(rollback_bundle.to_dict())
    rollback_exact = rollback_digest == source_before
    if not rollback_exact:
        blockers.append("orbit_rollback_reconstruction_mismatch")

    source_after = canonical_digest(source_bundle.to_dict())
    source_unchanged = source_before == source_after
    if not source_unchanged:
        blockers.append("orbit_source_mutated")

    ready = not blockers
    payload = {
        "version": VERSION,
        "status": READY if ready else BLOCKED,
        "source_bundle_digest_before": source_before,
        "source_bundle_digest_after": source_after,
        "shadow_bundle_digest": shadow_digest,
        "shadow_receipt_digest": shadow_receipt.receipt_digest,
        "rollback_bundle_digest": rollback_digest,
        "sample_receipts": [sample.to_dict() for sample in samples],
        "sample_count": len(samples),
        "all_samples_admissible": all_samples,
        "rollback_reconstruction_exact": rollback_exact,
        "source_unchanged": source_unchanged,
        "orbit_only": True,
        "production_apply_ready": False,
        "state_write_performed": False,
        "authority_widened": False,
        "blockers": blockers,
    }
    return ConnectionOrbitValidationReceipt(
        status=payload["status"],
        source_bundle_digest_before=source_before,
        source_bundle_digest_after=source_after,
        shadow_bundle_digest=shadow_digest,
        shadow_receipt_digest=shadow_receipt.receipt_digest,
        rollback_bundle_digest=rollback_digest,
        sample_receipts=samples,
        sample_count=len(samples),
        all_samples_admissible=all_samples,
        rollback_reconstruction_exact=rollback_exact,
        source_unchanged=source_unchanged,
        orbit_only=True,
        production_apply_ready=False,
        state_write_performed=False,
        authority_widened=False,
        blockers=tuple(blockers),
        receipt_digest=canonical_digest(payload),
    )
