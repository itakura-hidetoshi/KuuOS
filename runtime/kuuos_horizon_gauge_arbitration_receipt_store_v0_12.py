from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import write_json

def persist_receipt(data, receipt):
    if data["license"].get("receipt_write_allowed") is True:
        write_json(data["paths"]["receipt"], receipt)
