from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import integer

def recovery_state_base(data):
    state = data["state"]
    pending = data["pending"]
    if pending is None or state.get("arbitration_run_id") != data["run_id"]:
        return state
    outcome = data["outcome"]
    kind = str(outcome.get("commitment_outcome_class", "holding"))
    restored = dict(state)
    restored["arbitration_state_digest"] = pending.get("previous_arbitration_state_digest", "")
    restored["total_cycles"] = max(0, integer(state.get("total_cycles"), 1) - 1)
    transport_field = "total_plural_cycles" if outcome.get("arbitration_class") == "plural_transport" else "total_aligned_cycles"
    restored[transport_field] = max(0, integer(state.get(transport_field), 1) - 1)
    class_field = f"total_{kind}_cycles"
    restored[class_field] = max(0, integer(state.get(class_field), 1) - 1)
    return restored
