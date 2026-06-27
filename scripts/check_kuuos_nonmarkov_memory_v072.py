#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_leibniz_candidate_validation_v0_71 import validate_leibniz_candidate
from runtime.kuuos_leibniz_module_connection_v0_71 import (
    FreeLeftModuleSection,
    rect_close,
)
from runtime.kuuos_memory_history_v0_72 import (
    MemoryHistoryFrame,
    ReadOnlyMemoryHistory,
)
from runtime.kuuos_module_connection_v0_70 import zero_matrix
from runtime.kuuos_nonmarkov_candidate_validation_v0_72 import (
    BLOCKED,
    READY,
    validate_nonmarkov_candidate,
)
from runtime.kuuos_nonmarkov_memory_connection_v0_72 import (
    NonMarkovMemoryConnection,
    apply_nonmarkov_connection,
)
from runtime.kuuos_nonmarkov_memory_kernel_v0_72 import (
    FiniteMemoryKernel,
    MemoryKernelDeformation,
    MemoryKernelTerm,
)
from scripts.check_kuuos_noncommutative_leibniz_v071 import (
    fixture as leibniz_fixture,
    square_matrix,
)


def history_fixture(source_capsule_digest: str) -> ReadOnlyMemoryHistory:
    frame_seven = FreeLeftModuleSection(
        (
            (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, -1.0, 0.0, 0.0),
            (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 1.5, 0.0, 0.0),
        ),
        2,
        10,
    )
    frame_eight = FreeLeftModuleSection(
        (
            (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0),
            (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, -0.5, 0.0, 0.0),
        ),
        2,
        10,
    )
    frame_nine = FreeLeftModuleSection(
        (
            (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.25, 0.0, 0.0),
            (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.75, 1.0, 0.0, 0.0),
        ),
        2,
        10,
    )
    return ReadOnlyMemoryHistory(
        "memory-history-v072",
        source_capsule_digest,
        (
            MemoryHistoryFrame(7, frame_seven, source_capsule_digest),
            MemoryHistoryFrame(8, frame_eight, source_capsule_digest),
            MemoryHistoryFrame(9, frame_nine, source_capsule_digest),
        ),
    )


def main() -> int:
    leibniz_inputs = leibniz_fixture()
    calculus, module, source, _, gauge, algebra_samples, sections, _ = leibniz_inputs
    base_connection, base_receipt = validate_leibniz_candidate(*leibniz_inputs)
    assert base_receipt.status == "LEIBNIZ_CONNECTION_CANDIDATE_READY"

    source_capsule_digest = canonical_digest({"memory_capsule": "read-only-v072"})
    history = history_fixture(source_capsule_digest)
    history_digest_before = history.digest

    source_kernel = FiniteMemoryKernel(
        module.digest,
        history.digest,
        calculus.direction_labels,
        module.module_rank,
        (
            MemoryKernelTerm(
                "dt",
                1,
                square_matrix(10, {(6, 6): 0.1, (7, 7): 0.2}),
            ),
        ),
    )
    deformation = MemoryKernelDeformation(
        source_kernel.digest,
        (
            MemoryKernelTerm(
                "dt",
                3,
                square_matrix(10, {(6, 6): 0.25, (7, 7): -0.25}),
            ),
            MemoryKernelTerm(
                "dx",
                2,
                square_matrix(10, {(6, 7): 0.15, (7, 6): -0.15}),
            ),
        ),
    )

    candidate, receipt = validate_nonmarkov_candidate(
        module,
        calculus,
        base_connection,
        history,
        source_kernel,
        deformation,
        gauge,
        algebra_samples,
        sections,
        10,
    )
    assert receipt.status == READY
    assert receipt.memory_supported
    assert receipt.semantic_projectors_commute
    assert receipt.protected_part_zero
    assert receipt.authority_filtration_preserved
    assert receipt.kernel_left_module_linear
    assert receipt.pathwise_leibniz_exact
    assert receipt.gauge_covariant
    assert receipt.nonmarkov_history_dependence
    assert receipt.rollback_exact
    assert receipt.source_history_unchanged
    assert receipt.source_kernel_unchanged
    assert receipt.candidate_only
    assert receipt.live_effect_allowed is False
    assert receipt.state_write_allowed is False
    assert receipt.authority_widening_allowed is False
    assert history.digest == history_digest_before

    source_connection = NonMarkovMemoryConnection(base_connection, source_kernel)
    source_value = apply_nonmarkov_connection(
        source_connection,
        calculus,
        module,
        0,
        sections[0],
        history,
        10,
    )
    candidate_value = apply_nonmarkov_connection(
        candidate,
        calculus,
        module,
        0,
        sections[0],
        history,
        10,
    )
    assert not rect_close(source_value.values, candidate_value.values)

    invalid_deformation = replace(
        deformation,
        delta_terms=(
            MemoryKernelTerm(
                "dt",
                2,
                square_matrix(10, {(8, 6): 1.0}),
            ),
        ),
    )
    _, invalid_receipt = validate_nonmarkov_candidate(
        module,
        calculus,
        base_connection,
        history,
        source_kernel,
        invalid_deformation,
        gauge,
        algebra_samples,
        sections,
        10,
    )
    assert invalid_receipt.status == BLOCKED
    assert "memory_kernel_not_memory_supported" in invalid_receipt.blockers
    assert "memory_kernel_semantic_projector_noncommuting" in invalid_receipt.blockers
    assert "memory_kernel_authority_filtration_not_preserved" in invalid_receipt.blockers

    missing_history_deformation = replace(
        deformation,
        delta_terms=(
            MemoryKernelTerm("dt", 4, zero_matrix(10)),
            MemoryKernelTerm(
                "dx",
                4,
                square_matrix(10, {(6, 6): 0.1}),
            ),
        ),
    )
    _, missing_receipt = validate_nonmarkov_candidate(
        module,
        calculus,
        base_connection,
        history,
        source_kernel,
        missing_history_deformation,
        gauge,
        algebra_samples,
        sections,
        10,
    )
    assert missing_receipt.status == BLOCKED
    assert "memory_kernel_required_history_missing" in missing_receipt.blockers

    print(json.dumps({
        "status": "KUUOS_NONMARKOV_MEMORY_V0_72_VALIDATED",
        "history_digest": history.digest,
        "source_kernel_digest": source_kernel.digest,
        "candidate_kernel_digest": receipt.candidate_kernel_digest,
        "candidate_connection_digest": candidate.digest,
        "checks": [
            "read-only-history",
            "memory-submodule-support",
            "semantic-projector-commutation",
            "authority-filtration",
            "kernel-left-module-linearity",
            "pathwise-leibniz",
            "nonmarkov-history-dependence",
            "gauge-covariance",
            "exact-kernel-rollback",
            "cross-channel-and-missing-history-fail-closed",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
