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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_next_cycle_candidate_weighting_receipt_ledger_v10_9 import build_physical_quantum_qi_next_cycle_candidate_weighting_receipt_ledger

BRIDGE_BOUNDARY = {
    "next_cycle_candidate_weighting_bridge_only": True,
    "next_cycle_candidate_weighting_only": True,
    "does_not_execute_path": True,
    "does_not_run_runner": True,
    "does_not_start_next_cycle": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_authorize_execution": True,
    "candidate_weighting_not_truth": True,
    "bridge_does_not_mutate_receipt_ledger": True,
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
        "physical_quantum_qi_next_cycle_candidate_weighting_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_next_cycle_candidate_weighting_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_RECEIPT_LEDGER_LICENSE_READY",
        "bridge_packet_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def bridge_packet(decision: str) -> dict[str, Any]:
    mode, status = {
        "accept": ("increase_candidate_path_weight", "weighted_candidate"),
        "hold": ("open_probe_candidate_channel", "probe_only_candidate"),
        "block": ("install_barrier_candidate_potential", "blocked_candidate"),
    }[decision]
    weighting = {
        "accept": {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "hold": {"path_weight_delta": 0, "probe_potential_required": True, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "block": {"path_weight_delta": 0, "probe_potential_required": False, "barrier_potential_required": True, "barrier_blocks_ready_weight": True},
    }[decision]
    packet = {
        "version": "physical_quantum_qi_next_cycle_candidate_weighting_bridge_packet_v10_8",
        "physical_quantum_qi_next_cycle_candidate_weighting_bridge_considered": True,
        "source_reentry_intake_decision": decision,
        "source_intake_action": "source-action",
        "bridge_mode": mode,
        "next_cycle_candidate_status": status,
        "candidate_weighting": weighting,
        "source_digests": {"reentry_intake_receipt_record": "source-digest"},
        "boundary": dict(BRIDGE_BOUNDARY),
        "epoch": 1,
    }
    packet["bridge_packet_digest"] = f"bridge-digest-{decision}"
    return packet


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "physical_quantum_qi_next_cycle_candidate_weighting_bridge_packet.json", packet)
    result = build_physical_quantum_qi_next_cycle_candidate_weighting_receipt_ledger(
        runtime_context=ctx(runtime),
        next_cycle_candidate_weighting_receipt_ledger_license=license_packet,
    )
    ledger = read_jsonl(runtime / "physical_quantum_qi_next_cycle_candidate_weighting_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    assert ledger[-1]["boundary"]["receipt_ledger_only"] is True, label
    assert ledger[-1]["boundary"]["next_cycle_candidate_weighting_receipt_only"] is True, label
    assert ledger[-1]["boundary"]["does_not_start_next_cycle"] is True, label
    assert ledger[-1]["boundary"]["does_not_authorize_execution"] is True, label
    assert ledger[-1]["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, ledger = run(root, "accept", bridge_packet("accept"), lic())
        assert_ready("accept", out, ledger)
        assert out["bridge_mode"] == "increase_candidate_path_weight"
        assert ledger[-1]["next_cycle_candidate_status"] == "weighted_candidate"
        assert ledger[-1]["candidate_weighting"]["path_weight_delta"] == 3

        out, ledger = run(root, "hold", bridge_packet("hold"), lic())
        assert_ready("hold", out, ledger)
        assert out["bridge_mode"] == "open_probe_candidate_channel"
        assert ledger[-1]["next_cycle_candidate_status"] == "probe_only_candidate"
        assert ledger[-1]["candidate_weighting"]["probe_potential_required"] is True

        out, ledger = run(root, "block", bridge_packet("block"), lic())
        assert_ready("block", out, ledger)
        assert out["bridge_mode"] == "install_barrier_candidate_potential"
        assert ledger[-1]["next_cycle_candidate_status"] == "blocked_candidate"
        assert ledger[-1]["candidate_weighting"]["barrier_blocks_ready_weight"] is True

        out, ledger = run(root, "chain", bridge_packet("accept"), lic())
        assert_ready("chain_1", out, ledger)
        out, ledger = run(root, "chain", bridge_packet("hold"), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        bad_accept = bridge_packet("accept")
        bad_accept["candidate_weighting"]["path_weight_delta"] = 0
        out, ledger = run(root, "bad_accept", bad_accept, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_RECEIPT_LEDGER_BLOCKED"
        assert "accept_bridge_without_positive_weight_delta" in out["blockers"]
        assert ledger == []

        bad_boundary = bridge_packet("accept")
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, ledger = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_RECEIPT_LEDGER_BLOCKED"
        assert "bridge_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_RECEIPT_LEDGER_BLOCKED"
        assert "next_cycle_candidate_weighting_bridge_packet_missing_or_invalid" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "license_block", bridge_packet("accept"), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_next_cycle_candidate_weighting_receipt_ledger_v10_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
