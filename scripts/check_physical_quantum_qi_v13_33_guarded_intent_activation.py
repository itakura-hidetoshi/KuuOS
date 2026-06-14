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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_33_guarded_intent_activation import build_physical_quantum_qi_v13_33_guarded_intent_activation
from scripts.check_physical_quantum_qi_v13_32_integration_receipt_activation import activation_license as v13_32_license
from scripts.check_physical_quantum_qi_v13_32_integration_receipt_activation import prepare_v13_31, run as run_v13_32

FLOW = {
    "reinforce": ("cycle_gate_reentry_integration_admit", "integrated_candidate_to_guarded_intent_ready", "guarded_execution_intent_ready", "emit_guarded_ready_intent", 1),
    "probe": ("cycle_gate_reentry_integration_hold", "integrated_candidate_to_guarded_intent_hold", "guarded_execution_intent_hold", "emit_guarded_hold_intent", 0),
    "barrier": ("cycle_gate_reentry_integration_block", "integrated_candidate_to_guarded_intent_block", "guarded_execution_intent_block", "emit_guarded_block_intent", 0),
}


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def latest_jsonl(path: pathlib.Path) -> dict[str, Any]:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return json.loads(lines[-1])


def rewrite_latest_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    lines[-1] = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def bridge_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_5_TO_V13_6_GUARDED_INTENT_BRIDGE_LICENSE_READY",
        "v13_5_integration_receipt_ledger_read_allowed": True,
        "v13_6_guarded_intent_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def guarded_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_LICENSE_READY",
        "cycle_gate_reentry_integration_receipt_ledger_read_allowed": True,
        "bridge_packet_write_allowed": True,
        "guarded_execution_intent_packet_write_allowed": True,
        "bridge_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_33_GUARDED_INTENT_ACTIVATION_LICENSE_READY",
        "v13_32_activation_record_read_allowed": True,
        "v13_5_receipt_ledger_read_allowed": True,
        "v13_18_bridge_invoke_allowed": True,
        "v13_6_guarded_intent_bridge_invoke_allowed": True,
        "activation_record_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v13_18_bridge_license": bridge_license(),
        "v13_6_guarded_intent_bridge_license": guarded_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_33_guarded_intent_activation_enabled": True,
        "apply_physical_quantum_qi_v13_33_guarded_intent_activation": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_packet: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_33_guarded_intent_activation(
        runtime_context=context(root),
        v13_33_guarded_intent_activation_license=license_packet,
    ).to_dict()


def prepare_v13_32(root: pathlib.Path, kind: str) -> None:
    prepare_v13_31(root, kind)
    result = run_v13_32(root, v13_32_license())
    assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_32_INTEGRATION_RECEIPT_ACTIVATION_READY", result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)
        for kind in ("reinforce", "probe", "barrier"):
            root = base / kind
            prepare_v13_32(root, kind)
            result = run(root, activation_license())
            integration, bridge, guarded, emit, count = FLOW[kind]
            assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_33_GUARDED_INTENT_ACTIVATION_READY", (kind, result)
            assert result["activation_status"] == "guarded_intent_activation_completed"
            assert result["integration_status"] == integration
            assert result["bridge_status"] == bridge
            assert result["guarded_execution_intent_status"] == guarded
            assert result["guarded_intent_emit_action"] == emit
            assert result["guarded_execution_intent_count"] == count
            assert result["v13_18_bridge_invoked"] is True
            assert result["v13_6_guarded_intent_bridge_invoked"] is True
            assert result["guarded_intent_ready_state_written"] is True
            assert result["bridge_packet_written"] is True
            assert result["guarded_execution_intent_packet_written"] is True
            assert result["bridge_state_written"] is True
            assert result["bridge_ledger_appended"] is True
            record = read_json(root / "physical_quantum_qi_v13_33_guarded_intent_activation_record.json")
            bridge_packet = read_json(root / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_packet.json")
            intent_packet = read_json(root / "physical_quantum_qi_guarded_execution_intent_packet.json")
            bridge_record = latest_jsonl(root / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_ledger.jsonl")
            assert record["source_v13_18_ready_state_digest"]
            assert record["source_v13_6_bridge_packet_digest"] == bridge_packet["integrated_candidate_to_guarded_intent_bridge_digest"]
            assert record["source_v13_6_guarded_intent_packet_digest"] == intent_packet["guarded_execution_intent_packet_digest"]
            assert record["source_v13_6_bridge_record_digest"] == bridge_record["record_digest"]

        root = base / "digest_mismatch"
        prepare_v13_32(root, "reinforce")
        source_path = root / "physical_quantum_qi_v13_32_integration_receipt_activation_record.json"
        source = read_json(source_path)
        source["source_v13_5_receipt_record_digest"] = "wrong-receipt-digest"
        write_json(source_path, source)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_18_bridge_invoked"] is False
        assert "v13_32_receipt_record_digest_mismatch" in result["blockers"]

        root = base / "boundary_loss"
        prepare_v13_32(root, "reinforce")
        ledger_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl"
        receipt_record = latest_jsonl(ledger_path)
        receipt_record["boundary"]["integrated_cycle_gate_state_traceable"] = False
        rewrite_latest_jsonl(ledger_path, receipt_record)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_18_bridge_invoked"] is True
        assert result["v13_6_guarded_intent_bridge_invoked"] is False
        assert "v13_18_bridge_not_ready" in result["blockers"]

        root = base / "license_block"
        prepare_v13_32(root, "reinforce")
        result = run(root, activation_license(v13_6_guarded_intent_bridge_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_18_bridge_invoked"] is False
        assert result["v13_6_guarded_intent_bridge_invoked"] is False
        assert "v13_6_guarded_intent_bridge_invoke_not_allowed" in result["blockers"]

    print("physical_quantum_qi_v13_33_guarded_intent_activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
