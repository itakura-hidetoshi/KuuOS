#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)
from runtime.kuuos_leibniz_module_connection_v0_71 import (
    FreeLeftModuleSection,
    LeibnizModuleConnection,
    rect_add,
    rect_close,
    rect_norm_sq,
    rect_sub,
    section_gauge_transform,
    section_left_action,
)
from runtime.kuuos_memory_history_v0_72 import (
    MemoryHistoryFrame,
    ReadOnlyMemoryHistory,
)
from runtime.kuuos_module_connection_v0_70 import Matrix, conjugate
from runtime.kuuos_noncommutative_differential_calculus_v0_71 import (
    InnerDifferentialCalculus,
)
from runtime.kuuos_nonmarkov_memory_kernel_v0_72 import (
    FiniteMemoryKernel,
    MemoryKernelTerm,
    kernel_issues,
    memory_contribution,
    memory_contribution_from_frames,
)
from runtime.kuuos_state_module_v0_70 import KuuStateModule

VERSION = "kuuos_nonmarkov_memory_connection_v0_72"
TOLERANCE = 1.0e-10


@dataclass(frozen=True)
class NonMarkovMemoryConnection:
    base_connection: LeibnizModuleConnection
    memory_kernel: FiniteMemoryKernel
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["base_connection"] = self.base_connection.to_dict()
        payload["memory_kernel"] = self.memory_kernel.to_dict()
        return payload

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())

    def require_compatible(
        self,
        calculus: InnerDifferentialCalculus,
        module: KuuStateModule,
        history: ReadOnlyMemoryHistory,
    ) -> None:
        self.base_connection.require_compatible(calculus, module)
        issues = kernel_issues(module, history, self.memory_kernel)
        if issues:
            raise ValueError(issues[0])
        if self.memory_kernel.direction_labels != calculus.direction_labels:
            raise ValueError("memory_connection_direction_basis_mismatch")

    def apply(
        self,
        calculus: InnerDifferentialCalculus,
        direction_index: int,
        current: FreeLeftModuleSection,
        history: ReadOnlyMemoryHistory,
        current_epoch: int,
    ) -> FreeLeftModuleSection:
        self.require_compatible(calculus, _module_stub(self), history)
        direction_label = calculus.direction_labels[direction_index]
        base_value = self.base_connection.apply(calculus, direction_index, current)
        memory_value = memory_contribution(
            self.memory_kernel,
            history,
            direction_label,
            current_epoch,
        )
        return FreeLeftModuleSection(
            rect_add(base_value.values, memory_value.values),
            current.context_dimension,
            current.module_rank,
        )

    def gauge_transform(self, gauge: SignedPermutation) -> "NonMarkovMemoryConnection":
        terms = tuple(
            MemoryKernelTerm(
                term.direction_label,
                term.lag,
                conjugate(term.operator, gauge),
            )
            for term in self.memory_kernel.terms
        )
        kernel = FiniteMemoryKernel(
            self.memory_kernel.source_module_digest,
            self.memory_kernel.source_history_digest,
            self.memory_kernel.direction_labels,
            self.memory_kernel.module_rank,
            terms,
            candidate_only=self.memory_kernel.candidate_only,
        )
        return NonMarkovMemoryConnection(
            self.base_connection.gauge_transform(gauge),
            kernel,
        )


def _module_stub(connection: NonMarkovMemoryConnection) -> KuuStateModule:
    raise RuntimeError("module_argument_required")


def apply_with_frames(
    connection: NonMarkovMemoryConnection,
    calculus: InnerDifferentialCalculus,
    direction_index: int,
    current: FreeLeftModuleSection,
    frames: tuple[MemoryHistoryFrame, ...],
    current_epoch: int,
) -> FreeLeftModuleSection:
    direction_label = calculus.direction_labels[direction_index]
    base_value = connection.base_connection.apply(calculus, direction_index, current)
    memory_value = memory_contribution_from_frames(
        connection.memory_kernel,
        frames,
        direction_label,
        current_epoch,
    )
    return FreeLeftModuleSection(
        rect_add(base_value.values, memory_value.values),
        current.context_dimension,
        current.module_rank,
    )


def apply_nonmarkov_connection(
    connection: NonMarkovMemoryConnection,
    calculus: InnerDifferentialCalculus,
    module: KuuStateModule,
    direction_index: int,
    current: FreeLeftModuleSection,
    history: ReadOnlyMemoryHistory,
    current_epoch: int,
) -> FreeLeftModuleSection:
    connection.require_compatible(calculus, module, history)
    return apply_with_frames(
        connection,
        calculus,
        direction_index,
        current,
        history.frames,
        current_epoch,
    )


def pathwise_leibniz_residual(
    connection: NonMarkovMemoryConnection,
    calculus: InnerDifferentialCalculus,
    module: KuuStateModule,
    direction_index: int,
    algebra_element: Matrix,
    current: FreeLeftModuleSection,
    history: ReadOnlyMemoryHistory,
    current_epoch: int,
):
    acted_current = section_left_action(algebra_element, current)
    left = apply_with_frames(
        connection,
        calculus,
        direction_index,
        acted_current,
        history.acted_sections(algebra_element),
        current_epoch,
    )
    derivative_term = section_left_action(
        calculus.derivative(direction_index, algebra_element),
        current,
    )
    transported = section_left_action(
        algebra_element,
        apply_nonmarkov_connection(
            connection,
            calculus,
            module,
            direction_index,
            current,
            history,
            current_epoch,
        ),
    )
    return rect_sub(left.values, rect_add(derivative_term.values, transported.values))


def satisfies_pathwise_leibniz(
    connection: NonMarkovMemoryConnection,
    calculus: InnerDifferentialCalculus,
    module: KuuStateModule,
    direction_index: int,
    algebra_element: Matrix,
    current: FreeLeftModuleSection,
    history: ReadOnlyMemoryHistory,
    current_epoch: int,
) -> bool:
    return rect_norm_sq(pathwise_leibniz_residual(
        connection,
        calculus,
        module,
        direction_index,
        algebra_element,
        current,
        history,
        current_epoch,
    )) <= TOLERANCE


def history_frames_gauge_transform(
    frames: tuple[MemoryHistoryFrame, ...],
    gauge: SignedPermutation,
) -> tuple[MemoryHistoryFrame, ...]:
    return tuple(
        MemoryHistoryFrame(
            frame.epoch,
            section_gauge_transform(frame.section, gauge),
            frame.source_capsule_digest,
        )
        for frame in frames
    )


def nonmarkov_gauge_covariant_on(
    connection: NonMarkovMemoryConnection,
    calculus: InnerDifferentialCalculus,
    direction_index: int,
    current: FreeLeftModuleSection,
    history: ReadOnlyMemoryHistory,
    current_epoch: int,
    gauge: SignedPermutation,
) -> bool:
    transformed_connection = connection.gauge_transform(gauge)
    transformed_current = section_gauge_transform(current, gauge)
    transformed_frames = history_frames_gauge_transform(history.frames, gauge)
    left = apply_with_frames(
        transformed_connection,
        calculus,
        direction_index,
        transformed_current,
        transformed_frames,
        current_epoch,
    )
    right = section_gauge_transform(
        apply_with_frames(
            connection,
            calculus,
            direction_index,
            current,
            history.frames,
            current_epoch,
        ),
        gauge,
    )
    return rect_close(left.values, right.values)
