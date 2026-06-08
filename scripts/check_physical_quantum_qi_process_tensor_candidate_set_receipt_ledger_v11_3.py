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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_process_tensor_candidate_set_receipt_ledger_v11_3 import build_physical_quantum_qi_process_tensor_candidate_set_receipt_ledger

CANDIDATE_SET_BOUNDARY = {
    "candidate_set_build_only": True,
    "history_bearing_process_tensor": True,
    "non_markov_context_required": True,
    "multi_time_window_required": True,
    "finite_horizon_only": True,
    "does_not_execute_path": True,
    "does_not_run_runner": True,
    "does_not_start_next_cycle": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_authorize_execution": True,
    "does_not_select_final_path": True,
    "does_not_promote_truth": True,
    "candidate_weighting_not_truth": True,
    "admissible_set_not_execution_set": True,
    "fail_closed_on_boundary_loss": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v11-3",
    "memory_kernel_digest": "memory-kernel-digest-v11-3",
    "history_window_digest": "history-window-digest-v11-3",
    "instrument_trace_digest": "instrument-trace-digest-v11-3",
    "non_markov_context_digest": "non-markov-context-digest-v11-3",
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
        "physical_quantum_qi_process_tensor_candidate_set_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_process_tensor_candidate_set_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_CANDIDATE_SET_RECEIPT_LEDGER_LICENSE_READY",
        "candidate_set_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def candidate(kind: str, idx: int) -> dict[str, Any]:
    decision = {"admitted": "admit_candidate", "probe": "hold_candidate", "blocked": "block_candidate"}[kind]
    status = {"admitted": "weighted_candidate", "probe": "probe_only_candidate", "blocked": "blocked_candidate"}[kind]
    weighting = {
        "admitted": {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "probe": {"path_weight_delta": 0, "probe_potential_required": True, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "blocked": {"path_weight_delta": 0, "probe_potential_required": False, "barrier_potential_required": True, "barrier_blocks_ready_weight": True},
    }[kind]
    return {
        "candidate_id": f"candidate-{kind}-{idx}",
        "gate_receipt_digest": f"gate-receipt-{kind}-{idx}",
        "cycle_gate_decision": decision,
        "source_candidate_status": status,
        "candidate_weighting": weighting,
        "process_tensor_context": dict(PT),
    }


def candidate_set(*, admitted: int = 1, probe: int = 1, blocked: int = 1) -> dict[str, Any]:
    packet = {
        "version": "physical_quantum_qi_process_tensor_admissible_candidate_set_v11_2",
        "physical_quantum_qi_process_tensor_candidate_set_considered": True,
        "admitted_candidates": [candidate("admitted", i) for i in range(admitted)],
        "probe_candidates": [candidate("probe", i) for i in range(probe)],
        "blocked_candidates": [candidate("blocked", i) for i in range(blocked)],
        "counts": {"admitted": admitted, "probe": probe, "blocked": blocked},
        "process_tensor_context": dict(PT),
        "boundary": dict(CANDIDATE_SET_BOUNDARY),
        "epoch": 1,
    }
    packet["candidate_set_digest"] = "candidate-set-digest-v11-3"
    return packet


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "physical_quantum_qi_process_tensor_admissible_candidate_set.json", packet)
    result = build_physical_quantum_qi_process_tensor_candidate_set_receipt_ledger(
        runtime_context=ctx(runtime),
        process_tensor_candidate_set_receipt_ledger_license=license_packet,
    )
    ledger = read_jsonl(runtime / "physical_quantum_qi_process_tensor_candidate_set_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_CANDIDATE_SET_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    assert ledger[-1]["boundary"]["receipt_ledger_only"] is True, label
    assert ledger[-1]["boundary"]["process_tensor_candidate_set_receipt_only"] is True, label
    assert ledger[-1]["boundary"]["history_bearing_process_tensor"] is True, label
    assert ledger[-1]["boundary"]["non_markov_context_required"] is True, label
    assert ledger[-1]["boundary"]["does_not_start_next_cycle"] is True, label
    assert ledger[-1]["boundary"]["does_not_authorize_execution"] is True, label
    assert ledger[-1]["boundary"]["admissible_set_not_execution_set"] is True, label
    assert ledger[-1]["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, ledger = run(root, "mixed", candidate_set(admitted=1, probe=1, blocked=1), lic())
        assert_ready("mixed", out, ledger)
        assert out["admitted_count"] == 1 and out["probe_count"] == 1 and out["blocked_count"] == 1
        assert ledger[-1]["process_tensor_context"]["memory_kernel_digest"] == "memory-kernel-digest-v11-3"

        out, ledger = run(root, "admit_only", candidate_set(admitted=2, probe=0, blocked=0), lic())
        assert_ready("admit_only", out, ledger)
        assert out["admitted_count"] == 2 and out["probe_count"] == 0 and out["blocked_count"] == 0

        out, ledger = run(root, "chain", candidate_set(admitted=1, probe=0, blocked=0), lic())
        assert_ready("chain_1", out, ledger)
        out, ledger = run(root, "chain", candidate_set(admitted=0, probe=1, blocked=0), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        bad_count = candidate_set(admitted=1, probe=0, blocked=0)
        bad_count["counts"]["admitted"] = 2
        out, ledger = run(root, "bad_count", bad_count, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_CANDIDATE_SET_RECEIPT_LEDGER_BLOCKED"
        assert "admitted_count_mismatch" in out["blockers"]
        assert ledger == []

        missing_memory = candidate_set(admitted=1, probe=0, blocked=0)
        missing_memory["process_tensor_context"].pop("memory_kernel_digest")
        out, ledger = run(root, "missing_memory", missing_memory, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_CANDIDATE_SET_RECEIPT_LEDGER_BLOCKED"
        assert "process_tensor_context_memory_kernel_digest_missing" in out["blockers"]
        assert ledger == []

        bad_boundary = candidate_set(admitted=1, probe=0, blocked=0)
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, ledger = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_CANDIDATE_SET_RECEIPT_LEDGER_BLOCKED"
        assert "candidate_set_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_CANDIDATE_SET_RECEIPT_LEDGER_BLOCKED"
        assert "process_tensor_admissible_candidate_set_missing_or_invalid" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "license_block", candidate_set(admitted=1, probe=0, blocked=0), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_CANDIDATE_SET_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_process_tensor_candidate_set_receipt_ledger_v11_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
