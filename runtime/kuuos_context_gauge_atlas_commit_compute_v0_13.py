from runtime.kuuos_context_gauge_atlas_bundle_update_v0_13 import commit_atlas
from runtime.kuuos_context_gauge_atlas_outcome_v0_13 import build_outcome


def compute_commit(data):
    data["atlas_outcome"] = {}
    data["updated_atlas_bundle"] = data["atlas_bundle"]
    if data["blockers"]:
        return data
    outcome = build_outcome(
        atlas_run_id=data["run_id"], cycle_index=data["cycle_index"],
        decision=data["decision"], local_result=data["local_result"],
        local_outcome=data["local_outcome"])
    updated, duplicate = commit_atlas(
        previous=data["atlas_bundle"], decision=data["decision"],
        outcome=outcome, plan=data["plan"])
    if duplicate:
        data["warnings"].append("local_outcome_already_committed_to_atlas")
    data["atlas_outcome"] = outcome
    data["updated_atlas_bundle"] = updated
    return data
