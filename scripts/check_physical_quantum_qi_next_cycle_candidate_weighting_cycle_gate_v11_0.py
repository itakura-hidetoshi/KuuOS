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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_v11_0 import build_physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate

RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "next_cycle_candidate_weighting_receipt_only": True,
    "does_not_execute_path": True,
    "does_not_run_runner": True,
    "does_not_start_next_cycle": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_authorize_execution": True,
    "candidate_weighting_not_truth": True,
    "receipt_does_not_mutate_bridge_packet": True,
    "receipt_does_not_start_next_cycle": True,
    "barrier_potential_can_only_block_or_probe": True,
    "replayable_receipt": True,
    "fail_closed_on_boundary_loss": True,
}


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_enabled": True,
        "apply_physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_CYCLE_GATE_LICENSE_READY",
        "candidate_weighting_receipt_ledger_read_allowed": True,
        "cycle_gate_packet_write_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def receipt(status: str) -> dict[str, Any]:
    mode = {
        "weighted_candidate": "increase_candidate_path_weight",
        "probe_only_candidate": "open_probe_candidate_channel",
        "blocked_candidate": "install_barrier_candidate_potential",
    }[status]
    weighting = {
        "weighted_candidate": {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "probe_only_candidate": {"path_weight_delta": 0, "probe_potential_required": True, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "blocked_candidate": {"path_weight_delta": 0, "probe_potential_required": False, "barrier_potential_required": True, "barrier_blocks_ready_weight": True},
    }[status]
    return {
        "version": "physical_quantum_qi_next_cycle_candidate_weighting_receipt_record_v10_9",
        "record_type": "physical_quantum_qi_next_cycle_candidate_weighting_receipt",
        "source_reentry_intake_decision": "source-decision",
        "bridge_mode": mode,
        "next_cycle_candidate_status": status,
        "candidate_weighting": weighting,
        "source_bridge_packet_digest": f"source-{status}",
        "prev_record_digest": "GENESIS",
        "record_digest": f"digest-{status}",
        "boundary": dict(RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, record: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if record is not None:
        append_jsonl(runtime / "physical_quantum_qi_next_cycle_candidate_weighting_receipt_ledger.jsonl", record)
    result = build_physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate(
        runtime_context=ctx(runtime),
        next_cycle_candidate_weighting_cycle_gate_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_packet.json")
    return result.to_dict(), packet


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_CYCLE_GATE_READY", label
    assert out["gate_packet_written"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["cycle_gate_only"] is True, label
    assert packet["boundary"]["does_not_start_next_cycle"] is True, label
    assert packet["boundary"]["does_not_execute_path"] is True, label
    assert packet["boundary"]["does_not_authorize_execution"] is True, label
    assert packet["boundary"]["gate_does_not_select_final_path"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, packet = run(root, "weighted", receipt("weighted_candidate"), lic())
        assert_ready("weighted", out, packet)
        assert out["cycle_gate_decision"] == "admit_candidate"
        assert packet["source_candidate_status"] == "weighted_candidate"

        out, packet = run(root, "probe", receipt("probe_only_candidate"), lic())
        assert_ready("probe", out, packet)
        assert out["cycle_gate_decision"] == "hold_candidate"
        assert packet["source_candidate_status"] == "probe_only_candidate"

        out, packet = run(root, "blocked", receipt("blocked_candidate"), lic())
        assert_ready("blocked", out, packet)
        assert out["cycle_gate_decision"] == "block_candidate"
        assert packet["source_candidate_status"] == "blocked_candidate"

        bad_weighted = receipt("weighted_candidate")
        bad_weighted["candidate_weighting"]["path_weight_delta"] = 0
        out, packet = run(root, "bad_weighted", bad_weighted, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_CYCLE_GATE_BLOCKED"
        assert "weighted_candidate_without_positive_delta" in out["blockers"]
        assert packet == {}

        bad_boundary = receipt("weighted_candidate")
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, packet = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_CYCLE_GATE_BLOCKED"
        assert "candidate_weighting_receipt_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_CYCLE_GATE_BLOCKED"
        assert "candidate_weighting_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "license_block", receipt("weighted_candidate"), lic(cycle_gate_packet_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_CYCLE_GATE_BLOCKED"
        assert "cycle_gate_packet_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_v11_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
