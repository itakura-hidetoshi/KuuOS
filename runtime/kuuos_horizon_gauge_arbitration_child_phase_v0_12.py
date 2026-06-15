from runtime.kuuos_horizon_gauge_arbitration_child_execute_v0_12 import execute_child

def run_child(data):
    if data["blockers"]:
        return data
    result, bundle, outcome, gauge = execute_child(
        root=data["root"], context=data["context"], sources=data["sources"],
        root_packet=data["root_packet"], registry=data["registry"],
        child_plan=data["child_plan"], child_license=data["child_license"],
        paths=data["paths"], blockers=data["blockers"])
    data["child_result"] = result
    data["child_horizon_bundle"] = bundle
    data["child_horizon_outcome"] = outcome
    data["current_gauge_bundle"] = gauge
    return data
