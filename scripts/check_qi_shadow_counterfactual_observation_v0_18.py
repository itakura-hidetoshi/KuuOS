#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile
from typing import Any, Mapping

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_shadow_counterfactual_observation_core_v0_18 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REPORT_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
    report_digest,
    sha,
)
from runtime.kuuos_indra_qi_shadow_counterfactual_observation_runtime_v0_18 import BLOCKED, READY, build_shadow_counterfactual_observation


def write(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(dict(value), ensure_ascii=False, sort_keys=True), encoding="utf-8")


def sources(root: pathlib.Path, decision: str) -> dict[str, Any]:
    world = {
        "version": "indra_qi_world_model_v0_1",
        "world_model_id": "world-a",
        "local_world_patches": [{"patch_id": value} for value in ("p0", "p1", "p2", "p3")],
        "indra_connections": [],
        "qi_flow_channels": [],
        "holonomy_cycles": [],
        "mandala_inclusion": {"multi_world_noncollapse": True, "single_ontology_forced": False},
        "epoch": 1,
    }
    world["indra_qi_world_state_digest"] = sha(world)
    entries = [
        {
            "shadow_slot_id": "slot-l0",
            "lineage_id": "l0",
            "lineage_kind": "explore",
            "requested_shadow_cycles": 3,
            "observation_budget": 8,
            "normalized_shadow_weight": 0.34,
            "rollback_corridor_digest": sha({"rollback": "l0"}),
            "shadow_baseline_digest": sha({"baseline": "l0"}),
            "shadow_overlay_digest": sha({"overlay": "l0"}),
            "sandbox_trial_passed": True,
            "rollback_corridor_match": True,
            "shadow_isolation_preserved": True,
        },
        {
            "shadow_slot_id": "slot-l1",
            "lineage_id": "l1",
            "lineage_kind": "recovery",
            "requested_shadow_cycles": 3,
            "observation_budget": 8,
            "normalized_shadow_weight": 0.33,
            "rollback_corridor_digest": sha({"rollback": "l1"}),
            "shadow_baseline_digest": sha({"baseline": "l1"}),
            "shadow_overlay_digest": sha({"overlay": "l1"}),
            "sandbox_trial_passed": True,
            "rollback_corridor_match": True,
            "shadow_isolation_preserved": True,
        },
        {
            "shadow_slot_id": "slot-l2",
            "lineage_id": "l2",
            "lineage_kind": "minority_preservation",
            "requested_shadow_cycles": 3,
            "observation_budget": 8,
            "normalized_shadow_weight": 0.33,
            "rollback_corridor_digest": sha({"rollback": "l2"}),
            "shadow_baseline_digest": sha({"baseline": "l2"}),
            "shadow_overlay_digest": sha({"overlay": "l2"}),
            "sandbox_trial_passed": True,
            "rollback_corridor_match": True,
            "shadow_isolation_preserved": True,
        },
    ]
    roster = {
        "version": "indra_qi_reversible_shadow_roster_v0_17",
        "shadow_program_id": "shadow-program-a",
        "admission_run_id": "admission-run-a",
        "world_model_id": "world-a",
        "source_trial_decision": "sandbox_trial_set_ready",
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_candidate_set_digest": sha({"candidate": 1}),
        "source_trial_state_digest": sha({"trial-state": 1}),
        "source_trial_recommendation_digest": sha({"trial-rec": 1}),
        "shadow_admission_proposal_digest": sha({"proposal": 1}),
        "shadow_entries": entries,
        "shadow_roster_analysis": {},
        "shadow_only": True,
        "live_route_enabled": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "candidate_weighting_not_truth": True,
        "recommendation_only": True,
        "epoch": 2,
    }
    roster["shadow_roster_digest"] = sha(roster)
    state = {
        "version": "indra_qi_reversible_shadow_admission_state_v0_17",
        "shadow_program_id": "shadow-program-a",
        "world_model_id": "world-a",
        "last_admission_run_id": "admission-run-a",
        "last_source_world_state_digest": world["indra_qi_world_state_digest"],
        "latest_shadow_admission_decision": decision,
        "latest_shadow_roster_digest": roster["shadow_roster_digest"],
        "epoch": 3,
    }
    state["shadow_admission_state_digest"] = sha(state)
    recommendation = {
        "version": "indra_qi_reversible_shadow_admission_recommendation_v0_17",
        "shadow_program_id": "shadow-program-a",
        "admission_run_id": "admission-run-a",
        "world_model_id": "world-a",
        "source_trial_decision": "sandbox_trial_set_ready",
        "decision": decision,
        "decision_reasons": ["test"],
        "shadow_roster_ready": decision == "reversible_shadow_admission_ready",
        "shadow_roster_digest": roster["shadow_roster_digest"],
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "recommendation_only": True,
        "shadow_admission_not_live_routing": True,
        "direct_live_route_authority": False,
        "direct_lineage_selection_authority": False,
        "direct_lineage_execution_authority": False,
        "direct_world_update_authority": False,
        "direct_external_actuation_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "truth_authority": False,
        "epoch": 3,
    }
    recommendation["shadow_admission_recommendation_digest"] = sha(recommendation)
    write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
    write(root / "indra_qi_reversible_shadow_roster_v0_17.json", roster)
    write(root / "indra_qi_reversible_shadow_admission_state_v0_17.json", state)
    write(root / "indra_qi_reversible_shadow_admission_recommendation_v0_17.json", recommendation)
    return {"world": world, "roster": roster, "state": state, "recommendation": recommendation}


def plan(source: Mapping[str, Any], cycle_id: str = "observation-cycle-a") -> dict[str, Any]:
    value = {
        "version": PLAN_VERSION,
        "observation_program_id": "observation-program-a",
        "observation_cycle_id": cycle_id,
        "world_model_id": "world-a",
        "expected_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "expected_shadow_roster_digest": source["roster"]["shadow_roster_digest"],
        "expected_source_admission_state_digest": source["state"]["shadow_admission_state_digest"],
        "expected_source_admission_recommendation_digest": source["recommendation"]["shadow_admission_recommendation_digest"],
        "observation_policy": {
            "minimum_projection_lineages": 3,
            "maximum_projection_lineages": 4,
            "minimum_projection_coverage_ratio": 1.0,
            "minimum_deterministic_replay_ratio": 1.0,
            "maximum_adverse_metric_shift": 0.20,
            "minimum_pareto_frontier_lineages": 2,
            "minimum_distinct_counterfactual_signatures": 3,
            "minimum_recovery_projections": 1,
            "minimum_minority_projections": 1,
            "require_shared_observation_input": True,
            "require_shadow_baseline_binding": True,
            "require_shadow_overlay_binding": True,
            "require_live_route_disabled": True,
            "require_external_actuation_disabled": True,
            "require_world_update_disabled": True,
            "require_policy_boundary_preserved": True,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    value["counterfactual_observation_plan_digest"] = plan_digest(value)
    return value


def metrics(debt: float, reserve: float, residue: float, scar: float, branch: float) -> dict[str, float]:
    return {
        "observation_debt": debt,
        "recoverability_reserve": reserve,
        "intervention_residue": residue,
        "scar_pressure": scar,
        "branch_energy": branch,
    }


def projection(entry: Mapping[str, Any], index: int, projected: Mapping[str, Any], shared: str, *, deterministic: bool = True, live: bool = False) -> dict[str, Any]:
    output = sha({"output": entry["lineage_id"], "index": index})
    return {
        "projection_id": f"projection-{entry['lineage_id']}",
        "lineage_id": entry["lineage_id"],
        "shadow_slot_id": entry["shadow_slot_id"],
        "shadow_cycle_index": 1,
        "observation_budget_used": 3,
        "observation_input_digest": shared,
        "shadow_baseline_digest": entry["shadow_baseline_digest"],
        "shadow_overlay_digest": entry["shadow_overlay_digest"],
        "baseline_metrics": metrics(0.5, 0.5, 0.4, 0.4, 0.5),
        "projected_metrics": dict(projected),
        "output_digest": output,
        "replay_output_digest": output if deterministic else sha({"different": entry["lineage_id"]}),
        "counterfactual_signature_digest": sha({"signature": entry["lineage_id"]}),
        "process_tensor_context_digest": sha({"process": entry["lineage_id"]}),
        "non_markov_context_digest": sha({"memory": entry["lineage_id"]}),
        "live_route_attempted": live,
        "external_actuation_attempted": False,
        "world_update_attempted": False,
        "policy_boundary_preserved": True,
    }


def report(plan_value: Mapping[str, Any], source: Mapping[str, Any], mode: str = "ready") -> dict[str, Any]:
    shared = sha({"shared-observation": 1})
    entries = source["roster"]["shadow_entries"]
    projections = [
        projection(entries[0], 0, metrics(0.30, 0.55, 0.30, 0.35, 0.70), shared),
        projection(entries[1], 1, metrics(0.40, 0.75, 0.35, 0.20, 0.55), shared),
        projection(entries[2], 2, metrics(0.35, 0.60, 0.20, 0.30, 0.65), shared),
    ]
    if mode == "nondeterministic":
        projections[1] = projection(entries[1], 1, metrics(0.40, 0.75, 0.35, 0.20, 0.55), shared, deterministic=False)
    elif mode == "adverse":
        projections[2] = projection(entries[2], 2, metrics(0.90, 0.20, 0.80, 0.80, 0.10), shared)
    elif mode == "live":
        projections[0] = projection(entries[0], 0, metrics(0.30, 0.55, 0.30, 0.35, 0.70), shared, live=True)
    value = {
        "version": REPORT_VERSION,
        "observation_cycle_id": plan_value["observation_cycle_id"],
        "source_shadow_roster_digest": source["roster"]["shadow_roster_digest"],
        "shared_observation_input_digest": shared,
        "projections": projections,
    }
    value["counterfactual_observation_report_digest"] = report_digest(value)
    return value


def license_value(plan_value: Mapping[str, Any], report_value: Mapping[str, Any], source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": LICENSE_VERSION,
        "license_id": "license-" + str(plan_value["observation_cycle_id"]),
        "bound_counterfactual_observation_plan_digest": plan_value["counterfactual_observation_plan_digest"],
        "bound_counterfactual_observation_report_digest": report_value["counterfactual_observation_report_digest"],
        "bound_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "bound_shadow_roster_digest": source["roster"]["shadow_roster_digest"],
        "bound_source_admission_state_digest": source["state"]["shadow_admission_state_digest"],
        "bound_source_admission_recommendation_digest": source["recommendation"]["shadow_admission_recommendation_digest"],
        "state_write_allowed": True,
        "comparison_write_allowed": True,
        "ledger_append_allowed": True,
        "recommendation_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "live_route_authority_granted": False,
        "external_actuation_authority_granted": False,
        "world_update_authority_granted": False,
        "lineage_selection_authority_granted": False,
        "lineage_execution_authority_granted": False,
        "truth_authority_granted": False,
        "direct_promotion_authority_granted": False,
        "direct_rollback_authority_granted": False,
        "direct_quarantine_authority_granted": False,
    }


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "indra_qi_shadow_counterfactual_observation_v0_18_enabled": True,
        "apply_indra_qi_shadow_counterfactual_observation_v0_18": True,
    }


def execute(root: pathlib.Path, source_decision: str, mode: str = "ready"):
    source = sources(root, source_decision)
    plan_value = plan(source)
    report_value = report(plan_value, source, mode)
    names = (
        "ku_indra_qi_noncommutative_mandala_world_state.json",
        "indra_qi_reversible_shadow_roster_v0_17.json",
        "indra_qi_reversible_shadow_admission_state_v0_17.json",
        "indra_qi_reversible_shadow_admission_recommendation_v0_17.json",
    )
    before = {name: (root / name).read_bytes() for name in names}
    result = build_shadow_counterfactual_observation(
        runtime_context=context(root),
        counterfactual_observation_plan=plan_value,
        counterfactual_observation_license=license_value(plan_value, report_value, source),
        counterfactual_observation_report=report_value,
    )
    after = {name: (root / name).read_bytes() for name in names}
    assert before == after
    return source, plan_value, report_value, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, report_value, result = execute(root, "reversible_shadow_admission_ready", "ready")
        assert result.status == READY and result.decision == "shadow_counterfactual_cycle_ready"
        comparison = json.loads((root / "indra_qi_shadow_counterfactual_comparison_v0_18.json").read_text())
        recommendation = json.loads((root / "indra_qi_shadow_counterfactual_observation_recommendation_v0_18.json").read_text())
        assert comparison["winner_selected"] is False
        assert comparison["pareto_frontier_not_winner_selection"] is True
        assert recommendation["direct_lineage_selection_authority"] is False
        assert len(recommendation["pareto_frontier_lineage_ids"]) >= 2
        replay = build_shadow_counterfactual_observation(
            runtime_context=context(root),
            counterfactual_observation_plan=plan_value,
            counterfactual_observation_license=license_value(plan_value, report_value, source),
            counterfactual_observation_report=report_value,
        )
        assert replay.status == BLOCKED and "counterfactual_replay_detected" in replay.blockers

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "reversible_shadow_admission_ready", "nondeterministic")
        assert result.status == READY and result.decision == "redesign_shadow_observation_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "reversible_shadow_admission_ready", "adverse")
        assert result.status == READY and result.decision == "redesign_shadow_observation_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "reversible_shadow_admission_ready", "live")
        assert result.status == READY and result.decision == "quarantine_recommended"

    for source_decision, expected in (
        ("hold_for_observation", "hold_for_observation"),
        ("redesign_shadow_roster_recommended", "redesign_shadow_observation_recommended"),
        ("rollback_recommended", "rollback_recommended"),
        ("quarantine_recommended", "quarantine_recommended"),
    ):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(pathlib.Path(directory), source_decision, "ready")
            assert result.status == READY and result.decision == expected

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "reversible_shadow_admission_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        report_value["projections"][0]["observation_budget_used"] = 999
        result = build_shadow_counterfactual_observation(
            runtime_context=context(root),
            counterfactual_observation_plan=plan_value,
            counterfactual_observation_license=license_value(plan_value, report_value, source),
            counterfactual_observation_report=report_value,
        )
        assert result.status == BLOCKED and "counterfactual_report_digest_invalid" in result.blockers

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "reversible_shadow_admission_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        source["world"]["world_model_id"] = "tampered"
        write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", source["world"])
        result = build_shadow_counterfactual_observation(
            runtime_context=context(root),
            counterfactual_observation_plan=plan_value,
            counterfactual_observation_license=license_value(plan_value, report_value, source),
            counterfactual_observation_report=report_value,
        )
        assert result.status == BLOCKED and "counterfactual_source_world_invalid" in result.blockers

    manifest = json.loads((ROOT / "manifests/qi_shadow_counterfactual_observation_v0_18.json").read_text())
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_shadow_counterfactual_observation_v0_18 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
