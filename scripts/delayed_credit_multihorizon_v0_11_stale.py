from scripts.delayed_credit_multihorizon_v0_11_runner import execute, jsonl, read
from scripts.delayed_credit_multihorizon_v0_11_test_support import initial_horizon, source

def check_stale(runtime_root, root, registry, snap4):
    stale_current = dict(snap4)
    stale_current["horizon_bundle"] = initial_horizon()
    before = len(jsonl(runtime_root / "execution_ledger.jsonl"))
    _, stale = execute(runtime_root, "horizon-stale", [source("horizon-stale")], root, registry, stale_current)
    assert stale.status.endswith("BLOCKED")
    assert "horizon_plan_expected_previous_horizon_bundle_digest_mismatch" in stale.blockers
    assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == before
    assert read(runtime_root / "kuuos_delayed_credit_multihorizon_bundle_v0_11.json")["generation"] == 4
