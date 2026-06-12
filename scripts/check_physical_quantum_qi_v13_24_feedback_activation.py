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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_6_to_v12_7_feedback_activation_v13_24 import (
    build_physical_quantum_qi_v12_6_to_v12_7_feedback_activation,
)

PT = {
    "process_tensor_digest": "pt-v13-24",
    "memory_kernel_digest": "memory-v13-24",
    "history_window_digest": "history-v13-24",
    "instrument_trace_digest": "instrument-v13-24",
    "non_markov_context_digest": "non-markov-v13-24",
}
BOUNDARY = {
    "guarded_transition_executor": True,
    "runtime_local_external_state_only": True,
    "license_gated_execution": True,
    "no_dry_run_required": True,
    "fail_closed_on_boundary_loss": True,
}


def write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def feedback_bridge_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_LICENSE_READY",
        "v12_6_execution_record_read_allowed": True,
        "v12_6_next_cycle_state_read_allowed": True,
        "v12_6_memory_consumption_ledger_read_allowed": True,
        "v12_6_external_state_mutation_ledger_read_allowed": True,
        "v12_7_feedback_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_FEEDBACK_ACTIVATION_LICENSE_READY",
        "v13_23_activation_record_read_allowed": True,
        "v12_6_execution_record_read_allowed": True,
        "v13_10_feedback_bridge_invoke_allowed": True,
        "activation_record_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "feedback_bridge_license": feedback_bridge_license(),
    }
    value.update(overrides)
    return value


def activation_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v12_6_to_v12_7_feedback_activation_enabled": True,
        "apply_physical_quantum_qi_v12_6_to_v12_7_feedback_activation": True,
        "runtime_root": str(root),
    }


def expected(kind: str) -> tuple[str, str, bool, bool, bool]:
    if kind == "executed":
        return (
            "guarded_transition_executed",
            "process_tensor_feedback_reinforce_next_cycle",
            True,
            True,
            True,
        )
    if kind == "hold":
        return (
            "guarded_transition_hold",
            "process_tensor_feedback_hold_context",
            False,
            False,
            False,
        )
    return (
        "guarded_transition_block",
        "process_tensor_feedback_block_context",
        False,
        False,
        False,
    )


def prepare(root: pathlib.Path, kind: str, *, omit_memory: bool = False) -> None:
    execution_status, _, next_seen, memory_seen, external_seen = expected(kind)
    digest = f"execution-record-{kind}"
    intent_count = 1 if kind == "executed" else 0
    write_json(
        root / "physical_quantum_qi_guarded_transition_execution_record.json",
        {
            "version": "physical_quantum_qi_guarded_transition_execution_record_v12_6",
            "execution_status": execution_status,
            "intent_count": intent_count,
            "effects": {
                "internal_transition_record": True,
                "next_cycle_state_update": next_seen,
                "memory_consumption": memory_seen,
                "external_state_mutation": external_seen,
            },
            "process_tensor_context": dict(PT),
            "source_guarded_execution_intent_receipt_digest": "intent-receipt-v13-24",
            "boundary": dict(BOUNDARY),
            "execution_record_digest": digest,
            "epoch": 1,
        },
    )
    write_json(
        root / "physical_quantum_qi_v13_23_executor_activation_record.json",
        {
            "version": "physical_quantum_qi_v13_23_executor_activation_record",
            "activation_status": "executor_activation_completed",
            "expected_execution_status": execution_status,
            "observed_execution_status": execution_status,
            "expected_effects": {
                "internal_transition_record": True,
                "next_cycle_state_update": next_seen,
                "memory_consumption": memory_seen,
                "external_state_mutation": external_seen,
            },
            "process_tensor_context": dict(PT),
            "source_v13_9_ready_state_digest": "ready-state-v13-24",
            "source_v12_5_receipt_digest": "intent-receipt-v13-24",
            "source_v12_6_execution_record_digest": digest,
            "activation_record_digest": f"activation-record-{kind}",
            "boundary": {
                "actual_executor_activation": True,
                "license_gated_execution": True,
                "no_dry_run_required": True,
                "runtime_local_external_state_only": True,
                "uses_process_tensor_feedback": True,
                "candidate_weighting_not_truth": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": 1,
        },
    )
    if next_seen:
        write_json(
            root / "physical_quantum_qi_next_cycle_state.json",
            {
                "next_cycle_started": True,
                "source_execution_record_digest": digest,
                "epoch": 1,
            },
        )
    if memory_seen and not omit_memory:
        append_jsonl(
            root / "physical_quantum_qi_memory_consumption_ledger.jsonl",
            {
                "memory_consumed": True,
                "source_execution_record_digest": digest,
                "epoch": 1,
            },
        )
    if external_seen:
        append_jsonl(
            root / "physical_quantum_qi_external_state_mutation_ledger.jsonl",
            {
                "external_state_mutated": True,
                "source_execution_record_digest": digest,
                "epoch": 1,
            },
        )


def run(root: pathlib.Path, license_packet: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v12_6_to_v12_7_feedback_activation(
        runtime_context=activation_context(root),
        v12_6_to_v12_7_feedback_activation_license=license_packet,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        for kind in ("executed", "hold", "block"):
            root = base / kind
            prepare(root, kind)
            result = run(root, activation_license())
            execution_status, feedback_status, next_seen, memory_seen, external_seen = expected(kind)
            assert result["status"] == "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_FEEDBACK_ACTIVATION_READY", (kind, result)
            assert result["execution_status"] == execution_status
            assert result["expected_feedback_status"] == feedback_status
            assert result["observed_feedback_status"] == feedback_status
            assert result["feedback_bridge_invoked"] is True
            assert result["feedback_ready_state_written"] is True
            assert result["feedback_bridge_ledger_appended"] is True
            ready_state = json.loads(
                (root / "physical_quantum_qi_v12_7_process_tensor_feedback_ready_state.json").read_text(encoding="utf-8")
            )
            assert ready_state["observed_effects"]["next_cycle_observed"] is next_seen
            assert ready_state["observed_effects"]["memory_feedback_observed"] is memory_seen
            assert ready_state["observed_effects"]["external_backaction_observed"] is external_seen

        root = base / "digest_mismatch"
        prepare(root, "executed")
        activation = json.loads(
            (root / "physical_quantum_qi_v13_23_executor_activation_record.json").read_text(encoding="utf-8")
        )
        activation["source_v12_6_execution_record_digest"] = "wrong-digest"
        write_json(root / "physical_quantum_qi_v13_23_executor_activation_record.json", activation)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["feedback_bridge_invoked"] is False
        assert "v13_23_activation_execution_record_digest_mismatch" in result["blockers"]

        root = base / "missing_effect"
        prepare(root, "executed", omit_memory=True)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["feedback_bridge_invoked"] is True
        assert "v13_10_feedback_bridge_not_ready" in result["blockers"]

        root = base / "license_block"
        prepare(root, "executed")
        result = run(root, activation_license(v13_10_feedback_bridge_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert result["feedback_bridge_invoked"] is False
        assert "v13_10_feedback_bridge_invoke_not_allowed" in result["blockers"]

    print("physical_quantum_qi_v13_24_feedback_activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
