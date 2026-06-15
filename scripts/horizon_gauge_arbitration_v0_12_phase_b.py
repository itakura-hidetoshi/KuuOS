from scripts.horizon_gauge_arbitration_v0_12_execute import execute
from scripts.horizon_gauge_arbitration_v0_12_snapshots import snapshots
from scripts.horizon_gauge_arbitration_v0_12_test_support import source

def run_phase_b(runtime_root, root, registry, portfolio, snap2):
    _, third = execute(runtime_root, "arbitration-003", [source("arbitration-event-003")], root, registry, snap2)
    assert third.status.endswith("READY"), third.blockers
    assert third.child_policy_mode == "exploit"
    assert third.arbitration_curvature >= 0.0
    assert min(third.transported_short_weight, third.transported_medium_weight, third.transported_long_weight) >= 0.12
    snap3 = snapshots(runtime_root, portfolio)
    _, fourth = execute(runtime_root, "arbitration-004", [source("arbitration-event-004")], root, registry, snap3)
    assert fourth.status.endswith("READY"), fourth.blockers
    assert fourth.child_policy_mode == "exploit"
    snap4 = snapshots(runtime_root, portfolio)
    bundle = snap4["arbitration_bundle"]
    section = bundle["sections"][0]
    assert bundle["generation"] == 4
    assert len(bundle["arbitration_holonomy"]) == 4
    assert len(bundle["outcomes"]) == 4
    assert len(bundle["processed_child_horizon_outcome_digests"]) == 4
    assert len(bundle["processed_child_effect_digests"]) == 4
    assert section["cycle_count"] == 4
    assert section["aligned_cycle_count"] + section["plural_cycle_count"] == 4
    assert section["cumulative_curvature"] >= 0.0
    state = snap4["arbitration_state"]
    assert state["total_cycles"] == 4
    assert state["total_aligned_cycles"] + state["total_plural_cycles"] == 4
    assert state["multiple_child_cycle_count"] == 0
    assert state["winner_take_all_collapse_count"] == 0
    assert state["hard_gate_bypass_count"] == 0
    assert snap4["experiment_bundle"]["total_trial_count"] == 1
    assert snap4["experiment_bundle"]["trial_budget_spent"] == 0.2
    return snap4
