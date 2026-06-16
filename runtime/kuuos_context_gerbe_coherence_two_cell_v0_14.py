from __future__ import annotations

from itertools import combinations
from typing import Any, Mapping

from runtime.context_gerbe_math_v014 import postcomposition_residue, triple_overlap
from runtime.context_math_v013 import overlap
from runtime.kuuos_context_gauge_atlas_transport_v0_13 import outcome_phase
from runtime.kuuos_context_gauge_atlas_types_v0_13 import mapping, sha


def build_two_cells(
    *,
    gerbe_run_id: str,
    target_context_key: str,
    source_atlas_decision_digest: str,
    transitions: list[dict[str, Any]],
    floor: float,
    minimum_triple_overlap: float,
    phase_gain: float,
) -> tuple[list[dict[str, Any]], list[float], list[tuple[float, Mapping[str, float]]]]:
    cells: list[dict[str, Any]] = []
    residues: list[float] = []
    weighted_sections: list[tuple[float, Mapping[str, float]]] = []
    for left, right in combinations(transitions, 2):
        left_chart = mapping(left.get("chart"))
        right_chart = mapping(right.get("chart"))
        source_pair_overlap = overlap(
            mapping(left_chart.get("context_signature")),
            mapping(right_chart.get("context_signature")),
        )
        support = triple_overlap(
            source_pair_overlap,
            left.get("target_overlap", 0.0),
            right.get("target_overlap", 0.0),
        )
        if support < minimum_triple_overlap:
            continue
        direct, composite, residue = postcomposition_residue(
            mapping(left.get("transported_section")),
            [outcome_phase(right_chart, phase_gain)],
            floor,
        )
        cells.append(
            {
                "two_cell_id": "gerbe-two-cell-" + sha(
                    {
                        "run": gerbe_run_id,
                        "source": left.get("source_chart_id", ""),
                        "mediator": right.get("source_chart_id", ""),
                        "target": target_context_key,
                        "atlas_decision": source_atlas_decision_digest,
                    }
                )[:18],
                "source_chart_id": left.get("source_chart_id", ""),
                "mediator_chart_id": right.get("source_chart_id", ""),
                "target_context_key": target_context_key,
                "source_pair_overlap": source_pair_overlap,
                "left_target_overlap": left.get("target_overlap", 0.0),
                "right_target_overlap": right.get("target_overlap", 0.0),
                "triple_overlap": support,
                "direct_section": direct,
                "composite_section": composite,
                "coherence_residue": residue,
                "localized_on_triple_overlap": True,
                "pairwise_transport_from_v0_13": True,
            }
        )
        residues.append(residue)
        weighted_sections.append((support / 2.0, direct))
        weighted_sections.append((support / 2.0, composite))
    return cells, residues, weighted_sections
