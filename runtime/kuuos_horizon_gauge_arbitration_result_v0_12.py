#!/usr/bin/env python3
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import VERSION, HorizonGaugeArbitrationResult

DECISION_STR = ("consensus_mode", "short_dominant_mode", "medium_dominant_mode", "long_dominant_mode")
DECISION_FLOAT = ("short_medium_residual", "medium_long_residual", "short_long_residual", "arbitration_curvature", "transported_short_weight", "transported_medium_weight", "transported_long_weight")
OUTCOME_FLOAT = ("commitment_progress_score", "recovery_cost", "terminal_section_ratio")
PATH_FIELDS = ("state", "bundle", "decision", "outcome", "child_plan", "child_license", "receipt", "ledger", "audit")

def result_packet(*, status, packet_id, run_id, cycle_index, root, decision, outcome, arbitration_bundle, child_result, recovered_pending, paths, blockers, warnings):
    data = {
        "version": VERSION, "status": status, "packet_id": packet_id,
        "arbitration_run_id": run_id, "cycle_index": cycle_index,
        "runtime_root": str(root), "context_key": str(decision.get("context_key", "")),
        "arbitration_class": str(outcome.get("arbitration_class", decision.get("arbitration_class", ""))),
        "commitment_outcome_class": str(outcome.get("commitment_outcome_class", "")),
        "child_policy_mode": str(child_result.get("child_policy_mode", "")),
        "child_live_adapter_id": str(child_result.get("child_live_adapter_id", "")),
        "child_live_domain_action": str(child_result.get("child_live_domain_action", "")),
        "arbitration_bundle_digest": str(arbitration_bundle.get("arbitration_bundle_digest", "")),
        "child_horizon_bundle_digest": str(outcome.get("child_horizon_bundle_digest", "")),
        "child_horizon_outcome_digest": str(outcome.get("child_horizon_outcome_digest", "")),
        "child_effect_receipt_digest": str(outcome.get("child_effect_receipt_digest", "")),
        "idempotent_replay": False, "recovered_pending_run": recovered_pending,
        "blockers": blockers, "warnings": warnings,
    }
    data.update({field: str(decision.get(field, "")) for field in DECISION_STR})
    data.update({field: float(decision.get(field, 0.0)) for field in DECISION_FLOAT})
    data.update({field: float(outcome.get(field, 0.0)) for field in OUTCOME_FLOAT})
    for field in PATH_FIELDS:
        data[field + "_path"] = str(paths[field])
    return HorizonGaugeArbitrationResult(**data)
