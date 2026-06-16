from runtime.kuuos_context_gauge_atlas_decision_v0_13 import build_atlas_decision
from runtime.kuuos_context_gauge_atlas_lift_license_v0_13 import build_local_license
from runtime.kuuos_context_gauge_atlas_lift_plan_v0_13 import build_local_plan
from runtime.kuuos_context_gauge_atlas_recovery_v0_13 import load_pending_packets


def build_packets(data):
    if data["blockers"]:
        return data
    if data["pending"] is not None:
        decision, local_plan, local_license = load_pending_packets(atlas_run_id=data["run_id"], pending=data["pending"], paths=data["paths"], blockers=data["blockers"])
    else:
        decision = build_atlas_decision(atlas_run_id=data["run_id"], cycle_index=data["cycle_index"], target_context_key=data["context_key"], target_signature=data["context_signature"], atlas_bundle=data["atlas_bundle"], plan=data["plan"])
        local_plan = build_local_plan(atlas_plan=data["plan"], decision=decision, sources=data["sources"], root_packet=data["root_packet"], registry=data["registry"], current=data["current"])
        local_license = build_local_license(local_plan=local_plan, sources=data["sources"], root_packet=data["root_packet"], registry=data["registry"], current=data["current"])
    data.update({"decision": decision, "local_plan": local_plan, "local_license": local_license})
    return data
