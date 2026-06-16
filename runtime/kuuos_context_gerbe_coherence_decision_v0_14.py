from __future__ import annotations

from typing import Any, Mapping

from runtime.context_math_v013 import HORIZONS, aggregate
from runtime.kuuos_context_gauge_atlas_types_v0_13 import (
    clamp,
    decision_digest as atlas_decision_digest,
    mapping,
)
from runtime.kuuos_context_gerbe_coherence_access_v0_14 import (
    atlas_base_section,
    atlas_transitions,
)
from runtime.kuuos_context_gerbe_coherence_fourfold_v0_14 import build_fourfold_witnesses
from runtime.kuuos_context_gerbe_coherence_two_cell_v0_14 import build_two_cells
from runtime.kuuos_context_gerbe_coherence_types_v0_14 import (
    DECISION_VERSION,
    decision_digest,
)


def build_gerbe_coherence(
    *,
    gerbe_run_id: str,
    atlas_decision: Mapping[str, Any],
    atlas_bundle: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    source_decision_digest = str(atlas_decision.get("atlas_decision_digest", ""))
    if not source_decision_digest or source_decision_digest != atlas_decision_digest(atlas_decision):
        raise ValueError("source_atlas_decision_digest_invalid")
    source_bundle_digest = str(atlas_decision.get("source_atlas_bundle_digest", ""))
    if source_bundle_digest != str(atlas_bundle.get("atlas_bundle_digest", "")):
        raise ValueError("source_atlas_bundle_digest_mismatch")

    floor = clamp(plan.get("minimum_horizon_weight"), 0.12)
    triple_threshold = clamp(plan.get("minimum_triple_overlap"), 0.45)
    quadruple_threshold = clamp(plan.get("minimum_quadruple_overlap"), triple_threshold)
    phase_gain = clamp(plan.get("transition_phase_gain"), 0.06)
    local_retention = clamp(plan.get("gerbe_local_retention"), 0.7)
    two_curvature_threshold = clamp(plan.get("plural_gerbe_two_curvature_threshold"), 0.06)
    higher_defect_threshold = clamp(plan.get("plural_higher_cocycle_threshold"), 0.04)

    target_context_key = str(atlas_decision.get("target_context_key", ""))
    target_signature = mapping(atlas_decision.get("target_context_signature"))
    transitions = atlas_transitions(
        atlas_decision=atlas_decision,
        atlas_bundle=atlas_bundle,
        floor=floor,
    )
    atlas_base = atlas_base_section(atlas_decision, plan, floor)
    two_cells, residues, weighted = build_two_cells(
        gerbe_run_id=gerbe_run_id,
        target_context_key=target_context_key,
        source_atlas_decision_digest=source_decision_digest,
        transitions=transitions,
        floor=floor,
        minimum_triple_overlap=triple_threshold,
        phase_gain=phase_gain,
    )
    witnesses, defects = build_fourfold_witnesses(
        gerbe_run_id=gerbe_run_id,
        target_context_key=target_context_key,
        source_atlas_decision_digest=source_decision_digest,
        transitions=transitions,
        floor=floor,
        minimum_quadruple_overlap=quadruple_threshold,
        phase_gain=phase_gain,
    )

    two_curvature = round(sum(residues) / len(residues), 6) if residues else 0.0
    higher_defect = round(max(defects, default=0.0), 6)
    lifted = aggregate([(local_retention, atlas_base), *weighted], atlas_base, floor)
    if not two_cells:
        gerbe_class = "no_triple_overlap"
    elif two_curvature >= two_curvature_threshold or higher_defect >= higher_defect_threshold:
        gerbe_class = "plural_gerbe_transport"
    else:
        gerbe_class = "coherent_gerbe_transport"

    packet = {
        "version": DECISION_VERSION,
        "gerbe_run_id": gerbe_run_id,
        "cycle_index": int(atlas_decision.get("cycle_index", 0)),
        "target_context_key": target_context_key,
        "target_context_signature": dict(target_signature),
        "source_atlas_bundle_digest": source_bundle_digest,
        "source_atlas_decision_digest": source_decision_digest,
        "source_atlas_class": atlas_decision.get("atlas_class", ""),
        "gerbe_class": gerbe_class,
        "compatible_chart_count": len(transitions),
        "two_cell_count": len(two_cells),
        "quadruple_witness_count": len(witnesses),
        "two_cells": two_cells,
        "quadruple_witnesses": witnesses,
        "gerbe_two_curvature": two_curvature,
        "higher_cocycle_defect": higher_defect,
        "lifted_base_short_horizon_weight": lifted["short"],
        "lifted_base_medium_horizon_weight": lifted["medium"],
        "lifted_base_long_horizon_weight": lifted["long"],
        "lifted_weight_sum": round(sum(lifted[horizon] for horizon in HORIZONS), 6),
        "v0_13_decision_is_the_only_pairwise_transport_source": True,
        "two_cell_residue_is_not_a_veto": True,
        "higher_cocycle_defect_is_not_a_veto": True,
        "global_trivialization_forbidden": True,
        "v0_13_authority_preserved": True,
        "surface_holonomy_append_only": True,
        "gerbe_decision_digest": "",
    }
    packet["gerbe_decision_digest"] = decision_digest(packet)
    return packet
