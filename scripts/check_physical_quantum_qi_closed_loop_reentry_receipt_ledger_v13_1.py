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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_closed_loop_reentry_receipt_ledger_v13_1 import build_physical_quantum_qi_closed_loop_reentry_receipt_ledger

PT = {
    "process_tensor_digest": "pt-digest-v13-1",
    "memory_kernel_digest": "memory-kernel-digest-v13-1",
    "history_window_digest": "history-window-digest-v13-1",
    "instrument_trace_digest": "instrument-trace-digest-v13-1",
    "non_markov_context_digest": "non-markov-context-digest-v13-1",
}
PACKET_BOUNDARY = {
    "closed_loop_path_integral_reentry_only": True,
    "feeds_candidate_weighting_cycle": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "closed_loop_reentry_not_unbounded_execution": True,
    "license_gated_closed_loop": True,
    "fail_closed_on_boundary_loss": True,
}
CYCLE_BOUNDARY = {
    "candidate_weighting_cycle_state_only": True,
    "closed_loop_reentry_applied": True,
    "can_feed_next_candidate_weighting_cycle": True,
    "non_markov_feedback_preserved": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_closed_loop_reentry_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_closed_loop_reentry_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_LICENSE_READY",
        "closed_loop_reentry_packet_read_allowed": True,
        "candidate_weighting_cycle_state_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def weighting(status: str) -> dict[str, Any]:
    if status == "closed_loop_reentry_reinforced":
        return {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if status == "closed_loop_reentry_probe_opened":
        return {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def action_for(status: str) -> str:
    return {
        "closed_loop_reentry_reinforced": "reinforce_path_weight",
        "closed_loop_reentry_probe_opened": "open_probe_potential",
        "closed_loop_reentry_barrier_added": "add_barrier_potential",
    }[status]


def packet(status: str, *, bad_boundary: bool = False, bad_weight: bool = False, missing_context: bool = False) -> dict[str, Any]:
    w = weighting(status)
    if bad_weight:
        if status == "closed_loop_reentry_reinforced":
            w["path_weight_delta"] = 0
        elif status == "closed_loop_reentry_probe_opened":
            w["barrier_potential_required"] = True
        else:
            w["barrier_blocks_ready_weight"] = False
    boundary = dict(PACKET_BOUNDARY)
    if bad_boundary:
        boundary["feeds_candidate_weighting_cycle"] = False
    context = dict(PT)
    if missing_context:
        context["memory_kernel_digest"] = ""
    pkt = {
        "version": "physical_quantum_qi_closed_loop_path_integral_reentry_packet_v13_0",
        "closed_loop_path_integral_reentry_considered": True,
        "closed_loop_reentry_status": status,
        "reentry_weighting_action": action_for(status),
        "candidate_weighting": w,
        "process_tensor_context": context,
        "source_digests": {
            "reentry_weighting_state": "reentry-weighting-state-digest-v13-1",
            "feedback_to_reentry_weighting_bridge": "feedback-to-reentry-bridge-digest-v13-1",
        },
        "boundary": boundary,
        "epoch": 1,
    }
    pkt["closed_loop_path_integral_reentry_digest"] = f"closed-loop-reentry-digest-{status}"
    return pkt


def cycle_for(pkt: dict[str, Any], *, mismatch: bool = False, bad_boundary: bool = False) -> dict[str, Any]:
    w = dict(pkt["candidate_weighting"])
    if mismatch:
        w["path_weight_delta"] = int(w.get("path_weight_delta", 0)) + 1
    boundary = dict(CYCLE_BOUNDARY)
    if bad_boundary:
        boundary["closed_loop_reentry_applied"] = False
    cy = {
        "version": "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state_v13_0",
        "candidate_weighting_cycle_ready": True,
        "closed_loop_reentry_status": pkt["closed_loop_reentry_status"],
        "reentry_weighting_action": pkt["reentry_weighting_action"],
        "candidate_weighting": w,
        "process_tensor_context": dict(PT),
        "source_closed_loop_path_integral_reentry_digest": pkt["closed_loop_path_integral_reentry_digest"],
        "boundary": boundary,
        "epoch": 1,
    }
    cy["candidate_weighting_cycle_state_digest"] = f"candidate-weighting-cycle-digest-{pkt['closed_loop_reentry_status']}"
    return cy


def run(root: pathlib.Path, name: str, pkt: dict[str, Any] | None, cycle: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if pkt is not None:
        dump(runtime / "physical_quantum_qi_closed_loop_path_integral_reentry_packet.json", pkt)
    if cycle is not None:
        dump(runtime / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json", cycle)
    result = build_physical_quantum_qi_closed_loop_reentry_receipt_ledger(
        runtime_context=ctx(runtime),
        closed_loop_reentry_receipt_ledger_license=license_packet,
    )
    ledger = load_jsonl(runtime / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    latest = ledger[-1]
    assert latest["boundary"]["receipt_ledger_only"] is True, label
    assert latest["boundary"]["closed_loop_reentry_receipt_only"] is True, label
    assert latest["boundary"]["candidate_weighting_cycle_traceable"] is True, label
    assert latest["boundary"]["uses_process_tensor_feedback"] is True, label
    assert latest["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        for status in ["closed_loop_reentry_reinforced", "closed_loop_reentry_probe_opened", "closed_loop_reentry_barrier_added"]:
            pkt = packet(status)
            out, ledger = run(root, status, pkt, cycle_for(pkt), lic())
            assert_ready(status, out, ledger)
            assert out["closed_loop_reentry_status"] == status
            assert out["reentry_weighting_action"] == action_for(status)

        pkt = packet("closed_loop_reentry_reinforced")
        out, ledger = run(root, "chain", pkt, cycle_for(pkt), lic())
        assert_ready("chain_1", out, ledger)
        pkt2 = packet("closed_loop_reentry_probe_opened")
        out, ledger = run(root, "chain", pkt2, cycle_for(pkt2), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        pkt = packet("closed_loop_reentry_reinforced", bad_boundary=True)
        out, ledger = run(root, "bad_boundary", pkt, cycle_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_BLOCKED"
        assert "closed_loop_path_integral_reentry_boundary_feeds_candidate_weighting_cycle_missing" in out["blockers"]
        assert ledger == []

        pkt = packet("closed_loop_reentry_reinforced", bad_weight=True)
        out, ledger = run(root, "bad_weight", pkt, cycle_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_BLOCKED"
        assert "closed_loop_receipt_reinforce_without_positive_path_weight_delta" in out["blockers"]
        assert ledger == []

        pkt = packet("closed_loop_reentry_probe_opened")
        out, ledger = run(root, "cycle_mismatch", pkt, cycle_for(pkt, mismatch=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_BLOCKED"
        assert "candidate_weighting_cycle_state_weighting_mismatch" in out["blockers"]
        assert ledger == []

        pkt = packet("closed_loop_reentry_barrier_added", missing_context=True)
        out, ledger = run(root, "missing_context", pkt, cycle_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_BLOCKED"
        assert "process_tensor_context_memory_kernel_digest_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_BLOCKED"
        assert "closed_loop_path_integral_reentry_packet_missing_or_invalid" in out["blockers"]
        assert "candidate_weighting_cycle_state_missing_or_invalid" in out["blockers"]
        assert ledger == []

        pkt = packet("closed_loop_reentry_reinforced")
        out, ledger = run(root, "license", pkt, cycle_for(pkt), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_closed_loop_reentry_receipt_ledger_v13_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
