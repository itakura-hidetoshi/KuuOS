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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_32_integration_receipt_activation import build_physical_quantum_qi_v13_32_integration_receipt_activation
from scripts.check_physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation import activation_license as v13_31_license
from scripts.check_physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation import prepare_v13_30, run as run_v13_31

FLOW = {
    "reinforce": ("cycle_gate_reentry_integration_admit", "integrated_cycle_gate_admit", "integrated_admissible_candidate_set_admit", 1),
    "probe": ("cycle_gate_reentry_integration_hold", "integrated_cycle_gate_hold", "integrated_admissible_candidate_set_probe", 1),
    "barrier": ("cycle_gate_reentry_integration_block", "integrated_cycle_gate_block", "integrated_admissible_candidate_set_block", 0),
}


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def latest_jsonl(path: pathlib.Path) -> dict[str, Any]:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return json.loads(lines[-1])


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
        "license_status": "PHYSICAL_QUANTUM_QI_V13_32_INTEGRATION_RECEIPT_ACTIVATION_LICENSE_READY",
        "v13_31_activation_record_read_allowed": True,
        "v13_4_integration_packet_read_allowed": True,
        "v13_4_integration_ledger_read_allowed": True,
        "v13_17_bridge_invoke_allowed": True,
        "v13_5_receipt_ledger_invoke_allowed": True,
        "activation_record_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v13_17_bridge_license": bridge_license(),
        "v13_5_receipt_ledger_license": ledger_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_32_integration_receipt_activation_enabled": True,
        "apply_physical_quantum_qi_v13_32_integration_receipt_activation": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_packet: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_32_integration_receipt_activation(
        runtime_context=context(root),
        v13_32_integration_receipt_activation_license=license_packet,
    ).to_dict()


def prepare_v13_31(root: pathlib.Path, kind: str) -> None:
    prepare_v13_30(root, kind)
    result = run_v13_31(root, v13_31_license())
    assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_31_CYCLE_GATE_REENTRY_INTEGRATION_ACTIVATION_READY", result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)
        for kind in ("reinforce", "probe", "barrier"):
            root = base / kind
            prepare_v13_31(root, kind)
            result = run(root, activation_license())
            integration_status, gate_status, set_status, count = FLOW[kind]
            assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_32_INTEGRATION_RECEIPT_ACTIVATION_READY", (kind, result)
            assert result["activation_status"] == "integration_receipt_activation_completed"
            assert result["integration_status"] == integration_status
            assert result["integrated_cycle_gate_status"] == gate_status
            assert result["integrated_admissible_candidate_set_status"] == set_status
            assert result["admissible_candidate_count"] == count
            assert result["v13_17_bridge_invoked"] is True
            assert result["v13_5_receipt_ledger_invoked"] is True
            assert result["receipt_ready_state_written"] is True
            assert result["bridge_ledger_appended"] is True
            assert result["receipt_ledger_appended"] is True
            record = read_json(root / "physical_quantum_qi_v13_32_integration_receipt_activation_record.json")
            ledger_receipt = read_json(root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_receipt.json")
            receipt_record = latest_jsonl(root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl")
            assert record["source_v13_17_receipt_ready_state_digest"]
            assert ledger_receipt["record_digest"] == receipt_record["record_digest"]
            assert record["source_v13_5_receipt_record_digest"] == receipt_record["record_digest"]

        root = base / "digest_mismatch"
        prepare_v13_31(root, "reinforce")
        source_path = root / "physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_record.json"
        source = read_json(source_path)
        source["source_v13_4_integration_packet_digest"] = "wrong-integration-digest"
        write_json(source_path, source)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_17_bridge_invoked"] is False
        assert "v13_31_integration_packet_digest_mismatch" in result["blockers"]

        root = base / "candidate_count_mismatch"
        prepare_v13_31(root, "reinforce")
        packet_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json"
        packet = read_json(packet_path)
        packet["integrated_candidates"] = []
        write_json(packet_path, packet)
        source_path = root / "physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_record.json"
        source = read_json(source_path)
        source["source_v13_4_integration_packet_digest"] = packet["cycle_gate_reentry_integration_digest"]
        write_json(source_path, source)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_17_bridge_invoked"] is False
        assert "v13_4_packet_candidate_count_mismatch" in result["blockers"]

        root = base / "license_block"
        prepare_v13_31(root, "reinforce")
        result = run(root, activation_license(v13_5_receipt_ledger_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_17_bridge_invoked"] is False
        assert result["v13_5_receipt_ledger_invoked"] is False
        assert "v13_5_receipt_ledger_invoke_not_allowed" in result["blockers"]

    print("physical_quantum_qi_v13_32_integration_receipt_activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
