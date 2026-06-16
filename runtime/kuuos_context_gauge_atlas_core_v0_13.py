from runtime.kuuos_context_gauge_atlas_commit_compute_v0_13 import compute_commit
from runtime.kuuos_context_gauge_atlas_commit_write_v0_13 import write_commit
from runtime.kuuos_context_gauge_atlas_finalize_receipt_v0_13 import finalize_receipt
from runtime.kuuos_context_gauge_atlas_finalize_state_v0_13 import finalize_state
from runtime.kuuos_context_gauge_atlas_local_phase_v0_13 import run_local_cycle
from runtime.kuuos_context_gauge_atlas_packet_build_v0_13 import build_packets
from runtime.kuuos_context_gauge_atlas_packet_write_v0_13 import write_packets
from runtime.kuuos_context_gauge_atlas_prepare_v0_13 import prepare_atlas
from runtime.kuuos_context_gauge_atlas_result_v0_13 import result_packet
from runtime.kuuos_context_gauge_atlas_types_v0_13 import BLOCKED, READY


def build_context_gauge_atlas(**kwargs):
    data = prepare_atlas(**kwargs)
    if data["replay"] is not None:
        return data["replay"]
    data = build_packets(data)
    data = write_packets(data)
    data.setdefault("local_result", {})
    data.setdefault("local_outcome", {})
    data.setdefault("atlas_outcome", {})
    data.setdefault("updated_atlas_bundle", data["atlas_bundle"])
    data = run_local_cycle(data)
    data = compute_commit(data)
    data = write_commit(data)
    status = READY if not data["blockers"] else BLOCKED
    if status == READY:
        data = finalize_state(data)
    data = finalize_receipt(data, status)
    return result_packet(
        status=status, packet_id=data["packet_id"],
        atlas_run_id=data["run_id"], cycle_index=data["cycle_index"],
        root=data["root"], decision=data.get("decision", {}),
        outcome=data.get("atlas_outcome", {}),
        atlas_bundle=data.get("updated_atlas_bundle", data["atlas_bundle"]),
        recovered_pending=data["recovered_pending"], paths=data["paths"],
        blockers=data["blockers"], warnings=data["warnings"])
