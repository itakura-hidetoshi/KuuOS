#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EmptinessClaim:
    names_k_as_object: bool = False
    treats_k_as_nothingness: bool = False
    treats_k_as_creator: bool = False
    observes_k_directly: bool = False
    collapses_k_and_kperp: bool = False
    has_lineage: bool = True
    has_boundary: bool = True
    has_context: bool = True
    has_scope: bool = True
    appearance_in_kperp: bool = True


def evaluate_emptiness(c: EmptinessClaim) -> dict:
    if c.names_k_as_object:
        status, reason = "REJECT", "K_must_not_be_objectified"
    elif c.treats_k_as_creator:
        status, reason = "REJECT", "K_must_not_be_creator_substance"
    elif c.treats_k_as_nothingness:
        status, reason = "REPAIR", "K_is_not_nihilistic_nothingness"
    elif c.observes_k_directly:
        status, reason = "HOLD", "direct_K_observation_forbidden"
    elif c.collapses_k_and_kperp:
        status, reason = "HOLD", "K_and_K_perp_must_not_collapse"
    elif not c.appearance_in_kperp:
        status, reason = "REJECT", "appearances_must_be_measured_in_K_perp"
    elif not all([c.has_lineage, c.has_boundary, c.has_context, c.has_scope]):
        status, reason = "OBSERVE", "dependent_origination_metadata_incomplete"
    else:
        status, reason = "CANDIDATE", "valid_non_reified_conditioned_appearance"
    return {
        "status": status,
        "reason": reason,
        "emptiness_ground": "K",
        "appearance_space": "K_perp",
        "direct_K_observable": False,
        "execution_authority_granted": False,
        "proof_authority_granted": False,
        "truth_authority_granted": False,
        "essence_authority_granted": False,
        "teni_authority_granted": False,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(evaluate_emptiness(EmptinessClaim()), ensure_ascii=False, indent=2))
