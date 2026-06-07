#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_tri_os_readiness_stage_intake_validator_v9_8.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"tri_os_readiness_stage_intake_validator_enabled": True, "apply_tri_os_readiness_stage_intake_validator": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "TRI_OS_READINESS_STAGE_INTAKE_VALIDATOR_LICENSE_READY", "stage_packets_read_allowed": True, "stage_intake_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def memory(overwrite: bool = False, append: bool = True, action: str = "stage_append_only_recall_anchor") -> dict[str, Any]:
    return {"version": "tri_os_readiness_stage_packet_v9_7", "target_os": "MemoryOS", "readiness": "ready", "stage_mode": "stage_candidate", "next_stage_action": action, "stage_payload": {"memory_stage": action, "append_only_required": append, "allow_overwrite": overwrite}, "boundary": {"stage_packet_only": True, "does_not_consume_memory": True, "does_not_overwrite_memory": True, "append_only_memory_required": True, "does_not_authorize_execution": True}}


def plan(commit: bool = False, authority: str = "advisory_only", stage: str = "stage_weighted_candidate_front") -> dict[str, Any]:
    return {"version": "tri_os_readiness_stage_packet_v9_7", "target_os": "PlanOS", "readiness": "ready", "stage_mode": "stage_candidate", "next_stage_action": stage, "stage_payload": {"plan_stage": stage, "candidate_weighting_authority": authority, "commit_allowed": commit}, "boundary": {"stage_packet_only": True, "does_not_commit_plan": True, "candidate_weighting_not_truth": True, "does_not_authorize_execution": True}}


def run_gov(run_allowed: bool = False, queue: bool = True, exit_gate: bool = True, stage: str = "stage_bounded_queue_gate_candidate") -> dict[str, Any]:
    return {"version": "tri_os_readiness_stage_packet_v9_7", "target_os": "RunGovernance", "readiness": "ready", "stage_mode": "stage_candidate", "next_stage_action": stage, "stage_payload": {"run_governance_stage": stage, "queue_gate_required": queue, "exit_gate_required": exit_gate, "run_allowed": run_allowed}, "boundary": {"stage_packet_only": True, "does_not_run_runner": True, "queue_gate_required": True, "exit_gate_required": True, "does_not_authorize_execution": True}}


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
    return done.returncode, load_json(op), load_json(runtime / "tri_os_readiness_stage_intake_decision_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "TRI_OS_READINESS_STAGE_INTAKE_VALIDATOR_READY", case
    assert out["stage_intake_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["tri_os_readiness_stage_intake_considered"] is True, case
    assert packet["boundary"]["fail_closed_on_boundary_loss"] is True, case
    assert packet["boundary"]["does_not_authorize_execution"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"memory_os_readiness_stage_packet.json": memory(), "plan_os_readiness_stage_packet.json": plan(), "run_governance_readiness_stage_packet.json": run_gov()}
        code, out, packet = run(root, "all_accept", files, lic())
        assert_ready("all_accept", code, out, packet)
        assert out["memory_stage_decision"] == "accept"
        assert out["plan_stage_decision"] == "accept"
        assert out["run_governance_stage_decision"] == "accept"

        warn_files = {"memory_os_readiness_stage_packet.json": memory(append=False), "plan_os_readiness_stage_packet.json": plan(stage=""), "run_governance_readiness_stage_packet.json": run_gov(queue=False, exit_gate=False)}
        code, out, packet = run(root, "holds", warn_files, lic())
        assert_ready("holds", code, out, packet)
        assert out["memory_stage_decision"] == "hold"
        assert out["plan_stage_decision"] == "hold"
        assert out["run_governance_stage_decision"] == "hold"

        bad_files = {"memory_os_readiness_stage_packet.json": memory(overwrite=True), "plan_os_readiness_stage_packet.json": plan(commit=True, authority="commit"), "run_governance_readiness_stage_packet.json": run_gov(run_allowed=True)}
        code, out, packet = run(root, "blocks", bad_files, lic())
        assert_ready("blocks", code, out, packet)
        assert out["memory_stage_decision"] == "block"
        assert out["plan_stage_decision"] == "block"
        assert out["run_governance_stage_decision"] == "block"
        assert "memory_stage_overwrite_attempt" in packet["decisions"]["MemoryOS"]["blockers"]
        assert "plan_stage_commit_attempt" in packet["decisions"]["PlanOS"]["blockers"]
        assert "run_governance_stage_run_attempt" in packet["decisions"]["RunGovernance"]["blockers"]

        repair = memory()
        repair["readiness"] = "repair_required"
        repair["boundary"]["repair_required_blocks_ready_state"] = False
        code, out, packet = run(root, "bad_repair_boundary", {"memory_os_readiness_stage_packet.json": repair, "plan_os_readiness_stage_packet.json": plan(), "run_governance_readiness_stage_packet.json": run_gov()}, lic())
        assert_ready("bad_repair_boundary", code, out, packet)
        assert out["memory_stage_decision"] == "block"
        assert "memoryos_repair_ready_block_boundary_missing" in packet["decisions"]["MemoryOS"]["blockers"]

        code, out, packet = run(root, "missing", {}, lic())
        assert_ready("missing", code, out, packet)
        assert out["memory_stage_decision"] == "block"
        assert out["plan_stage_decision"] == "block"
        assert out["run_governance_stage_decision"] == "block"

        code, out, packet = run(root, "license_block", files, lic(stage_intake_packet_write_allowed=False))
        assert code == 1
        assert "stage_intake_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("tri_os_readiness_stage_intake_validator_v9_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
