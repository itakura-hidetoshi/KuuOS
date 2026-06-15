from runtime.kuuos_horizon_gauge_arbitration_receipt_v0_12 import build_receipt

def receipt_for(data, status):
    return build_receipt(status=status, packet_id=data["packet_id"], run_id=data["run_id"], cycle_index=data["cycle_index"], decision=data.get("decision", {}), outcome=data.get("outcome", {}), arbitration_bundle=data.get("updated_bundle", data["bundle"]), child_result=data.get("child_result", {}), blockers=data["blockers"], warnings=data["warnings"])
