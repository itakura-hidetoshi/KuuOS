#!/usr/bin/env python3
from runtime.kuuos_context_gauge_atlas_basis_v0_13 import empty_bundle, initial_chart
from runtime.kuuos_context_gauge_atlas_decision_v0_13 import build_atlas_decision
from runtime.kuuos_context_gauge_atlas_types_v0_13 import decision_digest


def observed(key, signature, short, medium, long, outcome):
    packet = initial_chart(key, signature)
    packet.update({"cycle_count": 1, "last_short_weight": short, "last_medium_weight": medium, "last_long_weight": long, "last_commitment_outcome_class": outcome})
    return packet


def main():
    a = {"wake_kind": "observation", "source_kinds": ["observation"], "signal_kinds": ["progress"], "source_ids": ["a"]}
    b = {"wake_kind": "observation", "source_kinds": ["observation"], "signal_kinds": ["progress"], "source_ids": ["b"]}
    target = {"wake_kind": "observation", "source_kinds": ["observation"], "signal_kinds": ["progress"], "source_ids": ["a", "b"]}
    bundle = empty_bundle("agent")
    bundle["charts"] = [observed("a", a, .70, .20, .10, "exploring"), observed("b", b, .15, .25, .60, "stabilizing")]
    plan = {"base_short_horizon_weight": .5, "base_medium_horizon_weight": .3, "base_long_horizon_weight": .2, "minimum_horizon_weight": .12, "minimum_chart_overlap": .5, "target_chart_retention": .7, "transition_phase_gain": .06, "plural_atlas_curvature_threshold": .08}
    decision = build_atlas_decision(atlas_run_id="atlas-1", cycle_index=1, target_context_key="target", target_signature=target, atlas_bundle=bundle, plan=plan)
    assert decision["compatible_chart_count"] == 2
    assert decision["atlas_curvature"] > 0
    assert decision["cocycle_defect"] > 0
    weights = [decision["transported_short_weight"], decision["transported_medium_weight"], decision["transported_long_weight"]]
    assert abs(sum(weights) - 1) < 1e-5 and min(weights) >= .12
    assert decision["atlas_decision_digest"] == decision_digest(decision)
    text = repr(decision).lower()
    for token in ("'nodes'", "'edges'", "'graph'", "'dependencies'"):
        assert token not in text
    print("PASS: context gauge atlas v0.13 kernel")


if __name__ == "__main__":
    main()
