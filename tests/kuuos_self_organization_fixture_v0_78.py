from __future__ import annotations

from runtime.kuuos_self_organization_types_v0_78 import (
    ObservationContext,
    SelfOrganizationPolicy,
    StructureState,
)


def make_context(
    context_id: str,
    authority: float,
    audit: float,
    coupling: float,
    memory: float,
) -> ObservationContext:
    return ObservationContext(
        context_id,
        (
            ("audit", audit),
            ("authority", authority),
            ("coupling", coupling),
            ("memory", memory),
        ),
        (
            ("audit", 1.0),
            ("authority", 1.0),
            ("coupling", 1.0),
            ("memory", 1.0),
        ),
    )


def make_source() -> StructureState:
    return StructureState(
        0,
        (
            ("audit", 1.0),
            ("authority", 1.0),
            ("coupling", 0.0),
            ("memory", 0.0),
        ),
        ("audit", "authority"),
    )


def make_policy() -> SelfOrganizationPolicy:
    return SelfOrganizationPolicy(
        max_candidates=16,
        max_changed_coordinates=2,
        step_fractions=(0.25, 0.5, 1.0),
    )
