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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_path_integral_reentry_intake_receipt_ledger_v10_7 import build_physical_quantum_qi_path_integral_reentry_intake_receipt_ledger

BOUNDARY = {
    "reentry_intake_validation_only": True,
    "does_not_execute_path": True,
    "does_not_run_runner": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_authorize_execution": True,
    "candidate_weighting_not_truth": True,
    "barrier_potential_can_only_block_or_probe": True,
    "fail_closed_on_boundary_loss": True,
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
        "physical_quantum_qi_path_integral_reentry_intake_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_path_integral_reentry_intake_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_RECEIPT_LEDGER_LICENSE_READY",
        "reentry_intake_packet_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def packet(decision: str, *, warnings: list[str] | None = None) -> dict[str, Any]:
    counts = {
        "accept": {"reinforce_path_weight": 3, "open_probe_potential": 0, "add_barrier_potential": 0},
        "hold": {"reinforce_path_weight": 2, "open_probe_potential": 1, "add_barrier_potential": 0},
        "block": {"reinforce_path_weight": 2, "open_probe_potential": 0, "add_barrier_potential": 1},
    }[decision]
    return {
        "version": "physical_quantum_qi_path_integral_reentry_intake_decision_packet_v10_6",
        "physical_quantum_qi_path_integral_reentry_intake_considered": True,
        "reentry_intake_decision": decision,
        "counts": counts,
        "blockers": [],
        "warnings": warnings or [],
        "boundary": dict(BOUNDARY),
    }


def run(root: pathlib.Path, name: str, value: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if value is not None:
        dump(runtime / "physical_quantum_qi_path_integral_reentry_intake_decision_packet.json", value)
    result = build_physical_quantum_qi_path_integral_reentry_intake_receipt_ledger(
        runtime_context=ctx(runtime),
        reentry_intake_receipt_ledger_license=license_packet,
    )
    ledger = read_jsonl(runtime / "physical_quantum_qi_path_integral_reentry_intake_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    assert ledger[-1]["boundary"]["receipt_ledger_only"] is True, label
    assert ledger[-1]["boundary"]["replayable_receipt"] is True, label
    assert ledger[-1]["boundary"]["does_not_execute_path"] is True, label
    assert ledger[-1]["boundary"]["does_not_authorize_execution"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, ledger = run(root, "accept", packet("accept"), lic())
        assert_ready("accept", out, ledger)
        assert out["intake_action"] == "reinforce_path_weight"
        assert ledger[-1]["next_cycle_candidate_potential"]["path_weight_delta"] == 3

        out, ledger = run(root, "hold", packet("hold"), lic())
        assert_ready("hold", out, ledger)
        assert out["intake_action"] == "open_probe_potential"
        assert ledger[-1]["next_cycle_candidate_potential"]["probe_potential_required"] is True

        out, ledger = run(root, "block", packet("block"), lic())
        assert_ready("block", out, ledger)
        assert out["intake_action"] == "add_barrier_potential"
        assert ledger[-1]["next_cycle_candidate_potential"]["barrier_blocks_ready_weight"] is True

        out, ledger = run(root, "chain", packet("accept"), lic())
        assert_ready("chain_1", out, ledger)
        out, ledger = run(root, "chain", packet("hold"), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        bad_accept = packet("accept")
        bad_accept["counts"]["reinforce_path_weight"] = 0
        out, ledger = run(root, "bad_accept", bad_accept, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_RECEIPT_LEDGER_BLOCKED"
        assert "accept_without_reinforce_path_weight" in out["blockers"]
        assert ledger == []

        bad_boundary = packet("accept")
        bad_boundary["boundary"]["does_not_authorize_execution"] = False
        out, ledger = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_RECEIPT_LEDGER_BLOCKED"
        assert "does_not_authorize_execution_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_RECEIPT_LEDGER_BLOCKED"
        assert "physical_quantum_qi_path_integral_reentry_intake_decision_packet_missing_or_invalid" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "license_block", packet("accept"), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_path_integral_reentry_intake_receipt_ledger_v10_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
