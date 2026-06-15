from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import append_jsonl, sha

def persist_audit(data, receipt):
    if data["license"].get("audit_append_allowed") is True:
        record = dict(receipt)
        record["audit_record_digest"] = sha(receipt)
        append_jsonl(data["paths"]["audit"], record)
