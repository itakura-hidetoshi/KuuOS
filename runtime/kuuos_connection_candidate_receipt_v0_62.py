#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any

from runtime.kuuos_discrete_gauge_connection_v0_60 import ChartPair, KuuConnection
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_os_curvature_holonomy_v0_61 import (
    CurvatureChannelReceipt,
    MemoryHolonomyReceipt,
    OSGaugeBundle,
    decompose_os_curvature,
    memory_holonomy,
)

VERSION = "kuuos_connection_improvement_candidate_v0_62"


@dataclass(frozen=True)
class ConnectionCandidatePolicy:
    max_changed_links: int = 2
    require_strict_curvature_decrease: bool = True
    preserve_memory_holonomy_observables: bool = True
    tolerance: float = 1e-12
    max_catalog_product: int = 4096

    def __post_init__(self) -> None:
        if self.max_changed_links < 0:
            raise ValueError("max_changed_links_negative")
        if self.tolerance < 0.0 or not math.isfinite(self.tolerance):
            raise ValueError("connection_policy_tolerance_invalid")
        if self.max_catalog_product < 1:
            raise ValueError("max_catalog_product_positive_required")


@dataclass(frozen=True)
class ConnectionCandidateReceipt:
    source_bundle_digest: str
    source_connection_digest: str
    candidate_connection_digest: str
    rollback_digest: str
    changed_links: tuple[ChartPair, ...]
    source_curvature: CurvatureChannelReceipt
    candidate_curvature: CurvatureChannelReceipt
    source_memory_holonomy: MemoryHolonomyReceipt
    candidate_memory_holonomy: MemoryHolonomyReceipt
    connection_domain_preserved: bool
    group_preserved: bool
    fields_preserved: bool
    source_bindings_preserved: bool
    protected_holonomy_observables_preserved: bool
    curvature_nonincreasing: bool
    curvature_strictly_decreased: bool
    change_budget_respected: bool
    candidate_only: bool
    state_write_performed: bool
    admissible: bool
    blockers: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["changed_links"] = [list(pair) for pair in self.changed_links]
        payload["source_curvature"] = self.source_curvature.to_dict()
        payload["candidate_curvature"] = self.candidate_curvature.to_dict()
        payload["source_memory_holonomy"] = self.source_memory_holonomy.to_dict()
        payload["candidate_memory_holonomy"] = self.candidate_memory_holonomy.to_dict()
        payload["blockers"] = list(self.blockers)
        return payload


def _domain(connection: KuuConnection) -> tuple[ChartPair, ...]:
    return tuple(sorted(connection.transports))


def _field_signature(bundle: OSGaugeBundle) -> dict[str, Any]:
    return {
        role: field.to_dict()
        for role, field in sorted(bundle.fields.items())
    }


def _source_signature(bundle: OSGaugeBundle) -> dict[str, str]:
    return {
        role: field.source_digest
        for role, field in sorted(bundle.fields.items())
    }


def _close(left: float, right: float, tolerance: float) -> bool:
    return abs(float(left) - float(right)) <= tolerance


def _holonomy_observables_equal(
    left: MemoryHolonomyReceipt,
    right: MemoryHolonomyReceipt,
    tolerance: float,
) -> bool:
    return (
        left.path == right.path
        and _close(left.wilson_observable, right.wilson_observable, tolerance)
        and _close(left.holonomy_defect, right.holonomy_defect, tolerance)
        and _close(
            left.memory_channel_return_energy,
            right.memory_channel_return_energy,
            tolerance,
        )
    )


def evaluate_connection_candidate(
    source_bundle: OSGaugeBundle,
    candidate_connection: KuuConnection,
    *,
    policy: ConnectionCandidatePolicy = ConnectionCandidatePolicy(),
) -> ConnectionCandidateReceipt:
    source_digest = canonical_digest(source_bundle.to_dict())
    source_connection = source_bundle.connection
    source_domain = _domain(source_connection)
    domain_preserved = _domain(candidate_connection) == source_domain
    group_preserved = candidate_connection.group == source_bundle.group
    blockers: list[str] = []

    if not group_preserved:
        blockers.append("connection_group_changed")
    if not domain_preserved:
        blockers.append("connection_domain_changed")

    source_curvature = decompose_os_curvature(source_bundle)
    source_memory = memory_holonomy(source_bundle)
    if group_preserved and domain_preserved:
        candidate_bundle = OSGaugeBundle(
            source_bundle.group,
            candidate_connection,
            source_bundle.fields,
        )
        fields_preserved = _field_signature(candidate_bundle) == _field_signature(source_bundle)
        sources_preserved = _source_signature(candidate_bundle) == _source_signature(source_bundle)
        candidate_curvature = decompose_os_curvature(candidate_bundle)
        candidate_memory = memory_holonomy(candidate_bundle)
    else:
        fields_preserved = False
        sources_preserved = False
        candidate_curvature = source_curvature
        candidate_memory = source_memory

    if not fields_preserved:
        blockers.append("os_fields_changed")
    if not sources_preserved:
        blockers.append("source_bindings_changed")

    changed_links = tuple(
        pair for pair in source_domain
        if candidate_connection.transports.get(pair) != source_connection.transports.get(pair)
    ) if domain_preserved else ()
    budget_ok = len(changed_links) <= policy.max_changed_links
    if not budget_ok:
        blockers.append("connection_change_budget_exceeded")

    holonomy_ok = _holonomy_observables_equal(
        source_memory,
        candidate_memory,
        policy.tolerance,
    )
    if policy.preserve_memory_holonomy_observables and not holonomy_ok:
        blockers.append("protected_memory_holonomy_changed")

    source_total = source_curvature.total_curvature
    candidate_total = candidate_curvature.total_curvature
    nonincreasing = candidate_total <= source_total + policy.tolerance
    strict = candidate_total < source_total - policy.tolerance
    if not nonincreasing:
        blockers.append("os_curvature_increased")
    if policy.require_strict_curvature_decrease and not strict:
        blockers.append("strict_curvature_decrease_missing")

    source_connection_digest = canonical_digest(source_connection.to_dict())
    candidate_connection_digest = canonical_digest(candidate_connection.to_dict())
    payload = {
        "version": VERSION,
        "source_bundle_digest": source_digest,
        "source_connection_digest": source_connection_digest,
        "candidate_connection_digest": candidate_connection_digest,
        "rollback_digest": source_digest,
        "changed_links": [list(pair) for pair in changed_links],
        "source_curvature": source_curvature.to_dict(),
        "candidate_curvature": candidate_curvature.to_dict(),
        "source_memory_holonomy": source_memory.to_dict(),
        "candidate_memory_holonomy": candidate_memory.to_dict(),
        "connection_domain_preserved": domain_preserved,
        "group_preserved": group_preserved,
        "fields_preserved": fields_preserved,
        "source_bindings_preserved": sources_preserved,
        "protected_holonomy_observables_preserved": holonomy_ok,
        "curvature_nonincreasing": nonincreasing,
        "curvature_strictly_decreased": strict,
        "change_budget_respected": budget_ok,
        "candidate_only": True,
        "state_write_performed": False,
        "admissible": not blockers,
        "blockers": blockers,
    }
    return ConnectionCandidateReceipt(
        source_bundle_digest=source_digest,
        source_connection_digest=source_connection_digest,
        candidate_connection_digest=candidate_connection_digest,
        rollback_digest=source_digest,
        changed_links=changed_links,
        source_curvature=source_curvature,
        candidate_curvature=candidate_curvature,
        source_memory_holonomy=source_memory,
        candidate_memory_holonomy=candidate_memory,
        connection_domain_preserved=domain_preserved,
        group_preserved=group_preserved,
        fields_preserved=fields_preserved,
        source_bindings_preserved=sources_preserved,
        protected_holonomy_observables_preserved=holonomy_ok,
        curvature_nonincreasing=nonincreasing,
        curvature_strictly_decreased=strict,
        change_budget_respected=budget_ok,
        candidate_only=True,
        state_write_performed=False,
        admissible=not blockers,
        blockers=tuple(blockers),
        receipt_digest=canonical_digest(payload),
    )
