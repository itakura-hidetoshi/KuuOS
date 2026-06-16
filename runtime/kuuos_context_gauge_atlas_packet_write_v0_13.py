from runtime.kuuos_context_gauge_atlas_pending_v0_13 import pending_record
from runtime.kuuos_context_gauge_atlas_types_v0_13 import append_jsonl, write_json


def write_packets(data):
    if data["blockers"] or data["pending"] is not None:
        return data
    p = data["paths"]
    write_json(p["atlas_decision"], data["decision"])
    write_json(p["atlas_child_plan"], data["local_plan"])
    write_json(p["atlas_child_license"], data["local_license"])
    append_jsonl(p["atlas_ledger"], pending_record(packet_id=data["packet_id"], atlas_run_id=data["run_id"], plan=data["plan"], source_batch_digest=data["source_batch"], previous_state_digest=data["atlas_state"].get("atlas_state_digest", ""), previous_bundle_digest=data["atlas_bundle"].get("atlas_bundle_digest", ""), decision=data["decision"], local_plan=data["local_plan"], cycle_index=data["cycle_index"]))
    return data
