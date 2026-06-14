#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_41_counterfactual_integration_receipt import (
    build_physical_quantum_qi_v13_41_counterfactual_integration_receipt,
)
from scripts.check_physical_quantum_qi_v13_40_counterfactual_integration_activation import (
    activation_license as v13_40_license,
    prepare_v13_39,
    run as run_v13_40,
)

EXPECTED_WEIGHTING = {
    "path_weight_delta": 0,
    "probe_potential_required": True,
    "barrier_potential_required": False,
    "barrier_blocks_ready_weight": False,
    "memory_feedback_weight": 0,
    "external_backaction_weight": 0,
    "next_cycle_amplitude_delta": 0,
}


def sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def without(value: dict[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value)
    payload.pop(field, None)
    return payload


def valid_digest(value: dict[str, Any], field: str) -> bool:
    return bool(value.get(field)) and value[field] == sha(without(value, field))


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


def prepare_v13_40(root: pathlib.Path, recovery_id: str, rollback_id: str, mutation_id: str) -> dict[str, Any]:
    prepare_v13_39(root, recovery_id, rollback_id, mutation_id)
    result = run_v13_40(root, v13_40_license())
    assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_40_COUNTERFACTUAL_INTEGRATION_ACTIVATION_READY", result
    return result


def bridge_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_LICENSE_READY",
        "v13_4_integration_packet_read_allowed": True,
        "v13_4_integrated_cycle_gate_state_read_allowed": True,
        "v13_4_integrated_admissible_candidate_set_read_allowed": True,
        "v13_5_integration_receipt_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ledger_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_LICENSE_READY",
        "integration_packet_read_allowed": True,
        "integrated_cycle_gate_state_read_allowed": True,
        "integrated_admissible_candidate_set_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_41_COUNTERFACTUAL_INTEGRATION_RECEIPT_LICENSE_READY",
        "v13_40_activation_record_read_allowed": True,
        "v13_40_receipt_read_allowed": True,
        "v13_40_activation_ledger_read_allowed": True,
        "v13_40_annotated_candidate_read_allowed": True,
        "v13_4_integration_packet_read_allowed": True,
        "v13_4_cycle_gate_state_read_allowed": True,
        "v13_4_candidate_set_read_allowed": True,
        "v13_4_integration_ledger_read_allowed": True,
        "v13_17_bridge_invoke_allowed": True,
        "v13_5_receipt_ledger_invoke_allowed": True,
        "annotated_receipt_write_allowed": True,
        "activation_record_write_allowed": True,
        "activation_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v13_17_bridge_license": bridge_license(),
        "v13_5_receipt_ledger_license": ledger_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_41_counterfactual_integration_receipt_enabled": True,
        "apply_physical_quantum_qi_v13_41_counterfactual_integration_receipt": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_value: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_41_counterfactual_integration_receipt(
        runtime_context=context(root),
        v13_41_counterfactual_integration_receipt_license=license_value,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        prepare_v13_40(root, "receipt-recovery-success", "receipt-rollback-success", "receipt-mutation-success")
        result = run(root, activation_license())
        assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_41_COUNTERFACTUAL_INTEGRATION_RECEIPT_READY", result
        assert result["activation_status"] == "counterfactual_integration_receipt_completed"
        assert result["selected_probe_type"] == "observation_debt_probe"
        assert result["candidate_count"] == 4
        assert result["admissible_candidate_count"] == 1
        assert result["integration_status"] == "cycle_gate_reentry_integration_hold"
        assert result["integrated_cycle_gate_status"] == "integrated_cycle_gate_hold"
        assert result["integrated_admissible_candidate_set_status"] == "integrated_admissible_candidate_set_probe"
        assert result["v13_17_bridge_invoked"] is True
        assert result["v13_5_receipt_ledger_invoked"] is True
        assert result["annotated_receipt_written"] is True
        assert result["activation_ledger_appended"] is True
        assert result["v13_5_receipt_record_digest"]

        source = read_json(root / "physical_quantum_qi_v13_40_counterfactual_integration_activation_record.json")
        source_ledger = latest(root / "physical_quantum_qi_counterfactual_integration_activation_ledger.jsonl")
        annotated_candidate = read_json(root / "physical_quantum_qi_v13_40_counterfactual_integration_candidate.json")
        packet = read_json(root / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json")
        cycle_state = read_json(root / "physical_quantum_qi_integrated_cycle_gate_state.json")
        candidate_set = read_json(root / "physical_quantum_qi_integrated_admissible_candidate_set.json")
        integration_record = latest(root / "physical_quantum_qi_cycle_gate_reentry_integration_ledger.jsonl")
        ready_state = read_json(root / "physical_quantum_qi_v13_5_cycle_gate_reentry_integration_receipt_ready_state.json")
        bridge_record = latest(root / "physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge_ledger.jsonl")
        generic_receipt = latest(root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl")
        generic_ledger_receipt = read_json(root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_receipt.json")
        annotated_receipt = read_json(root / "physical_quantum_qi_v13_41_counterfactual_integration_receipt_record.json")
        activation = read_json(root / "physical_quantum_qi_v13_41_counterfactual_integration_receipt_activation_record.json")
        activation_ledger = latest(root / "physical_quantum_qi_counterfactual_integration_receipt_activation_ledger.jsonl")

        assert valid_digest(source, "counterfactual_integration_activation_record_digest")
        assert valid_digest(source_ledger, "record_digest")
        assert valid_digest(annotated_candidate, "counterfactual_integration_candidate_digest")
        assert valid_digest(packet, "cycle_gate_reentry_integration_digest")
        assert valid_digest(cycle_state, "integrated_cycle_gate_state_digest")
        assert valid_digest(candidate_set, "integrated_admissible_candidate_set_digest")
        assert valid_digest(integration_record, "record_digest")
        assert valid_digest(ready_state, "integration_receipt_ready_state_digest")
        assert valid_digest(bridge_record, "record_digest")
        assert valid_digest(generic_receipt, "record_digest")
        assert valid_digest(annotated_receipt, "counterfactual_integration_receipt_record_digest")
        assert valid_digest(activation, "counterfactual_integration_receipt_activation_record_digest")
        assert valid_digest(activation_ledger, "record_digest")
        assert generic_ledger_receipt["record_digest"] == generic_receipt["record_digest"]

        generic_candidate = candidate_set["integrated_candidates"][0]
        receipt_candidate = generic_receipt["integrated_candidates"][0]
        assert generic_receipt["record_type"] == "physical_quantum_qi_cycle_gate_reentry_integration_receipt"
        assert generic_receipt["integration_status"] == "cycle_gate_reentry_integration_hold"
        assert generic_receipt["integrated_cycle_gate_status"] == "integrated_cycle_gate_hold"
        assert generic_receipt["integrated_admissible_candidate_set_status"] == "integrated_admissible_candidate_set_probe"
        assert generic_receipt["admissible_candidate_count"] == 1
        assert generic_receipt["candidate_weighting"] == EXPECTED_WEIGHTING
        assert receipt_candidate["candidate_id"] == "closed_loop_reentry_probe_candidate"
        assert receipt_candidate["candidate_mode"] == "probe_candidate"
        assert receipt_candidate["admissibility_status"] == "admissible_candidate_probe_required"
        assert receipt_candidate["candidate_digest"] == generic_candidate["candidate_digest"]

        assert annotated_receipt["record_type"] == "physical_quantum_qi_counterfactual_integration_receipt"
        assert annotated_receipt["receipt_status"] == "counterfactual_integration_receipt_recorded"
        assert annotated_receipt["selected_probe_type"] == "observation_debt_probe"
        assert annotated_receipt["selected_probe_candidate"]["probe_type"] == "observation_debt_probe"
        assert annotated_receipt["candidate_count"] == 4
        assert annotated_receipt["admissible_candidate_count"] == 1
        assert annotated_receipt["candidate_weighting"] == EXPECTED_WEIGHTING
        assert annotated_receipt["generic_integration_candidate"]["candidate_digest"] == receipt_candidate["candidate_digest"]
        assert annotated_receipt["boundary"]["hold_only_integration_preserved"] is True
        assert annotated_receipt["boundary"]["not_direct_execution_authority"] is True
        assert annotated_receipt["boundary"]["not_world_update_authority"] is True
        assert annotated_receipt["boundary"]["requires_future_probe_evaluation"] is True
        assert annotated_receipt["source_digests"]["v13_40_activation_record"] == source[
            "counterfactual_integration_activation_record_digest"
        ]
        assert annotated_receipt["source_digests"]["v13_40_activation_ledger_record"] == source_ledger["record_digest"]
        assert annotated_receipt["source_digests"]["v13_40_annotated_candidate"] == annotated_candidate[
            "counterfactual_integration_candidate_digest"
        ]
        assert annotated_receipt["source_digests"]["v13_4_integration_packet"] == packet[
            "cycle_gate_reentry_integration_digest"
        ]
        assert annotated_receipt["source_digests"]["v13_4_cycle_state"] == cycle_state[
            "integrated_cycle_gate_state_digest"
        ]
        assert annotated_receipt["source_digests"]["v13_4_candidate_set"] == candidate_set[
            "integrated_admissible_candidate_set_digest"
        ]
        assert annotated_receipt["source_digests"]["v13_4_integration_record"] == integration_record["record_digest"]
        assert annotated_receipt["source_digests"]["v13_17_ready_state"] == ready_state[
            "integration_receipt_ready_state_digest"
        ]
        assert annotated_receipt["source_digests"]["v13_17_bridge_record"] == bridge_record["record_digest"]
        assert annotated_receipt["source_digests"]["v13_5_receipt_record"] == generic_receipt["record_digest"]

        assert activation["source_v13_41_annotated_receipt_digest"] == annotated_receipt[
            "counterfactual_integration_receipt_record_digest"
        ]
        assert activation["source_v13_5_receipt_record_digest"] == generic_receipt["record_digest"]
        assert activation_ledger["source_activation_record_digest"] == activation[
            "counterfactual_integration_receipt_activation_record_digest"
        ]
        assert activation_ledger["source_v13_5_receipt_record_digest"] == generic_receipt["record_digest"]
        assert activation_ledger["source_v13_41_annotated_receipt_digest"] == annotated_receipt[
            "counterfactual_integration_receipt_record_digest"
        ]

        activation_count = len(records(root / "physical_quantum_qi_counterfactual_integration_receipt_activation_ledger.jsonl"))
        receipt_count = len(records(root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl"))
        replay = run(root, activation_license())
        assert replay["status"].endswith("BLOCKED")
        assert "counterfactual_integration_receipt_recovery_replay" in replay["blockers"]
        assert replay["v13_17_bridge_invoked"] is False
        assert replay["v13_5_receipt_ledger_invoked"] is False
        assert len(records(root / "physical_quantum_qi_counterfactual_integration_receipt_activation_ledger.jsonl")) == activation_count
        assert len(records(root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl")) == receipt_count

        root = base / "source_digest_tamper"
        prepare_v13_40(root, "receipt-recovery-source", "receipt-rollback-source", "receipt-mutation-source")
        source_path = root / "physical_quantum_qi_v13_40_counterfactual_integration_activation_record.json"
        source_value = read_json(source_path)
        source_value["source_v13_4_integration_record_digest"] = "wrong-integration-record-digest"
        write_json(source_path, source_value)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_40_activation_record_digest_invalid" in result["blockers"]
        assert "v13_40_integration_record_digest_mismatch" in result["blockers"]
        assert result["v13_17_bridge_invoked"] is False

        root = base / "annotated_boundary_loss"
        prepare_v13_40(root, "receipt-recovery-boundary", "receipt-rollback-boundary", "receipt-mutation-boundary")
        annotated_path = root / "physical_quantum_qi_v13_40_counterfactual_integration_candidate.json"
        annotated_value = read_json(annotated_path)
        annotated_value["boundary"]["failed_path_not_reinforced"] = False
        write_json(annotated_path, annotated_value)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_40_annotated_candidate_digest_invalid" in result["blockers"]
        assert "v13_40_annotated_candidate_boundary_failed_path_not_reinforced_missing" in result["blockers"]
        assert result["v13_17_bridge_invoked"] is False

        root = base / "packet_tamper"
        prepare_v13_40(root, "receipt-recovery-packet", "receipt-rollback-packet", "receipt-mutation-packet")
        packet_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json"
        packet_value = read_json(packet_path)
        packet_value["candidate_weighting"]["path_weight_delta"] = 1
        write_json(packet_path, packet_value)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_4_packet_weighting_invalid" in result["blockers"]
        assert "v13_4_packet_digest_invalid" in result["blockers"]
        assert result["v13_17_bridge_invoked"] is False

        root = base / "nested_bridge_license_block"
        prepare_v13_40(root, "receipt-recovery-bridge", "receipt-rollback-bridge", "receipt-mutation-bridge")
        broken_bridge = bridge_license()
        broken_bridge["v13_4_integration_packet_read_allowed"] = False
        result = run(root, activation_license(v13_17_bridge_license=broken_bridge))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_17_bridge_invoked"] is True
        assert result["v13_5_receipt_ledger_invoked"] is False
        assert "v13_17_bridge_not_ready" in result["blockers"]

        root = base / "nested_ledger_license_block"
        prepare_v13_40(root, "receipt-recovery-ledger", "receipt-rollback-ledger", "receipt-mutation-ledger")
        broken_ledger = ledger_license()
        broken_ledger["receipt_ledger_append_allowed"] = False
        result = run(root, activation_license(v13_5_receipt_ledger_license=broken_ledger))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_17_bridge_invoked"] is True
        assert result["v13_5_receipt_ledger_invoked"] is True
        assert "v13_5_receipt_ledger_not_ready" in result["blockers"]
        assert result["activation_ledger_appended"] is False

        root = base / "top_license_block"
        prepare_v13_40(root, "receipt-recovery-license", "receipt-rollback-license", "receipt-mutation-license")
        result = run(root, activation_license(v13_5_receipt_ledger_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert "v13_5_receipt_ledger_invoke_not_allowed" in result["blockers"]
        assert result["v13_17_bridge_invoked"] is False
        assert result["v13_5_receipt_ledger_invoked"] is False

    print("physical_quantum_qi_v13_41_counterfactual_integration_receipt checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
