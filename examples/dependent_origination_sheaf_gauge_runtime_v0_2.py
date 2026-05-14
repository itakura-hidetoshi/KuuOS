#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SheafGaugeDependentOriginationClaim:
    # Hard anti-reification / anti-graph guards.
    claims_self_origin: bool = False
    claims_independent_essence: bool = False
    hides_conditions: bool = False
    collapses_to_flat_graph: bool = False

    # Site / cover layer.
    has_site: bool = True
    has_cover_family: bool = True
    cover_is_nonempty: bool = True
    has_local_sections: bool = True
    has_restriction_maps: bool = True
    restriction_maps_respect_scope: bool = True

    # Sheaf gluing layer.
    overlap_compatibility_ok: bool = True
    cocycle_condition_ok: bool = True
    gluing_witness_ok: bool = True
    uniqueness_up_to_boundary_ok: bool = True

    # Gauge / fibered context layer.
    has_fibered_context: bool = True
    has_gauge_connection: bool = True
    parallel_transport_defined: bool = True
    holonomy_recorded: bool = True
    curvature_exposed: bool = True

    # Governance boundary.
    lineage_bound: bool = True
    boundary_visible: bool = True
    context_visible: bool = True
    scope_visible: bool = True


def evaluate_sheaf_gauge_dependent_origination(c: SheafGaugeDependentOriginationClaim) -> dict:
    if c.claims_self_origin:
        status, reason = "REJECT", "self_origin_is_forbidden"
    elif c.claims_independent_essence:
        status, reason = "REJECT", "independent_essence_is_forbidden"
    elif c.hides_conditions:
        status, reason = "REJECT", "hidden_conditions_are_forbidden"
    elif c.collapses_to_flat_graph:
        status, reason = "REJECT", "flat_graph_collapse_forbidden_in_v0_2"
    elif not all([c.has_site, c.has_cover_family, c.cover_is_nonempty]):
        status, reason = "OBSERVE", "site_and_cover_family_required"
    elif not all([c.has_local_sections, c.has_restriction_maps, c.restriction_maps_respect_scope]):
        status, reason = "HOLD", "local_sections_and_restriction_maps_required"
    elif not c.overlap_compatibility_ok:
        status, reason = "HOLD", "overlap_compatibility_required"
    elif not c.cocycle_condition_ok:
        status, reason = "HOLD", "cocycle_condition_required"
    elif not c.gluing_witness_ok:
        status, reason = "HOLD", "gluing_witness_required"
    elif not c.uniqueness_up_to_boundary_ok:
        status, reason = "HOLD", "uniqueness_up_to_boundary_required"
    elif not all([c.has_fibered_context, c.has_gauge_connection, c.parallel_transport_defined]):
        status, reason = "HOLD", "fibered_gauge_context_required"
    elif not c.holonomy_recorded:
        status, reason = "OBSERVE", "holonomy_record_required"
    elif not c.curvature_exposed:
        status, reason = "OBSERVE", "curvature_must_be_exposed"
    elif not all([c.lineage_bound, c.boundary_visible, c.context_visible, c.scope_visible]):
        status, reason = "OBSERVE", "lineage_boundary_context_scope_visibility_required"
    else:
        status, reason = "CANDIDATE", "valid_sheaf_gauge_conditioned_appearance"
    return {
        "status": status,
        "reason": reason,
        "principle": "dependent_origination_sheaf_gauge",
        "graph_only_model_allowed": False,
        "self_origin_allowed": False,
        "independent_essence_allowed": False,
        "site_cover_required": True,
        "gluing_required": True,
        "gauge_connection_required": True,
        "holonomy_record_required": True,
        "curvature_visibility_required": True,
        "execution_authority_granted": False,
        "proof_authority_granted": False,
        "truth_authority_granted": False,
        "essence_authority_granted": False,
        "teni_authority_granted": False,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(evaluate_sheaf_gauge_dependent_origination(SheafGaugeDependentOriginationClaim()), ensure_ascii=False, indent=2))
