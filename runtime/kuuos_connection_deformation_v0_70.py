#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_module_connection_v0_70 import (
    EndomorphismValuedOneForm,
    Matrix,
    ModuleConnection,
)
from runtime.kuuos_state_module_v0_70 import KuuStateModule

VERSION = "kuuos_connection_deformation_v0_70"
TOLERANCE = 1.0e-12


def _near_zero(value: float) -> bool:
    return abs(float(value)) <= TOLERANCE


def commutes_with_projector(value: Matrix, coordinates: Iterable[int]) -> bool:
    selected = set(coordinates)
    rank = len(value)
    return all(
        _near_zero(value[row][column])
        for row in range(rank)
        for column in range(rank)
        if (row in selected) != (column in selected)
    )


def vanishes_on_submodule(value: Matrix, coordinates: Iterable[int]) -> bool:
    selected = set(coordinates)
    rank = len(value)
    return all(
        _near_zero(value[row][column])
        for column in selected
        for row in range(rank)
    )


def preserves_submodule(value: Matrix, coordinates: Iterable[int]) -> bool:
    selected = set(coordinates)
    rank = len(value)
    return all(
        _near_zero(value[row][column])
        for column in selected
        for row in range(rank)
        if row not in selected
    )


@dataclass(frozen=True)
class ConnectionDeformation:
    alpha: EndomorphismValuedOneForm
    source_connection_digest: str
    candidate_only: bool = True
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.source_connection_digest:
            raise ValueError("deformation_source_connection_digest_missing")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["alpha"] = self.alpha.to_dict()
        return payload

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())

    def candidate_connection(self, source: ModuleConnection) -> ModuleConnection:
        if source.digest != self.source_connection_digest:
            raise ValueError("deformation_source_connection_mismatch")
        source.connection_form.require_same_space(self.alpha)
        return ModuleConnection(
            source.connection_form.add(self.alpha),
            source.source_module_digest,
            source.gauge_group_digest,
        )


def deformation_issues(
    module: KuuStateModule,
    source: ModuleConnection,
    deformation: ConnectionDeformation,
) -> tuple[str, ...]:
    issues: list[str] = []
    if source.source_module_digest != module.digest:
        issues.append("connection_module_binding_mismatch")
    if source.digest != deformation.source_connection_digest:
        issues.append("deformation_source_connection_mismatch")
    if not deformation.candidate_only:
        issues.append("deformation_not_candidate_only")
    try:
        source.connection_form.require_same_space(deformation.alpha)
    except ValueError as error:
        issues.append(str(error))
        return tuple(dict.fromkeys(issues))

    projectors = module.all_projectors()
    for component in deformation.alpha.components:
        if any(
            not commutes_with_projector(component, projector.coordinates)
            for projector in projectors
        ):
            issues.append("deformation_semantic_projector_noncommuting")
        if not vanishes_on_submodule(component, module.protected_projector.coordinates):
            issues.append("deformation_protected_part_nonzero")
        if any(
            not preserves_submodule(component, level.coordinates)
            for level in module.authority_filtration
        ):
            issues.append("deformation_authority_filtration_not_preserved")
    return tuple(dict.fromkeys(issues))
