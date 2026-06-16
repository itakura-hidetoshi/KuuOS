from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_types_v0_13 import REPLAYED, VERSION, ContextGaugeAtlasResult, integer


def _float(value: Mapping[str, Any], field: str) -> float:
    try:
        return float(value.get(field, 0.0))
    except (TypeError, ValueError):
        return 0.0


def result_packet(*, status: str, packet_id: str, atlas_run_id: str, cycle_index: int, root: Any, decision: Mapping[str, Any], outcome: Mapping[str, Any], atlas_bundle: Mapping[str, Any], recovered_pending: bool, paths: Mapping[str, Any], blockers: list[str], warnings: list[str], replay: bool = False) -> ContextGaugeAtlasResult:
    return ContextGaugeAtlasResult(
        version=VERSION,
        status=status,
        packet_id=packet_id,
        atlas_run_id=atlas_run_id,
        cycle_index=cycle_index,
        runtime_root=str(root),
        target_context_key=str(decision.get("target_context_key", "")),
        atlas_class=str(decision.get("atlas_class", "")),
        compatible_chart_count=integer(decision.get("compatible_chart_count"), 0),
        atlas_curvature=_float(decision, "atlas_curvature"),
        cocycle_defect=_float(decision, "cocycle_defect"),
        transported_short_weight=_float(decision, "transported_short_weight"),
        transported_medium_weight=_float(decision, "transported_medium_weight"),
        transported_long_weight=_float(decision, "transported_long_weight"),
        child_arbitration_class=str(outcome.get("child_arbitration_class", "")),
        child_commitment_outcome_class=str(outcome.get("child_commitment_outcome_class", "")),
        child_policy_mode=str(outcome.get("child_policy_mode", "")),
        child_live_adapter_id=str(outcome.get("child_live_adapter_id", "")),
        child_live_domain_action=str(outcome.get("child_live_domain_action", "")),
        atlas_bundle_digest=str(atlas_bundle.get("atlas_bundle_digest", "")),
        child_arbitration_bundle_digest=str(outcome.get("child_arbitration_bundle_digest", "")),
        child_arbitration_outcome_digest=str(outcome.get("child_arbitration_outcome_digest", "")),
        child_effect_receipt_digest=str(outcome.get("child_effect_receipt_digest", "")),
        idempotent_replay=replay,
        recovered_pending_run=recovered_pending,
        state_path=str(paths["atlas_state"]),
        bundle_path=str(paths["atlas_bundle"]),
        decision_path=str(paths["atlas_decision"]),
        outcome_path=str(paths["atlas_outcome"]),
        child_plan_path=str(paths["atlas_child_plan"]),
        child_license_path=str(paths["atlas_child_license"]),
        receipt_path=str(paths["atlas_receipt"]),
        ledger_path=str(paths["atlas_ledger"]),
        audit_path=str(paths["atlas_audit"]),
        blockers=blockers,
        warnings=warnings,
    )


def replay_result(row: Mapping[str, Any], root: Any, paths: Mapping[str, Any]) -> ContextGaugeAtlasResult:
    decision = dict(row)
    outcome = dict(row)
    bundle = {"atlas_bundle_digest": row.get("atlas_bundle_digest", "")}
    return result_packet(status=REPLAYED, packet_id=str(row.get("packet_id", "")), atlas_run_id=str(row.get("atlas_run_id", "")), cycle_index=integer(row.get("cycle_index"), 0), root=root, decision=decision, outcome=outcome, atlas_bundle=bundle, recovered_pending=False, paths=paths, blockers=[], warnings=["atlas_run_replay_no_new_local_cycle_or_transport"], replay=True)
