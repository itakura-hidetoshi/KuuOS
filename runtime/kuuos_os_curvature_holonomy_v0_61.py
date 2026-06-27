#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any, Mapping, Sequence

from runtime.kuuos_discrete_gauge_connection_v0_60 import KuuConnection
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)
from runtime.kuuos_os_gauge_field_types_v0_61 import (
    ChannelPreservingGaugeGroup,
    OSAssociatedGaugeField,
    OS_ROLES,
    VERSION,
)


def _channel_energy(
    connection: KuuConnection,
    source: OSAssociatedGaugeField,
    target: OSAssociatedGaugeField,
    indices: Sequence[int],
) -> float:
    transported = connection.transport(source.chart_id, target.chart_id, source.values)
    return sum((transported[index] - target.values[index]) ** 2 for index in indices)


@dataclass(frozen=True)
class CurvatureChannelReceipt:
    version: str
    epistemic_curvature: float
    verification_curvature: float
    memory_return_curvature: float
    total_curvature: float
    observe_source_digest: str
    verify_source_digest: str
    memory_source_digest: str
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MemoryHolonomyReceipt:
    version: str
    path: tuple[str, ...]
    wilson_observable: float
    holonomy_defect: float
    memory_channel_return_energy: float
    observe_source_digest: str
    memory_source_digest: str
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["path"] = list(self.path)
        return payload


@dataclass(frozen=True)
class OSGaugeBundle:
    group: ChannelPreservingGaugeGroup
    connection: KuuConnection
    fields: Mapping[str, OSAssociatedGaugeField]

    def __post_init__(self) -> None:
        if self.connection.group != self.group:
            raise ValueError("os_gauge_bundle_group_mismatch")
        if set(self.fields) != set(OS_ROLES):
            raise ValueError("os_gauge_bundle_roles_incomplete")
        chart_ids: set[str] = set()
        normalized: dict[str, OSAssociatedGaugeField] = {}
        for role in OS_ROLES:
            field = self.fields[role]
            if field.role != role:
                raise ValueError("os_gauge_bundle_role_key_mismatch")
            if len(field.values) != self.group.dimension:
                raise ValueError("os_gauge_bundle_dimension_mismatch")
            if field.chart_id in chart_ids:
                raise ValueError("os_gauge_bundle_chart_duplicate")
            chart_ids.add(field.chart_id)
            normalized[role] = field
        object.__setattr__(self, "fields", normalized)

    def gauge_transform(
        self,
        local_gauges: Mapping[str, SignedPermutation],
    ) -> "OSGaugeBundle":
        identity = self.group.identity()
        transformed_fields: dict[str, OSAssociatedGaugeField] = {}
        for role, field in self.fields.items():
            element = self.group.require_admissible(
                local_gauges.get(field.chart_id, identity)
            )
            transformed_fields[role] = field.gauge_transform(element)
        return OSGaugeBundle(
            self.group,
            self.connection.gauge_transform(local_gauges),
            transformed_fields,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": VERSION,
            "group": self.group.to_dict(),
            "connection": self.connection.to_dict(),
            "fields": {
                role: field.to_dict()
                for role, field in sorted(self.fields.items())
            },
        }


def decompose_os_curvature(bundle: OSGaugeBundle) -> CurvatureChannelReceipt:
    layout = bundle.group.layout
    observe = bundle.fields["observe"]
    verify = bundle.fields["verify"]
    memory = bundle.fields["memory"]

    epistemic = _channel_energy(
        bundle.connection,
        observe,
        verify,
        layout.epistemic,
    )
    verification = _channel_energy(
        bundle.connection,
        verify,
        memory,
        layout.verification,
    )
    memory_return = _channel_energy(
        bundle.connection,
        memory,
        observe,
        layout.memory,
    )
    payload = {
        "version": VERSION,
        "epistemic_curvature": round(epistemic, 12),
        "verification_curvature": round(verification, 12),
        "memory_return_curvature": round(memory_return, 12),
        "total_curvature": round(epistemic + verification + memory_return, 12),
        "observe_source_digest": observe.source_digest,
        "verify_source_digest": verify.source_digest,
        "memory_source_digest": memory.source_digest,
    }
    return CurvatureChannelReceipt(
        **payload,
        receipt_digest=canonical_digest(payload),
    )


def memory_holonomy(bundle: OSGaugeBundle) -> MemoryHolonomyReceipt:
    observe = bundle.fields["observe"]
    verify = bundle.fields["verify"]
    memory = bundle.fields["memory"]
    path = (
        observe.chart_id,
        verify.chart_id,
        memory.chart_id,
        observe.chart_id,
    )
    holonomy = bundle.connection.path_transport(path)
    wilson = holonomy.normalized_trace()
    holonomy_defect = (1.0 - wilson) / 2.0
    returned = holonomy.apply(observe.values)
    return_energy = sum(
        (returned[index] - observe.values[index]) ** 2
        for index in bundle.group.layout.memory
    )
    payload = {
        "version": VERSION,
        "path": list(path),
        "wilson_observable": round(wilson, 12),
        "holonomy_defect": round(holonomy_defect, 12),
        "memory_channel_return_energy": round(return_energy, 12),
        "observe_source_digest": observe.source_digest,
        "memory_source_digest": memory.source_digest,
    }
    return MemoryHolonomyReceipt(
        version=VERSION,
        path=path,
        wilson_observable=payload["wilson_observable"],
        holonomy_defect=payload["holonomy_defect"],
        memory_channel_return_energy=payload["memory_channel_return_energy"],
        observe_source_digest=observe.source_digest,
        memory_source_digest=memory.source_digest,
        receipt_digest=canonical_digest(payload),
    )


def os_gauge_invariance_residual(
    bundle: OSGaugeBundle,
    local_gauges: Mapping[str, SignedPermutation],
) -> float:
    transformed = bundle.gauge_transform(local_gauges)
    before_curvature = decompose_os_curvature(bundle)
    after_curvature = decompose_os_curvature(transformed)
    before_holonomy = memory_holonomy(bundle)
    after_holonomy = memory_holonomy(transformed)
    pairs = (
        (before_curvature.epistemic_curvature, after_curvature.epistemic_curvature),
        (before_curvature.verification_curvature, after_curvature.verification_curvature),
        (before_curvature.memory_return_curvature, after_curvature.memory_return_curvature),
        (before_curvature.total_curvature, after_curvature.total_curvature),
        (before_holonomy.wilson_observable, after_holonomy.wilson_observable),
        (before_holonomy.holonomy_defect, after_holonomy.holonomy_defect),
        (
            before_holonomy.memory_channel_return_energy,
            after_holonomy.memory_channel_return_energy,
        ),
    )
    residual = max(abs(float(left) - float(right)) for left, right in pairs)
    if not math.isfinite(residual):
        raise ValueError("os_gauge_invariance_residual_nonfinite")
    return residual
