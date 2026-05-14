#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

CANONICAL_PROOF_REPO = "itakura-hidetoshi/4d-mass-gap"
SPECTRAL_GAP_FORMALIZATION = "MGAP4D/Spectral/GapFormalization.lean"
SPECTRAL_GAP_WITNESS = "MGAP4D/Spectral/Gap.lean"
NORMALIZED_GAP_VALUE = "33/20"


@dataclass(frozen=True)
class MassGapTwoTruthsClaim:
    # Reference binding to the canonical proof repo.
    canonical_repo_bound: bool = True
    spectral_gap_formalization_visible: bool = True
    spectral_witness_visible: bool = True
    normalized_gap_value_is_33_20: bool = True
    positive_lower_bound_surface_visible: bool = True

    # Two truths boundary.
    ultimate_truth_non_reified: bool = True
    conventional_truth_surface_visible: bool = True
    vacuum_sector_boundary_visible: bool = True
    orthogonal_sector_boundary_visible: bool = True
    k_not_objectified: bool = True
    k_not_directly_observed: bool = True
    k_and_k_perp_not_collapsed: bool = True

    # Governance / release boundary inherited from 4d-mass-gap.
    non_theorem_completion_boundary_visible: bool = True
    final_gap_release_not_unlocked: bool = True
    main_pre_mathlib_boundary_preserved: bool = True

    # Anti-collapse guards.
    claims_final_theorem_release: bool = False
    treats_gap_as_ultimate_truth_object: bool = False
    treats_conventional_as_ultimate: bool = False
    collapses_two_truths: bool = False
    claims_execution_authority_from_gap: bool = False


def evaluate_massgap_two_truths(c: MassGapTwoTruthsClaim) -> dict:
    if not c.canonical_repo_bound:
        status, reason = "OBSERVE", "canonical_4d_mass_gap_repo_binding_required"
    elif not all([c.spectral_gap_formalization_visible, c.spectral_witness_visible]):
        status, reason = "OBSERVE", "spectral_formalization_and_witness_surfaces_required"
    elif not c.normalized_gap_value_is_33_20:
        status, reason = "HOLD", "normalized_gap_value_33_20_required"
    elif not c.positive_lower_bound_surface_visible:
        status, reason = "HOLD", "positive_lower_bound_surface_required"
    elif c.claims_final_theorem_release:
        status, reason = "REJECT", "kuuos_reference_does_not_unlock_final_gap_release"
    elif c.treats_gap_as_ultimate_truth_object:
        status, reason = "REJECT", "mass_gap_must_not_objectify_ultimate_truth"
    elif c.treats_conventional_as_ultimate:
        status, reason = "REJECT", "conventional_truth_must_not_be_promoted_to_ultimate_truth"
    elif c.collapses_two_truths:
        status, reason = "REJECT", "two_truths_collapse_forbidden"
    elif c.claims_execution_authority_from_gap:
        status, reason = "REJECT", "mass_gap_bridge_does_not_grant_execution_authority"
    elif not all([c.ultimate_truth_non_reified, c.k_not_objectified, c.k_not_directly_observed]):
        status, reason = "HOLD", "ultimate_truth_non_reification_boundary_required"
    elif not all([c.conventional_truth_surface_visible, c.orthogonal_sector_boundary_visible]):
        status, reason = "OBSERVE", "conventional_truth_orthogonal_surface_required"
    elif not c.vacuum_sector_boundary_visible:
        status, reason = "OBSERVE", "vacuum_sector_boundary_required"
    elif not c.k_and_k_perp_not_collapsed:
        status, reason = "HOLD", "k_and_k_perp_must_not_collapse"
    elif not all([c.non_theorem_completion_boundary_visible, c.final_gap_release_not_unlocked, c.main_pre_mathlib_boundary_preserved]):
        status, reason = "HOLD", "mgap4d_release_boundary_must_be_preserved"
    else:
        status, reason = "CANDIDATE", "massgap_backed_two_truths_boundary_valid"
    return {
        "status": status,
        "reason": reason,
        "runtime": "massgap_two_truths_runtime_v0_1",
        "canonical_proof_repo": CANONICAL_PROOF_REPO,
        "spectral_gap_formalization": SPECTRAL_GAP_FORMALIZATION,
        "spectral_gap_witness": SPECTRAL_GAP_WITNESS,
        "normalized_gap_value": NORMALIZED_GAP_VALUE,
        "ultimate_truth_objectification_allowed": False,
        "two_truths_collapse_allowed": False,
        "conventional_truth_is_gap_stabilized": True,
        "kuuos_reference_opens_final_theorem_release": False,
        "execution_authority_granted": False,
        "proof_authority_granted": False,
        "truth_authority_granted": False,
        "essence_authority_granted": False,
        "teni_authority_granted": False,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(evaluate_massgap_two_truths(MassGapTwoTruthsClaim()), ensure_ascii=False, indent=2))
