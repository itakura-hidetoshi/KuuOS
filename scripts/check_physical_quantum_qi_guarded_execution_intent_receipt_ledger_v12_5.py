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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_guarded_execution_intent_receipt_ledger_v12_5 import build_physical_quantum_qi_guarded_execution_intent_receipt_ledger

PACKET_BOUNDARY = {
    "guarded_execution_intent_only": True,
    "execution_layer_entrypoint": True,
    "no_dry_run_required": True,
    "transition_candidate_envelope_required": True,
    "history_bearing_process_tensor": True,
    "non_markov_context_required": True,
    "multi_time_window_required": True,
    "finite_horizon_only": True,
    "memory_kernel_visible": True,
    "requires_guarded_execution_license": True,
    "intent_not_world_mutation": True,
    "does_not_start_next_cycle": True,
    "does_not_mutate_external_state": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_promote_truth": True,
    "candidate_weighting_not_truth": True,
    "fail_closed_on_boundary_loss": True,
}
INTENT_BOUNDARY = {
    "guarded_execution_intent_only": True,
    "execution_layer_entrypoint": True,
    "no_dry_run_required": True,
    "requires_guarded_execution_license": True,
    "intent_not_world_mutation": True,
    "does_not_start_next_cycle": True,
    "does_not_mutate_external_state": True,
    "does_not_consume_memory": True,
    "does_not_promote_truth": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v12-5",
    "memory_kernel_digest": "memory-kernel-digest-v12-5",
    "history_window_digest": "history-window-digest-v12-5",
    "instrument_trace_digest": "instrument-trace-digest-v12-5",
    "non_markov_context_digest": "non-markov-context-digest-v12-5",
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
        "physical_quantum_qi_guarded_execution_intent_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_guarded_execution_intent_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_LICENSE_READY",
        "guarded_execution_intent_packet_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def intent(*, mismatch: bool = False, bad_boundary: bool = False, bad_weighting: bool = False) -> dict[str, Any]:
    boundary = dict(INTENT_BOUNDARY)
    if bad_boundary:
        boundary["does_not_mutate_external_state"] = False
    context = dict(PT)
    if mismatch:
        context["instrument_trace_digest"] = "mismatch"
    weighting = {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False}
    if bad_weighting:
        weighting["probe_potential_required"] = True
    return {
        "intent_type": "physical_quantum_qi_guarded_execution_intent",
        "intent_index": 0,
        "candidate_id": "candidate-admit-0",
        "transition_precheck_decision": "transition_precheck_admit_candidate",
        "corridor_stability_gate_decision": "corridor_stability_admit",
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_transition_candidate_envelope_digest": "transition-candidate-envelope-digest-v12-5",
        "guarded_execution_intent_digest": "guarded-execution-intent-digest-v12-5",
        "boundary": boundary,
    }


def packet(status: str) -> dict[str, Any]:
    envelope_status = {
        "guarded_execution_intent_ready": "transition_candidate_envelope_ready",
        "guarded_execution_intent_hold": "transition_candidate_envelope_hold",
        "guarded_execution_intent_block": "transition_candidate_envelope_block",
    }[status]
    precheck = {
        "guarded_execution_intent_ready": "transition_precheck_admit_candidate",
        "guarded_execution_intent_hold": "transition_precheck_hold_candidate",
        "guarded_execution_intent_block": "transition_precheck_block_candidate",
    }[status]
    intents = [intent()] if status == "guarded_execution_intent_ready" else []
    pkt = {
        "version": "physical_quantum_qi_guarded_execution_intent_packet_v12_4",
        "physical_quantum_qi_guarded_execution_intent_considered": True,
        "execution_intent_status": status,
        "envelope_status": envelope_status,
        "transition_precheck_decision": precheck,
        "intent_count": len(intents),
        "envelope_count": 1 if status == "guarded_execution_intent_ready" else 0,
        "guarded_execution_intents": intents,
        "transition_candidate_envelopes": [],
        "process_tensor_context": dict(PT),
        "source_digests": {
            "transition_candidate_envelope_receipt": "transition-candidate-envelope-receipt-digest-v12-5",
            "transition_candidate_envelope_packet": "transition-candidate-envelope-packet-digest-v12-5",
            "stable_corridor_transition_precheck_receipt": "transition-precheck-receipt-digest-v12-5",
        },
        "boundary": dict(PACKET_BOUNDARY),
        "epoch": 1,
    }
    pkt["guarded_execution_intent_packet_digest"] = f"guarded-execution-intent-packet-digest-{status}"
    return pkt


def run(root: pathlib.Path, name: str, pkt: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if pkt is not None:
        dump(runtime / "physical_quantum_qi_guarded_execution_intent_packet.json", pkt)
    result = build_physical_quantum_qi_guarded_execution_intent_receipt_ledger(
        runtime_context=ctx(runtime),
        guarded_execution_intent_receipt_ledger_license=license_packet,
    )
    ledger = read_jsonl(runtime / "physical_quantum_qi_guarded_execution_intent_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    latest = ledger[-1]
    assert latest["boundary"]["receipt_ledger_only"] is True, label
    assert latest["boundary"]["guarded_execution_intent_receipt_only"] is True, label
    assert latest["boundary"]["execution_layer_entrypoint"] is True, label
    assert latest["boundary"]["no_dry_run_required"] is True, label
    assert latest["boundary"]["does_not_mutate_external_state"] is True, label
    assert latest["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, ledger = run(root, "ready", packet("guarded_execution_intent_ready"), lic())
        assert_ready("ready", out, ledger)
        assert out["execution_intent_status"] == "guarded_execution_intent_ready"
        assert out["intent_count"] == 1
        assert ledger[-1]["guarded_execution_intents"][0]["intent_type"] == "physical_quantum_qi_guarded_execution_intent"

        out, ledger = run(root, "hold", packet("guarded_execution_intent_hold"), lic())
        assert_ready("hold", out, ledger)
        assert out["execution_intent_status"] == "guarded_execution_intent_hold"
        assert out["intent_count"] == 0

        out, ledger = run(root, "block", packet("guarded_execution_intent_block"), lic())
        assert_ready("block", out, ledger)
        assert out["execution_intent_status"] == "guarded_execution_intent_block"
        assert out["intent_count"] == 0

        out, ledger = run(root, "chain", packet("guarded_execution_intent_ready"), lic())
        assert_ready("chain_1", out, ledger)
        out, ledger = run(root, "chain", packet("guarded_execution_intent_hold"), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        bad_packet = packet("guarded_execution_intent_ready")
        bad_packet["guarded_execution_intents"][0] = intent(mismatch=True)
        out, ledger = run(root, "mismatch", bad_packet, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_BLOCKED"
        assert "guarded_execution_intent_0_instrument_trace_digest_mismatch" in out["blockers"]
        assert ledger == []

        bad_boundary = packet("guarded_execution_intent_ready")
        bad_boundary["guarded_execution_intents"][0] = intent(bad_boundary=True)
        out, ledger = run(root, "bad_intent_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_BLOCKED"
        assert "guarded_execution_intent_0_boundary_does_not_mutate_external_state_missing" in out["blockers"]
        assert ledger == []

        bad_weight = packet("guarded_execution_intent_ready")
        bad_weight["guarded_execution_intents"][0] = intent(bad_weighting=True)
        out, ledger = run(root, "bad_weight", bad_weight, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_BLOCKED"
        assert "guarded_execution_intent_0_with_probe_or_barrier" in out["blockers"]
        assert ledger == []

        bad_packet_boundary = packet("guarded_execution_intent_ready")
        bad_packet_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, ledger = run(root, "bad_packet_boundary", bad_packet_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_BLOCKED"
        assert "guarded_execution_intent_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_BLOCKED"
        assert "guarded_execution_intent_packet_missing_or_invalid" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "license_block", packet("guarded_execution_intent_ready"), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_guarded_execution_intent_receipt_ledger_v12_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
