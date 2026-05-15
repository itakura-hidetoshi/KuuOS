#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(name: str, rel_path: str) -> Any:
    path = ROOT / rel_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load {rel_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


emptiness = load_module("emptiness_runtime_v0_1", "examples/emptiness_runtime_v0_1.py")
dependent_origination = load_module(
    "dependent_origination_sheaf_gauge_runtime_v0_2",
    "examples/dependent_origination_sheaf_gauge_runtime_v0_2.py",
)
two_truths = load_module("two_truths_runtime_v0_1", "examples/two_truths_runtime_v0_1.py")


@dataclass(frozen=True)
class KuStringEmptinessDependentOriginationTwoTruthsClaim:
    emptiness_claim: dict[str, Any] | None = None
    dependent_origination_claim: dict[str, Any] | None = None
    two_truths_claim: dict[str, Any] | None = None

    # KuString-MGAP4D-Emptiness Core v0.2 triangle.
    k_is_non_reified_reference_ground: bool = True
    delta_rel_present: bool = True
    string_mode_in_kperp: bool = True
    string_mode_worldsheet_consistent: bool = True
    string_mode_non_substance: bool = True
    brane_is_boundary_condition: bool = True
    brane_not_substance: bool = True
    brane_supports_world_phase: bool = True
    h_world_restricted_to_kperp: bool = True
    gap_stabilizer_33_20_reference: bool = True
    psi_star_in_kperp: bool = True
    psi_star_not_k: bool = True
    centered_observable_removes_k_component: bool = True
    spectral_weight_33_20_positive: bool = True

    # Anti-collapse guards.
    collapses_k_into_delta_rel: bool = False
    treats_string_or_brane_as_k: bool = False
    treats_gap_as_ultimate_truth_object: bool = False
    treats_observable_as_direct_k_measurement: bool = False


def _status_rank(status: str) -> int:
    return {"CANDIDATE": 0, "OBSERVE": 1, "REPAIR": 2, "HOLD": 3, "REJECT": 4}.get(status, 3)


def evaluate_ku_string_emptiness_do_two_truths(
    c: KuStringEmptinessDependentOriginationTwoTruthsClaim,
) -> dict[str, Any]:
    e = emptiness.evaluate_emptiness(emptiness.EmptinessClaim(**(c.emptiness_claim or {})))
    d = dependent_origination.evaluate_sheaf_gauge_dependent_origination(
        dependent_origination.SheafGaugeDependentOriginationClaim(**(c.dependent_origination_claim or {}))
    )
    t = two_truths.evaluate_two_truths(two_truths.TwoTruthsClaim(**(c.two_truths_claim or {})))

    sub = [e, d, t]
    worst = max(sub, key=lambda x: _status_rank(x["status"]))

    if worst["status"] == "REJECT":
        status, reason = "REJECT", "subruntime_rejected"
    elif c.collapses_k_into_delta_rel:
        status, reason = "REJECT", "K_must_not_collapse_into_delta_rel"
    elif c.treats_string_or_brane_as_k:
        status, reason = "REJECT", "string_or_brane_must_not_be_identified_with_K"
    elif c.treats_gap_as_ultimate_truth_object:
        status, reason = "REJECT", "gap_must_not_reify_ultimate_truth"
    elif c.treats_observable_as_direct_k_measurement:
        status, reason = "REJECT", "observable_must_not_measure_K_directly"
    elif not c.k_is_non_reified_reference_ground:
        status, reason = "HOLD", "K_non_reified_reference_ground_required"
    elif not c.delta_rel_present:
        status, reason = "HOLD", "dependent_origination_delta_rel_required"
    elif not all([c.string_mode_in_kperp, c.string_mode_worldsheet_consistent, c.string_mode_non_substance]):
        status, reason = "HOLD", "string_mode_must_be_conditioned_non_substance_in_K_perp"
    elif not all([c.brane_is_boundary_condition, c.brane_not_substance, c.brane_supports_world_phase]):
        status, reason = "HOLD", "brane_must_be_boundary_condition_not_substance"
    elif not all([c.h_world_restricted_to_kperp, c.gap_stabilizer_33_20_reference]):
        status, reason = "HOLD", "gap_stabilizer_must_act_on_K_perp_as_reference_barrier"
    elif not all([c.psi_star_in_kperp, c.psi_star_not_k]):
        status, reason = "HOLD", "psi_star_must_be_conditioned_excitation_not_K"
    elif not all([c.centered_observable_removes_k_component, c.spectral_weight_33_20_positive]):
        status, reason = "HOLD", "centered_observable_and_spectral_weight_required"
    elif worst["status"] != "CANDIDATE":
        status, reason = worst["status"], "subruntime_requires_attention"
    else:
        status, reason = "CANDIDATE", "K_delta_rel_string_brane_Kperp_two_truths_triangle_closed"

    return {
        "status": status,
        "reason": reason,
        "principle": "emptiness_dependent_origination_two_truths_runtime",
        "triangle": "K -> delta_rel -> String/Brane -> K_perp -> H_world_gap -> two_truths_non_collapse_barrier",
        "emptiness": e,
        "dependent_origination": d,
        "two_truths": t,
        "K_is_object_allowed": False,
        "K_direct_observation_allowed": False,
        "flat_graph_dependent_origination_allowed": False,
        "string_or_brane_identified_with_K_allowed": False,
        "gap_reifies_ultimate_truth_allowed": False,
        "observable_directly_measures_K_allowed": False,
        "paramartha_samvrti_collapse_allowed": False,
        "mass_gap_bridge_role": "reference_only_non_collapse_barrier",
        "execution_authority_granted": False,
        "proof_authority_granted": False,
        "truth_authority_granted": False,
        "essence_authority_granted": False,
        "teni_authority_granted": False,
    }


if __name__ == "__main__":
    result = evaluate_ku_string_emptiness_do_two_truths(
        KuStringEmptinessDependentOriginationTwoTruthsClaim()
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
