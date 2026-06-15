#!/usr/bin/env python3
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import write_json


def write_packets(data):
    if data["blockers"] or data["pending"] is not None:
        return data
    p = data["paths"]
    write_json(p["decision"], data["decision"])
    write_json(p["child_plan"], data["child_plan"])
    write_json(p["child_license"], data["child_license"])
    return data
