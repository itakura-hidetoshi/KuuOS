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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_closed_loop_path_integral_reentry_v13_0 import build_physical_quantum_qi_closed_loop_path_integral_reentry
from runtime.kuuos_runtime_daemon_physical_quantum_qi_feedback_to_reentry_weighting_bridge_v12_9 import build_physical_quantum_qi_feedback_to_reentry_weighting_bridge
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_v13_12 import build_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge

PT = {
    "process_tensor_digest": "pt-digest-v13-12",
    "memory_kernel_digest": "memory-kernel-digest-v13-12",
    "history_window_digest": "history-window-digest-v13-12",
    "instrument_trace_digest": "instrument-trace-digest-v13-12",
    "non_markov_context_digest": "non-markov-context-digest-v13-12",
}
PACKET_BOUNDARY = {
    "feedback_to_reentry_weighting_bridge_only": True,
    "process_tensor_feedback_required": True,
    "feeds_next_path_integral_reentry": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "bridge_not_unbounded_execution": True,
    "license_gated_bridge": True,
    "fail_closed_on_boundary_loss": True,
}
STATE_BOUNDARY = {
    "reentry_weighting_state_only": True,
    "can_feed_next_path_integral_reentry": True,
    "non_markov_feedback_preserved": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}
FEEDBACK_RECEIPT_BOUNDARY = {
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


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def bridge_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_enabled": True,
        "apply_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge": True,
        "runtime_root": str(root),
    }


def bridge_lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_LICENSE_READY",
        "v12_9_feedback_to_reentry_weighting_packet_read_allowed": True,
        "v12_9_reentry_weighting_state_read_allowed": True,
        "v13_0_closed_loop_reentry_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


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


def v13_0_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_closed_loop_path_integral_reentry_enabled": True,
        "apply_physical_quantum_qi_closed_loop_path_integral_reentry": True,
        "runtime_root": str(root),
    }


def v13_0_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_LICENSE_READY",
        "reentry_weighting_state_read_allowed": True,
        "closed_loop_reentry_packet_write_allowed": True,
        "candidate_weighting_cycle_state_write_allowed": True,
        "closed_loop_reentry_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def kind_parts(kind: str) -> tuple[str, str, str, dict[str, Any]]:
    if kind == "reinforce":
        return "reentry_weighting_reinforce", "reinforce_path_weight", "closed_loop_reentry_reinforced", {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if kind == "probe":
        return "reentry_weighting_hold", "open_probe_potential", "closed_loop_reentry_probe_opened", {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return "reentry_weighting_block", "add_barrier_potential", "closed_loop_reentry_barrier_added", {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def feedback_status(kind: str) -> str:
    return {
        "reinforce": "process_tensor_feedback_reinforce_next_cycle",
        "probe": "process_tensor_feedback_hold_context",
        "barrier": "process_tensor_feedback_block_context",
    }[kind]


def packet_and_state(kind: str, *, bad_packet_boundary: bool = False, bad_state_boundary: bool = False, bad_weight: bool = False, bad_status: bool = False, missing_context: bool = False, digest_mismatch: bool = False) -> tuple[dict[str, Any], dict[str, Any]]:
    status, action, _, weighting = kind_parts(kind)
    if bad_weight:
        if kind == "reinforce":
            weighting["path_weight_delta"] = 0
        elif kind == "probe":
            weighting["barrier_potential_required"] = True
        else:
            weighting["barrier_blocks_ready_weight"] = False
    context = dict(PT)
    if missing_context:
        context["memory_kernel_digest"] = ""
    packet_boundary = dict(PACKET_BOUNDARY)
    if bad_packet_boundary:
        packet_boundary["feeds_next_path_integral_reentry"] = False
    packet = {
        "version": "physical_quantum_qi_feedback_to_reentry_weighting_bridge_packet_v12_9",
        "feedback_to_reentry_weighting_bridge_considered": True,
        "feedback_status": feedback_status(kind),
        "reentry_weighting_status": "wrong_status" if bad_status else status,
        "reentry_weighting_action": action,
        "candidate_weighting": dict(weighting),
        "process_tensor_context": context,
        "source_digests": {
            "process_tensor_feedback_receipt": "feedback-receipt-digest-v13-12",
            "process_tensor_execution_feedback": "feedback-packet-digest-v13-12",
            "execution_record": "execution-record-digest-v13-12",
        },
        "boundary": packet_boundary,
        "epoch": 1,
    }
    packet["feedback_to_reentry_weighting_bridge_digest"] = f"v12-9-bridge-digest-{kind}"
    state_boundary = dict(STATE_BOUNDARY)
    if bad_state_boundary:
        state_boundary["can_feed_next_path_integral_reentry"] = False
    state = {
        "version": "physical_quantum_qi_reentry_weighting_state_v12_9",
        "reentry_weighting_state_ready": True,
        "feedback_status": feedback_status(kind),
        "reentry_weighting_status": status,
        "reentry_weighting_action": action,
        "candidate_weighting": dict(weighting),
        "can_feed_next_path_integral_reentry": True,
        "source_feedback_to_reentry_weighting_bridge_digest": "mismatch" if digest_mismatch else packet["feedback_to_reentry_weighting_bridge_digest"],
        "process_tensor_context": context,
        "boundary": state_boundary,
        "epoch": 1,
    }
    state["reentry_weighting_state_digest"] = f"v12-9-state-digest-{kind}"
    return packet, state


def feedback_receipt(kind: str) -> dict[str, Any]:
    status, action, _, weighting = kind_parts(kind)
    return {
        "version": "physical_quantum_qi_process_tensor_feedback_receipt_record_v12_8",
        "record_type": "physical_quantum_qi_process_tensor_feedback_receipt",
        "feedback_status": feedback_status(kind),
        "execution_status": "guarded_transition_executed" if kind == "reinforce" else ("guarded_transition_hold" if kind == "probe" else "guarded_transition_block"),
        "path_weight_delta": weighting["path_weight_delta"],
        "memory_feedback_weight": weighting["memory_feedback_weight"],
        "external_backaction_weight": weighting["external_backaction_weight"],
        "next_cycle_amplitude_delta": weighting["next_cycle_amplitude_delta"],
        "observed_effects": {},
        "process_tensor_context": dict(PT),
        "source_process_tensor_execution_feedback_digest": "feedback-packet-digest-v13-12",
        "source_execution_record_digest": "execution-record-digest-v13-12",
        "source_next_cycle_state_digest": "next-cycle-digest-v13-12",
        "source_memory_consumption_digest": "memory-digest-v13-12",
        "source_external_state_mutation_digest": "external-digest-v13-12",
        "prev_record_digest": "GENESIS",
        "record_digest": f"feedback-receipt-digest-{kind}",
        "boundary": dict(FEEDBACK_RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def write_pair(runtime: pathlib.Path, pkt: dict[str, Any] | None, state: dict[str, Any] | None) -> None:
    if pkt is not None:
        dump(runtime / "physical_quantum_qi_feedback_to_reentry_weighting_bridge_packet.json", pkt)
    if state is not None:
        dump(runtime / "physical_quantum_qi_reentry_weighting_state.json", state)


def run_bridge(root: pathlib.Path, name: str, pkt: dict[str, Any] | None, state: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    write_pair(runtime, pkt, state)
    out = build_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge(
        runtime_context=bridge_ctx(runtime),
        v12_9_to_v13_0_reentry_bridge_license=license_packet,
    ).to_dict()
    ready = load_json(runtime / "physical_quantum_qi_v13_0_closed_loop_reentry_ready_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_ledger.jsonl")
    return out, ready, ledger


def assert_bridge_ready(label: str, out: dict[str, Any], ready: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_READY", (label, out)
    assert out["reentry_ready_state_written"] is True, label
    assert out["bridge_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert ready["boundary"]["can_feed_v13_0_closed_loop_path_integral_reentry"] is True, label
    assert ready["boundary"]["does_not_run_closed_loop_reentry"] is True, label
    assert ledger[-1]["boundary"]["v13_0_closed_loop_reentry_ready_state_traceable"] is True, label


def assert_v13_0_accepts(runtime: pathlib.Path, label: str, expected: str) -> None:
    out = build_physical_quantum_qi_closed_loop_path_integral_reentry(
        runtime_context=v13_0_ctx(runtime),
        closed_loop_path_integral_reentry_license=v13_0_lic(),
    ).to_dict()
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_READY", (label, out)
    assert out["closed_loop_reentry_status"] == expected, (label, out)
    assert out["candidate_weighting_cycle_updated"] is True, label
    assert out["closed_loop_ledger_appended"] is True, label


def run_full_v12_8_to_v13_0(root: pathlib.Path, kind: str) -> None:
    runtime = root / f"full_{kind}"
    append_jsonl(runtime / "physical_quantum_qi_process_tensor_feedback_receipt_ledger.jsonl", feedback_receipt(kind))
    v12_9 = build_physical_quantum_qi_feedback_to_reentry_weighting_bridge(
        runtime_context=v12_9_ctx(runtime),
        feedback_to_reentry_weighting_bridge_license=v12_9_lic(),
    ).to_dict()
    assert v12_9["status"] == "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_READY", v12_9
    out, ready, ledger = run_bridge(root, f"full_{kind}", None, None, bridge_lic())
    assert_bridge_ready(f"full_{kind}", out, ready, ledger)
    _, _, expected, _ = kind_parts(kind)
    assert out["expected_v13_0_closed_loop_reentry_status"] == expected
    assert_v13_0_accepts(runtime, f"full_{kind}", expected)


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        for kind in ["reinforce", "probe", "barrier"]:
            pkt, st = packet_and_state(kind)
            out, ready, ledger = run_bridge(root, kind, pkt, st, bridge_lic())
            assert_bridge_ready(kind, out, ready, ledger)
            _, _, expected, _ = kind_parts(kind)
            assert out["expected_v13_0_closed_loop_reentry_status"] == expected
            assert_v13_0_accepts(root / kind, kind, expected)

        for kind in ["reinforce", "probe", "barrier"]:
            run_full_v12_8_to_v13_0(root, kind)

        pkt, st = packet_and_state("reinforce")
        out, ready, ledger = run_bridge(root, "chain", pkt, st, bridge_lic())
        assert_bridge_ready("chain_1", out, ready, ledger)
        pkt2, st2 = packet_and_state("probe")
        out, ready, ledger = run_bridge(root, "chain", pkt2, st2, bridge_lic())
        assert_bridge_ready("chain_2", out, ready, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        pkt, st = packet_and_state("reinforce", bad_packet_boundary=True)
        out, ready, ledger = run_bridge(root, "bad_packet_boundary", pkt, st, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_BLOCKED"
        assert "feedback_to_reentry_weighting_bridge_boundary_feeds_next_path_integral_reentry_missing" in out["blockers"]
        assert ready == {}
        assert ledger == []

        pkt, st = packet_and_state("probe", bad_state_boundary=True)
        out, ready, ledger = run_bridge(root, "bad_state_boundary", pkt, st, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_BLOCKED"
        assert "reentry_weighting_state_boundary_can_feed_next_path_integral_reentry_missing" in out["blockers"]
        assert ready == {}

        pkt, st = packet_and_state("barrier", bad_weight=True)
        out, ready, ledger = run_bridge(root, "bad_weight", pkt, st, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_BLOCKED"
        assert "v13_0_reentry_bridge_barrier_weighting_invalid" in out["blockers"]
        assert ready == {}

        pkt, st = packet_and_state("reinforce", bad_status=True)
        out, ready, ledger = run_bridge(root, "bad_status", pkt, st, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_BLOCKED"
        assert "reentry_weighting_packet_status_mismatch" in out["blockers"]
        assert ready == {}

        pkt, st = packet_and_state("reinforce", digest_mismatch=True)
        out, ready, ledger = run_bridge(root, "digest_mismatch", pkt, st, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_BLOCKED"
        assert "reentry_weighting_state_source_bridge_digest_mismatch" in out["blockers"]
        assert ready == {}

        pkt, st = packet_and_state("reinforce", missing_context=True)
        out, ready, ledger = run_bridge(root, "missing_context", pkt, st, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_BLOCKED"
        assert "process_tensor_context_memory_kernel_digest_missing" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "missing", None, None, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_BLOCKED"
        assert "feedback_to_reentry_weighting_bridge_packet_missing_or_invalid" in out["blockers"]
        assert "reentry_weighting_state_missing_or_invalid" in out["blockers"]
        assert ready == {}

        pkt, st = packet_and_state("reinforce")
        out, ready, ledger = run_bridge(root, "license", pkt, st, bridge_lic(v13_0_closed_loop_reentry_ready_state_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_BLOCKED"
        assert "v13_0_closed_loop_reentry_ready_state_write_not_allowed" in out["blockers"]
        assert ready == {}

    print("physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_v13_12 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
