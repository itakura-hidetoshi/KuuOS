from runtime.kuuos_context_gauge_atlas_record_v0_13 import committed_record
from runtime.kuuos_context_gauge_atlas_state_v0_13 import build_state
from runtime.kuuos_context_gauge_atlas_types_v0_13 import append_jsonl, write_json


def finalize_state(data):
    if data["blockers"]:
        return data
    current = data["atlas_state"]
    updated = data["updated_atlas_bundle"]
    if current.get("atlas_run_id") == data["run_id"] and current.get("atlas_bundle_digest") == updated.get("atlas_bundle_digest"):
        state = current
    else:
        state = build_state(
            previous=current, atlas_run_id=data["run_id"],
            cycle_index=data["cycle_index"], decision=data["decision"],
            outcome=data["atlas_outcome"], atlas_bundle=updated)
        write_json(data["paths"]["atlas_state"], state)
    row = committed_record(
        packet_id=data["packet_id"], atlas_run_id=data["run_id"],
        plan=data["plan"], cycle_index=data["cycle_index"],
        decision=data["decision"], outcome=data["atlas_outcome"],
        atlas_bundle=updated, state=state)
    append_jsonl(data["paths"]["atlas_ledger"], row)
    data["new_atlas_state"] = state
    return data
