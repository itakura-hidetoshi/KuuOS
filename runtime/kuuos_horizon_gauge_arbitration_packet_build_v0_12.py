#!/usr/bin/env python3
from runtime.kuuos_horizon_gauge_arbitration_child_license_v0_12 import build_child_horizon_license
from runtime.kuuos_horizon_gauge_arbitration_child_plan_v0_12 import build_child_horizon_plan
from runtime.kuuos_horizon_gauge_arbitration_decision_v0_12 import build_arbitration_decision
from runtime.kuuos_horizon_gauge_arbitration_recovery_load_v0_12 import load_recovery_packets


def build_packets(data):
    if data["blockers"]:
        return data
    if data["pending"] is not None:
        decision, child_plan, child_license = load_recovery_packets(
            run_id=data["run_id"],
            pending=data["pending"],
            paths=data["paths"],
            blockers=data["blockers"],
        )
    else:
        decision = build_arbitration_decision(
            arbitration_run_id=data["run_id"],
            cycle_index=data["cycle_index"],
            context_key=data["context_key"],
            horizon_bundle=data["values"]["horizon_bundle"],
            arbitration_bundle=data["bundle"],
            gauge_bundle=data["values"]["gauge_bundle"],
            plan=data["plan"],
        )
        child_plan = build_child_horizon_plan(
            arbitration_plan=data["plan"],
            decision=decision,
            source_packets=data["sources"],
            root_packet=data["root_packet"],
            adapter_registry=data["registry"],
            upstream=data["upstream"],
        )
        child_license = build_child_horizon_license(
            child_plan=child_plan,
            source_packets=data["sources"],
            root_packet=data["root_packet"],
            adapter_registry=data["registry"],
            upstream=data["upstream"],
        )
    data.update({"decision": decision, "child_plan": child_plan, "child_license": child_license})
    return data
