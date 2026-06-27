#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    AssociatedField,
    canonical_digest,
)
from runtime.kuuos_memoryos_predictive_shielded_memory_v0_37 import (
    validate_predictive_shielded_memory_capsule,
)
from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_verify_os_kernel_v0_1 import validate_verify_state
from runtime.kuuos_os_gauge_field_types_v0_61 import (
    OSAssociatedGaugeField,
    os_field_values,
)


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name}_mapping_required")
    return value


def _sequence(value: Any, name: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{name}_sequence_required")
    return value


def _unit(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}_number_required")
    number = float(value)
    if number < 0.0 or number > 1.0:
        raise ValueError(f"{name}_unit_interval_required")
    return number


def _mean(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return sum(float(value) for value in values) / float(len(values))


def _history_depth(event_index: Any, phase_count: int) -> float:
    if isinstance(event_index, bool) or not isinstance(event_index, int) or event_index < 0:
        raise ValueError("event_index_invalid")
    return min(1.0, float(event_index) / float(max(1, phase_count)))


def _boundary_digest(source: Mapping[str, Any]) -> str:
    boundary = _mapping(source.get("boundary"), "source_boundary")
    non_authority = _mapping(source.get("non_authority"), "source_non_authority")
    return canonical_digest({"boundary": dict(boundary), "non_authority": dict(non_authority)})


def project_observe_state(
    state: Mapping[str, Any],
    *,
    chart_id: str = "observe",
) -> OSAssociatedGaugeField:
    errors = validate_observe_state(state)
    if errors:
        raise ValueError("observe_state_invalid:" + ";".join(errors))
    if state.get("current_phase") != "commit" or state.get("observation_recorded") is not True:
        raise ValueError("observe_state_not_committed")

    quality = _mapping(state.get("quality_report"), "quality_report")
    quality_components = [
        _unit(quality.get(name), f"observe_{name}")
        for name in ("coverage", "freshness", "provenance", "calibration", "completeness")
    ]
    support = _mean(quality_components)
    conflict = _unit(quality.get("conflict"), "observe_conflict")
    uncertainty = max(1.0 - support, conflict)
    source_digest = str(state.get("observe_state_digest", ""))

    field = AssociatedField(
        field_id=f"observe:{state['observe_id']}",
        chart_id=chart_id,
        values=os_field_values(
            evidence_support=support,
            uncertainty=uncertainty,
            contradiction=conflict,
            criterion_coverage=0.0,
            verification_debt=1.0 if state.get("verification_required") is True else 0.0,
            history_depth=_history_depth(state.get("event_index"), 7),
            residue_load=1.0 if state.get("reobservation_required") is True else 0.0,
            predictive_uncertainty=1.0,
        ),
        owner="ObserveOS",
        authority_class="non_authoritative_observation",
        lineage_digest=source_digest,
    )
    return OSAssociatedGaugeField(
        role="observe",
        source_version=str(state.get("version", "")),
        source_digest=source_digest,
        boundary_digest=_boundary_digest(state),
        field=field,
    )


def project_verify_state(
    state: Mapping[str, Any],
    *,
    chart_id: str = "verify",
) -> OSAssociatedGaugeField:
    errors = validate_verify_state(state)
    if errors:
        raise ValueError("verify_state_invalid:" + ";".join(errors))
    if state.get("current_phase") != "commit" or state.get("verification_recorded") is not True:
        raise ValueError("verify_state_not_committed")

    report = _mapping(state.get("corroboration_report"), "corroboration_report")
    support_components = [
        _unit(report.get(name), f"verify_{name}")
        for name in (
            "evidence_sufficiency",
            "assessor_independence",
            "provenance_integrity",
            "method_reproducibility",
            "criterion_coverage",
        )
    ]
    support = _mean(support_components)
    criterion_coverage = _unit(report.get("criterion_coverage"), "verify_criterion_coverage")
    unresolved = 1.0 if report.get("unresolved_conflict") is True else 0.0
    route = str(state.get("route", ""))
    route_uncertainty = {
        "VERIFICATION_PASSED": 0.0,
        "VERIFICATION_FAILED": 0.5,
        "VERIFICATION_INDETERMINATE": 1.0,
    }.get(route)
    if route_uncertainty is None:
        raise ValueError("verify_route_not_committed")
    contradiction = max(unresolved, 1.0 if route == "VERIFICATION_FAILED" else 0.0)
    uncertainty = max(1.0 - support, route_uncertainty, unresolved)
    source_digest = str(state.get("verify_state_digest", ""))

    field = AssociatedField(
        field_id=f"verify:{state['verify_id']}",
        chart_id=chart_id,
        values=os_field_values(
            evidence_support=support,
            uncertainty=uncertainty,
            contradiction=contradiction,
            criterion_coverage=criterion_coverage,
            verification_debt=1.0 if state.get("verification_required") is True else 0.0,
            history_depth=_history_depth(state.get("event_index"), 6),
            residue_load=(
                1.0
                if state.get("reobservation_required") is True
                or state.get("corrective_action_required") is True
                else 0.0
            ),
            predictive_uncertainty=uncertainty,
        ),
        owner="VerifyOS",
        authority_class="evidence_bound_verification_not_truth",
        lineage_digest=source_digest,
    )
    return OSAssociatedGaugeField(
        role="verify",
        source_version=str(state.get("version", "")),
        source_digest=source_digest,
        boundary_digest=_boundary_digest(state),
        field=field,
    )


def project_memory_capsule(
    capsule: Mapping[str, Any],
    *,
    chart_id: str = "memory",
) -> OSAssociatedGaugeField:
    errors = validate_predictive_shielded_memory_capsule(capsule)
    if errors:
        raise ValueError("memory_capsule_invalid:" + ";".join(errors))

    records = _sequence(capsule.get("memory_records"), "memory_records")
    confidence = [float(_mapping(record, "memory_record")["confidence_milli"]) / 1000.0 for record in records]
    uncertainty_values = [float(_mapping(record, "memory_record")["uncertainty_milli"]) / 1000.0 for record in records]
    residues = _sequence(capsule.get("contradiction_residue"), "contradiction_residue")
    predictive = _mapping(capsule.get("predictive_state_candidate"), "predictive_state_candidate")
    predictive_uncertainty = _unit(
        float(predictive.get("uncertainty_milli")) / 1000.0,
        "memory_predictive_uncertainty",
    )
    denominator = max(1, len(records))
    residue_load = min(1.0, float(len(residues)) / float(denominator))
    route = str(capsule.get("capsule_route", ""))
    verification_debt = 0.0 if route == "READY_FOR_SHIELDED_RETRIEVAL" else 1.0
    source_digest = str(capsule.get("memory_capsule_digest", ""))

    field = AssociatedField(
        field_id=f"memory:{capsule['mission_id']}:{capsule['lineage_id']}",
        chart_id=chart_id,
        values=os_field_values(
            evidence_support=_mean(confidence),
            uncertainty=_mean(uncertainty_values),
            contradiction=residue_load,
            criterion_coverage=0.0,
            verification_debt=verification_debt,
            history_depth=min(1.0, float(int(capsule.get("sequence_index", 0)) + 1) / 16.0),
            residue_load=residue_load,
            predictive_uncertainty=predictive_uncertainty,
        ),
        owner="MemoryOS",
        authority_class="shielded_read_only_memory_candidate",
        lineage_digest=source_digest,
    )
    return OSAssociatedGaugeField(
        role="memory",
        source_version=str(capsule.get("version", "")),
        source_digest=source_digest,
        boundary_digest=_boundary_digest(capsule),
        field=field,
    )


def project_bound_os_triplet(
    *,
    observe_state: Mapping[str, Any],
    verify_state: Mapping[str, Any],
    memory_capsule: Mapping[str, Any],
) -> dict[str, OSAssociatedGaugeField]:
    observe = project_observe_state(observe_state)
    verify = project_verify_state(verify_state)
    memory = project_memory_capsule(memory_capsule)

    if verify_state.get("source_observe_state_digest") != observe.source_digest:
        raise ValueError("verify_observe_source_binding_mismatch")
    if observe_state.get("lineage_id") != verify_state.get("lineage_id"):
        raise ValueError("observe_verify_lineage_mismatch")
    if verify_state.get("lineage_id") != memory_capsule.get("lineage_id"):
        raise ValueError("verify_memory_lineage_mismatch")

    verify_digest = verify.source_digest
    memory_sources = {
        str(source_digest)
        for record in _sequence(memory_capsule.get("memory_records"), "memory_records")
        for source_digest in _sequence(
            _mapping(record, "memory_record").get("source_digests"),
            "memory_record_source_digests",
        )
    }
    if verify_digest not in memory_sources:
        raise ValueError("memory_verify_source_binding_missing")

    return {"observe": observe, "verify": verify, "memory": memory}
