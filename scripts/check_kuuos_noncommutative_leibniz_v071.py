#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_connection_deformation_v0_70 import ConnectionDeformation
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)
from runtime.kuuos_leibniz_candidate_validation_v0_71 import (
    BLOCKED,
    READY,
    validate_leibniz_candidate,
)
from runtime.kuuos_leibniz_module_connection_v0_71 import (
    FreeLeftModuleSection,
    LeibnizModuleConnection,
)
from runtime.kuuos_module_connection_v0_70 import (
    EndomorphismValuedOneForm,
    ModuleConnection,
    matrix,
    matrix_add,
    zero_matrix,
)
from runtime.kuuos_noncommutative_differential_calculus_v0_71 import (
    InnerDifferentialCalculus,
)
from runtime.kuuos_state_module_v0_70 import KuuStateModule, Projector, SubmoduleSpec


def square_matrix(rank: int, entries: dict[tuple[int, int], float]):
    values = [[0.0 for _ in range(rank)] for _ in range(rank)]
    for (row, column), value in entries.items():
        values[row][column] = value
    return matrix(values, rank)


def fixture():
    h_dt = square_matrix(2, {(0, 0): 1.0})
    h_dx = square_matrix(2, {(1, 1): 1.0})
    calculus = InnerDifferentialCalculus(
        "kuuos-matrix-context-algebra",
        2,
        ("dt", "dx"),
        (h_dt, h_dx),
    )

    module = KuuStateModule(
        calculus.digest,
        10,
        (
            Projector("observe", (2, 3)),
            Projector("verify", (4, 5)),
            Projector("memory", (6, 7)),
            Projector("ethics", (8, 9)),
        ),
        (
            SubmoduleSpec("F0-protected", (0, 1)),
            SubmoduleSpec("F1-observe", (0, 1, 2, 3)),
            SubmoduleSpec("F2-verify", (0, 1, 2, 3, 4, 5)),
            SubmoduleSpec("F3-memory", (0, 1, 2, 3, 4, 5, 6, 7)),
            SubmoduleSpec("F4-ethics", tuple(range(10))),
        ),
        Projector("protected", (0, 1)),
    )

    source_form = EndomorphismValuedOneForm(
        calculus.direction_labels,
        (
            square_matrix(10, {(2, 3): 1.0, (3, 2): -1.0}),
            square_matrix(10, {(2, 2): 1.0, (3, 3): -1.0}),
        ),
        10,
    )
    source_module_connection = ModuleConnection(
        source_form,
        module.digest,
        canonical_digest({"module": module.digest, "gauge": "channel-preserving"}),
    )
    source = LeibnizModuleConnection(calculus.digest, source_module_connection)

    alpha = EndomorphismValuedOneForm(
        calculus.direction_labels,
        (
            zero_matrix(10),
            square_matrix(10, {(2, 2): -1.0, (3, 3): 1.0}),
        ),
        10,
    )
    deformation = ConnectionDeformation(alpha, source_module_connection.digest)
    gauge = SignedPermutation(
        (0, 1, 3, 2, 4, 5, 6, 7, 8, 9),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    )

    identity = square_matrix(2, {(0, 0): 1.0, (1, 1): 1.0})
    e12 = square_matrix(2, {(0, 1): 1.0})
    e21 = square_matrix(2, {(1, 0): 1.0})
    diagonal = square_matrix(2, {(0, 0): 2.0, (1, 1): -1.0})
    algebra_samples = (identity, e12, e21, matrix_add(e12, diagonal))

    section_one = FreeLeftModuleSection(
        (
            (0.0, 0.0, 1.0, 2.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0),
            (0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0),
        ),
        2,
        10,
    )
    section_two = FreeLeftModuleSection(
        (
            (0.0, 0.0, 0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0),
            (0.0, 0.0, 1.5, 0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
        ),
        2,
        10,
    )
    return (
        calculus,
        module,
        source,
        deformation,
        gauge,
        algebra_samples,
        (section_one, section_two),
        (e12, e21),
    )


def main() -> int:
    inputs = fixture()
    candidate, receipt = validate_leibniz_candidate(*inputs)
    assert receipt.status == READY
    assert receipt.algebra_noncommutative
    assert receipt.differential_leibniz_exact
    assert receipt.differential_directions_commute
    assert receipt.source_connection_leibniz_exact
    assert receipt.candidate_connection_leibniz_exact
    assert receipt.connection_difference_module_linear
    assert receipt.curvature_module_linear
    assert receipt.gauge_covariant
    assert receipt.semantic_projectors_commute
    assert receipt.protected_part_zero
    assert receipt.authority_filtration_preserved
    assert receipt.curvature_nonincreasing
    assert receipt.rollback_exact
    assert receipt.source_unchanged
    assert receipt.candidate_only
    assert receipt.live_effect_allowed is False
    assert receipt.authority_widening_allowed is False
    assert candidate.digest == receipt.candidate_connection_digest

    calculus, module, source, deformation, gauge, algebra_samples, sections, witness = inputs
    commuting_witness = (algebra_samples[0], algebra_samples[0])
    _, witness_blocked = validate_leibniz_candidate(
        module,
        calculus,
        source,
        deformation,
        gauge,
        algebra_samples,
        sections,
        commuting_witness,
    )
    assert witness_blocked.status == BLOCKED
    assert "context_algebra_noncommutative_witness_missing" in witness_blocked.blockers

    cross_channel_alpha = EndomorphismValuedOneForm(
        calculus.direction_labels,
        (
            square_matrix(10, {(4, 2): 1.0}),
            zero_matrix(10),
        ),
        10,
    )
    cross_channel = replace(deformation, alpha=cross_channel_alpha)
    _, cross_channel_receipt = validate_leibniz_candidate(
        module,
        calculus,
        source,
        cross_channel,
        gauge,
        algebra_samples,
        sections,
        witness,
    )
    assert cross_channel_receipt.status == BLOCKED
    assert "deformation_semantic_projector_noncommuting" in cross_channel_receipt.blockers
    assert "deformation_authority_filtration_not_preserved" in cross_channel_receipt.blockers

    print(json.dumps({
        "status": "KUUOS_NONCOMMUTATIVE_LEIBNIZ_V0_71_VALIDATED",
        "calculus_digest": calculus.digest,
        "module_digest": module.digest,
        "source_connection_digest": source.digest,
        "candidate_connection_digest": candidate.digest,
        "checks": [
            "noncommutative-context-algebra",
            "inner-derivation-leibniz",
            "commuting-differential-directions",
            "source-and-candidate-leibniz",
            "connection-difference-module-linearity",
            "curvature-module-linearity",
            "gauge-covariance",
            "semantic-and-filtration-admissibility",
            "exact-rollback",
            "fail-closed-witness-and-cross-channel",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
