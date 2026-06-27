#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from runtime.kuuos_connection_evaluation_types_v0_64 import (
    ConnectionEvaluationCaseReceipt,
    ConnectionEvaluationPolicy,
)
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_os_curvature_holonomy_v0_61 import (
    OSGaugeBundle,
    decompose_os_curvature,
    memory_holonomy,
)


def connection_domain(bundle: OSGaugeBundle) -> tuple[tuple[str, str], ...]:
    return tuple(sorted(bundle.connection.transports))


def field_signature(bundle: OSGaugeBundle) -> dict[str, Any]:
    return {role: field.to_dict() for role, field in sorted(bundle.fields.items())}


def source_signature(bundle: OSGaugeBundle) -> dict[str, str]:
    return {role: field.source_digest for role, field in sorted(bundle.fields.items())}


def close_value(left: float, right: float, tolerance: float) -> bool:
    return abs(float(left) - float(right)) <= tolerance


def memory_observables_preserved(source, candidate, tolerance: float) -> bool:
    return (
        source.path == candidate.path
        and close_value(source.wilson_observable, candidate.wilson_observable, tolerance)
        and close_value(source.holonomy_defect, candidate.holonomy_defect, tolerance)
        and close_value(
            source.memory_channel_return_energy,
            candidate.memory_channel_return_energy,
            tolerance,
        )
    )


def evaluate_connection_case(
    case_id: str,
    source_bundle: OSGaugeBundle,
    candidate_connection,
    reference_bundle: OSGaugeBundle,
    policy: ConnectionEvaluationPolicy,
) -> ConnectionEvaluationCaseReceipt:
    blockers: list[str] = []
    source_digest = canonical_digest(source_bundle.to_dict())
    group_ok = (
        source_bundle.group == reference_bundle.group
        and candidate_connection.group == source_bundle.group
    )
    domain_ok = (
        connection_domain(source_bundle) == connection_domain(reference_bundle)
        and tuple(sorted(candidate_connection.transports)) == connection_domain(source_bundle)
    )
    if not group_ok:
        blockers.append("evaluation_case_group_mismatch")
    if not domain_ok:
        blockers.append("evaluation_case_connection_domain_mismatch")

    if blockers:
        payload = {
            "case_id": case_id,
            "source_bundle_digest": source_digest,
            "source_curvature": None,
            "candidate_curvature": None,
            "curvature_nonincreasing": False,
            "curvature_strictly_decreased": False,
            "memory_holonomy_preserved": False,
            "fields_preserved": False,
            "source_bindings_preserved": False,
            "admissible": False,
            "blockers": blockers,
        }
        return ConnectionEvaluationCaseReceipt(
            case_id=case_id,
            source_bundle_digest=source_digest,
            source_curvature=None,
            candidate_curvature=None,
            curvature_nonincreasing=False,
            curvature_strictly_decreased=False,
            memory_holonomy_preserved=False,
            fields_preserved=False,
            source_bindings_preserved=False,
            admissible=False,
            blockers=tuple(blockers),
            receipt_digest=canonical_digest(payload),
        )

    candidate_bundle = OSGaugeBundle(
        source_bundle.group,
        candidate_connection,
        source_bundle.fields,
    )
    fields_ok = field_signature(candidate_bundle) == field_signature(source_bundle)
    sources_ok = source_signature(candidate_bundle) == source_signature(source_bundle)
    source_curvature = decompose_os_curvature(source_bundle)
    candidate_curvature = decompose_os_curvature(candidate_bundle)
    source_memory = memory_holonomy(source_bundle)
    candidate_memory = memory_holonomy(candidate_bundle)

    nonincreasing = (
        candidate_curvature.total_curvature
        <= source_curvature.total_curvature + policy.tolerance
    )
    strict = (
        candidate_curvature.total_curvature
        < source_curvature.total_curvature - policy.tolerance
    )
    holonomy_ok = memory_observables_preserved(
        source_memory,
        candidate_memory,
        policy.tolerance,
    )
    if not nonincreasing:
        blockers.append("evaluation_case_curvature_increased")
    if not holonomy_ok:
        blockers.append("evaluation_case_memory_holonomy_changed")
    if not fields_ok:
        blockers.append("evaluation_case_fields_changed")
    if not sources_ok:
        blockers.append("evaluation_case_source_bindings_changed")

    payload = {
        "case_id": case_id,
        "source_bundle_digest": source_digest,
        "source_curvature": source_curvature.total_curvature,
        "candidate_curvature": candidate_curvature.total_curvature,
        "curvature_nonincreasing": nonincreasing,
        "curvature_strictly_decreased": strict,
        "memory_holonomy_preserved": holonomy_ok,
        "fields_preserved": fields_ok,
        "source_bindings_preserved": sources_ok,
        "admissible": not blockers,
        "blockers": blockers,
    }
    return ConnectionEvaluationCaseReceipt(
        case_id=case_id,
        source_bundle_digest=source_digest,
        source_curvature=source_curvature.total_curvature,
        candidate_curvature=candidate_curvature.total_curvature,
        curvature_nonincreasing=nonincreasing,
        curvature_strictly_decreased=strict,
        memory_holonomy_preserved=holonomy_ok,
        fields_preserved=fields_ok,
        source_bindings_preserved=sources_ok,
        admissible=not blockers,
        blockers=tuple(blockers),
        receipt_digest=canonical_digest(payload),
    )
