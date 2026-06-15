import pathlib, tempfile
from scripts.delayed_credit_multihorizon_v0_11_runner import jsonl, no_graph, read
from scripts.horizon_gauge_arbitration_v0_12_phase_a_fixed import run_phase_a
from scripts.horizon_gauge_arbitration_v0_12_phase_b import run_phase_b
from scripts.horizon_gauge_arbitration_v0_12_stale import check_stale
from scripts.horizon_gauge_arbitration_v0_12_test_support import experiment_registry, root_packet

def run_scenario():
    with tempfile.TemporaryDirectory() as directory:
        runtime_root = pathlib.Path(directory)
        root = root_packet()
        registry = experiment_registry()
        portfolio, snap2 = run_phase_a(runtime_root, root, registry)
        snap4 = run_phase_b(runtime_root, root, registry, portfolio, snap2)
        check_stale(runtime_root, root, registry, snap4)
        rows = jsonl(runtime_root / "kuuos_horizon_gauge_arbitration_ledger_v0_12.jsonl")
        committed = [row for row in rows if row.get("phase") == "committed"]
        assert [row["child_policy_mode"] for row in committed] == ["experiment", "reobserve", "exploit", "exploit"]
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 5
        assert read(runtime_root / "runtime_state.json")["tick"] == 4
        no_graph(snap4["arbitration_bundle"])
    return 0
