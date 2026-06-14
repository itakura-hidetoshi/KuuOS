#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_34_world_model_mutation import compute_world_model_digest
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_37_counterfactual_recovery_reentry import (
    build_physical_quantum_qi_v13_37_counterfactual_recovery_reentry,
    compute_counterfactual_recovery_plan_digest,
)
from scripts.check_physical_quantum_qi_v13_36_model_state_rollback_executor import (
    license_packet as v13_36_license,
    prepare_v13_35,
    rollback_plan,
    run as run_v13_36,
)


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def records(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def latest(path: pathlib.Path) -> dict[str, Any]:
    values = records(path)
    return values[-1] if values else {}


def prepare_v13_36(root: pathlib.Path, mutation_id: str, rollback_id: str) -> dict[str, Any]:
    prepare_v13_35(root, mutation_id)
    plan = rollback_plan(root, rollback_id, mutation_id)
    result = run_v13_36(root, plan, v13_36_license(plan))
    assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_36_MODEL_STATE_ROLLBACK_EXECUTOR_READY", result
    return result


def v13_0_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_LICENSE_READY",
        "reentry_weighting_state_read_allowed": True,
        "closed_loop_reentry_packet_write_allowed": True,
        "candidate_weighting_cycle_state_write_allowed": True,
        "closed_loop_reentry_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def v13_1_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_LICENSE_READY",
        "closed_loop_reentry_packet_read_allowed": True,
        "candidate_weighting_cycle_state_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def recovery_plan(
    recovery_id: str,
    rollback_id: str,
    mutation_id: str,
    *,
    candidates: list[str] | None = None,
    excluded: list[str] | None = None,
) -> dict[str, Any]:
    plan = {
        "version": "physical_quantum_qi_counterfactual_recovery_plan_v13_37",
        "recovery_id": recovery_id,
        "rollback_id": rollback_id,
        "mutation_id": mutation_id,
        "reason": "select an alternative probe after rollback compensation",
        "probe_only_reentry": True,
        "preferred_probe_type": "safe_reentry_window_probe",
        "target_time_slice": "rollback_reassessment_window",
        "candidate_probe_types": candidates
        if candidates is not None
        else [
            "safe_reentry_window_probe",
            "recoverability_branch_probe",
            "observation_debt_probe",
            "memory_kernel_probe",
        ],
        "excluded_probe_types": excluded or [],
    }
    plan["recovery_plan_digest"] = compute_counterfactual_recovery_plan_digest(plan)
    return plan


def license_packet(plan: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_37_COUNTERFACTUAL_RECOVERY_REENTRY_LICENSE_READY",
        "v13_36_rollback_receipt_read_allowed": True,
        "rollback_ledger_read_allowed": True,
        "compensation_feedback_read_allowed": True,
        "compensation_feedback_ledger_read_allowed": True,
        "world_model_state_read_allowed": True,
        "v13_35_execution_record_read_allowed": True,
        "counterfactual_packet_write_allowed": True,
        "reentry_weighting_state_write_allowed": True,
        "v13_0_reentry_invoke_allowed": True,
        "v13_1_receipt_ledger_invoke_allowed": True,
        "recovery_ledger_append_allowed": True,
        "activation_record_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "bound_recovery_plan_digest": plan["recovery_plan_digest"],
        "v13_0_reentry_license": v13_0_license(),
        "v13_1_receipt_ledger_license": v13_1_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path, plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_37_counterfactual_recovery_reentry_enabled": True,
        "apply_physical_quantum_qi_v13_37_counterfactual_recovery_reentry": True,
        "runtime_root": str(root),
        "counterfactual_recovery_plan": plan,
    }


def run(root: pathlib.Path, plan: dict[str, Any], license_value: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_37_counterfactual_recovery_reentry(
        runtime_context=context(root, plan),
        v13_37_counterfactual_recovery_reentry_license=license_value,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        mutation_id = "cf-recovery-mutation"
        rollback_id = "cf-recovery-rollback"
        prepare_v13_36(root, mutation_id, rollback_id)
        plan = recovery_plan("cf-recovery-success-001", rollback_id, mutation_id)
        result = run(root, plan, license_packet(plan))
        assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_37_COUNTERFACTUAL_RECOVERY_REENTRY_READY", result
        assert result["recovery_status"] == "counterfactual_recovery_reentry_completed"
        assert result["selected_probe_type"] == "observation_debt_probe"
        assert result["candidate_count"] == 4
        assert result["counterfactual_lattice_ready"] is True
        assert result["v13_0_reentry_invoked"] is True
        assert result["v13_1_receipt_ledger_invoked"] is True
        assert result["closed_loop_reentry_status"] == "closed_loop_reentry_probe_opened"
        assert result["closed_loop_receipt_record_digest"]
        assert result["recovery_ledger_appended"] is True

        packet = read_json(root / "physical_quantum_qi_v13_37_counterfactual_recovery_packet.json")
        reentry_state = read_json(root / "physical_quantum_qi_reentry_weighting_state.json")
        closed_loop_packet = read_json(root / "physical_quantum_qi_closed_loop_path_integral_reentry_packet.json")
        cycle_state = read_json(root / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json")
        closed_loop_record = latest(root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl")
        activation = read_json(root / "physical_quantum_qi_v13_37_counterfactual_recovery_reentry_record.json")
        recovery_record = latest(root / "physical_quantum_qi_counterfactual_recovery_ledger.jsonl")

        assert packet["selected_probe_type"] == "observation_debt_probe"
        assert packet["boundary"]["rollback_path_not_reinforced"] is True
        assert packet["boundary"]["not_world_update_authority"] is True
        assert reentry_state["reentry_weighting_action"] == "open_probe_potential"
        assert reentry_state["candidate_weighting"] == {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
        assert closed_loop_packet["closed_loop_reentry_status"] == "closed_loop_reentry_probe_opened"
        assert cycle_state["candidate_weighting_cycle_ready"] is True
        assert closed_loop_record["record_digest"] == result["closed_loop_receipt_record_digest"]
        assert closed_loop_record["candidate_weighting"]["path_weight_delta"] == 0
        assert closed_loop_record["candidate_weighting"]["probe_potential_required"] is True
        assert activation["source_v13_1_closed_loop_receipt_record_digest"] == closed_loop_record["record_digest"]
        assert recovery_record["source_activation_record_digest"] == activation[
            "counterfactual_recovery_reentry_record_digest"
        ]

        recovery_count = len(records(root / "physical_quantum_qi_counterfactual_recovery_ledger.jsonl"))
        receipt_count = len(records(root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl"))
        replay = run(root, plan, license_packet(plan))
        assert replay["status"].endswith("BLOCKED")
        assert "counterfactual_recovery_id_replay" in replay["blockers"]
        assert "counterfactual_recovery_rollback_already_consumed" in replay["blockers"]
        assert len(records(root / "physical_quantum_qi_counterfactual_recovery_ledger.jsonl")) == recovery_count
        assert len(records(root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl")) == receipt_count

        root = base / "compensation_tamper"
        mutation_id = "cf-compensation-tamper-mutation"
        rollback_id = "cf-compensation-tamper-rollback"
        prepare_v13_36(root, mutation_id, rollback_id)
        compensation_path = root / "physical_quantum_qi_world_model_rollback_compensation_feedback.json"
        compensation = read_json(compensation_path)
        compensation["process_tensor_feedback_kernel"]["path_weight_delta"] = 0
        write_json(compensation_path, compensation)
        plan = recovery_plan("cf-compensation-tamper", rollback_id, mutation_id)
        result = run(root, plan, license_packet(plan))
        assert result["status"].endswith("BLOCKED")
        assert result["counterfactual_lattice_ready"] is False
        assert "v13_36_compensation_feedback_digest_invalid" in result["blockers"]
        assert "v13_36_compensation_feedback_ledger_mismatch" in result["blockers"]
        assert "v13_36_compensation_path_weight_not_negative" in result["blockers"]
        assert not (root / "physical_quantum_qi_v13_37_counterfactual_recovery_packet.json").is_file()

        root = base / "world_digest_mismatch"
        mutation_id = "cf-world-digest-mutation"
        rollback_id = "cf-world-digest-rollback"
        prepare_v13_36(root, mutation_id, rollback_id)
        world_path = root / "physical_quantum_qi_world_model_state.json"
        world = read_json(world_path)
        world["state"]["clinical"]["status"] = "post-rollback-unrelated-change"
        world["world_model_digest"] = compute_world_model_digest(world)
        write_json(world_path, world)
        plan = recovery_plan("cf-world-digest", rollback_id, mutation_id)
        result = run(root, plan, license_packet(plan))
        assert result["status"].endswith("BLOCKED")
        assert "restored_world_model_receipt_digest_mismatch" in result["blockers"]
        assert "restored_world_model_record_digest_mismatch" in result["blockers"]
        assert result["v13_0_reentry_invoked"] is False

        root = base / "no_candidates"
        mutation_id = "cf-no-candidates-mutation"
        rollback_id = "cf-no-candidates-rollback"
        prepare_v13_36(root, mutation_id, rollback_id)
        plan = recovery_plan(
            "cf-no-candidates",
            rollback_id,
            mutation_id,
            candidates=["safe_reentry_window_probe"],
            excluded=["safe_reentry_window_probe"],
        )
        result = run(root, plan, license_packet(plan))
        assert result["status"].endswith("BLOCKED")
        assert "counterfactual_recovery_candidate_probe_types_missing" in result["blockers"]
        assert result["counterfactual_lattice_ready"] is False

        root = base / "execution_context_loss"
        mutation_id = "cf-context-loss-mutation"
        rollback_id = "cf-context-loss-rollback"
        prepare_v13_36(root, mutation_id, rollback_id)
        execution_path = root / "physical_quantum_qi_guarded_transition_execution_record.json"
        execution = read_json(execution_path)
        execution["process_tensor_context"]["memory_kernel_digest"] = ""
        write_json(execution_path, execution)
        plan = recovery_plan("cf-context-loss", rollback_id, mutation_id)
        result = run(root, plan, license_packet(plan))
        assert result["status"].endswith("BLOCKED")
        assert "process_tensor_context_memory_kernel_digest_missing" in result["blockers"]
        assert result["v13_0_reentry_invoked"] is False

        root = base / "unbound_plan"
        mutation_id = "cf-unbound-mutation"
        rollback_id = "cf-unbound-rollback"
        prepare_v13_36(root, mutation_id, rollback_id)
        plan = recovery_plan("cf-unbound", rollback_id, mutation_id)
        result = run(root, plan, license_packet(plan, bound_recovery_plan_digest="wrong-plan-digest"))
        assert result["status"].endswith("BLOCKED")
        assert "counterfactual_recovery_plan_not_bound_to_license" in result["blockers"]
        assert result["counterfactual_lattice_ready"] is False

        root = base / "license_block"
        mutation_id = "cf-license-block-mutation"
        rollback_id = "cf-license-block-rollback"
        prepare_v13_36(root, mutation_id, rollback_id)
        plan = recovery_plan("cf-license-block", rollback_id, mutation_id)
        result = run(root, plan, license_packet(plan, v13_0_reentry_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert "v13_0_reentry_invoke_not_allowed" in result["blockers"]
        assert result["v13_0_reentry_invoked"] is False
        assert result["v13_1_receipt_ledger_invoked"] is False

    print("physical_quantum_qi_v13_37_counterfactual_recovery_reentry checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
