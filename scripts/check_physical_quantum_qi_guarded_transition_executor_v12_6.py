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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_guarded_transition_executor_v12_6 import build_physical_quantum_qi_guarded_transition_executor

RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "guarded_execution_intent_receipt_only": True,
    "execution_layer_entrypoint": True,
    "no_dry_run_required": True,
    "requires_guarded_execution_license": True,
    "intent_not_world_mutation": True,
    "does_not_start_next_cycle": True,
    "does_not_mutate_external_state": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_promote_truth": True,
    "receipt_does_not_mutate_intent_packet": True,
    "replayable_receipt": True,
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
    "process_tensor_digest": "pt-digest-v12-6",
    "memory_kernel_digest": "memory-kernel-digest-v12-6",
    "history_window_digest": "history-window-digest-v12-6",
    "instrument_trace_digest": "instrument-trace-digest-v12-6",
    "non_markov_context_digest": "non-markov-context-digest-v12-6",
}


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


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_guarded_transition_executor_enabled": True,
        "apply_physical_quantum_qi_guarded_transition_executor": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_LICENSE_READY",
        "guarded_execution_intent_receipt_ledger_read_allowed": True,
        "internal_transition_record_write_allowed": True,
        "next_cycle_state_write_allowed": True,
        "memory_consumption_append_allowed": True,
        "external_state_mutation_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def intent(*, mismatch: bool = False, bad_boundary: bool = False, bad_weighting: bool = False) -> dict[str, Any]:
    boundary = dict(INTENT_BOUNDARY)
    if bad_boundary:
        boundary["requires_guarded_execution_license"] = False
    context = dict(PT)
    if mismatch:
        context["non_markov_context_digest"] = "mismatch"
    weighting = {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False}
    if bad_weighting:
        weighting["barrier_blocks_ready_weight"] = True
    return {
        "intent_index": 0,
        "intent_type": "physical_quantum_qi_guarded_execution_intent",
        "candidate_id": "candidate-admit-0",
        "transition_precheck_decision": "transition_precheck_admit_candidate",
        "corridor_stability_gate_decision": "corridor_stability_admit",
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_transition_candidate_envelope_digest": "transition-envelope-digest-v12-6",
        "guarded_execution_intent_digest": "guarded-intent-digest-v12-6",
        "boundary": boundary,
    }


def receipt(status: str) -> dict[str, Any]:
    intents = [intent()] if status == "guarded_execution_intent_ready" else []
    return {
        "version": "physical_quantum_qi_guarded_execution_intent_receipt_record_v12_5",
        "record_type": "physical_quantum_qi_guarded_execution_intent_receipt",
        "execution_intent_status": status,
        "intent_count": len(intents),
        "guarded_execution_intents": intents,
        "process_tensor_context": dict(PT),
        "source_guarded_execution_intent_packet_digest": "guarded-intent-packet-digest-v12-6",
        "prev_record_digest": "GENESIS",
        "record_digest": f"guarded-intent-receipt-{status}",
        "boundary": dict(RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, rec: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], pathlib.Path]:
    runtime = root / name
    if rec is not None:
        append_jsonl(runtime / "physical_quantum_qi_guarded_execution_intent_receipt_ledger.jsonl", rec)
    result = build_physical_quantum_qi_guarded_transition_executor(
        runtime_context=ctx(runtime),
        guarded_transition_executor_license=license_packet,
    )
    return result.to_dict(), runtime


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, runtime = run(root, "ready", receipt("guarded_execution_intent_ready"), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_READY"
        assert out["execution_status"] == "guarded_transition_executed"
        assert out["internal_transition_record_written"] is True
        assert out["next_cycle_state_updated"] is True
        assert out["memory_consumption_appended"] is True
        assert out["external_state_mutation_appended"] is True
        record = load_json(runtime / "physical_quantum_qi_guarded_transition_execution_record.json")
        assert record["boundary"]["can_update_next_cycle_state"] is True
        assert load_json(runtime / "physical_quantum_qi_next_cycle_state.json")["next_cycle_started"] is True
        assert load_jsonl(runtime / "physical_quantum_qi_memory_consumption_ledger.jsonl")[-1]["memory_consumed"] is True
        assert load_jsonl(runtime / "physical_quantum_qi_external_state_mutation_ledger.jsonl")[-1]["external_state_mutated"] is True

        out, runtime = run(root, "hold", receipt("guarded_execution_intent_hold"), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_READY"
        assert out["execution_status"] == "guarded_transition_hold"
        assert out["internal_transition_record_written"] is True
        assert out["next_cycle_state_updated"] is False
        assert not (runtime / "physical_quantum_qi_next_cycle_state.json").exists()

        out, runtime = run(root, "block", receipt("guarded_execution_intent_block"), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_READY"
        assert out["execution_status"] == "guarded_transition_block"
        assert out["external_state_mutation_appended"] is False

        bad = receipt("guarded_execution_intent_ready")
        bad["guarded_execution_intents"][0] = intent(mismatch=True)
        out, runtime = run(root, "mismatch", bad, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_BLOCKED"
        assert "guarded_transition_executor_intent_0_non_markov_context_digest_mismatch" in out["blockers"]
        assert not (runtime / "physical_quantum_qi_guarded_transition_execution_record.json").exists()

        bad = receipt("guarded_execution_intent_ready")
        bad["guarded_execution_intents"][0] = intent(bad_boundary=True)
        out, runtime = run(root, "bad_boundary", bad, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_BLOCKED"
        assert "guarded_transition_executor_intent_0_boundary_requires_guarded_execution_license_missing" in out["blockers"]

        bad = receipt("guarded_execution_intent_ready")
        bad["guarded_execution_intents"][0] = intent(bad_weighting=True)
        out, runtime = run(root, "bad_weight", bad, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_BLOCKED"
        assert "guarded_transition_executor_intent_0_with_probe_or_barrier" in out["blockers"]

        bad_receipt = receipt("guarded_execution_intent_ready")
        bad_receipt["boundary"]["does_not_start_next_cycle"] = False
        out, runtime = run(root, "bad_receipt", bad_receipt, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_BLOCKED"
        assert "guarded_execution_intent_receipt_boundary_does_not_start_next_cycle_missing" in out["blockers"]

        out, runtime = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_BLOCKED"
        assert "guarded_execution_intent_receipt_ledger_missing" in out["blockers"]

        out, runtime = run(root, "license_block", receipt("guarded_execution_intent_ready"), lic(external_state_mutation_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_BLOCKED"
        assert "external_state_mutation_append_not_allowed" in out["blockers"]

    print("physical_quantum_qi_guarded_transition_executor_v12_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
