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

from runtime.kuuos_indra_qi_licensed_sandbox_lineage_trial_core_v0_16 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REPORT_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
    report_digest,
    sha,
)
from runtime.kuuos_indra_qi_licensed_sandbox_lineage_trial_runtime_v0_16 import BLOCKED, READY, build_licensed_sandbox_lineage_trial


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
        {"lineage_id": "l0", "lineage_kind": "explore", "candidate_weight": 0.34},
        {"lineage_id": "l1", "lineage_kind": "recovery", "candidate_weight": 0.33},
        {"lineage_id": "l2", "lineage_kind": "reobserve", "candidate_weight": 0.33},
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
        "version": "indra_qi_multi_lineage_evolution_state_v0_15",
        "evolution_id": "evolution-a",
        "world_model_id": "world-a",
        "last_evolution_run_id": "evolution-run-a",
        "last_source_world_state_digest": world["indra_qi_world_state_digest"],
        "latest_multi_lineage_decision": decision,
        "latest_candidate_set_digest": candidate["candidate_set_digest"],
        "epoch": 3,
    }
    state["multi_lineage_state_digest"] = sha(state)
    recommendation = {
        "version": "indra_qi_multi_lineage_evolution_recommendation_v0_15",
        "evolution_id": "evolution-a",
        "evolution_run_id": "evolution-run-a",
        "world_model_id": "world-a",
        "source_ecology_decision": "ecology_compatible_bounded_promotion",
        "decision": decision,
        "candidate_set_ready": decision.endswith("_ready"),
        "candidate_set_digest": candidate["candidate_set_digest"],
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "recommendation_only": True,
        "candidate_weighting_not_truth": True,
        "direct_lineage_selection_authority": False,
        "direct_lineage_execution_authority": False,
        "direct_world_update_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "truth_authority": False,
        "epoch": 3,
    }
    recommendation["multi_lineage_recommendation_digest"] = sha(recommendation)
    write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
    write(root / "indra_qi_multi_lineage_candidate_set_v0_15.json", candidate)
    write(root / "indra_qi_multi_lineage_evolution_state_v0_15.json", state)
    write(root / "indra_qi_multi_lineage_evolution_recommendation_v0_15.json", recommendation)
    return {"world": world, "candidate": candidate, "state": state, "recommendation": recommendation}


def plan(source: Mapping[str, Any], run_id: str = "trial-run-a") -> dict[str, Any]:
    result = {
        "version": PLAN_VERSION,
        "trial_program_id": "trial-program-a",
        "trial_run_id": run_id,
        "world_model_id": "world-a",
        "expected_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "expected_candidate_set_digest": source["candidate"]["candidate_set_digest"],
        "expected_source_evolution_state_digest": source["state"]["multi_lineage_state_digest"],
        "expected_source_evolution_recommendation_digest": source["recommendation"]["multi_lineage_recommendation_digest"],
        "trial_policy": {
            "minimum_trial_lineages": 3,
            "maximum_trial_lineages": 8,
            "maximum_attempts_per_lineage": 2,
            "maximum_duration_ms": 5000,
            "maximum_cpu_ms": 4000,
            "maximum_peak_memory_mb": 256,
            "minimum_lineage_coverage_ratio": 1.0,
            "minimum_passing_lineage_ratio": 1.0,
            "minimum_deterministic_replay_ratio": 1.0,
            "maximum_trial_residual_score": 0.20,
            "require_network_disabled": True,
            "require_external_actuation_disabled": True,
            "require_filesystem_overlay": True,
            "require_snapshot_restore": True,
            "require_policy_boundary_preserved": True,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    result["sandbox_trial_plan_digest"] = plan_digest(result)
    return result


def trial(lineage_id: str, *, deterministic: bool = True, network: bool = False, exit_code: int = 0, residual: float = 0.1) -> dict[str, Any]:
    output = sha({"output": lineage_id})
    rollback = sha({"rollback": lineage_id})
    return {
        "trial_id": "trial-" + lineage_id,
        "lineage_id": lineage_id,
        "attempt_index": 0,
        "sandbox_image_digest": sha({"image": 1}),
        "sandbox_snapshot_digest": sha({"snapshot": lineage_id}),
        "input_digest": sha({"input": lineage_id}),
        "output_digest": output,
        "replay_output_digest": output if deterministic else sha({"different": lineage_id}),
        "rollback_state_digest": rollback,
        "expected_rollback_state_digest": rollback,
        "stdout_digest": sha({"stdout": lineage_id}),
        "stderr_digest": sha({"stderr": lineage_id}),
        "duration_ms": 100,
        "cpu_ms": 80,
        "peak_memory_mb": 32,
        "residual_score": residual,
        "network_access_attempted": network,
        "external_actuation_attempted": False,
        "filesystem_overlay_used": True,
        "policy_boundary_preserved": True,
        "process_exit_code": exit_code,
    }


def report(plan_value: Mapping[str, Any], source: Mapping[str, Any], mode: str = "pass") -> dict[str, Any]:
    trials = [trial("l0"), trial("l1"), trial("l2")]
    if mode == "nondeterministic":
        trials[1] = trial("l1", deterministic=False)
    elif mode == "network":
        trials[0] = trial("l0", network=True)
    elif mode == "failure":
        trials[2] = trial("l2", exit_code=2, residual=0.5)
    result = {
        "version": REPORT_VERSION,
        "trial_run_id": plan_value["trial_run_id"],
        "source_candidate_set_digest": source["candidate"]["candidate_set_digest"],
        "source_evolution_recommendation_digest": source["recommendation"]["multi_lineage_recommendation_digest"],
        "trials": trials,
    }
    result["sandbox_trial_report_digest"] = report_digest(result)
    return result


def license_value(plan_value: Mapping[str, Any], report_value: Mapping[str, Any], source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": LICENSE_VERSION,
        "license_id": "license-" + str(plan_value["trial_run_id"]),
        "bound_sandbox_trial_plan_digest": plan_value["sandbox_trial_plan_digest"],
        "bound_sandbox_trial_report_digest": report_value["sandbox_trial_report_digest"],
        "bound_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "bound_candidate_set_digest": source["candidate"]["candidate_set_digest"],
        "bound_source_evolution_state_digest": source["state"]["multi_lineage_state_digest"],
        "bound_source_evolution_recommendation_digest": source["recommendation"]["multi_lineage_recommendation_digest"],
        "state_write_allowed": True,
        "ledger_append_allowed": True,
        "recommendation_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "network_authority_granted": False,
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
        "indra_qi_licensed_sandbox_lineage_trial_v0_16_enabled": True,
        "apply_indra_qi_licensed_sandbox_lineage_trial_v0_16": True,
    }


def execute(root: pathlib.Path, source_decision: str, mode: str = "pass"):
    source = sources(root, source_decision)
    plan_value = plan(source)
    report_value = report(plan_value, source, mode)
    names = (
        "ku_indra_qi_noncommutative_mandala_world_state.json",
        "indra_qi_multi_lineage_candidate_set_v0_15.json",
        "indra_qi_multi_lineage_evolution_state_v0_15.json",
        "indra_qi_multi_lineage_evolution_recommendation_v0_15.json",
    )
    before = {name: (root / name).read_bytes() for name in names}
    result = build_licensed_sandbox_lineage_trial(
        runtime_context=context(root),
        sandbox_trial_plan=plan_value,
        sandbox_trial_license=license_value(plan_value, report_value, source),
        sandbox_trial_report=report_value,
    )
    after = {name: (root / name).read_bytes() for name in names}
    assert before == after
    return source, plan_value, report_value, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, report_value, result = execute(root, "diverse_bounded_evolution_ready", "pass")
        assert result.status == READY and result.decision == "sandbox_trial_set_ready"
        recommendation = json.loads((root / "indra_qi_licensed_sandbox_lineage_trial_recommendation_v0_16.json").read_text())
        assert recommendation["trial_evidence_not_execution_authority"] is True
        assert recommendation["direct_lineage_execution_authority"] is False
        assert recommendation["direct_external_actuation_authority"] is False
        replay = build_licensed_sandbox_lineage_trial(
            runtime_context=context(root),
            sandbox_trial_plan=plan_value,
            sandbox_trial_license=license_value(plan_value, report_value, source),
            sandbox_trial_report=report_value,
        )
        assert replay.status == BLOCKED and "sandbox_trial_replay_detected" in replay.blockers

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "branch_reopening_candidate_set_ready", "nondeterministic")
        assert result.status == READY and result.decision == "redesign_sandbox_trials_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "focus_reobserve_candidate_set_ready", "failure")
        assert result.status == READY and result.decision == "redesign_sandbox_trials_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(pathlib.Path(directory), "diverse_bounded_evolution_ready", "network")
        assert result.status == READY and result.decision == "quarantine_recommended"

    for source_decision, expected in (
        ("hold_for_observation", "hold_for_observation"),
        ("redesign_candidate_set_recommended", "redesign_sandbox_trials_recommended"),
        ("rollback_recommended", "rollback_recommended"),
        ("quarantine_recommended", "quarantine_recommended"),
    ):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(pathlib.Path(directory), source_decision, "pass")
            assert result.status == READY and result.decision == expected

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "diverse_bounded_evolution_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        report_value["trials"][0]["duration_ms"] = 999999
        result = build_licensed_sandbox_lineage_trial(
            runtime_context=context(root),
            sandbox_trial_plan=plan_value,
            sandbox_trial_license=license_value(plan_value, report_value, source),
            sandbox_trial_report=report_value,
        )
        assert result.status == BLOCKED and "sandbox_trial_report_digest_invalid" in result.blockers

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "diverse_bounded_evolution_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        source["world"]["world_model_id"] = "tampered"
        write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", source["world"])
        result = build_licensed_sandbox_lineage_trial(
            runtime_context=context(root),
            sandbox_trial_plan=plan_value,
            sandbox_trial_license=license_value(plan_value, report_value, source),
            sandbox_trial_report=report_value,
        )
        assert result.status == BLOCKED and "sandbox_trial_source_world_invalid" in result.blockers

    manifest = json.loads((ROOT / "manifests/qi_licensed_sandbox_lineage_trial_v0_16.json").read_text())
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_licensed_sandbox_lineage_trial_v0_16 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
