#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_tri_os_feedback_action_intake_validator_v9_4.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"tri_os_feedback_action_intake_validator_enabled": True, "apply_tri_os_feedback_action_intake_validator": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "TRI_OS_FEEDBACK_ACTION_INTAKE_VALIDATOR_LICENSE_READY", "action_packets_read_allowed": True, "action_intake_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def memory(overwrite: bool = False, operation: str = "append_recall_anchor_candidate") -> dict[str, Any]:
    return {"version": "tri_os_feedback_action_packet_v9_3", "target_os": "MemoryOS", "feedback_mode": "open_next_stage", "feedback_action": "open_append_only_recall_anchor", "action_payload": {"memory_operation": operation, "allow_overwrite": overwrite}, "boundary": {"action_packet_only": True, "does_not_consume_memory": True, "does_not_overwrite_memory": True, "append_only_memory_required": True, "does_not_authorize_execution": True}}


def plan(authority: str = "advisory_only", operation: str = "open_weighted_candidate_front") -> dict[str, Any]:
    return {"version": "tri_os_feedback_action_packet_v9_3", "target_os": "PlanOS", "feedback_mode": "open_next_stage", "feedback_action": "open_weighted_candidate_planning", "action_payload": {"plan_operation": operation, "candidate_weighting_authority": authority}, "boundary": {"action_packet_only": True, "does_not_commit_plan": True, "candidate_weighting_not_truth": True, "does_not_authorize_execution": True}}


def run_gov(queue: bool = True, exit_gate: bool = True, allow_run: bool = False) -> dict[str, Any]:
    return {"version": "tri_os_feedback_action_packet_v9_3", "target_os": "RunGovernance", "feedback_mode": "open_next_stage", "feedback_action": "open_bounded_queue_gate", "action_payload": {"run_governance_operation": "open_bounded_queue_gate_candidate", "queue_gate_required": queue, "exit_gate_required": exit_gate}, "boundary": {"action_packet_only": True, "does_not_run_runner": not allow_run, "queue_gate_required": True, "exit_gate_required": True, "does_not_authorize_execution": True}}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    for file_name, payload in files.items():
        dump(runtime / file_name, payload)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "tri_os_feedback_action_intake_decision_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "TRI_OS_FEEDBACK_ACTION_INTAKE_VALIDATOR_READY", case
    assert out["action_intake_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["tri_os_feedback_action_intake_considered"] is True, case
    assert packet["boundary"]["fail_closed_on_boundary_loss"] is True, case
    assert packet["boundary"]["does_not_authorize_execution"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"memory_os_feedback_action_packet.json": memory(), "plan_os_feedback_action_packet.json": plan(), "run_governance_feedback_action_packet.json": run_gov()}
        code, out, packet = run(root, "all_accept", files, lic())
        assert_ready("all_accept", code, out, packet)
        assert out["memory_action_decision"] == "accept"
        assert out["plan_action_decision"] == "accept"
        assert out["run_governance_action_decision"] == "accept"

        warn_files = {"memory_os_feedback_action_packet.json": memory(operation=""), "plan_os_feedback_action_packet.json": plan(operation=""), "run_governance_feedback_action_packet.json": run_gov(queue=False, exit_gate=False)}
        code, out, packet = run(root, "holds", warn_files, lic())
        assert_ready("holds", code, out, packet)
        assert out["memory_action_decision"] == "hold"
        assert out["plan_action_decision"] == "hold"
        assert out["run_governance_action_decision"] == "hold"

        bad_files = {"memory_os_feedback_action_packet.json": memory(overwrite=True), "plan_os_feedback_action_packet.json": plan(authority="commit"), "run_governance_feedback_action_packet.json": run_gov(allow_run=True)}
        code, out, packet = run(root, "blocks", bad_files, lic())
        assert_ready("blocks", code, out, packet)
        assert out["memory_action_decision"] == "block"
        assert out["plan_action_decision"] == "block"
        assert out["run_governance_action_decision"] == "block"
        assert "memory_overwrite_attempt" in packet["decisions"]["MemoryOS"]["blockers"]
        assert "plan_candidate_authority_leak" in packet["decisions"]["PlanOS"]["blockers"]
        assert "run_governance_runner_boundary_missing" in packet["decisions"]["RunGovernance"]["blockers"]

        code, out, packet = run(root, "missing", {}, lic())
        assert_ready("missing", code, out, packet)
        assert out["memory_action_decision"] == "block"
        assert out["plan_action_decision"] == "block"
        assert out["run_governance_action_decision"] == "block"

        code, out, packet = run(root, "license_block", files, lic(action_intake_packet_write_allowed=False))
        assert code == 1
        assert "action_intake_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("tri_os_feedback_action_intake_validator_v9_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
