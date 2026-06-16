from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, integer
from runtime.kuuos_context_gerbe_coherence_types_v0_14 import BUNDLE_VERSION, bundle_digest


def empty_gerbe_bundle(agent_id: str) -> dict[str, Any]:
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": agent_id,
        "generation": 0,
        "surface_holonomy": [],
        "decisions": [],
        "processed_decision_digests": [],
        "last_atlas_bundle_digest": "",
        "last_atlas_decision_digest": "",
    }
    packet["gerbe_bundle_digest"] = bundle_digest(packet)
    return packet


def commit_surface_cycle(
    *,
    previous: Mapping[str, Any],
    decision: Mapping[str, Any],
    max_surface_holonomy: int = 256,
    max_decisions: int = 256,
) -> tuple[dict[str, Any], bool]:
    digest = str(decision.get("gerbe_decision_digest", ""))
    if not digest:
        raise ValueError("gerbe_decision_digest_missing")

    processed = {str(item) for item in as_list(previous.get("processed_decision_digests"))}
    if digest in processed:
        return dict(previous), True

    record = {
        "gerbe_run_id": decision.get("gerbe_run_id", ""),
        "cycle_index": decision.get("cycle_index", 0),
        "target_context_key": decision.get("target_context_key", ""),
        "gerbe_class": decision.get("gerbe_class", ""),
        "two_cell_count": decision.get("two_cell_count", 0),
        "quadruple_witness_count": decision.get("quadruple_witness_count", 0),
        "gerbe_two_curvature": decision.get("gerbe_two_curvature", 0.0),
        "higher_cocycle_defect": decision.get("higher_cocycle_defect", 0.0),
        "source_atlas_decision_digest": decision.get("source_atlas_decision_digest", ""),
        "gerbe_decision_digest": digest,
    }
    holonomy = as_list(previous.get("surface_holonomy")) + [record]
    decisions = as_list(previous.get("decisions")) + [dict(decision)]
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": previous.get("agent_id", ""),
        "generation": integer(previous.get("generation"), 0) + 1,
        "surface_holonomy": holonomy[-max(1, int(max_surface_holonomy)):],
        "decisions": decisions[-max(1, int(max_decisions)):],
        "processed_decision_digests": sorted(processed | {digest}),
        "last_atlas_bundle_digest": decision.get("source_atlas_bundle_digest", ""),
        "last_atlas_decision_digest": decision.get("source_atlas_decision_digest", ""),
    }
    packet["gerbe_bundle_digest"] = bundle_digest(packet)
    return packet, False
