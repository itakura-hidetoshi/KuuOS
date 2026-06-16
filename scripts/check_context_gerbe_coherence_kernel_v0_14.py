#!/usr/bin/env python3

from runtime.kuuos_context_gauge_atlas_basis_v0_13 import empty_bundle, initial_chart
from runtime.kuuos_context_gauge_atlas_decision_v0_13 import build_atlas_decision
from runtime.kuuos_context_gauge_atlas_types_v0_13 import bundle_digest as atlas_bundle_digest
from runtime.kuuos_context_gerbe_coherence_bundle_v0_14 import (
    commit_surface_cycle,
    empty_gerbe_bundle,
)
from runtime.kuuos_context_gerbe_coherence_types_v0_14 import bundle_digest, decision_digest
from runtime.kuuos_context_gerbe_coherence_v0_14 import build_gerbe_coherence


def observed(key, signature, short, medium, long, outcome):
    packet = initial_chart(key, signature)
    packet.update(
        {
            "cycle_count": 1,
            "last_short_weight": short,
            "last_medium_weight": medium,
            "last_long_weight": long,
            "last_commitment_outcome_class": outcome,
        }
    )
    return packet


def main():
    a = {
        "wake_kind": "observation",
        "source_kinds": ["observation", "sensor"],
        "signal_kinds": ["progress", "repair"],
        "source_ids": ["a", "shared"],
    }
    b = {
        "wake_kind": "observation",
        "source_kinds": ["observation", "sensor"],
        "signal_kinds": ["progress", "stability"],
        "source_ids": ["b", "shared"],
    }
    c = {
        "wake_kind": "observation",
        "source_kinds": ["observation", "sensor"],
        "signal_kinds": ["repair", "stability"],
        "source_ids": ["c", "shared"],
    }
    target = {
        "wake_kind": "observation",
        "source_kinds": ["observation", "sensor"],
        "signal_kinds": ["progress", "repair", "stability"],
        "source_ids": ["a", "b", "c", "shared"],
    }
    atlas_bundle = empty_bundle("agent")
    atlas_bundle["charts"] = [
        observed("a", a, .70, .18, .12, "exploring"),
        observed("b", b, .18, .70, .12, "progressing"),
        observed("c", c, .18, .22, .60, "stabilizing"),
    ]
    atlas_bundle["atlas_bundle_digest"] = atlas_bundle_digest(atlas_bundle)
    plan = {
        "base_short_horizon_weight": .5,
        "base_medium_horizon_weight": .3,
        "base_long_horizon_weight": .2,
        "minimum_horizon_weight": .12,
        "minimum_chart_overlap": .5,
        "minimum_triple_overlap": .5,
        "minimum_quadruple_overlap": .5,
        "target_chart_retention": .7,
        "transition_phase_gain": .06,
        "plural_atlas_curvature_threshold": .08,
        "gerbe_local_retention": .7,
        "plural_gerbe_two_curvature_threshold": .2,
        "plural_higher_cocycle_threshold": .2,
    }
    atlas_decision = build_atlas_decision(
        atlas_run_id="atlas-parent-1",
        cycle_index=1,
        target_context_key="target",
        target_signature=target,
        atlas_bundle=atlas_bundle,
        plan=plan,
    )
    assert atlas_decision["compatible_chart_count"] == 3

    decision = build_gerbe_coherence(
        gerbe_run_id="gerbe-1",
        atlas_decision=atlas_decision,
        atlas_bundle=atlas_bundle,
        plan=plan,
    )
    assert decision["source_atlas_decision_digest"] == atlas_decision["atlas_decision_digest"]
    assert decision["source_atlas_bundle_digest"] == atlas_bundle["atlas_bundle_digest"]
    assert decision["compatible_chart_count"] == 3
    assert decision["two_cell_count"] == 3
    assert decision["quadruple_witness_count"] == 1
    assert decision["gerbe_two_curvature"] > 0.0
    assert decision["higher_cocycle_defect"] > 0.0
    assert all(cell["pairwise_transport_from_v0_13"] for cell in decision["two_cells"])
    assert all(witness["pairwise_transport_from_v0_13"] for witness in decision["quadruple_witnesses"])
    weights = [
        decision["lifted_base_short_horizon_weight"],
        decision["lifted_base_medium_horizon_weight"],
        decision["lifted_base_long_horizon_weight"],
    ]
    assert abs(sum(weights) - 1.0) < 1e-5 and min(weights) >= .12
    assert decision["gerbe_decision_digest"] == decision_digest(decision)
    assert decision["v0_13_decision_is_the_only_pairwise_transport_source"] is True
    assert decision["two_cell_residue_is_not_a_veto"] is True
    assert decision["higher_cocycle_defect_is_not_a_veto"] is True
    assert decision["global_trivialization_forbidden"] is True
    assert decision["v0_13_authority_preserved"] is True

    gerbe_bundle = empty_gerbe_bundle("agent")
    committed, replayed = commit_surface_cycle(previous=gerbe_bundle, decision=decision)
    assert replayed is False
    assert committed["generation"] == 1
    assert len(committed["surface_holonomy"]) == 1
    assert committed["last_atlas_decision_digest"] == atlas_decision["atlas_decision_digest"]
    assert committed["gerbe_bundle_digest"] == bundle_digest(committed)
    replay, replayed = commit_surface_cycle(previous=committed, decision=decision)
    assert replayed is True and replay == committed

    tampered = dict(atlas_decision)
    tampered["transported_short_weight"] = .99
    try:
        build_gerbe_coherence(
            gerbe_run_id="gerbe-tampered",
            atlas_decision=tampered,
            atlas_bundle=atlas_bundle,
            plan=plan,
        )
        raise AssertionError("tampered atlas decision was accepted")
    except ValueError as error:
        assert str(error) == "source_atlas_decision_digest_invalid"

    text = repr({"decision": decision, "bundle": committed}).lower()
    for token in ("'nodes'", "'edges'", "'graph'", "'dependencies'"):
        assert token not in text
    print("PASS: context gerbe coherence v0.14 kernel")


if __name__ == "__main__":
    main()
