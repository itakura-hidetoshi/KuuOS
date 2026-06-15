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

from runtime.kuuos_indra_qi_longitudinal_shadow_evidence_core_v0_19 import (
    BENEFIT_FIELDS,
    LICENSE_VERSION,
    PLAN_VERSION,
    REPORT_VERSION,
    REQUIRED_BOUNDARY,
    cycle_digest,
    plan_digest,
    report_digest,
    sha,
)
from runtime.kuuos_indra_qi_longitudinal_shadow_evidence_runtime_v0_19 import (
    BLOCKED,
    READY,
    build_longitudinal_shadow_evidence,
)


def write(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(dict(value), ensure_ascii=False, sort_keys=True), encoding="utf-8")


def sources(root: pathlib.Path, decision: str) -> dict[str, Any]:
    world = {
        "version": "indra_qi_world_model_v0_1",
        "world_model_id": "world-a",
        "mandala_inclusion": {"multi_world_noncollapse": True, "single_ontology_forced": False},
        "epoch": 1,
    }
    world["indra_qi_world_state_digest"] = sha(world)
    roster_digest = sha({"roster": "a"})
    comparison = {
        "version": "indra_qi_shadow_counterfactual_comparison_v0_18",
        "observation_program_id": "observation-program-a",
        "observation_cycle_id": "cycle-3",
        "world_model_id": "world-a",
        "source_shadow_admission_decision": "reversible_shadow_admission_ready",
        "shared_observation_input_digest": sha({"shared": 3}),
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_shadow_roster_digest": roster_digest,
        "source_admission_state_digest": sha({"admission-state": 1}),
        "source_admission_recommendation_digest": sha({"admission-rec": 1}),
        "counterfactual_observation_report_digest": sha({"report": 3}),
        "projection_analysis": {},
        "pareto_frontier_not_winner_selection": True,
        "winner_selected": False,
        "live_route_enabled": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "recommendation_only": True,
        "epoch": 30,
    }
    comparison["counterfactual_comparison_digest"] = sha(comparison)
    state = {
        "version": "indra_qi_shadow_counterfactual_observation_state_v0_18",
        "observation_program_id": "observation-program-a",
        "world_model_id": "world-a",
        "last_observation_cycle_id": "cycle-3",
        "latest_counterfactual_observation_decision": decision,
        "latest_counterfactual_comparison_digest": comparison["counterfactual_comparison_digest"],
        "epoch": 31,
    }
    state["counterfactual_observation_state_digest"] = sha(state)
    recommendation = {
        "version": "indra_qi_shadow_counterfactual_observation_recommendation_v0_18",
        "observation_program_id": "observation-program-a",
        "observation_cycle_id": "cycle-3",
        "world_model_id": "world-a",
        "source_shadow_admission_decision": "reversible_shadow_admission_ready",
        "decision": decision,
        "decision_reasons": ["test"],
        "counterfactual_cycle_ready": decision == "shadow_counterfactual_cycle_ready",
        "winner_selected": False,
        "counterfactual_comparison_digest": comparison["counterfactual_comparison_digest"],
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_shadow_roster_digest": roster_digest,
        "recommendation_only": True,
        "pareto_frontier_not_winner_selection": True,
        "direct_live_route_authority": False,
        "direct_lineage_selection_authority": False,
        "direct_lineage_execution_authority": False,
        "direct_world_update_authority": False,
        "direct_external_actuation_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "truth_authority": False,
        "epoch": 31,
    }
    recommendation["counterfactual_observation_recommendation_digest"] = sha(recommendation)
    write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
    write(root / "indra_qi_shadow_counterfactual_comparison_v0_18.json", comparison)
    write(root / "indra_qi_shadow_counterfactual_observation_state_v0_18.json", state)
    write(root / "indra_qi_shadow_counterfactual_observation_recommendation_v0_18.json", recommendation)
    return {"world": world, "comparison": comparison, "state": state, "recommendation": recommendation, "roster_digest": roster_digest}


def plan(source: Mapping[str, Any], run_id: str = "evidence-run-a") -> dict[str, Any]:
    value = {
        "version": PLAN_VERSION,
        "evidence_program_id": "evidence-program-a",
        "evidence_run_id": run_id,
        "world_model_id": "world-a",
        "expected_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "expected_latest_comparison_digest": source["comparison"]["counterfactual_comparison_digest"],
        "expected_source_observation_state_digest": source["state"]["counterfactual_observation_state_digest"],
        "expected_source_observation_recommendation_digest": source["recommendation"]["counterfactual_observation_recommendation_digest"],
        "evidence_policy": {
            "minimum_evidence_cycles": 3,
            "maximum_evidence_cycles": 12,
            "minimum_lineage_coverage_ratio": 1.0,
            "minimum_persistent_frontier_lineages": 2,
            "minimum_persistent_frontier_ratio": 0.66,
            "maximum_single_lineage_frontier_share": 0.60,
            "minimum_sustained_benefit_ratio": 0.66,
            "maximum_metric_volatility": 0.30,
            "minimum_recovery_persistence_ratio": 0.66,
            "minimum_minority_persistence_ratio": 0.66,
            "maximum_single_lineage_only_frontier_streak": 1,
            "require_cycle_chain": True,
            "require_monotonic_cycle_index": True,
            "require_monotonic_epoch": True,
            "require_same_shadow_roster": True,
            "require_winner_selected_false": True,
            "require_live_route_disabled": True,
            "require_external_actuation_disabled": True,
            "require_world_update_disabled": True,
            "require_policy_boundary_preserved": True,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    value["longitudinal_evidence_plan_digest"] = plan_digest(value)
    return value


def vector(seed: float, *, adverse: bool = False) -> dict[str, float]:
    if adverse:
        return {field: -0.5 for field in BENEFIT_FIELDS}
    offsets = [0.12, 0.10, 0.08, 0.06, 0.09]
    return {field: round(seed + offsets[index], 3) for index, field in enumerate(BENEFIT_FIELDS)}


def observation(lineage_id: str, kind: str, benefit: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "lineage_id": lineage_id,
        "lineage_kind": kind,
        "benefit_vector": dict(benefit),
        "deterministic_replay": True,
        "counterfactual_signature_digest": sha({"signature": lineage_id, "benefit": benefit}),
        "process_tensor_context_digest": sha({"process": lineage_id}),
        "non_markov_context_digest": sha({"memory": lineage_id}),
    }


def cycle(index: int, source: Mapping[str, Any], frontier: list[str], *, mode: str = "ready", previous: str = "GENESIS") -> dict[str, Any]:
    seeds = {
        "l0": 0.02 + index * 0.01,
        "l1": 0.03 + index * 0.01,
        "l2": 0.01 + index * 0.01,
    }
    observations = [
        observation("l0", "explore", vector(seeds["l0"])),
        observation("l1", "recovery", vector(seeds["l1"])),
        observation("l2", "minority_preservation", vector(seeds["l2"])),
    ]
    if mode == "volatile" and index == 2:
        observations[2] = observation("l2", "minority_preservation", vector(0.0, adverse=True))
    value = {
        "cycle_index": index,
        "observation_cycle_id": f"cycle-{index}",
        "source_shadow_roster_digest": source["roster_digest"],
        "source_comparison_digest": source["comparison"]["counterfactual_comparison_digest"] if index == 3 else sha({"comparison": index}),
        "pareto_frontier_lineage_ids": frontier,
        "lineage_observations": observations,
        "winner_selected": False,
        "live_route_attempted": mode == "boundary" and index == 2,
        "external_actuation_attempted": False,
        "world_update_attempted": False,
        "policy_boundary_preserved": True,
        "prev_cycle_evidence_digest": previous,
        "epoch": 100 + index,
    }
    value["cycle_evidence_digest"] = cycle_digest(value)
    return value


def report(plan_value: Mapping[str, Any], source: Mapping[str, Any], mode: str = "ready") -> dict[str, Any]:
    if mode == "collapse":
        frontiers = [["l0"], ["l0"], ["l0"]]
    else:
        frontiers = [["l0", "l1"], ["l1", "l2"], ["l0", "l2"]]
    cycles: list[dict[str, Any]] = []
    previous = "GENESIS"
    for index, frontier in enumerate(frontiers, start=1):
        current = cycle(index, source, frontier, mode=mode, previous=previous)
        cycles.append(current)
        previous = current["cycle_evidence_digest"]
    value = {
        "version": REPORT_VERSION,
        "evidence_run_id": plan_value["evidence_run_id"],
        "latest_comparison_digest": source["comparison"]["counterfactual_comparison_digest"],
        "source_observation_recommendation_digest": source["recommendation"]["counterfactual_observation_recommendation_digest"],
        "cycles": cycles,
    }
    value["longitudinal_evidence_report_digest"] = report_digest(value)
    return value


def license_value(plan_value: Mapping[str, Any], report_value: Mapping[str, Any], source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": LICENSE_VERSION,
        "license_id": "license-" + str(plan_value["evidence_run_id"]),
        "bound_longitudinal_evidence_plan_digest": plan_value["longitudinal_evidence_plan_digest"],
        "bound_longitudinal_evidence_report_digest": report_value["longitudinal_evidence_report_digest"],
        "bound_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "bound_latest_comparison_digest": source["comparison"]["counterfactual_comparison_digest"],
        "bound_source_observation_state_digest": source["state"]["counterfactual_observation_state_digest"],
        "bound_source_observation_recommendation_digest": source["recommendation"]["counterfactual_observation_recommendation_digest"],
        "state_write_allowed": True,
        "summary_write_allowed": True,
        "ledger_append_allowed": True,
        "recommendation_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "winner_selection_authority_granted": False,
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
        "indra_qi_longitudinal_shadow_evidence_v0_19_enabled": True,
        "apply_indra_qi_longitudinal_shadow_evidence_v0_19": True,
    }


def execute(root: pathlib.Path, source_decision: str, mode: str = "ready"):
    source = sources(root, source_decision)
    plan_value = plan(source)
    report_value = report(plan_value, source, mode)
    names = (
        "ku_indra_qi_noncommutative_mandala_world_state.json",
        "indra_qi_shadow_counterfactual_comparison_v0_18.json",
        "indra_qi_shadow_counterfactual_observation_state_v0_18.json",
        "indra_qi_shadow_counterfactual_observation_recommendation_v0_18.json",
    )
    before = {name: (root / name).read_bytes() for name in names}
    result = build_longitudinal_shadow_evidence(
        runtime_context=context(root),
        longitudinal_evidence_plan=plan_value,
        longitudinal_evidence_license=license_value(plan_value, report_value, source),
        longitudinal_evidence_report=report_value,
    )
    after = {name: (root / name).read_bytes() for name in names}
    assert before == after
    return source, plan_value, report_value, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, report_value, result = execute(root, "shadow_counterfactual_cycle_ready", "ready")
        assert result.status == READY
        assert result.decision == "longitudinal_shadow_evidence_ready"
        summary = json.loads((root / "indra_qi_longitudinal_shadow_evidence_summary_v0_19.json").read_text())
        recommendation = json.loads((root / "indra_qi_longitudinal_shadow_evidence_recommendation_v0_19.json").read_text())
        assert summary["winner_selected"] is False
        assert summary["stability_without_collapse"] is True
        assert recommendation["direct_winner_selection_authority"] is False
        assert len(recommendation["longitudinal_analysis"]["persistent_frontier_lineage_ids"]) >= 2
        replay = build_longitudinal_shadow_evidence(
            runtime_context=context(root),
            longitudinal_evidence_plan=plan_value,
            longitudinal_evidence_license=license_value(plan_value, report_value, source),
            longitudinal_evidence_report=report_value,
        )
        assert replay.status == BLOCKED
        assert "longitudinal_replay_detected" in replay.blockers

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "shadow_counterfactual_cycle_ready", "volatile")
        assert result.status == READY
        assert result.decision == "extend_longitudinal_observation_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "shadow_counterfactual_cycle_ready", "collapse")
        assert result.status == READY
        assert result.decision == "restore_shadow_diversity_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "shadow_counterfactual_cycle_ready", "boundary")
        assert result.status == READY
        assert result.decision == "quarantine_recommended"

    for source_decision, expected in (
        ("hold_for_observation", "hold_for_observation"),
        ("redesign_shadow_observation_recommended", "extend_longitudinal_observation_recommended"),
        ("rollback_recommended", "rollback_recommended"),
        ("quarantine_recommended", "quarantine_recommended"),
    ):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(pathlib.Path(directory), source_decision, "ready")
            assert result.status == READY
            assert result.decision == expected

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "shadow_counterfactual_cycle_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        report_value["cycles"][0]["epoch"] = 9999
        result = build_longitudinal_shadow_evidence(
            runtime_context=context(root),
            longitudinal_evidence_plan=plan_value,
            longitudinal_evidence_license=license_value(plan_value, report_value, source),
            longitudinal_evidence_report=report_value,
        )
        assert result.status == BLOCKED
        assert "longitudinal_report_digest_invalid" in result.blockers

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "shadow_counterfactual_cycle_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        source["world"]["world_model_id"] = "tampered"
        write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", source["world"])
        result = build_longitudinal_shadow_evidence(
            runtime_context=context(root),
            longitudinal_evidence_plan=plan_value,
            longitudinal_evidence_license=license_value(plan_value, report_value, source),
            longitudinal_evidence_report=report_value,
        )
        assert result.status == BLOCKED
        assert "longitudinal_source_world_invalid" in result.blockers

    manifest = json.loads((ROOT / "manifests/qi_longitudinal_shadow_evidence_v0_19.json").read_text())
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_longitudinal_shadow_evidence_v0_19 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
