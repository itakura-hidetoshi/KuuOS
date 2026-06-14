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
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_36_model_state_rollback_executor import (
    build_physical_quantum_qi_v13_36_model_state_rollback_executor,
    compute_model_state_rollback_plan_digest,
)
from scripts.check_physical_quantum_qi_v13_35_model_state_feedback_activation import (
    activation_license as v13_35_license,
    prepare_v13_34,
    run as run_v13_35,
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


def prepare_v13_35(root: pathlib.Path, mutation_id: str) -> dict[str, Any]:
    prepare_v13_34(root, mutation_id)
    result = run_v13_35(root, v13_35_license())
    assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_35_MODEL_STATE_FEEDBACK_ACTIVATION_READY", result
    return result


def rollback_plan(
    root: pathlib.Path,
    rollback_id: str,
    mutation_id: str,
    *,
    expected_digest: str | None = None,
    activation_digest: str | None = None,
) -> dict[str, Any]:
    world = read_json(root / "physical_quantum_qi_world_model_state.json")
    activation = read_json(root / "physical_quantum_qi_v13_35_model_state_feedback_activation_record.json")
    plan = {
        "version": "physical_quantum_qi_model_state_rollback_plan_v13_36",
        "rollback_id": rollback_id,
        "mutation_id": mutation_id,
        "reason": "restore licensed pre-mutation WORLD model snapshot",
        "restore_snapshot_exactly": True,
        "expected_current_world_model_digest": expected_digest if expected_digest is not None else compute_world_model_digest(world),
        "source_v13_35_activation_record_digest": activation_digest if activation_digest is not None else str(activation.get("model_state_feedback_activation_record_digest", "")),
    }
    plan["rollback_plan_digest"] = compute_model_state_rollback_plan_digest(plan)
    return plan


def license_packet(plan: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_36_MODEL_STATE_ROLLBACK_EXECUTOR_LICENSE_READY",
        "v13_35_activation_record_read_allowed": True,
        "v13_34_mutation_ledger_read_allowed": True,
        "rollback_snapshot_read_allowed": True,
        "world_model_state_read_allowed": True,
        "world_model_state_write_allowed": True,
        "rollback_ledger_append_allowed": True,
        "compensation_feedback_write_allowed": True,
        "compensation_feedback_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "explicit_model_state_rollback_allowed": True,
        "bound_rollback_plan_digest": plan["rollback_plan_digest"],
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path, plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_36_model_state_rollback_executor_enabled": True,
        "apply_physical_quantum_qi_v13_36_model_state_rollback_executor": True,
        "runtime_root": str(root),
        "model_state_rollback_plan": plan,
    }


def run(root: pathlib.Path, plan: dict[str, Any], license_value: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_36_model_state_rollback_executor(
        runtime_context=context(root, plan),
        v13_36_model_state_rollback_executor_license=license_value,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        mutation_id = "rollback-success-mutation"
        prepare_v13_35(root, mutation_id)
        snapshot = read_json(root / f"physical_quantum_qi_world_model_rollback_snapshot_{mutation_id}.json")
        changed = read_json(root / "physical_quantum_qi_world_model_state.json")
        plan = rollback_plan(root, "rollback-success-001", mutation_id)
        result = run(root, plan, license_packet(plan))
        assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_36_MODEL_STATE_ROLLBACK_EXECUTOR_READY", result
        assert result["rollback_status"] == "model_state_rollback_applied"
        assert result["world_model_restored"] is True
        assert result["rollback_ledger_appended"] is True
        assert result["compensation_feedback_appended"] is True
        assert result["before_rollback_world_model_digest"] == compute_world_model_digest(changed)
        restored = read_json(root / "physical_quantum_qi_world_model_state.json")
        assert restored == snapshot["world_model_state"]
        assert result["restored_world_model_digest"] == snapshot["before_world_model_digest"]
        assert compute_world_model_digest(restored) == result["restored_world_model_digest"]
        rollback_record = latest(root / "physical_quantum_qi_world_model_rollback_ledger.jsonl")
        compensation = read_json(root / "physical_quantum_qi_world_model_rollback_compensation_feedback.json")
        compensation_record = latest(root / "physical_quantum_qi_world_model_rollback_compensation_feedback_ledger.jsonl")
        assert rollback_record["record_digest"] == result["rollback_record_digest"]
        assert rollback_record["before_rollback_world_model_digest"] == result["before_rollback_world_model_digest"]
        assert rollback_record["restored_world_model_digest"] == result["restored_world_model_digest"]
        assert compensation["feedback_status"] == "process_tensor_feedback_compensate_rollback"
        assert compensation["process_tensor_feedback_kernel"]["path_weight_delta"] == -1
        assert compensation["process_tensor_feedback_kernel"]["memory_feedback_weight"] == 1
        assert compensation["process_tensor_feedback_kernel"]["external_backaction_weight"] == 1
        assert compensation["process_tensor_feedback_kernel"]["next_cycle_amplitude_delta"] == 0
        assert compensation["observed_effects"]["next_cycle_requires_reassessment"] is True
        assert compensation_record["rollback_compensation_feedback_digest"] == result["compensation_feedback_digest"]

        rollback_count = len(records(root / "physical_quantum_qi_world_model_rollback_ledger.jsonl"))
        compensation_count = len(records(root / "physical_quantum_qi_world_model_rollback_compensation_feedback_ledger.jsonl"))
        replay = run(root, plan, license_packet(plan))
        assert replay["status"].endswith("BLOCKED")
        assert "model_state_rollback_id_replay" in replay["blockers"]
        assert "model_state_mutation_already_rolled_back" in replay["blockers"]
        assert len(records(root / "physical_quantum_qi_world_model_rollback_ledger.jsonl")) == rollback_count
        assert len(records(root / "physical_quantum_qi_world_model_rollback_compensation_feedback_ledger.jsonl")) == compensation_count

        root = base / "current_digest_mismatch"
        mutation_id = "rollback-current-digest-mismatch"
        prepare_v13_35(root, mutation_id)
        world_path = root / "physical_quantum_qi_world_model_state.json"
        world = read_json(world_path)
        original_changed = dict(world)
        world["state"]["clinical"]["status"] = "later-unrelated-change"
        world["world_model_digest"] = compute_world_model_digest(world)
        write_json(world_path, world)
        plan = rollback_plan(root, "rollback-current-mismatch", mutation_id)
        result = run(root, plan, license_packet(plan))
        assert result["status"].endswith("BLOCKED")
        assert "world_model_state_not_at_mutation_after_digest" in result["blockers"]
        assert result["world_model_restored"] is False
        assert read_json(world_path) == world
        assert original_changed != world

        root = base / "snapshot_tamper"
        mutation_id = "rollback-snapshot-tamper"
        prepare_v13_35(root, mutation_id)
        world_before_attempt = read_json(root / "physical_quantum_qi_world_model_state.json")
        snapshot_path = root / f"physical_quantum_qi_world_model_rollback_snapshot_{mutation_id}.json"
        snapshot = read_json(snapshot_path)
        snapshot["world_model_state"]["state"]["clinical"]["status"] = "tampered-snapshot"
        write_json(snapshot_path, snapshot)
        plan = rollback_plan(root, "rollback-snapshot-tamper", mutation_id)
        result = run(root, plan, license_packet(plan))
        assert result["status"].endswith("BLOCKED")
        assert "rollback_snapshot_digest_mismatch" in result["blockers"]
        assert "rollback_snapshot_before_state_digest_mismatch" in result["blockers"]
        assert read_json(root / "physical_quantum_qi_world_model_state.json") == world_before_attempt

        root = base / "activation_digest_mismatch"
        mutation_id = "rollback-activation-digest-mismatch"
        prepare_v13_35(root, mutation_id)
        plan = rollback_plan(root, "rollback-activation-mismatch", mutation_id, activation_digest="wrong-activation-digest")
        result = run(root, plan, license_packet(plan))
        assert result["status"].endswith("BLOCKED")
        assert "model_state_rollback_activation_digest_mismatch" in result["blockers"]
        assert result["world_model_restored"] is False

        root = base / "unbound_plan"
        mutation_id = "rollback-unbound-plan"
        prepare_v13_35(root, mutation_id)
        plan = rollback_plan(root, "rollback-unbound", mutation_id)
        result = run(root, plan, license_packet(plan, bound_rollback_plan_digest="different-digest"))
        assert result["status"].endswith("BLOCKED")
        assert "model_state_rollback_plan_not_bound_to_license" in result["blockers"]
        assert result["world_model_restored"] is False

        root = base / "license_block"
        mutation_id = "rollback-license-block"
        prepare_v13_35(root, mutation_id)
        plan = rollback_plan(root, "rollback-license-block", mutation_id)
        result = run(root, plan, license_packet(plan, explicit_model_state_rollback_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert "explicit_model_state_rollback_not_allowed" in result["blockers"]
        assert result["world_model_restored"] is False

    print("physical_quantum_qi_v13_36_model_state_rollback_executor checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
