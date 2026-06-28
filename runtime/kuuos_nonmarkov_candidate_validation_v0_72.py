#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)
from runtime.kuuos_leibniz_module_connection_v0_71 import (
    FreeLeftModuleSection,
    LeibnizModuleConnection,
    rect_close,
)
from runtime.kuuos_memory_history_v0_72 import (
    MemoryHistoryFrame,
    ReadOnlyMemoryHistory,
)
from runtime.kuuos_module_connection_v0_70 import Matrix
from runtime.kuuos_noncommutative_differential_calculus_v0_71 import (
    InnerDifferentialCalculus,
)
from runtime.kuuos_nonmarkov_memory_connection_v0_72 import (
    NonMarkovMemoryConnection,
    nonmarkov_gauge_covariant_on,
    satisfies_pathwise_leibniz,
)
from runtime.kuuos_nonmarkov_memory_kernel_v0_72 import (
    FiniteMemoryKernel,
    MemoryKernelDeformation,
    deform_memory_kernel,
    kernel_issues,
    memory_contribution_from_frames,
    memory_kernel_left_linear_on,
    memory_projector_coordinates,
    rollback_memory_kernel,
)
from runtime.kuuos_state_module_v0_70 import KuuStateModule

VERSION = "kuuos_nonmarkov_candidate_validation_v0_72"
READY = "NONMARKOV_MEMORY_CANDIDATE_READY"
BLOCKED = "NONMARKOV_MEMORY_CANDIDATE_BLOCKED"


@dataclass(frozen=True)
class NonMarkovMemoryCandidateReceipt:
    status: str
    source_history_digest: str
    source_kernel_digest: str
    candidate_kernel_digest: str
    base_connection_digest: str
    candidate_connection_digest: str
    deformation_digest: str
    memory_supported: bool
    semantic_projectors_commute: bool
    protected_part_zero: bool
    authority_filtration_preserved: bool
    kernel_left_module_linear: bool
    pathwise_leibniz_exact: bool
    gauge_covariant: bool
    nonmarkov_history_dependence: bool
    rollback_exact: bool
    source_history_unchanged: bool
    source_kernel_unchanged: bool
    candidate_only: bool
    live_effect_allowed: bool
    state_write_allowed: bool
    authority_widening_allowed: bool
    blockers: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload


def nonmarkov_receipt_digest(receipt: NonMarkovMemoryCandidateReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


def _zero_memory_coordinates(
    section: FreeLeftModuleSection,
    coordinates: tuple[int, ...],
) -> FreeLeftModuleSection:
    selected = set(coordinates)
    values = tuple(
        tuple(0.0 if column in selected else value for column, value in enumerate(row))
        for row in section.values
    )
    return FreeLeftModuleSection(values, section.context_dimension, section.module_rank)


def _history_dependence_verified(
    module: KuuStateModule,
    kernel: FiniteMemoryKernel,
    history: ReadOnlyMemoryHistory,
    current_epoch: int,
) -> bool:
    long_term = next((term for term in kernel.terms if term.lag > 1), None)
    if long_term is None:
        return False
    target_epoch = current_epoch - long_term.lag
    target = history.frame_at(target_epoch)
    if target is None:
        return False
    coordinates = memory_projector_coordinates(module)
    altered_frames = tuple(
        MemoryHistoryFrame(
            frame.epoch,
            _zero_memory_coordinates(frame.section, coordinates)
            if frame.epoch == target_epoch
            else frame.section,
            frame.source_capsule_digest,
        )
        for frame in history.frames
    )
    original = memory_contribution_from_frames(
        kernel,
        history.frames,
        long_term.direction_label,
        current_epoch,
    )
    altered = memory_contribution_from_frames(
        kernel,
        altered_frames,
        long_term.direction_label,
        current_epoch,
    )
    return not rect_close(original.values, altered.values)


def validate_nonmarkov_candidate(
    module: KuuStateModule,
    calculus: InnerDifferentialCalculus,
    base_connection: LeibnizModuleConnection,
    history: ReadOnlyMemoryHistory,
    source_kernel: FiniteMemoryKernel,
    deformation: MemoryKernelDeformation,
    gauge: SignedPermutation,
    algebra_samples: tuple[Matrix, ...],
    current_sections: tuple[FreeLeftModuleSection, ...],
    current_epoch: int,
) -> tuple[NonMarkovMemoryConnection, NonMarkovMemoryCandidateReceipt]:
    issues: list[str] = []
    history_digest_before = history.digest
    source_kernel_digest_before = source_kernel.digest

    source_issues = kernel_issues(module, history, source_kernel)
    issues.extend(source_issues)
    try:
        candidate_kernel = deform_memory_kernel(source_kernel, deformation)
    except ValueError as error:
        issues.append(str(error))
        candidate_kernel = source_kernel
    candidate_issues = kernel_issues(module, history, candidate_kernel)
    issues.extend(candidate_issues)

    source_connection = NonMarkovMemoryConnection(base_connection, source_kernel)
    candidate_connection = NonMarkovMemoryConnection(base_connection, candidate_kernel)

    kernel_left_module_linear = False
    pathwise_leibniz_exact = False
    gauge_covariant = False
    nonmarkov_history_dependence = False
    try:
        kernel_left_module_linear = all(
            memory_kernel_left_linear_on(
                kernel,
                history,
                algebra_element,
                direction_label,
                current_epoch,
            )
            for kernel in (source_kernel, candidate_kernel)
            for algebra_element in algebra_samples
            for direction_label in calculus.direction_labels
        )
        pathwise_leibniz_exact = all(
            satisfies_pathwise_leibniz(
                connection,
                calculus,
                module,
                direction_index,
                algebra_element,
                current,
                history,
                current_epoch,
            )
            for connection in (source_connection, candidate_connection)
            for direction_index in range(len(calculus.direction_labels))
            for algebra_element in algebra_samples
            for current in current_sections
        )
        gauge_covariant = module.is_admissible_gauge(gauge) and all(
            nonmarkov_gauge_covariant_on(
                connection,
                calculus,
                direction_index,
                current,
                history,
                current_epoch,
                gauge,
            )
            for connection in (source_connection, candidate_connection)
            for direction_index in range(len(calculus.direction_labels))
            for current in current_sections
        )
        nonmarkov_history_dependence = _history_dependence_verified(
            module,
            candidate_kernel,
            history,
            current_epoch,
        )
    except ValueError as error:
        issues.append(str(error))

    if not kernel_left_module_linear:
        issues.append("memory_kernel_not_left_module_linear")
    if not pathwise_leibniz_exact:
        issues.append("nonmarkov_pathwise_leibniz_failed")
    if not gauge_covariant:
        issues.append("nonmarkov_connection_not_gauge_covariant")
    if not nonmarkov_history_dependence:
        issues.append("nonmarkov_history_dependence_missing")

    rollback_exact = False
    try:
        _, rollback_exact = rollback_memory_kernel(
            source_kernel,
            candidate_kernel,
            deformation,
        )
    except ValueError as error:
        issues.append(str(error))
    if not rollback_exact:
        issues.append("memory_kernel_rollback_not_exact")

    source_history_unchanged = history.digest == history_digest_before
    source_kernel_unchanged = source_kernel.digest == source_kernel_digest_before
    if not source_history_unchanged:
        issues.append("source_memory_history_changed")
    if not source_kernel_unchanged:
        issues.append("source_memory_kernel_changed")

    combined_issues = tuple(dict.fromkeys(source_issues + candidate_issues))
    memory_supported = "memory_kernel_not_memory_supported" not in combined_issues
    semantic_ok = "memory_kernel_semantic_projector_noncommuting" not in combined_issues
    protected_ok = "memory_kernel_protected_part_nonzero" not in combined_issues
    filtration_ok = "memory_kernel_authority_filtration_not_preserved" not in combined_issues
    issues = list(dict.fromkeys(issues))
    status = READY if not issues else BLOCKED

    receipt = NonMarkovMemoryCandidateReceipt(
        status,
        history.digest,
        source_kernel.digest,
        candidate_kernel.digest,
        base_connection.digest,
        candidate_connection.digest,
        deformation.digest,
        memory_supported,
        semantic_ok,
        protected_ok,
        filtration_ok,
        kernel_left_module_linear,
        pathwise_leibniz_exact,
        gauge_covariant,
        nonmarkov_history_dependence,
        rollback_exact,
        source_history_unchanged,
        source_kernel_unchanged,
        source_kernel.candidate_only and deformation.candidate_only,
        False,
        False,
        False,
        tuple(issues),
        "",
    )
    return candidate_connection, replace(
        receipt,
        receipt_digest=nonmarkov_receipt_digest(receipt),
    )
