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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_25_feedback_receipt_activation import (
    build_physical_quantum_qi_v13_25_feedback_receipt_activation,
)

PT = {
    "process_tensor_digest": "pt-v13-25",
    "memory_kernel_digest": "memory-v13-25",
    "history_window_digest": "history-v13-25",
    "instrument_trace_digest": "instrument-v13-25",
    "non_markov_context_digest": "non-markov-v13-25",
}
EXECUTION_BOUNDARY = {
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


def feedback_status(kind: str) -> tuple[str, str]:
    if kind == "executed":
        return "guarded_transition_executed", "process_tensor_feedback_reinforce_next_cycle"
    if kind == "hold":
        return "guarded_transition_hold", "process_tensor_feedback_hold_context"
    return "guarded_transition_block", "process_tensor_feedback_block_context"


def observed_effects(kind: str) -> dict[str, bool]:
    enabled = kind == "executed"
    return {
        "next_cycle_observed": enabled,
        "memory_feedback_observed": enabled,
        "external_backaction_observed": enabled,
    }


def feedback_kernel(kind: str) -> dict[str, Any]:
    _, status = feedback_status(kind)
    if kind == "executed":
        return {
            "feedback_status": status,
            "path_weight_delta": 1,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if kind == "hold":
        return {
            "feedback_status": status,
            "path_weight_delta": 0,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return {
        "feedback_status": status,
        "path_weight_delta": -1,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def prepare(root: pathlib.Path, kind: str, *, omit_memory: bool = False, bad_ready_digest: bool = False) -> None:
    execution_status, expected_feedback = feedback_status(kind)
    effect = kind == "executed"
    execution_digest = f"execution-v13-25-{kind}"
    ready_digest = f"ready-v13-25-{kind}"

    write_json(
        root / "physical_quantum_qi_guarded_transition_execution_record.json",
        {
            "version": "physical_quantum_qi_guarded_transition_execution_record_v12_6",
            "execution_status": execution_status,
            "intent_count": 1 if effect else 0,
            "effects": {
                "internal_transition_record": True,
                "next_cycle_state_update": effect,
                "memory_consumption": effect,
                "external_state_mutation": effect,
            },
            "process_tensor_context": dict(PT),
            "source_guarded_execution_intent_receipt_digest": "intent-receipt-v13-25",
            "boundary": dict(EXECUTION_BOUNDARY),
            "execution_record_digest": execution_digest,
            "epoch": 1,
        },
    )

    if effect:
        write_json(
            root / "physical_quantum_qi_next_cycle_state.json",
            {
                "next_cycle_started": True,
                "source_execution_record_digest": execution_digest,
                "next_cycle_state_digest": "next-cycle-v13-25",
                "epoch": 1,
            },
        )
        if not omit_memory:
            append_jsonl(
                root / "physical_quantum_qi_memory_consumption_ledger.jsonl",
                {
                    "memory_consumed": True,
                    "source_execution_record_digest": execution_digest,
                    "memory_consumption_digest": "memory-consumption-v13-25",
                    "epoch": 1,
                },
            )
        append_jsonl(
            root / "physical_quantum_qi_external_state_mutation_ledger.jsonl",
            {
                "external_state_mutated": True,
                "source_execution_record_digest": execution_digest,
                "external_state_mutation_digest": "external-mutation-v13-25",
                "epoch": 1,
            },
        )

    write_json(
        root / "physical_quantum_qi_v12_7_process_tensor_feedback_ready_state.json",
        {
            "version": "physical_quantum_qi_v12_7_process_tensor_feedback_ready_state_v13_10",
            "process_tensor_feedback_ready_state": True,
            "bridge_status": "v12_6_to_v12_7_process_tensor_feedback_bridge_" + expected_feedback.rsplit("_", 1)[-1],
            "execution_status": execution_status,
            "expected_v12_7_feedback_status": expected_feedback,
            "observed_effects": observed_effects(kind),
            "expected_feedback_kernel": feedback_kernel(kind),
            "source_execution_record_digest": execution_digest,
            "source_guarded_execution_intent_receipt_digest": "intent-receipt-v13-25",
            "process_tensor_context": dict(PT),
            "boundary": {
                "v12_7_process_tensor_feedback_ready_state_only": True,
                "v12_6_guarded_transition_execution_record_required": True,
                "can_feed_v12_7_process_tensor_execution_feedback": True,
                "uses_execution_effects_as_non_markov_feedback": True,
                "history_window_feedback_required": True,
                "memory_kernel_feedback_required": True,
                "external_backaction_visible": True,
                "feedback_not_direct_truth": True,
                "bridge_not_direct_feedback_append": True,
                "does_not_run_feedback_runtime": True,
                "fail_closed_on_boundary_loss": True,
            },
            "process_tensor_feedback_ready_state_digest": ready_digest,
            "epoch": 1,
        },
    )

    write_json(
        root / "physical_quantum_qi_v13_24_feedback_activation_record.json",
        {
            "version": "physical_quantum_qi_v13_24_feedback_activation_record",
            "activation_status": "feedback_activation_completed",
            "execution_status": execution_status,
            "expected_feedback_status": expected_feedback,
            "observed_feedback_status": expected_feedback,
            "source_v13_23_activation_record_digest": "activation-v13-23",
            "source_v12_6_execution_record_digest": execution_digest,
            "source_v13_10_feedback_ready_state_digest": "wrong-ready" if bad_ready_digest else ready_digest,
            "feedback_activation_record_digest": f"activation-v13-24-{kind}",
            "boundary": {
                "post_execution_feedback_activation": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "license_gated_feedback_activation": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": 1,
        },
    )


def v12_7_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_LICENSE_READY",
        "guarded_transition_execution_record_read_allowed": True,
        "next_cycle_state_read_allowed": True,
        "memory_consumption_ledger_read_allowed": True,
        "external_state_mutation_ledger_read_allowed": True,
        "process_tensor_feedback_append_allowed": True,
        "path_integral_feedback_state_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def v13_11_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_LICENSE_READY",
        "v12_7_process_tensor_feedback_packet_read_allowed": True,
        "v12_7_path_integral_feedback_state_read_allowed": True,
        "v12_8_feedback_receipt_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_25_FEEDBACK_RECEIPT_ACTIVATION_LICENSE_READY",
        "v13_24_activation_record_read_allowed": True,
        "v13_10_feedback_ready_state_read_allowed": True,
        "v12_7_feedback_runtime_invoke_allowed": True,
        "v13_11_receipt_bridge_invoke_allowed": True,
        "activation_record_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v12_7_feedback_license": v12_7_license(),
        "v13_11_receipt_bridge_license": v13_11_license(),
    }
    value.update(overrides)
    return value


def activation_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_25_feedback_receipt_activation_enabled": True,
        "apply_physical_quantum_qi_v13_25_feedback_receipt_activation": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_packet: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_25_feedback_receipt_activation(
        runtime_context=activation_context(root),
        v13_25_feedback_receipt_activation_license=license_packet,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        expected_reentry = {
            "executed": ("process_tensor_feedback_reinforce_next_cycle", "reentry_weighting_reinforce", "reinforce_path_weight"),
            "hold": ("process_tensor_feedback_hold_context", "reentry_weighting_hold", "open_probe_potential"),
            "block": ("process_tensor_feedback_block_context", "reentry_weighting_block", "add_barrier_potential"),
        }

        for kind, (feedback, reentry_status, action) in expected_reentry.items():
            root = base / kind
            prepare(root, kind)
            result = run(root, activation_license())
            assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_25_FEEDBACK_RECEIPT_ACTIVATION_READY", (kind, result)
            assert result["observed_feedback_status"] == feedback
            assert result["v12_7_feedback_invoked"] is True
            assert result["v13_11_receipt_bridge_invoked"] is True
            assert result["feedback_packet_written"] is True
            assert result["path_integral_feedback_state_written"] is True
            assert result["feedback_receipt_ready_state_written"] is True
            ready = json.loads(
                (root / "physical_quantum_qi_v12_8_process_tensor_feedback_receipt_ready_state.json").read_text(encoding="utf-8")
            )
            assert ready["expected_v12_9_reentry_weighting_status"] == reentry_status
            assert ready["expected_v12_9_reentry_weighting_action"] == action

        root = base / "digest_mismatch"
        prepare(root, "executed", bad_ready_digest=True)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v12_7_feedback_invoked"] is False
        assert "v13_24_feedback_ready_state_digest_mismatch" in result["blockers"]

        root = base / "missing_effect"
        prepare(root, "executed", omit_memory=True)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v12_7_feedback_invoked"] is True
        assert result["v13_11_receipt_bridge_invoked"] is False
        assert "v12_7_feedback_runtime_not_ready" in result["blockers"]

        root = base / "license_block"
        prepare(root, "executed")
        result = run(root, activation_license(v13_11_receipt_bridge_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert result["v12_7_feedback_invoked"] is False
        assert result["v13_11_receipt_bridge_invoked"] is False
        assert "v13_11_receipt_bridge_invoke_not_allowed" in result["blockers"]

    print("physical_quantum_qi_v13_25_feedback_receipt_activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
