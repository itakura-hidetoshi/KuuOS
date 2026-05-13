#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

GAP = Fraction(33, 20)


@dataclass(frozen=True)
class Packet:
    k_ok: bool = True
    k_object: bool = False
    k_direct: bool = False
    k_perp_ok: bool = True
    delta_ok: bool = True
    string_in_kperp: bool = True
    string_ok: bool = True
    brane_ok: bool = True
    brane_substance: bool = False
    gap_domain: str = "K_perp"
    psi_in_kperp: bool = True
    psi_norm_one: bool = True
    psi_gap: Fraction = GAP
    observable_centered: bool = True
    spectral_weight_positive: bool = True


def centered_observable(name: str = "A") -> str:
    return f"{name}_circ = {name} - <K,{name}K>I"


def evaluate(p: Packet) -> dict:
    status = "CANDIDATE"
    reason = "valid_world_phase_candidate"

    if p.k_object:
        status, reason = "REJECT", "K_must_not_be_object"
    elif p.k_direct:
        status, reason = "HOLD", "direct_K_measurement_forbidden"
    elif not p.k_ok:
        status, reason = "REPAIR", "H_world_K_zero_required"
    elif not p.k_perp_ok:
        status, reason = "HOLD", "K_perp_boundary_required"
    elif not p.delta_ok:
        status, reason = "OBSERVE", "delta_rel_conditions_incomplete"
    elif not p.string_in_kperp:
        status, reason = "REJECT", "StringMode_must_live_in_K_perp"
    elif not p.string_ok:
        status, reason = "HOLD", "StringMode_consistency_required"
    elif not p.brane_ok:
        status, reason = "HOLD", "Brane_support_required"
    elif p.brane_substance:
        status, reason = "REJECT", "Brane_must_not_be_substance"
    elif p.gap_domain != "K_perp":
        status, reason = "REJECT", "Gap_must_be_on_K_perp"
    elif not p.psi_in_kperp:
        status, reason = "REJECT", "psi_star_must_be_in_K_perp"
    elif not p.psi_norm_one:
        status, reason = "HOLD", "psi_star_norm_one_required"
    elif p.psi_gap != GAP:
        status, reason = "HOLD", "internal_gap_33_20_required"
    elif not p.observable_centered:
        status, reason = "HOLD", "centered_observable_required"
    elif not p.spectral_weight_positive:
        status, reason = "OBSERVE", "local_detection_required"

    return {
        "status": status,
        "reason": reason,
        "gap": str(GAP),
        "gap_domain": p.gap_domain,
        "centered_observable": centered_observable(),
        "execution_authority_granted": False,
        "proof_authority_granted": False,
        "truth_authority_granted": False,
        "essence_authority_granted": False,
        "teni_authority_granted": False,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(evaluate(Packet()), ensure_ascii=False, indent=2))
