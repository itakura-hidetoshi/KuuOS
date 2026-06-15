from runtime.kuuos_horizon_gauge_arbitration_packet_build_v0_12 import build_packets
from runtime.kuuos_horizon_gauge_arbitration_packet_write_v0_12 import write_packets
from runtime.kuuos_horizon_gauge_arbitration_pending_append_v0_12 import append_pending
from runtime.kuuos_horizon_gauge_arbitration_prepare_base_v0_12 import prepare_base
from runtime.kuuos_horizon_gauge_arbitration_prepare_guard_basic_v0_12 import apply_basic_guards
from runtime.kuuos_horizon_gauge_arbitration_prepare_guard_digest_v0_12 import apply_digest_guards
from runtime.kuuos_horizon_gauge_arbitration_prepare_identity_v0_12 import attach_identity

def start_pipeline(kwargs):
    data = prepare_base(**kwargs)
    if data["replay"] is not None:
        return data
    for step in (apply_basic_guards, apply_digest_guards, attach_identity, build_packets, write_packets, append_pending):
        data = step(data)
    data.setdefault("child_result", {})
    data.setdefault("outcome", {})
    data.setdefault("updated_bundle", data["bundle"])
    return data
