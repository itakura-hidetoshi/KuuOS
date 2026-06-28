#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)
from runtime.kuuos_leibniz_module_connection_v0_71 import (
    rect_norm_sq,
    section_gauge_transform,
)
from runtime.kuuos_memory_history_v0_72 import (
    MemoryHistoryFrame,
    ReadOnlyMemoryHistory,
)
from runtime.kuuos_module_connection_v0_70 import conjugate
from runtime.kuuos_nonmarkov_memory_kernel_v0_72 import (
    FiniteMemoryKernel,
    MemoryKernelTerm,
    memory_contribution_from_frames,
)

TOLERANCE = 1.0e-9


def memory_return_score(
    kernel: FiniteMemoryKernel,
    frames: tuple[MemoryHistoryFrame, ...],
    current_epoch: int,
) -> float:
    return sum(
        rect_norm_sq(memory_contribution_from_frames(
            kernel,
            frames,
            direction,
            current_epoch,
        ).values)
        for direction in kernel.direction_labels
    )


def transformed_kernel(
    kernel: FiniteMemoryKernel,
    gauge: SignedPermutation,
) -> FiniteMemoryKernel:
    return FiniteMemoryKernel(
        kernel.source_module_digest,
        kernel.source_history_digest,
        kernel.direction_labels,
        kernel.module_rank,
        tuple(
            MemoryKernelTerm(
                term.direction_label,
                term.lag,
                conjugate(term.operator, gauge),
            )
            for term in kernel.terms
        ),
        candidate_only=kernel.candidate_only,
    )


def transformed_frames(
    history: ReadOnlyMemoryHistory,
    gauge: SignedPermutation,
) -> tuple[MemoryHistoryFrame, ...]:
    return tuple(
        MemoryHistoryFrame(
            frame.epoch,
            section_gauge_transform(frame.section, gauge),
            frame.source_capsule_digest,
        )
        for frame in history.frames
    )


def score_is_gauge_invariant(
    kernel: FiniteMemoryKernel,
    history: ReadOnlyMemoryHistory,
    current_epoch: int,
    gauge: SignedPermutation,
    tolerance: float = TOLERANCE,
) -> bool:
    source_score = memory_return_score(kernel, history.frames, current_epoch)
    gauge_score = memory_return_score(
        transformed_kernel(kernel, gauge),
        transformed_frames(history, gauge),
        current_epoch,
    )
    return abs(source_score - gauge_score) <= tolerance


def changed_term_count(
    source: FiniteMemoryKernel,
    evaluated: FiniteMemoryKernel,
) -> int:
    def term_map(kernel: FiniteMemoryKernel) -> dict[tuple[str, int], str]:
        return {
            (term.direction_label, term.lag): canonical_digest([
                list(row) for row in term.operator
            ])
            for term in kernel.terms
        }

    source_map = term_map(source)
    evaluated_map = term_map(evaluated)
    keys = set(source_map) | set(evaluated_map)
    return sum(source_map.get(key) != evaluated_map.get(key) for key in keys)
