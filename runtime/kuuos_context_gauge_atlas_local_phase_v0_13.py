from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, read_json
from runtime.kuuos_horizon_gauge_arbitration_core_v0_12 import build_horizon_gauge_arbitration
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import READY, REPLAYED


def run_local_cycle(data):
    if data["blockers"]:
        data.update({"local_result": {}, "local_outcome": {}})
        return data
    child = build_horizon_gauge_arbitration(
        runtime_context={
            "runtime_root": str(data["root"]),
            "horizon_gauge_arbitration_enabled": True,
            "execute_one_arbitration_cycle": True,
            "allowed_domain_actions": as_list(data["context"].get("allowed_domain_actions")),
        },
        source_packets=data["sources"],
        root_principles_packet=data["root_packet"],
        adapter_registry=data["registry"],
        arbitration_plan=data["local_plan"],
        arbitration_license=data["local_license"],
    )
    result = child.to_dict()
    if child.status not in {READY, REPLAYED}:
        data["blockers"].extend([f"local_{item}" for item in child.blockers])
    outcome = read_json(data["paths"]["outcome"])
    if not data["blockers"]:
        if not str(outcome.get("arbitration_outcome_digest", "")):
            data["blockers"].append("local_arbitration_outcome_missing")
        if outcome.get("child_effect_receipt_digest") != result.get("child_effect_receipt_digest"):
            data["blockers"].append("local_effect_receipt_digest_mismatch")
    data.update({"local_result": result, "local_outcome": outcome})
    return data
