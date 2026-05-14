#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DependentOriginationClaim:
    claims_self_origin: bool = False
    claims_independent_essence: bool = False
    hides_conditions: bool = False
    collapses_to_flat_graph: bool = False
    has_lineage: bool = True
    has_boundary: bool = True
    has_context: bool = True
    has_scope: bool = True
    has_conditions: bool = True
    has_relation_roles: bool = True
    local_compatibility_ok: bool = True
    gluing_witness_ok: bool = True


def evaluate_dependent_origination(c: DependentOriginationClaim) -> dict:
    if c.claims_self_origin:
        status, reason = "REJECT", "self_origin_is_forbidden"
    elif c.claims_independent_essence:
        status, reason = "REJECT", "independent_essence_is_forbidden"
    elif c.hides_conditions:
        status, reason = "REJECT", "hidden_conditions_are_forbidden"
    elif c.collapses_to_flat_graph:
        status, reason = "REPAIR", "dependent_origination_is_not_flat_graph_only"
    elif not all([c.has_lineage, c.has_boundary, c.has_context, c.has_scope]):
        status, reason = "OBSERVE", "lineage_boundary_context_scope_required"
    elif not c.has_conditions:
        status, reason = "OBSERVE", "conditions_required"
    elif not c.has_relation_roles:
        status, reason = "OBSERVE", "relation_roles_required"
    elif not c.local_compatibility_ok:
        status, reason = "HOLD", "local_compatibility_required"
    elif not c.gluing_witness_ok:
        status, reason = "HOLD", "gluing_witness_required"
    else:
        status, reason = "CANDIDATE", "valid_conditioned_relational_appearance"
    return {
        "status": status,
        "reason": reason,
        "principle": "dependent_origination",
        "self_origin_allowed": False,
        "independent_essence_allowed": False,
        "execution_authority_granted": False,
        "proof_authority_granted": False,
        "truth_authority_granted": False,
        "essence_authority_granted": False,
        "teni_authority_granted": False,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(evaluate_dependent_origination(DependentOriginationClaim()), ensure_ascii=False, indent=2))
