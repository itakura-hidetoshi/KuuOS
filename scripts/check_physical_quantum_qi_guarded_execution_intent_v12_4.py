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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_guarded_execution_intent_v12_4 import build_physical_quantum_qi_guarded_execution_intent

RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "transition_candidate_envelope_receipt_only": True,
    "envelope_receipt_only": True,
    "transition_candidate_envelope_only": True,
    "envelope_build_only": True,
    "history_bearing_process_tensor": True,
    "non_markov_context_required": True,
    "multi_time_window_required": True,
    "finite_horizon_only": True,
    "memory_kernel_visible": True,
    "does_not_execute_path": True,
    "does_not_run_runner": True,
    "does_not_start_next_cycle": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_authorize_execution": True,
    "does_not_select_final_path": True,
    "does_not_promote_truth": True,
    "candidate_weighting_not_truth": True,
    "envelope_not_transition_start": True,
    "receipt_does_not_mutate_envelope_packet": True,
    "replayable_receipt": True,
    "fail_closed_on_boundary_loss": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v12-4",
    "memory_kernel_digest": "memory-kernel-digest-v12-4",
    "history_window_digest": "history-window-digest-v12-4",
    "instrument_trace_digest": "instrument-trace-digest-v12-4",
    "non_markov_context_digest": "non-markov-context-digest-v12-4",
}


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_guarded_execution_intent_enabled": True,
        "apply_physical_quantum_qi_guarded_execution_intent": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_LICENSE_READY",
        "transition_candidate_envelope_receipt_ledger_read_allowed": True,
        "guarded_execution_intent_packet_write_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def envelope(*, mismatch: bool = False, bad_boundary: bool = False, bad_weighting: bool = False) -> dict[str, Any]:
    boundary = {
        "transition_candidate_envelope_only": True,
        "envelope_build_only": True,
        "does_not_start_next_cycle": True,
        "does_not_authorize_execution": True,
        "does_not_select_final_path": True,
        "does_not_execute_path": True,
    }
    if bad_boundary:
        boundary["does_not_authorize_execution"] = False
    context = dict(PT)
    if mismatch:
        context["memory_kernel_digest"] = "mismatch"
    weighting = {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False}
    if bad_weighting:
        weighting["barrier_potential_required"] = True
    return {
        "envelope_type": "physical_quantum_qi_transition_candidate_envelope",
        "candidate_id": "candidate-admit-0",
        "corridor_lane": "admit_lane",
        "corridor_rank": 0,
        "transition_precheck_decision": "transition_precheck_admit_candidate",
        "corridor_stability_gate_decision": "corridor_stability_admit",
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "transition_candidate_envelope_digest": "transition-candidate-envelope-digest-v12-4",
        "boundary": boundary,
    }


def receipt(status: str) -> dict[str, Any]:
    precheck = {
        "transition_candidate_envelope_ready": "transition_precheck_admit_candidate",
        "transition_candidate_envelope_hold": "transition_precheck_hold_candidate",
        "transition_candidate_envelope_block": "transition_precheck_block_candidate",
    }[status]
    envs = [envelope()] if status == "transition_candidate_envelope_ready" else []
    return {
        "version": "physical_quantum_qi_transition_candidate_envelope_receipt_record_v12_3",
        "record_type": "physical_quantum_qi_transition_candidate_envelope_receipt",
        "envelope_status": status,
        "transition_precheck_decision": precheck,
        "envelope_count": len(envs),
        "transition_candidate_envelopes": envs,
        "process_tensor_context": dict(PT),
        "source_transition_candidate_envelope_packet_digest": "envelope-packet-digest-v12-4",
        "source_stable_corridor_transition_precheck_receipt_digest": "transition-precheck-receipt-digest-v12-4",
        "prev_record_digest": "GENESIS",
        "record_digest": f"transition-envelope-receipt-{status}",
        "boundary": dict(RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, record: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if record is not None:
        append_jsonl(runtime / "physical_quantum_qi_transition_candidate_envelope_receipt_ledger.jsonl", record)
    result = build_physical_quantum_qi_guarded_execution_intent(
        runtime_context=ctx(runtime),
        guarded_execution_intent_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_guarded_execution_intent_packet.json")
    return result.to_dict(), packet


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_READY", label
    assert out["intent_packet_written"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["guarded_execution_intent_only"] is True, label
    assert packet["boundary"]["execution_layer_entrypoint"] is True, label
    assert packet["boundary"]["no_dry_run_required"] is True, label
    assert packet["boundary"]["requires_guarded_execution_license"] is True, label
    assert packet["boundary"]["intent_not_world_mutation"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, packet = run(root, "ready", receipt("transition_candidate_envelope_ready"), lic())
        assert_ready("ready", out, packet)
        assert out["execution_intent_status"] == "guarded_execution_intent_ready"
        assert out["intent_count"] == 1
        assert packet["guarded_execution_intents"][0]["boundary"]["execution_layer_entrypoint"] is True
        assert packet["guarded_execution_intents"][0]["boundary"]["no_dry_run_required"] is True

        out, packet = run(root, "hold", receipt("transition_candidate_envelope_hold"), lic())
        assert_ready("hold", out, packet)
        assert out["execution_intent_status"] == "guarded_execution_intent_hold"
        assert out["intent_count"] == 0

        out, packet = run(root, "block", receipt("transition_candidate_envelope_block"), lic())
        assert_ready("block", out, packet)
        assert out["execution_intent_status"] == "guarded_execution_intent_block"
        assert out["intent_count"] == 0

        bad_env = receipt("transition_candidate_envelope_ready")
        bad_env["transition_candidate_envelopes"][0] = envelope(mismatch=True)
        out, packet = run(root, "mismatch", bad_env, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_BLOCKED"
        assert "transition_candidate_envelope_0_memory_kernel_digest_mismatch" in out["blockers"]
        assert packet == {}

        bad_boundary = receipt("transition_candidate_envelope_ready")
        bad_boundary["transition_candidate_envelopes"][0] = envelope(bad_boundary=True)
        out, packet = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_BLOCKED"
        assert "transition_candidate_envelope_0_boundary_does_not_authorize_execution_missing" in out["blockers"]
        assert packet == {}

        bad_weighting = receipt("transition_candidate_envelope_ready")
        bad_weighting["transition_candidate_envelopes"][0] = envelope(bad_weighting=True)
        out, packet = run(root, "bad_weighting", bad_weighting, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_BLOCKED"
        assert "execution_intent_envelope_0_with_probe_or_barrier" in out["blockers"]
        assert packet == {}

        bad_receipt = receipt("transition_candidate_envelope_ready")
        bad_receipt["boundary"]["does_not_start_next_cycle"] = False
        out, packet = run(root, "bad_receipt", bad_receipt, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_BLOCKED"
        assert "transition_candidate_envelope_receipt_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_BLOCKED"
        assert "transition_candidate_envelope_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "license_block", receipt("transition_candidate_envelope_ready"), lic(guarded_execution_intent_packet_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_BLOCKED"
        assert "guarded_execution_intent_packet_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_guarded_execution_intent_v12_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
