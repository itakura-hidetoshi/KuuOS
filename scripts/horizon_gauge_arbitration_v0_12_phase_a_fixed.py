from runtime.kuuos_horizon_gauge_arbitration_core_v0_12 import build_horizon_gauge_arbitration
from scripts.delayed_credit_multihorizon_v0_11_runner import jsonl, read
from scripts.horizon_gauge_arbitration_v0_12_execute import execute
from scripts.horizon_gauge_arbitration_v0_12_snapshots import seed_current, snapshots
from scripts.horizon_gauge_arbitration_v0_12_test_support import arbitration_context, license_packet, source

def run_phase_a(runtime_root, root, registry):
    seed_result, portfolio, current = seed_current(runtime_root, root, registry)
    assert seed_result.live_adapter_id == "adapter-a"
    sources1 = [source("arbitration-event-001")]
    plan1, first = execute(runtime_root, "arbitration-001", sources1, root, registry, current)
    assert first.status.endswith("READY"), first.blockers
    assert first.child_policy_mode == "experiment"
    assert first.arbitration_class == "aligned_transport"
    assert first.arbitration_curvature == 0.0
    first_weights = (first.transported_short_weight, first.transported_medium_weight, first.transported_long_weight)
    assert abs(sum(first_weights) - 1.0) < 1e-5
    assert min(first_weights) >= 0.12
    snap1 = snapshots(runtime_root, portfolio)
    assert snap1["arbitration_bundle"]["generation"] == 1
    assert snap1["experiment_bundle"]["trial_budget_spent"] == 0.2
    rows = len(jsonl(runtime_root / "execution_ledger.jsonl"))
    replay = build_horizon_gauge_arbitration(runtime_context=arbitration_context(runtime_root), source_packets=sources1, root_principles_packet=root, adapter_registry=registry, arbitration_plan=plan1, arbitration_license=license_packet(plan1, sources1, root, registry, current))
    assert replay.status.endswith("REPLAYED")
    assert replay.idempotent_replay is True
    assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == rows
    _, second = execute(runtime_root, "arbitration-002", [source("arbitration-event-002")], root, registry, snap1)
    assert second.status.endswith("READY"), second.blockers
    assert second.child_policy_mode == "reobserve"
    assert second.arbitration_curvature > 0.0
    weights = (second.transported_short_weight, second.transported_medium_weight, second.transported_long_weight)
    assert abs(sum(weights) - 1.0) < 1e-5
    assert min(weights) >= 0.12
    assert any(abs(a - b) > 1e-6 for a, b in zip(weights, first_weights))
    child_plan = read(runtime_root / "kuuos_horizon_gauge_arbitration_child_plan_v0_12.json")
    assert child_plan["short_horizon_weight"] == second.transported_short_weight
    assert child_plan["medium_horizon_weight"] == second.transported_medium_weight
    assert child_plan["long_horizon_weight"] == second.transported_long_weight
    return portfolio, snapshots(runtime_root, portfolio)
