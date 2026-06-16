from runtime.kuuos_context_gauge_atlas_receipt_v0_13 import build_receipt
from runtime.kuuos_context_gauge_atlas_types_v0_13 import append_jsonl, sha, write_json


def finalize_receipt(data, status):
    receipt = build_receipt(
        status=status, packet_id=data["packet_id"],
        atlas_run_id=data["run_id"], cycle_index=data["cycle_index"],
        decision=data.get("decision", {}), outcome=data.get("atlas_outcome", {}),
        atlas_bundle=data.get("updated_atlas_bundle", data["atlas_bundle"]),
        blockers=data["blockers"], warnings=data["warnings"])
    if data["license"].get("receipt_write_allowed") is True:
        write_json(data["paths"]["atlas_receipt"], receipt)
    if data["license"].get("audit_append_allowed") is True:
        record = dict(receipt)
        record["audit_record_digest"] = sha(receipt)
        append_jsonl(data["paths"]["atlas_audit"], record)
    data["receipt"] = receipt
    return data
