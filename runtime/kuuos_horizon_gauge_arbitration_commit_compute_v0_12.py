from runtime.kuuos_horizon_gauge_arbitration_commit_v0_12 import commit_arbitration_outcome

def compute_commit(data):
    data["outcome"] = {}
    data["updated_bundle"] = data["bundle"]
    if data["blockers"]:
        return data
    updated, outcome, replayed = commit_arbitration_outcome(
        arbitration_run_id=data["run_id"],
        cycle_index=data["cycle_index"],
        previous_bundle=data["bundle"],
        child_horizon_bundle=data["child_horizon_bundle"],
        child_horizon_outcome=data["child_horizon_outcome"],
        decision=data["decision"],
        gauge_bundle=data["current_gauge_bundle"],
        plan=data["plan"],
    )
    if replayed:
        data["warnings"].append("child_horizon_outcome_already_processed")
    data["outcome"] = outcome
    data["updated_bundle"] = updated
    return data
