from runtime.kuuos_delayed_credit_multihorizon_core_v0_11 import build_delayed_credit_multihorizon
from scripts.delayed_credit_multihorizon_v0_11_runner import execute, jsonl, seed, snapshots
from scripts.delayed_credit_multihorizon_v0_11_test_support import horizon_context, license_packet, source

def first_two(runtime_root, root, registry):
    seed_result, portfolio, current = seed(runtime_root, root, registry)
    assert seed_result.live_adapter_id == "adapter-a"
    sources1 = [source("horizon-event-001")]
    plan1, first = execute(runtime_root, "horizon-001", sources1, root, registry, current)
    assert first.status.endswith("READY"), first.blockers
    assert first.child_policy_mode == "experiment"
    assert first.short_experiment_credit > 0.0
    assert first.medium_experiment_credit > 0.0
    snap1 = snapshots(runtime_root, portfolio)
    rows = len(jsonl(runtime_root / "execution_ledger.jsonl"))
    replay = build_delayed_credit_multihorizon(
        runtime_context=horizon_context(runtime_root), source_packets=sources1,
        root_principles_packet=root, adapter_registry=registry,
        horizon_plan=plan1,
        horizon_license=license_packet(plan1, sources1, root, registry,
            current["regret_bundle"]["regret_bundle_digest"],
            current["horizon_bundle"]["horizon_bundle_digest"]),
    )
    assert replay.status.endswith("REPLAYED")
    assert replay.idempotent_replay is True
    assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == rows
    _, second = execute(runtime_root, "horizon-002", [source("horizon-event-002")], root, registry, snap1)
    assert second.status.endswith("READY"), second.blockers
    assert second.child_policy_mode == "reobserve"
    assert second.adapted_base_experiment_threshold < 0.6
    assert second.medium_reobserve_credit > 0.0
    assert second.long_reobserve_credit > 0.0
    return portfolio, snapshots(runtime_root, portfolio)
