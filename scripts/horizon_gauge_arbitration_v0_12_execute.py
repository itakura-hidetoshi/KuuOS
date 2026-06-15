from runtime.kuuos_horizon_gauge_arbitration_core_v0_12 import build_horizon_gauge_arbitration
from scripts.horizon_gauge_arbitration_v0_12_test_support import arbitration_context, license_packet, plan

def execute(runtime_root, run_id, sources, root, registry, current):
    packet = plan(run_id, sources, root, registry, current)
    result = build_horizon_gauge_arbitration(
        runtime_context=arbitration_context(runtime_root),
        source_packets=sources,
        root_principles_packet=root,
        adapter_registry=registry,
        arbitration_plan=packet,
        arbitration_license=license_packet(packet, sources, root, registry, current),
    )
    return packet, result
