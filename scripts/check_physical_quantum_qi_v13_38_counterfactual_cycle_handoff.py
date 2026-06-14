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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_38_counterfactual_cycle_handoff import (
    build_physical_quantum_qi_v13_38_counterfactual_cycle_handoff,
)
from scripts.check_physical_quantum_qi_v13_37_counterfactual_recovery_reentry import (
    license_packet as v13_37_license,
    prepare_v13_36,
    recovery_plan,
    run as run_v13_37,
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


def prepare_v13_37(root: pathlib.Path, recovery_id: str, rollback_id: str, mutation_id: str) -> dict[str, Any]:
    prepare_v13_36(root, mutation_id, rollback_id)
    plan = recovery_plan(recovery_id, rollback_id, mutation_id)
    result = run_v13_37(root, plan, v13_37_license(plan))
    assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_37_COUNTERFACTUAL_RECOVERY_REENTRY_READY", result
    return result


def bridge_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_LICENSE_READY",
        "v13_1_closed_loop_reentry_receipt_ledger_read_allowed": True,
        "v13_2_handoff_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def handoff_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_LICENSE_READY",
        "closed_loop_reentry_receipt_ledger_read_allowed": True,
        "handoff_packet_write_allowed": True,
        "cycle_gate_input_write_allowed": True,
        "admissible_candidate_set_seed_write_allowed": True,
        "handoff_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_38_COUNTERFACTUAL_CYCLE_HANDOFF_LICENSE_READY",
        "v13_37_activation_record_read_allowed": True,
        "v13_37_receipt_read_allowed": True,
        "v13_37_recovery_ledger_read_allowed": True,
        "v13_37_counterfactual_packet_read_allowed": True,
        "v13_1_receipt_ledger_read_allowed": True,
        "v13_14_bridge_invoke_allowed": True,
        "v13_2_handoff_invoke_allowed": True,
        "annotated_seed_write_allowed": True,
        "activation_record_write_allowed": True,
        "activation_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v13_14_bridge_license": bridge_license(),
        "v13_2_handoff_license": handoff_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_38_counterfactual_cycle_handoff_enabled": True,
        "apply_physical_quantum_qi_v13_38_counterfactual_cycle_handoff": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_value: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_38_counterfactual_cycle_handoff(
        runtime_context=context(root),
        v13_38_counterfactual_cycle_handoff_license=license_value,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        prepare_v13_37(root, "handoff-recovery-success", "handoff-rollback-success", "handoff-mutation-success")
        result = run(root, activation_license())
        assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_38_COUNTERFACTUAL_CYCLE_HANDOFF_READY", result
        assert result["activation_status"] == "counterfactual_cycle_handoff_completed"
        assert result["selected_probe_type"] == "observation_debt_probe"
        assert result["candidate_count"] == 4
        assert result["handoff_status"] == "candidate_weighting_cycle_handoff_probe"
        assert result["cycle_gate_decision"] == "hold_candidate"
        assert result["admissible_candidate_seed_mode"] == "probe_candidate_seed"
        assert result["v13_14_bridge_invoked"] is True
        assert result["v13_2_handoff_invoked"] is True
        assert result["annotated_seed_written"] is True
        assert result["activation_ledger_appended"] is True

        annotated = read_json(root / "physical_quantum_qi_v13_38_counterfactual_candidate_seed.json")
        activation = read_json(root / "physical_quantum_qi_v13_38_counterfactual_cycle_handoff_record.json")
        activation_record = latest(root / "physical_quantum_qi_counterfactual_cycle_handoff_ledger.jsonl")
        handoff_packet = read_json(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json")
        cycle_input = read_json(root / "physical_quantum_qi_next_cycle_gate_input.json")
        seed = read_json(root / "physical_quantum_qi_admissible_candidate_set_seed.json")
        handoff_record = latest(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_ledger.jsonl")
        receipt_record = latest(root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl")

        assert annotated["counterfactual_candidate_seed_ready"] is True
        assert annotated["selected_probe_type"] == "observation_debt_probe"
        assert annotated["selected_probe_candidate"]["probe_type"] == "observation_debt_probe"
        assert annotated["candidate_weighting"] == EXPECTED_WEIGHTING
        assert annotated["boundary"]["failed_path_not_reinforced"] is True
        assert annotated["boundary"]["not_direct_execution_authority"] is True
        assert annotated["boundary"]["not_world_update_authority"] is True
        assert annotated["source_digests"]["v13_2_handoff_packet"] == handoff_packet[
            "candidate_weighting_cycle_handoff_digest"
        ]
        assert annotated["source_digests"]["v13_2_cycle_gate_input"] == cycle_input["cycle_gate_input_digest"]
        assert annotated["source_digests"]["v13_2_candidate_seed"] == seed["admissible_candidate_set_seed_digest"]
        assert annotated["source_digests"]["v13_2_handoff_record"] == handoff_record["record_digest"]
        assert handoff_packet["handoff_status"] == "candidate_weighting_cycle_handoff_probe"
        assert cycle_input["cycle_gate_decision"] == "hold_candidate"
        assert seed["admissible_candidate_seed_mode"] == "probe_candidate_seed"
        assert seed["candidate_weighting"] == EXPECTED_WEIGHTING
        assert handoff_record["source_closed_loop_reentry_receipt_digest"] == receipt_record["record_digest"]
        assert activation["source_v13_38_counterfactual_candidate_seed_digest"] == annotated[
            "counterfactual_candidate_seed_digest"
        ]
        assert activation_record["source_activation_record_digest"] == activation[
            "counterfactual_cycle_handoff_record_digest"
        ]

        activation_count = len(records(root / "physical_quantum_qi_counterfactual_cycle_handoff_ledger.jsonl"))
        handoff_count = len(records(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_ledger.jsonl"))
        replay = run(root, activation_license())
        assert replay["status"].endswith("BLOCKED")
        assert "counterfactual_cycle_handoff_recovery_replay" in replay["blockers"]
        assert replay["v13_14_bridge_invoked"] is False
        assert replay["v13_2_handoff_invoked"] is False
        assert len(records(root / "physical_quantum_qi_counterfactual_cycle_handoff_ledger.jsonl")) == activation_count
        assert len(records(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_ledger.jsonl")) == handoff_count

        root = base / "source_digest_mismatch"
        prepare_v13_37(root, "handoff-recovery-digest", "handoff-rollback-digest", "handoff-mutation-digest")
        source_path = root / "physical_quantum_qi_v13_37_counterfactual_recovery_reentry_record.json"
        source = read_json(source_path)
        source["source_v13_1_closed_loop_receipt_record_digest"] = "wrong-receipt-digest"
        write_json(source_path, source)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_37_source_receipt_record_digest_mismatch" in result["blockers"]
        assert result["v13_14_bridge_invoked"] is False

        root = base / "boundary_loss"
        prepare_v13_37(root, "handoff-recovery-boundary", "handoff-rollback-boundary", "handoff-mutation-boundary")
        packet_path = root / "physical_quantum_qi_v13_37_counterfactual_recovery_packet.json"
        packet = read_json(packet_path)
        packet["boundary"]["rollback_path_not_reinforced"] = False
        write_json(packet_path, packet)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_37_counterfactual_packet_digest_mismatch" in result["blockers"]
        assert "v13_37_counterfactual_packet_boundary_rollback_path_not_reinforced_missing" in result["blockers"]
        assert result["v13_14_bridge_invoked"] is False

        root = base / "receipt_weighting_tamper"
        prepare_v13_37(root, "handoff-recovery-weight", "handoff-rollback-weight", "handoff-mutation-weight")
        receipt_ledger = root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl"
        receipt = latest(receipt_ledger)
        receipt["candidate_weighting"]["path_weight_delta"] = 1
        rewrite_latest(receipt_ledger, receipt)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_1_receipt_probe_weighting_invalid" in result["blockers"]
        assert result["v13_14_bridge_invoked"] is False

        root = base / "ranked_candidate_loss"
        prepare_v13_37(root, "handoff-recovery-rank", "handoff-rollback-rank", "handoff-mutation-rank")
        packet_path = root / "physical_quantum_qi_v13_37_counterfactual_recovery_packet.json"
        packet = read_json(packet_path)
        packet["ranked_candidates"] = [
            item for item in packet["ranked_candidates"] if item.get("probe_type") != packet["selected_probe_type"]
        ]
        write_json(packet_path, packet)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert "v13_37_counterfactual_packet_digest_mismatch" in result["blockers"]
        assert "v13_37_selected_probe_not_in_ranked_candidates" in result["blockers"]
        assert result["v13_14_bridge_invoked"] is False

        root = base / "nested_bridge_license_block"
        prepare_v13_37(root, "handoff-recovery-nested", "handoff-rollback-nested", "handoff-mutation-nested")
        broken_bridge = bridge_license()
        broken_bridge["v13_1_closed_loop_reentry_receipt_ledger_read_allowed"] = False
        result = run(root, activation_license(v13_14_bridge_license=broken_bridge))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_14_bridge_invoked"] is True
        assert result["v13_2_handoff_invoked"] is False
        assert "v13_14_bridge_not_ready" in result["blockers"]

        root = base / "top_license_block"
        prepare_v13_37(root, "handoff-recovery-license", "handoff-rollback-license", "handoff-mutation-license")
        result = run(root, activation_license(v13_2_handoff_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert "v13_2_handoff_invoke_not_allowed" in result["blockers"]
        assert result["v13_14_bridge_invoked"] is False
        assert result["v13_2_handoff_invoked"] is False

    print("physical_quantum_qi_v13_38_counterfactual_cycle_handoff checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
