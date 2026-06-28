#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_connection_deformation_v0_70 import (
    commutes_with_projector,
    preserves_submodule,
    vanishes_on_submodule,
)
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_leibniz_module_connection_v0_71 import (
    FreeLeftModuleSection,
    left_action,
    rect_add,
    rect_close,
    right_action,
)
from runtime.kuuos_memory_history_v0_72 import (
    MemoryHistoryFrame,
    ReadOnlyMemoryHistory,
)
from runtime.kuuos_module_connection_v0_70 import (
    Matrix,
    matrix,
    matrix_add,
    matrix_sub,
    zero_matrix,
)
from runtime.kuuos_state_module_v0_70 import KuuStateModule

VERSION = "kuuos_finite_nonmarkov_memory_kernel_v0_72"


def _matrix_is_zero(value: Matrix, tolerance: float = 1.0e-12) -> bool:
    return all(abs(entry) <= tolerance for row in value for entry in row)


def supported_on_coordinates(value: Matrix, coordinates: tuple[int, ...]) -> bool:
    selected = set(coordinates)
    rank = len(value)
    return all(
        abs(value[row][column]) <= 1.0e-12
        for row in range(rank)
        for column in range(rank)
        if row not in selected or column not in selected
    )


@dataclass(frozen=True)
class MemoryKernelTerm:
    direction_label: str
    lag: int
    operator: Matrix

    def to_dict(self) -> dict[str, Any]:
        return {
            "direction_label": self.direction_label,
            "lag": self.lag,
            "operator": [list(row) for row in self.operator],
        }


@dataclass(frozen=True)
class FiniteMemoryKernel:
    source_module_digest: str
    source_history_digest: str
    direction_labels: tuple[str, ...]
    module_rank: int
    terms: tuple[MemoryKernelTerm, ...]
    candidate_only: bool = True
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.source_module_digest:
            raise ValueError("memory_kernel_module_digest_missing")
        if not self.source_history_digest:
            raise ValueError("memory_kernel_history_digest_missing")
        if self.module_rank <= 0:
            raise ValueError("memory_kernel_module_rank_invalid")
        if not self.direction_labels:
            raise ValueError("memory_kernel_direction_basis_empty")
        if len(set(self.direction_labels)) != len(self.direction_labels):
            raise ValueError("memory_kernel_direction_basis_not_unique")
        keys: set[tuple[str, int]] = set()
        normalized: list[MemoryKernelTerm] = []
        for term in self.terms:
            if term.direction_label not in self.direction_labels:
                raise ValueError("memory_kernel_direction_unknown")
            if term.lag <= 0:
                raise ValueError("memory_kernel_lag_invalid")
            key = (term.direction_label, term.lag)
            if key in keys:
                raise ValueError("memory_kernel_term_duplicate")
            keys.add(key)
            normalized.append(MemoryKernelTerm(
                term.direction_label,
                term.lag,
                matrix(term.operator, self.module_rank),
            ))
        object.__setattr__(self, "terms", tuple(normalized))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["direction_labels"] = list(self.direction_labels)
        payload["terms"] = [term.to_dict() for term in self.terms]
        return payload

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class MemoryKernelDeformation:
    source_kernel_digest: str
    delta_terms: tuple[MemoryKernelTerm, ...]
    candidate_only: bool = True

    def __post_init__(self) -> None:
        if not self.source_kernel_digest:
            raise ValueError("memory_kernel_deformation_source_missing")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_kernel_digest": self.source_kernel_digest,
            "delta_terms": [term.to_dict() for term in self.delta_terms],
            "candidate_only": self.candidate_only,
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


def memory_projector_coordinates(module: KuuStateModule) -> tuple[int, ...]:
    for projector in module.semantic_projectors:
        if projector.label == "memory":
            return projector.coordinates
    raise ValueError("memory_projector_missing")


def kernel_issues(
    module: KuuStateModule,
    history: ReadOnlyMemoryHistory,
    kernel: FiniteMemoryKernel,
) -> tuple[str, ...]:
    issues: list[str] = []
    if kernel.source_module_digest != module.digest:
        issues.append("memory_kernel_module_binding_mismatch")
    if kernel.source_history_digest != history.digest:
        issues.append("memory_kernel_history_binding_mismatch")
    if kernel.module_rank != module.module_rank:
        issues.append("memory_kernel_module_rank_mismatch")
    if kernel.module_rank != history.module_rank:
        issues.append("memory_kernel_history_rank_mismatch")
    if not kernel.candidate_only:
        issues.append("memory_kernel_not_candidate_only")

    memory_coordinates = memory_projector_coordinates(module)
    for term in kernel.terms:
        if not supported_on_coordinates(term.operator, memory_coordinates):
            issues.append("memory_kernel_not_memory_supported")
        if any(
            not commutes_with_projector(term.operator, projector.coordinates)
            for projector in module.all_projectors()
        ):
            issues.append("memory_kernel_semantic_projector_noncommuting")
        if not vanishes_on_submodule(term.operator, module.protected_projector.coordinates):
            issues.append("memory_kernel_protected_part_nonzero")
        if any(
            not preserves_submodule(term.operator, level.coordinates)
            for level in module.authority_filtration
        ):
            issues.append("memory_kernel_authority_filtration_not_preserved")
    return tuple(dict.fromkeys(issues))


def _term_map(kernel: FiniteMemoryKernel) -> dict[tuple[str, int], Matrix]:
    return {
        (term.direction_label, term.lag): term.operator
        for term in kernel.terms
    }


def deform_memory_kernel(
    source: FiniteMemoryKernel,
    deformation: MemoryKernelDeformation,
) -> FiniteMemoryKernel:
    if deformation.source_kernel_digest != source.digest:
        raise ValueError("memory_kernel_deformation_source_mismatch")
    if not deformation.candidate_only:
        raise ValueError("memory_kernel_deformation_not_candidate_only")
    values = _term_map(source)
    for term in deformation.delta_terms:
        if term.direction_label not in source.direction_labels:
            raise ValueError("memory_kernel_deformation_direction_unknown")
        if term.lag <= 0:
            raise ValueError("memory_kernel_deformation_lag_invalid")
        normalized = matrix(term.operator, source.module_rank)
        key = (term.direction_label, term.lag)
        values[key] = matrix_add(values.get(key, zero_matrix(source.module_rank)), normalized)
    terms = tuple(
        MemoryKernelTerm(direction, lag, operator)
        for (direction, lag), operator in sorted(values.items())
        if not _matrix_is_zero(operator)
    )
    return FiniteMemoryKernel(
        source.source_module_digest,
        source.source_history_digest,
        source.direction_labels,
        source.module_rank,
        terms,
        candidate_only=True,
    )


def rollback_memory_kernel(
    source: FiniteMemoryKernel,
    candidate: FiniteMemoryKernel,
    deformation: MemoryKernelDeformation,
) -> tuple[FiniteMemoryKernel, bool]:
    if deformation.source_kernel_digest != source.digest:
        raise ValueError("memory_kernel_rollback_source_mismatch")
    values = _term_map(candidate)
    for term in deformation.delta_terms:
        normalized = matrix(term.operator, source.module_rank)
        key = (term.direction_label, term.lag)
        values[key] = matrix_sub(values.get(key, zero_matrix(source.module_rank)), normalized)
    terms = tuple(
        MemoryKernelTerm(direction, lag, operator)
        for (direction, lag), operator in sorted(values.items())
        if not _matrix_is_zero(operator)
    )
    recovered = FiniteMemoryKernel(
        source.source_module_digest,
        source.source_history_digest,
        source.direction_labels,
        source.module_rank,
        terms,
        candidate_only=source.candidate_only,
    )
    return recovered, recovered.digest == source.digest


def memory_contribution_from_frames(
    kernel: FiniteMemoryKernel,
    frames: tuple[MemoryHistoryFrame, ...],
    direction_label: str,
    current_epoch: int,
) -> FreeLeftModuleSection:
    if not frames:
        raise ValueError("memory_kernel_frames_empty")
    first = frames[0].section
    result = tuple(
        tuple(0.0 for _ in range(first.module_rank))
        for _ in range(first.context_dimension)
    )
    by_epoch = {frame.epoch: frame for frame in frames}
    for term in kernel.terms:
        if term.direction_label != direction_label:
            continue
        frame = by_epoch.get(current_epoch - term.lag)
        if frame is None:
            raise ValueError("memory_kernel_required_history_missing")
        result = rect_add(result, right_action(frame.section.values, term.operator))
    return FreeLeftModuleSection(result, first.context_dimension, first.module_rank)


def memory_contribution(
    kernel: FiniteMemoryKernel,
    history: ReadOnlyMemoryHistory,
    direction_label: str,
    current_epoch: int,
) -> FreeLeftModuleSection:
    if kernel.source_history_digest != history.digest:
        raise ValueError("memory_kernel_history_binding_mismatch")
    return memory_contribution_from_frames(
        kernel,
        history.frames,
        direction_label,
        current_epoch,
    )


def memory_kernel_left_linear_on(
    kernel: FiniteMemoryKernel,
    history: ReadOnlyMemoryHistory,
    algebra_element: Matrix,
    direction_label: str,
    current_epoch: int,
) -> bool:
    acted = memory_contribution_from_frames(
        kernel,
        history.acted_sections(algebra_element),
        direction_label,
        current_epoch,
    )
    original = memory_contribution(kernel, history, direction_label, current_epoch)
    expected = left_action(algebra_element, original.values)
    return rect_close(acted.values, expected)
