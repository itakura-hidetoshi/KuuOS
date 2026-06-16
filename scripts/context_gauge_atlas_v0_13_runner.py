import pathlib
from runtime.kuuos_context_gauge_atlas_core_v0_13 import build_context_gauge_atlas
from scripts.delayed_credit_multihorizon_v0_11_runner import read
from scripts.horizon_gauge_arbitration_v0_12_snapshots import seed_current as local_seed_current, snapshots as local_snapshots
from scripts.context_gauge_atlas_v0_13_test_support import atlas_context, initial_atlas, license_packet, plan


def seed_current(runtime_root, root, registry):
    result, portfolio, current = local_seed_current(runtime_root, root, registry)
    current["atlas_state"] = {}
    current["atlas_bundle"] = initial_atlas()
    return result, portfolio, current


def snapshots(runtime_root: pathlib.Path, portfolio):
    current = local_snapshots(runtime_root, portfolio)
    state_path = runtime_root / "kuuos_context_gauge_atlas_state_v0_13.json"
    bundle_path = runtime_root / "kuuos_context_gauge_atlas_bundle_v0_13.json"
    current["atlas_state"] = read(state_path) if state_path.is_file() else {}
    current["atlas_bundle"] = read(bundle_path) if bundle_path.is_file() else initial_atlas()
    return current


def execute(runtime_root, run_id, sources, root, registry, current):
    packet = plan(run_id, sources, root, registry, current)
    result = build_context_gauge_atlas(
        runtime_context=atlas_context(runtime_root),
        source_packets=sources,
        root_principles_packet=root,
        adapter_registry=registry,
        atlas_plan=packet,
        atlas_license=license_packet(packet, sources, root, registry, current),
    )
    return packet, result
