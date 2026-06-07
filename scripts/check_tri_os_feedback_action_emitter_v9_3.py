#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_tri_os_feedback_action_emitter_v9_3.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"tri_os_feedback_action_emitter_enabled": True, "apply_tri_os_feedback_action_emitter": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "TRI_OS_FEEDBACK_ACTION_EMITTER_LICENSE_READY", "feedback_packet_read_allowed": True, "memory_action_write_allowed": True, "plan_action_write_allowed": True, "run_governance_action_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def feedback(mem_mode: str = "open_next_stage", plan_mode: str = "open_next_stage", run_mode: str = "open_next_stage") -> dict[str, Any]:
    action = {
        "open_next_stage": {"MemoryOS": "open_append_only_recall_anchor", "PlanOS": "open_weighted_candidate_planning", "RunGovernance": "open_bounded_queue_gate"},
        "request_more_evidence": {"MemoryOS": "request_memory_reobserve_anchor", "PlanOS": "request_plan_redecomposition_evidence", "RunGovernance": "request_exit_blocker_review"},
        "quarantine_or_repair": {"MemoryOS": "quarantine_memory_handoff", "PlanOS": "block_plan_handoff_input", "RunGovernance": "block_governance_handoff_input"},
    }
    return {
        "version": "tri_os_intake_feedback_router_packet_v9_2",
        "tri_os_intake_feedback_considered": True,
        "feedback": {
            "MemoryOS": {"feedback_mode": mem_mode, "feedback_action": action.get(mem_mode, {}).get("MemoryOS", "bad"), "reason_window": {"recent_decisions": []}},
            "PlanOS": {"feedback_mode": plan_mode, "feedback_action": action.get(plan_mode, {}).get("PlanOS", "bad"), "reason_window": {"recent_decisions": []}},
            "RunGovernance": {"feedback_mode": run_mode, "feedback_action": action.get(run_mode, {}).get("RunGovernance", "bad"), "reason_window": {"recent_decisions": []}},
        },
        "boundary": {"feedback_only": True, "does_not_authorize_execution": True},
    }


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "tri_os_intake_feedback_router_packet.json", packet)
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
        load_json(runtime / "memory_os_feedback_action_packet.json"),
        load_json(runtime / "plan_os_feedback_action_packet.json"),
        load_json(runtime / "run_governance_feedback_action_packet.json"),
    )


def assert_ready(case: str, code: int, out: dict[str, Any], mem: dict[str, Any], plan: dict[str, Any], run_packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "TRI_OS_FEEDBACK_ACTION_EMITTER_READY", case
    assert out["action_packets_written"] == 3, case
    assert not out["blockers"], case
    assert mem["boundary"]["does_not_overwrite_memory"] is True, case
    assert plan["boundary"]["does_not_commit_plan"] is True, case
    assert run_packet["boundary"]["does_not_run_runner"] is True, case
    assert run_packet["boundary"]["does_not_authorize_execution"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, mem, plan, run_packet = run(root, "all_open", feedback(), lic())
        assert_ready("all_open", code, out, mem, plan, run_packet)
        assert mem["action_payload"]["memory_operation"] == "append_recall_anchor_candidate"
        assert plan["action_payload"]["plan_operation"] == "open_weighted_candidate_front"
        assert run_packet["action_payload"]["run_governance_operation"] == "open_bounded_queue_gate_candidate"

        code, out, mem, plan, run_packet = run(root, "mixed", feedback("request_more_evidence", "quarantine_or_repair", "open_next_stage"), lic())
        assert_ready("mixed", code, out, mem, plan, run_packet)
        assert mem["action_payload"]["memory_operation"] == "reobserve_memory_anchor"
        assert plan["action_payload"]["plan_operation"] == "quarantine_plan_handoff"
        assert run_packet["action_payload"]["run_governance_operation"] == "open_bounded_queue_gate_candidate"

        code, out, mem, plan, run_packet = run(root, "missing", None, lic())
        assert code == 1
        assert "tri_os_intake_feedback_router_packet_missing_or_invalid" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}

        bad = feedback()
        bad["tri_os_intake_feedback_considered"] = False
        code, out, mem, plan, run_packet = run(root, "bad_considered", bad, lic())
        assert code == 1
        assert "tri_os_intake_feedback_considered_not_true" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}

        bad_mode = feedback("bad_mode", "open_next_stage", "open_next_stage")
        code, out, mem, plan, run_packet = run(root, "bad_mode", bad_mode, lic())
        assert code == 1
        assert "memoryos_feedback_mode_invalid" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}

        code, out, mem, plan, run_packet = run(root, "license_block", feedback(), lic(plan_action_write_allowed=False))
        assert code == 1
        assert "plan_action_write_not_allowed" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}
    print("tri_os_feedback_action_emitter_v9_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
