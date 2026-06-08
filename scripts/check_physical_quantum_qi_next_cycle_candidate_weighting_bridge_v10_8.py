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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_next_cycle_candidate_weighting_bridge_v10_8 import build_physical_quantum_qi_next_cycle_candidate_weighting_bridge

RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "reentry_intake_receipt_only": True,
    "does_not_execute_path": True,
    "does_not_run_runner": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_authorize_execution": True,
    "candidate_weighting_not_truth": True,
    "barrier_potential_can_only_block_or_probe": True,
    "receipt_does_not_authorize_execution": True,
    "replayable_receipt": True,
    "fail_closed_on_boundary_loss": True,
}


def dump_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_next_cycle_candidate_weighting_bridge_enabled": True,
        "apply_physical_quantum_qi_next_cycle_candidate_weighting_bridge": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_BRIDGE_LICENSE_READY",
        "receipt_ledger_read_allowed": True,
        "bridge_packet_write_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def receipt(decision: str) -> dict[str, Any]:
    action = {
        "accept": "reinforce_path_weight",
        "hold": "open_probe_potential",
        "block": "add_barrier_potential",
    }[decision]
    potential = {
        "accept": {
            "path_weight_delta": 3,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
        },
        "hold": {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
        },
        "block": {
            "path_weight_delta": 0,
            "probe_potential_required": False,
            "barrier_potential_required": True,
            "barrier_blocks_ready_weight": True,
        },
    }[decision]
    return {
        "version": "physical_quantum_qi_path_integral_reentry_intake_receipt_record_v10_7",
        "record_type": "physical_quantum_qi_path_integral_reentry_intake_receipt",
        "reentry_intake_decision": decision,
        "intake_action": action,
        "next_cycle_candidate_potential": potential,
        "prev_record_digest": "GENESIS",
        "record_digest": f"digest-{decision}",
        "boundary": dict(RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, record: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if record is not None:
        dump_jsonl(runtime / "physical_quantum_qi_path_integral_reentry_intake_receipt_ledger.jsonl", record)
    result = build_physical_quantum_qi_next_cycle_candidate_weighting_bridge(
        runtime_context=ctx(runtime),
        next_cycle_candidate_weighting_bridge_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_next_cycle_candidate_weighting_bridge_packet.json")
    return result.to_dict(), packet


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_BRIDGE_READY", label
    assert out["bridge_packet_written"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["next_cycle_candidate_weighting_only"] is True, label
    assert packet["boundary"]["does_not_start_next_cycle"] is True, label
    assert packet["boundary"]["does_not_execute_path"] is True, label
    assert packet["boundary"]["does_not_authorize_execution"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, packet = run(root, "accept", receipt("accept"), lic())
        assert_ready("accept", out, packet)
        assert out["bridge_mode"] == "increase_candidate_path_weight"
        assert packet["next_cycle_candidate_status"] == "weighted_candidate"
        assert packet["candidate_weighting"]["path_weight_delta"] == 3

        out, packet = run(root, "hold", receipt("hold"), lic())
        assert_ready("hold", out, packet)
        assert out["bridge_mode"] == "open_probe_candidate_channel"
        assert packet["next_cycle_candidate_status"] == "probe_only_candidate"
        assert packet["candidate_weighting"]["probe_potential_required"] is True

        out, packet = run(root, "block", receipt("block"), lic())
        assert_ready("block", out, packet)
        assert out["bridge_mode"] == "install_barrier_candidate_potential"
        assert packet["next_cycle_candidate_status"] == "blocked_candidate"
        assert packet["candidate_weighting"]["barrier_blocks_ready_weight"] is True

        bad_accept = receipt("accept")
        bad_accept["next_cycle_candidate_potential"]["path_weight_delta"] = 0
        out, packet = run(root, "bad_accept", bad_accept, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_BRIDGE_BLOCKED"
        assert "accept_receipt_without_positive_path_weight_delta" in out["blockers"]
        assert packet == {}

        bad_boundary = receipt("accept")
        bad_boundary["boundary"]["does_not_start_next_cycle"] = True
        bad_boundary["boundary"]["does_not_authorize_execution"] = False
        out, packet = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_BRIDGE_BLOCKED"
        assert "receipt_boundary_does_not_authorize_execution_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_BRIDGE_BLOCKED"
        assert "reentry_intake_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "license_block", receipt("accept"), lic(bridge_packet_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_BRIDGE_BLOCKED"
        assert "bridge_packet_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_next_cycle_candidate_weighting_bridge_v10_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
