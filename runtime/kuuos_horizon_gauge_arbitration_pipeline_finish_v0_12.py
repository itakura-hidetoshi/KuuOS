from runtime.kuuos_horizon_gauge_arbitration_audit_store_v0_12 import persist_audit
from runtime.kuuos_horizon_gauge_arbitration_child_phase_v0_12 import run_child
from runtime.kuuos_horizon_gauge_arbitration_commit_compute_v0_12 import compute_commit
from runtime.kuuos_horizon_gauge_arbitration_commit_write_v0_12 import write_commit
from runtime.kuuos_horizon_gauge_arbitration_finalize_state_v0_12 import finalize_state
from runtime.kuuos_horizon_gauge_arbitration_receipt_build_v0_12 import receipt_for
from runtime.kuuos_horizon_gauge_arbitration_receipt_store_v0_12 import persist_receipt
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import BLOCKED, READY

def finish_pipeline(data):
    for step in (run_child, compute_commit, write_commit):
        data = step(data)
    status = READY if not data["blockers"] else BLOCKED
    if status == READY:
        data = finalize_state(data)
    receipt = receipt_for(data, status)
    persist_receipt(data, receipt)
    persist_audit(data, receipt)
    data["final_status"] = status
    return data
