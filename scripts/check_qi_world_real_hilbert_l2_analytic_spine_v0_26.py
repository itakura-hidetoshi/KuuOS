#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_world_real_hilbert_l2_analytic_spine_embedding_v0_26 import (
    analyze_embedding,
    evaluate_analysis,
)


def main() -> int:
    coordinates = [
        {"basis_id": "p:a", "source_kind": "local_patch", "source_id": "a", "coordinate": 0.5, "weight": 1.0},
        {"basis_id": "c:ab", "source_kind": "indra_connection", "source_id": "ab", "coordinate": 0.2, "weight": 1.1},
        {"basis_id": "f:q", "source_kind": "qi_flow", "source_id": "q", "coordinate": 0.4, "weight": 1.5},
        {"basis_id": "h:aba", "source_kind": "holonomy_cycle", "source_id": "aba", "coordinate": 0.15, "weight": 2.0},
        {"basis_id": "s:o", "source_kind": "ku_string", "source_id": "o", "coordinate": 0.1, "weight": 1.3},
        {"basis_id": "m:h", "source_kind": "m_brane_surface", "source_id": "h", "coordinate": -0.2, "weight": 1.8},
    ]
    projections = [
        {"role": "scar", "basis_ids": ["h:aba"]},
        {"role": "recovery", "basis_ids": ["p:a", "c:ab"]},
        {"role": "minority_preservation", "basis_ids": ["s:o"]},
    ]
    entities = {
        "local_patch": {"a"},
        "indra_connection": {"ab"},
        "qi_flow": {"q"},
        "holonomy_cycle": {"aba"},
        "ku_string": {"o"},
        "m_brane_surface": {"h"},
    }
    policy = {
        "minimum_coordinate_count": 6,
        "maximum_coordinate_count": 32,
        "maximum_absolute_coordinate": 1.0,
        "minimum_coercivity_lower_bound": 1.0,
        "maximum_norm_squared": 10.0,
        "maximum_weighted_energy": 20.0,
        "numeric_tolerance": 1e-9,
    }
    norm_sq = sum(item["coordinate"] ** 2 for item in coordinates)
    energy = sum(item["weight"] * item["coordinate"] ** 2 for item in coordinates)
    report = {"declared_observables": {"norm_squared": norm_sq, "weighted_energy": energy, "coercivity_lower_bound": 1.0}}
    analysis = analyze_embedding(coordinates, projections, report, {"analytic_policy": policy}, {"entities": entities})
    decision, _ = evaluate_analysis(analysis, [])
    assert decision == "world_l2_analytic_spine_ready"
    assert analysis["rayleigh_lower_bound_verified"] is True
    assert analysis["source_coverage_ratio"] == 1.0
    print("qi_world_real_hilbert_l2_analytic_spine_v0_26 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
