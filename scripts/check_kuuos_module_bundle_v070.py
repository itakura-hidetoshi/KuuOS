#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_connection_deformation_v0_70 import ConnectionDeformation
from runtime.kuuos_context_algebra_v0_70 import ContextAlgebra
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)
from runtime.kuuos_module_candidate_validation_v0_70 import (
    BLOCKED,
    READY,
    validate_module_candidate,
)
from runtime.kuuos_module_connection_v0_70 import (
    EndomorphismValuedOneForm,
    ModuleConnection,
    matrix,
    zero_matrix,
)
from runtime.kuuos_state_module_v0_70 import KuuStateModule, Projector, SubmoduleSpec


def block_matrix(rank: int, entries: dict[tuple[int, int], float]):
    values = [[0.0 for _ in range(rank)] for _ in range(rank)]
    for (row, column), value in entries.items():
        values[row][column] = value
    return matrix(values, rank)


def fixture():
    algebra = ContextAlgebra("kuuos-context-algebra", ("dt", "dx"), noncommutative=True)
    module = KuuStateModule(
        algebra.digest,
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
        algebra.differential_directions,
        (
            block_matrix(10, {(2, 3): 1.0, (3, 2): -1.0}),
            block_matrix(10, {(2, 2): 1.0, (3, 3): -1.0}),
        ),
        10,
    )
    source = ModuleConnection(
        source_form,
        module.digest,
        canonical_digest({"module": module.digest, "gauge": "channel-preserving"}),
    )
    alpha = EndomorphismValuedOneForm(
        algebra.differential_directions,
        (
            zero_matrix(10),
            block_matrix(10, {(2, 2): -1.0, (3, 3): 1.0}),
        ),
        10,
    )
    deformation = ConnectionDeformation(alpha, source.digest)
    gauge = SignedPermutation(
        (0, 1, 3, 2, 4, 5, 6, 7, 8, 9),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    )
    return algebra, module, source, deformation, gauge


def main() -> int:
    algebra, module, source, deformation, gauge = fixture()
    candidate, receipt = validate_module_candidate(module, source, deformation, gauge)
    assert receipt.status == READY
    assert receipt.source_curvature_observable > receipt.candidate_curvature_observable
    assert receipt.curvature_nonincreasing
    assert receipt.semantic_projectors_commute
    assert receipt.protected_part_zero
    assert receipt.authority_filtration_preserved
    assert receipt.gauge_observables_preserved
    assert receipt.rollback_exact
    assert receipt.source_unchanged
    assert receipt.candidate_only
    assert receipt.live_effect_allowed is False
    assert receipt.authority_widening_allowed is False
    assert candidate.digest == receipt.candidate_connection_digest

    invalid_alpha = EndomorphismValuedOneForm(
        algebra.differential_directions,
        (
            block_matrix(10, {(4, 2): 1.0}),
            zero_matrix(10),
        ),
        10,
    )
    invalid = replace(deformation, alpha=invalid_alpha)
    _, invalid_receipt = validate_module_candidate(module, source, invalid, gauge)
    assert invalid_receipt.status == BLOCKED
    assert "deformation_semantic_projector_noncommuting" in invalid_receipt.blockers
    assert "deformation_authority_filtration_not_preserved" in invalid_receipt.blockers

    protected_alpha = EndomorphismValuedOneForm(
        algebra.differential_directions,
        (
            block_matrix(10, {(0, 0): 1.0}),
            zero_matrix(10),
        ),
        10,
    )
    protected = replace(deformation, alpha=protected_alpha)
    _, protected_receipt = validate_module_candidate(module, source, protected, gauge)
    assert protected_receipt.status == BLOCKED
    assert "deformation_protected_part_nonzero" in protected_receipt.blockers

    print(json.dumps({
        "status": "KUUOS_MODULE_BUNDLE_V0_70_VALIDATED",
        "algebra_digest": algebra.digest,
        "module_digest": module.digest,
        "source_connection_digest": source.digest,
        "candidate_connection_digest": candidate.digest,
        "checks": [
            "fiber-direct-sum",
            "semantic-projector-commutation",
            "protected-vanishing",
            "authority-filtration",
            "curvature-decrease",
            "gauge-invariance",
            "exact-rollback",
            "candidate-only-boundary",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
