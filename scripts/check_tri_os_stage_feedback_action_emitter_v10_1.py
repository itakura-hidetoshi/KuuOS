#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_tri_os_stage_feedback_action_emitter_v10_1.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"tri_os_stage_feedback_action_emitter_enabled": True, "apply_tri_os_stage_feedback_action_emitter": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "TRI_OS_STAGE_FEEDBACK_ACTION_EMITTER_LICENSE_READY", "stage_feedback_packet_read_allowed": True, "memory_action_write_allowed": True, "plan_action_write_allowed": True, "run_governance_action_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def feedback(mem: str = "final_stage_candidate", plan: str = "final_stage_candidate", run: str = "final_stage_candidate") -> dict[str, Any]:
    action = {
        "MemoryOS": {"final_stage_candidate": "stage_ready_recall_anchor_candidate", "stage_evidence_request": "request_memory_stage_evidence", "stage_repair_quarantine": "repair_memory_stage_quarantine"},
        "PlanOS": {"final_stage_candidate": "stage_ready_weighted_candidate_front", "stage_evidence_request": "request_plan_stage_evidence", "stage_repair_quarantine": "repair_plan_stage_quarantine"},
        "RunGovernance": {"final_stage_candidate": "stage_ready_bounded_queue_gate", "stage_evidence_request": "request_run_governance_stage_evidence", "stage_repair_quarantine": "repair_run_governance_stage_quarantine"},
    }
    return {
        "version": "tri_os_stage_intake_feedback_router_packet_v10_0",
        "tri_os_stage_intake_feedback_considered": True,
        "feedback": {
            "MemoryOS": {"stage_feedback_mode": mem, "stage_feedback_action": action["MemoryOS"].get(mem, "bad"), "history": {}},
            "PlanOS": {"stage_feedback_mode": plan, "stage_feedback_action": action["PlanOS"].get(plan, "bad"), "history": {}},
            "RunGovernance": {"stage_feedback_mode": run, "stage_feedback_action": action["RunGovernance"].get(run, "bad"), "history": {}},
        },
        "boundary": {"stage_feedback_only": True, "does_not_authorize_execution": True},
    }


def run_case(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "tri_os_stage_intake_feedback_router_packet.json", packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return (
        done.returncode,
        load_json(op),
        load_json(runtime / "memory_os_stage_feedback_action_packet.json"),
        load_json(runtime / "plan_os_stage_feedback_action_packet.json"),
        load_json(runtime / "run_governance_stage_feedback_action_packet.json"),
    )


def assert_ready(case: str, code: int, out: dict[str, Any], mem: dict[str, Any], plan: dict[str, Any], run_packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "TRI_OS_STAGE_FEEDBACK_ACTION_EMITTER_READY", case
    assert out["action_packets_written"] == 3, case
    assert not out["blockers"], case
    assert mem["boundary"]["does_not_overwrite_memory"] is True, case
    assert plan["boundary"]["does_not_commit_plan"] is True, case
    assert run_packet["boundary"]["does_not_run_runner"] is True, case
    assert run_packet["boundary"]["does_not_authorize_execution"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, mem, plan, run_packet = run_case(root, "all_final", feedback(), lic())
        assert_ready("all_final", code, out, mem, plan, run_packet)
        assert mem["action_payload"]["final_candidate_allowed"] is True
        assert plan["action_payload"]["final_candidate_allowed"] is True
        assert run_packet["action_payload"]["final_candidate_allowed"] is True

        code, out, mem, plan, run_packet = run_case(root, "mixed", feedback("stage_evidence_request", "stage_repair_quarantine", "final_stage_candidate"), lic())
        assert_ready("mixed", code, out, mem, plan, run_packet)
        assert mem["action_payload"]["evidence_request_required"] is True
        assert plan["action_payload"]["repair_quarantine_required"] is True
        assert plan["boundary"]["repair_quarantine_blocks_final_candidate"] is True
        assert run_packet["action_payload"]["final_candidate_allowed"] is True

        code, out, mem, plan, run_packet = run_case(root, "missing", None, lic())
        assert code == 1
        assert "tri_os_stage_intake_feedback_router_packet_missing_or_invalid" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}

        bad = feedback()
        bad["tri_os_stage_intake_feedback_considered"] = False
        code, out, mem, plan, run_packet = run_case(root, "bad_considered", bad, lic())
        assert code == 1
        assert "tri_os_stage_intake_feedback_considered_not_true" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}

        bad_mode = feedback("bad", "final_stage_candidate", "final_stage_candidate")
        code, out, mem, plan, run_packet = run_case(root, "bad_mode", bad_mode, lic())
        assert code == 1
        assert "memoryos_stage_feedback_mode_invalid" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}

        code, out, mem, plan, run_packet = run_case(root, "license_block", feedback(), lic(run_governance_action_write_allowed=False))
        assert code == 1
        assert "run_governance_action_write_not_allowed" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}
    print("tri_os_stage_feedback_action_emitter_v10_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
