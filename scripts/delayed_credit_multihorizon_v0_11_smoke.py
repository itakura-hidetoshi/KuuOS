from scripts.delayed_credit_multihorizon_v0_11_runner import execute, seed, snapshots
from scripts.delayed_credit_multihorizon_v0_11_test_support import source

def first_two(runtime_root, root, registry):
    seed_result, portfolio, current = seed(runtime_root, root, registry)
    assert seed_result.live_adapter_id == "adapter-a"
    _, first = execute(runtime_root, "horizon-001", [source("horizon-event-001")], root, registry, current)
    assert first.status.endswith("READY"), first.blockers
    assert first.child_policy_mode == "experiment"
    assert first.short_experiment_credit > 0.0
    assert first.medium_experiment_credit > 0.0
    snap1 = snapshots(runtime_root, portfolio)
    _, second = execute(runtime_root, "horizon-002", [source("horizon-event-002")], root, registry, snap1)
    assert second.status.endswith("READY"), second.blockers
    assert second.child_policy_mode == "reobserve"
    assert second.adapted_base_experiment_threshold < 0.6
    assert second.medium_reobserve_credit > 0.0
    assert second.long_reobserve_credit > 0.0
    return portfolio, snapshots(runtime_root, portfolio)
