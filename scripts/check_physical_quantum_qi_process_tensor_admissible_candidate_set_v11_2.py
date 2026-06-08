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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_process_tensor_admissible_candidate_set_v11_2 import build_physical_quantum_qi_process_tensor_admissible_candidate_set

GATE_RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "cycle_gate_receipt_only": True,
    "does_not_execute_path": True,
    "does_not_run_runner": True,
    "does_not_start_next_cycle": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_authorize_execution": True,
    "candidate_weighting_not_truth": True,
    "receipt_does_not_mutate_gate_packet": True,
    "receipt_does_not_select_final_path": True,
    "receipt_does_not_promote_truth": True,
    "replayable_receipt": True,
    "fail_closed_on_boundary_loss": True,
}
PROCESS_TENSOR_BOUNDARY = {
    "history_bearing_process_tensor": True,
    "non_markov_context_required": True,
    "multi_time_window_required": True,
    "finite_horizon_only": True,
    "memory_kernel_visible": True,
    "does_not_execute_path": True,
    "does_not_run_runner": True,
    "does_not_start_next_cycle": True,
    "does_not_authorize_execution": True,
    "candidate_set_build_only": True,
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


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_process_tensor_admissible_candidate_set_enabled": True,
        "apply_physical_quantum_qi_process_tensor_admissible_candidate_set": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_ADMISSIBLE_CANDIDATE_SET_LICENSE_READY",
        "gate_receipt_ledger_read_allowed": True,
        "process_tensor_context_read_allowed": True,
        "candidate_set_write_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def process_tensor_context(*, markov_only: bool = False, missing_memory: bool = False) -> dict[str, Any]:
    payload = {
        "process_tensor_context_considered": True,
        "qi_process_tensor_mode": "history_bearing_non_markov",
        "history_window": ["t-2", "t-1", "t0"],
        "instrument_trace": ["observe", "gate", "candidate-set"],
        "process_tensor_digest": "pt-digest-v11-2",
        "memory_kernel_digest": "memory-kernel-digest-v11-2",
        "non_markov_context_digest": "non-markov-context-digest-v11-2",
        "markov_only_context": markov_only,
        "boundary": dict(PROCESS_TENSOR_BOUNDARY),
    }
    if missing_memory:
        payload.pop("memory_kernel_digest")
    return payload


def gate_receipt(decision: str) -> dict[str, Any]:
    status = {
        "admit_candidate": "weighted_candidate",
        "hold_candidate": "probe_only_candidate",
        "block_candidate": "blocked_candidate",
    }[decision]
    weighting = {
        "admit_candidate": {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "hold_candidate": {"path_weight_delta": 0, "probe_potential_required": True, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "block_candidate": {"path_weight_delta": 0, "probe_potential_required": False, "barrier_potential_required": True, "barrier_blocks_ready_weight": True},
    }[decision]
    return {
        "version": "physical_quantum_qi_next_cycle_gate_receipt_record_v11_1",
        "record_type": "physical_quantum_qi_next_cycle_gate_receipt",
        "cycle_gate_decision": decision,
        "source_candidate_status": status,
        "candidate_weighting": weighting,
        "source_cycle_gate_packet_digest": f"source-{decision}",
        "prev_record_digest": "GENESIS",
        "record_digest": f"digest-{decision}",
        "boundary": dict(GATE_RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def prepare(root: pathlib.Path, name: str, records: list[dict[str, Any]], pt: dict[str, Any] | None) -> pathlib.Path:
    runtime = root / name
    for record in records:
        append_jsonl(runtime / "physical_quantum_qi_next_cycle_gate_receipt_ledger.jsonl", record)
    if pt is not None:
        dump(runtime / "physical_quantum_qi_process_tensor_candidate_context.json", pt)
    return runtime


def run_case(root: pathlib.Path, name: str, records: list[dict[str, Any]], pt: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    runtime = prepare(root, name, records, pt)
    result = build_physical_quantum_qi_process_tensor_admissible_candidate_set(
        runtime_context=ctx(runtime),
        process_tensor_admissible_candidate_set_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_process_tensor_admissible_candidate_set.json")
    return result.to_dict(), packet


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_ADMISSIBLE_CANDIDATE_SET_READY", label
    assert out["candidate_set_written"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["candidate_set_build_only"] is True, label
    assert packet["boundary"]["history_bearing_process_tensor"] is True, label
    assert packet["boundary"]["non_markov_context_required"] is True, label
    assert packet["boundary"]["does_not_start_next_cycle"] is True, label
    assert packet["boundary"]["does_not_authorize_execution"] is True, label
    assert packet["boundary"]["admissible_set_not_execution_set"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, packet = run_case(
            root,
            "mixed",
            [gate_receipt("admit_candidate"), gate_receipt("hold_candidate"), gate_receipt("block_candidate")],
            process_tensor_context(),
            lic(),
        )
        assert_ready("mixed", out, packet)
        assert out["admitted_count"] == 1
        assert out["probe_count"] == 1
        assert out["blocked_count"] == 1
        assert packet["admitted_candidates"][0]["process_tensor_context"]["process_tensor_digest"] == "pt-digest-v11-2"

        out, packet = run_case(root, "admit_only", [gate_receipt("admit_candidate")], process_tensor_context(), lic())
        assert_ready("admit_only", out, packet)
        assert packet["counts"] == {"admitted": 1, "probe": 0, "blocked": 0}

        out, packet = run_case(root, "markov_only", [gate_receipt("admit_candidate")], process_tensor_context(markov_only=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_ADMISSIBLE_CANDIDATE_SET_BLOCKED"
        assert "markov_only_context_forbidden" in out["blockers"]
        assert packet == {}

        out, packet = run_case(root, "missing_memory", [gate_receipt("admit_candidate")], process_tensor_context(missing_memory=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_ADMISSIBLE_CANDIDATE_SET_BLOCKED"
        assert "memory_kernel_digest_missing" in out["blockers"]
        assert packet == {}

        bad_receipt = gate_receipt("admit_candidate")
        bad_receipt["boundary"]["does_not_start_next_cycle"] = False
        out, packet = run_case(root, "bad_receipt", [bad_receipt], process_tensor_context(), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_ADMISSIBLE_CANDIDATE_SET_BLOCKED"
        assert "gate_receipt_0_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert packet == {}

        out, packet = run_case(root, "missing_pt", [gate_receipt("admit_candidate")], None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_ADMISSIBLE_CANDIDATE_SET_BLOCKED"
        assert "process_tensor_context_missing_or_invalid" in out["blockers"]
        assert packet == {}

        out, packet = run_case(root, "license_block", [gate_receipt("admit_candidate")], process_tensor_context(), lic(candidate_set_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_ADMISSIBLE_CANDIDATE_SET_BLOCKED"
        assert "candidate_set_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_process_tensor_admissible_candidate_set_v11_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
