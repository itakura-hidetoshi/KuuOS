import pathlib
from scripts.delayed_credit_multihorizon_v0_11_runner import read, seed, snapshots as horizon_snapshots
from scripts.horizon_gauge_arbitration_v0_12_test_support import initial_arbitration

def snapshots(runtime_root: pathlib.Path, portfolio):
    result = horizon_snapshots(runtime_root, portfolio)
    state_path = runtime_root / "kuuos_horizon_gauge_arbitration_state_v0_12.json"
    bundle_path = runtime_root / "kuuos_horizon_gauge_arbitration_bundle_v0_12.json"
    result["arbitration_state"] = read(state_path) if state_path.is_file() else {}
    result["arbitration_bundle"] = read(bundle_path) if bundle_path.is_file() else initial_arbitration()
    return result

def seed_current(runtime_root, root, registry):
    seed_result, portfolio, current = seed(runtime_root, root, registry)
    current["arbitration_state"] = {}
    current["arbitration_bundle"] = initial_arbitration()
    return seed_result, portfolio, current
