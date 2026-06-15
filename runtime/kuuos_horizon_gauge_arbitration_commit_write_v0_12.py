from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import write_json

def write_commit(data):
    if data["blockers"]:
        return data
    write_json(data["paths"]["outcome"], data["outcome"])
    write_json(data["paths"]["bundle"], data["updated_bundle"])
    return data
