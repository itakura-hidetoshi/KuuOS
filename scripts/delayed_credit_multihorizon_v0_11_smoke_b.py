from scripts.delayed_credit_multihorizon_v0_11_runner import execute, no_graph, snapshots
from scripts.delayed_credit_multihorizon_v0_11_test_support import source

def last_two(runtime_root, root, registry, portfolio, snap2):
    _, third = execute(runtime_root, "horizon-003", [source("horizon-event-003")], root, registry, snap2)
    assert third.status.endswith("READY"), third.blockers
    assert third.child_policy_mode == "exploit"
    assert third.child_live_domain_action == "advance_tick"
    assert third.long_exploit_credit > 0.0
    snap3 = snapshots(runtime_root, portfolio)
    _, fourth = execute(runtime_root, "horizon-004", [source("horizon-event-004")], root, registry, snap3)
    assert fourth.status.endswith("READY"), fourth.blockers
    assert fourth.child_policy_mode == "exploit"
    snap4 = snapshots(runtime_root, portfolio)
    section = snap4["horizon_bundle"]["sections"][0]
    assert section["cycle_count"] == 4
    assert section["short_cycle_count"] == 4
    assert section["medium_cycle_count"] == 4
    assert section["long_cycle_count"] == 3
    assert section["cumulative_commitment_progress"] > 0.0
    assert section["cumulative_recovery_cost"] > 0.0
    assert section["long_exploit_credit"] > 0.0
    assert snap4["horizon_bundle"]["generation"] == 4
    assert len(snap4["horizon_bundle"]["processed_child_regret_outcome_digests"]) == 4
    assert len(snap4["horizon_bundle"]["processed_child_effect_digests"]) == 4
    state = snap4["horizon_state"]
    assert state["total_experiment_children"] == 1
    assert state["total_reobserve_children"] == 1
    assert state["total_exploit_children"] == 2
    assert state["effectless_credit_update_count"] == 0
    assert state["hard_gate_bypass_count"] == 0
    assert snap4["experiment_bundle"]["trial_budget_spent"] == 0.2
    no_graph(snap4["horizon_bundle"])
    return snap4
