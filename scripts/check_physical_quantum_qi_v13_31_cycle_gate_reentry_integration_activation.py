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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation import build_physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation
from scripts.check_physical_quantum_qi_v13_29_cycle_handoff_activation import parts
from scripts.check_physical_quantum_qi_v13_30_handoff_receipt_activation import activation_license as v13_30_license
from scripts.check_physical_quantum_qi_v13_30_handoff_receipt_activation import prepare_v13_29, run as run_v13_30

FLOW = {
    "reinforce": ("cycle_gate_reentry_integration_admit", "integrated_cycle_gate_admit", "integrated_admissible_candidate_set_admit"),
    "probe": ("cycle_gate_reentry_integration_hold", "integrated_cycle_gate_hold", "integrated_admissible_candidate_set_probe"),
    "barrier": ("cycle_gate_reentry_integration_block", "integrated_cycle_gate_block", "integrated_admissible_candidate_set_block"),
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
        "license_status": "PHYSICAL_QUANTUM_QI_V13_31_CYCLE_GATE_REENTRY_INTEGRATION_ACTIVATION_LICENSE_READY",
        "v13_30_activation_record_read_allowed": True,
        "v13_3_receipt_ledger_read_allowed": True,
        "v13_16_bridge_invoke_allowed": True,
        "v13_4_integration_invoke_allowed": True,
        "activation_record_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v13_16_bridge_license": bridge_license(),
        "v13_4_integration_license": integration_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_enabled": True,
        "apply_physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_packet: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation(
        runtime_context=context(root),
        v13_31_cycle_gate_reentry_integration_activation_license=license_packet,
    ).to_dict()


def prepare_v13_30(root: pathlib.Path, kind: str) -> None:
    prepare_v13_29(root, kind)
    result = run_v13_30(root, v13_30_license())
    assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_30_HANDOFF_RECEIPT_ACTIVATION_READY", result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)
        for kind in ("reinforce", "probe", "barrier"):
            root = base / kind
            prepare_v13_30(root, kind)
            result = run(root, activation_license())
            _, _, handoff_status, _, _, _ = parts(kind)
            integration_status, cycle_status, set_status = FLOW[kind]
            assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_31_CYCLE_GATE_REENTRY_INTEGRATION_ACTIVATION_READY", (kind, result)
            assert result["activation_status"] == "cycle_gate_reentry_integration_activation_completed"
            assert result["handoff_status"] == handoff_status
            assert result["integration_status"] == integration_status
            assert result["integrated_cycle_gate_status"] == cycle_status
            assert result["integrated_admissible_candidate_set_status"] == set_status
            assert result["v13_16_bridge_invoked"] is True
            assert result["v13_4_integration_invoked"] is True
            assert result["integration_ready_state_written"] is True
            assert result["integration_packet_written"] is True
            assert result["integrated_cycle_gate_state_written"] is True
            assert result["integrated_admissible_candidate_set_written"] is True
            assert result["integration_ledger_appended"] is True
            record = read_json(root / "physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_record.json")
            integration_record = latest_jsonl(root / "physical_quantum_qi_cycle_gate_reentry_integration_ledger.jsonl")
            assert record["source_v13_16_integration_ready_state_digest"]
            assert record["source_v13_4_integration_packet_digest"]
            assert record["source_v13_4_integration_record_digest"] == integration_record["record_digest"]

        root = base / "digest_mismatch"
        prepare_v13_30(root, "reinforce")
        source_path = root / "physical_quantum_qi_v13_30_handoff_receipt_activation_record.json"
        source = read_json(source_path)
        source["source_v13_3_receipt_record_digest"] = "wrong-receipt-digest"
        write_json(source_path, source)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_16_bridge_invoked"] is False
        assert "v13_30_receipt_record_digest_mismatch" in result["blockers"]

        root = base / "receipt_weighting_mismatch"
        prepare_v13_30(root, "reinforce")
        ledger_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl"
        receipt_record = latest_jsonl(ledger_path)
        receipt_record["candidate_weighting"]["path_weight_delta"] = 0
        rewrite_latest_jsonl(ledger_path, receipt_record)
        source_path = root / "physical_quantum_qi_v13_30_handoff_receipt_activation_record.json"
        source = read_json(source_path)
        source["source_v13_3_receipt_record_digest"] = receipt_record["record_digest"]
        write_json(source_path, source)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_16_bridge_invoked"] is True
        assert result["v13_4_integration_invoked"] is False
        assert "v13_16_bridge_not_ready" in result["blockers"]

        root = base / "license_block"
        prepare_v13_30(root, "reinforce")
        result = run(root, activation_license(v13_4_integration_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_16_bridge_invoked"] is False
        assert result["v13_4_integration_invoked"] is False
        assert "v13_4_integration_invoke_not_allowed" in result["blockers"]

    print("physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
