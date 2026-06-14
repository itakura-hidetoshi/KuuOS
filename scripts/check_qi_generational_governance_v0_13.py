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

from runtime.kuuos_indra_qi_generational_governance_core_v0_13 import LICENSE_VERSION, PLAN_VERSION, REPLAY_VERSION, REQUIRED_BOUNDARY, plan_digest, replay_digest, sha
from runtime.kuuos_indra_qi_generational_governance_runtime_v0_13 import BLOCKED, READY, build_governance


def write(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(dict(value), sort_keys=True), encoding="utf-8")


def source(root: pathlib.Path, generation: int, previous_state: str, source_v011: str, values: Mapping[str, Any]) -> dict[str, Any]:
    runner = "runner-a"
    target = sha({"target": generation})
    handoff = {"version": "indra_qi_bounded_cycle_handoff_packet_v0_12", "runner_id": runner, "generation_run_id": f"run-{generation}", "generation_index": generation, "completed_generations": generation + 1, "max_generations": 8, "runner_status": "bounded_cycle_ready_for_next_generation", "stop_reason": "", "source_v0_11_handoff_packet_digest": source_v011, "target_v0_11_handoff_packet_digest": target, "dynamic_metrics": dict(values), "epoch": generation}
    handoff["generation_handoff_digest"] = sha(handoff)
    record = {"version": "indra_qi_bounded_cycle_record_v0_12", "runner_id": runner, "generation_run_id": handoff["generation_run_id"], "generation_index": generation, "source_generation_handoff_digest": handoff["generation_handoff_digest"], "target_v0_11_handoff_packet_digest": target, "runner_status": handoff["runner_status"], "epoch": generation}
    record["generation_record_digest"] = sha(record)
    state = {"version": "indra_qi_bounded_generational_cycle_state_v0_12", "runner_id": runner, "runner_status": handoff["runner_status"], "completed_generations": generation + 1, "last_generation_run_id": handoff["generation_run_id"], "last_generation_record_digest": record["generation_record_digest"], "latest_v0_11_handoff_packet_digest": target, "dynamic_metrics": dict(values), "prev_runner_state_digest": previous_state, "epoch": generation}
    state["runner_state_digest"] = sha(state)
    write(root / "indra_qi_bounded_cycle_handoff_v0_12.json", handoff)
    write(root / "indra_qi_bounded_cycle_record_v0_12.json", record)
    write(root / "indra_qi_bounded_cycle_state_v0_12.json", state)
    return {"handoff": handoff, "record": record, "state": state}


def plan(value: Mapping[str, Any], review: str) -> dict[str, Any]:
    result = {"version": PLAN_VERSION, "monitor_id": "monitor-a", "review_run_id": review, "runner_id": "runner-a", "expected_source_v0_12_runner_state_digest": value["state"]["runner_state_digest"], "governance_policy": {"minimum_window_generations": 2, "maximum_window_generations": 8, "minimum_replay_cases": 2, "minimum_replay_pass_ratio": 1.0, "maximum_observation_debt_drift": 0.05, "maximum_intervention_residue_drift": 0.05, "maximum_recoverability_loss": 0.05, "regression_epsilon": 0.01, "maximum_regression_steps": 1, "maximum_collapse_pressure": 0.35, "quarantine_collapse_pressure": 0.75, "quarantine_consecutive_regressions": 3, "collapse_weights": {"observation_debt": 0.35, "recoverability_loss": 0.40, "intervention_residue": 0.25}}, "boundary": dict(REQUIRED_BOUNDARY)}
    result["governance_plan_digest"] = plan_digest(result)
    return result


def license_value(plan_value: Mapping[str, Any], value: Mapping[str, Any]) -> dict[str, Any]:
    return {"version": LICENSE_VERSION, "license_id": "license-" + str(plan_value["review_run_id"]), "bound_governance_plan_digest": plan_value["governance_plan_digest"], "bound_source_v0_12_runner_state_digest": value["state"]["runner_state_digest"], "bound_source_generation_handoff_digest": value["handoff"]["generation_handoff_digest"], "state_write_allowed": True, "ledger_append_allowed": True, "recommendation_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True, "execution_authority_granted": False, "truth_authority_granted": False, "direct_promotion_authority_granted": False, "direct_rollback_authority_granted": False, "direct_quarantine_authority_granted": False}


def replay(plan_value: Mapping[str, Any], value: Mapping[str, Any], passed: bool = True) -> dict[str, Any]:
    handoff = value["handoff"]["generation_handoff_digest"]
    cases = []
    for index in range(2):
        expected = sha({"case": index, "source": handoff})
        cases.append({"case_id": f"case-{index}", "source_generation_handoff_digest": handoff, "replay_input_digest": sha({"input": index}), "expected_output_digest": expected, "observed_output_digest": expected if passed else sha({"wrong": index})})
    result = {"version": REPLAY_VERSION, "review_run_id": plan_value["review_run_id"], "source_generation_handoff_digest": handoff, "cases": cases}
    result["replay_report_digest"] = replay_digest(result)
    return result


def context(root: pathlib.Path) -> dict[str, Any]:
    return {"runtime_root": str(root), "indra_qi_generational_governance_v0_13_enabled": True, "apply_indra_qi_generational_governance_v0_13": True}


def run(root: pathlib.Path, generation: int, previous_state: str, source_v011: str, values: Mapping[str, Any], passed: bool = True):
    value = source(root, generation, previous_state, source_v011, values)
    plan_value = plan(value, f"review-{generation}")
    result = build_governance(runtime_context=context(root), governance_plan=plan_value, governance_license=license_value(plan_value, value), replay_report=replay(plan_value, value, passed))
    return value, plan_value, result


def main() -> int:
    stable = {"state_count": 2, "maximum_observation_debt": 0.20, "minimum_recoverability_reserve": 0.80, "maximum_intervention_residue": 0.15}
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        first, _, result = run(root, 0, "GENESIS", "GENESIS-V011", stable)
        assert result.status == READY and result.decision == "hold_for_observation"
        before = [(root / name).read_bytes() for name in ("indra_qi_bounded_cycle_handoff_v0_12.json", "indra_qi_bounded_cycle_record_v0_12.json", "indra_qi_bounded_cycle_state_v0_12.json")]
        improved = {"state_count": 2, "maximum_observation_debt": 0.18, "minimum_recoverability_reserve": 0.82, "maximum_intervention_residue": 0.14}
        second, second_plan, promoted = run(root, 1, first["state"]["runner_state_digest"], first["handoff"]["target_v0_11_handoff_packet_digest"], improved)
        assert promoted.status == READY and promoted.decision == "promote_bounded"
        recommendation = json.loads((root / "indra_qi_generational_governance_recommendation_v0_13.json").read_text())
        assert recommendation["recommendation_only"] and not recommendation["direct_promotion_authority"]
        assert before != [(root / name).read_bytes() for name in ("indra_qi_bounded_cycle_handoff_v0_12.json", "indra_qi_bounded_cycle_record_v0_12.json", "indra_qi_bounded_cycle_state_v0_12.json")]
        same = build_governance(runtime_context=context(root), governance_plan=second_plan, governance_license=license_value(second_plan, second), replay_report=replay(second_plan, second))
        assert same.status == BLOCKED
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        first, _, _ = run(root, 0, "GENESIS", "GENESIS-V011", stable)
        _, _, failed = run(root, 1, first["state"]["runner_state_digest"], first["handoff"]["target_v0_11_handoff_packet_digest"], stable, False)
        assert failed.decision == "rollback_recommended"
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        first, _, _ = run(root, 0, "GENESIS", "GENESIS-V011", stable)
        collapse = {"state_count": 2, "maximum_observation_debt": 0.95, "minimum_recoverability_reserve": 0.05, "maximum_intervention_residue": 0.95}
        _, _, quarantined = run(root, 1, first["state"]["runner_state_digest"], first["handoff"]["target_v0_11_handoff_packet_digest"], collapse)
        assert quarantined.decision == "quarantine_recommended"
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        first, _, _ = run(root, 0, "GENESIS", "GENESIS-V011", stable)
        _, _, broken = run(root, 1, first["state"]["runner_state_digest"], "WRONG-LINEAGE", stable)
        assert broken.status == BLOCKED and "generational_governance_v0_11_lineage_discontinuous" in broken.blockers
    manifest = json.loads((ROOT / "manifests/qi_generational_governance_v0_13.json").read_text())
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_generational_governance_v0_13 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
