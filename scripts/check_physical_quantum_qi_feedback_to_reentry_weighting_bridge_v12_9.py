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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_feedback_to_reentry_weighting_bridge_v12_9 import build_physical_quantum_qi_feedback_to_reentry_weighting_bridge

PT = {
    "process_tensor_digest": "pt-digest-v12-9",
    "memory_kernel_digest": "memory-kernel-digest-v12-9",
    "history_window_digest": "history-window-digest-v12-9",
    "instrument_trace_digest": "instrument-trace-digest-v12-9",
    "non_markov_context_digest": "non-markov-context-digest-v12-9",
}
BOUNDARY = {
    "receipt_ledger_only": True,
    "process_tensor_feedback_receipt_only": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "path_integral_feedback_traceable": True,
    "feedback_not_direct_truth": True,
    "feedback_not_unbounded_execution": True,
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
        "physical_quantum_qi_feedback_to_reentry_weighting_bridge_enabled": True,
        "apply_physical_quantum_qi_feedback_to_reentry_weighting_bridge": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_LICENSE_READY",
        "process_tensor_feedback_receipt_ledger_read_allowed": True,
        "reentry_weighting_bridge_packet_write_allowed": True,
        "reentry_weighting_state_write_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def receipt(status: str, *, bad_boundary: bool = False, bad_weight: bool = False, missing_context: bool = False) -> dict[str, Any]:
    reinforce = status == "process_tensor_feedback_reinforce_next_cycle"
    hold = status == "process_tensor_feedback_hold_context"
    path_delta = 1 if reinforce else (0 if hold else -1)
    if bad_weight:
        path_delta = 0
    context = dict(PT)
    if missing_context:
        context["non_markov_context_digest"] = ""
    boundary = dict(BOUNDARY)
    if bad_boundary:
        boundary["path_integral_feedback_traceable"] = False
    return {
        "version": "physical_quantum_qi_process_tensor_feedback_receipt_record_v12_8",
        "record_type": "physical_quantum_qi_process_tensor_feedback_receipt",
        "feedback_status": status,
        "execution_status": "guarded_transition_executed" if reinforce else ("guarded_transition_hold" if hold else "guarded_transition_block"),
        "path_weight_delta": path_delta,
        "memory_feedback_weight": 1 if reinforce else 0,
        "external_backaction_weight": 1 if reinforce else 0,
        "next_cycle_amplitude_delta": 1 if reinforce else 0,
        "observed_effects": {},
        "process_tensor_context": context,
        "source_process_tensor_execution_feedback_digest": "process-tensor-execution-feedback-digest-v12-9",
        "source_execution_record_digest": "execution-record-digest-v12-9",
        "prev_record_digest": "GENESIS",
        "record_digest": f"process-tensor-feedback-receipt-{status}",
        "boundary": boundary,
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, rec: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if rec is not None:
        append_jsonl(runtime / "physical_quantum_qi_process_tensor_feedback_receipt_ledger.jsonl", rec)
    result = build_physical_quantum_qi_feedback_to_reentry_weighting_bridge(
        runtime_context=ctx(runtime),
        feedback_to_reentry_weighting_bridge_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_feedback_to_reentry_weighting_bridge_packet.json")
    state = load_json(runtime / "physical_quantum_qi_reentry_weighting_state.json")
    return result.to_dict(), packet, state


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any], state: dict[str, Any]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_READY", label
    assert out["reentry_weighting_packet_written"] is True, label
    assert out["reentry_weighting_state_updated"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["feedback_to_reentry_weighting_bridge_only"] is True, label
    assert packet["boundary"]["feeds_next_path_integral_reentry"] is True, label
    assert packet["boundary"]["candidate_weighting_not_truth"] is True, label
    assert state["boundary"]["not_direct_execution_authority"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, packet, state = run(root, "reinforce", receipt("process_tensor_feedback_reinforce_next_cycle"), lic())
        assert_ready("reinforce", out, packet, state)
        assert out["reentry_weighting_action"] == "reinforce_path_weight"
        assert out["path_weight_delta"] == 1
        assert out["probe_potential_required"] is False
        assert out["barrier_potential_required"] is False
        assert packet["candidate_weighting"]["memory_feedback_weight"] == 1

        out, packet, state = run(root, "hold", receipt("process_tensor_feedback_hold_context"), lic())
        assert_ready("hold", out, packet, state)
        assert out["reentry_weighting_action"] == "open_probe_potential"
        assert out["path_weight_delta"] == 0
        assert out["probe_potential_required"] is True
        assert out["barrier_potential_required"] is False

        out, packet, state = run(root, "block", receipt("process_tensor_feedback_block_context"), lic())
        assert_ready("block", out, packet, state)
        assert out["reentry_weighting_action"] == "add_barrier_potential"
        assert out["path_weight_delta"] == 0
        assert out["probe_potential_required"] is False
        assert out["barrier_potential_required"] is True
        assert packet["candidate_weighting"]["barrier_blocks_ready_weight"] is True

        out, packet, state = run(root, "bad_boundary", receipt("process_tensor_feedback_reinforce_next_cycle", bad_boundary=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_BLOCKED"
        assert "process_tensor_feedback_receipt_boundary_path_integral_feedback_traceable_missing" in out["blockers"]
        assert packet == {}
        assert state == {}

        out, packet, state = run(root, "bad_weight", receipt("process_tensor_feedback_reinforce_next_cycle", bad_weight=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_BLOCKED"
        assert "reinforce_receipt_without_positive_path_weight_delta" in out["blockers"]
        assert packet == {}

        out, packet, state = run(root, "missing_context", receipt("process_tensor_feedback_hold_context", missing_context=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_BLOCKED"
        assert "process_tensor_context_non_markov_context_digest_missing" in out["blockers"]
        assert packet == {}

        out, packet, state = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_BLOCKED"
        assert "process_tensor_feedback_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet, state = run(root, "license", receipt("process_tensor_feedback_hold_context"), lic(reentry_weighting_state_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_BLOCKED"
        assert "reentry_weighting_state_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_feedback_to_reentry_weighting_bridge_v12_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
