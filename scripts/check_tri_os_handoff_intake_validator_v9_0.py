#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_tri_os_handoff_intake_validator_v9_0.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"tri_os_handoff_intake_validator_enabled": True, "apply_tri_os_handoff_intake_validator": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "TRI_OS_HANDOFF_INTAKE_VALIDATOR_LICENSE_READY", "handoff_packets_read_allowed": True, "intake_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def memory(fit: str = "high", visible: bool = True) -> dict[str, Any]:
    return {"version": "memory_os_qi_process_tensor_handoff_packet_v8_9", "target_os": "MemoryOS", "route_fit": fit, "handoff_kind": "process_tensor_recall_anchor", "recall_anchor": {"non_markov_history_visible": visible}, "boundary": {"does_not_overwrite_memory": True, "does_not_create_memory_authority": True}}


def plan(fit: str = "high", dominant: str = "light_progress") -> dict[str, Any]:
    return {"version": "plan_os_physical_quantum_qi_handoff_packet_v8_9", "target_os": "PlanOS", "route_fit": fit, "handoff_kind": "weighted_candidate_paths", "plan_candidates": {"dominant_path": dominant}, "boundary": {"candidate_weighting_not_truth": True, "advisory_plan_input_only": True, "does_not_authorize_execution": True}}


def run_gov(exit_visible: bool = True, queue_visible: bool = True) -> dict[str, Any]:
    return {"version": "run_governance_qi_que_handoff_packet_v8_9", "target_os": "RunGovernance", "route_fit": "high", "handoff_kind": "bounded_queue_exit_control", "governance_candidate": {"exit_gate_visible": exit_visible, "queued_bounded_execution": queue_visible}, "boundary": {"queue_gate_required": True, "exit_gate_required": True, "blocker_visibility_required": True, "does_not_authorize_execution": True}}


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
    return done.returncode, load_json(op), load_json(runtime / "tri_os_handoff_intake_decision_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "TRI_OS_HANDOFF_INTAKE_VALIDATOR_READY", case
    assert out["intake_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["tri_os_handoff_intake_considered"] is True, case
    assert packet["boundary"]["fail_closed_on_boundary_loss"] is True, case
    assert packet["boundary"]["does_not_authorize_execution"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {
            "memory_os_qi_process_tensor_handoff_packet.json": memory(),
            "plan_os_physical_quantum_qi_handoff_packet.json": plan(),
            "run_governance_qi_que_handoff_packet.json": run_gov(),
        }
        code, out, packet = run(root, "all_accept", files, lic())
        assert_ready("all_accept", code, out, packet)
        assert out["memory_decision"] == "accept"
        assert out["plan_decision"] == "accept"
        assert out["run_governance_decision"] == "accept"

        warn_files = {
            "memory_os_qi_process_tensor_handoff_packet.json": memory("high", False),
            "plan_os_physical_quantum_qi_handoff_packet.json": plan("high", ""),
            "run_governance_qi_que_handoff_packet.json": run_gov(False, False),
        }
        code, out, packet = run(root, "holds", warn_files, lic())
        assert_ready("holds", code, out, packet)
        assert out["memory_decision"] == "hold"
        assert out["plan_decision"] == "hold"
        assert out["run_governance_decision"] == "hold"

        bad_plan = plan()
        bad_plan["boundary"]["does_not_authorize_execution"] = False
        code, out, packet = run(root, "plan_block", {"memory_os_qi_process_tensor_handoff_packet.json": memory(), "plan_os_physical_quantum_qi_handoff_packet.json": bad_plan, "run_governance_qi_que_handoff_packet.json": run_gov()}, lic())
        assert_ready("plan_block", code, out, packet)
        assert out["memory_decision"] == "accept"
        assert out["plan_decision"] == "block"
        assert out["run_governance_decision"] == "accept"
        assert "plan_execution_boundary_missing" in packet["decisions"]["PlanOS"]["blockers"]

        code, out, packet = run(root, "missing_run", {"memory_os_qi_process_tensor_handoff_packet.json": memory(), "plan_os_physical_quantum_qi_handoff_packet.json": plan()}, lic())
        assert_ready("missing_run", code, out, packet)
        assert out["run_governance_decision"] == "block"
        assert "run_governance_handoff_missing" in packet["decisions"]["RunGovernance"]["blockers"]

        code, out, packet = run(root, "license_block", files, lic(intake_packet_write_allowed=False))
        assert code == 1
        assert "intake_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("tri_os_handoff_intake_validator_v9_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
