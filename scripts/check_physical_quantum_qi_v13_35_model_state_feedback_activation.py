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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_35_model_state_feedback_activation import (
    build_physical_quantum_qi_v13_35_model_state_feedback_activation,
)
from scripts.check_physical_quantum_qi_v13_34_world_model_mutation import (
    initial_world_state,
    license_packet as v13_34_license,
    mutation_plan,
    prepare_v13_33,
    run as run_v13_34,
)


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def jsonl_records(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def latest_jsonl(path: pathlib.Path) -> dict[str, Any]:
    records = jsonl_records(path)
    return records[-1] if records else {}


def v12_7_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_LICENSE_READY",
        "guarded_transition_execution_record_read_allowed": True,
        "next_cycle_state_read_allowed": True,
        "memory_consumption_ledger_read_allowed": True,
        "external_state_mutation_ledger_read_allowed": True,
        "process_tensor_feedback_append_allowed": True,
        "path_integral_feedback_state_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def v12_8_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_LICENSE_READY",
        "process_tensor_execution_feedback_packet_read_allowed": True,
        "path_integral_feedback_state_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_35_MODEL_STATE_FEEDBACK_ACTIVATION_LICENSE_READY",
        "v13_34_mutation_receipt_read_allowed": True,
        "v13_34_mutation_ledger_read_allowed": True,
        "world_model_state_read_allowed": True,
        "rollback_snapshot_read_allowed": True,
        "guarded_execution_intent_packet_read_allowed": True,
        "execution_effect_record_write_allowed": True,
        "next_cycle_state_write_allowed": True,
        "memory_feedback_append_allowed": True,
        "external_backaction_append_allowed": True,
        "v12_7_feedback_invoke_allowed": True,
        "v12_8_receipt_ledger_invoke_allowed": True,
        "activation_record_write_allowed": True,
        "activation_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v12_7_feedback_license": v12_7_license(),
        "v12_8_receipt_ledger_license": v12_8_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_35_model_state_feedback_activation_enabled": True,
        "apply_physical_quantum_qi_v13_35_model_state_feedback_activation": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_value: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_35_model_state_feedback_activation(
        runtime_context=context(root),
        v13_35_model_state_feedback_activation_license=license_value,
    ).to_dict()


def prepare_v13_34(root: pathlib.Path, mutation_id: str) -> dict[str, Any]:
    prepare_v13_33(root, "reinforce")
    initial_world_state(root)
    plan = mutation_plan(
        root,
        mutation_id,
        [
            {"op": "set", "path": "/state/clinical/status", "value": "feedback-observed"},
            {"op": "increment", "path": "/state/network/harmony_score", "value": 0.1},
        ],
    )
    result = run_v13_34(root, plan, v13_34_license(plan))
    assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_34_WORLD_MODEL_MUTATION_READY", result
    return result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        mutation = prepare_v13_34(root, "feedback-success-001")
        result = run(root, activation_license())
        assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_35_MODEL_STATE_FEEDBACK_ACTIVATION_READY", result
        assert result["activation_status"] == "model_state_feedback_activation_completed"
        assert result["mutation_id"] == "feedback-success-001"
        assert result["rollback_ready"] is True
        assert result["execution_effects_published"] is True
        assert result["v12_7_feedback_invoked"] is True
        assert result["v12_8_receipt_ledger_invoked"] is True
        assert result["feedback_status"] == "process_tensor_feedback_reinforce_next_cycle"
        assert result["feedback_record_digest"]
        assert result["activation_ledger_appended"] is True

        execution = read_json(root / "physical_quantum_qi_guarded_transition_execution_record.json")
        next_cycle = read_json(root / "physical_quantum_qi_next_cycle_state.json")
        memory = latest_jsonl(root / "physical_quantum_qi_memory_consumption_ledger.jsonl")
        external = latest_jsonl(root / "physical_quantum_qi_external_state_mutation_ledger.jsonl")
        feedback_packet = read_json(root / "physical_quantum_qi_process_tensor_execution_feedback_packet.json")
        feedback_state = read_json(root / "physical_quantum_qi_path_integral_feedback_state.json")
        feedback_receipt = latest_jsonl(root / "physical_quantum_qi_process_tensor_feedback_receipt_ledger.jsonl")
        activation_record = read_json(root / "physical_quantum_qi_v13_35_model_state_feedback_activation_record.json")
        activation_ledger = latest_jsonl(root / "physical_quantum_qi_model_state_feedback_activation_ledger.jsonl")

        assert execution["execution_status"] == "guarded_transition_executed"
        assert execution["effects"] == {
            "internal_transition_record": True,
            "next_cycle_state_update": True,
            "memory_consumption": True,
            "external_state_mutation": True,
        }
        assert next_cycle["next_cycle_started"] is True
        assert memory["memory_consumed"] is True
        assert external["external_state_mutated"] is True
        assert external["before_world_model_digest"] == mutation["before_world_model_digest"]
        assert external["after_world_model_digest"] == mutation["after_world_model_digest"]
        assert external["rollback_ready"] is True
        assert feedback_packet["feedback_status"] == "process_tensor_feedback_reinforce_next_cycle"
        assert feedback_state["path_integral_feedback_ready"] is True
        assert feedback_state["source_process_tensor_execution_feedback_digest"] == feedback_packet[
            "process_tensor_execution_feedback_digest"
        ]
        assert feedback_receipt["record_digest"] == result["feedback_record_digest"]
        assert activation_record["source_process_tensor_feedback_receipt_digest"] == feedback_receipt["record_digest"]
        assert activation_ledger["source_activation_record_digest"] == activation_record[
            "model_state_feedback_activation_record_digest"
        ]

        activation_count = len(jsonl_records(root / "physical_quantum_qi_model_state_feedback_activation_ledger.jsonl"))
        feedback_count = len(jsonl_records(root / "physical_quantum_qi_process_tensor_feedback_receipt_ledger.jsonl"))
        replay = run(root, activation_license())
        assert replay["status"].endswith("BLOCKED")
        assert "model_state_feedback_activation_replay" in replay["blockers"]
        assert len(jsonl_records(root / "physical_quantum_qi_model_state_feedback_activation_ledger.jsonl")) == activation_count
        assert len(jsonl_records(root / "physical_quantum_qi_process_tensor_feedback_receipt_ledger.jsonl")) == feedback_count

        root = base / "world_digest_mismatch"
        prepare_v13_34(root, "feedback-world-digest-mismatch")
        world_path = root / "physical_quantum_qi_world_model_state.json"
        world = read_json(world_path)
        world["state"]["clinical"]["status"] = "tampered-after-write"
        write_json(world_path, world)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["execution_effects_published"] is False
        assert "world_model_state_embedded_digest_mismatch" in result["blockers"]
        assert not (root / "physical_quantum_qi_guarded_transition_execution_record.json").is_file()

        root = base / "snapshot_mismatch"
        prepare_v13_34(root, "feedback-snapshot-mismatch")
        snapshot_path = root / "physical_quantum_qi_world_model_rollback_snapshot_feedback-snapshot-mismatch.json"
        snapshot = read_json(snapshot_path)
        snapshot["before_world_model_digest"] = "wrong-before-digest"
        write_json(snapshot_path, snapshot)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["rollback_ready"] is False
        assert "rollback_snapshot_digest_mismatch" in result["blockers"]
        assert "rollback_snapshot_before_state_digest_mismatch" in result["blockers"]
        assert result["execution_effects_published"] is False

        root = base / "receipt_mismatch"
        prepare_v13_34(root, "feedback-receipt-mismatch")
        receipt_path = root / "physical_quantum_qi_v13_34_world_model_mutation_receipt.json"
        receipt = read_json(receipt_path)
        receipt["after_world_model_digest"] = "wrong-after-digest"
        write_json(receipt_path, receipt)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_34_after_world_model_digest_mismatch" in result["blockers"]
        assert result["v12_7_feedback_invoked"] is False

        root = base / "nested_license_block"
        prepare_v13_34(root, "feedback-nested-license-block")
        broken_v12_7 = v12_7_license()
        broken_v12_7["external_state_mutation_ledger_read_allowed"] = False
        result = run(root, activation_license(v12_7_feedback_license=broken_v12_7))
        assert result["status"].endswith("BLOCKED")
        assert "v12_7_feedback_external_state_mutation_ledger_read_not_allowed" in result["blockers"]
        assert result["execution_effects_published"] is False
        assert result["v12_7_feedback_invoked"] is False

        root = base / "top_license_block"
        prepare_v13_34(root, "feedback-top-license-block")
        result = run(root, activation_license(external_backaction_append_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert "external_backaction_append_not_allowed" in result["blockers"]
        assert result["execution_effects_published"] is False

    print("physical_quantum_qi_v13_35_model_state_feedback_activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
