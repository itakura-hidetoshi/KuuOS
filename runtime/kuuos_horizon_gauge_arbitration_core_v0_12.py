from runtime.kuuos_horizon_gauge_arbitration_pipeline_start_v0_12 import start_pipeline
from runtime.kuuos_horizon_gauge_arbitration_pipeline_finish_v0_12 import finish_pipeline
from runtime.kuuos_horizon_gauge_arbitration_result_v0_12 import result_packet

def build_horizon_gauge_arbitration(**kwargs):
    data = start_pipeline(kwargs)
    if data["replay"] is not None:
        return data["replay"]
    data = finish_pipeline(data)
    return result_packet(status=data["final_status"], packet_id=data["packet_id"], run_id=data["run_id"], cycle_index=data["cycle_index"], root=data["root"], decision=data.get("decision", {}), outcome=data.get("outcome", {}), arbitration_bundle=data.get("updated_bundle", data["bundle"]), child_result=data.get("child_result", {}), recovered_pending=data["recovered_pending"], paths=data["paths"], blockers=data["blockers"], warnings=data["warnings"])
