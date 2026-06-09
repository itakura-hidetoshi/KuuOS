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
from runtime.kuuos_runtime_daemon_physical_quantum_qi_process_tensor_feedback_receipt_ledger_v12_8 import build_physical_quantum_qi_process_tensor_feedback_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_v13_11 import build_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge

PT = {
    "process_tensor_digest": "pt-digest-v13-11",
    "memory_kernel_digest": "memory-kernel-digest-v13-11",
    "history_window_digest": "history-window-digest-v13-11",
    "instrument_trace_digest": "instrument-trace-digest-v13-11",
    "non_markov_context_digest": "non-markov-context-digest-v13-11",
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
    "non_markov_feedback_preserved": True,
    "feedback_not_direct_authority": True,
}
KERNEL_FLAGS = {
    "non_markov_feedback_required": True,
    "history_window_feedback_required": True,
    "instrument_trace_feedback_required": True,
    "process_tensor_feedback_not_truth": True,
}


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def bridge_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_enabled": True,
        "apply_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge": True,
        "runtime_root": str(root),
    }


def bridge_lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_LICENSE_READY",
        "v12_7_process_tensor_feedback_packet_read_allowed": True,
        "v12_7_path_integral_feedback_state_read_allowed": True,
        "v12_8_feedback_receipt_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def v12_8_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_process_tensor_feedback_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_process_tensor_feedback_receipt_ledger": True,
        "runtime_root": str(root),
    }


def v12_8_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_LICENSE_READY",
        "process_tensor_execution_feedback_packet_read_allowed": True,
        "path_integral_feedback_state_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def v12_9_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_feedback_to_reentry_weighting_bridge_enabled": True,
        "apply_physical_quantum_qi_feedback_to_reentry_weighting_bridge": True,
        "runtime_root": str(root),
    }


def v12_9_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_LICENSE_READY",
        "process_tensor_feedback_receipt_ledger_read_allowed": True,
        "reentry_weighting_bridge_packet_write_allowed": True,
        "reentry_weighting_state_write_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def parts(kind: str) -> tuple[str, str, dict[str, Any], dict[str, Any], bool, str, str]:
    if kind == "reinforce":
        feedback = "process_tensor_feedback_reinforce_next_cycle"
        execution = "guarded_transition_executed"
        kernel = {
            **KERNEL_FLAGS,
            "feedback_status": feedback,
            "path_weight_delta": 2,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
        observed = {"next_cycle_observed": True, "memory_feedback_observed": True, "external_backaction_observed": True}
        return feedback, execution, kernel, observed, True, "reentry_weighting_reinforce", "reinforce_path_weight"
    if kind == "hold":
        feedback = "process_tensor_feedback_hold_context"
        execution = "guarded_transition_hold"
        kernel = {
            **KERNEL_FLAGS,
            "feedback_status": feedback,
            "path_weight_delta": 0,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
        observed = {"next_cycle_observed": False, "memory_feedback_observed": False, "external_backaction_observed": False}
        return feedback, execution, kernel, observed, False, "reentry_weighting_hold", "open_probe_potential"
    feedback = "process_tensor_feedback_block_context"
    execution = "guarded_transition_block"
    kernel = {
        **KERNEL_FLAGS,
        "feedback_status": feedback,
        "path_weight_delta": -1,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }
    observed = {"next_cycle_observed": False, "memory_feedback_observed": False, "external_backaction_observed": False}
    return feedback, execution, kernel, observed, False, "reentry_weighting_block", "add_barrier_potential"


def packet(kind: str, *, bad_boundary: bool = False, bad_kernel: bool = False, bad_status: bool = False, missing_context: bool = False) -> dict[str, Any]:
    feedback, execution, kernel, observed, _, _, _ = parts(kind)
    if bad_kernel:
        if kind == "reinforce":
            kernel["memory_feedback_weight"] = 0
        elif kind == "hold":
            kernel["external_backaction_weight"] = 1
        else:
            kernel["path_weight_delta"] = 0
    boundary = dict(PACKET_BOUNDARY)
    if bad_boundary:
        boundary["feeds_path_integral_weighting"] = False
    context = dict(PT)
    if missing_context:
        context["process_tensor_digest"] = ""
    payload = {
        "version": "physical_quantum_qi_process_tensor_execution_feedback_packet_v12_7",
        "feedback_status": feedback,
        "execution_status": "wrong_execution" if bad_status else execution,
        "process_tensor_feedback_kernel": kernel,
        "observed_effects": observed,
        "process_tensor_context": context,
        "source_digests": {
            "execution_record": "execution-record-digest-v13-11",
            "next_cycle_state": "next-cycle-state-digest-v13-11" if kind == "reinforce" else "",
            "memory_consumption": "memory-consumption-digest-v13-11" if kind == "reinforce" else "",
            "external_state_mutation": "external-state-mutation-digest-v13-11" if kind == "reinforce" else "",
        },
        "boundary": boundary,
        "epoch": 1,
    }
    payload["process_tensor_execution_feedback_digest"] = f"process-tensor-feedback-digest-{kind}"
    return payload


def state_for(pkt: dict[str, Any], *, mismatch: bool = False, bad_boundary: bool = False) -> dict[str, Any]:
    kernel = dict(pkt["process_tensor_feedback_kernel"])
    if mismatch:
        kernel["path_weight_delta"] = int(kernel.get("path_weight_delta", 0)) + 1
    boundary = dict(STATE_BOUNDARY)
    boundary["can_feed_next_path_integral_cycle"] = pkt["feedback_status"] == "process_tensor_feedback_reinforce_next_cycle"
    if bad_boundary:
        boundary["non_markov_feedback_preserved"] = False
    payload = {
        "version": "physical_quantum_qi_path_integral_feedback_state_v12_7",
        "path_integral_feedback_ready": True,
        "feedback_status": pkt["feedback_status"],
        "path_weight_delta": kernel["path_weight_delta"],
        "memory_feedback_weight": kernel["memory_feedback_weight"],
        "external_backaction_weight": kernel["external_backaction_weight"],
        "next_cycle_amplitude_delta": kernel["next_cycle_amplitude_delta"],
        "source_process_tensor_execution_feedback_digest": pkt["process_tensor_execution_feedback_digest"],
        "process_tensor_context": dict(pkt["process_tensor_context"]),
        "boundary": boundary,
        "epoch": 1,
    }
    payload["path_integral_feedback_state_digest"] = f"path-integral-feedback-state-digest-{pkt['feedback_status']}"
    return payload


def write_inputs(runtime: pathlib.Path, pkt: dict[str, Any] | None, state: dict[str, Any] | None) -> None:
    if pkt is not None:
        dump(runtime / "physical_quantum_qi_process_tensor_execution_feedback_packet.json", pkt)
    if state is not None:
        dump(runtime / "physical_quantum_qi_path_integral_feedback_state.json", state)


def run_bridge(root: pathlib.Path, name: str, pkt: dict[str, Any] | None, state: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    write_inputs(runtime, pkt, state)
    out = build_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge(
        runtime_context=bridge_ctx(runtime),
        v12_7_to_v12_8_feedback_receipt_bridge_license=license_packet,
    ).to_dict()
    ready = load_json(runtime / "physical_quantum_qi_v12_8_process_tensor_feedback_receipt_ready_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_ledger.jsonl")
    return out, ready, ledger


def assert_bridge_ready(label: str, out: dict[str, Any], ready: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_READY", (label, out)
    assert out["feedback_receipt_ready_state_written"] is True, label
    assert out["bridge_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert ready["boundary"]["can_feed_v12_8_process_tensor_feedback_receipt_ledger"] is True, label
    assert ready["boundary"]["can_feed_v12_9_feedback_to_reentry_weighting_bridge_after_receipt"] is True, label
    assert ledger[-1]["boundary"]["v12_8_feedback_receipt_ready_state_traceable"] is True, label


def assert_v12_8_v12_9_accept(runtime: pathlib.Path, label: str, expected_status: str, expected_action: str) -> None:
    v12_8 = build_physical_quantum_qi_process_tensor_feedback_receipt_ledger(
        runtime_context=v12_8_ctx(runtime),
        process_tensor_feedback_receipt_ledger_license=v12_8_lic(),
    ).to_dict()
    assert v12_8["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_READY", (label, v12_8)
    assert v12_8["ledger_appended"] is True, label
    v12_9 = build_physical_quantum_qi_feedback_to_reentry_weighting_bridge(
        runtime_context=v12_9_ctx(runtime),
        feedback_to_reentry_weighting_bridge_license=v12_9_lic(),
    ).to_dict()
    assert v12_9["status"] == "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_READY", (label, v12_9)
    assert v12_9["reentry_weighting_status"] == expected_status, (label, v12_9)
    assert v12_9["reentry_weighting_action"] == expected_action, (label, v12_9)


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        for kind in ["reinforce", "hold", "block"]:
            pkt = packet(kind)
            st = state_for(pkt)
            out, ready, ledger = run_bridge(root, kind, pkt, st, bridge_lic())
            assert_bridge_ready(kind, out, ready, ledger)
            _, _, _, _, _, expected_status, expected_action = parts(kind)
            assert out["expected_v12_9_reentry_weighting_status"] == expected_status
            assert out["expected_v12_9_reentry_weighting_action"] == expected_action
            assert_v12_8_v12_9_accept(root / kind, kind, expected_status, expected_action)

        pkt = packet("reinforce")
        st = state_for(pkt)
        out, ready, ledger = run_bridge(root, "chain", pkt, st, bridge_lic())
        assert_bridge_ready("chain_1", out, ready, ledger)
        pkt2 = packet("hold")
        st2 = state_for(pkt2)
        out, ready, ledger = run_bridge(root, "chain", pkt2, st2, bridge_lic())
        assert_bridge_ready("chain_2", out, ready, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        pkt = packet("reinforce", bad_boundary=True)
        out, ready, ledger = run_bridge(root, "bad_boundary", pkt, state_for(pkt), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_BLOCKED"
        assert "v12_7_process_tensor_feedback_boundary_feeds_path_integral_weighting_missing" in out["blockers"]
        assert ready == {}
        assert ledger == []

        pkt = packet("reinforce", bad_kernel=True)
        out, ready, ledger = run_bridge(root, "bad_kernel", pkt, state_for(pkt), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_BLOCKED"
        assert "v12_8_bridge_reinforce_without_memory_feedback_weight" in out["blockers"]
        assert ready == {}

        pkt = packet("hold")
        out, ready, ledger = run_bridge(root, "state_mismatch", pkt, state_for(pkt, mismatch=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_BLOCKED"
        assert "v12_7_path_integral_feedback_state_path_weight_delta_mismatch" in out["blockers"]
        assert ready == {}

        pkt = packet("block", bad_status=True)
        out, ready, ledger = run_bridge(root, "status_mismatch", pkt, state_for(pkt), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_BLOCKED"
        assert "v12_7_process_tensor_feedback_execution_status_mismatch" in out["blockers"]
        assert ready == {}

        pkt = packet("reinforce", missing_context=True)
        out, ready, ledger = run_bridge(root, "missing_context", pkt, state_for(pkt), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_BLOCKED"
        assert "process_tensor_context_process_tensor_digest_missing" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "missing", None, None, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_BLOCKED"
        assert "v12_7_process_tensor_execution_feedback_packet_missing_or_invalid" in out["blockers"]
        assert "v12_7_path_integral_feedback_state_missing_or_invalid" in out["blockers"]
        assert ready == {}

        pkt = packet("reinforce")
        out, ready, ledger = run_bridge(root, "license", pkt, state_for(pkt), bridge_lic(v12_8_feedback_receipt_ready_state_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_BLOCKED"
        assert "v12_8_feedback_receipt_ready_state_write_not_allowed" in out["blockers"]
        assert ready == {}

    print("physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_v13_11 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
