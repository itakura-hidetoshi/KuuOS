from scripts.delayed_credit_multihorizon_v0_11_runner import jsonl, read
from scripts.horizon_gauge_arbitration_v0_12_execute import execute
from scripts.horizon_gauge_arbitration_v0_12_test_support import initial_arbitration, source

def check_stale(runtime_root, root, registry, snap4):
    stale_current = dict(snap4)
    stale_current["arbitration_bundle"] = initial_arbitration()
    before = len(jsonl(runtime_root / "execution_ledger.jsonl"))
    _, stale = execute(runtime_root, "arbitration-stale", [source("arbitration-stale")], root, registry, stale_current)
    assert stale.status.endswith("BLOCKED")
    assert "arbitration_plan_expected_previous_arbitration_bundle_digest_mismatch" in stale.blockers
    assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == before
    bundle = read(runtime_root / "kuuos_horizon_gauge_arbitration_bundle_v0_12.json")
    assert bundle["generation"] == 4
