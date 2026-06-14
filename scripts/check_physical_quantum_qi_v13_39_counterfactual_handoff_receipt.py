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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_39_counterfactual_handoff_receipt import (
    build_physical_quantum_qi_v13_39_counterfactual_handoff_receipt,
)
from scripts.check_physical_quantum_qi_v13_38_counterfactual_cycle_handoff import (
    activation_license as v13_38_license,
    prepare_v13_37,
    run as run_v13_38,
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


def prepare_v13_38(root: pathlib.Path, recovery_id: str, rollback_id: str, mutation_id: str) -> dict[str, Any]:
    prepare_v13_37(root, recovery_id, rollback_id, mutation_id)
    result = run_v13_38(root, v13_38_license())
    assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_38_COUNTERFACTUAL_CYCLE_HANDOFF_READY", result
    return result


def bridge_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_LICENSE_READY",
        "v13_2_handoff_packet_read_allowed": True,
        "v13_2_cycle_gate_input_read_allowed": True,
        "v13_2_admissible_candidate_set_seed_read_allowed": True,
        "v13_3_handoff_receipt_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ledger_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_LICENSE_READY",
        "handoff_packet_read_allowed": True,
        "cycle_gate_input_read_allowed": True,
        "admissible_candidate_set_seed_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_39_COUNTERFACTUAL_HANDOFF_RECEIPT_LICENSE_READY",
        "v13_38_activation_record_read_allowed": True,
        "v13_38_receipt_read_allowed": True,
        "v13_38_activation_ledger_read_allowed": True,
        "v13_38_annotated_seed_read_allowed": True,
        "v13_2_handoff_packet_read_allowed": True,
        "v13_2_cycle_gate_input_read_allowed": True,
        "v13_2_candidate_seed_read_allowed": True,
        "v13_2_handoff_ledger_read_allowed": True,
        "v13_15_bridge_invoke_allowed": True,
        "v13_3_receipt_ledger_invoke_allowed": True,
        "annotated_receipt_write_allowed": True,
        "activation_record_write_allowed": True,
        "activation_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v13_15_bridge_license": bridge_license(),
        "v13_3_receipt_ledger_license": ledger_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_enabled": True,
        "apply_physical_quantum_qi_v13_39_counterfactual_handoff_receipt": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_value: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_39_counterfactual_handoff_receipt(
        runtime_context=context(root),
        v13_39_counterfactual_handoff_receipt_license=license_value,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        prepare_v13_38(root, "receipt-recovery-success", "receipt-rollback-success", "receipt-mutation-success")
        result = run(root, activation_license())
        assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_39_COUNTERFACTUAL_HANDOFF_RECEIPT_READY", result
        assert result["activation_status"] == "counterfactual_handoff_receipt_completed"
        assert result["selected_probe_type"] == "observation_debt_probe"
        assert result["candidate_count"] == 4
        assert result["handoff_status"] == "candidate_weighting_cycle_handoff_probe"
        assert result["cycle_gate_decision"] == "hold_candidate"
        assert result["admissible_candidate_seed_mode"] == "probe_candidate_seed"
        assert result["v13_15_bridge_invoked"] is True
        assert result["v13_3_receipt_ledger_invoked"] is True
        assert result["annotated_receipt_written"] is True
        assert result["activation_ledger_appended"] is True
        assert result["v13_3_receipt_record_digest"]

        annotated = read_json(root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_record.json")
        activation = read_json(root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_activation_record.json")
        activation_ledger = latest(root / "physical_quantum_qi_counterfactual_handoff_receipt_activation_ledger.jsonl")
        ready_state = read_json(root / "physical_quantum_qi_v13_3_candidate_weighting_cycle_handoff_receipt_ready_state.json")
        bridge_record = latest(root / "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_ledger.jsonl")
        generic_receipt = read_json(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_receipt.json")
        generic_record = latest(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl")
        source = read_json(root / "physical_quantum_qi_v13_38_counterfactual_cycle_handoff_record.json")
        source_seed = read_json(root / "physical_quantum_qi_v13_38_counterfactual_candidate_seed.json")

        assert generic_receipt["record_digest"] == generic_record["record_digest"]
        assert generic_record["record_digest"] == result["v13_3_receipt_record_digest"]
        assert generic_record["record_type"] == "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt"
        assert generic_record["handoff_status"] == "candidate_weighting_cycle_handoff_probe"
        assert generic_record["cycle_gate_decision"] == "hold_candidate"
        assert generic_record["admissible_candidate_seed_mode"] == "probe_candidate_seed"
        assert generic_record["candidate_weighting"] == EXPECTED_WEIGHTING
        assert annotated["record_type"] == "physical_quantum_qi_counterfactual_handoff_receipt"
        assert annotated["receipt_status"] == "counterfactual_handoff_receipt_recorded"
        assert annotated["selected_probe_type"] == "observation_debt_probe"
        assert annotated["selected_probe_candidate"]["probe_type"] == "observation_debt_probe"
        assert annotated["candidate_weighting"] == EXPECTED_WEIGHTING
        assert annotated["boundary"]["failed_path_not_reinforced"] is True
        assert annotated["boundary"]["not_direct_execution_authority"] is True
        assert annotated["boundary"]["not_world_update_authority"] is True
        assert annotated["source_digests"]["v13_38_activation_record"] == source[
            "counterfactual_cycle_handoff_record_digest"
        ]
        assert annotated["source_digests"]["v13_38_annotated_seed"] == source_seed[
            "counterfactual_candidate_seed_digest"
        ]
        assert annotated["source_digests"]["v13_15_ready_state"] == ready_state[
            "handoff_receipt_ready_state_digest"
        ]
        assert annotated["source_digests"]["v13_15_bridge_record"] == bridge_record["record_digest"]
        assert annotated["source_digests"]["v13_3_receipt_record"] == generic_record["record_digest"]
        assert activation["source_v13_39_annotated_receipt_digest"] == annotated[
            "counterfactual_handoff_receipt_record_digest"
        ]
        assert activation["source_v13_3_receipt_record_digest"] == generic_record["record_digest"]
        assert activation_ledger["source_activation_record_digest"] == activation[
            "counterfactual_handoff_receipt_activation_record_digest"
        ]
        assert activation_ledger["source_v13_3_receipt_record_digest"] == generic_record["record_digest"]

        activation_count = len(records(root / "physical_quantum_qi_counterfactual_handoff_receipt_activation_ledger.jsonl"))
        generic_count = len(records(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl"))
        replay = run(root, activation_license())
        assert replay["status"].endswith("BLOCKED")
        assert "counterfactual_handoff_receipt_recovery_replay" in replay["blockers"]
        assert replay["v13_15_bridge_invoked"] is False
        assert replay["v13_3_receipt_ledger_invoked"] is False
        assert len(records(root / "physical_quantum_qi_counterfactual_handoff_receipt_activation_ledger.jsonl")) == activation_count
        assert len(records(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl")) == generic_count

        root = base / "source_digest_tamper"
        prepare_v13_38(root, "receipt-recovery-source", "receipt-rollback-source", "receipt-mutation-source")
        source_path = root / "physical_quantum_qi_v13_38_counterfactual_cycle_handoff_record.json"
        source = read_json(source_path)
        source["source_v13_2_handoff_packet_digest"] = "wrong-handoff-packet-digest"
        write_json(source_path, source)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_38_activation_record_digest_invalid" in result["blockers"]
        assert "v13_38_source_handoff_packet_digest_mismatch" in result["blockers"]
        assert result["v13_15_bridge_invoked"] is False

        root = base / "annotated_seed_boundary_loss"
        prepare_v13_38(root, "receipt-recovery-boundary", "receipt-rollback-boundary", "receipt-mutation-boundary")
        seed_path = root / "physical_quantum_qi_v13_38_counterfactual_candidate_seed.json"
        annotated_seed = read_json(seed_path)
        annotated_seed["boundary"]["failed_path_not_reinforced"] = False
        write_json(seed_path, annotated_seed)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_38_annotated_seed_digest_invalid" in result["blockers"]
        assert "v13_38_annotated_seed_boundary_failed_path_not_reinforced_missing" in result["blockers"]
        assert result["v13_15_bridge_invoked"] is False

        root = base / "handoff_packet_tamper"
        prepare_v13_38(root, "receipt-recovery-packet", "receipt-rollback-packet", "receipt-mutation-packet")
        packet_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json"
        packet = read_json(packet_path)
        packet["candidate_weighting"]["path_weight_delta"] = 1
        write_json(packet_path, packet)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_2_handoff_packet_weighting_invalid" in result["blockers"]
        assert "v13_2_handoff_packet_digest_invalid" in result["blockers"]
        assert result["v13_15_bridge_invoked"] is False

        root = base / "gate_tamper"
        prepare_v13_38(root, "receipt-recovery-gate", "receipt-rollback-gate", "receipt-mutation-gate")
        gate_path = root / "physical_quantum_qi_next_cycle_gate_input.json"
        gate = read_json(gate_path)
        gate["cycle_gate_decision"] = "block_candidate"
        write_json(gate_path, gate)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_2_cycle_gate_input_semantics_invalid" in result["blockers"]
        assert "v13_2_cycle_gate_input_digest_invalid" in result["blockers"]
        assert result["v13_15_bridge_invoked"] is False

        root = base / "nested_bridge_license_block"
        prepare_v13_38(root, "receipt-recovery-bridge", "receipt-rollback-bridge", "receipt-mutation-bridge")
        broken_bridge = bridge_license()
        broken_bridge["v13_2_cycle_gate_input_read_allowed"] = False
        result = run(root, activation_license(v13_15_bridge_license=broken_bridge))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_15_bridge_invoked"] is True
        assert result["v13_3_receipt_ledger_invoked"] is False
        assert "v13_15_bridge_not_ready" in result["blockers"]

        root = base / "nested_ledger_license_block"
        prepare_v13_38(root, "receipt-recovery-ledger", "receipt-rollback-ledger", "receipt-mutation-ledger")
        broken_ledger = ledger_license()
        broken_ledger["receipt_ledger_append_allowed"] = False
        result = run(root, activation_license(v13_3_receipt_ledger_license=broken_ledger))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_15_bridge_invoked"] is True
        assert result["v13_3_receipt_ledger_invoked"] is True
        assert "v13_3_receipt_ledger_not_ready" in result["blockers"]
        assert result["activation_ledger_appended"] is False

        root = base / "top_license_block"
        prepare_v13_38(root, "receipt-recovery-license", "receipt-rollback-license", "receipt-mutation-license")
        result = run(root, activation_license(v13_3_receipt_ledger_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert "v13_3_receipt_ledger_invoke_not_allowed" in result["blockers"]
        assert result["v13_15_bridge_invoked"] is False
        assert result["v13_3_receipt_ledger_invoked"] is False

    print("physical_quantum_qi_v13_39_counterfactual_handoff_receipt checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
