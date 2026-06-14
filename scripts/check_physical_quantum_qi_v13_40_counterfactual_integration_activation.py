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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_40_counterfactual_integration_activation import (
    build_physical_quantum_qi_v13_40_counterfactual_integration_activation,
)
from scripts.check_physical_quantum_qi_v13_39_counterfactual_handoff_receipt import (
    activation_license as v13_39_license,
    prepare_v13_38,
    run as run_v13_39,
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


def rewrite_latest(path: pathlib.Path, payload: dict[str, Any]) -> None:
    values = records(path)
    values[-1] = payload
    path.write_text(
        "".join(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n" for value in values),
        encoding="utf-8",
    )


def prepare_v13_39(root: pathlib.Path, recovery_id: str, rollback_id: str, mutation_id: str) -> dict[str, Any]:
    prepare_v13_38(root, recovery_id, rollback_id, mutation_id)
    result = run_v13_39(root, v13_39_license())
    assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_39_COUNTERFACTUAL_HANDOFF_RECEIPT_READY", result
    return result


def bridge_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_LICENSE_READY",
        "v13_3_handoff_receipt_ledger_read_allowed": True,
        "v13_4_integration_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def integration_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_LICENSE_READY",
        "candidate_weighting_cycle_handoff_receipt_ledger_read_allowed": True,
        "integration_packet_write_allowed": True,
        "integrated_cycle_gate_state_write_allowed": True,
        "integrated_admissible_candidate_set_write_allowed": True,
        "integration_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_40_COUNTERFACTUAL_INTEGRATION_ACTIVATION_LICENSE_READY",
        "v13_39_activation_record_read_allowed": True,
        "v13_39_receipt_read_allowed": True,
        "v13_39_activation_ledger_read_allowed": True,
        "v13_39_annotated_receipt_read_allowed": True,
        "v13_3_receipt_ledger_read_allowed": True,
        "v13_16_bridge_invoke_allowed": True,
        "v13_4_integration_invoke_allowed": True,
        "annotated_candidate_write_allowed": True,
        "activation_record_write_allowed": True,
        "activation_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v13_16_bridge_license": bridge_license(),
        "v13_4_integration_license": integration_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_40_counterfactual_integration_activation_enabled": True,
        "apply_physical_quantum_qi_v13_40_counterfactual_integration_activation": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_value: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_40_counterfactual_integration_activation(
        runtime_context=context(root),
        v13_40_counterfactual_integration_activation_license=license_value,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        prepare_v13_39(root, "integration-recovery-success", "integration-rollback-success", "integration-mutation-success")
        result = run(root, activation_license())
        assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_40_COUNTERFACTUAL_INTEGRATION_ACTIVATION_READY", result
        assert result["activation_status"] == "counterfactual_integration_activation_completed"
        assert result["selected_probe_type"] == "observation_debt_probe"
        assert result["candidate_count"] == 4
        assert result["integration_status"] == "cycle_gate_reentry_integration_hold"
        assert result["integrated_cycle_gate_status"] == "integrated_cycle_gate_hold"
        assert result["integrated_admissible_candidate_set_status"] == "integrated_admissible_candidate_set_probe"
        assert result["v13_16_bridge_invoked"] is True
        assert result["v13_4_integration_invoked"] is True
        assert result["annotated_candidate_written"] is True
        assert result["activation_ledger_appended"] is True
        assert result["v13_4_integration_record_digest"]

        annotated = read_json(root / "physical_quantum_qi_v13_40_counterfactual_integration_candidate.json")
        activation = read_json(root / "physical_quantum_qi_v13_40_counterfactual_integration_activation_record.json")
        activation_ledger = latest(root / "physical_quantum_qi_counterfactual_integration_activation_ledger.jsonl")
        ready_state = read_json(root / "physical_quantum_qi_v13_4_cycle_gate_reentry_integration_ready_state.json")
        bridge_record = latest(root / "physical_quantum_qi_v13_3_to_v13_4_integration_bridge_ledger.jsonl")
        packet = read_json(root / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json")
        cycle_state = read_json(root / "physical_quantum_qi_integrated_cycle_gate_state.json")
        candidate_set = read_json(root / "physical_quantum_qi_integrated_admissible_candidate_set.json")
        integration_record = latest(root / "physical_quantum_qi_cycle_gate_reentry_integration_ledger.jsonl")
        source = read_json(root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_activation_record.json")
        source_receipt = read_json(root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_record.json")

        assert packet["integration_status"] == "cycle_gate_reentry_integration_hold"
        assert packet["integrated_cycle_gate_status"] == "integrated_cycle_gate_hold"
        assert packet["integrated_admissible_candidate_set_status"] == "integrated_admissible_candidate_set_probe"
        assert cycle_state["integrated_cycle_gate_status"] == "integrated_cycle_gate_hold"
        assert cycle_state["cycle_gate_decision"] == "hold_candidate"
        assert candidate_set["integrated_admissible_candidate_set_status"] == "integrated_admissible_candidate_set_probe"
        assert candidate_set["admissible_candidate_count"] == 1
        generic_candidate = candidate_set["integrated_candidates"][0]
        assert generic_candidate["candidate_id"] == "closed_loop_reentry_probe_candidate"
        assert generic_candidate["candidate_mode"] == "probe_candidate"
        assert generic_candidate["admissibility_status"] == "admissible_candidate_probe_required"
        assert generic_candidate["candidate_weighting"] == EXPECTED_WEIGHTING

        assert annotated["counterfactual_integration_candidate_ready"] is True
        assert annotated["selected_probe_type"] == "observation_debt_probe"
        assert annotated["selected_probe_candidate"]["probe_type"] == "observation_debt_probe"
        assert annotated["generic_integrated_candidate"]["candidate_digest"] == generic_candidate["candidate_digest"]
        assert annotated["candidate_weighting"] == EXPECTED_WEIGHTING
        assert annotated["boundary"]["integrated_cycle_gate_hold_required"] is True
        assert annotated["boundary"]["not_direct_execution_authority"] is True
        assert annotated["boundary"]["not_world_update_authority"] is True
        assert annotated["source_digests"]["v13_39_activation_record"] == source[
            "counterfactual_handoff_receipt_activation_record_digest"
        ]
        assert annotated["source_digests"]["v13_39_annotated_receipt"] == source_receipt[
            "counterfactual_handoff_receipt_record_digest"
        ]
        assert annotated["source_digests"]["v13_16_ready_state"] == ready_state["integration_ready_state_digest"]
        assert annotated["source_digests"]["v13_16_bridge_record"] == bridge_record["record_digest"]
        assert annotated["source_digests"]["v13_4_integration_packet"] == packet[
            "cycle_gate_reentry_integration_digest"
        ]
        assert annotated["source_digests"]["v13_4_cycle_state"] == cycle_state[
            "integrated_cycle_gate_state_digest"
        ]
        assert annotated["source_digests"]["v13_4_candidate_set"] == candidate_set[
            "integrated_admissible_candidate_set_digest"
        ]
        assert annotated["source_digests"]["v13_4_integration_record"] == integration_record["record_digest"]
        assert activation["source_v13_40_annotated_candidate_digest"] == annotated[
            "counterfactual_integration_candidate_digest"
        ]
        assert activation["source_v13_4_integration_record_digest"] == integration_record["record_digest"]
        assert activation_ledger["source_activation_record_digest"] == activation[
            "counterfactual_integration_activation_record_digest"
        ]
        assert activation_ledger["source_v13_4_integration_record_digest"] == integration_record["record_digest"]

        activation_count = len(records(root / "physical_quantum_qi_counterfactual_integration_activation_ledger.jsonl"))
        integration_count = len(records(root / "physical_quantum_qi_cycle_gate_reentry_integration_ledger.jsonl"))
        replay = run(root, activation_license())
        assert replay["status"].endswith("BLOCKED")
        assert "counterfactual_integration_recovery_replay" in replay["blockers"]
        assert replay["v13_16_bridge_invoked"] is False
        assert replay["v13_4_integration_invoked"] is False
        assert len(records(root / "physical_quantum_qi_counterfactual_integration_activation_ledger.jsonl")) == activation_count
        assert len(records(root / "physical_quantum_qi_cycle_gate_reentry_integration_ledger.jsonl")) == integration_count

        root = base / "source_digest_tamper"
        prepare_v13_39(root, "integration-recovery-source", "integration-rollback-source", "integration-mutation-source")
        source_path = root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_activation_record.json"
        source = read_json(source_path)
        source["source_v13_3_receipt_record_digest"] = "wrong-receipt-digest"
        write_json(source_path, source)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_39_activation_record_digest_invalid" in result["blockers"]
        assert "v13_39_generic_receipt_digest_mismatch" in result["blockers"]
        assert result["v13_16_bridge_invoked"] is False

        root = base / "annotated_receipt_boundary_loss"
        prepare_v13_39(root, "integration-recovery-boundary", "integration-rollback-boundary", "integration-mutation-boundary")
        annotated_path = root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_record.json"
        source_annotated = read_json(annotated_path)
        source_annotated["boundary"]["failed_path_not_reinforced"] = False
        write_json(annotated_path, source_annotated)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_39_annotated_receipt_record_digest_invalid" in result["blockers"]
        assert "v13_39_annotated_receipt_boundary_failed_path_not_reinforced_missing" in result["blockers"]
        assert result["v13_16_bridge_invoked"] is False

        root = base / "generic_receipt_tamper"
        prepare_v13_39(root, "integration-recovery-generic", "integration-rollback-generic", "integration-mutation-generic")
        generic_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl"
        generic = latest(generic_path)
        generic["candidate_weighting"]["path_weight_delta"] = 1
        rewrite_latest(generic_path, generic)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_3_receipt_weighting_invalid" in result["blockers"]
        assert "v13_3_receipt_record_digest_invalid" in result["blockers"]
        assert result["v13_16_bridge_invoked"] is False

        root = base / "nested_bridge_license_block"
        prepare_v13_39(root, "integration-recovery-bridge", "integration-rollback-bridge", "integration-mutation-bridge")
        broken_bridge = bridge_license()
        broken_bridge["v13_3_handoff_receipt_ledger_read_allowed"] = False
        result = run(root, activation_license(v13_16_bridge_license=broken_bridge))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_16_bridge_invoked"] is True
        assert result["v13_4_integration_invoked"] is False
        assert "v13_16_bridge_not_ready" in result["blockers"]

        root = base / "nested_integration_license_block"
        prepare_v13_39(root, "integration-recovery-runtime", "integration-rollback-runtime", "integration-mutation-runtime")
        broken_integration = integration_license()
        broken_integration["integration_ledger_append_allowed"] = False
        result = run(root, activation_license(v13_4_integration_license=broken_integration))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_16_bridge_invoked"] is True
        assert result["v13_4_integration_invoked"] is True
        assert "v13_4_integration_not_ready" in result["blockers"]
        assert result["activation_ledger_appended"] is False

        root = base / "top_license_block"
        prepare_v13_39(root, "integration-recovery-license", "integration-rollback-license", "integration-mutation-license")
        result = run(root, activation_license(v13_4_integration_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert "v13_4_integration_invoke_not_allowed" in result["blockers"]
        assert result["v13_16_bridge_invoked"] is False
        assert result["v13_4_integration_invoked"] is False

    print("physical_quantum_qi_v13_40_counterfactual_integration_activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
