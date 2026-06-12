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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_v13_5 import build_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_v13_4 import build_physical_quantum_qi_cycle_gate_reentry_integration
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge_v13_17 import build_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge

PT = {
    "process_tensor_digest": "pt-digest-v13-17",
    "memory_kernel_digest": "memory-kernel-digest-v13-17",
    "history_window_digest": "history-window-digest-v13-17",
    "instrument_trace_digest": "instrument-trace-digest-v13-17",
    "non_markov_context_digest": "non-markov-context-digest-v13-17",
}
PACKET_BOUNDARY = {
    "cycle_gate_reentry_integration_only": True,
    "candidate_weighting_cycle_handoff_receipt_required": True,
    "integrates_cycle_gate": True,
    "integrates_admissible_candidate_set": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "integration_not_direct_execution": True,
    "license_gated_integration": True,
    "fail_closed_on_boundary_loss": True,
}
GATE_BOUNDARY = {
    "integrated_cycle_gate_state_only": True,
    "from_candidate_weighting_cycle_handoff_receipt": True,
    "uses_process_tensor_feedback": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}
SET_BOUNDARY = {
    "integrated_admissible_candidate_set_only": True,
    "from_candidate_weighting_cycle_handoff_receipt": True,
    "uses_process_tensor_feedback": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}
HANDOFF_RECEIPT_BOUNDARY = {
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
        "physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge_enabled": True,
        "apply_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge": True,
        "runtime_root": str(root),
    }


def bridge_lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_LICENSE_READY",
        "v13_4_integration_packet_read_allowed": True,
        "v13_4_integrated_cycle_gate_state_read_allowed": True,
        "v13_4_integrated_admissible_candidate_set_read_allowed": True,
        "v13_5_integration_receipt_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


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


def v13_5_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger": True,
        "runtime_root": str(root),
    }


def v13_5_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_LICENSE_READY",
        "integration_packet_read_allowed": True,
        "integrated_cycle_gate_state_read_allowed": True,
        "integrated_admissible_candidate_set_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def parts(kind: str) -> tuple[str, str, str, int, dict[str, Any]]:
    if kind == "admit":
        return "cycle_gate_reentry_integration_admit", "integrated_cycle_gate_admit", "integrated_admissible_candidate_set_admit", 1, {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if kind == "hold":
        return "cycle_gate_reentry_integration_hold", "integrated_cycle_gate_hold", "integrated_admissible_candidate_set_probe", 1, {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return "cycle_gate_reentry_integration_block", "integrated_cycle_gate_block", "integrated_admissible_candidate_set_block", 0, {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def handoff_status(kind: str) -> str:
    return {"admit": "candidate_weighting_cycle_handoff_reinforce", "hold": "candidate_weighting_cycle_handoff_probe", "block": "candidate_weighting_cycle_handoff_barrier"}[kind]


def write_integration_inputs(runtime: pathlib.Path, kind: str, *, bad_packet_boundary: bool = False, bad_gate: bool = False, bad_set: bool = False, bad_count: bool = False, bad_weight: bool = False, missing_context: bool = False) -> None:
    integration, gate_status, set_status, count, weight = parts(kind)
    if bad_weight:
        if kind == "admit":
            weight["path_weight_delta"] = 0
        elif kind == "hold":
            weight["barrier_potential_required"] = True
        else:
            weight["barrier_blocks_ready_weight"] = False
    context = dict(PT)
    if missing_context:
        context["instrument_trace_digest"] = ""
    boundary = dict(PACKET_BOUNDARY)
    if bad_packet_boundary:
        boundary["integrates_cycle_gate"] = False
    candidates = [{"candidate_id": "candidate-v13-17", "source": "bridge-test"}] if count == 1 else []
    if bad_count:
        candidates = [] if count == 1 else [{"candidate_id": "unexpected"}]
    digest = f"integration-digest-{kind}"
    packet = {
        "version": "physical_quantum_qi_cycle_gate_reentry_integration_packet_v13_4",
        "cycle_gate_reentry_integration_considered": True,
        "integration_status": integration,
        "integrated_cycle_gate_status": "wrong_gate" if bad_gate else gate_status,
        "integrated_admissible_candidate_set_status": "wrong_set" if bad_set else set_status,
        "integrated_candidates": candidates,
        "candidate_weighting": dict(weight),
        "process_tensor_context": context,
        "source_digests": {
            "candidate_weighting_cycle_handoff_receipt": "handoff-receipt-digest-v13-17",
            "candidate_weighting_cycle_handoff": "handoff-digest-v13-17",
        },
        "boundary": boundary,
        "cycle_gate_reentry_integration_digest": digest,
        "epoch": 1,
    }
    gate = {
        "version": "physical_quantum_qi_integrated_cycle_gate_state_v13_4",
        "integrated_cycle_gate_ready": True,
        "integrated_cycle_gate_status": gate_status,
        "candidate_weighting": dict(weight),
        "source_cycle_gate_reentry_integration_digest": digest,
        "process_tensor_context": context,
        "boundary": dict(GATE_BOUNDARY),
        "integrated_cycle_gate_state_digest": f"gate-state-digest-{kind}",
        "epoch": 1,
    }
    cset = {
        "version": "physical_quantum_qi_integrated_admissible_candidate_set_v13_4",
        "integrated_admissible_candidate_set_ready": True,
        "integrated_admissible_candidate_set_status": set_status,
        "admissible_candidate_count": count,
        "integrated_candidates": candidates if not bad_count else ([] if count == 1 else [{"candidate_id": "unexpected"}]),
        "candidate_weighting": dict(weight),
        "source_cycle_gate_reentry_integration_digest": digest,
        "process_tensor_context": context,
        "boundary": dict(SET_BOUNDARY),
        "integrated_admissible_candidate_set_digest": f"candidate-set-digest-{kind}",
        "epoch": 1,
    }
    dump(runtime / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json", packet)
    dump(runtime / "physical_quantum_qi_integrated_cycle_gate_state.json", gate)
    dump(runtime / "physical_quantum_qi_integrated_admissible_candidate_set.json", cset)


def handoff_receipt(kind: str) -> dict[str, Any]:
    _, _, _, _, weight = parts(kind)
    return {
        "version": "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_record_v13_3",
        "record_type": "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt",
        "handoff_status": handoff_status(kind),
        "cycle_gate_decision": "reweight_candidate" if kind == "admit" else ("hold_candidate" if kind == "hold" else "block_candidate"),
        "admissible_candidate_seed_mode": "reinforce_admissible_candidate_seed" if kind == "admit" else ("probe_candidate_seed" if kind == "hold" else "barrier_candidate_seed"),
        "candidate_weighting": dict(weight),
        "process_tensor_context": dict(PT),
        "source_candidate_weighting_cycle_handoff_digest": "handoff-digest-v13-17",
        "source_closed_loop_reentry_receipt_digest": "closed-loop-reentry-receipt-digest-v13-17",
        "prev_record_digest": "GENESIS",
        "record_digest": "handoff-receipt-digest-v13-17",
        "boundary": {
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
        },
        "epoch": 1,
    }


def run_bridge(root: pathlib.Path, name: str, *, kind: str | None, license_packet: dict[str, Any], **kwargs: Any) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if kind is not None:
        write_integration_inputs(runtime, kind, **kwargs)
    out = build_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge(
        runtime_context=bridge_ctx(runtime),
        v13_4_to_v13_5_integration_receipt_bridge_license=license_packet,
    ).to_dict()
    ready = load_json(runtime / "physical_quantum_qi_v13_5_cycle_gate_reentry_integration_receipt_ready_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge_ledger.jsonl")
    return out, ready, ledger


def assert_bridge_ready(label: str, out: dict[str, Any], ready: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_READY", (label, out)
    assert out["receipt_ready_state_written"] is True, label
    assert out["bridge_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert ready["boundary"]["can_feed_v13_5_cycle_gate_reentry_integration_receipt_ledger"] is True, label
    assert ready["boundary"]["does_not_run_receipt_ledger"] is True, label
    assert ledger[-1]["boundary"]["v13_5_integration_receipt_ready_state_traceable"] is True, label


def assert_v13_5_accepts(runtime: pathlib.Path, label: str, expected: str, gate_status: str, set_status: str, count: int) -> None:
    out = build_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger(
        runtime_context=v13_5_ctx(runtime),
        cycle_gate_reentry_integration_receipt_ledger_license=v13_5_lic(),
    ).to_dict()
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_READY", (label, out)
    assert out["integration_status"] == expected, (label, out)
    assert out["integrated_cycle_gate_status"] == gate_status, (label, out)
    assert out["integrated_admissible_candidate_set_status"] == set_status, (label, out)
    assert out["admissible_candidate_count"] == count, (label, out)
    assert out["ledger_appended"] is True, label


def run_full_v13_4_to_v13_5(root: pathlib.Path, kind: str) -> None:
    runtime = root / f"full_{kind}"
    append_jsonl(runtime / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl", handoff_receipt(kind))
    v13_4 = build_physical_quantum_qi_cycle_gate_reentry_integration(
        runtime_context=v13_4_ctx(runtime),
        cycle_gate_reentry_integration_license=v13_4_lic(),
    ).to_dict()
    assert v13_4["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_READY", v13_4
    out, ready, ledger = run_bridge(root, f"full_{kind}", kind=None, license_packet=bridge_lic())
    assert_bridge_ready(f"full_{kind}", out, ready, ledger)
    expected, gate_status, set_status, count, _ = parts(kind)
    assert_v13_5_accepts(runtime, f"full_{kind}", expected, gate_status, set_status, count)


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        for kind in ["admit", "hold", "block"]:
            out, ready, ledger = run_bridge(root, kind, kind=kind, license_packet=bridge_lic())
            assert_bridge_ready(kind, out, ready, ledger)
            expected, gate_status, set_status, count, _ = parts(kind)
            assert out["integration_status"] == expected
            assert out["integrated_cycle_gate_status"] == gate_status
            assert out["integrated_admissible_candidate_set_status"] == set_status
            assert_v13_5_accepts(root / kind, kind, expected, gate_status, set_status, count)

        for kind in ["admit", "hold", "block"]:
            run_full_v13_4_to_v13_5(root, kind)

        out, ready, ledger = run_bridge(root, "chain", kind="admit", license_packet=bridge_lic())
        assert_bridge_ready("chain_1", out, ready, ledger)
        out, ready, ledger = run_bridge(root, "chain", kind="hold", license_packet=bridge_lic())
        assert_bridge_ready("chain_2", out, ready, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        out, ready, ledger = run_bridge(root, "bad_packet_boundary", kind="admit", license_packet=bridge_lic(), bad_packet_boundary=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_BLOCKED"
        assert "cycle_gate_reentry_integration_boundary_integrates_cycle_gate_missing" in out["blockers"]
        assert ready == {}
        assert ledger == []

        out, ready, ledger = run_bridge(root, "bad_gate", kind="hold", license_packet=bridge_lic(), bad_gate=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_BLOCKED"
        assert "cycle_gate_reentry_integration_gate_status_mismatch" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "bad_set", kind="block", license_packet=bridge_lic(), bad_set=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_BLOCKED"
        assert "cycle_gate_reentry_integration_candidate_set_status_mismatch" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "bad_count", kind="admit", license_packet=bridge_lic(), bad_count=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_BLOCKED"
        assert "cycle_gate_reentry_integration_candidate_count_mismatch" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "bad_weight", kind="block", license_packet=bridge_lic(), bad_weight=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_BLOCKED"
        assert "v13_5_bridge_block_weighting_invalid" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "missing_context", kind="admit", license_packet=bridge_lic(), missing_context=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_BLOCKED"
        assert "process_tensor_context_instrument_trace_digest_missing" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "missing", kind=None, license_packet=bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_BLOCKED"
        assert "cycle_gate_reentry_integration_packet_missing_or_invalid" in out["blockers"]
        assert "integrated_cycle_gate_state_missing_or_invalid" in out["blockers"]
        assert "integrated_admissible_candidate_set_missing_or_invalid" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "license", kind="admit", license_packet=bridge_lic(v13_5_integration_receipt_ready_state_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_BLOCKED"
        assert "v13_5_integration_receipt_ready_state_write_not_allowed" in out["blockers"]
        assert ready == {}

    print("physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge_v13_17 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
