#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import sha, without

VERSION = "kuuos_context_gerbe_coherence_v0_14"
DECISION_VERSION = "kuuos_context_gerbe_coherence_decision_v0_14"
BUNDLE_VERSION = "kuuos_context_gerbe_coherence_bundle_v0_14"
READY = "KUUOS_CONTEXT_GERBE_COHERENCE_V0_14_READY"
REPLAYED = "KUUOS_CONTEXT_GERBE_COHERENCE_V0_14_REPLAYED"

REQUIRED_BOUNDARY = {
    "v0_13_decision_is_the_only_pairwise_transport_source": True,
    "pairwise_atlas_transitions_preserved": True,
    "triple_overlap_two_cells_enabled": True,
    "quadruple_overlap_coherence_observed": True,
    "two_cell_residue_is_not_a_veto": True,
    "higher_cocycle_defect_is_not_a_veto": True,
    "global_trivialization_forbidden": True,
    "one_v0_13_local_lift_per_gerbe_cycle": True,
    "v0_13_authority_preserved": True,
    "surface_holonomy_append_only": True,
    "deterministic_replay_required": True,
    "graph_semantics_forbidden": True,
}


def decision_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "gerbe_decision_digest"))


def bundle_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "gerbe_bundle_digest"))
