#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_world_real_hilbert_l2_analytic_spine_embedding_v0_26 import *

@dataclass(frozen=True)
class Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    spine_id: str
    analysis_run_id: str
    world_model_id: str
    decision: str
    coordinate_count: int
    norm_squared: float
    weighted_energy: float
    coercivity_lower_bound: float
    rayleigh_lower_bound_verified: bool
    source_world_state_digest: str
    world_l2_embedding_report_digest: str
    world_l2_spine_state_digest: str
    ledger_record_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def finalize_world_l2_spine(
    *,
    root: pathlib.Path,
    plan: Mapping[str, Any],
    license_value: Mapping[str, Any],
    report: Mapping[str, Any],
    source: Mapping[str, Any],
    coordinates: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    analysis: Mapping[str, Any],
    decision: str,
    reason: str,
    blockers: list[str],
    prior: list[dict[str, Any]],
    prior_state: Mapping[str, Any],
    report_sha: str,
    source_digest: str,
) -> Result:
    spine_id = str(plan.get("spine_id", ""))
    run_id = str(plan.get("analysis_run_id", ""))
    world_model_id = str(plan.get("world_model_id", ""))
    ledger_path = root / "indra_qi_world_real_hilbert_l2_analytic_spine_ledger_v0_26.jsonl"
    now = int(time.time())
    source_fields = {
        "source_world_state_digest": source_digest,
        "world_l2_embedding_report_digest": report_sha,
    }
    no_authority = {
        "direct_world_update_authority": False,
        "direct_external_actuation_authority": False,
        "direct_truth_authority": False,
        "direct_unbounded_operator_execution_authority": False,
        "direct_self_adjointness_theorem_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
    }
    state = {
        "version": STATE_VERSION,
        "spine_id": spine_id,
        "analysis_run_id": run_id,
        "world_model_id": world_model_id,
        **source_fields,
        "carrier": {
            "scalar_field": "real",
            "space_kind": "ell2_countable_real",
            "index_set_kind": "countable_feature_basis",
            "runtime_vector_kind": "finite_support_witness_in_ell2",
            "complete_real_hilbert_space_declared": True,
        },
        "representation_boundary": {
            "world_not_identified_with_hilbert_vector": True,
            "map_kind": "nonlinear_observation_embedding",
            "linear_required": False,
            "injective_required": False,
            "surjective_required": False,
            "multi_world_noncollapse_preserved": True,
            "two_truths_gap_preserved": True,
        },
        "coordinate_basis": coordinates,
        "diagnostic_projections": projections,
        "analytic_observables": analysis,
        "operator_template": dict(mapping(report.get("operator_template"))),
        "decision": decision,
        "decision_reason": reason,
        "recommendation_only": True,
        **no_authority,
        "prev_world_l2_spine_state_digest": str(
            prior_state.get("world_l2_spine_state_digest", "GENESIS")
        )
        if prior_state
        else "GENESIS",
        "epoch": now,
    }
    state["world_l2_spine_state_digest"] = state_digest(state)

    recommendation = {
        "version": RECOMMENDATION_VERSION,
        "spine_id": spine_id,
        "analysis_run_id": run_id,
        "world_model_id": world_model_id,
        **source_fields,
        "decision": decision,
        "decision_reasons": [reason],
        "analytic_spine_ready": decision == "world_l2_analytic_spine_ready",
        "analytic_observables": analysis,
        "recommendation_only": True,
        "runtime_validation_not_mathematical_theorem": True,
        "world_state_unchanged": True,
        **no_authority,
        "boundary": dict(REQUIRED_BOUNDARY),
        "epoch": now,
    }
    recommendation["world_l2_spine_recommendation_digest"] = sha(recommendation)

    ledger = {
        "version": LEDGER_VERSION,
        "record_type": "world_real_hilbert_l2_analytic_spine",
        "spine_id": spine_id,
        "analysis_run_id": run_id,
        "world_model_id": world_model_id,
        **source_fields,
        "decision": decision,
        "analytic_observables": analysis,
        "world_l2_spine_state_digest": state["world_l2_spine_state_digest"],
        "recommendation_only": True,
        "source_world_state_unchanged": True,
        **no_authority,
        "prev_record_digest": str(prior[-1].get("record_digest", "GENESIS")) if prior else "GENESIS",
        "epoch": now,
    }
    ledger["record_digest"] = sha(ledger)

    status = READY if not blockers else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "spine_id": spine_id,
        "analysis_run_id": run_id,
        "world_model_id": world_model_id,
        **source_fields,
        "decision": decision,
        "coordinate_count": int(analysis.get("coordinate_count", 0)),
        "norm_squared": number(analysis.get("norm_squared")),
        "weighted_energy": number(analysis.get("weighted_energy")),
        "coercivity_lower_bound": number(analysis.get("coercivity_lower_bound")),
        "rayleigh_lower_bound_verified": analysis.get("rayleigh_lower_bound_verified") is True,
        "world_l2_spine_state_digest": state["world_l2_spine_state_digest"] if not blockers else "",
        "ledger_record_digest": ledger["record_digest"] if not blockers else "",
        "blockers": blockers,
        "source_world_state_unchanged": True,
        "recommendation_only": True,
        **no_authority,
        "epoch": now,
    }
    receipt["packet_id"] = "indra-qi-world-real-hilbert-l2-spine-" + sha(receipt)[:16]

    if not blockers:
        write_json(root / "indra_qi_world_real_hilbert_l2_analytic_spine_state_v0_26.json", state)
        write_json(
            root / "indra_qi_world_real_hilbert_l2_analytic_spine_recommendation_v0_26.json",
            recommendation,
        )
        append_jsonl(ledger_path, ledger)
    if license_value.get("receipt_write_allowed") is True:
        write_json(root / "indra_qi_world_real_hilbert_l2_analytic_spine_receipt_v0_26.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append_jsonl(
            root / "indra_qi_world_real_hilbert_l2_analytic_spine_audit_v0_26.jsonl",
            {**receipt, "audit_record_digest": sha(receipt)},
        )

    return Result(
        VERSION,
        status,
        str(receipt["packet_id"]),
        str(root),
        spine_id,
        run_id,
        world_model_id,
        decision,
        int(analysis.get("coordinate_count", 0)),
        number(analysis.get("norm_squared")),
        number(analysis.get("weighted_energy")),
        number(analysis.get("coercivity_lower_bound")),
        analysis.get("rayleigh_lower_bound_verified") is True,
        source_digest,
        report_sha,
        state["world_l2_spine_state_digest"] if not blockers else "",
        ledger["record_digest"] if not blockers else "",
        blockers,
    )
