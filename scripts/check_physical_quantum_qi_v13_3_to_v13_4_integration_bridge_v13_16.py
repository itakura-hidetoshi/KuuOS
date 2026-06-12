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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_v13_3 import build_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_v13_4 import build_physical_quantum_qi_cycle_gate_reentry_integration
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_3_to_v13_4_integration_bridge_v13_16 import build_physical_quantum_qi_v13_3_to_v13_4_integration_bridge

PT = {
    "process_tensor_digest": "pt-digest-v13-16",
    "memory_kernel_digest": "memory-kernel-digest-v13-16",
    "history_window_digest": "history-window-digest-v13-16",
    "instrument_trace_digest": "instrument-trace-digest-v13-16",
    "non_markov_context_digest": "non-markov-context-digest-v13-16",
}
RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "candidate_weighting_cycle_handoff_receipt_only": True,
    "cycle_gate_input_traceable": True,
    "admissible_candidate_set_seed_traceable": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "handoff_not_direct_execution": True,
    "replayable_receipt": True,
    "fail_closed_on_boundary_loss": True,
}
HANDOFF_BOUNDARY = {
    "candidate_weighting_cycle_handoff_only": True,
    "closed_loop_reentry_receipt_required": True,
    "hands_off_to_cycle_gate": True,
    "hands_off_to_admissible_candidate_set": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "handoff_not_direct_execution": True,
    "license_gated_handoff": True,
    "fail_closed_on_boundary_loss": True,
}
GATE_BOUNDARY = {
    "cycle_gate_input_only": True,
    "from_closed_loop_reentry_handoff": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}
SEED_BOUNDARY = {
    "admissible_candidate_set_seed_only": True,
    "from_closed_loop_reentry_handoff": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


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
        "physical_quantum_qi_v13_3_to_v13_4_integration_bridge_enabled": True,
        "apply_physical_quantum_qi_v13_3_to_v13_4_integration_bridge": True,
        "runtime_root": str(root),
    }


def bridge_lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_LICENSE_READY",
        "v13_3_handoff_receipt_ledger_read_allowed": True,
        "v13_4_integration_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def v13_3_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger": True,
        "runtime_root": str(root),
    }


def v13_3_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_LICENSE_READY",
        "handoff_packet_read_allowed": True,
        "cycle_gate_input_read_allowed": True,
        "admissible_candidate_set_seed_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def v13_4_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_cycle_gate_reentry_integration_enabled": True,
        "apply_physical_quantum_qi_cycle_gate_reentry_integration": True,
        "runtime_root": str(root),
    }


def v13_4_lic() -> dict[str, Any]:
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


def parts(kind: str) -> tuple[str, str, str, str, str, dict[str, Any]]:
    if kind == "reinforce":
        return "candidate_weighting_cycle_handoff_reinforce", "reweight_candidate", "reinforce_admissible_candidate_seed", "cycle_gate_reentry_integration_admit", "integrated_cycle_gate_admit", {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if kind == "probe":
        return "candidate_weighting_cycle_handoff_probe", "hold_candidate", "probe_candidate_seed", "cycle_gate_reentry_integration_hold", "integrated_cycle_gate_hold", {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return "candidate_weighting_cycle_handoff_barrier", "block_candidate", "barrier_candidate_seed", "cycle_gate_reentry_integration_block", "integrated_cycle_gate_block", {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def receipt(kind: str, *, bad_boundary: bool = False, bad_gate: bool = False, bad_seed: bool = False, bad_weight: bool = False, missing_context: bool = False) -> dict[str, Any]:
    handoff, gate, seed, _, _, weight = parts(kind)
    if bad_weight:
        if kind == "reinforce":
            weight["path_weight_delta"] = 0
        elif kind == "probe":
            weight["barrier_potential_required"] = True
        else:
            weight["barrier_blocks_ready_weight"] = False
    context = dict(PT)
    if missing_context:
        context["process_tensor_digest"] = ""
    boundary = dict(RECEIPT_BOUNDARY)
    if bad_boundary:
        boundary["cycle_gate_input_traceable"] = False
    return {
        "version": "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_record_v13_3",
        "record_type": "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt",
        "handoff_status": handoff,
        "cycle_gate_decision": "wrong_gate" if bad_gate else gate,
        "admissible_candidate_seed_mode": "wrong_seed" if bad_seed else seed,
        "candidate_weighting": dict(weight),
        "process_tensor_context": context,
        "source_candidate_weighting_cycle_handoff_digest": f"handoff-digest-{kind}",
        "source_closed_loop_reentry_receipt_digest": "closed-loop-reentry-receipt-digest-v13-16",
        "prev_record_digest": "GENESIS",
        "record_digest": f"handoff-receipt-digest-{kind}",
        "boundary": boundary,
        "epoch": 1,
    }


def write_handoff_inputs(runtime: pathlib.Path, kind: str) -> None:
    handoff, gate, seed, _, _, weight = parts(kind)
    packet = {
        "version": "physical_quantum_qi_candidate_weighting_cycle_handoff_packet_v13_2",
        "candidate_weighting_cycle_handoff_considered": True,
        "handoff_status": handoff,
        "cycle_gate_decision": gate,
        "admissible_candidate_seed_mode": seed,
        "candidate_weighting": dict(weight),
        "process_tensor_context": dict(PT),
        "source_digests": {"closed_loop_reentry_receipt": "closed-loop-reentry-receipt-digest-v13-16"},
        "boundary": dict(HANDOFF_BOUNDARY),
        "candidate_weighting_cycle_handoff_digest": f"handoff-digest-{kind}",
        "epoch": 1,
    }
    gate_payload = {
        "version": "physical_quantum_qi_next_cycle_gate_input_v13_2",
        "cycle_gate_input_ready": True,
        "cycle_gate_decision": gate,
        "candidate_weighting": dict(weight),
        "source_candidate_weighting_cycle_handoff_digest": packet["candidate_weighting_cycle_handoff_digest"],
        "process_tensor_context": dict(PT),
        "boundary": dict(GATE_BOUNDARY),
        "cycle_gate_input_digest": f"gate-digest-{kind}",
        "epoch": 1,
    }
    seed_payload = {
        "version": "physical_quantum_qi_admissible_candidate_set_seed_v13_2",
        "admissible_candidate_set_seed_ready": True,
        "admissible_candidate_seed_mode": seed,
        "candidate_weighting": dict(weight),
        "source_candidate_weighting_cycle_handoff_digest": packet["candidate_weighting_cycle_handoff_digest"],
        "process_tensor_context": dict(PT),
        "boundary": dict(SEED_BOUNDARY),
        "admissible_candidate_set_seed_digest": f"seed-digest-{kind}",
        "epoch": 1,
    }
    dump(runtime / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json", packet)
    dump(runtime / "physical_quantum_qi_next_cycle_gate_input.json", gate_payload)
    dump(runtime / "physical_quantum_qi_admissible_candidate_set_seed.json", seed_payload)


def run_bridge(root: pathlib.Path, name: str, rec: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if rec is not None:
        append_jsonl(runtime / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl", rec)
    out = build_physical_quantum_qi_v13_3_to_v13_4_integration_bridge(
        runtime_context=bridge_ctx(runtime),
        v13_3_to_v13_4_integration_bridge_license=license_packet,
    ).to_dict()
    ready = load_json(runtime / "physical_quantum_qi_v13_4_cycle_gate_reentry_integration_ready_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_v13_3_to_v13_4_integration_bridge_ledger.jsonl")
    return out, ready, ledger


def assert_bridge_ready(label: str, out: dict[str, Any], ready: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_READY", (label, out)
    assert out["integration_ready_state_written"] is True, label
    assert out["bridge_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert ready["boundary"]["can_feed_v13_4_cycle_gate_reentry_integration"] is True, label
    assert ready["boundary"]["does_not_run_integration_runtime"] is True, label
    assert ledger[-1]["boundary"]["v13_4_integration_ready_state_traceable"] is True, label


def assert_v13_4_accepts(runtime: pathlib.Path, label: str, expected: str, cycle_status: str) -> None:
    out = build_physical_quantum_qi_cycle_gate_reentry_integration(
        runtime_context=v13_4_ctx(runtime),
        cycle_gate_reentry_integration_license=v13_4_lic(),
    ).to_dict()
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_READY", (label, out)
    assert out["integration_status"] == expected, (label, out)
    assert out["integrated_cycle_gate_status"] == cycle_status, (label, out)
    assert out["integration_packet_written"] is True, label
    assert out["integrated_cycle_gate_state_written"] is True, label
    assert out["integrated_admissible_candidate_set_written"] is True, label
    assert out["integration_ledger_appended"] is True, label


def run_full_v13_3_to_v13_4(root: pathlib.Path, kind: str) -> None:
    runtime = root / f"full_{kind}"
    write_handoff_inputs(runtime, kind)
    v13_3 = build_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger(
        runtime_context=v13_3_ctx(runtime),
        candidate_weighting_cycle_handoff_receipt_ledger_license=v13_3_lic(),
    ).to_dict()
    assert v13_3["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_READY", v13_3
    out, ready, ledger = run_bridge(root, f"full_{kind}", None, bridge_lic())
    assert_bridge_ready(f"full_{kind}", out, ready, ledger)
    _, _, _, expected, cycle_status, _ = parts(kind)
    assert_v13_4_accepts(runtime, f"full_{kind}", expected, cycle_status)


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        for kind in ["reinforce", "probe", "barrier"]:
            out, ready, ledger = run_bridge(root, kind, receipt(kind), bridge_lic())
            assert_bridge_ready(kind, out, ready, ledger)
            _, _, _, expected, cycle_status, _ = parts(kind)
            assert out["expected_v13_4_integration_status"] == expected
            assert out["expected_v13_4_integrated_cycle_gate_status"] == cycle_status
            assert_v13_4_accepts(root / kind, kind, expected, cycle_status)

        for kind in ["reinforce", "probe", "barrier"]:
            run_full_v13_3_to_v13_4(root, kind)

        out, ready, ledger = run_bridge(root, "chain", receipt("reinforce"), bridge_lic())
        assert_bridge_ready("chain_1", out, ready, ledger)
        out, ready, ledger = run_bridge(root, "chain", receipt("probe"), bridge_lic())
        assert_bridge_ready("chain_2", out, ready, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        out, ready, ledger = run_bridge(root, "bad_boundary", receipt("reinforce", bad_boundary=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_BLOCKED"
        assert "candidate_weighting_cycle_handoff_receipt_boundary_cycle_gate_input_traceable_missing" in out["blockers"]
        assert ready == {}
        assert ledger == []

        out, ready, ledger = run_bridge(root, "bad_gate", receipt("probe", bad_gate=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_BLOCKED"
        assert "candidate_weighting_cycle_handoff_receipt_gate_decision_mismatch" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "bad_seed", receipt("barrier", bad_seed=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_BLOCKED"
        assert "candidate_weighting_cycle_handoff_receipt_seed_mode_mismatch" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "bad_weight", receipt("barrier", bad_weight=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_BLOCKED"
        assert "v13_4_bridge_barrier_weighting_invalid" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "missing_context", receipt("reinforce", missing_context=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_BLOCKED"
        assert "process_tensor_context_process_tensor_digest_missing" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "missing", None, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_BLOCKED"
        assert "candidate_weighting_cycle_handoff_receipt_ledger_missing" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "license", receipt("reinforce"), bridge_lic(v13_4_integration_ready_state_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_BLOCKED"
        assert "v13_4_integration_ready_state_write_not_allowed" in out["blockers"]
        assert ready == {}

    print("physical_quantum_qi_v13_3_to_v13_4_integration_bridge_v13_16 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
