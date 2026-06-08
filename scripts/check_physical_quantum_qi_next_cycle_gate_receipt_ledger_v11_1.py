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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_next_cycle_gate_receipt_ledger_v11_1 import build_physical_quantum_qi_next_cycle_gate_receipt_ledger

GATE_BOUNDARY = {
    "cycle_gate_only": True,
    "next_cycle_candidate_gate_only": True,
    "does_not_execute_path": True,
    "does_not_run_runner": True,
    "does_not_start_next_cycle": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_authorize_execution": True,
    "candidate_weighting_not_truth": True,
    "gate_does_not_mutate_receipt_ledger": True,
    "gate_does_not_select_final_path": True,
    "gate_does_not_promote_truth": True,
    "barrier_potential_can_only_block_or_probe": True,
    "fail_closed_on_boundary_loss": True,
}


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_next_cycle_gate_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_next_cycle_gate_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_GATE_RECEIPT_LEDGER_LICENSE_READY",
        "cycle_gate_packet_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def gate_packet(decision: str) -> dict[str, Any]:
    status = {
        "admit_candidate": "weighted_candidate",
        "hold_candidate": "probe_only_candidate",
        "block_candidate": "blocked_candidate",
    }[decision]
    weighting = {
        "admit_candidate": {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "hold_candidate": {"path_weight_delta": 0, "probe_potential_required": True, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "block_candidate": {"path_weight_delta": 0, "probe_potential_required": False, "barrier_potential_required": True, "barrier_blocks_ready_weight": True},
    }[decision]
    packet = {
        "version": "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_packet_v11_0",
        "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_considered": True,
        "source_candidate_status": status,
        "source_bridge_mode": "source-bridge-mode",
        "cycle_gate_decision": decision,
        "candidate_weighting": weighting,
        "source_digests": {"candidate_weighting_receipt_record": "source-digest"},
        "boundary": dict(GATE_BOUNDARY),
        "epoch": 1,
    }
    packet["cycle_gate_packet_digest"] = f"cycle-gate-digest-{decision}"
    return packet


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_packet.json", packet)
    result = build_physical_quantum_qi_next_cycle_gate_receipt_ledger(
        runtime_context=ctx(runtime),
        next_cycle_gate_receipt_ledger_license=license_packet,
    )
    ledger = read_jsonl(runtime / "physical_quantum_qi_next_cycle_gate_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_GATE_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    assert ledger[-1]["boundary"]["receipt_ledger_only"] is True, label
    assert ledger[-1]["boundary"]["cycle_gate_receipt_only"] is True, label
    assert ledger[-1]["boundary"]["does_not_start_next_cycle"] is True, label
    assert ledger[-1]["boundary"]["does_not_authorize_execution"] is True, label
    assert ledger[-1]["boundary"]["receipt_does_not_select_final_path"] is True, label
    assert ledger[-1]["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, ledger = run(root, "admit", gate_packet("admit_candidate"), lic())
        assert_ready("admit", out, ledger)
        assert out["cycle_gate_decision"] == "admit_candidate"
        assert ledger[-1]["source_candidate_status"] == "weighted_candidate"

        out, ledger = run(root, "hold", gate_packet("hold_candidate"), lic())
        assert_ready("hold", out, ledger)
        assert out["cycle_gate_decision"] == "hold_candidate"
        assert ledger[-1]["source_candidate_status"] == "probe_only_candidate"

        out, ledger = run(root, "block", gate_packet("block_candidate"), lic())
        assert_ready("block", out, ledger)
        assert out["cycle_gate_decision"] == "block_candidate"
        assert ledger[-1]["source_candidate_status"] == "blocked_candidate"

        out, ledger = run(root, "chain", gate_packet("admit_candidate"), lic())
        assert_ready("chain_1", out, ledger)
        out, ledger = run(root, "chain", gate_packet("hold_candidate"), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        bad_admit = gate_packet("admit_candidate")
        bad_admit["candidate_weighting"]["path_weight_delta"] = 0
        out, ledger = run(root, "bad_admit", bad_admit, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_GATE_RECEIPT_LEDGER_BLOCKED"
        assert "admit_gate_without_positive_delta" in out["blockers"]
        assert ledger == []

        bad_boundary = gate_packet("admit_candidate")
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, ledger = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_GATE_RECEIPT_LEDGER_BLOCKED"
        assert "cycle_gate_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_GATE_RECEIPT_LEDGER_BLOCKED"
        assert "next_cycle_candidate_weighting_cycle_gate_packet_missing_or_invalid" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "license_block", gate_packet("admit_candidate"), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_GATE_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_next_cycle_gate_receipt_ledger_v11_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
