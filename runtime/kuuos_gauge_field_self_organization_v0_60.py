#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any, Mapping

from runtime.kuuos_discrete_gauge_connection_v0_60 import GaugeAction, KuuConnection, Plaquette, gauge_action
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import VERSION, AssociatedField, ConstitutionalGaugeGroup, SignedPermutation, canonical_digest


@dataclass(frozen=True)
class GaugeConfiguration:
    group: ConstitutionalGaugeGroup
    connection: KuuConnection
    fields: Mapping[str, AssociatedField]
    plaquettes: tuple[Plaquette, ...] = ()

    def __post_init__(self) -> None:
        if self.connection.group != self.group:
            raise ValueError("connection_group_mismatch")
        normalized: dict[str, AssociatedField] = {}
        for chart_id, field in self.fields.items():
            if chart_id != field.chart_id:
                raise ValueError("field_chart_key_mismatch")
            if field.dimension != self.group.dimension:
                raise ValueError("field_group_dimension_mismatch")
            normalized[str(chart_id)] = field
        if not normalized:
            raise ValueError("configuration_fields_missing")
        object.__setattr__(self, "fields", normalized)

    def action(self) -> GaugeAction:
        return gauge_action(self.connection, self.fields, self.plaquettes)

    def gauge_transform(self, local_gauges: Mapping[str, SignedPermutation]) -> "GaugeConfiguration":
        identity = self.group.identity()
        fields = {
            chart_id: field.gauge_transform(self.group.require_admissible(local_gauges.get(chart_id, identity)))
            for chart_id, field in self.fields.items()
        }
        return GaugeConfiguration(self.group, self.connection.gauge_transform(local_gauges), fields, self.plaquettes)

    def protected_state(self) -> dict[str, tuple[float, ...]]:
        return {
            chart_id: self.group.protected_projection(field.values)
            for chart_id, field in sorted(self.fields.items())
        }

    def gauge_invariant_observables(self) -> dict[str, Any]:
        return {
            "field_norms": {
                chart_id: round(field.norm_sq(), 12)
                for chart_id, field in sorted(self.fields.items())
            },
            "wilson_observables": [
                round(self.connection.wilson_observable(plaquette), 12)
                for plaquette in self.plaquettes
            ],
            "action": self.action().to_dict(),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": VERSION,
            "group": self.group.to_dict(),
            "connection": self.connection.to_dict(),
            "fields": {
                chart_id: field.to_dict()
                for chart_id, field in sorted(self.fields.items())
            },
            "plaquettes": [list(plaquette) for plaquette in self.plaquettes],
        }


@dataclass(frozen=True)
class SelfOrganizationReceipt:
    version: str
    status: str
    source_digest: str
    candidate_digest: str
    source_action: GaugeAction
    candidate_action: GaugeAction
    protected_state_preserved: bool
    ownership_preserved: bool
    authority_preserved: bool
    action_nonincreasing: bool
    rollback_bound: bool
    rollback_digest: str
    blockers: tuple[str, ...]

    @property
    def admissible(self) -> bool:
        return self.status == "KUUOS_GAUGE_SELF_ORGANIZATION_CANDIDATE_ADMISSIBLE"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["source_action"] = self.source_action.to_dict()
        payload["candidate_action"] = self.candidate_action.to_dict()
        payload["blockers"] = list(self.blockers)
        payload["admissible"] = self.admissible
        return payload


def build_covariant_relaxation_candidate(configuration: GaugeConfiguration, *, rate: float = 0.25) -> GaugeConfiguration:
    if not 0.0 <= rate <= 1.0:
        raise ValueError("relaxation_rate_out_of_range")
    incoming = {chart: [field.values] for chart, field in configuration.fields.items()}
    for source, target in configuration.connection.oriented_pairs():
        if source not in configuration.fields or target not in configuration.fields:
            continue
        incoming[target].append(configuration.connection.transport(source, target, configuration.fields[source].values))
        incoming[source].append(configuration.connection.transport(target, source, configuration.fields[target].values))

    protected = set(configuration.group.protected_coordinates)
    fields: dict[str, AssociatedField] = {}
    source_digest = canonical_digest(configuration.to_dict())
    for chart_id, field in configuration.fields.items():
        samples = incoming[chart_id]
        means = tuple(
            sum(sample[index] for sample in samples) / len(samples)
            for index in range(configuration.group.dimension)
        )
        values = tuple(
            field.values[index]
            if index in protected
            else (1.0 - rate) * field.values[index] + rate * means[index]
            for index in range(configuration.group.dimension)
        )
        fields[chart_id] = field.with_values(
            values,
            lineage={"kind": "covariant_relaxation", "source": source_digest, "rate": rate, "chart": chart_id},
        )
    return GaugeConfiguration(configuration.group, configuration.connection, fields, configuration.plaquettes)


def evaluate_self_organization_candidate(
    source: GaugeConfiguration,
    candidate: GaugeConfiguration,
    *,
    rollback_digest: str | None = None,
    tolerance: float = 1e-10,
) -> SelfOrganizationReceipt:
    blockers: list[str] = []
    source_digest = canonical_digest(source.to_dict())
    candidate_digest = canonical_digest(candidate.to_dict())
    if source.group != candidate.group:
        blockers.append("constitutional_gauge_group_changed")
    if set(source.fields) != set(candidate.fields):
        blockers.append("chart_domain_changed")
    protected = source.protected_state() == candidate.protected_state()
    if not protected:
        blockers.append("protected_state_changed")
    common = set(source.fields) & set(candidate.fields)
    ownership = all(source.fields[x].owner == candidate.fields[x].owner for x in common)
    authority = all(source.fields[x].authority_class == candidate.fields[x].authority_class for x in common)
    if not ownership:
        blockers.append("field_ownership_changed")
    if not authority:
        blockers.append("field_authority_changed")
    source_action = source.action()
    candidate_action = candidate.action()
    nonincreasing = candidate_action.total <= source_action.total + abs(tolerance)
    if not nonincreasing:
        blockers.append("gauge_action_increased")
    effective_rollback_digest = str(rollback_digest or source_digest)
    rollback_bound = bool(effective_rollback_digest)
    if not rollback_bound:
        blockers.append("rollback_digest_missing")
    status = "KUUOS_GAUGE_SELF_ORGANIZATION_CANDIDATE_ADMISSIBLE" if not blockers else "KUUOS_GAUGE_SELF_ORGANIZATION_CANDIDATE_BLOCKED"
    return SelfOrganizationReceipt(
        VERSION,
        status,
        source_digest,
        candidate_digest,
        source_action,
        candidate_action,
        protected,
        ownership,
        authority,
        nonincreasing,
        rollback_bound,
        effective_rollback_digest,
        tuple(blockers),
    )


def gauge_covariance_residual(configuration: GaugeConfiguration, local_gauges: Mapping[str, SignedPermutation]) -> float:
    before = configuration.gauge_invariant_observables()
    after = configuration.gauge_transform(local_gauges).gauge_invariant_observables()
    residual = abs(float(before["action"]["total"]) - float(after["action"]["total"]))
    for chart_id, value in before["field_norms"].items():
        residual = max(residual, abs(float(value) - float(after["field_norms"][chart_id])))
    for left, right in zip(before["wilson_observables"], after["wilson_observables"], strict=True):
        residual = max(residual, abs(float(left) - float(right)))
    if not math.isfinite(residual):
        raise ValueError("gauge_covariance_residual_nonfinite")
    return residual
