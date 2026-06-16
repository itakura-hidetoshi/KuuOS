from __future__ import annotations

from itertools import combinations
from typing import Any

from runtime.context_gerbe_math_v014 import order_residue, quadruple_overlap
from runtime.context_math_v013 import overlap
from runtime.kuuos_context_gauge_atlas_transport_v0_13 import outcome_phase
from runtime.kuuos_context_gauge_atlas_types_v0_13 import mapping, sha


def build_fourfold_witnesses(
    *,
    gerbe_run_id: str,
    target_context_key: str,
    source_atlas_decision_digest: str,
    transitions: list[dict[str, Any]],
    floor: float,
    minimum_quadruple_overlap: float,
    phase_gain: float,
) -> tuple[list[dict[str, Any]], list[float]]:
    witnesses: list[dict[str, Any]] = []
    defects: list[float] = []
    for first, second, third in combinations(transitions, 3):
        first_chart = mapping(first.get("chart"))
        second_chart = mapping(second.get("chart"))
        third_chart = mapping(third.get("chart"))
        first_second = overlap(
            mapping(first_chart.get("context_signature")),
            mapping(second_chart.get("context_signature")),
        )
        first_third = overlap(
            mapping(first_chart.get("context_signature")),
            mapping(third_chart.get("context_signature")),
        )
        second_third = overlap(
            mapping(second_chart.get("context_signature")),
            mapping(third_chart.get("context_signature")),
        )
        support = quadruple_overlap(
            first_second,
            first_third,
            first.get("target_overlap", 0.0),
            second_third,
            second.get("target_overlap", 0.0),
            third.get("target_overlap", 0.0),
        )
        if support < minimum_quadruple_overlap:
            continue
        left_path, right_path, defect = order_residue(
            mapping(first.get("transported_section")),
            [outcome_phase(second_chart, phase_gain), outcome_phase(third_chart, phase_gain)],
            [outcome_phase(third_chart, phase_gain), outcome_phase(second_chart, phase_gain)],
            floor,
        )
        witnesses.append(
            {
                "witness_id": "gerbe-fourfold-" + sha(
                    {
                        "run": gerbe_run_id,
                        "first": first.get("source_chart_id", ""),
                        "second": second.get("source_chart_id", ""),
                        "third": third.get("source_chart_id", ""),
                        "target": target_context_key,
                        "atlas_decision": source_atlas_decision_digest,
                    }
                )[:18],
                "quadruple_overlap": support,
                "left_composite_section": left_path,
                "right_composite_section": right_path,
                "higher_cocycle_defect": defect,
                "localized_on_quadruple_overlap": True,
                "pairwise_transport_from_v0_13": True,
            }
        )
        defects.append(defect)
    return witnesses, defects
