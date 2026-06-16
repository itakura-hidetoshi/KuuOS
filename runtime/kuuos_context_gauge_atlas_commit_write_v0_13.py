from runtime.kuuos_context_gauge_atlas_types_v0_13 import write_json


def write_commit(data):
    if data["blockers"]:
        return data
    write_json(data["paths"]["atlas_outcome"], data["atlas_outcome"])
    write_json(data["paths"]["atlas_bundle"], data["updated_atlas_bundle"])
    return data
