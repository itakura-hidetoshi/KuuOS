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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_process_tensor_feedback_receipt_ledger_v12_8 import build_physical_quantum_qi_process_tensor_feedback_receipt_ledger

PT = {
    "process_tensor_digest": "pt-digest-v12-8",
    "memory_kernel_digest": "memory-kernel-digest-v12-8",
    "history_window_digest": "history-window-digest-v12-8",
    "instrument_trace_digest": "instrument-trace-digest-v12-8",
    "non_markov_context_digest": "non-markov-context-digest-v12-8",
}
PACKET_BOUNDARY = {
    "process_tensor_execution_feedback_only": True,
    "uses_execution_effects_as_non_markov_feedback": True,
    "feeds_path_integral_weighting": True,
    "history_window_feedback_required": True,
    "memory_kernel_feedback_required": True,
    "external_backaction_visible": True,
    "feedback_not_direct_truth": True,
    "feedback_not_unbounded_execution": True,
    "runtime_local_feedback_only": True,
    "fail_closed_on_boundary_loss": True,
}
STATE_BOUNDARY = {
    "path_integral_feedback_state_only": True,
    "can_feed_next_path_integral_cycle": True,
    "non_markov_feedback_preserved": True,
    "feedback_not_direct_authority": True,
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
        "physical_quantum_qi_process_tensor_feedback_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_process_tensor_feedback_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_LICENSE_READY",
        "process_tensor_execution_feedback_packet_read_allowed": True,
        "path_integral_feedback_state_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def packet(status: str, *, bad_boundary: bool = False, bad_kernel: bool = False) -> dict[str, Any]:
    execution = {
        "process_tensor_feedback_reinforce_next_cycle": "guarded_transition_executed",
        "process_tensor_feedback_hold_context": "guarded_transition_hold",
        "process_tensor_feedback_block_context": "guarded_transition_block",
    }[status]
    reinforce = status == "process_tensor_feedback_reinforce_next_cycle"
    path_delta = 1 if reinforce else (0 if status.endswith("hold_context") else -1)
    kernel = {
        "feedback_status": status,
        "path_weight_delta": path_delta,
        "memory_feedback_weight": 1 if reinforce else 0,
        "external_backaction_weight": 1 if reinforce else 0,
        "next_cycle_amplitude_delta": 1 if reinforce else 0,
        "non_markov_feedback_required": True,
        "history_window_feedback_required": True,
        "instrument_trace_feedback_required": True,
        "process_tensor_feedback_not_truth": True,
    }
    if bad_kernel:
        kernel["process_tensor_feedback_not_truth"] = False
    boundary = dict(PACKET_BOUNDARY)
    if bad_boundary:
        boundary["runtime_local_feedback_only"] = False
    pkt = {
        "version": "physical_quantum_qi_process_tensor_execution_feedback_packet_v12_7",
        "feedback_status": status,
        "execution_status": execution,
        "process_tensor_feedback_kernel": kernel,
        "observed_effects": {
            "next_cycle_observed": reinforce,
            "memory_feedback_observed": reinforce,
            "external_backaction_observed": reinforce,
        },
        "process_tensor_context": dict(PT),
        "source_digests": {
            "execution_record": "execution-record-digest-v12-8",
            "next_cycle_state": "next-cycle-state-digest-v12-8" if reinforce else "",
            "memory_consumption": "memory-consumption-digest-v12-8" if reinforce else "",
            "external_state_mutation": "external-state-mutation-digest-v12-8" if reinforce else "",
        },
        "boundary": boundary,
        "epoch": 1,
    }
    pkt["process_tensor_execution_feedback_digest"] = f"process-tensor-feedback-digest-{status}"
    return pkt


def state_for(pkt: dict[str, Any], *, mismatch: bool = False, bad_boundary: bool = False) -> dict[str, Any]:
    kernel = pkt["process_tensor_feedback_kernel"]
    boundary = dict(STATE_BOUNDARY)
    if pkt["feedback_status"] != "process_tensor_feedback_reinforce_next_cycle":
        boundary["can_feed_next_path_integral_cycle"] = False
    if bad_boundary:
        boundary["non_markov_feedback_preserved"] = False
    st = {
        "version": "physical_quantum_qi_path_integral_feedback_state_v12_7",
        "path_integral_feedback_ready": True,
        "feedback_status": pkt["feedback_status"],
        "path_weight_delta": kernel["path_weight_delta"] + (1 if mismatch else 0),
        "memory_feedback_weight": kernel["memory_feedback_weight"],
        "external_backaction_weight": kernel["external_backaction_weight"],
        "next_cycle_amplitude_delta": kernel["next_cycle_amplitude_delta"],
        "source_process_tensor_execution_feedback_digest": pkt["process_tensor_execution_feedback_digest"],
        "process_tensor_context": dict(PT),
        "boundary": boundary,
        "epoch": 1,
    }
    st["path_integral_feedback_state_digest"] = f"path-integral-feedback-state-digest-{pkt['feedback_status']}"
    return st


def run(root: pathlib.Path, name: str, pkt: dict[str, Any] | None, state: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if pkt is not None:
        dump(runtime / "physical_quantum_qi_process_tensor_execution_feedback_packet.json", pkt)
    if state is not None:
        dump(runtime / "physical_quantum_qi_path_integral_feedback_state.json", state)
    result = build_physical_quantum_qi_process_tensor_feedback_receipt_ledger(
        runtime_context=ctx(runtime),
        process_tensor_feedback_receipt_ledger_license=license_packet,
    )
    ledger = load_jsonl(runtime / "physical_quantum_qi_process_tensor_feedback_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    latest = ledger[-1]
    assert latest["boundary"]["process_tensor_feedback_receipt_only"] is True, label
    assert latest["boundary"]["non_markov_feedback_preserved"] is True, label
    assert latest["boundary"]["path_integral_feedback_traceable"] is True, label
    assert latest["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        pkt = packet("process_tensor_feedback_reinforce_next_cycle")
        out, ledger = run(root, "reinforce", pkt, state_for(pkt), lic())
        assert_ready("reinforce", out, ledger)
        assert out["path_weight_delta"] == 1
        assert out["memory_feedback_weight"] == 1
        assert out["external_backaction_weight"] == 1
        assert out["next_cycle_amplitude_delta"] == 1

        pkt = packet("process_tensor_feedback_hold_context")
        out, ledger = run(root, "hold", pkt, state_for(pkt), lic())
        assert_ready("hold", out, ledger)
        assert out["path_weight_delta"] == 0

        pkt = packet("process_tensor_feedback_block_context")
        out, ledger = run(root, "block", pkt, state_for(pkt), lic())
        assert_ready("block", out, ledger)
        assert out["path_weight_delta"] == -1

        pkt = packet("process_tensor_feedback_reinforce_next_cycle")
        out, ledger = run(root, "chain", pkt, state_for(pkt), lic())
        assert_ready("chain_1", out, ledger)
        pkt2 = packet("process_tensor_feedback_hold_context")
        out, ledger = run(root, "chain", pkt2, state_for(pkt2), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        pkt = packet("process_tensor_feedback_reinforce_next_cycle", bad_boundary=True)
        out, ledger = run(root, "bad_boundary", pkt, state_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_BLOCKED"
        assert "process_tensor_execution_feedback_boundary_runtime_local_feedback_only_missing" in out["blockers"]
        assert ledger == []

        pkt = packet("process_tensor_feedback_reinforce_next_cycle", bad_kernel=True)
        out, ledger = run(root, "bad_kernel", pkt, state_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_BLOCKED"
        assert "process_tensor_feedback_kernel_process_tensor_feedback_not_truth_missing" in out["blockers"]
        assert ledger == []

        pkt = packet("process_tensor_feedback_reinforce_next_cycle")
        out, ledger = run(root, "state_mismatch", pkt, state_for(pkt, mismatch=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_BLOCKED"
        assert "path_integral_feedback_state_path_weight_delta_mismatch" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing_state", packet("process_tensor_feedback_hold_context"), None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_BLOCKED"
        assert "path_integral_feedback_state_missing_or_invalid" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "license", packet("process_tensor_feedback_hold_context"), state_for(packet("process_tensor_feedback_hold_context")), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_process_tensor_feedback_receipt_ledger_v12_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
