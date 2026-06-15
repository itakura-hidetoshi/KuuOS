from runtime.kuuos_horizon_gauge_arbitration_record_v0_12 import committed_record
from runtime.kuuos_horizon_gauge_arbitration_state_base_v0_12 import recovery_state_base
from runtime.kuuos_horizon_gauge_arbitration_state_v0_12 import build_state
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import append_jsonl, write_json

def finalize_state(data):
    if data["blockers"]:
        return data
    state = build_state(
        previous_state=recovery_state_base(data),
        run_id=data["run_id"], cycle_index=data["cycle_index"],
        decision=data["decision"], outcome=data["outcome"],
        arbitration_bundle=data["updated_bundle"])
    row = committed_record(
        packet_id=data["packet_id"], run_id=data["run_id"], plan=data["plan"],
        cycle_index=data["cycle_index"], decision=data["decision"],
        outcome=data["outcome"], arbitration_bundle=data["updated_bundle"],
        child_result=data["child_result"], state=state)
    write_json(data["paths"]["state"], state)
    append_jsonl(data["paths"]["ledger"], row)
    data["new_state"] = state
    return data
