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

from runtime.kuuos_indra_qi_reversible_shadow_admission_core_v0_17 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    PROPOSAL_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
    proposal_digest,
    sha,
)
from runtime.kuuos_indra_qi_reversible_shadow_admission_runtime_v0_17 import BLOCKED, READY, build_reversible_shadow_admission


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
    lineages = [
        {
            "lineage_id": "l0",
            "lineage_kind": "explore",
            "candidate_weight": 0.34,
            "rollback_corridor_digest": sha({"rollback": "l0"}),
            "preserves_minority_path": True,
            "recovery_path": False,
        },
        {
            "lineage_id": "l1",
            "lineage_kind": "recovery",
            "candidate_weight": 0.33,
            "rollback_corridor_digest": sha({"rollback": "l1"}),
            "preserves_minority_path": False,
            "recovery_path": True,
        },
        {
            "lineage_id": "l2",
            "lineage_kind": "minority_preservation",
            "candidate_weight": 0.33,
            "rollback_corridor_digest": sha({"rollback": "l2"}),
            "preserves_minority_path": True,
            "recovery_path": False,
        },
    ]
    candidate = {
        "version": "indra_qi_multi_lineage_candidate_set_v0_15",
        "evolution_id": "evolution-a",
        "evolution_run_id": "evolution-run-a",
        "world_model_id": "world-a",
        "source_ecology_decision": "ecology_compatible_bounded_promotion",
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_path_ecology_state_digest": sha({"ecology-state": 1}),
        "source_path_ecology_recommendation_digest": sha({"ecology-rec": 1}),
        "lineage_proposal_digest": sha({"proposal": 1}),
        "candidate_lineages": lineages,
        "candidate_set_analysis": {},
        "candidate_weighting_not_truth": True,
        "candidate_set_not_selection": True,
        "candidate_set_not_execution": True,
        "recommendation_only": True,
        "epoch": 2,
    }
    candidate["candidate_set_digest"] = sha(candidate)
    state = {
        "version": "indra_qi_licensed_sandbox_lineage_trial_state_v0_16",
        "trial_program_id": "trial-program-a",
        "world_model_id": "world-a",
        "last_trial_run_id": "trial-run-a",
        "last_source_world_state_digest": world["indra_qi_world_state_digest"],
        "last_source_candidate_set_digest": candidate["candidate_set_digest"],
        "latest_sandbox_trial_decision": decision,
        "epoch": 3,
    }
    state["sandbox_trial_state_digest"] = sha(state)
    trial_results = [
        {
            "trial_id": f"trial-{lineage_id}",
            "lineage_id": lineage_id,
            "attempt_index": 0,
            "isolation_preserved": True,
            "deterministic_replay": True,
            "snapshot_restored": True,
            "resource_budget_preserved": True,
            "residual_bounded": True,
            "process_succeeded": True,
            "trial_passed": True,
        }
        for lineage_id in ("l0", "l1", "l2")
    ]
    recommendation = {
        "version": "indra_qi_licensed_sandbox_lineage_trial_recommendation_v0_16",
        "trial_program_id": "trial-program-a",
        "trial_run_id": "trial-run-a",
        "world_model_id": "world-a",
        "source_evolution_decision": "diverse_bounded_evolution_ready",
        "decision": decision,
        "decision_reasons": ["test"],
        "trial_set_ready": decision == "sandbox_trial_set_ready",
        "trial_analysis": {"trial_results": trial_results},
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_candidate_set_digest": candidate["candidate_set_digest"],
        "source_evolution_state_digest": sha({"evolution-state": 1}),
        "source_evolution_recommendation_digest": sha({"evolution-rec": 1}),
        "sandbox_trial_report_digest": sha({"report": 1}),
        "recommendation_only": True,
        "trial_evidence_not_execution_authority": True,
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
    recommendation["sandbox_trial_recommendation_digest"] = sha(recommendation)
    write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
    write(root / "indra_qi_multi_lineage_candidate_set_v0_15.json", candidate)
    write(root / "indra_qi_licensed_sandbox_lineage_trial_state_v0_16.json", state)
    write(root / "indra_qi_licensed_sandbox_lineage_trial_recommendation_v0_16.json", recommendation)
    return {"world": world, "candidate": candidate, "state": state, "recommendation": recommendation}


def plan(source: Mapping[str, Any], run_id: str = "admission-run-a") -> dict[str, Any]:
    value = {
        "version": PLAN_VERSION,
        "shadow_program_id": "shadow-program-a",
        "admission_run_id": run_id,
        "world_model_id": "world-a",
        "expected_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "expected_candidate_set_digest": source["candidate"]["candidate_set_digest"],
        "expected_source_trial_state_digest": source["state"]["sandbox_trial_state_digest"],
        "expected_source_trial_recommendation_digest": source["recommendation"]["sandbox_trial_recommendation_digest"],
        "shadow_policy": {
            "minimum_shadow_lineages": 3,
            "maximum_shadow_lineages": 4,
            "maximum_shadow_cycles": 3,
            "maximum_observation_budget_per_lineage": 10,
            "maximum_total_observation_budget": 24,
            "maximum_single_shadow_weight": 0.50,
            "minimum_distinct_lineage_kinds": 3,
            "minimum_recovery_lineages": 1,
            "minimum_minority_lineages": 1,
            "require_all_admitted_lineages_sandbox_passed": True,
            "require_rollback_corridor_match": True,
            "require_shadow_baseline": True,
            "require_shadow_overlay": True,
            "require_live_route_disabled": True,
            "require_external_actuation_disabled": True,
            "require_world_update_disabled": True,
            "require_policy_boundary_preserved": True,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    value["shadow_admission_plan_digest"] = plan_digest(value)
    return value


def entry(lineage_id: str, weight: float, *, live: bool = False, bad_rollback: bool = False) -> dict[str, Any]:
    return {
        "shadow_slot_id": "slot-" + lineage_id,
        "lineage_id": lineage_id,
        "requested_shadow_cycles": 2,
        "observation_budget": 6,
        "shadow_weight": weight,
        "rollback_corridor_digest": sha({"rollback": "wrong" if bad_rollback else lineage_id}),
        "shadow_baseline_digest": sha({"baseline": lineage_id}),
        "shadow_overlay_digest": sha({"overlay": lineage_id}),
        "live_route_enabled": live,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "policy_boundary_preserved": True,
    }


def proposal(plan_value: Mapping[str, Any], source: Mapping[str, Any], mode: str = "ready") -> dict[str, Any]:
    entries = [entry("l0", 0.34), entry("l1", 0.33), entry("l2", 0.33)]
    if mode == "dominant":
        entries = [entry("l0", 0.80), entry("l1", 0.10), entry("l2", 0.10)]
    elif mode == "live":
        entries[0] = entry("l0", 0.34, live=True)
    elif mode == "rollback":
        entries[1] = entry("l1", 0.33, bad_rollback=True)
    value = {
        "version": PROPOSAL_VERSION,
        "admission_run_id": plan_value["admission_run_id"],
        "source_candidate_set_digest": source["candidate"]["candidate_set_digest"],
        "source_trial_recommendation_digest": source["recommendation"]["sandbox_trial_recommendation_digest"],
        "shadow_entries": entries,
    }
    value["shadow_admission_proposal_digest"] = proposal_digest(value)
    return value


def license_value(plan_value: Mapping[str, Any], proposal_value: Mapping[str, Any], source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": LICENSE_VERSION,
        "license_id": "license-" + str(plan_value["admission_run_id"]),
        "bound_shadow_admission_plan_digest": plan_value["shadow_admission_plan_digest"],
        "bound_shadow_admission_proposal_digest": proposal_value["shadow_admission_proposal_digest"],
        "bound_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "bound_candidate_set_digest": source["candidate"]["candidate_set_digest"],
        "bound_source_trial_state_digest": source["state"]["sandbox_trial_state_digest"],
        "bound_source_trial_recommendation_digest": source["recommendation"]["sandbox_trial_recommendation_digest"],
        "state_write_allowed": True,
        "shadow_roster_write_allowed": True,
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
        "indra_qi_reversible_shadow_admission_v0_17_enabled": True,
        "apply_indra_qi_reversible_shadow_admission_v0_17": True,
    }


def execute(root: pathlib.Path, source_decision: str, mode: str = "ready"):
    source = sources(root, source_decision)
    plan_value = plan(source)
    proposal_value = proposal(plan_value, source, mode)
    names = (
        "ku_indra_qi_noncommutative_mandala_world_state.json",
        "indra_qi_multi_lineage_candidate_set_v0_15.json",
        "indra_qi_licensed_sandbox_lineage_trial_state_v0_16.json",
        "indra_qi_licensed_sandbox_lineage_trial_recommendation_v0_16.json",
    )
    before = {name: (root / name).read_bytes() for name in names}
    result = build_reversible_shadow_admission(
        runtime_context=context(root),
        shadow_admission_plan=plan_value,
        shadow_admission_license=license_value(plan_value, proposal_value, source),
        shadow_admission_proposal=proposal_value,
    )
    after = {name: (root / name).read_bytes() for name in names}
    assert before == after
    return source, plan_value, proposal_value, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, proposal_value, result = execute(root, "sandbox_trial_set_ready", "ready")
        assert result.status == READY and result.decision == "reversible_shadow_admission_ready"
        roster = json.loads((root / "indra_qi_reversible_shadow_roster_v0_17.json").read_text())
        recommendation = json.loads((root / "indra_qi_reversible_shadow_admission_recommendation_v0_17.json").read_text())
        assert roster["shadow_only"] is True and roster["live_route_enabled"] is False
        assert recommendation["shadow_admission_not_live_routing"] is True
        assert recommendation["direct_lineage_execution_authority"] is False
        replay = build_reversible_shadow_admission(
            runtime_context=context(root),
            shadow_admission_plan=plan_value,
            shadow_admission_license=license_value(plan_value, proposal_value, source),
            shadow_admission_proposal=proposal_value,
        )
        assert replay.status == BLOCKED and "shadow_admission_replay_detected" in replay.blockers

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "sandbox_trial_set_ready", "dominant")
        assert result.status == READY and result.decision == "redesign_shadow_roster_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "sandbox_trial_set_ready", "rollback")
        assert result.status == READY and result.decision == "redesign_shadow_roster_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "sandbox_trial_set_ready", "live")
        assert result.status == READY and result.decision == "quarantine_recommended"

    for source_decision, expected in (
        ("hold_for_observation", "hold_for_observation"),
        ("redesign_sandbox_trials_recommended", "redesign_shadow_roster_recommended"),
        ("rollback_recommended", "rollback_recommended"),
        ("quarantine_recommended", "quarantine_recommended"),
    ):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(pathlib.Path(directory), source_decision, "ready")
            assert result.status == READY and result.decision == expected

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "sandbox_trial_set_ready")
        plan_value = plan(source)
        proposal_value = proposal(plan_value, source)
        proposal_value["shadow_entries"][0]["observation_budget"] = 999
        result = build_reversible_shadow_admission(
            runtime_context=context(root),
            shadow_admission_plan=plan_value,
            shadow_admission_license=license_value(plan_value, proposal_value, source),
            shadow_admission_proposal=proposal_value,
        )
        assert result.status == BLOCKED and "shadow_admission_proposal_digest_invalid" in result.blockers

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "sandbox_trial_set_ready")
        plan_value = plan(source)
        proposal_value = proposal(plan_value, source)
        source["world"]["world_model_id"] = "tampered"
        write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", source["world"])
        result = build_reversible_shadow_admission(
            runtime_context=context(root),
            shadow_admission_plan=plan_value,
            shadow_admission_license=license_value(plan_value, proposal_value, source),
            shadow_admission_proposal=proposal_value,
        )
        assert result.status == BLOCKED and "shadow_admission_source_world_invalid" in result.blockers

    manifest = json.loads((ROOT / "manifests/qi_reversible_shadow_admission_v0_17.json").read_text())
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_reversible_shadow_admission_v0_17 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
